"""Utility functions for Dr. CDJ."""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def verify_ffmpeg(path: str) -> bool:
    """Verify FFmpeg binary is working.
    
    Args:
        path: Path to ffmpeg binary
        
    Returns:
        True if binary works, False otherwise
    """
    if not path or path in ("ffmpeg", "ffprobe"):
        return False
    
    try:
        result = subprocess.run(
            [path, "-version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def get_resource_path(filename: str) -> str:
    """Return correct path for a resource.
    
    Search order:
    1. Environment variables DR_CDJ_FFMPEG_PATH / DR_CDJ_FFPROBE_PATH
    2. 'bin' directory in PyInstaller bundle
    3. Root directory of PyInstaller bundle
    4. System PATH
    
    Args:
        filename: File name (e.g., "ffmpeg", "ffprobe")
        
    Returns:
        Full path to file or just filename if not found.
    """
    # 1. Environment variables (highest priority)
    env_var = f"DR_CDJ_{filename.upper()}_PATH"
    if env_var in os.environ:
        path = Path(os.environ[env_var])
        if path.exists() and verify_ffmpeg(str(path)):
            return str(path)
    
    # 2. If in PyInstaller bundle, search in bundle directories
    if getattr(sys, 'frozen', False):
        # Determine base directory
        if hasattr(sys, '_MEIPASS'):
            # _MEIPASS is the temp folder where PyInstaller extracts files
            base_path = Path(sys._MEIPASS)
        else:
            # Fallback: executable directory
            base_path = Path(sys.executable).parent
        
        # Possible binary locations (in priority order)
        possible_paths = [
            # Bundle subdirectory 'bin' (new method with download-ffmpeg.py)
            base_path / "bin" / filename,
            # Bundle root
            base_path / filename,
            # macOS .app bundle locations - PyInstaller puts binaries in Frameworks/
            base_path.parent / "Frameworks" / "bin" / filename,
            base_path.parent / "Frameworks" / filename,
            base_path.parent / "Resources" / "bin" / filename,
            base_path.parent / "Resources" / filename,
            base_path.parent / "MacOS" / "bin" / filename,
            base_path.parent / "MacOS" / filename,
            # Windows
            base_path / f"{filename}.exe",
            base_path / "bin" / f"{filename}.exe",
        ]
        
        for path in possible_paths:
        # Check file exists and is executable
            try:
                # For symlinks, resolve() raises error if broken
                if path.is_symlink():
                    resolved = path.resolve(strict=True)
                    if not resolved.exists():
                        continue
                elif not path.exists():
                    continue
                
                # Verify it's executable (unix)
                if os.name != 'nt':
                    import stat
                    try:
                        st = os.stat(path)
                        if not st.st_mode & stat.S_IXUSR:
                            os.chmod(path, st.st_mode | stat.S_IXUSR)
                    except:
                        pass
                
                # Verify binary actually works
                if verify_ffmpeg(str(path)):
                    return str(path)
                    
            except (OSError, RuntimeError):
                continue
    
    # 3. Search in app local directory (~/.dr_cdj/bin)
    local_dir = Path.home() / ".dr_cdj" / "bin" / filename
    if local_dir.exists() and verify_ffmpeg(str(local_dir)):
        return str(local_dir)
    
    # 4. Search in system PATH
    system_path = shutil.which(filename)
    if system_path and verify_ffmpeg(system_path):
        return system_path
    
    # 5. Fallback: return name (allows graceful error)
    return filename


def get_ffmpeg_path() -> str:
    """Return path to ffmpeg.
    
    Returns:
        Full path to ffmpeg binary
    """
    return get_resource_path("ffmpeg")


def get_ffprobe_path() -> str:
    """Return path to ffprobe.
    
    Returns:
        Full path to ffprobe binary
    """
    return get_resource_path("ffprobe")


def get_binary_info() -> dict:
    """Return information about found FFmpeg binaries.
    
    Returns:
        Dict with info about ffmpeg and ffprobe
    """
    ffmpeg_path = get_ffmpeg_path()
    ffprobe_path = get_ffprobe_path()
    
    info = {
        "ffmpeg": {
            "path": ffmpeg_path,
            "bundled": ffmpeg_path != "ffmpeg" and shutil.which("ffmpeg") != ffmpeg_path,
            "working": verify_ffmpeg(ffmpeg_path),
        },
        "ffprobe": {
            "path": ffprobe_path,
            "bundled": ffprobe_path != "ffprobe" and shutil.which("ffprobe") != ffprobe_path,
            "working": verify_ffmpeg(ffprobe_path),
        }
    }
    
    return info
