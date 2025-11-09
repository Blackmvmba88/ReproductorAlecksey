#!/usr/bin/env python3
"""
Quick Start Guide for ReproductorAlecksey
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import box

console = Console()

QUICK_START = """
# 🎵 ReproductorAlecksey - Guía Rápida

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Instalar yt-dlp

```bash
pip install yt-dlp
```

### 3. Instalar FFmpeg

- **Linux**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Descarga desde https://ffmpeg.org/

## 🎮 Modos de Uso

### Modo 1: Launcher (Recomendado)

El launcher te permite acceder a todas las funciones desde un solo lugar:

```bash
python launcher.py
```

### Modo 2: Terminal UI

Interfaz interactiva de terminal con tema neón:

```bash
python reproductor.py
```

**Funciones:**
- Descargar videos de YouTube y otras plataformas
- Preview de videos antes de descargar
- Ver lista de archivos descargados
- Acceso rápido a otras herramientas

### Modo 3: Web UI

Interfaz web moderna con tema neón:

```bash
python web_ui.py
```

Luego abre tu navegador en: http://localhost:5000

**Funciones:**
- Preview de videos con thumbnails
- Descarga en diferentes formatos
- Vista de archivos descargados
- Interfaz responsive y animada

### Modo 4: Visualizador de Audio

Visualiza audio con ondas sinusoidales y ecualizador:

```bash
python audio_visualizer.py archivo.mp3
```

O ejecuta sin argumentos para seleccionar un archivo:

```bash
python audio_visualizer.py
```

**Controles:**
- `W` - Modo Waveform (ondas)
- `S` - Modo Spectrum (espectro)
- `E` - Modo Equalizer (ecualizador)
- `SPACE` - Pausar/Reanudar
- `R` - Reiniciar
- `Q` - Salir

### Modo 5: Mejorador de Audio

Mejora la calidad de tus archivos de audio:

```bash
# Solo normalizar
python audio_enhancer.py archivo.mp3 --normalize

# Normalizar + Bass boost
python audio_enhancer.py archivo.mp3 --normalize --bass-boost

# Todas las mejoras
python audio_enhancer.py archivo.mp3 --all
```

## 📋 Ejemplos de Uso

### Ejemplo 1: Descargar un video

```bash
python reproductor.py
# Selecciona opción 1
# Ingresa la URL del video
# Verifica el preview
# Confirma la descarga
```

### Ejemplo 2: Visualizar audio descargado

```bash
python launcher.py
# Selecciona opción 3
# Elige un archivo de la lista
# Usa las teclas W, S, E para cambiar modos
```

### Ejemplo 3: Mejorar calidad de audio

```bash
python launcher.py
# Selecciona opción 4
# Elige un archivo de la lista
# Selecciona tipo de mejora
```

## 🎨 Tema Neón

El programa usa colores neón vibrantes:

- 💗 Rosa - Títulos y bordes principales
- 💙 Cyan - Información y acciones
- 💚 Verde - Confirmaciones y éxito
- 💛 Amarillo - Advertencias y etiquetas
- 🧡 Naranja - Archivos y elementos
- 💜 Púrpura - Botones y acciones
- 💙 Azul - Fondos y detalles

## 📁 Archivos Descargados

Los archivos se guardan en:

```
~/ReproductorAlecksey/downloads/
```

## 🆘 Problemas Comunes

### "yt-dlp no encontrado"
```bash
pip install --upgrade yt-dlp
```

### "FFmpeg no encontrado"
Instala FFmpeg según tu sistema operativo (ver arriba)

### Error en visualización
```bash
pip install --upgrade pygame numpy
```

### Error en Web UI
```bash
pip install --upgrade flask flask-cors
```

## 💡 Tips

1. **Preview siempre**: Usa la función de preview antes de descargar
2. **Formatos**: Elige "bestaudio" para solo audio y ahorrar espacio
3. **Visualizador**: El modo Equalizer es el más espectacular
4. **Mejoras de audio**: Usa "--all" para obtener la mejor calidad
5. **Web UI**: Más cómodo para descargar múltiples videos

## 🎯 Atajos de Teclado

### Terminal UI
- Números del menú para navegación rápida
- Enter para confirmar
- Ctrl+C para salir en cualquier momento

### Visualizador
- W/S/E para cambiar modos
- SPACE para pausar
- R para reiniciar
- Q para salir

## 🌐 URLs Soportadas

El programa soporta múltiples plataformas vía yt-dlp:
- YouTube
- Vimeo
- SoundCloud
- Twitch
- Twitter
- Y más de 1000 sitios web

## 📊 Características del Visualizador

- **Waveform**: Ondas sinusoidales con efectos de brillo
- **Spectrum**: Análisis FFT con barras de frecuencia
- **Equalizer**: Bandas ecualizadas con animación sinusoidal
- **60 FPS**: Animaciones fluidas
- **Colores dinámicos**: Ciclo de colores automático

## 🔧 Requisitos del Sistema

- Python 3.8 o superior
- 2 GB RAM mínimo (4 GB recomendado)
- Conexión a internet para descargas
- Soporte OpenGL para visualizador

---

¿Necesitas más ayuda? Consulta el README.md completo.
"""

def main():
    console.print(Panel(
        "[bold cyan]🎵 ReproductorAlecksey - Guía Rápida 🎵[/bold cyan]",
        border_style="magenta",
        box=box.DOUBLE
    ))
    
    md = Markdown(QUICK_START)
    console.print(md)
    
    console.print("\n")
    console.print(Panel(
        "[bold green]✨ ¡Listo para comenzar! Ejecuta: python launcher.py[/bold green]",
        border_style="green"
    ))

if __name__ == "__main__":
    main()
