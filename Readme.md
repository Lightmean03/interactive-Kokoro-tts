# 🎵 Interactive Kokoro TTS

A web-based frontend for the [Kokoro Text-to-Speech model](https://huggingface.co/hexgrad/Kokoro-82M), designed to make high-quality voice synthesis easily accessible through an intuitive interface.

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
- 🐳 **Docker Ready** - Easy deployment with Docker and Docker Compose
- 🚀 **Fast Generation** - Leverages Kokoro's lightweight 82M parameter model
- 📱 **Mobile Friendly** - Responsive design works on all devices

## 🖼️ Screenshots

### Main Interface
<img src="https://github.com/Lightmean03/interactive-Kokoro-tts/blob/master/Example%20Screenshots/ttsMainSC.png?raw=true" alt="Screenshot of Site">

### Voice Selection
<img src="https://github.com/Lightmean03/interactive-Kokoro-tts/blob/master/Example%20Screenshots/ttsVoiceMenuSC.png?raw=true" alt="Voice Selection Picture">
### Audio Generation
<img src="https://github.com/Lightmean03/interactive-Kokoro-tts/blob/master/Example%20Screenshots/ttsAudioMenuSC.png?raw=true" alt="Audio Generation and Control Picture"> 

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/Lightmean03/interactive-Kokoro-tts.git
cd interactive-Kokoro-tts
```

2. **Run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Open your browser:**
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

## 📋 Requirements

### System Requirements
- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 5GB for models and cache
- **Python:** 3.11 or higher

### Dependencies
- Flask 3.0+
- Kokoro TTS 0.9.4+
- PyTorch
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

### Basic Docker Run
```bash
docker build -t kokoro-tts .
docker run -d -p 5000:5000 --name kokoro-tts-app kokoro-tts
```

### With Volume Mounts
```bash
docker run -d \
  --name kokoro-tts-app \
  -p 5000:5000 \
  -v $(pwd)/audio_cache:/app/temp \
  -v $(pwd)/model_cache:/home/appuser/.cache \
  kokoro-tts
```

### Resource Limits
```bash
docker run -d \
  --name kokoro-tts-app \
  --memory=2g \
  --cpus=1.0 \
  -p 5000:5000 \
  kokoro-tts
```

## 📡 API Endpoints

The application provides the following REST API endpoints:

- `GET /` - Main web interface
- `POST /generate` - Generate audio from text
- `GET /audio/<id>` - Stream generated audio
- `GET /download/<id>` - Download audio file
- `GET /health` - Health check endpoint

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
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV` - Flask environment (production/development)
- `HOST` - Bind address (default: 0.0.0.0)
- `PORT` - Port number (default: 5000)
- `TEMP_DIR` - Temporary files directory (default: /app/temp)

### Docker Compose Override
Create a `docker-compose.override.yml` file for custom settings:

```yaml
version: '3.8'
services:
  kokoro-tts:
    environment:
      - PORT=8080
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
├── app.py                 # Main Flask application
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── requirements.txt      # Python dependencies
├── .dockerignore        # Docker ignore rules
├── templates/
│   └── index.html       # Web interface template
├── audio_cache/         # Generated audio files (auto-created)
└── model_cache/         # Model cache directory (auto-created)
```

## 📝 Usage Tips

1. **Voice Selection** - Each voice has different characteristics. Experiment to find the best fit for your content.
2. **Text Length** - Optimal results with 100-200 tokens. Very short or very long texts may have quality issues.
3. **Special Pronunciation** - Use phonetic notation like `[Kokoro](/kˈOkəɹO/)` for custom pronunciations.
4. **Resource Management** - Audio files are automatically cleaned up after 1 hour to save disk space.
5. **Find A Voice You Like** - Changing voices can lead to longer loading times, the intial generation will also take longer. 

## 🐛 Troubleshooting

### Common Issues

**"Can't find model 'en_core_web_sm'"**
```bash
python -m spacy download en_core_web_sm
```

**Docker container exits immediately**
```bash
docker logs kokoro-tts-app
# Check logs for specific error messages
```

**Out of memory errors**
```bash
# Reduce Docker memory limits or close other applications
docker run --memory=2g --cpus=1.0 -p 5000:5000 kokoro-tts
```

**Audio not playing**
- Check browser console for errors
- Ensure audio files are being generated (check `/audio/<id>` endpoint)
- Verify browser supports HTML5 audio

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


**Made with ❤️ to make high-quality text-to-speech accessible to everyone**
