"""Downloader automatico per FFmpeg su macOS."""

import os
import sys
import stat
import urllib.request
import urllib.error
import zipfile
import tarfile
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class FFmpegDownloader:
    """Gestisce il download e l'installazione automatica di FFmpeg."""
    
    # URL per download FFmpeg statico per macOS (evermeet.cx)
    # FFmpeg and ffprobe are separate downloads
    FFMPEG_URLS = {
        "arm64": {
            "ffmpeg": "https://evermeet.cx/ffmpeg/ffmpeg-6.1.1.zip",
            "ffprobe": "https://evermeet.cx/ffmpeg/ffprobe-6.1.1.zip",
        },
        "x86_64": {
            "ffmpeg": "https://evermeet.cx/ffmpeg/ffmpeg-6.1.1.zip",
            "ffprobe": "https://evermeet.cx/ffmpeg/ffprobe-6.1.1.zip",
        },
    }
    
    def __init__(self, install_dir: Optional[Path] = None):
        """Inizializza il downloader.
        
        Args:
            install_dir: Directory dove installare FFmpeg. 
                        Default: ~/.dr_cdj/bin
        """
        if install_dir is None:
            self.install_dir = Path.home() / ".dr_cdj" / "bin"
        else:
            self.install_dir = Path(install_dir)
        
        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.ffmpeg_path = self.install_dir / "ffmpeg"
        self.ffprobe_path = self.install_dir / "ffprobe"
    
    def is_ffmpeg_installed(self) -> bool:
        """Verifica se FFmpeg è già installato nella directory dell'app."""
        return self.ffmpeg_path.exists() and self.ffprobe_path.exists()
    
    def get_system_arch(self) -> str:
        """Rileva l'architettura del sistema."""
        import platform
        machine = platform.machine()
        if machine == "arm64":
            return "arm64"
        return "x86_64"
    
    def download_ffmpeg(self, progress_callback=None) -> bool:
        """Scarica e installa FFmpeg e FFprobe.
        
        Args:
            progress_callback: Funzione callback(progress_percent, status_message)
        
        Returns:
            True se l'installazione è riuscita, False altrimenti
        """
        try:
            arch = self.get_system_arch()
            urls = self.FFMPEG_URLS.get(arch, self.FFMPEG_URLS["x86_64"])
            
            logger.info(f"Downloading FFmpeg for {arch}")
            
            # Download both ffmpeg and ffprobe
            for i, (binary_name, url) in enumerate(urls.items()):
                if progress_callback:
                    base_percent = i * 50
                    progress_callback(base_percent, f"Download {binary_name}...")
                
                logger.info(f"Downloading {binary_name} from {url}")
                
                temp_zip = self.install_dir / f"{binary_name}_download.zip"
                
                def make_progress_handler(base):
                    def handler(block_num, block_size, total_size):
                        if total_size > 0 and progress_callback:
                            percent = min(int((block_num * block_size / total_size) * 45), 45)
                            progress_callback(base + percent, f"Download {binary_name}... {percent}%")
                    return handler
                
                # Download
                urllib.request.urlretrieve(url, temp_zip, reporthook=make_progress_handler(i * 50))
                
                if progress_callback:
                    progress_callback(i * 50 + 45, f"Estrazione {binary_name}...")
                
                # Extract
                if temp_zip.exists():
                    with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                        zip_ref.extractall(self.install_dir)
                    temp_zip.unlink()
                
                if progress_callback:
                    progress_callback(i * 50 + 50, f"{binary_name} pronto")
            
            # Find and rename extracted files
            for file in self.install_dir.glob("*"):
                if file.is_file() and not file.name.endswith('.zip'):
                    if 'ffmpeg' in file.name.lower() and 'ffprobe' not in file.name.lower():
                        file.rename(self.ffmpeg_path)
                        self.ffmpeg_path.chmod(self.ffmpeg_path.stat().st_mode | stat.S_IEXEC)
                    elif 'ffprobe' in file.name.lower():
                        file.rename(self.ffprobe_path)
                        self.ffprobe_path.chmod(self.ffprobe_path.stat().st_mode | stat.S_IEXEC)
            
            if progress_callback:
                progress_callback(100, "FFmpeg installato!")
            
            success = self.is_ffmpeg_installed()
            if success:
                logger.info(f"FFmpeg installato in {self.install_dir}")
            else:
                logger.error(f"FFmpeg non trovato dopo il download. Files: {list(self.install_dir.glob('*'))}")
            
            return success
            
        except Exception as e:
            logger.exception("Errore durante il download di FFmpeg")
            if progress_callback:
                progress_callback(0, f"Errore: {str(e)}")
            return False
    
    def get_ffmpeg_path(self) -> Optional[Path]:
        """Restituisce il path a FFmpeg se installato."""
        if self.is_ffmpeg_installed():
            return self.ffmpeg_path
        return None


def check_and_install_ffmpeg(parent_window=None):
    """Controlla FFmpeg e offre di installarlo se mancante.
    
    Args:
        parent_window: Finestra parent per le dialog (opzionale)
    
    Returns:
        Tuple (ffmpeg_path, ffprobe_path) o (None, None) se non disponibile
    """
    import subprocess
    
    # Prima controlla se FFmpeg è nel PATH di sistema
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
        if result.returncode == 0:
            logger.info("FFmpeg trovato nel sistema")
            return "ffmpeg", "ffprobe"
    except:
        pass
    
    # Controlla nella directory dell'app
    downloader = FFmpegDownloader()
    
    if downloader.is_ffmpeg_installed():
        logger.info("FFmpeg trovato in ~/.dr_cdj/bin")
        return str(downloader.ffmpeg_path), str(downloader.ffprobe_path)
    
    # FFmpeg non trovato, chiedi all'utente
    return None, None


def show_ffmpeg_install_dialog(parent=None):
    """Mostra una dialog per installare FFmpeg.
    
    Returns:
        True se l'utente vuole installare, False altrimenti
    """
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        if parent is None:
            root = tk.Tk()
            root.withdraw()
        
        result = messagebox.askyesno(
            "FFmpeg Richiesto",
            "Dr. CDJ richiede FFmpeg per analizzare e convertire file audio.\n\n"
            "FFmpeg non è installato sul tuo sistema.\n\n"
            "Vuoi scaricarlo e installarlo automaticamente?\n\n"
            "(Dimensione: ~30 MB)",
            icon='warning'
        )
        
        if parent is None:
            root.destroy()
        
        return result
        
    except Exception as e:
        logger.error(f"Errore nella dialog: {e}")
        # Fallback: assumiamo che l'utente voglia installare
        return True


def install_ffmpeg_with_progress(parent=None):
    """Installa FFmpeg mostrando una progress bar.
    
    Returns:
        Tuple (ffmpeg_path, ffprobe_path) o (None, None)
    """
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Crea finestra progresso
        progress_window = tk.Toplevel(parent) if parent else tk.Tk()
        progress_window.title("Installazione FFmpeg")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        progress_window.configure(bg="#1a1a1f")
        
        # Centra la finestra
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (150 // 2)
        progress_window.geometry(f"400x150+{x}+{y}")
        
        # Label
        label = tk.Label(
            progress_window,
            text="Download FFmpeg in corso...",
            font=("SF Pro Display", 14, "bold"),
            bg="#1a1a1f",
            fg="#fafafa"
        )
        label.pack(pady=20)
        
        # Status
        status_label = tk.Label(
            progress_window,
            text="Connessione...",
            font=("SF Pro Display", 11),
            bg="#1a1a1f",
            fg="#a1a1aa"
        )
        status_label.pack(pady=5)
        
        # Progress bar
        progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(
            progress_window,
            variable=progress_var,
            maximum=100,
            length=350,
            mode='determinate'
        )
        progress_bar.pack(pady=10)
        
        # Stile progress bar
        style = ttk.Style()
        style.configure("TProgressbar", thickness=20, background="#6366f1")
        
        def update_progress(percent, message):
            progress_var.set(percent)
            status_label.config(text=message)
            progress_window.update()
        
        def do_install():
            downloader = FFmpegDownloader()
            success = downloader.download_ffmpeg(update_progress)
            
            if success:
                status_label.config(text="✅ FFmpeg installato con successo!", fg="#22c55e")
                progress_window.after(1500, progress_window.destroy)
            else:
                status_label.config(text="❌ Errore durante l'installazione", fg="#ef4444")
                progress_window.after(2000, progress_window.destroy)
        
        # Avvia installazione in background
        import threading
        thread = threading.Thread(target=do_install)
        thread.daemon = True
        thread.start()
        
        if not parent:
            progress_window.mainloop()
        
        # Verifica risultato
        downloader = FFmpegDownloader()
        if downloader.is_ffmpeg_installed():
            return str(downloader.ffmpeg_path), str(downloader.ffprobe_path)
        
        return None, None
        
    except Exception as e:
        logger.exception("Errore durante l'installazione con progresso")
        # Fallback: installazione silenziosa
        downloader = FFmpegDownloader()
        if downloader.download_ffmpeg():
            return str(downloader.ffmpeg_path), str(downloader.ffprobe_path)
        return None, None


if __name__ == "__main__":
    # Test
    print("Testing FFmpeg downloader...")
    downloader = FFmpegDownloader()
    print(f"FFmpeg installed: {downloader.is_ffmpeg_installed()}")
    print(f"Install dir: {downloader.install_dir}")
    print(f"FFmpeg path: {downloader.get_ffmpeg_path()}")
