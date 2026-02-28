"""CDJ-Check: Audio Compatibility Checker & Converter per Pioneer CDJ-2000 Nexus."""

__version__ = "0.1.0"
__author__ = "CDJ-Check Team"

from cdj_check.analyzer import AudioAnalyzer
from cdj_check.compatibility import CompatibilityEngine, CompatibilityResult
from cdj_check.utils import get_ffmpeg_path, get_ffprobe_path, get_resource_path

__all__ = [
    "AudioAnalyzer",
    "CompatibilityEngine",
    "CompatibilityResult",
    "get_ffmpeg_path",
    "get_ffprobe_path",
    "get_resource_path",
]
