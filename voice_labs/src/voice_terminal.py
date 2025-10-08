from builtins import print, len, str, Exception, ValueError
import os
import json
import base64
import asyncio
import azure.cognitiveservices.speech as speechsdk
import threading
import time
import concurrent.futures
import aiohttp
from collections import deque
from system_prompt import system_message
from dotenv import load_dotenv

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

def synthesize_speech_azure_sdk(text, language="hi-IN"):
    """Convert text to speech using Azure Speech SDK - optimized version with fast speech rate."""
    try:
        # Use Hindi voice for single language support
        voice_name = "hi-IN-SwaraNeural"
        
        tts_speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        tts_speech_config.speech_synthesis_voice_name = voice_name
        
        # Create audio config for direct speaker output
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=tts_speech_config, audio_config=audio_config)
        
        # Use SSML to control speech rate for faster speech
        ssml = f'''
        <speak version="1.0" xml:lang="hi-IN">
            <voice name="{voice_name}">
                <prosody rate="1.2" pitch="+3%">
                    {text}
                </prosody>
            </voice>
        </speak>
        '''
        
        result = synthesizer.speak_ssml_async(ssml).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ Azure Speech synthesis successful - audio played (fast pace)")
            return True
            
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speechsdk.CancellationDetails(result)
            print(f"❌ Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"❌ Error details: {cancellation_details.error_details}")
                if cancellation_details.error_details:
                    print(f"❌ Full error: {cancellation_details.error_details}")
            return False
        else:
            print(f"❌ Unexpected result reason: {result.reason}")
            return False
            
    except Exception as e:
        print(f"❌ Error with Azure Speech SDK TTS: {e}")
        import traceback
        traceback.print_exc()
        return False

def synthesize_speech_fallback(text, language="hi-IN"):
    """Fallback TTS method using system default audio."""
    try:
        # Use Hindi voice for single language support
        voice_name = "hi-IN-SwaraNeural"
        
        tts_speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        tts_speech_config.speech_synthesis_voice_name = voice_name
        
        # Try without audio config (let system handle default output)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=tts_speech_config)
        
        # Use simple text
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ Fallback TTS synthesis successful")
            return True
        else:
            print(f"❌ Fallback TTS failed: {result.reason}")
            return False
            
    except Exception as e:
        print(f"❌ Fallback TTS error: {e}")
        return False

async def synthesize_speech_azure(text, language="hi-IN"):
    """Async wrapper for Azure Speech SDK TTS with optimized thread pool and fallback."""
    loop = asyncio.get_event_loop()
    
    # Try primary method first
    success = await loop.run_in_executor(tts_executor, synthesize_speech_azure_sdk, text, language)
    
    # If primary method fails, try fallback
    if not success:
        print("🔄 Trying fallback TTS method...")
        success = await loop.run_in_executor(tts_executor, synthesize_speech_fallback, text, language)
    
    return success

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

class ContinuousSpeechRecognizer:
    """Continuous speech recognition with live transcription."""
    
    def __init__(self):
        self.recognizer = None
        self.is_listening = False
        self.current_transcription = ""
        self.final_result = None
        self.recognition_done = threading.Event()
        
    def setup_recognizer(self):
        """Setup the continuous speech recognizer."""
        try:
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            self.recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config, 
                auto_detect_source_language_config=auto_detect_source_language_config,
                audio_config=audio_config
            )
            
            # Connect callbacks for live transcription
            self.recognizer.recognizing.connect(self.on_recognizing)
            self.recognizer.recognized.connect(self.on_recognized)
            self.recognizer.session_stopped.connect(self.on_session_stopped)
            self.recognizer.canceled.connect(self.on_canceled)
            
            return True
        except Exception as e:
            print(f"❌ Error setting up recognizer: {e}")
            return False
    
    def on_recognizing(self, evt):
        """Called during recognition - shows live transcription."""
        if evt.result.text and evt.result.text != self.current_transcription:
            # Clear previous line and show current transcription
            print(f"\r🎤 Live: {evt.result.text}", end="", flush=True)
            self.current_transcription = evt.result.text
    
    def on_recognized(self, evt):
        """Called when recognition is complete."""
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            if evt.result.text.strip():
                print(f"\r🗣️ Final: {evt.result.text}")
                self.final_result = evt.result.text.strip()
                self.stop_listening()
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("\r❌ No speech recognized")
            self.stop_listening()
    
    def on_session_stopped(self, evt):
        """Called when session stops."""
        print("\r🔇 Recognition session stopped")
        self.recognition_done.set()
    
    def on_canceled(self, evt):
        """Called when recognition is canceled."""
        print(f"\r❌ Recognition canceled: {evt.reason}")
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"❌ Error details: {evt.error_details}")
        self.recognition_done.set()
    
    def start_listening(self):
        """Start continuous listening."""
        if not self.setup_recognizer():
            return None
            
        self.is_listening = True
        self.final_result = None
        self.current_transcription = ""
        self.recognition_done.clear()
        
        print("🎤 Listening continuously... Speak now!")
        
        try:
            # Start continuous recognition
            self.recognizer.start_continuous_recognition_async()
            
            # Wait for recognition to complete (no timeout)
            self.recognition_done.wait()
            return self.final_result
                
        except Exception as e:
            print(f"\r❌ Error during recognition: {e}")
            return None
    
    def stop_listening(self):
        """Stop continuous listening."""
        if self.recognizer and self.is_listening:
            try:
                self.recognizer.stop_continuous_recognition_async()
                self.is_listening = False
            except Exception as e:
                print(f"❌ Error stopping recognition: {e}")

# Global recognizer instance
continuous_recognizer = ContinuousSpeechRecognizer()

async def main_voice_loop():
    """Main voice interaction loop with continuous recognition."""
    print("🔥 Starting AI Voice Bot Terminal...")
    print("🎤 Continuous Voice Bot - Speak anytime! Type 'quit' to exit or 'text' for text mode.")
    print("=" * 70)
    
    conversation_history = [{"role": "system", "content": SYSTEM_MESSAGE}]
    
    # Send initial greeting
    greeting = "Hello! I'm your AI voice assistant. I'm listening continuously - just start speaking!"
    print(f"🤖 AI: {greeting}")
    conversation_history.append({"role": "assistant", "content": greeting})
    
    # Play greeting audio
    await synthesize_speech_azure(greeting, "hi-IN")
    
    try:
        while True:
            print("\n" + "─" * 70)
            print("🎤 Ready to listen... (Type 'quit' to exit, 'text' for text input)")
            
            # Start continuous listening in a separate thread
            user_text = None
            
            # Use a simple approach - check for keyboard input while listening
            try:
                # Start listening for voice
                user_text = continuous_recognizer.start_listening()
                
                # Check if user wants to quit or use text mode
                if user_text and user_text.lower().strip() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("👋 Goodbye!")
                    break
                    
            except KeyboardInterrupt:
                print("\n🎤 Listening interrupted. Type command:")
                user_input = input("Enter 'quit' to exit, 'text' for text input, or press Enter to continue: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'text':
                    # Text input mode
                    user_text = input("Type your message: ").strip()
                else:
                    # Continue listening
                    continue
            
            if user_text and user_text.strip():
                print(f"🗣️ You said: {user_text}")
                
                # Add user message to conversation
                conversation_history.append({"role": "user", "content": user_text})
                
                # Get AI response
                print("🤖 Thinking...")
                ai_response = await get_azure_openai_response(conversation_history)
                print(f"🤖 AI: {ai_response}")
                
                # Add AI response to conversation
                conversation_history.append({"role": "assistant", "content": ai_response})
                
                # Generate TTS for AI response
                print("🔊 Speaking...")
                await synthesize_speech_azure(ai_response, "hi-IN")
                
            else:
                print("❌ No speech detected. Continuing to listen...")
                
    except KeyboardInterrupt:
        print("\n👋 Voice bot interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ Error in main loop: {e}")
    finally:
        # Cleanup
        continuous_recognizer.stop_listening()
        await http_manager.close()
        tts_executor.shutdown(wait=False)

if __name__ == "__main__":
    print("🔥 Starting Terminal AI Voice Bot...")
    
    # Windows-specific optimizations
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        print("🪟 Windows optimizations applied")
    
    # Run the main voice loop
    asyncio.run(main_voice_loop())
