#!/bin/bash

# Setup script for Linux systems to fix Docker permissions

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

# Update docker-compose.yml with correct user ID
echo "🐳 Updating Docker Compose configuration..."
sed -i "s/user: \"1000:1000\"/user: \"$USER_ID:$GROUP_ID\"/" docker-compose.yml

echo "✅ Linux setup complete!"
echo "🚀 You can now run: docker-compose up --build"
