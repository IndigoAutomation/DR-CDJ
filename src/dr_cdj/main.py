"""Entry point per Dr. CDJ con gestione errori robusta."""

import sys
import os
import traceback
import logging
import tempfile
from pathlib import Path

# Setup logging su file per debug - usa directory temporanea per evitare problemi permessi
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


def show_error_native(title, message):
    """Mostra un errore usando osascript (AppleScript) che funziona sempre su macOS."""
    import subprocess
    script = f'display dialog "{message}" with title "{title}" buttons {{"OK"}} default button "OK" with icon stop'
    try:
        subprocess.run(['osascript', '-e', script], capture_output=True, timeout=10)
    except:
        pass
    
    # Anche su stderr
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"ERRORE: {title}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    print(f"\n{message}", file=sys.stderr)
    print(f"\nLog: {log_file}", file=sys.stderr)


def check_ffmpeg():
    """Verifica che FFmpeg sia disponibile."""
    import subprocess
    
    ffmpeg_paths = [
        "ffmpeg",
        "/opt/homebrew/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
        "/usr/bin/ffmpeg",
    ]
    
    # Controlla anche nella directory dell'eseguibile (per bundle PyInstaller)
    if getattr(sys, 'frozen', False):
        bundle_dir = Path(sys.executable).parent
        ffmpeg_paths.insert(0, str(bundle_dir / "ffmpeg"))
        ffmpeg_paths.insert(0, str(bundle_dir / ".." / "MacOS" / "ffmpeg"))
    
    for path in ffmpeg_paths:
        try:
            result = subprocess.run(
                [path, "-version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"FFmpeg trovato: {path}")
                return path
        except:
            continue
    
    return None


def main():
    """Entry point principale con gestione errori."""
    try:
        logger.info("="*50)
        logger.info("Dr. CDJ - Avvio applicazione")
        logger.info(f"Python: {sys.version}")
        logger.info(f"Executable: {sys.executable}")
        logger.info(f"Frozen: {getattr(sys, 'frozen', False)}")
        logger.info(f"Working dir: {os.getcwd()}")
        logger.info(f"Log file: {log_file}")
        logger.info("="*50)
        
        # Verifica FFmpeg
        logger.info("Verifica FFmpeg...")
        ffmpeg_path = check_ffmpeg()
        
        if not ffmpeg_path:
            error_msg = (
                "FFmpeg è richiesto per l'analisi audio.\n\n"
                "Installa FFmpeg:\n"
                "• macOS: brew install ffmpeg\n"
                "• Linux: sudo apt-get install ffmpeg\n"
                "• Windows: ffmpeg.org\n\n"
                f"Log: {log_file}"
            )
            logger.error("FFmpeg non trovato")
            show_error_native("FFmpeg non trovato", error_msg)
            sys.exit(1)
        
        logger.info("Importazione moduli GUI...")
        
        # Importa tkinter
        try:
            import tkinter as tk
            logger.info("tkinter importato")
        except ImportError as e:
            logger.error(f"tkinter non disponibile: {e}")
            show_error_native("Errore GUI", f"tkinter non disponibile. Installa Python con supporto tkinter.\n\n{e}")
            sys.exit(1)
        
        # Importa customtkinter
        try:
            import customtkinter as ctk
            from tkinterdnd2 import TkinterDnD
            logger.info("customtkinter e tkinterdnd2 importati")
        except ImportError as e:
            logger.error(f"Dipendenza mancante: {e}")
            show_error_native("Dipendenza mancante", f"Librerie GUI non trovate.\n\n{e}")
            sys.exit(1)
        
        logger.info("Importazione GUI principale...")
        
        # Importa GUI principale
        try:
            from dr_cdj.gui import CDJCheckApp
        except Exception as e:
            logger.exception("Errore importazione GUI")
            show_error_native("Errore importazione", f"Impossibile caricare l'interfaccia:\n\n{e}")
            sys.exit(1)
        
        logger.info("Avvio GUI principale...")
        
        # Avvia app
        try:
            app = CDJCheckApp()
            app.run()
        except Exception as e:
            logger.exception("Errore durante esecuzione GUI")
            show_error_native("Errore applicazione", f"Errore durante l'esecuzione:\n\n{e}")
            sys.exit(1)
        
    except Exception as e:
        logger.exception("Errore fatale durante l'avvio")
        error_details = traceback.format_exc()
        show_error_native(
            "Errore di avvio",
            f"Si è verificato un errore durante l'avvio.\n\n{str(e)}\n\nLog: {log_file}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
