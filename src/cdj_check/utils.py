"""Utility functions per CDJ-Check."""

import sys
from pathlib import Path


def get_resource_path(filename: str) -> str:
    """Restituisce il path corretto per una risorsa.
    
    Quando l'app è frozen (PyInstaller), cerca nella directory dell'eseguibile.
    Altrimenti, restituisce il nome del file (assume sia nel PATH).
    
    Args:
        filename: Nome del file (es. "ffmpeg", "ffprobe")
        
    Returns:
        Path completo al file o solo il filename se non trovato.
    """
    # Determina la directory base
    if getattr(sys, 'frozen', False):
        # Siamo in un bundle (PyInstaller)
        # PyInstaller crea un temp folder e memorizza il path in _MEIPASS
        # o sys.executable è l'eseguibile stesso
        if hasattr(sys, '_MEIPASS'):
            # _MEIPASS è la cartella temporanea dove PyInstaller estrae i file
            base_path = Path(sys._MEIPASS)
        else:
            # Fallback: directory dell'eseguibile
            base_path = Path(sys.executable).parent
        
        # Su macOS, l'eseguibile è in CDJ-Check.app/Contents/MacOS/
        # I binari potrebbero essere lì o in Resources/
        possible_paths = [
            base_path / filename,
            base_path.parent / "Resources" / filename,
            base_path.parent / "MacOS" / filename,
            base_path / f"{filename}.exe",  # Windows
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
    
    # Se non frozen o file non trovato, restituisci il nome
    # (assume sia nel PATH di sistema)
    return filename


def get_ffmpeg_path() -> str:
    """Restituisce il path a ffmpeg."""
    return get_resource_path("ffmpeg")


def get_ffprobe_path() -> str:
    """Restituisce il path a ffprobe."""
    return get_resource_path("ffprobe")
