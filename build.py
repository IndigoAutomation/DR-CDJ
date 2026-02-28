#!/usr/bin/env python3
"""Script di build per CDJ-Check usando PyInstaller."""

import platform
import shutil
import subprocess
import sys
from pathlib import Path


def check_pyinstaller():
    """Verifica che PyInstaller sia installato."""
    if not shutil.which("pyinstaller"):
        print("❌ PyInstaller non trovato.")
        print("Installa con: pip install pyinstaller")
        sys.exit(1)


def get_ffmpeg_paths():
    """Trova ffmpeg e ffprobe."""
    system = platform.system()
    
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    
    if not ffmpeg or not ffprobe:
        print("❌ FFmpeg o ffprobe non trovati nel PATH.")
        print("Installa FFmpeg prima di continuare.")
        sys.exit(1)
    
    return ffmpeg, ffprobe


def build_macos():
    """Build per macOS (.app bundle)."""
    print("🍎 Build per macOS...")
    
    ffmpeg, ffprobe = get_ffmpeg_paths()
    
    cmd = [
        "pyinstaller",
        "--name", "CDJ-Check",
        "--windowed",
        "--onefile",
        "--clean",
        "--noconfirm",
        # Aggiungi ffmpeg e ffprobe come dati binari
        "--add-binary", f"{ffmpeg}:.",
        "--add-binary", f"{ffprobe}:.",
        # Hook personalizzato
        "--additional-hooks-dir", "hooks",
        # Icona (se esiste)
        # "--icon", "assets/icon.icns",
        # Nascondi terminale
        "--osx-bundle-identifier", "com.cdjcheck.app",
        "src/cdj_check/main.py",
    ]
    
    print(f"Eseguendo: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print("❌ Build fallito!")
        sys.exit(1)
    
    print("✅ Build completato!")
    print("Output: dist/CDJ-Check.app")


def build_windows():
    """Build per Windows (.exe)."""
    print("🪟 Build per Windows...")
    
    ffmpeg, ffprobe = get_ffmpeg_paths()
    
    cmd = [
        "pyinstaller",
        "--name", "CDJ-Check",
        "--windowed",
        "--onefile",
        "--clean",
        "--noconfirm",
        "--add-binary", f"{ffmpeg};.",
        "--add-binary", f"{ffprobe};.",
        "--additional-hooks-dir", "hooks",
        # "--icon", "assets/icon.ico",
        "src/cdj_check/main.py",
    ]
    
    print(f"Eseguendo: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print("❌ Build fallito!")
        sys.exit(1)
    
    print("✅ Build completato!")
    print("Output: dist/CDJ-Check.exe")


def build_linux():
    """Build per Linux (eseguibile)."""
    print("🐧 Build per Linux...")
    
    ffmpeg, ffprobe = get_ffmpeg_paths()
    
    cmd = [
        "pyinstaller",
        "--name", "CDJ-Check",
        "--windowed",
        "--onefile",
        "--clean",
        "--noconfirm",
        "--add-binary", f"{ffmpeg}:.",
        "--add-binary", f"{ffprobe}:.",
        "--additional-hooks-dir", "hooks",
        "src/cdj_check/main.py",
    ]
    
    print(f"Eseguendo: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print("❌ Build fallito!")
        sys.exit(1)
    
    print("✅ Build completato!")
    print("Output: dist/CDJ-Check")


def main():
    """Entry point."""
    check_pyinstaller()
    
    system = platform.system()
    
    if system == "Darwin":
        build_macos()
    elif system == "Windows":
        build_windows()
    elif system == "Linux":
        build_linux()
    else:
        print(f"❌ Sistema operativo non supportato: {system}")
        sys.exit(1)


if __name__ == "__main__":
    main()
