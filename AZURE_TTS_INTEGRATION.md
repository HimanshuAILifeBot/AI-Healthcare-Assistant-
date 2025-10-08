# Azure TTS Integration - Implementation Guide

## Overview
This document describes the Azure Text-to-Speech (TTS) integration that replaces the browser's Web Speech API with high-quality Azure Cognitive Services Speech.

## Changes Made

### 1. Backend Changes

#### New Files:
- **`backend/azure_tts.py`**: Core Azure TTS module
  - Implements `synthesize_speech_azure()` for async TTS generation
  - Includes LRU caching for improved performance
  - Thread pool executor for non-blocking operations
  - SSML support for better speech control
  - Multi-language support (English, Hindi, etc.)

- **`backend/test_azure_tts.py`**: Test script for Azure TTS
  - Verifies Azure credentials are configured correctly
  - Tests multiple languages and voices
  - Validates caching functionality

#### Modified Files:
- **`backend/main.py`**:
  - Added `/tts` endpoint for TTS requests
  - Imported Azure TTS functions
  - Added TTSRequest model import

- **`backend/models.py`**:
  - Added `TTSRequest` model with fields:
    - `text`: The text to convert to speech
    - `language`: Language code (default: "en-US")
    - `voice_name`: Optional specific voice name

- **`backend/config.py`**:
  - Added `AZURE_SPEECH_KEY` configuration
  - Added `AZURE_SPEECH_REGION` configuration

- **`backend/requirements.txt`**:
  - Added `azure-cognitiveservices-speech`
  - Added `aiohttp` for async HTTP support

- **`backend/.env.example`**:
  - Added Azure Speech credentials template

### 2. Frontend Changes

#### Modified Files:
- **`src/context/UserContext.jsx`**:
  - Replaced browser's `SpeechSynthesisUtterance` with Azure TTS API calls
  - Added `audioRef` for playing Azure-generated audio
  - Added `base64ToBlob()` helper function to convert base64 audio data
  - Added `fallbackSpeak()` function for graceful degradation
  - Updated `speak()` function to:
    - Call backend `/tts` endpoint
    - Play Azure-generated audio
    - Fallback to browser TTS if Azure fails
  - Updated `disconnect()` to stop Azure audio playback

## Setup Instructions

### 1. Azure Prerequisites
1. Create an Azure account at https://azure.microsoft.com
2. Create a Speech Service resource:
   - Go to Azure Portal
   - Create a new "Speech Services" resource
   - Note your **API Key** and **Region**

### 2. Backend Configuration

1. **Install Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create/update `.env` file in the `backend` directory:
   ```bash
   # Existing variables...
   
   # Azure Speech Services for TTS
   AZURE_SPEECH_KEY=your_actual_azure_speech_key_here
   AZURE_SPEECH_REGION=your_azure_region_here  # e.g., eastus, westus2
   ```

3. **Test Azure TTS**:
   ```bash
   cd backend
   python test_azure_tts.py
   ```
   
   This should output:
   ```
   ✅ Success! Generated audio for all tests
   ✅ Azure TTS is configured correctly!
   ```

### 3. Run the Application

1. **Start Backend**:
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend**:
   ```bash
   npm run dev
   ```

3. **Test the Voice Assistant**:
   - Navigate to the Assistant page
   - Click "Start Voice Chat"
   - Speak to the assistant
   - Listen to Azure TTS responses (high-quality voice)

## Features

### Azure TTS Advantages:
1. **High-Quality Voices**: Natural-sounding neural voices
2. **Multi-Language Support**: English (US, GB, IN), Hindi, and more
3. **Caching**: Repeated phrases are cached for faster response
4. **SSML Support**: Fine control over speech parameters (rate, pitch, volume)
5. **Reliability**: Enterprise-grade service with 99.9% uptime SLA
6. **Fallback**: Gracefully falls back to browser TTS if Azure fails

### Supported Languages:
- `en-US`: English (United States) - Default
- `en-GB`: English (United Kingdom)
- `en-IN`: English (India)
- `hi-IN`: Hindi (India)

### Voice Customization:
You can specify custom voices in the frontend by modifying the TTS request:
```javascript
{
    text: "Your text here",
    language: "en-US",
    voice_name: "en-US-JennyNeural"  // Optional
}
```

## API Endpoints

### POST `/tts`
Convert text to speech using Azure TTS.

**Request Body**:
```json
{
    "text": "Hello, how can I help you?",
    "language": "en-US",
    "voice_name": null
}
```

**Response**:
```json
{
    "success": true,
    "audio_data": "base64_encoded_mp3_audio_data...",
    "text": "Hello, how can I help you?"
}
```

## Troubleshooting

### Issue: "Missing Azure Speech key" Error
**Solution**: Ensure `AZURE_SPEECH_KEY` is set in `backend/.env`

### Issue: "Missing Azure Speech region" Error
**Solution**: Ensure `AZURE_SPEECH_REGION` is set in `backend/.env`

### Issue: Audio not playing
**Solution**: 
1. Check browser console for errors
2. Verify backend is running and `/tts` endpoint is accessible
3. Test with `test_azure_tts.py` to ensure Azure credentials are valid

### Issue: Falls back to browser TTS
**Solution**: 
1. Check network connection to Azure
2. Verify Azure Speech Service is active in Azure Portal
3. Check backend logs for detailed error messages

## Performance Optimization

The implementation includes several optimizations:

1. **Caching**: LRU cache stores up to 100 recent TTS responses
2. **Thread Pool**: 6 worker threads handle TTS synthesis without blocking
3. **Async Operations**: Non-blocking I/O for better concurrency
4. **Audio Format**: MP3 at 16kHz for web compatibility and reasonable file size

## Cost Considerations

Azure Speech Services pricing:
- **Free Tier**: 0.5M characters per month
- **Standard**: $1 per 1M characters

For typical medical assistant usage (average 50 characters per response):
- Free tier: ~10,000 responses/month
- After free tier: $0.001 per response

## Migration Notes

### What Changed:
- **Before**: Browser's Web Speech API (client-side TTS)
- **After**: Azure Cognitive Services Speech (server-side TTS)

### Benefits:
- ✅ Higher quality, more natural voices
- ✅ Consistent voice across all browsers and devices
- ✅ Better language support and pronunciation
- ✅ Caching for improved performance
- ✅ Enterprise-grade reliability

### Backward Compatibility:
- The system gracefully falls back to browser TTS if:
  - Azure credentials are not configured
  - Azure service is unavailable
  - Network issues occur

## Future Enhancements

Possible improvements:
1. **Voice Selection**: Allow users to choose from multiple voices
2. **Speech Rate Control**: Let users adjust speaking speed
3. **Streaming TTS**: Stream audio for faster initial playback
4. **WebSocket TTS**: Real-time TTS over WebSocket for lower latency
5. **Custom Neural Voices**: Train custom voices for branded experience

## Support

For issues or questions:
1. Check Azure Speech Service status: https://status.azure.com
2. Review Azure Speech SDK documentation: https://learn.microsoft.com/azure/cognitive-services/speech-service/
3. Check application logs in backend terminal
4. Run `test_azure_tts.py` for diagnostic information
