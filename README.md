# 🎵 ReproductorAlecksey - Neon Edition

Reproductor multimedia avanzado con descarga de videos, visualización de audio y tema neón multicolor.

## ✨ Características

- 🔗 **Descarga de videos** con yt-dlp
- 📹 **Preview de videos** antes de descargar
- 🌊 **Visualizador de audio** con ondas sinusoidales y ecualizador
- 🎨 **Tema neón multicolor** (rosa, cyan, verde, amarillo, naranja, púrpura)
- 💻 **Interfaz de terminal** interactiva con Rich
- 🌐 **Web UI** con Flask
- 🎧 **Mejoramiento de audio** y análisis de frecuencias
- 📊 **Visualización local** de archivos multimedia

## 📋 Requisitos

- Python 3.8+
- yt-dlp
- FFmpeg (para conversión de audio)

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/Blackmvmba88/ReproductorAlecksey.git
cd ReproductorAlecksey
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Instala yt-dlp si no lo tienes:
```bash
pip install yt-dlp
```

4. Instala FFmpeg (requerido para conversión de audio):
   - **Linux**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Descarga desde https://ffmpeg.org/

## 🎮 Uso

### Interfaz de Terminal

Ejecuta el programa principal:
```bash
python reproductor.py
```

**Opciones del menú:**
- `1` - Descargar video desde URL (con preview)
- `2` - Ver archivos descargados
- `3` - Reproducir archivo local
- `4` - Abrir visualizador de audio
- `5` - Iniciar Web UI
- `6` - Información del sistema
- `0` - Salir

### Visualizador de Audio

Visualiza archivos de audio con ondas sinusoidales y ecualizador:
```bash
python audio_visualizer.py [archivo_audio]
```

**Controles del visualizador:**
- `W` - Modo Waveform (onda sinusoidal)
- `S` - Modo Spectrum (espectro de frecuencias)
- `E` - Modo Equalizer (ecualizador de bandas)
- `SPACE` - Pausar/Reanudar
- `R` - Reiniciar
- `Q` - Salir

### Web UI

Inicia el servidor web:
```bash
python web_ui.py
```

Luego abre tu navegador en: `http://localhost:5000`

**Funciones de la Web UI:**
- Preview de videos con thumbnail
- Descarga de videos en diferentes formatos
- Lista de archivos descargados
- Interfaz con tema neón animado

## 🎨 Tema Neón

El programa utiliza una paleta de colores neón vibrantes:
- 💗 Rosa (#FF10F0)
- 💙 Cyan (#00FFFF)
- 💚 Verde (#39FF14)
- 💛 Amarillo (#FFFF00)
- 🧡 Naranja (#FF6600)
- 💜 Púrpura (#BF00FF)
- 💙 Azul (#1B03A3)

## 📁 Estructura del Proyecto

```
ReproductorAlecksey/
├── reproductor.py          # Interfaz principal de terminal
├── audio_visualizer.py     # Visualizador de audio con ondas
├── web_ui.py              # Servidor web Flask
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
└── ~/ReproductorAlecksey/downloads/  # Directorio de descargas
```

## 🛠️ Tecnologías Utilizadas

- **yt-dlp**: Descarga de videos
- **Rich**: Interfaz de terminal con colores
- **Pygame**: Visualización gráfica
- **NumPy**: Procesamiento de audio
- **PyDub**: Conversión de formatos de audio
- **Flask**: Web UI
- **OpenCV**: Procesamiento de video

## 📝 Notas

- Los archivos se descargan en `~/ReproductorAlecksey/downloads/`
- El visualizador soporta formatos: MP3, WAV, M4A, OGG
- La descarga soporta formatos: MP4, MP3, WebM, MKV
- El análisis FFT proporciona visualización en tiempo real

## 🐛 Solución de Problemas

**Error "yt-dlp no encontrado":**
```bash
pip install --upgrade yt-dlp
```

**Error "FFmpeg no encontrado":**
- Instala FFmpeg siguiendo las instrucciones de instalación

**Error en la visualización de audio:**
- Asegúrate de que pygame esté instalado correctamente
- Verifica que el archivo de audio no esté corrupto

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👤 Autor

Blackmvmba88

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request
