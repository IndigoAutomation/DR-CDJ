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
# FFmpeg Setup
# =============================================================================
def setup_ffmpeg() -> bool:
    """
    Setup FFmpeg for the application.
    
    Priority:
    1. Bundled FFmpeg (included in app bundle)
    2. System FFmpeg (from PATH)
    3. Download FFmpeg if neither available
    
    Returns:
        True if FFmpeg is ready to use
    """
    from dr_cdj.utils import get_ffmpeg_path, get_ffprobe_path, verify_ffmpeg
    
    ffmpeg_path = get_ffmpeg_path()
    ffprobe_path = get_ffprobe_path()
    
    logger.info(f"FFmpeg path: {ffmpeg_path}")
    logger.info(f"FFprobe path: {ffprobe_path}")
    
    # Verify FFmpeg works
    if verify_ffmpeg(ffmpeg_path) and verify_ffmpeg(ffprobe_path):
        # Set environment variables for subprocess calls
        os.environ["DR_CDJ_FFMPEG_PATH"] = ffmpeg_path
        os.environ["DR_CDJ_FFPROBE_PATH"] = ffprobe_path
        logger.info("✅ FFmpeg verified and configured")
        return True
    
    logger.warning("Bundled/system FFmpeg not working, attempting download...")
    
    # Fallback: download FFmpeg
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
        
        # Setup FFmpeg (bundled, system, or download)
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
            from dr_cdj.gui import CDJCheckApp
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
            app = CDJCheckApp()
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
