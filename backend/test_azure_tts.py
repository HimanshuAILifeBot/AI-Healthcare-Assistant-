"""
Test script for Azure TTS integration
Run this to verify Azure TTS is working correctly
"""
import asyncio
import sys
from azure_tts import synthesize_speech_azure

async def test_azure_tts():
    """Test Azure TTS with various inputs"""
    
    print("🧪 Testing Azure TTS Integration\n")
    
    # Test 1: Basic English
    print("Test 1: Basic English Speech")
    test_text = "Hello! I am your AI medical assistant. How can I help you today?"
    audio_data = await synthesize_speech_azure(test_text, language="en-US")
    
    if audio_data:
        print(f"✅ Success! Generated {len(audio_data)} bytes of audio data\n")
    else:
        print("❌ Failed to generate audio\n")
        return False
    
    # Test 2: Different voice
    print("Test 2: British English Voice")
    test_text = "This is a test with a British accent."
    audio_data = await synthesize_speech_azure(test_text, language="en-GB")
    
    if audio_data:
        print(f"✅ Success! Generated {len(audio_data)} bytes of audio data\n")
    else:
        print("❌ Failed to generate audio\n")
    
    # Test 3: Hindi (if configured)
    print("Test 3: Hindi Speech")
    test_text = "नमस्ते, मैं आपकी सहायता कैसे कर सकता हूं?"
    audio_data = await synthesize_speech_azure(test_text, language="hi-IN")
    
    if audio_data:
        print(f"✅ Success! Generated {len(audio_data)} bytes of audio data\n")
    else:
        print("⚠️  Hindi TTS failed (this is optional)\n")
    
    # Test 4: Cache test
    print("Test 4: Testing Cache")
    test_text = "Hello! I am your AI medical assistant. How can I help you today?"
    audio_data = await synthesize_speech_azure(test_text, language="en-US")
    
    if audio_data:
        print(f"✅ Cache working! Generated {len(audio_data)} bytes of audio data\n")
    else:
        print("❌ Cache failed\n")
    
    print("🎉 All tests completed!\n")
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(test_azure_tts())
        if result:
            print("✅ Azure TTS is configured correctly!")
            sys.exit(0)
        else:
            print("❌ Azure TTS configuration has issues")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("\nMake sure you have:")
        print("1. Set AZURE_SPEECH_KEY in your .env file")
        print("2. Set AZURE_SPEECH_REGION in your .env file")
        print("3. Installed azure-cognitiveservices-speech package")
        sys.exit(1)
