from flask import Flask, render_template, request, jsonify, send_file
from kokoro import KPipeline
import soundfile as sf
import numpy as np
import os
import tempfile
import threading
import time
from datetime import datetime
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables
pipeline = None
audio_cache = {}  # Store generated audio temporarily

# Create temp directory if it doesn't exist
TEMP_DIR = os.environ.get('TEMP_DIR', '/app/temp')
os.makedirs(TEMP_DIR, exist_ok=True)

def init_pipeline():
    """Initialize the Kokoro pipeline"""
    global pipeline
    if pipeline is None:
        try:
            logger.info("Initializing Kokoro pipeline...")
            pipeline = KPipeline(lang_code='a')
            logger.info("Kokoro pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {e}")
            raise

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for Docker"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/generate', methods=['POST'])
def generate_audio():
    """Generate audio from text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        voice = data.get('voice', 'af_heart')
        
        if not text:
            return jsonify({'error': 'Please enter some text'}), 400
        
        logger.info(f"Generating audio for voice: {voice}, text length: {len(text)}")
        
        # Initialize pipeline if needed
        init_pipeline()
        
        # Generate audio
        generator = pipeline(text, voice=voice)
        audio_segments = []
        
        for i, (gs, ps, audio) in enumerate(generator):
            audio_segments.append(audio)
            logger.debug(f"Generated segment {i}: {gs}, {ps}")
        
        # Concatenate all segments
        if len(audio_segments) > 1:
            full_audio = np.concatenate(audio_segments)
        else:
            full_audio = audio_segments[0]
        
        # Generate unique ID for this audio
        audio_id = str(uuid.uuid4())
        
        # Save to temporary file in the temp directory
        temp_file = tempfile.NamedTemporaryFile(
            suffix='.wav', 
            delete=False, 
            dir=TEMP_DIR
        )
        temp_file.close()
        
        sf.write(temp_file.name, full_audio, 24000)
        
        # Store in cache
        audio_cache[audio_id] = {
            'file_path': temp_file.name,
            'created_at': time.time(),
            'text': text,
            'voice': voice
        }
        
        # Clean up old files (older than 1 hour)
        cleanup_old_files()
        
        logger.info(f"Audio generated successfully for ID: {audio_id}")
        
        return jsonify({
            'success': True,
            'audio_id': audio_id,
            'message': 'Audio generated successfully!'
        })
        
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        return jsonify({'error': f'Failed to generate audio: {str(e)}'}), 500

@app.route('/audio/<audio_id>')
def get_audio(audio_id):
    """Serve audio file"""
    if audio_id not in audio_cache:
        logger.warning(f"Audio ID not found: {audio_id}")
        return jsonify({'error': 'Audio not found'}), 404
    
    file_path = audio_cache[audio_id]['file_path']
    if not os.path.exists(file_path):
        logger.warning(f"Audio file not found: {file_path}")
        return jsonify({'error': 'Audio file not found'}), 404
    
    return send_file(file_path, mimetype='audio/wav')

@app.route('/download/<audio_id>')
def download_audio(audio_id):
    """Download audio file"""
    if audio_id not in audio_cache:
        return jsonify({'error': 'Audio not found'}), 404
    
    file_path = audio_cache[audio_id]['file_path']
    if not os.path.exists(file_path):
        return jsonify({'error': 'Audio file not found'}), 404
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    voice = audio_cache[audio_id]['voice']
    filename = f"kokoro_{voice}_{timestamp}.wav"
    
    return send_file(file_path, as_attachment=True, download_name=filename)

def cleanup_old_files():
    """Clean up audio files older than 1 hour"""
    current_time = time.time()
    to_remove = []
    
    for audio_id, data in audio_cache.items():
        if current_time - data['created_at'] > 3600:  # 1 hour
            try:
                os.unlink(data['file_path'])
                logger.info(f"Cleaned up old audio file: {data['file_path']}")
            except Exception as e:
                logger.warning(f"Failed to cleanup file {data['file_path']}: {e}")
            to_remove.append(audio_id)
    
    for audio_id in to_remove:
        del audio_cache[audio_id]

# Background cleanup task
def periodic_cleanup():
    """Run cleanup every 30 minutes"""
    while True:
        time.sleep(1800)  # 30 minutes
        cleanup_old_files()

# Start background cleanup thread
cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    # Create templates directory and HTML file if they don't exist
    os.makedirs('templates', exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎵 Kokoro TTS Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            text-align: center;
            padding: 30px 20px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .content {
            padding: 30px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        select, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        select:focus, textarea:focus {
            outline: none;
            border-color: #4facfe;
        }
        
        textarea {
            min-height: 150px;
            resize: vertical;
            font-family: inherit;
        }
        
        .btn {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            width: 100%;
            margin-bottom: 15px;
        }
        
        .btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(79, 172, 254, 0.3);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #333;
        }
        
        .btn-success {
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            color: #333;
        }
        
        .audio-controls {
            display: none;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            text-align: center;
        }
        
        .audio-controls.show {
            display: block;
        }
        
        .controls-row {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        
        .controls-row .btn {
            flex: 1;
            margin-bottom: 0;
        }
        
        .status {
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-weight: 600;
        }
        
        .status.loading {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #4facfe;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        audio {
            width: 100%;
            margin: 15px 0;
        }
        
        @media (max-width: 600px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .controls-row {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎵 Kokoro TTS</h1>
            <p>Transform text into natural-sounding speech</p>
        </div>
        
        <div class="content">
            <form id="ttsForm">
                <div class="form-group">
                    <label for="voice">Voice:</label>
                    <select id="voice" name="voice">
                        <optgroup label="🇺🇸 American English - Female">
                            <option value="af_alloy">AF Alloy</option>
                            <option value="af_aoede">AF Aoede</option>
                            <option value="af_bella">AF Bella</option>
                            <option value="af_heart" selected>AF Heart (Default)</option>
                            <option value="af_jessica">AF Jessica</option>
                            <option value="af_kore">AF Kore</option>
                            <option value="af_nicole">AF Nicole (ASMR)</option>
                            <option value="af_nova">AF Nova</option>
                            <option value="af_river">AF River</option>
                            <option value="af_sarah">AF Sarah</option>
                            <option value="af_sky">AF Sky</option>
                        </optgroup>
                        <optgroup label="🇺🇸 American English - Male">
                            <option value="am_adam">AM Adam</option>
                            <option value="am_echo">AM Echo</option>
                            <option value="am_eric">AM Eric</option>
                            <option value="am_fenrir">AM Fenrir</option>
                            <option value="am_liam">AM Liam</option>
                            <option value="am_michael">AM Michael</option>
                            <option value="am_onyx">AM Onyx</option>
                            <option value="am_puck">AM Puck</option>
                            <option value="am_santa">AM Santa</option>
                        </optgroup>
                        <optgroup label="🇬🇧 British English - Female">
                            <option value="bf_alice">BF Alice</option>
                            <option value="bf_emma">BF Emma</option>
                            <option value="bf_isabella">BF Isabella</option>
                            <option value="bf_lily">BF Lily</option>
                        </optgroup>
                        <optgroup label="🇬🇧 British English - Male">
                            <option value="bm_daniel">BM Daniel</option>
                            <option value="bm_fable">BM Fable</option>
                            <option value="bm_george">BM George</option>
                            <option value="bm_lewis">BM Lewis</option>
                        </optgroup>
                        <optgroup label="🇪🇸 Spanish - Female">
                            <option value="ef_dora">EF Dora</option>
                        </optgroup>
                        <optgroup label="🇪🇸 Spanish - Male">
                            <option value="em_alex">EM Alex</option>
                            <option value="em_santa">EM Santa</option>
                        </optgroup>
                        <optgroup label="🇫🇷 French - Female">
                            <option value="ff_siwis">FF Siwis</option>
                        </optgroup>
                        <optgroup label="🇮🇳 Hindi - Female">
                            <option value="hf_alpha">HF Alpha</option>
                            <option value="hf_beta">HF Beta</option>
                        </optgroup>
                        <optgroup label="🇮🇳 Hindi - Male">
                            <option value="hm_omega">HM Omega</option>
                            <option value="hm_psi">HM Psi</option>
                        </optgroup>
                        <optgroup label="🇮🇹 Italian - Female">
                            <option value="if_sara">IF Sara</option>
                        </optgroup>
                        <optgroup label="🇮🇹 Italian - Male">
                            <option value="im_nicola">IM Nicola</option>
                        </optgroup>
                        <optgroup label="🇯🇵 Japanese - Female">
                            <option value="jf_alpha">JF Alpha</option>
                            <option value="jf_gongitsune">JF Gongitsune</option>
                            <option value="jf_nezumi">JF Nezumi</option>
                            <option value="jf_tebukuro">JF Tebukuro</option>
                        </optgroup>
                        <optgroup label="🇯🇵 Japanese - Male">
                            <option value="jm_kumo">JM Kumo</option>
                        </optgroup>
                        <optgroup label="🇧🇷 Portuguese - Female">
                            <option value="pf_dora">PF Dora</option>
                        </optgroup>
                        <optgroup label="🇧🇷 Portuguese - Male">
                            <option value="pm_alex">PM Alex</option>
                            <option value="pm_santa">PM Santa</option>
                        </optgroup>
                        <optgroup label="🇨🇳 Chinese - Female">
                            <option value="zf_xiaobei">ZF Xiaobei</option>
                            <option value="zf_xiaoni">ZF Xiaoni</option>
                            <option value="zf_xiaoxiao">ZF Xiaoxiao</option>
                            <option value="zf_xiaoyi">ZF Xiaoyi</option>
                        </optgroup>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="text">Text to convert:</label>
                    <textarea id="text" name="text" placeholder="Enter the text you want to convert to speech...">[Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.</textarea>
                </div>
                
                <button type="submit" class="btn" id="generateBtn">
                    🎙️ Generate Audio
                </button>
            </form>
            
            <div id="status"></div>
            
            <div id="audioControls" class="audio-controls">
                <h3>🎵 Generated Audio</h3>
                <audio id="audioPlayer" controls autoplay>
                    Your browser does not support the audio element.
                </audio>
                
                <div class="controls-row">
                    <button type="button" class="btn btn-secondary" onclick="playAudio()">
                        ▶️ Play Again
                    </button>
                    <button type="button" class="btn btn-success" onclick="downloadAudio()">
                        💾 Download
                    </button>
                    <button type="button" class="btn btn-secondary" onclick="clearAudio()">
                        🗑️ Clear
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentAudioId = null;
        
        document.getElementById('ttsForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const text = document.getElementById('text').value.trim();
            const voice = document.getElementById('voice').value;
            
            if (!text) {
                showStatus('Please enter some text', 'error');
                return;
            }
            
            // Show loading state
            const generateBtn = document.getElementById('generateBtn');
            generateBtn.disabled = true;
            generateBtn.innerHTML = '<span class="spinner"></span>Generating...';
            showStatus('Generating audio, please wait...', 'loading');
            hideAudioControls();
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text, voice })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    currentAudioId = data.audio_id;
                    showStatus('✅ Audio generated successfully!', 'success');
                    showAudioControls();
                    
                    // Load and play audio
                    const audioPlayer = document.getElementById('audioPlayer');
                    audioPlayer.src = `/audio/${currentAudioId}`;
                    audioPlayer.load();
                } else {
                    showStatus(`❌ ${data.error}`, 'error');
                }
                
            } catch (error) {
                showStatus(`❌ Error: ${error.message}`, 'error');
            } finally {
                // Reset button
                generateBtn.disabled = false;
                generateBtn.innerHTML = '🎙️ Generate Audio';
            }
        });
        
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = `status ${type}`;
            status.style.display = 'block';
        }
        
        function showAudioControls() {
            document.getElementById('audioControls').classList.add('show');
        }
        
        function hideAudioControls() {
            document.getElementById('audioControls').classList.remove('show');
        }
        
        function playAudio() {
            const audioPlayer = document.getElementById('audioPlayer');
            audioPlayer.currentTime = 0;
            audioPlayer.play();
        }
        
        function downloadAudio() {
            if (currentAudioId) {
                window.open(`/download/${currentAudioId}`, '_blank');
            }
        }
        
        function clearAudio() {
            hideAudioControls();
            currentAudioId = null;
            document.getElementById('status').style.display = 'none';
        }
    </script>
</body>
</html>'''
    
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"🎵 Kokoro TTS Flask App Starting on {host}:{port}")
    logger.info("📍 Docker Health Check: /health")
    logger.info("🔧 Use Ctrl+C to stop the server")
    
    app.run(debug=False, host=host, port=port, threaded=True)