#!/usr/bin/env python3
"""
ReproductorAlecksey - Terminal-based Media Player with yt-dlp
Features: Video download, preview, audio visualization, and neon theme
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich import box
from rich.style import Style
import time

console = Console()

# Neon color theme
NEON_COLORS = {
    'pink': '#FF10F0',
    'cyan': '#00FFFF',
    'green': '#39FF14',
    'yellow': '#FFFF00',
    'orange': '#FF6600',
    'purple': '#BF00FF',
    'blue': '#1B03A3'
}

class ReproductorAlecksey:
    def __init__(self):
        self.downloads_dir = Path.home() / "ReproductorAlecksey" / "downloads"
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.current_playlist = []
        
    def show_banner(self):
        """Display neon-themed banner"""
        banner = """
 ██████╗ ███████╗██████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗ ██████╗████████╗ ██████╗ ██████╗ 
 ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
 ██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██║  ██║██║   ██║██║        ██║   ██║   ██║██████╔╝
 ██╔══██╗██╔══╝  ██╔═══╝ ██╔══██╗██║   ██║██║  ██║██║   ██║██║        ██║   ██║   ██║██╔══██╗
 ██║  ██║███████╗██║     ██║  ██║╚██████╔╝██████╔╝╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
 ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
        """
        console.print(Panel(
            Text(banner, style=f"bold {NEON_COLORS['cyan']}"),
            title="[bold magenta]🎵 Alecksey Media Player 🎵[/bold magenta]",
            subtitle="[bold cyan]v1.0 - Neon Edition[/bold cyan]",
            border_style=NEON_COLORS['pink'],
            box=box.DOUBLE
        ))
    
    def check_ytdlp(self):
        """Check if yt-dlp is available"""
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                   capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("[red]⚠️  yt-dlp no está instalado![/red]")
            console.print("[yellow]Instala con: pip install yt-dlp[/yellow]")
            return False
    
    def get_video_info(self, url):
        """Get video information using yt-dlp"""
        try:
            cmd = [
                'yt-dlp',
                '--dump-json',
                '--no-playlist',
                url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'thumbnail': info.get('thumbnail', ''),
                'description': info.get('description', '')[:200] + '...',
                'formats': len(info.get('formats', []))
            }
        except Exception as e:
            console.print(f"[red]Error obteniendo información: {e}[/red]")
            return None
    
    def preview_video(self, url):
        """Show video preview/information"""
        console.print(Panel(
            "[bold cyan]🔍 Obteniendo información del video...[/bold cyan]",
            border_style=NEON_COLORS['cyan']
        ))
        
        info = self.get_video_info(url)
        if not info:
            return False
        
        # Create preview table with neon styling
        table = Table(
            title="[bold magenta]📹 Preview del Video[/bold magenta]",
            box=box.DOUBLE_EDGE,
            border_style=NEON_COLORS['pink'],
            header_style=f"bold {NEON_COLORS['cyan']}"
        )
        
        table.add_column("Propiedad", style=NEON_COLORS['yellow'])
        table.add_column("Valor", style=NEON_COLORS['green'])
        
        table.add_row("🎬 Título", info['title'])
        table.add_row("⏱️  Duración", f"{info['duration'] // 60}:{info['duration'] % 60:02d}")
        table.add_row("👤 Autor", info['uploader'])
        table.add_row("👁️  Vistas", f"{info['view_count']:,}")
        table.add_row("🎥 Formatos", str(info['formats']))
        table.add_row("📝 Descripción", info['description'])
        
        console.print(table)
        return True
    
    def download_video(self, url, format_choice='best'):
        """Download video using yt-dlp with progress"""
        output_template = str(self.downloads_dir / '%(title)s.%(ext)s')
        
        cmd = [
            'yt-dlp',
            '-f', format_choice,
            '-o', output_template,
            '--newline',
            url
        ]
        
        console.print(Panel(
            f"[bold {NEON_COLORS['cyan']}]⬇️  Descargando...[/bold {NEON_COLORS['cyan']}]",
            border_style=NEON_COLORS['green']
        ))
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    # Display download progress with neon colors
                    if '[download]' in line:
                        console.print(f"[{NEON_COLORS['cyan']}]{line}[/{NEON_COLORS['cyan']}]")
                    else:
                        console.print(f"[dim]{line}[/dim]")
            
            process.wait()
            
            if process.returncode == 0:
                console.print(Panel(
                    "[bold green]✅ ¡Descarga completada![/bold green]",
                    border_style=NEON_COLORS['green']
                ))
                return True
            else:
                console.print(Panel(
                    "[bold red]❌ Error en la descarga[/bold red]",
                    border_style="red"
                ))
                return False
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return False
    
    def list_downloads(self):
        """List downloaded files"""
        files = list(self.downloads_dir.glob('*'))
        media_files = [f for f in files if f.suffix.lower() in ['.mp4', '.mp3', '.webm', '.mkv', '.m4a']]
        
        if not media_files:
            console.print(Panel(
                "[yellow]📂 No hay archivos descargados aún[/yellow]",
                border_style=NEON_COLORS['yellow']
            ))
            return
        
        table = Table(
            title="[bold magenta]📁 Archivos Descargados[/bold magenta]",
            box=box.DOUBLE_EDGE,
            border_style=NEON_COLORS['pink']
        )
        
        table.add_column("#", style=NEON_COLORS['cyan'])
        table.add_column("Archivo", style=NEON_COLORS['green'])
        table.add_column("Tamaño", style=NEON_COLORS['yellow'])
        
        for idx, file in enumerate(media_files, 1):
            size_mb = file.stat().st_size / (1024 * 1024)
            table.add_row(str(idx), file.name, f"{size_mb:.2f} MB")
        
        console.print(table)
    
    def show_main_menu(self):
        """Display main menu with neon styling"""
        menu = Table(
            title="[bold magenta]🎮 MENÚ PRINCIPAL[/bold magenta]",
            box=box.HEAVY,
            border_style=NEON_COLORS['pink'],
            show_header=False
        )
        
        menu.add_column("Opción", style=f"bold {NEON_COLORS['cyan']}")
        menu.add_column("Descripción", style=NEON_COLORS['green'])
        
        menu.add_row("1", "🔗 Descargar video (URL)")
        menu.add_row("2", "📋 Ver archivos descargados")
        menu.add_row("3", "🎵 Reproducir archivo local")
        menu.add_row("4", "🌊 Visualizador de audio")
        menu.add_row("5", "🌐 Iniciar Web UI")
        menu.add_row("6", "ℹ️  Información del sistema")
        menu.add_row("0", "❌ Salir")
        
        console.print(menu)
    
    def system_info(self):
        """Show system information"""
        table = Table(
            title="[bold cyan]ℹ️  Información del Sistema[/bold cyan]",
            box=box.DOUBLE_EDGE,
            border_style=NEON_COLORS['cyan']
        )
        
        table.add_column("Componente", style=NEON_COLORS['yellow'])
        table.add_column("Estado", style=NEON_COLORS['green'])
        
        # Check yt-dlp
        ytdlp_status = "✅ Instalado" if self.check_ytdlp() else "❌ No disponible"
        table.add_row("yt-dlp", ytdlp_status)
        
        # Check downloads directory
        table.add_row("Directorio de descargas", str(self.downloads_dir))
        
        # Count downloaded files
        files = list(self.downloads_dir.glob('*'))
        media_files = [f for f in files if f.suffix.lower() in ['.mp4', '.mp3', '.webm', '.mkv']]
        table.add_row("Archivos descargados", str(len(media_files)))
        
        console.print(table)
    
    def run(self):
        """Main application loop"""
        if not self.check_ytdlp():
            console.print("[red]Por favor instala yt-dlp primero[/red]")
            return
        
        while True:
            console.clear()
            self.show_banner()
            self.show_main_menu()
            
            choice = Prompt.ask(
                f"[bold {NEON_COLORS['pink']}]Elige una opción[/bold {NEON_COLORS['pink']}]",
                choices=["0", "1", "2", "3", "4", "5", "6"],
                default="1"
            )
            
            if choice == "0":
                console.print(Panel(
                    "[bold cyan]👋 ¡Hasta luego![/bold cyan]",
                    border_style=NEON_COLORS['cyan']
                ))
                break
            
            elif choice == "1":
                url = Prompt.ask(f"[bold {NEON_COLORS['cyan']}]🔗 Ingresa la URL[/bold {NEON_COLORS['cyan']}]")
                if url:
                    # Show preview first
                    if self.preview_video(url):
                        if Confirm.ask(f"[bold {NEON_COLORS['green']}]¿Descargar este video?[/bold {NEON_COLORS['green']}]"):
                            format_choice = Prompt.ask(
                                f"[bold {NEON_COLORS['yellow']}]Formato[/bold {NEON_COLORS['yellow']}]",
                                choices=["best", "bestvideo+bestaudio", "bestaudio"],
                                default="best"
                            )
                            self.download_video(url, format_choice)
                            Prompt.ask(f"[dim]Presiona Enter para continuar...[/dim]")
            
            elif choice == "2":
                self.list_downloads()
                Prompt.ask(f"[dim]Presiona Enter para continuar...[/dim]")
            
            elif choice == "3":
                console.print(Panel(
                    "[yellow]🎵 Reproductor de archivos locales - Próximamente[/yellow]",
                    border_style=NEON_COLORS['yellow']
                ))
                Prompt.ask(f"[dim]Presiona Enter para continuar...[/dim]")
            
            elif choice == "4":
                console.print(Panel(
                    "[yellow]🌊 Visualizador de audio - Ver audio_visualizer.py[/yellow]",
                    border_style=NEON_COLORS['yellow']
                ))
                Prompt.ask(f"[dim]Presiona Enter para continuar...[/dim]")
            
            elif choice == "5":
                console.print(Panel(
                    "[yellow]🌐 Web UI - Ver web_ui.py[/yellow]",
                    border_style=NEON_COLORS['yellow']
                ))
                Prompt.ask(f"[dim]Presiona Enter para continuar...[/dim]")
            
            elif choice == "6":
                self.system_info()
                Prompt.ask(f"[dim]Presiona Enter para continuar...[/dim]")


def main():
    try:
        app = ReproductorAlecksey()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[bold red]Programa interrumpido[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


if __name__ == "__main__":
    main()
