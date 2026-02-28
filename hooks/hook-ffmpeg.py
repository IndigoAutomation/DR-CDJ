"""Hook PyInstaller per includere FFmpeg e ffprobe."""

import os
import platform
import shutil
import sys
from pathlib import Path


def get_ffmpeg_paths():
    """Trova i path di ffmpeg e ffprobe."""
    system = platform.system()
    
    # Cerca nei path comuni
    possible_paths = []
    
    if system == "Darwin":  # macOS
        possible_paths = [
            "/opt/homebrew/bin",  # Apple Silicon
            "/usr/local/bin",      # Intel
        ]
    elif system == "Windows":
        possible_paths = [
            r"C:\Program Files\ffmpeg\bin",
            r"C:\ffmpeg\bin",
        ]
    else:  # Linux
        possible_paths = [
            "/usr/bin",
            "/usr/local/bin",
        ]
    
    ffmpeg_path = None
    ffprobe_path = None
    
    # Cerca nei path
    for base_path in possible_paths:
        if not Path(base_path).exists():
            continue
            
        ffmpeg = Path(base_path) / ("ffmpeg.exe" if system == "Windows" else "ffmpeg")
        ffprobe = Path(base_path) / ("ffprobe.exe" if system == "Windows" else "ffprobe")
        
        if ffmpeg.exists() and ffprobe.exists():
            ffmpeg_path = str(ffmpeg)
            ffprobe_path = str(ffprobe)
            break
    
    # Fallback: cerca nel PATH
    if not ffmpeg_path:
        ffmpeg_path = shutil.which("ffmpeg")
        ffprobe_path = shutil.which("ffprobe")
    
    return ffmpeg_path, ffprobe_path


def install_ffmpeg_binaries():
    """Restituisce i binari da includere."""
    ffmpeg, ffprobe = get_ffmpeg_paths()
    
    binaries = []
    
    if ffmpeg:
        binaries.append((ffmpeg, "."))
        print(f"Hook: includendo ffmpeg da {ffmpeg}")
    else:
        print("Hook: WARNING - ffmpeg non trovato!")
    
    if ffprobe:
        binaries.append((ffprobe, "."))
        print(f"Hook: includendo ffprobe da {ffprobe}")
    else:
        print("Hook: WARNING - ffprobe non trovato!")
    
    return binaries


# Esporta per PyInstaller
binaries = install_ffmpeg_binaries()
datas = []
