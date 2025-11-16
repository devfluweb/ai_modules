#!/bin/bash
# Quick Start Script for AI Extraction Testing (Linux/Mac)
# Run this to start the local testing server

echo ""
echo "========================================"
echo "  AI EXTRACTION TESTING - QUICK START"
echo "========================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "[WARNING] .env file not found!"
    echo ""
    echo "Please create a .env file with your Gemini API key:"
    echo "GEMINI_API_KEY=your_api_key_here"
    echo ""
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    exit 1
fi

echo "[1/3] Checking .env file... OK"
echo ""

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[2/3] Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
else
    echo "[2/3] Dependencies already installed... OK"
fi
echo ""

echo "[3/3] Starting server..."
echo ""
echo "========================================"
echo "  SERVER STARTING NOW"
echo "========================================"
echo ""
echo " Open your browser and go to:"
echo " http://localhost:5000"
echo ""
echo " Press Ctrl+C to stop the server"
echo ""

python3 app.py
