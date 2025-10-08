#!/bin/bash

# Azure TTS Integration Setup Script
# This script helps you set up the Azure TTS integration

echo "🚀 Azure TTS Integration Setup"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📦 Step 1: Installing Python dependencies..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🔑 Step 2: Azure Configuration"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit backend/.env and add your Azure credentials:"
    echo "   - AZURE_SPEECH_KEY=your_actual_key"
    echo "   - AZURE_SPEECH_REGION=your_region"
    echo ""
    echo "You can get these from: https://portal.azure.com"
    echo ""
else
    echo "✅ .env file already exists"
    
    # Check if Azure keys are configured
    if grep -q "AZURE_SPEECH_KEY=your_azure_speech_key" .env; then
        echo ""
        echo "⚠️  WARNING: Azure credentials not configured!"
        echo "   Please edit backend/.env and add your actual Azure credentials"
        echo ""
    else
        echo "✅ Azure credentials appear to be configured"
    fi
fi

echo ""
echo "🧪 Step 3: Testing Azure TTS"
echo ""

read -p "Do you want to test Azure TTS now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running Azure TTS test..."
    python test_azure_tts.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Azure TTS is working correctly!"
    else
        echo ""
        echo "❌ Azure TTS test failed"
        echo "   Please check your Azure credentials in backend/.env"
        exit 1
    fi
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Make sure backend/.env has valid Azure credentials"
echo "2. Start the backend:"
echo "   cd backend && uvicorn main:app --reload"
echo "3. Start the frontend:"
echo "   npm run dev"
echo "4. Test the voice assistant in your browser"
echo ""
echo "📚 Documentation:"
echo "   - See AZURE_TTS_INTEGRATION.md for detailed guide"
echo "   - See CHANGES_SUMMARY.md for list of changes"
echo ""
