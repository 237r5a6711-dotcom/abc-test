#!/bin/bash
# Quick Start Script for Video Streaming Solution

echo "======================================"
echo "Video Streaming Solution - Quick Start"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.6 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Check if requirements are installed
echo "Checking requirements..."
python3 -c "import cv2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "OpenCV not found. Installing requirements..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install requirements"
        exit 1
    fi
else
    echo "✓ Requirements already installed"
fi
echo ""

# Ask user what they want to run
echo "What would you like to run?"
echo ""
echo "1) Transmitter (send video from webcam)"
echo "2) Receiver (receive and display video)"
echo "3) Both (testing on same computer)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting Transmitter..."
        echo "Default settings: 640x480 @ 30fps"
        echo ""
        read -p "Use custom settings? (y/N): " custom
        if [[ $custom == "y" || $custom == "Y" ]]; then
            read -p "Width (default 640): " width
            width=${width:-640}
            read -p "Height (default 480): " height
            height=${height:-480}
            read -p "FPS (default 30): " fps
            fps=${fps:-30}
            read -p "Quality 1-100 (default 80): " quality
            quality=${quality:-80}
            echo ""
            echo "Starting transmitter with custom settings..."
            python3 transmitter.py --width $width --height $height --fps $fps --quality $quality
        else
            echo ""
            echo "Starting transmitter with default settings..."
            python3 transmitter.py
        fi
        ;;
    2)
        echo ""
        read -p "Transmitter IP address (default 127.0.0.1): " host
        host=${host:-127.0.0.1}
        echo ""
        echo "Starting receiver..."
        echo "Connecting to $host:9999"
        echo ""
        python3 receiver.py --host $host
        ;;
    3)
        echo ""
        echo "Starting both transmitter and receiver..."
        echo "This will open two terminal windows"
        echo ""
        
        # Start transmitter in background
        echo "Starting transmitter..."
        python3 transmitter.py &
        TRANSMITTER_PID=$!
        
        # Wait for transmitter to start
        sleep 3
        
        # Start receiver
        echo "Starting receiver..."
        python3 receiver.py
        
        # When receiver exits, kill transmitter
        kill $TRANSMITTER_PID 2>/dev/null
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
