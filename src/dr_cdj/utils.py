"""Utility functions per Dr. CDJ."""

import os
import sys
import shutil
from pathlib import Path


def get_resource_path(filename: str) -> str:
    """Restituisce il path corretto per una risorsa.
    
    Ricerca ordine:
    1. Variabili d'ambiente DR_CDJ_FFMPEG_PATH / DR_CDJ_FFPROBE_PATH
    2. Directory 'bin' nel bundle PyInstaller
    3. Directory root del bundle PyInstaller
    4. PATH di sistema
    
    Args:
        filename: Nome del file (es. "ffmpeg", "ffprobe")
        
    Returns:
        Path completo al file o solo il filename se non trovato.
    """
    # 1. Variabili d'ambiente (priorità massima)
    env_var = f"DR_CDJ_{filename.upper()}_PATH"
    if env_var in os.environ:
        path = Path(os.environ[env_var])
        if path.exists():
            return str(path)
    
    # 2. Se in bundle PyInstaller, cerca nelle directory bundle
    if getattr(sys, 'frozen', False):
        # Determina la directory base
        if hasattr(sys, '_MEIPASS'):
            # _MEIPASS è la cartella temporanea dove PyInstaller estrae i file
            base_path = Path(sys._MEIPASS)
        else:
            # Fallback: directory dell'eseguibile
            base_path = Path(sys.executable).parent
        
        # Possibili locations per i binari (in ordine di priorità)
        possible_paths = [
            # Bundle subdirectory 'bin' (nuovo metodo con download-ffmpeg.py)
            base_path / "bin" / filename,
            # Root del bundle
            base_path / filename,
            # macOS .app bundle locations
            base_path.parent / "Resources" / "bin" / filename,
            base_path.parent / "Resources" / filename,
            base_path.parent / "MacOS" / "bin" / filename,
            base_path.parent / "MacOS" / filename,
            # Windows
            base_path / f"{filename}.exe",
            base_path / "bin" / f"{filename}.exe",
        ]
        
        for path in possible_paths:
            if path.exists():
                # Verifica che sia eseguibile (unix)
                if os.name != 'nt':
                    import stat
                    try:
                        st = os.stat(path)
                        if not st.st_mode & stat.S_IXUSR:
                            os.chmod(path, st.st_mode | stat.S_IXUSR)
                    except:
                        pass
                return str(path)
    
    # 3. Cerca nel PATH di sistema
    system_path = shutil.which(filename)
    if system_path:
        return system_path
    
    # 4. Fallback: restituisci il nome (permette errore graceful)
    return filename


def verify_ffmpeg(path: str) -> bool:
    """Verifica che il binario FFmpeg sia funzionante.
    
    Args:
        path: Path al binario ffmpeg
        
    Returns:
        True se il binario funziona, False altrimenti
    """
    try:
        import subprocess
        result = subprocess.run(
            [path, "-version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def get_ffmpeg_path() -> str:
    """Restituisce il path a ffmpeg.
    
    Returns:
        Path completo al binario ffmpeg
    """
    path = get_resource_path("ffmpeg")
    
    # Se il path bundled non funziona, prova il sistema
    if path != "ffmpeg" and not verify_ffmpeg(path):
        system_ffmpeg = shutil.which("ffmpeg")
        if system_ffmpeg and verify_ffmpeg(system_ffmpeg):
            return system_ffmpeg
    
    return path


def get_ffprobe_path() -> str:
    """Restituisce il path a ffprobe.
    
    Returns:
        Path completo al binario ffprobe
    """
    path = get_resource_path("ffprobe")
    
    # Se il path bundled non funziona, prova il sistema
    if path != "ffprobe" and not verify_ffmpeg(path):
        system_ffprobe = shutil.which("ffprobe")
        if system_ffprobe and verify_ffmpeg(system_ffprobe):
            return system_ffprobe
    
    return path


def get_binary_info() -> dict:
    """Restituisce informazioni sui binari FFmpeg trovati.
    
    Returns:
        Dict con info su ffmpeg e ffprobe
    """
    ffmpeg_path = get_ffmpeg_path()
    ffprobe_path = get_ffprobe_path()
    
    info = {
        "ffmpeg": {
            "path": ffmpeg_path,
            "bundled": ffmpeg_path != "ffmpeg" and shutil.which("ffmpeg") != ffmpeg_path,
            "working": verify_ffmpeg(ffmpeg_path) if ffmpeg_path else False,
        },
        "ffprobe": {
            "path": ffprobe_path,
            "bundled": ffprobe_path != "ffprobe" and shutil.which("ffprobe") != ffprobe_path,
            "working": verify_ffmpeg(ffprobe_path) if ffprobe_path else False,
        }
    }
    
    return info
