#!/usr/bin/env python3
"""
Installation and Setup Script for ReproductorAlecksey
"""

import subprocess
import sys
import platform
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich import box

console = Console()

def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        console.print("[red]❌ Python 3.8 or higher is required[/red]")
        console.print(f"[yellow]Current version: {version.major}.{version.minor}.{version.micro}[/yellow]")
        return False
    console.print(f"[green]✅ Python {version.major}.{version.minor}.{version.micro}[/green]")
    return True

def check_pip():
    """Check if pip is installed"""
    try:
        subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                      capture_output=True, check=True)
        console.print("[green]✅ pip está instalado[/green]")
        return True
    except:
        console.print("[red]❌ pip no está instalado[/red]")
        return False

def install_requirements():
    """Install Python requirements"""
    console.print("\n[bold cyan]📦 Instalando dependencias de Python...[/bold cyan]")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Instalando paquetes...", total=None)
            
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print("[green]✅ Dependencias instaladas correctamente[/green]")
                return True
            else:
                console.print("[red]❌ Error instalando dependencias[/red]")
                console.print(result.stderr)
                return False
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return False

def check_ytdlp():
    """Check if yt-dlp is installed"""
    try:
        result = subprocess.run(['yt-dlp', '--version'], 
                               capture_output=True, text=True, check=True)
        console.print(f"[green]✅ yt-dlp {result.stdout.strip()}[/green]")
        return True
    except:
        console.print("[yellow]⚠️  yt-dlp no está instalado[/yellow]")
        return False

def install_ytdlp():
    """Install yt-dlp"""
    console.print("\n[bold cyan]📦 Instalando yt-dlp...[/bold cyan]")
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'yt-dlp'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print("[green]✅ yt-dlp instalado correctamente[/green]")
            return True
        else:
            console.print("[red]❌ Error instalando yt-dlp[/red]")
            return False
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                               capture_output=True, text=True, check=True)
        version_line = result.stdout.split('\n')[0]
        console.print(f"[green]✅ {version_line}[/green]")
        return True
    except:
        console.print("[yellow]⚠️  FFmpeg no está instalado[/yellow]")
        return False

def show_ffmpeg_instructions():
    """Show FFmpeg installation instructions"""
    system = platform.system()
    
    console.print("\n[bold yellow]📝 Instrucciones para instalar FFmpeg:[/bold yellow]\n")
    
    if system == "Linux":
        console.print("[cyan]Ubuntu/Debian:[/cyan]")
        console.print("  sudo apt-get update")
        console.print("  sudo apt-get install ffmpeg")
        console.print("\n[cyan]Fedora:[/cyan]")
        console.print("  sudo dnf install ffmpeg")
        console.print("\n[cyan]Arch:[/cyan]")
        console.print("  sudo pacman -S ffmpeg")
    elif system == "Darwin":
        console.print("[cyan]macOS (usando Homebrew):[/cyan]")
        console.print("  brew install ffmpeg")
    elif system == "Windows":
        console.print("[cyan]Windows:[/cyan]")
        console.print("  1. Descarga FFmpeg desde: https://ffmpeg.org/download.html")
        console.print("  2. Extrae el archivo ZIP")
        console.print("  3. Agrega la carpeta 'bin' al PATH del sistema")
    else:
        console.print(f"[yellow]Sistema operativo: {system}[/yellow]")
        console.print("Visita: https://ffmpeg.org/download.html")

def create_directories():
    """Create necessary directories"""
    downloads_dir = Path.home() / "ReproductorAlecksey" / "downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]✅ Directorio de descargas: {downloads_dir}[/green]")

def main():
    console.print(Panel(
        "[bold magenta]🎵 ReproductorAlecksey - Instalador 🎵[/bold magenta]",
        border_style="cyan",
        box=box.DOUBLE
    ))
    
    console.print("\n[bold]Verificando requisitos del sistema...[/bold]\n")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check pip
    if not check_pip():
        console.print("[red]Por favor instala pip primero[/red]")
        return
    
    # Check if we should install requirements
    console.print("\n[bold]Verificando dependencias...[/bold]\n")
    
    if Confirm.ask("[bold cyan]¿Instalar dependencias de Python?[/bold cyan]", default=True):
        if not install_requirements():
            console.print("[yellow]Algunas dependencias pueden no haberse instalado correctamente[/yellow]")
    
    # Check yt-dlp
    console.print("\n[bold]Verificando yt-dlp...[/bold]\n")
    if not check_ytdlp():
        if Confirm.ask("[bold cyan]¿Instalar yt-dlp?[/bold cyan]", default=True):
            install_ytdlp()
    
    # Check FFmpeg
    console.print("\n[bold]Verificando FFmpeg...[/bold]\n")
    if not check_ffmpeg():
        show_ffmpeg_instructions()
        console.print("\n[yellow]⚠️  FFmpeg es requerido para la conversión de audio[/yellow]")
    
    # Create directories
    console.print("\n[bold]Creando directorios...[/bold]\n")
    create_directories()
    
    # Final summary
    console.print("\n")
    console.print(Panel(
        "[bold green]✅ ¡Instalación completada![/bold green]\n\n"
        "Para comenzar, ejecuta:\n"
        "  [cyan]python launcher.py[/cyan]\n\n"
        "O consulta la guía rápida:\n"
        "  [cyan]python QUICKSTART.py[/cyan]",
        border_style="green",
        box=box.DOUBLE
    ))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Instalación cancelada[/red]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
