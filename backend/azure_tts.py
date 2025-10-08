"""
Azure Text-to-Speech Service
Provides high-quality speech synthesis using Azure Cognitive Services
"""
import os
import base64
import asyncio
import concurrent.futures
import re
from collections import deque
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

# Azure Speech Configuration
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')

# Validate Azure credentials
if not AZURE_SPEECH_KEY:
    raise ValueError('Missing Azure Speech key. Please set AZURE_SPEECH_KEY in the .env file.')
if not AZURE_SPEECH_REGION:
    raise ValueError('Missing Azure Speech region. Please set AZURE_SPEECH_REGION in the .env file.')


# Response Cache for TTS
class ResponseCache:
    """LRU Cache for TTS responses to improve performance"""
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


# Global cache and thread pool
response_cache = ResponseCache()
tts_executor = concurrent.futures.ThreadPoolExecutor(
    max_workers=6,
    thread_name_prefix="AzureTTS"
)


def detect_language(text):
    """
    Detect if text is primarily Hindi or English.
    Returns language code and appropriate voice.
    """
    # Check for Devanagari script (Hindi)
    hindi_chars = re.findall(r'[\u0900-\u097F]', text)
    english_chars = re.findall(r'[a-zA-Z]', text)
    
    hindi_count = len(hindi_chars)
    english_count = len(english_chars)
    
    # If more than 30% Hindi characters, use Hindi voice
    if hindi_count > 0 and hindi_count > english_count * 0.3:
        return "hi-IN", "hi-IN-SwaraNeural"
    else:
        return "en-IN", "en-IN-NeerjaNeural"  # Use Indian English for better pronunciation


def synthesize_speech_azure_sdk(text, language=None, voice_name=None):
    """
    Convert text to speech using Azure Speech SDK with auto language detection.
    
    Args:
        text: The text to convert to speech
        language: Language code (e.g., "en-US", "hi-IN") - auto-detected if None
        voice_name: Specific Azure voice name (optional)
    
    Returns:
        Base64 encoded audio data or None on error
    """
    try:
        # Auto-detect language if not provided
        if not language or not voice_name:
            detected_lang, detected_voice = detect_language(text)
            language = language or detected_lang
            voice_name = voice_name or detected_voice
            print(f"🔍 Detected language: {language}, Using voice: {voice_name}")
        
        # Check cache first
        cache_key = f"{text}:{language}:{voice_name}"
        cached_audio = response_cache.get(cache_key)
        if cached_audio:
            print("🎯 Using cached TTS response")
            return cached_audio
        
        # Configure Azure Speech
        tts_speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_SPEECH_KEY, 
            region=AZURE_SPEECH_REGION
        )
        tts_speech_config.speech_synthesis_voice_name = voice_name
        
        # Set output format for web compatibility
        tts_speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )
        
        # Create synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=tts_speech_config, 
            audio_config=None
        )
        
        # Create SSML for better, more natural control (matching voice_labs settings)
        ssml = f'''
        <speak version="1.0" xml:lang="{language}">
            <voice name="{voice_name}">
                <prosody rate="1.3" pitch="+3%">
                    {text}
                </prosody>
            </voice>
        </speak>
        '''
        
        # Synthesize speech
        result = synthesizer.speak_ssml(ssml)
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # Convert to base64 for easy transport
            audio_b64 = base64.b64encode(result.audio_data).decode('utf-8')
            
            # Cache the result
            response_cache.set(cache_key, audio_b64)
            
            print(f"✅ Azure Speech synthesis successful: {len(text)} chars")
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


async def synthesize_speech_azure(text, language=None, voice_name=None):
    """
    Async wrapper for Azure Speech SDK TTS with auto language detection.
    
    Args:
        text: The text to convert to speech
        language: Language code (optional, auto-detected if None)
        voice_name: Specific Azure voice name (optional)
    
    Returns:
        Base64 encoded audio data or None on error
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        tts_executor, 
        synthesize_speech_azure_sdk, 
        text, 
        language,
        voice_name
    )


def shutdown_tts():
    """Cleanup function to shutdown the thread pool"""
    tts_executor.shutdown(wait=False)
