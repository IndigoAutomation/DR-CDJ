#!/usr/bin/env python3
"""
Entry point per Dr. CDJ - Audio Compatibility Checker for Pioneer CDJ.

This app includes bundled FFmpeg binaries for completely standalone operation.
"""

import sys
import os
import subprocess
import traceback
import logging
import tempfile
from pathlib import Path

# =============================================================================
# Setup Logging
# =============================================================================
log_dir = Path(tempfile.gettempdir()) / "Dr-CDJ-Logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "app.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# Error Handling
# =============================================================================
def show_error_dialog(title: str, message: str):
    """Show error dialog using native macOS osascript."""
    try:
        script = f'display dialog "{message}" with title "{title}" buttons {{"OK"}} default button "OK" with icon stop'
        subprocess.run(['osascript', '-e', script], capture_output=True, timeout=10)
    except:
        pass
    
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"ERRORE: {title}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    print(f"\n{message}", file=sys.stderr)
    print(f"\nLog: {log_file}", file=sys.stderr)


# =============================================================================
# macOS Gatekeeper Fix
# =============================================================================
def remove_extended_attributes():
    """Remove macOS extended attributes from bundled binaries (Gatekeeper fix)."""
    if sys.platform != 'darwin':
        return
    
    if not getattr(sys, 'frozen', False):
        return
    
    try:
        # Find bundled binaries
        bundle_dir = Path(sys.executable).parent
        binary_paths = [
            bundle_dir.parent / "Frameworks" / "bin" / "ffmpeg",
            bundle_dir.parent / "Frameworks" / "bin" / "ffprobe",
            bundle_dir.parent / "Resources" / "bin" / "ffmpeg",
            bundle_dir.parent / "Resources" / "bin" / "ffprobe",
        ]
        
        for path in binary_paths:
            if path.exists():
                try:
                    # Remove com.apple.quarantine and com.apple.provenance
                    subprocess.run(
                        ['xattr', '-d', 'com.apple.quarantine', str(path)],
                        capture_output=True,
                        timeout=5
                    )
                    subprocess.run(
                        ['xattr', '-d', 'com.apple.provenance', str(path)],
                        capture_output=True,
                        timeout=5
                    )
                    logger.debug(f"Removed extended attributes from {path}")
                except:
                    pass
    except Exception as e:
        logger.warning(f"Could not remove extended attributes: {e}")


# =============================================================================
# FFmpeg Setup
# =============================================================================
def get_bundled_binaries():
    """Get paths to bundled FFmpeg binaries."""
    if not getattr(sys, 'frozen', False):
        return None, None
    
    bundle_dir = Path(sys.executable).parent
    
    # Search in possible locations
    possible_paths = [
        (bundle_dir.parent / "Frameworks" / "bin" / "ffmpeg", bundle_dir.parent / "Resources" / "bin" / "ffprobe"),
        (bundle_dir.parent / "Resources" / "bin" / "ffmpeg", bundle_dir.parent / "Frameworks" / "bin" / "ffprobe"),
        (bundle_dir / "bin" / "ffmpeg", bundle_dir / "bin" / "ffprobe"),
    ]
    
    for ffmpeg_path, ffprobe_path in possible_paths:
        ffmpeg_exists = ffmpeg_path.exists() or (ffmpeg_path.is_symlink() and ffmpeg_path.resolve().exists())
        ffprobe_exists = ffprobe_path.exists() or (ffprobe_path.is_symlink() and ffprobe_path.resolve().exists())
        
        if ffmpeg_exists and ffprobe_exists:
            return str(ffmpeg_path), str(ffprobe_path)
    
    return None, None


def copy_bundled_to_local():
    """Copy bundled FFmpeg binaries to local dir (bypasses Gatekeeper)."""
    import shutil
    
    local_dir = Path.home() / ".dr_cdj" / "bin"
    local_dir.mkdir(parents=True, exist_ok=True)
    
    ffmpeg_bundled, ffprobe_bundled = get_bundled_binaries()
    
    if not ffmpeg_bundled or not ffprobe_bundled:
        return None, None
    
    ffmpeg_local = local_dir / "ffmpeg"
    ffprobe_local = local_dir / "ffprobe"
    
    try:
        # Copy files
        shutil.copy2(ffmpeg_bundled, ffmpeg_local)
        shutil.copy2(ffprobe_bundled, ffprobe_local)
        
        # Remove extended attributes (Gatekeeper)
        if sys.platform == 'darwin':
            subprocess.run(['xattr', '-d', 'com.apple.provenance', str(ffmpeg_local)], capture_output=True)
            subprocess.run(['xattr', '-d', 'com.apple.provenance', str(ffprobe_local)], capture_output=True)
            subprocess.run(['xattr', '-d', 'com.apple.quarantine', str(ffmpeg_local)], capture_output=True)
            subprocess.run(['xattr', '-d', 'com.apple.quarantine', str(ffprobe_local)], capture_output=True)
        
        # Make executable
        ffmpeg_local.chmod(0o755)
        ffprobe_local.chmod(0o755)
        
        logger.info(f"Copied bundled FFmpeg to {local_dir}")
        return str(ffmpeg_local), str(ffprobe_local)
    except Exception as e:
        logger.warning(f"Could not copy bundled FFmpeg: {e}")
        return None, None


def setup_ffmpeg() -> bool:
    """
    Setup FFmpeg for the application.

    Priority:
    1. Bundled FFmpeg (copied to ~/.dr_cdj/bin/ on first launch) - standalone, no internet
    2. Previously cached FFmpeg (~/.dr_cdj/bin/) - fast path on subsequent launches
    3. System FFmpeg (from PATH)
    4. Download FFmpeg (last resort, requires internet)

    Returns:
        True if FFmpeg is ready to use
    """
    from dr_cdj.utils import verify_ffmpeg
    import shutil

    local_dir = Path.home() / ".dr_cdj" / "bin"
    local_ffmpeg = local_dir / "ffmpeg"
    local_ffprobe = local_dir / "ffprobe"

    # 0. If not cached locally yet, try to extract from the app bundle first
    if not (local_ffmpeg.exists() and local_ffprobe.exists()):
        logger.info("No local FFmpeg cache — checking app bundle...")
        ff, fp = copy_bundled_to_local()
        if ff and fp:
            logger.info(f"✅ Bundled FFmpeg extracted to ~/.dr_cdj/bin/")

    # 1. Use local cache (~/.dr_cdj/bin/) — covers both bundled-copy and previous download.
    #    Use os.access(X_OK) rather than verify_ffmpeg() here: launching an x86_64 binary
    #    via Rosetta 2 on first run can take >5 s (JIT compile), which exceeds the
    #    verify_ffmpeg timeout and causes an unnecessary fallback to system FFmpeg.
    #    The files are trusted (extracted from our own bundle or previously verified).
    if local_ffmpeg.exists() and local_ffprobe.exists():
        if os.access(str(local_ffmpeg), os.X_OK) and os.access(str(local_ffprobe), os.X_OK):
            os.environ["DR_CDJ_FFMPEG_PATH"] = str(local_ffmpeg)
            os.environ["DR_CDJ_FFPROBE_PATH"] = str(local_ffprobe)
            logger.info("✅ Using FFmpeg from ~/.dr_cdj/bin/")
            return True

    # 2. Try system FFmpeg
    system_ffmpeg = shutil.which("ffmpeg")
    system_ffprobe = shutil.which("ffprobe")

    if system_ffmpeg and system_ffprobe:
        if verify_ffmpeg(system_ffmpeg) and verify_ffmpeg(system_ffprobe):
            os.environ["DR_CDJ_FFMPEG_PATH"] = system_ffmpeg
            os.environ["DR_CDJ_FFPROBE_PATH"] = system_ffprobe
            logger.info("✅ Using system FFmpeg")
            return True

    # 3. Download FFmpeg (last resort)
    logger.info("No FFmpeg found locally or in bundle — downloading...")
    return download_ffmpeg_fallback()


def download_ffmpeg_fallback() -> bool:
    """Download FFmpeg as fallback when bundled version unavailable."""
    try:
        from dr_cdj.ffmpeg_downloader import FFmpegDownloader
        
        logger.info("Starting FFmpeg download...")
        downloader = FFmpegDownloader()
        
        if downloader.download_ffmpeg():
            # Update environment with downloaded paths
            os.environ["DR_CDJ_FFMPEG_PATH"] = str(downloader.ffmpeg_path)
            os.environ["DR_CDJ_FFPROBE_PATH"] = str(downloader.ffprobe_path)
            logger.info("✅ FFmpeg downloaded and configured")
            return True
        else:
            logger.error("FFmpeg download failed")
            return False
            
    except Exception as e:
        logger.exception("Error during FFmpeg download")
        return False


def show_ffmpeg_error():
    """Show error dialog for missing FFmpeg."""
    show_error_dialog(
        "FFmpeg Required",
        "Dr. CDJ requires FFmpeg to analyze audio files.\n\n"
        "Automatic download failed. Please:\n"
        "1. Check your internet connection\n"
        "2. Or install FFmpeg manually:\n"
        "   brew install ffmpeg\n\n"
        f"Log: {log_file}"
    )


# =============================================================================
# Main Entry Point
# =============================================================================
def main():
    """Main entry point with comprehensive error handling."""
    try:
        # Log startup info
        logger.info("="*50)
        logger.info("Dr. CDJ - Starting application")
        logger.info(f"Python: {sys.version}")
        logger.info(f"Executable: {sys.executable}")
        logger.info(f"Frozen: {getattr(sys, 'frozen', False)}")
        logger.info(f"Working dir: {os.getcwd()}")
        logger.info(f"Log file: {log_file}")
        logger.info("="*50)
        
        # Setup FFmpeg (bundled → local, system, or download)
        logger.info("Setting up FFmpeg...")
        if not setup_ffmpeg():
            show_ffmpeg_error()
            sys.exit(1)
        
        # Import GUI dependencies
        logger.info("Loading GUI...")
        try:
            import customtkinter as ctk
            from tkinterdnd2 import TkinterDnD
        except ImportError as e:
            logger.error(f"Missing GUI dependency: {e}")
            show_error_dialog(
                "Missing Dependencies",
                f"Required library not found: {e}\n\n"
                "Install with:\n"
                "pip install customtkinter tkinterdnd2"
            )
            sys.exit(1)
        
        # Import and start main application
        try:
            from dr_cdj.gui import DrCDJApp
        except Exception as e:
            logger.exception("Error importing main GUI")
            show_error_dialog(
                "Import Error",
                f"Failed to load application interface:\n\n{e}"
            )
            sys.exit(1)
        
        # Run the application
        logger.info("Starting main application...")
        try:
            app = DrCDJApp()
            app.run()
        except Exception as e:
            logger.exception("Runtime error")
            show_error_dialog(
                "Runtime Error",
                f"An error occurred during execution:\n\n{e}"
            )
            sys.exit(1)
            
    except Exception as e:
        logger.exception("Fatal startup error")
        error_details = traceback.format_exc()
        show_error_dialog(
            "Fatal Error",
            f"Could not start application:\n\n{str(e)}\n\nLog: {log_file}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
