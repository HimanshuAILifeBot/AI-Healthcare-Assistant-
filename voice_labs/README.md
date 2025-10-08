# AI Voice Assistant with Separate Frontend

A modern AI voice assistant with separated frontend and backend architecture. The system provides Speech-to-Text (STT), Text-to-Speech (TTS), and Large Language Model (LLM) capabilities with a beautiful web interface.

## 🏗️ Architecture

```
Frontend (Port 3000)          Backend API (Port 8000)
┌─────────────────────┐      ┌──────────────────────┐
│  HTML/CSS/JS        │      │  FastAPI Server      │
│  - Voice Recognition│ ────►│  - WebSocket Handler │
│  - Audio Playback   │      │  - Azure OpenAI      │
│  - Modern UI        │      │  - Azure Speech      │
└─────────────────────┘      └──────────────────────┘
```

## ✨ Features

### Frontend Features
- **🎤 Voice Recognition**: Web Speech API for real-time voice input
- **🔊 Audio Playback**: Automatic playback of AI responses
- **🎨 Modern UI**: Beautiful gradient design with animations
- **⚙️ Settings Panel**: Customizable voice settings
- **📱 Responsive**: Works on desktop and mobile devices
- **🔄 Auto-reconnect**: Automatic WebSocket reconnection
- **⏹️ Stop Controls**: Stop recording, playback, or processing
- **📊 Visual Feedback**: Voice visualizer and status indicators

### Backend Features
- **🧠 LLM Integration**: Azure OpenAI for intelligent conversations
- **🗣️ Text-to-Speech**: Azure Speech Services with Hindi/English support
- **📡 WebSocket API**: Real-time bidirectional communication
- **💾 Response Caching**: TTS response caching for better performance
- **🔄 Async Processing**: Fully asynchronous for optimal performance
- **🌐 CORS Support**: Cross-origin requests enabled

## 🚀 Quick Start

### Option 1: Use the Batch Script (Windows)
```bash
# Double-click or run:
start_voice_assistant.bat
```

### Option 2: Manual Setup

1. **Start the Backend API**:
   ```bash
   python src/voice_bot.py
   ```

2. **Start the Frontend Server**:
   ```bash
   cd frontend
   python server.py
   ```

3. **Open your browser**: Navigate to `http://localhost:3000`

## 📋 Prerequisites

### Environment Variables
Create a `.env` file in the root directory:
```env
AZURE_OPENAI_API_KEY=your_openai_api_key
AZURE_OPENAI_ENDPOINT=your_openai_endpoint
OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_SPEECH_KEY=your_speech_key
AZURE_SPEECH_REGION=your_speech_region
```

### Dependencies
```bash
pip install -r requirements.txt
```

## 🎯 How to Use

1. **🌐 Open Frontend**: Navigate to `http://localhost:3000`
2. **🔗 Auto-Connect**: The app will automatically connect to the voice bot API
3. **🎤 Voice Input**: Click the microphone button to start voice recording
4. **⌨️ Text Input**: Or type your message in the text input field
5. **🔊 Listen**: AI responses will be played automatically
6. **⚙️ Customize**: Use the settings panel to adjust voice parameters

## 🎛️ Frontend Controls

- **🎤 Microphone Button**: Start/stop voice recording (green = ready, red = recording)
- **⏹️ Stop Button**: Stop all current actions (recording, playback, processing)
- **📝 Text Input**: Type messages manually
- **⚙️ Settings**: Adjust voice rate, pitch, volume, and behavior
- **🔄 Status Indicator**: Shows connection status (green = connected, red = disconnected)

## 🔧 API Endpoints

### HTTP Endpoints
- `GET /`: API information and status
- `WebSocket /voice-chat`: Real-time voice communication

### WebSocket Protocol

**Client → Server**:
```json
{
  "type": "user_text",
  "text": "Your message here"
}
```

**Server → Client**:
```json
{
  "type": "audio_response",
  "text": "AI response text",
  "audio_data": "base64_encoded_mp3_audio"
}
```

## 📁 Project Structure

```
├── src/
│   ├── voice_bot.py          # Backend API server
│   └── system_prompt.py      # AI system message
├── frontend/
│   ├── index.html           # Main HTML page
│   ├── styles.css           # Modern CSS styling
│   ├── script.js            # Frontend JavaScript logic
│   └── server.py            # Frontend HTTP server
├── requirements.txt         # Python dependencies
├── start_voice_assistant.bat # Windows batch script
└── README.md               # This file
```

## 🔧 Technical Details

### Frontend Stack
- **HTML5**: Semantic markup with modern features
- **CSS3**: Gradient backgrounds, animations, responsive design
- **Vanilla JavaScript**: No frameworks, pure ES6+ code
- **Web APIs**: Speech Recognition, Audio, WebSocket

### Backend Stack
- **FastAPI**: Modern Python web framework
- **Azure OpenAI**: GPT-4 for intelligent responses
- **Azure Speech Services**: Text-to-speech synthesis
- **WebSocket**: Real-time communication
- **Async/Await**: Non-blocking I/O operations

### Audio Processing
- **Input**: Web Speech API (browser-based STT)
- **Output**: Azure TTS → MP3 format → Web Audio API
- **Format**: 16kHz, 32kbps, mono MP3 for web compatibility
- **Voice**: Hindi (hi-IN-SwaraNeural) with customizable settings

## 🛠️ Customization

### Modify Voice Settings
Edit the settings in the frontend or adjust the TTS configuration in `voice_bot.py`:
```python
# In synthesize_speech_azure_sdk function
voice_name = "hi-IN-SwaraNeural"  # Change voice
tts_speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
)
```

### Customize UI Theme
Modify `frontend/styles.css` to change colors, animations, or layout:
```css
/* Change gradient background */
body {
    background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%);
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Microphone not working**: Check browser permissions for microphone access
2. **Audio not playing**: Interact with the page first (browser autoplay policy)
3. **Connection failed**: Ensure both servers are running and ports are available
4. **CORS errors**: Backend includes CORS middleware, but check browser console

### Port Conflicts
- Frontend: Automatically finds available port starting from 3000
- Backend: Uses port 8000 (can be changed in `voice_bot.py`)

## 🎨 Features Showcase

- **🎭 Animated Voice Visualizer**: Visual feedback during voice input
- **🎯 Smart Status Indicators**: Real-time connection and processing status
- **🎪 Smooth Animations**: CSS transitions and keyframe animations
- **📱 Mobile Responsive**: Adapts to different screen sizes
- **🎛️ Advanced Settings**: Fine-tune voice parameters
- **🔄 Auto-Reconnection**: Handles network interruptions gracefully
- **💾 Settings Persistence**: Remembers your preferences

## 🚫 Removed Components

This version has removed all Twilio-related functionality:
- ❌ Phone call integration
- ❌ Twilio media streams
- ❌ Audio format conversions (mulaw/PCM)
- ❌ Telephony features
- ❌ Complex audio routing

The focus is now on a clean, modern web-based voice assistant experience! 🎉
