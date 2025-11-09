#!/usr/bin/env python3
"""
Web UI for ReproductorAlecksey
Flask-based web interface with neon theme
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import subprocess
from pathlib import Path
import threading

app = Flask(__name__)
CORS(app)

# Configuration
DOWNLOADS_DIR = Path.home() / "ReproductorAlecksey" / "downloads"
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

class VideoDownloader:
    def __init__(self):
        self.active_downloads = {}
    
    def get_video_info(self, url):
        """Get video information"""
        try:
            cmd = ['yt-dlp', '--dump-json', '--no-playlist', url]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)
            return {
                'success': True,
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'thumbnail': info.get('thumbnail', ''),
                'description': info.get('description', '')[:300] + '...'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def download_video(self, url, format_choice='best'):
        """Download video in background"""
        output_template = str(DOWNLOADS_DIR / '%(title)s.%(ext)s')
        
        cmd = [
            'yt-dlp',
            '-f', format_choice,
            '-o', output_template,
            url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {'success': result.returncode == 0}
        except Exception as e:
            return {'success': False, 'error': str(e)}

downloader = VideoDownloader()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/info', methods=['POST'])
def get_info():
    """Get video information"""
    data = request.json
    url = data.get('url', '')
    if not url:
        return jsonify({'success': False, 'error': 'URL required'})
    
    info = downloader.get_video_info(url)
    return jsonify(info)

@app.route('/api/download', methods=['POST'])
def download():
    """Start download"""
    data = request.json
    url = data.get('url', '')
    format_choice = data.get('format', 'best')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL required'})
    
    # Download in background thread
    def download_thread():
        downloader.download_video(url, format_choice)
    
    thread = threading.Thread(target=download_thread)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Download started'})

@app.route('/api/files')
def list_files():
    """List downloaded files"""
    files = []
    for file in DOWNLOADS_DIR.glob('*'):
        if file.suffix.lower() in ['.mp4', '.mp3', '.webm', '.mkv', '.m4a']:
            files.append({
                'name': file.name,
                'size': file.stat().st_size,
                'path': str(file)
            })
    return jsonify({'success': True, 'files': files})

@app.route('/downloads/<path:filename>')
def download_file(filename):
    """Serve downloaded file"""
    return send_from_directory(DOWNLOADS_DIR, filename)

def create_templates():
    """Create HTML templates"""
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Create index.html with neon theme
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎵 ReproductorAlecksey - Web UI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0015 0%, #1a0033 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(255, 16, 240, 0.1);
            border: 2px solid #FF10F0;
            border-radius: 15px;
            box-shadow: 0 0 30px rgba(255, 16, 240, 0.3);
        }
        
        h1 {
            font-size: 3em;
            background: linear-gradient(45deg, #FF10F0, #00FFFF, #39FF14);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(255, 16, 240, 0.5);
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #00FFFF;
            font-size: 1.2em;
        }
        
        .card {
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid #00FFFF;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }
        
        .card h2 {
            color: #39FF14;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            color: #FFFF00;
            margin-bottom: 8px;
            font-weight: bold;
        }
        
        input[type="text"],
        select {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #FF10F0;
            border-radius: 8px;
            color: #fff;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        input[type="text"]:focus,
        select:focus {
            outline: none;
            border-color: #00FFFF;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        }
        
        button {
            padding: 15px 30px;
            background: linear-gradient(45deg, #FF10F0, #BF00FF);
            border: none;
            border-radius: 8px;
            color: #fff;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 0 20px rgba(255, 16, 240, 0.4);
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 30px rgba(255, 16, 240, 0.8);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .btn-info {
            background: linear-gradient(45deg, #00FFFF, #1B03A3);
            margin-right: 10px;
        }
        
        .preview {
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #39FF14;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            display: none;
        }
        
        .preview.active {
            display: block;
        }
        
        .preview img {
            width: 100%;
            max-width: 400px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        .preview-info {
            margin: 10px 0;
        }
        
        .preview-info span {
            color: #FFFF00;
            font-weight: bold;
        }
        
        .file-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .file-item {
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #FF6600;
            border-radius: 10px;
            padding: 15px;
            transition: all 0.3s;
        }
        
        .file-item:hover {
            border-color: #00FFFF;
            transform: translateY(-5px);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
        }
        
        .file-name {
            color: #00FFFF;
            font-weight: bold;
            margin-bottom: 8px;
            word-break: break-word;
        }
        
        .file-size {
            color: #39FF14;
            font-size: 0.9em;
        }
        
        .status {
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
        
        .status.success {
            background: rgba(57, 255, 20, 0.2);
            border: 2px solid #39FF14;
            color: #39FF14;
            display: block;
        }
        
        .status.error {
            background: rgba(255, 0, 0, 0.2);
            border: 2px solid #ff0000;
            color: #ff6666;
            display: block;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #00FFFF;
            display: none;
        }
        
        .loading.active {
            display: block;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .loading::after {
            content: '...';
            animation: pulse 1.5s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎵 REPRODUCTOR ALECKSEY 🎵</h1>
            <p class="subtitle">Neon Edition - Web UI</p>
        </header>
        
        <div class="card">
            <h2>🔗 Descargar Video</h2>
            
            <div class="input-group">
                <label for="videoUrl">URL del Video:</label>
                <input type="text" id="videoUrl" placeholder="https://youtube.com/watch?v=...">
            </div>
            
            <div class="input-group">
                <label for="format">Formato:</label>
                <select id="format">
                    <option value="best">Mejor calidad</option>
                    <option value="bestvideo+bestaudio">Mejor video + audio</option>
                    <option value="bestaudio">Solo audio</option>
                </select>
            </div>
            
            <button class="btn-info" onclick="getInfo()">📋 Preview</button>
            <button onclick="downloadVideo()">⬇️ Descargar</button>
            
            <div id="loading" class="loading">Cargando</div>
            <div id="status" class="status"></div>
            
            <div id="preview" class="preview">
                <img id="previewThumb" src="" alt="Thumbnail">
                <div class="preview-info">
                    <span>Título:</span> <span id="previewTitle"></span>
                </div>
                <div class="preview-info">
                    <span>Duración:</span> <span id="previewDuration"></span>
                </div>
                <div class="preview-info">
                    <span>Autor:</span> <span id="previewUploader"></span>
                </div>
                <div class="preview-info">
                    <span>Vistas:</span> <span id="previewViews"></span>
                </div>
                <div class="preview-info">
                    <span>Descripción:</span> <p id="previewDesc"></p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>📁 Archivos Descargados</h2>
            <button onclick="loadFiles()">🔄 Actualizar</button>
            <div id="fileList" class="file-list"></div>
        </div>
    </div>
    
    <script>
        async function getInfo() {
            const url = document.getElementById('videoUrl').value;
            if (!url) {
                showStatus('Por favor ingresa una URL', false);
                return;
            }
            
            showLoading(true);
            hideStatus();
            document.getElementById('preview').classList.remove('active');
            
            try {
                const response = await fetch('/api/info', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                
                const data = await response.json();
                showLoading(false);
                
                if (data.success) {
                    // Show preview
                    document.getElementById('previewThumb').src = data.thumbnail;
                    document.getElementById('previewTitle').textContent = data.title;
                    document.getElementById('previewDuration').textContent = 
                        Math.floor(data.duration / 60) + ':' + (data.duration % 60).toString().padStart(2, '0');
                    document.getElementById('previewUploader').textContent = data.uploader;
                    document.getElementById('previewViews').textContent = data.view_count.toLocaleString();
                    document.getElementById('previewDesc').textContent = data.description;
                    
                    document.getElementById('preview').classList.add('active');
                } else {
                    showStatus('Error: ' + data.error, false);
                }
            } catch (error) {
                showLoading(false);
                showStatus('Error de conexión: ' + error.message, false);
            }
        }
        
        async function downloadVideo() {
            const url = document.getElementById('videoUrl').value;
            const format = document.getElementById('format').value;
            
            if (!url) {
                showStatus('Por favor ingresa una URL', false);
                return;
            }
            
            showLoading(true);
            hideStatus();
            
            try {
                const response = await fetch('/api/download', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url, format: format})
                });
                
                const data = await response.json();
                showLoading(false);
                
                if (data.success) {
                    showStatus('¡Descarga iniciada! Actualiza la lista en unos momentos.', true);
                } else {
                    showStatus('Error: ' + data.error, false);
                }
            } catch (error) {
                showLoading(false);
                showStatus('Error de conexión: ' + error.message, false);
            }
        }
        
        async function loadFiles() {
            try {
                const response = await fetch('/api/files');
                const data = await response.json();
                
                const fileList = document.getElementById('fileList');
                fileList.innerHTML = '';
                
                if (data.success && data.files.length > 0) {
                    data.files.forEach(file => {
                        const fileItem = document.createElement('div');
                        fileItem.className = 'file-item';
                        
                        const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
                        
                        fileItem.innerHTML = `
                            <div class="file-name">🎵 ${file.name}</div>
                            <div class="file-size">${sizeMB} MB</div>
                        `;
                        
                        fileList.appendChild(fileItem);
                    });
                } else {
                    fileList.innerHTML = '<p style="color: #FFFF00;">No hay archivos descargados aún.</p>';
                }
            } catch (error) {
                console.error('Error loading files:', error);
            }
        }
        
        function showStatus(message, success) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + (success ? 'success' : 'error');
        }
        
        function hideStatus() {
            document.getElementById('status').style.display = 'none';
        }
        
        function showLoading(show) {
            document.getElementById('loading').classList.toggle('active', show);
        }
        
        // Load files on page load
        loadFiles();
    </script>
</body>
</html>"""
    
    with open(templates_dir / 'index.html', 'w') as f:
        f.write(html_content)

def main():
    print("🌐 Iniciando Web UI...")
    print("📂 Directorio de descargas:", DOWNLOADS_DIR)
    
    # Create templates
    create_templates()
    
    print("\n✅ Servidor iniciado!")
    print("🔗 Abre tu navegador en: http://localhost:5000")
    print("\nPresiona Ctrl+C para detener el servidor\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
