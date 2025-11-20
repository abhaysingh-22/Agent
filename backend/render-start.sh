#!/bin/bash

# Render.com startup script for production

echo "🚀 Starting Restaurant Agent Backend on Render..."

# Start the FastAPI server with uvicorn
uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
