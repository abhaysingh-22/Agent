#!/bin/bash

# Restaurant Agent Backend Startup Script

echo "🍕 Starting Restaurant Agent Backend..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY before running again."
    echo ""
    exit 1
fi

# Check if OPENAI_API_KEY is set
source .env
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "❌ Error: OPENAI_API_KEY is not configured in .env"
    echo "Please edit .env and add your actual OpenAI API key."
    echo ""
    exit 1
fi

echo "✅ Environment variables loaded"
echo ""

# Kill any existing process on port 8000
echo "🔍 Checking for existing processes on port ${PORT:-8000}..."
EXISTING_PID=$(lsof -ti:${PORT:-8000})
if [ ! -z "$EXISTING_PID" ]; then
    echo "⚠️  Found process running on port ${PORT:-8000} (PID: $EXISTING_PID)"
    echo "🛑 Killing existing process..."
    kill -9 $EXISTING_PID 2>/dev/null
    sleep 1
    echo "✅ Previous process terminated"
else
    echo "✅ Port ${PORT:-8000} is available"
fi
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Start the server
echo "🚀 Starting FastAPI server..."
echo "Server will be available at: http://localhost:${PORT:-8000}"
echo "Press Ctrl+C to stop"
echo ""

python app.py
