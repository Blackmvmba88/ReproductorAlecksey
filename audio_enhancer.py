#!/usr/bin/env python3
"""
Audio Enhancement Module
Features: Noise reduction, equalization, normalization
"""

import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from pathlib import Path

class AudioEnhancer:
    def __init__(self):
        self.sample_rate = 44100
    
    def load_audio(self, file_path):
        """Load audio file"""
        try:
            audio = AudioSegment.from_file(str(file_path))
            return audio
        except Exception as e:
            print(f"Error loading audio: {e}")
            return None
    
    def normalize_audio(self, audio):
        """Normalize audio levels"""
        return normalize(audio)
    
    def apply_bass_boost(self, audio, gain=10):
        """Boost bass frequencies"""
        # Simple bass boost by applying low-pass filter effect
        # This is a simplified version
        return audio.low_pass_filter(200).apply_gain(gain) + audio
    
    def apply_treble_boost(self, audio, gain=5):
        """Boost treble frequencies"""
        # Simple treble boost
        return audio.high_pass_filter(2000).apply_gain(gain) + audio
    
    def compress_audio(self, audio):
        """Apply dynamic range compression"""
        return compress_dynamic_range(audio)
    
    def enhance_audio(self, input_file, output_file=None, 
                     normalize_audio=True, 
                     bass_boost=False, 
                     treble_boost=False,
                     compress=False):
        """
        Apply audio enhancements
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output file (optional)
            normalize_audio: Apply normalization
            bass_boost: Apply bass boost
            treble_boost: Apply treble boost
            compress: Apply dynamic range compression
        
        Returns:
            Path to enhanced audio file
        """
        input_path = Path(input_file)
        
        if output_file is None:
            output_file = input_path.parent / f"{input_path.stem}_enhanced{input_path.suffix}"
        
        print(f"🎧 Cargando audio: {input_path.name}")
        audio = self.load_audio(input_file)
        
        if audio is None:
            return None
        
        print("⚡ Aplicando mejoras...")
        
        if normalize_audio:
            print("  📊 Normalizando...")
            audio = self.normalize_audio(audio)
        
        if bass_boost:
            print("  🔊 Aumentando graves...")
            audio = self.apply_bass_boost(audio)
        
        if treble_boost:
            print("  🎵 Aumentando agudos...")
            audio = self.apply_treble_boost(audio)
        
        if compress:
            print("  🎚️  Comprimiendo rango dinámico...")
            audio = self.compress_audio(audio)
        
        print(f"💾 Guardando: {Path(output_file).name}")
        audio.export(output_file, format=input_path.suffix[1:])
        
        print(f"✅ Audio mejorado guardado en: {output_file}")
        return output_file


def main():
    import sys
    
    enhancer = AudioEnhancer()
    
    if len(sys.argv) < 2:
        print("🎧 Audio Enhancer")
        print("Uso: python audio_enhancer.py <archivo_audio> [opciones]")
        print("\nOpciones:")
        print("  --normalize    : Normalizar niveles de audio")
        print("  --bass-boost   : Aumentar graves")
        print("  --treble-boost : Aumentar agudos")
        print("  --compress     : Comprimir rango dinámico")
        print("  --all          : Aplicar todas las mejoras")
        return
    
    input_file = sys.argv[1]
    
    # Parse options
    options = {
        'normalize_audio': '--normalize' in sys.argv or '--all' in sys.argv,
        'bass_boost': '--bass-boost' in sys.argv or '--all' in sys.argv,
        'treble_boost': '--treble-boost' in sys.argv or '--all' in sys.argv,
        'compress': '--compress' in sys.argv or '--all' in sys.argv
    }
    
    if not any(options.values()):
        # Default: only normalize
        options['normalize_audio'] = True
    
    enhancer.enhance_audio(input_file, **options)


if __name__ == "__main__":
    main()
