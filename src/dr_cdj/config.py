"""Configuration and constants for Dr.CDJ with multi-model support."""

from dataclasses import dataclass
from typing import Set, Dict


@dataclass(frozen=True)
class AudioFormat:
    """Represents a supported audio format."""

    name: str
    extensions: Set[str]
    sample_rates: Set[int]
    bit_depths: Set[int]
    is_lossless: bool


@dataclass(frozen=True)
class CDJProfile:
    """Compatibility profile for a CDJ model."""

    id: str
    name: str
    year: int
    description: str
    formats: Dict[str, AudioFormat]
    max_sample_rate: int
    max_bit_depth: int
    supports_lossless: bool


# ============================================================
# SUPPORTED CDJ PROFILES
# ============================================================

CDJ_PROFILES = {
    "cdj_2000_nxs": CDJProfile(
        id="cdj_2000_nxs",
        name="CDJ-2000 Nexus",
        year=2012,
        description="First generation Nexus - Club standard",
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
        description="Second generation - Adds FLAC and larger screen",
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
        description="Current flagship - High resolution support",
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
        description="Optical drive-less player - FLAC support",
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
        description="Compact entry-level - Similar to CDJ-2000NXS",
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

# Default profile
DEFAULT_PROFILE = "cdj_2000_nxs"

# ============================================================
# CONVERTIBLE FORMATS
# These formats can be converted for any profile
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

# All recognized formats (for analysis)
ALL_FORMATS = {}
for profile in CDJ_PROFILES.values():
    ALL_FORMATS.update(profile.formats)
ALL_FORMATS.update(CONVERTIBLE_FORMATS)

# Conversion preferences
DEFAULT_OUTPUT_FORMAT = "WAV"
DEFAULT_SAMPLE_RATE = 48000
DEFAULT_BIT_DEPTH = 24

# General technical limits
MAX_SAMPLE_RATE = 96000
MAX_BIT_DEPTH = 24
SUPPORTED_BIT_DEPTHS = {16, 24}
SUPPORTED_SAMPLE_RATES = {44100, 48000, 88200, 96000}

# FFmpeg configuration
FFPROBE_TIMEOUT = 30
FFMPEG_TIMEOUT = 300

# Batch configuration
DEFAULT_MAX_WORKERS = 2
MAX_MAX_WORKERS = 4

# Compatibility states
COMPATIBLE = "compatible"
CONVERTIBLE_LOSSLESS = "convertible_lossless"
CONVERTIBLE_LOSSY = "convertible_lossy"
INCOMPATIBLE = "incompatible"
ERROR = "error"

# ============================================================
# MODERN UI COLORS (Dark Theme — aligned with landing page)
# ============================================================

COLORS = {
    # Main colors — coral brand (CTA, logo, accents)
    "primary": "#d94f4f",           # Coral
    "primary_light": "#e06a6a",     # Coral light
    "primary_dark": "#c96418",      # Peach (gradient end)

    # Compatibility states
    "compatible": "#3db88a",        # Mint
    "compatible_bg": "#1b2b2b",     # Mint tint on bg-card
    "convertible_lossless": "#c9a820",  # Sunshine
    "convertible_lossless_bg": "#2e291d",  # Sunshine tint on bg-card
    "convertible_lossy": "#c96418", # Peach (warm orange)
    "convertible_lossy_bg": "#33231e",  # Peach tint on bg-card
    "incompatible": "#d94f4f",      # Coral
    "incompatible_bg": "#2f1d23",   # Coral tint on bg-card
    "error": "#d94f4f",             # Coral
    "error_bg": "#2f1d23",          # Coral tint on bg-card

    # Backgrounds and surfaces
    "background": "#090909",        # Landing --bg
    "surface": "#18181f",           # Landing --bg-card
    "surface_light": "#222228",     # rgba(255,255,255,0.08) su bg-card
    "surface_hover": "#292934",     # rgba(255,255,255,0.10) su bg-card
    "border": "#1e1e25",            # rgba(255,255,255,0.05) su bg-card
    "border_highlight": "#d94f4f",  # Coral border

    # Text
    "text": "#f0f0f0",              # Landing --text
    "text_secondary": "#8a8a94",    # Landing --text-dim
    "text_muted": "#5a5a64",        # Landing --text-muted
    "text_inverse": "#0a0a0d",      # Testo scuro su bottoni chiari (mint/turquoise)

    # Accent colors
    "accent_cyan": "#33a89f",       # Turquoise
    "accent_purple": "#8b50d4",     # Lavender
    "accent_blue": "#3080d8",       # Sky
}

# CDJ profile colors (gradients) — landing palette
PROFILE_COLORS = {
    "cdj_2000_nxs": ("#c9a820", "#a88a1a"),    # Sunshine
    "cdj_2000_nxs2": ("#d94f4f", "#c96418"),   # Coral → Peach
    "cdj_3000": ("#8b50d4", "#6b3aaa"),        # Lavender
    "xdj_1000_mk2": ("#33a89f", "#2a8a82"),    # Turquoise
    "xdj_700": ("#3db88a", "#2a9870"),         # Mint
}


def get_profile_color(profile_id: str) -> tuple:
    """Return gradient colors for a profile."""
    return PROFILE_COLORS.get(profile_id, (COLORS["primary"], COLORS["primary_dark"]))
