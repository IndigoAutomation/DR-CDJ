"""GUI moderna per CDJ-Check con info specifiche CDJ e massima qualità."""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional
from dataclasses import dataclass

try:
    import customtkinter as ctk
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    print("Errore: customtkinter e tkinterdnd2 sono richiesti.")
    print("Installa con: pip install customtkinter tkinterdnd2")
    sys.exit(1)

from cdj_check.analyzer import AudioAnalyzer, AudioMetadata
from cdj_check.compatibility import CompatibilityEngine, CompatibilityResult, CompatibilityStatus, ConversionPlan
from cdj_check.config import COLORS, CDJ_PROFILES, get_profile_color
from cdj_check.converter import AudioConverter, ConversionResult


@dataclass
class ConversionSettings:
    """Impostazioni personalizzate per la conversione."""
    output_format: str = "WAV"  # WAV, AIFF
    sample_rate: int = 48000    # 44100, 48000, 88200, 96000
    bit_depth: int = 24         # 16, 24
    output_dir: Optional[Path] = None


class ModernTooltip:
    """Tooltip moderno che appare al hover."""
    
    def __init__(self, widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window: Optional[ctk.CTkToplevel] = None
        self.after_id: Optional[str] = None
        
        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event=None):
        self.after_id = self.widget.after(self.delay, self._show)
    
    def _on_leave(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self._hide()
    
    def _show(self):
        if self.tooltip_window:
            return
        
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        self.tooltip_window.configure(fg_color=COLORS["surface_light"])
        
        label = ctk.CTkLabel(
            self.tooltip_window,
            text=self.text,
            font=("SF Pro Display", 11),
            text_color=COLORS["text_secondary"],
            fg_color=COLORS["surface_light"],
            corner_radius=6,
            padx=12,
            pady=6,
        )
        label.pack()
    
    def _hide(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class FileCard(ctk.CTkFrame):
    """Card moderna per visualizzare un file audio."""

    def __init__(
        self,
        master,
        result: CompatibilityResult,
        on_remove: Optional[callable] = None,
        on_convert_single: Optional[callable] = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        
        self.result = result
        self.on_remove = on_remove
        self.on_convert_single = on_convert_single
        
        # Stile in base allo stato
        self._setup_appearance()
        
        # Layout principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        # Content container
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=0, sticky="ew", padx=16, pady=12)
        self.content.grid_columnconfigure(1, weight=1)
        
        # Icona stato con cerchio colorato
        self._setup_status_icon()
        
        # Info file
        self._setup_file_info()
        
        # Dettagli tecnici
        self._setup_tech_specs()
        
        # Azioni (convert singolo)
        self._setup_actions()
    
    def _setup_appearance(self):
        """Configura l'aspetto in base allo stato."""
        border_color = self.result.status_color
        bg_color = self.result.status_bg_color
        
        self.configure(
            border_width=1,
            border_color=border_color,
            fg_color=bg_color,
            corner_radius=12,
        )
    
    def _setup_status_icon(self):
        """Crea l'icona di stato."""
        status_colors = {
            CompatibilityStatus.COMPATIBLE: (COLORS["compatible"], "✓"),
            CompatibilityStatus.CONVERTIBLE_LOSSLESS: (COLORS["convertible_lossless"], "⇄"),
            CompatibilityStatus.CONVERTIBLE_LOSSY: (COLORS["convertible_lossy"], "⚠"),
            CompatibilityStatus.INCOMPATIBLE: (COLORS["incompatible"], "✕"),
            CompatibilityStatus.ERROR: (COLORS["error"], "!"),
        }
        
        color, icon = status_colors.get(self.result.status, (COLORS["text_secondary"], "?"))
        
        # Cerchio con icona
        self.icon_frame = ctk.CTkFrame(
            self.content,
            width=36,
            height=36,
            fg_color=color,
            corner_radius=18,
        )
        self.icon_frame.grid(row=0, column=0, rowspan=2, padx=(0, 12))
        self.icon_frame.grid_propagate(False)
        
        self.icon_label = ctk.CTkLabel(
            self.icon_frame,
            text=icon,
            font=("SF Pro Display", 16, "bold"),
            text_color=COLORS["background"],
            width=36,
            height=36,
        )
        self.icon_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def _setup_file_info(self):
        """Configura le informazioni del file."""
        # Nome file
        filename = self.result.metadata.filename if self.result.metadata else self.result.filepath.name
        display_name = filename[:45] + "..." if len(filename) > 45 else filename
        
        self.name_label = ctk.CTkLabel(
            self.content,
            text=display_name,
            font=("SF Pro Display", 14, "bold"),
            text_color=COLORS["text"],
            anchor="w",
        )
        self.name_label.grid(row=0, column=1, sticky="w")
        
        # Messaggio stato
        status_text = self.result.message
        if len(status_text) > 60:
            status_text = status_text[:57] + "..."
        
        self.status_label = ctk.CTkLabel(
            self.content,
            text=status_text,
            font=("SF Pro Display", 12),
            text_color=self.result.status_color,
            anchor="w",
        )
        self.status_label.grid(row=1, column=1, sticky="w", pady=(2, 0))
    
    def _setup_tech_specs(self):
        """Configura le specifiche tecniche."""
        specs_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        specs_frame.grid(row=0, column=2, rowspan=2, padx=(20, 0), sticky="e")
        
        # Formato
        if self.result.metadata:
            codec = self.result.metadata.codec_formatted
            sr = self.result.metadata.sample_rate_formatted
            bd = self.result.metadata.bit_depth_formatted
            
            specs_text = f"{codec}  •  {sr}  •  {bd}"
        else:
            specs_text = "N/A"
        
        self.specs_label = ctk.CTkLabel(
            specs_frame,
            text=specs_text,
            font=("SF Pro Mono", 11),
            text_color=COLORS["text_muted"],
        )
        self.specs_label.pack()
        
        # Profilo
        profile_text = f"per {self.result.profile_name}"
        self.profile_label = ctk.CTkLabel(
            specs_frame,
            text=profile_text,
            font=("SF Pro Display", 10),
            text_color=COLORS["text_muted"],
        )
        self.profile_label.pack()
    
    def _setup_actions(self):
        """Configura le azioni disponibili."""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=0, column=1, padx=(0, 12), pady=12, sticky="ne")
        
        # Pulsante converti singolo (solo per file convertibili)
        if self.result.needs_conversion:
            self.convert_btn = ctk.CTkButton(
                actions_frame,
                text="⇄",
                font=("SF Pro Display", 14, "bold"),
                width=32,
                height=32,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_dark"],
                text_color=COLORS["text"],
                corner_radius=8,
                command=self._on_convert_click,
            )
            self.convert_btn.pack(pady=(0, 4))
            ModernTooltip(self.convert_btn, "Converti questo file")
        
        # Pulsante rimuovi
        self.remove_btn = ctk.CTkButton(
            actions_frame,
            text="✕",
            font=("SF Pro Display", 12, "bold"),
            width=32,
            height=32,
            fg_color="transparent",
            hover_color=COLORS["incompatible"],
            text_color=COLORS["text_muted"],
            corner_radius=8,
            command=self._on_remove_click,
        )
        self.remove_btn.pack()
        ModernTooltip(self.remove_btn, "Rimuovi dalla lista")
    
    def _on_convert_click(self):
        """Callback per conversione singolo file."""
        if self.on_convert_single:
            self.on_convert_single(self.result)
    
    def _on_remove_click(self):
        """Callback per rimozione file."""
        if self.on_remove:
            self.on_remove(self.result)


class ProfileInfoPanel(ctk.CTkFrame):
    """Pannello informazioni profilo CDJ."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(fg_color=COLORS["surface"], corner_radius=12)
        
        # Titolo
        self.title = ctk.CTkLabel(
            self,
            text="📋 Specifiche Player",
            font=("SF Pro Display", 14, "bold"),
            text_color=COLORS["text"],
        )
        self.title.pack(anchor="w", padx=16, pady=(12, 8))
        
        # Container info
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(fill="x", padx=16, pady=(0, 12))
        
        # Label per le info
        self.name_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("SF Pro Display", 13, "bold"),
            text_color=COLORS["primary_light"],
        )
        self.name_label.pack(anchor="w")
        
        self.desc_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("SF Pro Display", 11),
            text_color=COLORS["text_secondary"],
        )
        self.desc_label.pack(anchor="w", pady=(2, 0))
        
        self.max_quality_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("SF Pro Display", 12),
            text_color=COLORS["compatible"],
        )
        self.max_quality_label.pack(anchor="w", pady=(8, 0))
        
        self.formats_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("SF Pro Display", 11),
            text_color=COLORS["text_muted"],
        )
        self.formats_label.pack(anchor="w", pady=(4, 0))
    
    def update_info(self, profile_id: str):
        """Aggiorna le informazioni del profilo."""
        profile = CDJ_PROFILES.get(profile_id)
        if not profile:
            return
        
        self.name_label.configure(text=f"{profile.name} ({profile.year})")
        self.desc_label.configure(text=profile.description)
        
        max_sr = profile.max_sample_rate / 1000
        max_bd = profile.max_bit_depth
        self.max_quality_label.configure(
            text=f"🎯 Massima Qualità Supportata: {max_bd}-bit / {max_sr:.1f} kHz"
        )
        
        formats_text = "Formati nativi: " + ", ".join(profile.formats.keys())
        self.formats_label.configure(text=formats_text)


class ConversionSettingsPanel(ctk.CTkFrame):
    """Pannello impostazioni conversione."""

    def __init__(self, master, settings: ConversionSettings, on_change: callable, **kwargs):
        super().__init__(master, **kwargs)
        
        self.settings = settings
        self.on_change = on_change
        
        self.configure(fg_color=COLORS["surface"], corner_radius=12)
        
        # Titolo
        self.title = ctk.CTkLabel(
            self,
            text="⚙️ Impostazioni Conversione",
            font=("SF Pro Display", 14, "bold"),
            text_color=COLORS["text"],
        )
        self.title.pack(anchor="w", padx=16, pady=(12, 8))
        
        # Container per i controlli
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(fill="x", padx=16, pady=(0, 12))
        
        # Formato output
        self._setup_format_selector()
        
        # Sample rate
        self._setup_sample_rate_selector()
        
        # Bit depth
        self._setup_bit_depth_selector()
        
        # Cartella output
        self._setup_output_dir_selector()
        
        # Info massima qualità
        self._setup_quality_info()
    
    def _setup_format_selector(self):
        """Selettore formato output."""
        frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        frame.pack(fill="x", pady=4)
        
        label = ctk.CTkLabel(
            frame,
            text="Formato:",
            font=("SF Pro Display", 12),
            text_color=COLORS["text_secondary"],
            width=80,
        )
        label.pack(side="left")
        
        self.format_var = ctk.StringVar(value=self.settings.output_format)
        
        formats = ["WAV", "AIFF"]
        for fmt in formats:
            rb = ctk.CTkRadioButton(
                frame,
                text=fmt,
                variable=self.format_var,
                value=fmt,
                font=("SF Pro Display", 12),
                text_color=COLORS["text"],
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_light"],
                command=self._on_format_change,
            )
            rb.pack(side="left", padx=(8, 0))
    
    def _setup_sample_rate_selector(self):
        """Selettore sample rate."""
        frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        frame.pack(fill="x", pady=4)
        
        label = ctk.CTkLabel(
            frame,
            text="Sample Rate:",
            font=("SF Pro Display", 12),
            text_color=COLORS["text_secondary"],
            width=80,
        )
        label.pack(side="left")
        
        self.sr_var = ctk.StringVar(value=str(self.settings.sample_rate))
        
        sr_values = [("44.1 kHz", "44100"), ("48 kHz", "48000"), ("88.2 kHz", "88200"), ("96 kHz", "96000")]
        for text, value in sr_values:
            rb = ctk.CTkRadioButton(
                frame,
                text=text,
                variable=self.sr_var,
                value=value,
                font=("SF Pro Display", 11),
                text_color=COLORS["text"],
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_light"],
                command=self._on_sr_change,
            )
            rb.pack(side="left", padx=(4, 0))
    
    def _setup_bit_depth_selector(self):
        """Selettore bit depth."""
        frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        frame.pack(fill="x", pady=4)
        
        label = ctk.CTkLabel(
            frame,
            text="Bit Depth:",
            font=("SF Pro Display", 12),
            text_color=COLORS["text_secondary"],
            width=80,
        )
        label.pack(side="left")
        
        self.bd_var = ctk.StringVar(value=str(self.settings.bit_depth))
        
        bd_values = [("16-bit", "16"), ("24-bit", "24")]
        for text, value in bd_values:
            rb = ctk.CTkRadioButton(
                frame,
                text=text,
                variable=self.bd_var,
                value=value,
                font=("SF Pro Display", 12),
                text_color=COLORS["text"],
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_light"],
                command=self._on_bd_change,
            )
            rb.pack(side="left", padx=(8, 0))
    
    def _setup_output_dir_selector(self):
        """Selettore cartella output."""
        frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        frame.pack(fill="x", pady=4)
        
        label = ctk.CTkLabel(
            frame,
            text="Destinazione:",
            font=("SF Pro Display", 12),
            text_color=COLORS["text_secondary"],
            width=80,
        )
        label.pack(side="left")
        
        self.dir_label = ctk.CTkLabel(
            frame,
            text="CDJ_Ready (default)",
            font=("SF Pro Display", 11),
            text_color=COLORS["text_muted"],
        )
        self.dir_label.pack(side="left", padx=(8, 0))
        
        self.dir_btn = ctk.CTkButton(
            frame,
            text="Scegli...",
            font=("SF Pro Display", 11),
            width=70,
            height=24,
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["primary"],
            text_color=COLORS["text"],
            corner_radius=6,
            command=self._on_choose_dir,
        )
        self.dir_btn.pack(side="right")
    
    def _setup_quality_info(self):
        """Info qualità consigliata."""
        self.quality_info_label = ctk.CTkLabel(
            self.controls_frame,
            text="",
            font=("SF Pro Display", 11, "italic"),
            text_color=COLORS["accent_cyan"],
        )
        self.quality_info_label.pack(anchor="w", pady=(8, 0))
    
    def update_quality_info(self, profile_id: str):
        """Aggiorna l'info qualità in base al profilo."""
        profile = CDJ_PROFILES.get(profile_id)
        if profile:
            max_sr = profile.max_sample_rate / 1000
            max_bd = profile.max_bit_depth
            self.quality_info_label.configure(
                text=f"💡 Qualità consigliata per {profile.name}: {max_bd}-bit / {max_sr:.1f} kHz"
            )
    
    def set_max_quality(self, profile_id: str):
        """Imposta la massima qualità per il profilo."""
        profile = CDJ_PROFILES.get(profile_id)
        if not profile:
            return
        
        # Imposta bit depth massimo
        self.settings.bit_depth = profile.max_bit_depth
        self.bd_var.set(str(profile.max_bit_depth))
        
        # Imposta sample rate massimo
        self.settings.sample_rate = profile.max_sample_rate
        self.sr_var.set(str(profile.max_sample_rate))
        
        # Aggiorna info
        self.update_quality_info(profile_id)
        self.on_change()
    
    def _on_format_change(self):
        self.settings.output_format = self.format_var.get()
        self.on_change()
    
    def _on_sr_change(self):
        self.settings.sample_rate = int(self.sr_var.get())
        self.on_change()
    
    def _on_bd_change(self):
        self.settings.bit_depth = int(self.bd_var.get())
        self.on_change()
    
    def _on_choose_dir(self):
        dir_path = filedialog.askdirectory(title="Seleziona cartella di destinazione")
        if dir_path:
            self.settings.output_dir = Path(dir_path)
            display_path = dir_path[:30] + "..." if len(dir_path) > 30 else dir_path
            self.dir_label.configure(text=display_path)
            self.on_change()


class ProfileSelector(ctk.CTkFrame):
    """Selettore profilo CDJ moderno con info popup."""

    def __init__(self, master, on_change: callable, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_change = on_change
        
        self.configure(fg_color="transparent")
        
        # Label
        self.label = ctk.CTkLabel(
            self,
            text="Player Target",
            font=("SF Pro Display", 11),
            text_color=COLORS["text_muted"],
        )
        self.label.pack(anchor="w")
        
        # Dropdown container con stile
        self.dropdown_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=10,
        )
        self.dropdown_frame.pack(fill="x", pady=(4, 0))
        
        # Dropdown
        profiles = list(CDJ_PROFILES.keys())
        profile_names = [CDJ_PROFILES[p].name for p in profiles]
        
        self.dropdown = ctk.CTkOptionMenu(
            self.dropdown_frame,
            values=profile_names,
            command=self._on_select,
            font=("SF Pro Display", 13, "bold"),
            dropdown_font=("SF Pro Display", 12),
            fg_color=COLORS["surface"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_dark"],
            text_color=COLORS["text"],
            corner_radius=10,
            dynamic_resizing=False,
            width=200,
        )
        self.dropdown.pack(padx=2, pady=2)
        
        # Pulsante info
        self.info_btn = ctk.CTkButton(
            self,
            text="ℹ️ Info",
            font=("SF Pro Display", 10),
            width=60,
            height=22,
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["primary"],
            text_color=COLORS["text"],
            corner_radius=6,
            command=self._show_info,
        )
        self.info_btn.pack(anchor="w", pady=(4, 0))
        
        # Mappa nome -> id
        self._name_to_id = {CDJ_PROFILES[p].name: p for p in profiles}
    
    def _on_select(self, choice):
        """Callback selezione profilo."""
        profile_id = self._name_to_id.get(choice)
        if profile_id:
            self.on_change(profile_id)
    
    def _show_info(self):
        """Mostra info del profilo selezionato."""
        profile_id = self.get_selected_id()
        profile = CDJ_PROFILES.get(profile_id)
        if not profile:
            return
        
        # Crea dialog info
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Info {profile.name}")
        dialog.geometry("400x300")
        dialog.configure(fg_color=COLORS["background"])
        
        # Titolo
        title = ctk.CTkLabel(
            dialog,
            text=f"📀 {profile.name}",
            font=("SF Pro Display", 18, "bold"),
            text_color=COLORS["text"],
        )
        title.pack(pady=(20, 10))
        
        # Info
        info_text = f"Anno: {profile.year}\n\n"
        info_text += f"{profile.description}\n\n"
        info_text += f"Massima Qualità:\n"
        info_text += f"  • Sample Rate: fino a {profile.max_sample_rate/1000:.1f} kHz\n"
        info_text += f"  • Bit Depth: fino a {profile.max_bit_depth}-bit\n\n"
        info_text += f"Formati supportati:\n  • "
        info_text += "\n  • ".join(profile.formats.keys())
        
        info_label = ctk.CTkLabel(
            dialog,
            text=info_text,
            font=("SF Pro Display", 12),
            text_color=COLORS["text_secondary"],
            justify="left",
        )
        info_label.pack(pady=10, padx=20)
        
        # Pulsante chiudi
        close_btn = ctk.CTkButton(
            dialog,
            text="Chiudi",
            font=("SF Pro Display", 12),
            width=100,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            command=dialog.destroy,
        )
        close_btn.pack(pady=20)
    
    def get_selected_id(self) -> str:
        """Restituisce l'ID del profilo selezionato."""
        name = self.dropdown.get()
        return self._name_to_id.get(name, "cdj_2000_nxs")
    
    def set_profile(self, profile_id: str):
        """Imposta il profilo selezionato."""
        profile = CDJ_PROFILES.get(profile_id)
        if profile:
            self.dropdown.set(profile.name)


class CDJCheckApp:
    """Applicazione CDJ-Check GUI Moderna."""

    def __init__(self):
        """Inizializza l'applicazione."""
        # Setup tema dark moderno
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Finestra principale con supporto drag-and-drop
        self.root = TkinterDnD.Tk()
        self.root.title("CDJ-Check — Audio Compatibility Checker")
        self.root.geometry("1200x900")
        self.root.minsize(1100, 800)
        self.root.configure(bg=COLORS["background"])
        
        # Inizializza engine
        try:
            self.analyzer = AudioAnalyzer()
            self.compatibility = CompatibilityEngine()
            self.converter = AudioConverter(max_workers=2)
        except RuntimeError as e:
            messagebox.showerror(
                "FFmpeg non trovato",
                f"{e}\n\nInstalla FFmpeg per continuare:\n"
                "macOS: brew install ffmpeg\n"
                "Ubuntu: sudo apt-get install ffmpeg\n"
                "Windows: https://ffmpeg.org/download.html"
            )
            sys.exit(1)
        
        # Stato
        self.results: list[CompatibilityResult] = []
        self.file_items: list[FileCard] = []
        self.is_converting = False
        self.conversion_settings = ConversionSettings()
        
        self._setup_ui()
        
        # Imposta massima qualità per il profilo default
        self._apply_max_quality()
    
    def _setup_ui(self):
        """Configura l'interfaccia utente moderna."""
        # Container principale con padding generoso
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=COLORS["background"],
        )
        self.main_frame.pack(fill="both", expand=True, padx=24, pady=24)
        
        self.main_frame.grid_columnconfigure(0, weight=2)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        
        # Header con logo e selettore profilo
        self._setup_header()
        
        # Drop zone moderna
        self._setup_drop_zone()
        
        # Pannello laterale (info + impostazioni)
        self._setup_side_panel()
        
        # Lista file
        self._setup_file_list()
        
        # Action bar
        self._setup_action_bar()
    
    def _setup_header(self):
        """Configura l'header moderno."""
        header = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
        )
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        header.grid_columnconfigure(0, weight=1)
        
        # Logo e titolo
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="w")
        
        # Icona/logo
        self.logo_label = ctk.CTkLabel(
            logo_frame,
            text="◉",
            font=("SF Pro Display", 32),
            text_color=COLORS["primary"],
        )
        self.logo_label.pack(side="left")
        
        # Titolo e sottotitolo
        title_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        title_frame.pack(side="left", padx=(12, 0))
        
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="CDJ-Check",
            font=("SF Pro Display", 24, "bold"),
            text_color=COLORS["text"],
        )
        self.title_label.pack(anchor="w")
        
        self.subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Audio Compatibility Checker",
            font=("SF Pro Display", 12),
            text_color=COLORS["text_secondary"],
        )
        self.subtitle_label.pack(anchor="w")
        
        # Selettore profilo
        self.profile_selector = ProfileSelector(
            header,
            on_change=self._on_profile_change,
        )
        self.profile_selector.grid(row=0, column=1, sticky="e")
    
    def _setup_drop_zone(self):
        """Configura la drop zone moderna."""
        self.drop_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS["surface"],
            border_width=2,
            border_color=COLORS["border"],
            corner_radius=16,
            height=100,
        )
        self.drop_frame.grid(row=1, column=0, columnspan=2, sticky="new", pady=(0, 16))
        self.drop_frame.grid_propagate(False)
        
        # Icona
        self.drop_icon = ctk.CTkLabel(
            self.drop_frame,
            text="↗",
            font=("SF Pro Display", 32),
            text_color=COLORS["primary"],
        )
        self.drop_icon.place(relx=0.5, rely=0.30, anchor="center")
        
        # Testo principale
        self.drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="Trascina i file audio qui",
            font=("SF Pro Display", 14, "bold"),
            text_color=COLORS["text"],
        )
        self.drop_label.place(relx=0.5, rely=0.60, anchor="center")
        
        # Testo secondario
        self.drop_sublabel = ctk.CTkLabel(
            self.drop_frame,
            text="oppure clicca per selezionare",
            font=("SF Pro Display", 10),
            text_color=COLORS["text_muted"],
        )
        self.drop_sublabel.place(relx=0.5, rely=0.78, anchor="center")
        
        # Bind drag-and-drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind("<<Drop>>", self._on_drop)
        
        # Bind click per file picker
        self.drop_frame.bind("<Button-1>", lambda e: self._on_select_files())
        self.drop_icon.bind("<Button-1>", lambda e: self._on_select_files())
        self.drop_label.bind("<Button-1>", lambda e: self._on_select_files())
        self.drop_sublabel.bind("<Button-1>", lambda e: self._on_select_files())
        
        # Hover effects
        self.drop_frame.bind("<Enter>", self._on_drop_enter)
        self.drop_frame.bind("<Leave>", self._on_drop_leave)
    
    def _setup_side_panel(self):
        """Configura il pannello laterale con info e impostazioni."""
        self.side_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.side_panel.grid(row=2, column=1, rowspan=2, sticky="nsew", padx=(16, 0))
        
        # Pannello info profilo
        self.profile_info = ProfileInfoPanel(self.side_panel)
        self.profile_info.pack(fill="x", pady=(0, 12))
        
        # Pannello impostazioni conversione
        self.settings_panel = ConversionSettingsPanel(
            self.side_panel,
            settings=self.conversion_settings,
            on_change=self._on_settings_change,
        )
        self.settings_panel.pack(fill="x")
    
    def _setup_file_list(self):
        """Configura la lista file moderna."""
        # Container principale
        self.list_container = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
        )
        self.list_container.grid(row=2, column=0, rowspan=2, sticky="nsew", pady=(0, 16))
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(1, weight=1)
        
        # Header con contatore
        self.list_header = ctk.CTkFrame(
            self.list_container,
            fg_color="transparent",
            height=30,
        )
        self.list_header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        
        self.list_title = ctk.CTkLabel(
            self.list_header,
            text="File",
            font=("SF Pro Display", 14, "bold"),
            text_color=COLORS["text"],
        )
        self.list_title.pack(side="left")
        
        self.count_badge = ctk.CTkLabel(
            self.list_header,
            text="0",
            font=("SF Pro Display", 12, "bold"),
            text_color=COLORS["text"],
            fg_color=COLORS["surface"],
            corner_radius=10,
            width=28,
            height=20,
        )
        self.count_badge.pack(side="left", padx=(8, 0))
        
        # Frame scrollabile per le card
        self.list_frame = ctk.CTkScrollableFrame(
            self.list_container,
            fg_color="transparent",
            corner_radius=0,
        )
        self.list_frame.grid(row=1, column=0, sticky="nsew")
        
        # Label vuota
        self.empty_label = ctk.CTkLabel(
            self.list_frame,
            text="Nessun file caricato",
            font=("SF Pro Display", 14),
            text_color=COLORS["text_muted"],
        )
        self.empty_label.pack(pady=60)
    
    def _setup_action_bar(self):
        """Configura la barra azioni moderna."""
        action_bar = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS["surface"],
            corner_radius=12,
            height=70,
        )
        action_bar.grid(row=4, column=0, columnspan=2, sticky="ew")
        action_bar.grid_propagate(False)
        
        # Info conversione
        self.info_label = ctk.CTkLabel(
            action_bar,
            text="",
            font=("SF Pro Display", 12),
            text_color=COLORS["text_secondary"],
        )
        self.info_label.place(relx=0.02, rely=0.5, anchor="w")
        
        # Pulsante pulisci
        self.clear_btn = ctk.CTkButton(
            action_bar,
            text="Pulisci",
            font=("SF Pro Display", 13, "bold"),
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["incompatible"],
            text_color=COLORS["text"],
            width=100,
            height=36,
            corner_radius=8,
            command=self._on_clear,
            state="disabled",
        )
        self.clear_btn.place(relx=0.98, rely=0.5, anchor="e", x=-160)
        
        # Pulsante converti
        self.convert_btn = ctk.CTkButton(
            action_bar,
            text="Converti",
            font=("SF Pro Display", 14, "bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            text_color=COLORS["text"],
            width=140,
            height=40,
            corner_radius=10,
            command=self._on_convert,
            state="disabled",
        )
        self.convert_btn.place(relx=0.98, rely=0.5, anchor="e", x=-10)
        
        # Progress bar (nascosta inizialmente)
        self.progress = ctk.CTkProgressBar(
            action_bar,
            width=200,
            height=6,
            mode="determinate",
            progress_color=COLORS["primary"],
            fg_color=COLORS["surface_light"],
        )
        self.progress.set(0)
    
    def _apply_max_quality(self):
        """Applica la massima qualità per il profilo corrente."""
        profile_id = self.compatibility.profile_id
        self.settings_panel.set_max_quality(profile_id)
        self.profile_info.update_info(profile_id)
    
    def _on_settings_change(self):
        """Callback cambio impostazioni."""
        pass
    
    def _on_profile_change(self, profile_id: str):
        """Callback cambio profilo."""
        self.compatibility.set_profile(profile_id)
        
        # Aggiorna info profilo
        self.profile_info.update_info(profile_id)
        
        # Imposta massima qualità automaticamente
        self.settings_panel.set_max_quality(profile_id)
        
        # Rianalizza i file esistenti con il nuovo profilo
        if self.results:
            new_results = []
            for result in self.results:
                try:
                    metadata = result.metadata
                    if metadata:
                        new_result = self.compatibility.check(metadata)
                        new_results.append(new_result)
                    else:
                        new_results.append(result)
                except Exception:
                    new_results.append(result)
            
            self.results = new_results
            self._update_file_list()
    
    def _on_drop_enter(self, event):
        """Callback quando il mouse entra nella drop zone."""
        if not self.is_converting:
            self.drop_frame.configure(
                border_color=COLORS["primary"],
                fg_color=COLORS["surface_light"],
            )
            self.drop_icon.configure(text_color=COLORS["primary_light"])
    
    def _on_drop_leave(self, event):
        """Callback quando il mouse esce dalla drop zone."""
        if not self.is_converting:
            self.drop_frame.configure(
                border_color=COLORS["border"],
                fg_color=COLORS["surface"],
            )
            self.drop_icon.configure(text_color=COLORS["primary"])
    
    def _on_drop(self, event):
        """Callback per drop di file."""
        if self.is_converting:
            return
        
        # Parse file path(s)
        data = event.data
        
        # TkinterDnD può restituire path con {} per spazi su macOS
        if "{" in data:
            paths = []
            current = ""
            in_brace = False
            for char in data:
                if char == "{":
                    in_brace = True
                    current = ""
                elif char == "}":
                    in_brace = False
                    paths.append(current)
                elif in_brace:
                    current += char
                elif char != " ":
                    current += char
        else:
            paths = data.split()
        
        file_paths = []
        for path in paths:
            path = Path(path.strip())
            if path.is_file():
                file_paths.append(path)
            elif path.is_dir():
                # Aggiungi tutti i file audio nella cartella
                for ext in [".mp3", ".m4a", ".wav", ".aiff", ".aif", ".flac", ".ogg", ".opus", ".wma"]:
                    file_paths.extend(path.glob(f"*{ext}"))
                    file_paths.extend(path.glob(f"*{ext.upper()}"))
        
        if file_paths:
            self._analyze_files(file_paths)
    
    def _on_select_files(self):
        """Callback per selezione file."""
        if self.is_converting:
            return
        
        file_paths = filedialog.askopenfilenames(
            title="Seleziona file audio",
            filetypes=[
                ("Audio files", "*.mp3 *.m4a *.wav *.aiff *.aif *.flac *.ogg *.opus *.wma"),
                ("All files", "*.*"),
            ],
        )
        
        if file_paths:
            self._analyze_files([Path(p) for p in file_paths])
    
    def _analyze_files(self, file_paths: list[Path]):
        """Analizza i file selezionati."""
        # Aggiorna UI
        self.drop_label.configure(text="Analisi in corso...")
        self.root.update()
        
        # Analizza
        new_results = []
        for path in file_paths:
            try:
                metadata = self.analyzer.analyze(path)
                result = self.compatibility.check(metadata)
                new_results.append(result)
            except Exception as e:
                # Crea risultato errore
                metadata = AudioMetadata(
                    filepath=path,
                    filename=path.name,
                    format_name="UNKNOWN",
                    codec="ERROR",
                    sample_rate=None,
                    bit_depth=None,
                    channels=0,
                    bitrate=None,
                    duration=None,
                    is_lossy=False,
                    is_float=False,
                )
                from cdj_check.compatibility import CompatibilityStatus
                result = CompatibilityResult(
                    filepath=path,
                    metadata=metadata,
                    status=CompatibilityStatus.ERROR,
                    message=str(e)[:60],
                    profile_id=self.compatibility.profile_id,
                    profile_name=self.compatibility.profile.name,
                )
                new_results.append(result)
        
        # Aggiungi ai risultati esistenti
        self.results.extend(new_results)
        self._update_file_list()
        
        # Reset drop zone
        self.drop_label.configure(text="Trascina i file audio qui")
    
    def _update_file_list(self):
        """Aggiorna la lista file nella UI."""
        # Rimuovi vecchie card
        for item in self.file_items:
            item.destroy()
        self.file_items.clear()
        
        # Nascondi label vuota se ci sono file
        if self.results:
            self.empty_label.pack_forget()
        else:
            self.empty_label.pack(pady=60)
        
        # Aggiungi nuove card
        for result in self.results:
            card = FileCard(
                self.list_frame,
                result=result,
                on_remove=lambda r=result: self._on_remove_file(r),
                on_convert_single=lambda r=result: self._on_convert_single(r),
            )
            card.pack(fill="x", pady=(0, 8))
            self.file_items.append(card)
        
        # Aggiorna contatore
        count = len(self.results)
        self.count_badge.configure(text=str(count))
        
        # Aggiorna info conversione
        to_convert = sum(1 for r in self.results if r.needs_conversion)
        compatible = sum(1 for r in self.results if r.is_compatible)
        errors = sum(1 for r in self.results if r.status == CompatibilityStatus.ERROR)
        
        info_parts = []
        if compatible:
            info_parts.append(f"{compatible} pronti")
        if to_convert:
            info_parts.append(f"{to_convert} da convertire")
        if errors:
            info_parts.append(f"{errors} errori")
        
        self.info_label.configure(text=" • ".join(info_parts) if info_parts else "")
        
        # Abilita/disabilita pulsanti
        self.clear_btn.configure(state="normal" if self.results else "disabled")
        
        if to_convert and not self.is_converting:
            self.convert_btn.configure(state="normal", text=f"Converti ({to_convert})")
        else:
            self.convert_btn.configure(state="disabled", text="Converti")
    
    def _on_remove_file(self, result: CompatibilityResult):
        """Rimuove un file dalla lista."""
        if result in self.results:
            self.results.remove(result)
            self._update_file_list()
    
    def _on_convert_single(self, result: CompatibilityResult):
        """Converte un singolo file."""
        if not result.needs_conversion:
            return
        
        # Crea conversion plan personalizzato
        custom_plan = ConversionPlan(
            output_format=self.conversion_settings.output_format,
            target_sample_rate=self.conversion_settings.sample_rate,
            target_bit_depth=self.conversion_settings.bit_depth,
            reason=f"Personalizzato: {self.conversion_settings.bit_depth}bit/{self.conversion_settings.sample_rate/1000:.1f}kHz",
        )
        
        # Crea risultato modificato con piano personalizzato
        modified_result = CompatibilityResult(
            filepath=result.filepath,
            metadata=result.metadata,
            status=result.status,
            message=result.message,
            profile_id=result.profile_id,
            profile_name=result.profile_name,
            conversion_plan=custom_plan,
        )
        
        # Converti
        self.is_converting = True
        self.convert_btn.configure(state="disabled", text="Conversione...")
        self.clear_btn.configure(state="disabled")
        
        self.root.after(100, lambda: self._do_single_conversion(modified_result))
    
    def _do_single_conversion(self, result: CompatibilityResult):
        """Esegue conversione singolo file."""
        output_dir = self.conversion_settings.output_dir
        conv_result = self.converter.convert(result, output_dir=output_dir)
        
        self.is_converting = False
        self.convert_btn.configure(state="normal", text="Converti")
        self.clear_btn.configure(state="normal")
        
        if conv_result.success:
            message = f"✅ Conversione completata!\n\nFile salvato in:\n{conv_result.output_path}"
            messagebox.showinfo("Conversione Completata", message)
        else:
            messagebox.showerror("Errore Conversione", f"❌ {conv_result.message}")
    
    def _on_clear(self):
        """Pulisce tutti i file."""
        if self.is_converting:
            return
        
        self.results.clear()
        self._update_file_list()
    
    def _on_convert(self):
        """Avvia la conversione batch."""
        if self.is_converting:
            return
        
        to_convert = [r for r in self.results if r.needs_conversion]
        if not to_convert:
            return
        
        self.is_converting = True
        self.convert_btn.configure(state="disabled", text="Conversione...")
        self.clear_btn.configure(state="disabled")
        
        # Mostra progress bar
        self.progress.place(relx=0.35, rely=0.5, anchor="w")
        
        # Esegui conversione in background
        self.root.after(100, lambda: self._do_conversion_batch(to_convert))
    
    def _do_conversion_batch(self, to_convert: list[CompatibilityResult]):
        """Esegue conversione batch."""
        total = len(to_convert)
        
        def on_progress(done: int, total: int):
            self.progress.set(done / total)
            self.root.update()
        
        # Crea piani di conversione personalizzati
        custom_results = []
        for result in to_convert:
            custom_plan = ConversionPlan(
                output_format=self.conversion_settings.output_format,
                target_sample_rate=self.conversion_settings.sample_rate,
                target_bit_depth=self.conversion_settings.bit_depth,
                reason=f"Personalizzato: {self.conversion_settings.bit_depth}bit/{self.conversion_settings.sample_rate/1000:.1f}kHz",
            )
            
            custom_result = CompatibilityResult(
                filepath=result.filepath,
                metadata=result.metadata,
                status=result.status,
                message=result.message,
                profile_id=result.profile_id,
                profile_name=result.profile_name,
                conversion_plan=custom_plan,
            )
            custom_results.append(custom_result)
        
        output_dir = self.conversion_settings.output_dir
        results = self.converter.convert_batch(custom_results, output_dir=output_dir, progress_callback=on_progress)
        
        # Aggiorna UI finale
        self.is_converting = False
        
        to_convert_count = sum(1 for r in self.results if r.needs_conversion)
        self.convert_btn.configure(
            text=f"Converti ({to_convert_count})" if to_convert_count else "Converti",
            state="normal" if to_convert_count else "disabled",
        )
        self.clear_btn.configure(state="normal")
        self.progress.place_forget()
        self.progress.set(0)
        
        # Mostra risultato
        summary = self.converter.get_conversion_summary(results)
        if summary["failed"] == 0:
            message = f"✅ {summary['successful']} file convertiti con successo!"
            if self.conversion_settings.output_dir:
                message += f"\n\nCartella: {self.conversion_settings.output_dir}"
            else:
                message += "\n\nI file sono stati salvati nelle rispettive cartelle 'CDJ_Ready'."
            
            messagebox.showinfo("Conversione Completata", message)
        else:
            messagebox.showwarning(
                "Conversione completata con errori",
                f"⚠️ {summary['successful']} successi, {summary['failed']} fallimenti\n\n"
                f"Controlla i dettagli nella lista file."
            )
    
    def run(self):
        """Avvia l'applicazione."""
        self.root.mainloop()


def main():
    """Entry point per la GUI."""
    app = CDJCheckApp()
    app.run()


if __name__ == "__main__":
    main()
