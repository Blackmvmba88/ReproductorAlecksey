#!/usr/bin/env python3
"""
ReproductorAlecksey - Launcher
Quick access to all features
"""

import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console()

NEON_COLORS = {
    'pink': '#FF10F0',
    'cyan': '#00FFFF',
    'green': '#39FF14',
    'yellow': '#FFFF00',
}

def show_banner():
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎵  REPRODUCTOR ALECKSEY - NEON EDITION  🎵            ║
║                                                           ║
║        Multimedia Player & Downloader Suite               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    console.print(Panel(
        banner,
        border_style=NEON_COLORS['pink'],
        box=box.DOUBLE
    ))

def show_menu():
    table = Table(
        title="[bold magenta]🚀 LAUNCHER - Elige un Modo[/bold magenta]",
        box=box.HEAVY,
        border_style=NEON_COLORS['cyan']
    )
    
    table.add_column("Opción", style=f"bold {NEON_COLORS['pink']}")
    table.add_column("Descripción", style=NEON_COLORS['green'])
    table.add_column("Comando", style=NEON_COLORS['yellow'])
    
    table.add_row("1", "💻 Terminal UI", "python reproductor.py")
    table.add_row("2", "🌐 Web UI", "python web_ui.py")
    table.add_row("3", "🌊 Visualizador de Audio", "python audio_visualizer.py")
    table.add_row("4", "🎧 Mejorador de Audio", "python audio_enhancer.py")
    table.add_row("5", "📚 Ver README", "Mostrar documentación")
    table.add_row("0", "❌ Salir", "Exit")
    
    console.print(table)

def launch_terminal():
    """Launch terminal UI"""
    subprocess.run([sys.executable, "reproductor.py"])

def launch_web():
    """Launch web UI"""
    subprocess.run([sys.executable, "web_ui.py"])

def launch_visualizer():
    """Launch audio visualizer"""
    # Check for audio files
    downloads_dir = Path.home() / "ReproductorAlecksey" / "downloads"
    if downloads_dir.exists():
        audio_files = (list(downloads_dir.glob('*.mp3')) + 
                      list(downloads_dir.glob('*.m4a')) + 
                      list(downloads_dir.glob('*.wav')))
        
        if audio_files:
            console.print("[bold cyan]Archivos de audio encontrados:[/bold cyan]")
            for i, f in enumerate(audio_files[:10], 1):
                console.print(f"  {i}. {f.name}")
            
            choice = Prompt.ask(
                "[bold yellow]Elige un archivo (número) o presiona Enter para elegir manualmente[/bold yellow]",
                default=""
            )
            
            if choice.isdigit() and 1 <= int(choice) <= len(audio_files):
                subprocess.run([sys.executable, "audio_visualizer.py", str(audio_files[int(choice)-1])])
            else:
                subprocess.run([sys.executable, "audio_visualizer.py"])
        else:
            subprocess.run([sys.executable, "audio_visualizer.py"])
    else:
        subprocess.run([sys.executable, "audio_visualizer.py"])

def launch_enhancer():
    """Launch audio enhancer"""
    downloads_dir = Path.home() / "ReproductorAlecksey" / "downloads"
    if downloads_dir.exists():
        audio_files = (list(downloads_dir.glob('*.mp3')) + 
                      list(downloads_dir.glob('*.m4a')) + 
                      list(downloads_dir.glob('*.wav')))
        
        if audio_files:
            console.print("[bold cyan]Archivos de audio encontrados:[/bold cyan]")
            for i, f in enumerate(audio_files[:10], 1):
                console.print(f"  {i}. {f.name}")
            
            choice = Prompt.ask(
                "[bold yellow]Elige un archivo (número)[/bold yellow]"
            )
            
            if choice.isdigit() and 1 <= int(choice) <= len(audio_files):
                file_path = str(audio_files[int(choice)-1])
                
                console.print("[bold green]Opciones de mejora:[/bold green]")
                console.print("  1. Solo normalizar")
                console.print("  2. Normalizar + Bass boost")
                console.print("  3. Normalizar + Treble boost")
                console.print("  4. Todas las mejoras")
                
                opt = Prompt.ask("[bold yellow]Elige opción[/bold yellow]", choices=["1", "2", "3", "4"], default="1")
                
                if opt == "1":
                    subprocess.run([sys.executable, "audio_enhancer.py", file_path, "--normalize"])
                elif opt == "2":
                    subprocess.run([sys.executable, "audio_enhancer.py", file_path, "--normalize", "--bass-boost"])
                elif opt == "3":
                    subprocess.run([sys.executable, "audio_enhancer.py", file_path, "--normalize", "--treble-boost"])
                elif opt == "4":
                    subprocess.run([sys.executable, "audio_enhancer.py", file_path, "--all"])
            else:
                console.print("[red]Selección inválida[/red]")
        else:
            console.print("[yellow]No se encontraron archivos de audio.[/yellow]")
            console.print("Uso manual: python audio_enhancer.py <archivo> [opciones]")
    else:
        console.print("[yellow]Directorio de descargas no encontrado.[/yellow]")
        console.print("Uso manual: python audio_enhancer.py <archivo> [opciones]")

def show_readme():
    """Show README content"""
    readme_path = Path("README.md")
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            console.print(Panel(
                content,
                title="[bold cyan]📚 README[/bold cyan]",
                border_style=NEON_COLORS['green']
            ))
    else:
        console.print("[red]README.md no encontrado[/red]")

def main():
    while True:
        console.clear()
        show_banner()
        show_menu()
        
        choice = Prompt.ask(
            f"[bold {NEON_COLORS['pink']}]Elige una opción[/bold {NEON_COLORS['pink']}]",
            choices=["0", "1", "2", "3", "4", "5"],
            default="1"
        )
        
        if choice == "0":
            console.print(Panel(
                "[bold cyan]👋 ¡Hasta luego![/bold cyan]",
                border_style=NEON_COLORS['cyan']
            ))
            break
        elif choice == "1":
            launch_terminal()
        elif choice == "2":
            launch_web()
        elif choice == "3":
            launch_visualizer()
        elif choice == "4":
            launch_enhancer()
        elif choice == "5":
            show_readme()
            Prompt.ask("[dim]Presiona Enter para continuar...[/dim]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Programa interrumpido[/bold red]")
