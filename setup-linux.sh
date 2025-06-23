#!/bin/bash

# Setup script for Linux systems to fix Docker permissions and detect GPU

echo "🐧 Setting up Interactive Kokoro TTS for Linux..."

# Create directories with proper permissions
echo "📁 Creating directories..."
mkdir -p audio_cache model_cache

# Get current user ID and group ID
USER_ID=$(id -u)
GROUP_ID=$(id -g)

echo "👤 Current user ID: $USER_ID"
echo "👥 Current group ID: $GROUP_ID"

# Set permissions for mounted directories
echo "🔐 Setting permissions..."
sudo chown -R $USER_ID:$GROUP_ID audio_cache model_cache
chmod -R 755 audio_cache model_cache

# Check for NVIDIA GPU
echo "🔍 Checking for GPU support..."
if command -v nvidia-smi &> /dev/null; then
    echo "🚀 NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name --format=csv,noheader
    
    # Check for nvidia-docker
    if docker info | grep -q nvidia; then
        echo "✅ NVIDIA Docker runtime detected"
        echo "🎯 Using GPU-enabled configuration"
        
        # Update docker-compose.yml with correct user ID for GPU
        cp docker-compose-gpu.yml docker-compose.yml
        sed -i "s/user: \"1000:1000\"/user: \"$USER_ID:$GROUP_ID\"/" docker-compose.yml
        
        echo "📋 To run with GPU support:"
        echo "   docker-compose up --build"
    else
        echo "⚠️  NVIDIA Docker runtime not found"
        echo "📋 Install nvidia-docker for GPU acceleration:"
        echo "   https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
        echo "🔄 Falling back to CPU configuration"
        
        # Update regular docker-compose.yml with correct user ID
        sed -i "s/user: \"1000:1000\"/user: \"$USER_ID:$GROUP_ID\"/" docker-compose.yml
    fi
else
    echo "🖥️  No NVIDIA GPU detected, using CPU configuration"
    
    # Update docker-compose.yml with correct user ID for CPU
    sed -i "s/user: \"1000:1000\"/user: \"$USER_ID:$GROUP_ID\"/" docker-compose.yml
fi

echo ""
echo "✅ Linux setup complete!"
echo ""
echo "📋 Available commands:"
echo "   🐳 CPU-only:     docker-compose up --build"
echo "   🚀 GPU-enabled:  docker-compose -f docker-compose-gpu.yml up --build"
echo "   🔄 Rebuild:      docker-compose down && docker-compose up --build"
echo "   📊 Monitor:      docker stats kokoro-tts-app"
echo ""
echo "🌐 Access the app at: http://localhost:5000"
