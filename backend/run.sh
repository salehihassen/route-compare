#!/bin/bash
# Simple startup script for the Commute API

echo "🚀 Starting Commute Estimation API..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Copy EXAMPLE.env to .env and add your Google Maps API key:"
    echo "   cp EXAMPLE.env .env"
    echo ""
fi

# Start the API
python api.py
