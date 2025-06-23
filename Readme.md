# 🎵 Interactive Kokoro TTS

A beautiful web-based frontend for the [Kokoro Text-to-Speech model](https://huggingface.co/hexgrad/Kokoro-82M), designed to make high-quality voice synthesis easily accessible through an intuitive interface.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.0+-green.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

## ✨ Features

- 🎨 **Beautiful Web Interface** - Modern, responsive design with gradient themes
- 🗣️ **55+ Voice Options** - Support for all Kokoro voices across 9 languages
- 🌍 **Multi-Language Support** - English, Spanish, French, Japanese, Chinese, Hindi, Italian, Portuguese
- 🎧 **Instant Audio Playback** - Generated audio plays automatically
- 💾 **Download Functionality** - Save generated audio as WAV files
- 🚀 **GPU + CPU Support** - Automatic hardware detection with GPU acceleration when available
- 🖥️ **Cross-Platform** - Works on Windows, Linux, macOS with or without GPU
- 🐳 **Docker Ready** - Easy deployment with Docker and Docker Compose
- ⚡ **Fast Generation** - Leverages Kokoro's lightweight 82M parameter model
- 📱 **Mobile Friendly** - Responsive design works on all devices
- 📊 **Performance Monitoring** - Real-time device info and generation time display

## 🖼️ Screenshots

### Main Interface
<img src="https://github.com/Lightmean03/interactive-Kokoro-tts/blob/master/Example%20Screenshots/ttsMainSC.png?raw=true" alt="Screenshot of Site">

### Voice Selection
<img src="https://github.com/Lightmean03/interactive-Kokoro-tts/blob/master/Example%20Screenshots/ttsVoiceMenuSC.png?raw=true" alt="Voice Selection Picture">

### Audio Generation
<img src="https://github.com/Lightmean03/interactive-Kokoro-tts/blob/master/Example%20Screenshots/ttsAudioMenuSC.png?raw=true" alt="Audio Generation and Control Picture"> 

## 🚀 Quick Start

### Option 1: Docker (Recommended)

#### For Linux Systems:
```bash
# Clone the repository
git clone https://github.com/Lightmean03/interactive-Kokoro-tts.git
cd interactive-Kokoro-tts

# Run setup script to detect GPU and fix permissions
chmod +x setup-linux.sh
./setup-linux.sh

# For CPU-only systems:
docker-compose up --build

# For GPU-enabled systems:
docker-compose -f docker-compose-gpu.yml up --build
```

#### For Windows/WSL:
```bash
# Clone the repository
git clone https://github.com/Lightmean03/interactive-Kokoro-tts.git
cd interactive-Kokoro-tts

# Auto-detects GPU/CPU and runs accordingly
docker-compose up --build
```

#### Open your browser:
Navigate to `http://localhost:5000`

### Option 2: Local Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Lightmean03/interactive-Kokoro-tts.git
cd interactive-Kokoro-tts
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **Run the application:**
```bash
python app.py
```

4. **Open your browser:**
Navigate to `http://localhost:5000`

## 💻 Hardware Support

### 🚀 GPU Acceleration (Recommended)
- **NVIDIA GPUs** with CUDA support
- **Automatic Detection** - App detects and uses GPU when available
- **Faster Generation** - 3-5x speed improvement over CPU
- **Memory Requirements** - 2GB+ VRAM recommended

### 🖥️ CPU Fallback
- **Universal Support** - Works on any system with CPU
- **Optimized Threading** - Automatically adjusts thread count
- **Cross-Platform** - Linux, Windows, macOS compatible
- **Resource Efficient** - Lower memory usage

### 📊 Performance Comparison
| Hardware | Generation Time* | Memory Usage | Power Consumption |
|----------|------------------|--------------|-------------------|
| GPU (RTX 3070) | ~2-3 seconds | 3-4GB | High |
| CPU (8-core) | ~8-12 seconds | 2-3GB | Medium |
| CPU (4-core) | ~15-20 seconds | 2GB | Low |

*For ~100 tokens of text

## 📋 Requirements

### System Requirements
- **RAM:** 2GB minimum, 4GB recommended (6GB for GPU)
- **Storage:** 5GB for models and cache
- **Python:** 3.11 or higher

### For GPU Acceleration
- **NVIDIA GPU** with CUDA 11.0+ support
- **NVIDIA Docker Runtime** (Linux only)
- **Windows:** CUDA drivers + Docker Desktop
- **Linux:** NVIDIA Container Toolkit

### Dependencies
- Flask 3.0+
- Kokoro TTS 0.9.4+
- PyTorch (CPU or CUDA)
- SoundFile
- NumPy
- spaCy with English model

## 🎭 Available Voices

The application supports all 55+ voices from the Kokoro model:

### 🇺🇸 American English
**Female:** af_alloy, af_aoede, af_bella, af_heart, af_jessica, af_kore, af_nicole, af_nova, af_river, af_sarah, af_sky  
**Male:** am_adam, am_echo, am_eric, am_fenrir, am_liam, am_michael, am_onyx, am_puck, am_santa

### 🇬🇧 British English
**Female:** bf_alice, bf_emma, bf_isabella, bf_lily  
**Male:** bm_daniel, bm_fable, bm_george, bm_lewis

### 🇪🇸 Spanish
**Female:** ef_dora  
**Male:** em_alex, em_santa

### 🇫🇷 French
**Female:** ff_siwis

### 🇮🇳 Hindi
**Female:** hf_alpha, hf_beta  
**Male:** hm_omega, hm_psi

### 🇮🇹 Italian
**Female:** if_sara  
**Male:** im_nicola

### 🇯🇵 Japanese
**Female:** jf_alpha, jf_gongitsune, jf_nezumi, jf_tebukuro  
**Male:** jm_kumo

### 🇧🇷 Portuguese
**Female:** pf_dora  
**Male:** pm_alex, pm_santa

### 🇨🇳 Chinese
**Female:** zf_xiaobei, zf_xiaoni, zf_xiaoxiao, zf_xiaoyi

## 🐳 Docker Configuration

### GPU-Enabled Docker (Linux)
```bash
# Install NVIDIA Container Toolkit first
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

# Run with GPU support
docker-compose -f docker-compose-gpu.yml up --build
```

### CPU-Only Docker
```bash
# Works on any system
docker-compose up --build
```

### Manual Docker Commands

#### GPU-Enabled:
```bash
docker build -t kokoro-tts .
docker run -d \
  --name kokoro-tts-app \
  --gpus all \
  -p 5000:5000 \
  -v $(pwd)/audio_cache:/app/temp \
  -v $(pwd)/model_cache:/home/appuser/.cache \
  kokoro-tts
```

#### CPU-Only:
```bash
docker build -t kokoro-tts .
docker run -d \
  --name kokoro-tts-app \
  --memory=2g \
  --cpus=1.0 \
  -p 5000:5000 \
  -v $(pwd)/audio_cache:/app/temp \
  -v $(pwd)/model_cache:/home/appuser/.cache \
  kokoro-tts
```

## 📡 API Endpoints

The application provides the following REST API endpoints:

- `GET /` - Main web interface
- `POST /generate` - Generate audio from text
- `GET /audio/<id>` - Stream generated audio
- `GET /download/<id>` - Download audio file
- `GET /health` - Health check endpoint with device info
- `GET /device-info` - Current hardware information

### Example API Usage
```javascript
// Generate audio
const response = await fetch('/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        text: "Hello, world!",
        voice: "af_heart"
    })
});

const data = await response.json();
console.log(data.audio_id); // Use this ID to access the audio
console.log(data.device); // Shows GPU or CPU
console.log(data.generation_time); // Time taken to generate

// Check device info
const deviceInfo = await fetch('/device-info');
const device = await deviceInfo.json();
console.log(device.type); // "CUDA" or "CPU"
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV` - Flask environment (production/development)
- `HOST` - Bind address (default: 0.0.0.0)
- `PORT` - Port number (default: 5000)
- `TEMP_DIR` - Temporary files directory (default: /app/temp)
- `CUDA_VISIBLE_DEVICES` - GPU device selection (for multi-GPU)

### Docker Compose Override
Create a `docker-compose.override.yml` file for custom settings:

```yaml
version: '3.8'
services:
  kokoro-tts:
    environment:
      - PORT=8080
      - CUDA_VISIBLE_DEVICES=0  # Use specific GPU
    ports:
      - "8080:8080"
```

## 🛠️ Development

### Local Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run in development mode
export FLASK_ENV=development
python app.py
```

### Project Structure
```
interactive-Kokoro-tts/
├── app.py                    # Main Flask application
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # CPU Docker Compose setup
├── docker-compose-gpu.yml   # GPU Docker Compose setup
├── setup-linux.sh          # Linux setup script
├── requirements.txt         # Python dependencies
├── .dockerignore           # Docker ignore rules
├── templates/
│   └── index.html          # Web interface template
├── audio_cache/            # Generated audio files (auto-created)
└── model_cache/            # Model cache directory (auto-created)
```

## 📝 Usage Tips

1. **Voice Selection** - Each voice has different characteristics. Experiment to find the best fit for your content.
2. **Text Length** - Optimal results with 100-200 tokens. Very short or very long texts may have quality issues.
3. **Special Pronunciation** - Use phonetic notation like `[Kokoro](/kˈOkəɹO/)` for custom pronunciations.
4. **Resource Management** - Audio files are automatically cleaned up after 1 hour to save disk space.
5. **Find A Voice You Like** - Changing voices can lead to longer loading times, the initial generation will also take longer.
6. **GPU Performance** - First generation takes longer due to model loading; subsequent generations are much faster.
7. **Hardware Monitoring** - Check the device indicator in the header to see if GPU is being used.

## 🐛 Troubleshooting

### Common Issues

**"Can't find model 'en_core_web_sm'"**
```bash
python -m spacy download en_core_web_sm
```

**"could not create a primitive" (Linux CPU)**
```bash
# Use the CPU-optimized setup
./setup-linux.sh
docker-compose up --build
```

**GPU not detected on Linux**
```bash
# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

**Permission denied errors (Linux)**
```bash
# Run the setup script
chmod +x setup-linux.sh
./setup-linux.sh
```

**Docker container exits immediately**
```bash
docker logs kokoro-tts-app
# Check logs for specific error messages
```

**Out of memory errors**
```bash
# For GPU: Reduce batch size or use CPU
# For CPU: Reduce Docker memory limits
docker run --memory=2g --cpus=1.0 -p 5000:5000 kokoro-tts
```

**Audio not playing**
- Check browser console for errors
- Ensure audio files are being generated (check `/audio/<id>` endpoint)
- Verify browser supports HTML5 audio

### Performance Optimization

**For GPU systems:**
- Ensure CUDA drivers are up to date
- Monitor GPU memory usage with `nvidia-smi`
- Use `docker stats` to monitor container resources

**For CPU systems:**
- Close unnecessary applications
- Monitor with `htop` or `top`
- Adjust thread count in environment variables

## 📊 Monitoring

### Check Hardware Usage
```bash
# GPU monitoring
nvidia-smi

# Container monitoring
docker stats kokoro-tts-app

# API health check
curl http://localhost:5000/health

# Device info
curl http://localhost:5000/device-info
```

## 🙏 Credits and Acknowledgments

This project is a frontend interface for the amazing work done by the Kokoro TTS team:

- **Original Kokoro Model:** [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- **Model Architecture:** Based on [StyleTTS 2](https://arxiv.org/abs/2306.07691) by Li et al.
- **Original Repository:** [hexgrad/kokoro](https://github.com/hexgrad/kokoro)
- **Trained by:** @rzvzn on Discord
- **Architecture by:** Li et al @ [StyleTTS2](https://github.com/yl4579/StyleTTS2)

### Special Thanks
- 🛠️ [@yl4579](https://huggingface.co/yl4579) for architecting StyleTTS 2
- 🏆 [@Pendrokar](https://huggingface.co/Pendrokar) for adding Kokoro to TTS Spaces Arena
- 📊 Everyone who contributed synthetic training data
- ❤️ All compute sponsors who made Kokoro possible

**Note:** This frontend application is not affiliated with the original Kokoro authors. It's an independent project to make Kokoro more accessible through a web interface.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

The underlying Kokoro model is also licensed under Apache 2.0, making it free for both commercial and personal use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Lightmean03/interactive-Kokoro-tts/issues) page
2. Create a new issue with detailed information about your problem
3. Include system information, error logs, and steps to reproduce

## 🌟 Star History

If this project helped you, please consider giving it a star! ⭐

---

**Made with ❤️ to make high-quality text-to-speech accessible to everyone**

