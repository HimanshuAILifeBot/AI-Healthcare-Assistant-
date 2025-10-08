from builtins import print,len,str,Exception,ValueError
import os
import json
import base64
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import uvicorn
import azure.cognitiveservices.speech as speechsdk
import threading
import time
import concurrent.futures
import aiohttp
from collections import deque
from system_prompt import system_message

load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')

# Azure Speech Configuration
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')


SYSTEM_MESSAGE = system_message

# HTTP Session Manager for Azure OpenAI calls
class HTTPSessionManager:
    def __init__(self):
        self._session = None
        
    async def get_session(self):
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=30,
                keepalive_timeout=30,
                enable_cleanup_closed=True,
                ttl_dns_cache=300
            )
            timeout = aiohttp.ClientTimeout(
                total=6,
                connect=2,
                sock_read=4
            )
            self._session = aiohttp.ClientSession(
                connector=connector, 
                timeout=timeout
            )
        return self._session
    
    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

http_manager = HTTPSessionManager()

# Response Cache for TTS
class ResponseCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.access_order = deque()
        self.max_size = max_size
    
    def get(self, key):
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def set(self, key, value):
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            lru_key = self.access_order.popleft()
            del self.cache[lru_key]
        
        self.cache[key] = value
        self.access_order.append(key)

response_cache = ResponseCache()

# Thread Pool for TTS operations
tts_executor = concurrent.futures.ThreadPoolExecutor(
    max_workers=6,
    thread_name_prefix="TTS"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI app startup and shutdown."""
    print("🚀 Voice Bot Server starting up...")
    
    yield
    
    print("🔄 Server shutting down...")
    await http_manager.close()
    tts_executor.shutdown(wait=False)

app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validation
if not AZURE_OPENAI_API_KEY:
    raise ValueError('Missing Azure OpenAI API key. Please set AZURE_OPENAI_API_KEY in the .env file for GenAI functionality.')
if not AZURE_OPENAI_ENDPOINT:
    raise ValueError('Missing Azure OpenAI endpoint. Please set AZURE_OPENAI_ENDPOINT in the .env file.')
if not AZURE_SPEECH_KEY:
    raise ValueError('Missing Azure Speech key. Please set AZURE_SPEECH_KEY in the .env file.')

# Initialize Azure Speech Config with optimizations
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
speech_config.speech_recognition_language = "hi-IN"

# Optimized speech settings
speech_config.set_property(speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, "800")
speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "600")
speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "3000")
speech_config.enable_dictation()

# Multi-language recognition
auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
    languages=["hi-IN", "en-IN", "en-US"]
)

@app.get("/")
async def index_page():
    return {
        "message": "AI Voice Bot API Server",
        "status": "running",
        "endpoints": {
            "websocket": "/voice-chat",
            "frontend": "Open frontend/index.html in your browser"
        },
        "version": "2.0.0"
    }


def synthesize_speech_azure_sdk(text, language="hi-IN"):
    """Convert text to speech using Azure Speech SDK - optimized version."""
    try:
        # Check cache first
        cache_key = f"{text}:{language}"
        cached_audio = response_cache.get(cache_key)
        if cached_audio:
            print("🎯 Using cached TTS response")
            return cached_audio
        
        # Use Hindi voice for single language support
        voice_name = "hi-IN-SwaraNeural"
        
        tts_speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        tts_speech_config.speech_synthesis_voice_name = voice_name
        
        # Use standard audio format for web compatibility
        tts_speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )
        
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=tts_speech_config, audio_config=None)
        
        # Simplified SSML
        ssml = f'''
        <speak version="1.0" xml:lang="hi-IN">
            <voice name="{voice_name}">
                <prosody rate="1.3" pitch="+3%">
                    {text}
                </prosody>
            </voice>
        </speak>
        '''
        
        result = synthesizer.speak_ssml(ssml)
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_b64 = base64.b64encode(result.audio_data).decode('utf-8')
            # Cache the result
            response_cache.set(cache_key, audio_b64)
            print("✅ Azure Speech synthesis successful, cached")
            return audio_b64
            
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speechsdk.CancellationDetails(result)
            print(f"❌ Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"❌ Error details: {cancellation_details.error_details}")
            return None
            
    except Exception as e:
        print(f"❌ Error with Azure Speech SDK TTS: {e}")
        return None

async def synthesize_speech_azure(text, language="hi-IN"):
    """Async wrapper for Azure Speech SDK TTS with optimized thread pool."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(tts_executor, synthesize_speech_azure_sdk, text, language)

async def get_azure_openai_response(messages):
    """Get response from Azure OpenAI with optimized settings."""
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }
    
    data = {
        "messages": messages,
        "max_tokens": 100,
        "temperature": 0.5,
        "top_p": 0.8,
        "stream": False
    }
    
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={OPENAI_API_VERSION}"
    
    try:
        session = await http_manager.get_session()
        async with session.post(url, headers=headers, json=data) as response:
            result = await response.json()
            
            if 'error' in result:
                print(f"❌ Azure OpenAI API Error: {result['error']}")
                return "I'm sorry, I'm experiencing technical difficulties. Please try again."
            
            if 'choices' not in result or not result['choices']:
                print(f"❌ Unexpected response structure: {result}")
                return "I'm sorry, I'm having trouble understanding. Please repeat."
            
            return result['choices'][0]['message']['content']
                
    except Exception as e:
        print(f"❌ Error calling Azure OpenAI API: {e}")
        return "I'm sorry, I'm experiencing technical difficulties. Please contact us again later."



@app.websocket("/voice-chat")
async def handle_voice_chat(websocket: WebSocket):
    """Simple WebSocket handler for direct voice chat."""
    print("🎤 Client connected to voice chat")
    await websocket.accept()
    
    conversation_history = [{"role": "system", "content": SYSTEM_MESSAGE}]
    
    try:
        # Send initial greeting
        greeting = "Hello! I'm your AI voice assistant. How can I help you today?"
        conversation_history.append({"role": "assistant", "content": greeting})
        
        # Generate TTS for greeting
        audio_data = await synthesize_speech_azure(greeting, "hi-IN")
        if audio_data:
            await websocket.send_json({
                "type": "audio_response",
                "audio_data": audio_data,
                "text": greeting
            })
        
        async for message in websocket.iter_text():
            try:
                data = json.loads(message)
                
                if data.get("type") == "user_text":
                    user_text = data.get("text", "").strip()
                    if user_text:
                        print(f"🗣️ User said: {user_text}")
                        
                        # Add user message to conversation
                        conversation_history.append({"role": "user", "content": user_text})
                        
                        # Get AI response
                        ai_response = await get_azure_openai_response(conversation_history)
                        print(f"🤖 AI Response: {ai_response}")
                        
                        # Add AI response to conversation
                        conversation_history.append({"role": "assistant", "content": ai_response})
                        
                        # Generate TTS for AI response
                        audio_data = await synthesize_speech_azure(ai_response, "hi-IN")
                        
                        # Send response back to client
                        await websocket.send_json({
                            "type": "audio_response",
                            "audio_data": audio_data,
                            "text": ai_response
                        })
                        
            except json.JSONDecodeError:
                print("❌ Invalid JSON received")
            except Exception as e:
                print(f"❌ Error processing message: {e}")
                
    except WebSocketDisconnect:
        print("🔌 Client disconnected from voice chat")

if __name__ == "__main__":
    print("🔥 Starting Simple AI Voice Bot Server...")
    print("🌐 Server will be available at http://localhost:8000")
    print("🌐 WebSocket endpoint: ws://localhost:8000/voice-chat")
    
    # Windows-specific optimizations
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        print("🪟 Windows optimizations applied")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        workers=1,
        access_log=False,
        log_level="info",
        reload=False,
        use_colors=True
    )
