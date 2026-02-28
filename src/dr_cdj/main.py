"""Entry point per Dr. CDJ con gestione errori robusta e download FFmpeg."""

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


def check_ffmpeg_system():
    """Verifica che FFmpeg sia disponibile nel sistema."""
    import subprocess
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            logger.info("FFmpeg trovato nel sistema")
            return "ffmpeg", "ffprobe"
    except:
        pass
    
    return None, None


def check_ffmpeg_bundled():
    """Verifica che FFmpeg sia nel bundle dell'app."""
    import subprocess
    
    if getattr(sys, 'frozen', False):
        bundle_dir = Path(sys.executable).parent
        ffmpeg_paths = [
            bundle_dir / "ffmpeg",
            bundle_dir / ".." / "MacOS" / "ffmpeg",
            bundle_dir.parent / "ffmpeg",
        ]
        
        for path in ffmpeg_paths:
            try:
                result = subprocess.run(
                    [str(path), "-version"],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    logger.info(f"FFmpeg trovato nel bundle: {path}")
                    ffprobe_path = path.parent / "ffprobe"
                    return str(path), str(ffprobe_path)
            except:
                continue
    
    return None, None


def check_ffmpeg_local():
    """Verifica che FFmpeg sia installato localmente dall'app."""
    from dr_cdj.ffmpeg_downloader import FFmpegDownloader
    
    downloader = FFmpegDownloader()
    if downloader.is_ffmpeg_installed():
        logger.info("FFmpeg trovato in ~/.dr_cdj/bin")
        return str(downloader.ffmpeg_path), str(downloader.ffprobe_path)
    
    return None, None


def show_ffmpeg_dialog():
    """Mostra dialog per scaricare FFmpeg."""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        
        result = messagebox.askyesno(
            "FFmpeg Richiesto",
            "Dr. CDJ richiede FFmpeg per analizzare e convertire file audio.\n\n"
            "FFmpeg non è installato sul tuo sistema.\n\n"
            "Vuoi scaricarlo e installarlo automaticamente?\n\n"
            "(Dimensione: ~20 MB, richiede connessione internet)",
            icon='warning'
        )
        
        root.destroy()
        return result
        
    except Exception as e:
        logger.error(f"Errore nella dialog: {e}")
        # Fallback
        return True


def download_ffmpeg_dialog():
    """Mostra dialog di progresso e scarica FFmpeg."""
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Crea finestra progresso
        progress_window = tk.Tk()
        progress_window.title("Installazione FFmpeg")
        progress_window.geometry("450x180")
        progress_window.resizable(False, False)
        progress_window.configure(bg="#1a1a1f")
        
        # Centra la finestra
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (180 // 2)
        progress_window.geometry(f"450x180+{x}+{y}")
        
        # Titolo
        title = tk.Label(
            progress_window,
            text="📥 Download FFmpeg",
            font=("SF Pro Display", 16, "bold"),
            bg="#1a1a1f",
            fg="#6366f1"
        )
        title.pack(pady=15)
        
        # Status
        status_label = tk.Label(
            progress_window,
            text="Connessione al server...",
            font=("SF Pro Display", 12),
            bg="#1a1a1f",
            fg="#fafafa"
        )
        status_label.pack(pady=5)
        
        # Progress bar
        progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(
            progress_window,
            variable=progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        progress_bar.pack(pady=15, padx=25)
        
        # Info
        info_label = tk.Label(
            progress_window,
            text="Questo processo richiede solo pochi secondi",
            font=("SF Pro Display", 10),
            bg="#1a1a1f",
            fg="#71717a"
        )
        info_label.pack(pady=5)
        
        # Stile
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", thickness=12, background="#6366f1", troughcolor="#262626")
        
        result = [None, None]  # Per memorizzare il risultato
        
        def update_progress(percent, message):
            progress_var.set(percent)
            status_label.config(text=message)
            progress_window.update()
        
        def do_download():
            from dr_cdj.ffmpeg_downloader import FFmpegDownloader
            
            downloader = FFmpegDownloader()
            success = downloader.download_ffmpeg(update_progress)
            
            if success:
                status_label.config(text="✅ Installazione completata!", fg="#22c55e")
                result[0] = str(downloader.ffmpeg_path)
                result[1] = str(downloader.ffprobe_path)
                progress_window.after(1500, progress_window.destroy)
            else:
                status_label.config(text="❌ Errore durante il download", fg="#ef4444")
                info_label.config(text="Verifica la connessione internet e riprova")
                progress_window.after(3000, progress_window.destroy)
        
        # Avvia download in background
        import threading
        thread = threading.Thread(target=do_download)
        thread.daemon = True
        thread.start()
        
        progress_window.mainloop()
        
        return result[0], result[1]
        
    except Exception as e:
        logger.exception("Errore durante il download con dialog")
        # Fallback: download silenzioso
        try:
            from dr_cdj.ffmpeg_downloader import FFmpegDownloader
            downloader = FFmpegDownloader()
            if downloader.download_ffmpeg():
                return str(downloader.ffmpeg_path), str(downloader.ffprobe_path)
        except:
            pass
        return None, None


def setup_ffmpeg_environment(ffmpeg_path, ffprobe_path):
    """Configura le variabili d'ambiente per FFmpeg."""
    if ffmpeg_path and ffprobe_path:
        os.environ["DR_CDJ_FFMPEG_PATH"] = ffmpeg_path
        os.environ["DR_CDJ_FFPROBE_PATH"] = ffprobe_path
        logger.info(f"FFmpeg configurato: {ffmpeg_path}")
        return True
    return False


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
        
        ffmpeg_path = None
        ffprobe_path = None
        
        # 1. Controlla FFmpeg nel sistema
        logger.info("Controllo FFmpeg nel sistema...")
        ffmpeg_path, ffprobe_path = check_ffmpeg_system()
        
        # 2. Controlla FFmpeg nel bundle
        if not ffmpeg_path:
            logger.info("Controllo FFmpeg nel bundle...")
            ffmpeg_path, ffprobe_path = check_ffmpeg_bundled()
        
        # 3. Controlla FFmpeg in ~/.dr_cdj/bin
        if not ffmpeg_path:
            logger.info("Controllo FFmpeg in ~/.dr_cdj/bin...")
            ffmpeg_path, ffprobe_path = check_ffmpeg_local()
        
        # 4. Se non trovato, chiedi all'utente di scaricarlo
        if not ffmpeg_path:
            logger.warning("FFmpeg non trovato, richiesta installazione all'utente")
            
            # Prima mostra una dialog semplice
            if show_ffmpeg_dialog():
                logger.info("Utente ha accettato di scaricare FFmpeg")
                ffmpeg_path, ffprobe_path = download_ffmpeg_dialog()
            else:
                logger.warning("Utente ha rifiutato di scaricare FFmpeg")
                show_error_native(
                    "FFmpeg Richiesto",
                    "Dr. CDJ non può funzionare senza FFmpeg.\n\n"
                    "Puoi installarlo manualmente con:\n"
                    "brew install ffmpeg\n\n"
                    "Oppure riavvia l'app per scaricarlo automaticamente."
                )
                sys.exit(1)
        
        # Configura FFmpeg
        if ffmpeg_path:
            setup_ffmpeg_environment(ffmpeg_path, ffprobe_path)
            logger.info(f"FFmpeg pronto: {ffmpeg_path}")
        else:
            logger.error("FFmpeg non disponibile dopo tutti i tentativi")
            show_error_native(
                "Errore FFmpeg",
                "Impossibile scaricare FFmpeg.\n\n"
                "Verifica la connessione internet e riprova.\n\n"
                "Log: {log_file}"
            )
            sys.exit(1)
        
        # Importa e avvia la GUI principale
        logger.info("Importazione moduli GUI...")
        
        try:
            import customtkinter as ctk
            from tkinterdnd2 import TkinterDnD
            logger.info("customtkinter e tkinterdnd2 importati")
        except ImportError as e:
            logger.error(f"Dipendenza mancante: {e}")
            show_error_native(
                "Dipendenza mancante",
                "Librerie GUI non trovate.\n\n"
                f"Errore: {e}\n\n"
                "Installa le dipendenze:\n"
                "pip install customtkinter tkinterdnd2"
            )
            sys.exit(1)
        
        logger.info("Importazione GUI principale...")
        
        try:
            from dr_cdj.gui import CDJCheckApp
        except Exception as e:
            logger.exception("Errore importazione GUI")
            show_error_native(
                "Errore importazione",
                f"Impossibile caricare l'interfaccia:\n\n{e}"
            )
            sys.exit(1)
        
        logger.info("Avvio GUI principale...")
        
        # Avvia app
        try:
            app = CDJCheckApp()
            app.run()
        except Exception as e:
            logger.exception("Errore durante esecuzione GUI")
            show_error_native(
                "Errore applicazione",
                f"Errore durante l'esecuzione:\n\n{e}"
            )
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
