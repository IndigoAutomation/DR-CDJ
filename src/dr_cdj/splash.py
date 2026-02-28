"""Splash screen for Dr. CDJ - shows loading and errors at startup."""

import sys
import tkinter as tk
from pathlib import Path

try:
    import customtkinter as ctk
except ImportError:
    ctk = None


class SplashScreen:
    """Splash screen showing loading and any errors."""
    
    def __init__(self, title="Dr. CDJ"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f11")
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"400x300+{x}+{y}")
        
        # Icona
        try:
            self.root.iconbitmap(str(Path(__file__).parent / "assets" / "logo_256.ico"))
        except:
            pass
        
        # UI
        self._setup_ui()
        
        # Update
        self.root.update()
    
    def _setup_ui(self):
        """Setup UI splash screen."""
        # Frame principale
        frame = tk.Frame(self.root, bg="#0f0f11")
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Logo (testo)
        logo_label = tk.Label(
            frame,
            text="◉",
            font=("SF Pro Display", 64),
            fg="#6366f1",
            bg="#0f0f11"
        )
        logo_label.pack(pady=(20, 10))
        
        # Titolo
        title_label = tk.Label(
            frame,
            text="Dr. CDJ",
            font=("SF Pro Display", 24, "bold"),
            fg="#fafafa",
            bg="#0f0f11"
        )
        title_label.pack()
        
        # Sottotitolo
        subtitle_label = tk.Label(
            frame,
            text="Audio Compatibility Checker",
            font=("SF Pro Display", 11),
            fg="#a1a1aa",
            bg="#0f0f11"
        )
        subtitle_label.pack(pady=(5, 20))
        
        # Status label
        self.status_label = tk.Label(
            frame,
            text="Starting up...",
            font=("SF Pro Display", 12),
            fg="#22c55e",
            bg="#0f0f11"
        )
        self.status_label.pack(pady=10)
        
        # Progress bar
        self.progress = tk.DoubleVar(value=0)
        self.progress_bar = tk.Canvas(
            frame,
            width=300,
            height=6,
            bg="#262626",
            highlightthickness=0
        )
        self.progress_bar.pack(pady=10)
        
        # Error details (initially hidden)
        self.error_frame = tk.Frame(frame, bg="#0f0f11")
        self.error_text = tk.Text(
            self.error_frame,
            height=6,
            width=40,
            bg="#1a1a1f",
            fg="#f87171",
            font=("SF Mono", 9),
            wrap=tk.WORD,
            relief="flat",
            state="disabled"
        )
        self.error_text.pack(fill="both", expand=True)
    
    def update_status(self, message, progress=None):
        """Update status message."""
        self.status_label.config(text=message)
        if progress is not None:
            self._draw_progress(progress)
        self.root.update()
    
    def _draw_progress(self, value):
        """Draw progress bar."""
        self.progress_bar.delete("all")
        width = int(300 * value / 100)
        self.progress_bar.create_rectangle(
            0, 0, width, 6,
            fill="#6366f1",
            outline=""
        )
    
    def show_error(self, title, message, details=""):
        """Show an error in splash screen."""
        self.status_label.config(text=f"❌ {title}", fg="#ef4444")
        
        # Show error frame
        self.error_frame.pack(pady=10, fill="both", expand=True)
        
        # Insert error text
        self.error_text.config(state="normal")
        self.error_text.delete("1.0", tk.END)
        self.error_text.insert("1.0", f"{message}\n\n{details}")
        self.error_text.config(state="disabled")
        
        # Close button
        close_btn = tk.Button(
            self.root,
            text="Close",
            command=self.root.destroy,
            bg="#6366f1",
            fg="#fafafa",
            font=("SF Pro Display", 12, "bold"),
            relief="flat",
            padx=20,
            pady=8
        )
        close_btn.pack(pady=10)
        
        self.root.update()
    
    def close(self):
        """Close splash screen."""
        self.root.destroy()
    
    def run(self):
        """Start splash screen loop."""
        self.root.mainloop()
