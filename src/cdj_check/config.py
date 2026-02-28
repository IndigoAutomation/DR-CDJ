"""Configurazioni e costanti per CDJ-Check con supporto multipli modelli."""

from dataclasses import dataclass
from typing import Set, Dict


@dataclass(frozen=True)
class AudioFormat:
    """Rappresenta un formato audio supportato."""

    name: str
    extensions: Set[str]
    sample_rates: Set[int]
    bit_depths: Set[int]
    is_lossless: bool


@dataclass(frozen=True)
class CDJProfile:
    """Profilo di compatibilità per un modello CDJ."""

    id: str
    name: str
    year: int
    description: str
    formats: Dict[str, AudioFormat]
    max_sample_rate: int
    max_bit_depth: int
    supports_lossless: bool


# ============================================================
# PROFILI CDJ SUPPORTATI
# ============================================================

CDJ_PROFILES = {
    "cdj_2000_nxs": CDJProfile(
        id="cdj_2000_nxs",
        name="CDJ-2000 Nexus",
        year=2012,
        description="Prima generazione Nexus - Standard nei club",
        formats={
            "MP3": AudioFormat(
                name="MP3",
                extensions={".mp3"},
                sample_rates={44100},
                bit_depths=set(),
                is_lossless=False,
            ),
            "AAC": AudioFormat(
                name="AAC",
                extensions={".m4a", ".aac", ".mp4"},
                sample_rates={44100, 48000},
                bit_depths=set(),
                is_lossless=False,
            ),
            "WAV": AudioFormat(
                name="WAV",
                extensions={".wav", ".wave"},
                sample_rates={44100, 48000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "AIFF": AudioFormat(
                name="AIFF",
                extensions={".aiff", ".aif"},
                sample_rates={44100, 48000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
        },
        max_sample_rate=48000,
        max_bit_depth=24,
        supports_lossless=True,
    ),
    
    "cdj_2000_nxs2": CDJProfile(
        id="cdj_2000_nxs2",
        name="CDJ-2000 Nexus 2",
        year=2016,
        description="Seconda generazione - Aggiunge FLAC e schermo più grande",
        formats={
            "MP3": AudioFormat(
                name="MP3",
                extensions={".mp3"},
                sample_rates={44100},
                bit_depths=set(),
                is_lossless=False,
            ),
            "AAC": AudioFormat(
                name="AAC",
                extensions={".m4a", ".aac", ".mp4"},
                sample_rates={44100, 48000},
                bit_depths=set(),
                is_lossless=False,
            ),
            "WAV": AudioFormat(
                name="WAV",
                extensions={".wav", ".wave"},
                sample_rates={44100, 48000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "AIFF": AudioFormat(
                name="AIFF",
                extensions={".aiff", ".aif"},
                sample_rates={44100, 48000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "FLAC": AudioFormat(
                name="FLAC",
                extensions={".flac"},
                sample_rates={44100, 48000, 88200, 96000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
        },
        max_sample_rate=96000,
        max_bit_depth=24,
        supports_lossless=True,
    ),
    
    "cdj_3000": CDJProfile(
        id="cdj_3000",
        name="CDJ-3000",
        year=2020,
        description="Flagship attuale - Supporta alta risoluzione",
        formats={
            "MP3": AudioFormat(
                name="MP3",
                extensions={".mp3"},
                sample_rates={44100, 48000},
                bit_depths=set(),
                is_lossless=False,
            ),
            "AAC": AudioFormat(
                name="AAC",
                extensions={".m4a", ".aac", ".mp4"},
                sample_rates={44100, 48000},
                bit_depths=set(),
                is_lossless=False,
            ),
            "WAV": AudioFormat(
                name="WAV",
                extensions={".wav", ".wave"},
                sample_rates={44100, 48000, 88200, 96000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "AIFF": AudioFormat(
                name="AIFF",
                extensions={".aiff", ".aif"},
                sample_rates={44100, 48000, 88200, 96000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "FLAC": AudioFormat(
                name="FLAC",
                extensions={".flac"},
                sample_rates={44100, 48000, 88200, 96000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "ALAC": AudioFormat(
                name="ALAC",
                extensions={".m4a"},
                sample_rates={44100, 48000, 88200, 96000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
        },
        max_sample_rate=96000,
        max_bit_depth=24,
        supports_lossless=True,
    ),
    
    "xdj_1000_mk2": CDJProfile(
        id="xdj_1000_mk2",
        name="XDJ-1000MK2",
        year=2017,
        description="Player senza drive ottico - Supporta FLAC",
        formats={
            "MP3": AudioFormat(
                name="MP3",
                extensions={".mp3"},
                sample_rates={44100},
                bit_depths=set(),
                is_lossless=False,
            ),
            "AAC": AudioFormat(
                name="AAC",
                extensions={".m4a", ".aac", ".mp4"},
                sample_rates={44100, 48000},
                bit_depths=set(),
                is_lossless=False,
            ),
            "WAV": AudioFormat(
                name="WAV",
                extensions={".wav", ".wave"},
                sample_rates={44100, 48000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "AIFF": AudioFormat(
                name="AIFF",
                extensions={".aiff", ".aif"},
                sample_rates={44100, 48000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "FLAC": AudioFormat(
                name="FLAC",
                extensions={".flac"},
                sample_rates={44100, 48000, 88200, 96000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "ALAC": AudioFormat(
                name="ALAC",
                extensions={".m4a"},
                sample_rates={44100, 48000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
        },
        max_sample_rate=96000,
        max_bit_depth=24,
        supports_lossless=True,
    ),
    
    "xdj_700": CDJProfile(
        id="xdj_700",
        name="XDJ-700",
        year=2015,
        description="Entry-level compatto - Simile a CDJ-2000NXS",
        formats={
            "MP3": AudioFormat(
                name="MP3",
                extensions={".mp3"},
                sample_rates={44100},
                bit_depths=set(),
                is_lossless=False,
            ),
            "AAC": AudioFormat(
                name="AAC",
                extensions={".m4a", ".aac", ".mp4"},
                sample_rates={44100, 48000},
                bit_depths=set(),
                is_lossless=False,
            ),
            "WAV": AudioFormat(
                name="WAV",
                extensions={".wav", ".wave"},
                sample_rates={44100, 48000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
            "AIFF": AudioFormat(
                name="AIFF",
                extensions={".aiff", ".aif"},
                sample_rates={44100, 48000},
                bit_depths={16, 24},
                is_lossless=True,
            ),
        },
        max_sample_rate=48000,
        max_bit_depth=24,
        supports_lossless=True,
    ),
}

# Profilo di default
DEFAULT_PROFILE = "cdj_2000_nxs"

# ============================================================
# FORMATI CONVERTIBILI
# Questi formati possono essere convertiti per qualsiasi profilo
# ============================================================

CONVERTIBLE_FORMATS = {
    "FLAC": AudioFormat(
        name="FLAC",
        extensions={".flac"},
        sample_rates=set(),
        bit_depths=set(),
        is_lossless=True,
    ),
    "OGG": AudioFormat(
        name="OGG Vorbis",
        extensions={".ogg", ".oga"},
        sample_rates=set(),
        bit_depths=set(),
        is_lossless=False,
    ),
    "OPUS": AudioFormat(
        name="OPUS",
        extensions={".opus"},
        sample_rates=set(),
        bit_depths=set(),
        is_lossless=False,
    ),
    "WMA": AudioFormat(
        name="WMA",
        extensions={".wma"},
        sample_rates=set(),
        bit_depths=set(),
        is_lossless=False,
    ),
    "ALAC": AudioFormat(
        name="ALAC",
        extensions={".m4a"},
        sample_rates=set(),
        bit_depths=set(),
        is_lossless=True,
    ),
}

# Tutti i formati riconosciuti (per analisi)
ALL_FORMATS = {}
for profile in CDJ_PROFILES.values():
    ALL_FORMATS.update(profile.formats)
ALL_FORMATS.update(CONVERTIBLE_FORMATS)

# Preferenze di conversione
DEFAULT_OUTPUT_FORMAT = "WAV"
DEFAULT_SAMPLE_RATE = 48000
DEFAULT_BIT_DEPTH = 24

# Limiti tecnici generali
MAX_SAMPLE_RATE = 96000
MAX_BIT_DEPTH = 24
SUPPORTED_BIT_DEPTHS = {16, 24}
SUPPORTED_SAMPLE_RATES = {44100, 48000, 88200, 96000}

# Configurazione FFmpeg
FFPROBE_TIMEOUT = 30
FFMPEG_TIMEOUT = 300

# Configurazione batch
DEFAULT_MAX_WORKERS = 2
MAX_MAX_WORKERS = 4

# Stati di compatibilità
COMPATIBLE = "compatible"
CONVERTIBLE_LOSSLESS = "convertible_lossless"
CONVERTIBLE_LOSSY = "convertible_lossy"
INCOMPATIBLE = "incompatible"
ERROR = "error"

# ============================================================
# COLORI MODERNI PER UI (Dark Theme Premium)
# ============================================================

COLORS = {
    # Colori principali - Gradients
    "primary": "#6366f1",           # Indigo 500
    "primary_light": "#818cf8",     # Indigo 400
    "primary_dark": "#4f46e5",      # Indigo 600
    
    # Stati compatibilità
    "compatible": "#22c55e",        # Verde 500
    "compatible_bg": "#14532d",     # Verde 900
    "convertible_lossless": "#f59e0b",  # Amber 500
    "convertible_lossless_bg": "#78350f",  # Amber 900
    "convertible_lossy": "#f97316", # Orange 500
    "convertible_lossy_bg": "#7c2d12",  # Orange 900
    "incompatible": "#ef4444",      # Rosso 500
    "incompatible_bg": "#7f1d1d",   # Rosso 900
    "error": "#dc2626",             # Rosso 600
    "error_bg": "#7f1d1d",          # Rosso 900
    
    # Sfondi e superfici
    "background": "#0f0f11",        # Quasi nero con tinta blu
    "surface": "#1a1a1f",           # Superficie scura
    "surface_light": "#25252d",     # Superficie più chiara
    "surface_hover": "#2d2d38",     # Hover state
    "border": "#3f3f46",            # Bordi
    "border_highlight": "#6366f1",  # Bordo evidenziato
    
    # Testo
    "text": "#fafafa",              # Bianco quasi puro
    "text_secondary": "#a1a1aa",    # Grigio chiaro
    "text_muted": "#71717a",        # Grigio muto
    "text_inverse": "#18181b",      # Testo su sfondo chiaro
    
    # Accent colors
    "accent_cyan": "#06b6d4",       # Cyan 500
    "accent_pink": "#ec4899",       # Pink 500
    "accent_purple": "#8b5cf6",     # Purple 500
    "accent_blue": "#3b82f6",       # Blue 500
}

# Colori per profili CDJ (gradienti)
PROFILE_COLORS = {
    "cdj_2000_nxs": ("#f59e0b", "#d97706"),    # Amber
    "cdj_2000_nxs2": ("#ec4899", "#db2777"),  # Pink
    "cdj_3000": ("#8b5cf6", "#7c3aed"),       # Purple
    "xdj_1000_mk2": ("#06b6d4", "#0891b2"),   # Cyan
    "xdj_700": ("#22c55e", "#16a34a"),        # Green
}


def get_profile_color(profile_id: str) -> tuple:
    """Restituisce i colori del gradiente per un profilo."""
    return PROFILE_COLORS.get(profile_id, (COLORS["primary"], COLORS["primary_dark"]))
