#!/usr/bin/env python3
"""
Dr. CDJ - Installer
=====================
Script di installazione automatica per Dr. CDJ.
Verifica Python, installa dipendenze e configura l'ambiente.
"""

import sys
import subprocess
import os
from pathlib import Path


MIN_PYTHON_VERSION = (3, 11)
REQUIRED_PACKAGES = [
    "customtkinter>=5.2.0",
    "tkinterdnd2>=0.3.0",
]


def check_python_version():
    """Verifica che Python sia installato e alla versione corretta."""
    print("🔍 Verifica Python...")
    
    version = sys.version_info
    current = (version.major, version.minor)
    
    if current < MIN_PYTHON_VERSION:
        print(f"""
❌ ERRORE: Versione Python non supportata
   Trovata: Python {version.major}.{version.minor}.{version.micro}
   Richiesta: Python >= {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}

📥 Per installare Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}:
   
   macOS:
     brew install python@{MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}
   
   Linux (Ubuntu/Debian):
     sudo apt-get install python{MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}
   
   Windows:
     Scarica da https://python.org/downloads/
        """)
        return False
    
    print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} trovato")
    return True


def check_ffmpeg():
    """Verifica che FFmpeg sia installato."""
    print("\n🔍 Verifica FFmpeg...")
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"   ✅ {version_line}")
            return True
    except FileNotFoundError:
        pass
    except Exception:
        pass
    
    print("""
⚠️  FFmpeg non trovato!

📥 Installazione richiesta:

   macOS:
     brew install ffmpeg
   
   Linux (Ubuntu/Debian):
     sudo apt-get update
     sudo apt-get install ffmpeg
   
   Windows:
     Scarica da https://ffmpeg.org/download.html
     Aggiungi al PATH di sistema
    """)
    return False


def install_dependencies():
    """Installa le dipendenze Python necessarie."""
    print("\n📦 Installazione dipendenze...")
    
    for package in REQUIRED_PACKAGES:
        print(f"   Installazione {package}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", package],
                check=True
            )
            print(f"   ✅ {package} installato")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Errore installazione {package}: {e}")
            return False
    
    return True


def install_package():
    """Installa il pacchetto CDJ-Check in modalità sviluppo."""
    print("\n🔧 Installazione Dr. CDJ...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-e", "."],
            check=True
        )
        print("   ✅ Dr. CDJ installato")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Errore: {e}")
        return False


def create_launcher():
    """Crea uno script di avvio."""
    print("\n🚀 Creazione launcher...")
    
    launcher_content = """#!/bin/bash
# Dr. CDJ Launcher
cd "$(dirname "$0")"
python3 -m dr_cdj.gui
"""
    
    launcher_path = Path("dr-cdj.sh")
    with open(launcher_path, "w") as f:
        f.write(launcher_content)
    
    # Rendi eseguibile
    os.chmod(launcher_path, 0o755)
    print(f"   ✅ Launcher creato: {launcher_path.absolute()}")
    
    # Crea anche .command per macOS (doppio click)
    command_content = """#!/bin/bash
# Dr. CDJ - Doppio click per avviare
cd "$(dirname "$0")"
python3 -m dr_cdj.gui &
"""
    
    command_path = Path("Dr-CDJ.command")
    with open(command_path, "w") as f:
        f.write(command_content)
    
    os.chmod(command_path, 0o755)
    print(f"   ✅ Launcher macOS creato: {command_path.absolute()}")


def main():
    """Funzione principale."""
    print("""
╔═══════════════════════════════════════════╗
║         Dr. CDJ Installer                 ║
║    Audio Compatibility Checker            ║
╚═══════════════════════════════════════════╝
""")
    
    # Verifica Python
    if not check_python_version():
        sys.exit(1)
    
    # Verifica FFmpeg
    ffmpeg_ok = check_ffmpeg()
    
    # Installa dipendenze
    if not install_dependencies():
        print("\n❌ Installazione fallita")
        sys.exit(1)
    
    # Installa pacchetto
    if not install_package():
        print("\n❌ Installazione fallita")
        sys.exit(1)
    
    # Crea launcher
    create_launcher()
    
    # Riepilogo
    print("""
╔═══════════════════════════════════════════╗
║     ✅ Installazione Completata!          ║
╚═══════════════════════════════════════════╝

🎵 Per avviare Dr. CDJ:

   Terminale:
     dr-cdj
     # oppure
     python3 -m dr_cdj.gui

   Doppio click (macOS):
     Dr-CDJ.command

📁 File creati:
   • dr-cdj.sh      - Launcher Linux/macOS
   • Dr-CDJ.command - Launcher macOS (doppio click)
""")
    
    if not ffmpeg_ok:
        print("""
⚠️  ATTENZIONE: FFmpeg non è installato!
    L'app si avvierà ma non potrà analizzare/convertire file.
    
    Installa FFmpeg per il funzionamento completo.
""")


if __name__ == "__main__":
    main()
