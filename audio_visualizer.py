#!/usr/bin/env python3
"""
Audio Visualizer with Sinusoidal Wave Equalizer
Features: Real-time audio visualization, waveform display, frequency analysis
"""

import numpy as np
import pygame
import sys
import os
from pathlib import Path
import wave
import struct
from pydub import AudioSegment
import threading
import queue

# Neon colors for visualization
NEON_COLORS = {
    'pink': (255, 16, 240),
    'cyan': (0, 255, 255),
    'green': (57, 255, 20),
    'yellow': (255, 255, 0),
    'orange': (255, 102, 0),
    'purple': (191, 0, 255),
    'blue': (27, 3, 163)
}

class AudioVisualizer:
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("🌊 Visualizador de Audio - Neon Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Audio parameters
        self.chunk_size = 2048
        self.sample_rate = 44100
        self.audio_data = []
        self.current_frame = 0
        
        # Visualization mode
        self.viz_mode = 'waveform'  # waveform, spectrum, equalizer
        self.color_cycle = 0
        
    def load_audio(self, file_path):
        """Load audio file and extract data"""
        try:
            # Convert to wav if needed
            file_path = Path(file_path)
            if file_path.suffix.lower() in ['.mp3', '.m4a', '.ogg']:
                print(f"🔄 Convirtiendo {file_path.suffix} a WAV...")
                audio = AudioSegment.from_file(str(file_path))
                audio = audio.set_channels(1)  # Mono
                audio = audio.set_frame_rate(self.sample_rate)
                
                # Extract raw audio data
                samples = np.array(audio.get_array_of_samples())
                self.audio_data = samples / (2**15)  # Normalize to -1, 1
                print(f"✅ Audio cargado: {len(self.audio_data)} samples")
                return True
                
            elif file_path.suffix.lower() == '.wav':
                with wave.open(str(file_path), 'rb') as wav_file:
                    # Read WAV file
                    n_channels = wav_file.getnchannels()
                    sample_width = wav_file.getsampwidth()
                    framerate = wav_file.getframerate()
                    n_frames = wav_file.getnframes()
                    
                    # Read all frames
                    raw_data = wav_file.readframes(n_frames)
                    
                    # Convert to numpy array
                    if sample_width == 2:
                        fmt = f"{n_frames * n_channels}h"
                        data = struct.unpack(fmt, raw_data)
                        self.audio_data = np.array(data) / (2**15)
                    
                    # Convert stereo to mono if needed
                    if n_channels == 2:
                        self.audio_data = self.audio_data.reshape((-1, 2)).mean(axis=1)
                    
                    print(f"✅ Audio cargado: {len(self.audio_data)} samples")
                    return True
            
            return False
        except Exception as e:
            print(f"❌ Error cargando audio: {e}")
            return False
    
    def draw_waveform(self, data):
        """Draw sinusoidal waveform"""
        if len(data) == 0:
            return
        
        # Background gradient
        for y in range(self.height):
            color_ratio = y / self.height
            color = (
                int(10 * (1 - color_ratio)),
                int(20 * (1 - color_ratio)),
                int(40 * (1 - color_ratio))
            )
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
        
        # Draw waveform
        points = []
        step = max(1, len(data) // self.width)
        
        for x in range(self.width):
            idx = min(x * step, len(data) - 1)
            amplitude = data[idx]
            
            # Apply sinusoidal envelope for smoother visualization
            y = int(self.height / 2 + amplitude * self.height / 3 * np.sin(x * 0.01 + self.color_cycle))
            points.append((x, y))
        
        # Draw lines with neon glow effect
        for i in range(len(points) - 1):
            color_idx = (i + int(self.color_cycle * 10)) % len(list(NEON_COLORS.values()))
            color = list(NEON_COLORS.values())[color_idx]
            
            # Glow effect - draw multiple lines with decreasing alpha
            for thickness in range(5, 0, -1):
                glow_color = tuple(int(c * (thickness / 5)) for c in color)
                pygame.draw.line(self.screen, glow_color, points[i], points[i + 1], thickness)
    
    def draw_spectrum(self, data):
        """Draw frequency spectrum analyzer"""
        if len(data) == 0:
            return
        
        # Background
        self.screen.fill((5, 5, 15))
        
        # Perform FFT
        fft_data = np.fft.rfft(data)
        fft_magnitude = np.abs(fft_data)
        
        # Logarithmic scaling
        fft_magnitude = np.log10(fft_magnitude + 1)
        
        # Number of bars
        num_bars = 64
        bar_width = self.width // num_bars
        
        # Draw bars
        for i in range(num_bars):
            if i < len(fft_magnitude):
                magnitude = fft_magnitude[i * len(fft_magnitude) // num_bars]
                bar_height = int(magnitude * self.height / 4)
                
                # Color based on frequency (low=red, mid=green, high=blue)
                ratio = i / num_bars
                if ratio < 0.33:
                    color = NEON_COLORS['pink']
                elif ratio < 0.66:
                    color = NEON_COLORS['green']
                else:
                    color = NEON_COLORS['cyan']
                
                x = i * bar_width
                y = self.height - bar_height
                
                # Draw bar with glow
                for j in range(3):
                    glow_color = tuple(int(c * (3 - j) / 3) for c in color)
                    pygame.draw.rect(self.screen, glow_color,
                                   (x + j, y - j, bar_width - 2*j, bar_height + 2*j))
    
    def draw_equalizer(self, data):
        """Draw sinusoidal equalizer bands"""
        if len(data) == 0:
            return
        
        # Background
        self.screen.fill((5, 5, 20))
        
        # Perform FFT
        fft_data = np.fft.rfft(data)
        fft_magnitude = np.abs(fft_data)
        
        # Create frequency bands (equalizer style)
        num_bands = 32
        band_width = self.width // num_bands
        
        for i in range(num_bands):
            start_idx = i * len(fft_magnitude) // num_bands
            end_idx = (i + 1) * len(fft_magnitude) // num_bands
            band_magnitude = np.mean(fft_magnitude[start_idx:end_idx])
            
            # Apply sinusoidal modulation
            sine_mod = np.sin(i * 0.5 + self.color_cycle * 2)
            height = int(band_magnitude * 0.01 * self.height * (1 + sine_mod * 0.3))
            height = min(height, self.height - 50)
            
            # Color gradient
            color_list = list(NEON_COLORS.values())
            color = color_list[i % len(color_list)]
            
            x = i * band_width + band_width // 4
            y = self.height - height
            width = band_width // 2
            
            # Draw sinusoidal band
            points = []
            for py in range(height):
                wave_x = x + int(np.sin(py * 0.1 + self.color_cycle) * 5)
                points.append((wave_x, y + py))
                points.append((wave_x + width, y + py))
            
            if len(points) > 0:
                # Draw gradient filled polygon
                for py in range(0, height, 2):
                    ratio = py / height
                    glow_color = tuple(int(c * (1 - ratio * 0.7)) for c in color)
                    if py < len(points) // 2 - 2:
                        start_y = y + py
                        pygame.draw.line(self.screen, glow_color,
                                       (points[py*2][0], start_y),
                                       (points[py*2+1][0], start_y), 2)
    
    def draw_ui(self):
        """Draw UI controls"""
        font = pygame.font.Font(None, 24)
        
        # Mode indicator
        mode_text = f"Modo: {self.viz_mode.upper()}"
        text_surface = font.render(mode_text, True, NEON_COLORS['cyan'])
        self.screen.blit(text_surface, (10, 10))
        
        # Controls
        controls = [
            "W: Waveform | S: Spectrum | E: Equalizer",
            "SPACE: Pause | R: Reset | Q: Quit"
        ]
        for i, text in enumerate(controls):
            text_surface = font.render(text, True, NEON_COLORS['green'])
            self.screen.blit(text_surface, (10, 40 + i * 25))
        
        # Progress bar
        if len(self.audio_data) > 0:
            progress = self.current_frame / len(self.audio_data)
            bar_width = self.width - 40
            bar_height = 10
            bar_x = 20
            bar_y = self.height - 30
            
            # Background
            pygame.draw.rect(self.screen, (50, 50, 50),
                           (bar_x, bar_y, bar_width, bar_height))
            
            # Progress
            pygame.draw.rect(self.screen, NEON_COLORS['pink'],
                           (bar_x, bar_y, int(bar_width * progress), bar_height))
    
    def run(self, audio_file=None):
        """Main visualization loop"""
        if audio_file:
            if not self.load_audio(audio_file):
                print("No se pudo cargar el archivo de audio")
                return
        
        paused = False
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_w:
                        self.viz_mode = 'waveform'
                    elif event.key == pygame.K_s:
                        self.viz_mode = 'spectrum'
                    elif event.key == pygame.K_e:
                        self.viz_mode = 'equalizer'
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_r:
                        self.current_frame = 0
            
            if not paused and len(self.audio_data) > 0:
                # Get current chunk of audio data
                end_frame = min(self.current_frame + self.chunk_size, len(self.audio_data))
                chunk = self.audio_data[self.current_frame:end_frame]
                
                # Draw visualization based on mode
                if self.viz_mode == 'waveform':
                    self.draw_waveform(chunk)
                elif self.viz_mode == 'spectrum':
                    self.draw_spectrum(chunk)
                elif self.viz_mode == 'equalizer':
                    self.draw_equalizer(chunk)
                
                # Update frame position
                self.current_frame += self.chunk_size // 4  # Slower progression
                if self.current_frame >= len(self.audio_data):
                    self.current_frame = 0
                
                # Update color cycle for animations
                self.color_cycle += 0.05
            
            # Draw UI
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()


def main():
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        print("🌊 Visualizador de Audio")
        print("Uso: python audio_visualizer.py <archivo_audio>")
        print("\nBuscando archivos de audio...")
        
        downloads_dir = Path.home() / "ReproductorAlecksey" / "downloads"
        if downloads_dir.exists():
            audio_files = list(downloads_dir.glob('*.mp3')) + \
                         list(downloads_dir.glob('*.m4a')) + \
                         list(downloads_dir.glob('*.wav'))
            
            if audio_files:
                print("\nArchivos encontrados:")
                for i, f in enumerate(audio_files, 1):
                    print(f"{i}. {f.name}")
                
                choice = input("\nElige un archivo (número): ")
                try:
                    audio_file = str(audio_files[int(choice) - 1])
                except:
                    print("Selección inválida")
                    return
            else:
                print("No se encontraron archivos de audio")
                return
        else:
            print("No se encontró el directorio de descargas")
            return
    
    visualizer = AudioVisualizer()
    visualizer.run(audio_file)


if __name__ == "__main__":
    main()
