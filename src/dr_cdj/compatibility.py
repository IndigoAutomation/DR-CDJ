"""CompatibilityEngine: Multi-profile compatibility engine for CDJ."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from dr_cdj.analyzer import AudioMetadata
from dr_cdj.config import (
    CDJ_PROFILES,
    CONVERTIBLE_FORMATS,
    DEFAULT_PROFILE,
    DEFAULT_BIT_DEPTH,
    DEFAULT_SAMPLE_RATE,
    MAX_BIT_DEPTH,
    MAX_SAMPLE_RATE,
    CDJProfile,
)


class CompatibilityStatus(Enum):
    """Possible compatibility states."""

    COMPATIBLE = "compatible"
    CONVERTIBLE_LOSSLESS = "convertible_lossless"
    CONVERTIBLE_LOSSY = "convertible_lossy"
    INCOMPATIBLE = "incompatible"
    ERROR = "error"


@dataclass
class ConversionPlan:
    """Optimal conversion plan."""

    output_format: str
    target_sample_rate: int
    target_bit_depth: int
    reason: str


@dataclass
class CompatibilityResult:
    """Compatibility check result."""

    filepath: Path
    metadata: AudioMetadata
    status: CompatibilityStatus
    message: str
    profile_id: str
    profile_name: str
    conversion_plan: Optional[ConversionPlan] = None

    @property
    def is_compatible(self) -> bool:
        """True if file is already compatible."""
        return self.status == CompatibilityStatus.COMPATIBLE

    @property
    def needs_conversion(self) -> bool:
        """True if file needs conversion."""
        return self.status in (
            CompatibilityStatus.CONVERTIBLE_LOSSLESS,
            CompatibilityStatus.CONVERTIBLE_LOSSY,
        )

    @property
    def status_icon(self) -> str:
        """Status representative icon."""
        icons = {
            CompatibilityStatus.COMPATIBLE: "✓",
            CompatibilityStatus.CONVERTIBLE_LOSSLESS: "⇄",
            CompatibilityStatus.CONVERTIBLE_LOSSY: "⚠",
            CompatibilityStatus.INCOMPATIBLE: "✕",
            CompatibilityStatus.ERROR: "!",
        }
        return icons.get(self.status, "?")

    @property
    def status_color(self) -> str:
        """Color associated with status."""
        from dr_cdj.config import COLORS
        colors = {
            CompatibilityStatus.COMPATIBLE: COLORS["compatible"],
            CompatibilityStatus.CONVERTIBLE_LOSSLESS: COLORS["convertible_lossless"],
            CompatibilityStatus.CONVERTIBLE_LOSSY: COLORS["convertible_lossy"],
            CompatibilityStatus.INCOMPATIBLE: COLORS["incompatible"],
            CompatibilityStatus.ERROR: COLORS["error"],
        }
        return colors.get(self.status, COLORS["text_secondary"])

    @property
    def status_bg_color(self) -> str:
        """Background color associated with status."""
        from dr_cdj.config import COLORS
        colors = {
            CompatibilityStatus.COMPATIBLE: COLORS["compatible_bg"],
            CompatibilityStatus.CONVERTIBLE_LOSSLESS: COLORS["convertible_lossless_bg"],
            CompatibilityStatus.CONVERTIBLE_LOSSY: COLORS["convertible_lossy_bg"],
            CompatibilityStatus.INCOMPATIBLE: COLORS["incompatible_bg"],
            CompatibilityStatus.ERROR: COLORS["error_bg"],
        }
        return colors.get(self.status, COLORS["surface"])


class CompatibilityEngine:
    """Multi-profile compatibility engine for CDJ."""

    def __init__(self, profile_id: Optional[str] = None):
        """Initialize compatibility engine.
        
        Args:
            profile_id: CDJ profile ID to use. If None, uses default.
        """
        self.profile_id = profile_id or DEFAULT_PROFILE
        self.profile = CDJ_PROFILES.get(self.profile_id, CDJ_PROFILES[DEFAULT_PROFILE])

    def set_profile(self, profile_id: str) -> bool:
        """Change CDJ profile.
        
        Args:
            profile_id: New profile ID.
            
        Returns:
            True if profile was changed, False otherwise.
        """
        if profile_id in CDJ_PROFILES:
            self.profile_id = profile_id
            self.profile = CDJ_PROFILES[profile_id]
            return True
        return False

    def get_available_profiles(self) -> dict:
        """Return available profiles."""
        return {
            pid: {
                "name": p.name,
                "year": p.year,
                "description": p.description,
                "formats": list(p.formats.keys()),
            }
            for pid, p in CDJ_PROFILES.items()
        }

    def check(self, metadata: AudioMetadata) -> CompatibilityResult:
        """Check audio file compatibility.
        
        Args:
            metadata: Audio file metadata.
            
        Returns:
            CompatibilityResult with verdict and conversion plan.
        """
        try:
            return self._evaluate(metadata)
        except Exception as e:
            return CompatibilityResult(
                filepath=metadata.filepath,
                metadata=metadata,
                status=CompatibilityStatus.ERROR,
                message=f"Error: {str(e)[:50]}",
                profile_id=self.profile_id,
                profile_name=self.profile.name,
            )

    def _evaluate(self, metadata: AudioMetadata) -> CompatibilityResult:
        """Compatibility evaluation logic."""
        filepath = metadata.filepath
        codec = metadata.codec
        sample_rate = metadata.sample_rate
        bit_depth = metadata.bit_depth
        is_float = metadata.is_float
        is_lossy = metadata.is_lossy
        
        # Determina il formato base
        format_category = self._detect_format_category(metadata)
        
        # Verifica se il formato è supportato dal profilo
        if format_category in self.profile.formats:
            return self._check_supported_format(
                filepath, metadata, format_category, sample_rate, bit_depth, is_float
            )
        elif format_category in CONVERTIBLE_FORMATS:
            # Formato convertibile ma non nativo
            return self._check_unsupported_format(
                filepath, metadata, format_category, is_lossy
            )
        else:
            # Formato sconosciuto/incompatibile
            return CompatibilityResult(
                filepath=filepath,
                metadata=metadata,
                status=CompatibilityStatus.INCOMPATIBLE,
                message=f"{format_category} format not supported",
                profile_id=self.profile_id,
                profile_name=self.profile.name,
            )

    def _detect_format_category(self, metadata: AudioMetadata) -> str:
        """Detect format category from codec and extension."""
        codec = metadata.codec.lower() if metadata.codec else ""
        ext = metadata.filepath.suffix.lower() if metadata.filepath else ""
        
        # Mappatura codec/formato
        if "mp3" in codec or ext == ".mp3":
            return "MP3"
        elif "aac" in codec or ext in (".m4a", ".aac"):
            return "AAC"
        elif "pcm" in codec or codec in ("wav", "pcm_s16le", "pcm_s24le") or ext in (".wav", ".wave"):
            return "WAV"
        elif "aiff" in codec or codec == "pcm_s16be" or ext in (".aiff", ".aif"):
            return "AIFF"
        elif "flac" in codec or ext == ".flac":
            return "FLAC"
        elif "vorbis" in codec or ext == ".ogg":
            return "OGG"
        elif "opus" in codec or ext == ".opus":
            return "OPUS"
        elif "wma" in codec or ext == ".wma":
            return "WMA"
        elif "alac" in codec:
            return "ALAC"
        else:
            return "UNKNOWN"

    def _check_supported_format(
        self,
        filepath: Path,
        metadata: AudioMetadata,
        format_category: str,
        sample_rate: Optional[int],
        bit_depth: Optional[int],
        is_float: bool,
    ) -> CompatibilityResult:
        """Check compatibility for profile-supported format."""
        fmt = self.profile.formats[format_category]
        
        issues = []
        
        # Verifica sample rate
        if sample_rate and fmt.sample_rates and sample_rate not in fmt.sample_rates:
            if sample_rate > self.profile.max_sample_rate:
                issues.append(f"{sample_rate/1000:.1f}kHz → max {self.profile.max_sample_rate/1000:.1f}kHz")
            else:
                issues.append(f"{sample_rate/1000:.1f}kHz not supported")
        
        # Verifica bit depth (solo per formati PCM)
        if bit_depth and fmt.bit_depths:
            if bit_depth not in fmt.bit_depths:
                if is_float:
                    issues.append("32-bit float not supported")
                elif bit_depth > self.profile.max_bit_depth:
                    issues.append(f"{bit_depth}-bit too high")
                else:
                    issues.append(f"{bit_depth}-bit not supported")
        
        if issues:
            # Ha problemi ma è convertibile lossless
            plan = self._create_conversion_plan(metadata, lossless_source=True)
            return CompatibilityResult(
                filepath=filepath,
                metadata=metadata,
                status=CompatibilityStatus.CONVERTIBLE_LOSSLESS,
                message="; ".join(issues),
                profile_id=self.profile_id,
                profile_name=self.profile.name,
                conversion_plan=plan,
            )
        
        # Tutto OK
        return CompatibilityResult(
            filepath=filepath,
            metadata=metadata,
            status=CompatibilityStatus.COMPATIBLE,
            message=f"Ready for {self.profile.name}",
            profile_id=self.profile_id,
            profile_name=self.profile.name,
        )

    def _check_unsupported_format(
        self,
        filepath: Path,
        metadata: AudioMetadata,
        format_category: str,
        is_lossy: bool,
    ) -> CompatibilityResult:
        """Check for natively unsupported format (requires conversion)."""
        plan = self._create_conversion_plan(metadata, lossless_source=not is_lossy)
        
        if is_lossy:
            status = CompatibilityStatus.CONVERTIBLE_LOSSY
            message = f"{format_category} convertible (lossy source)"
        else:
            status = CompatibilityStatus.CONVERTIBLE_LOSSLESS
            message = f"{format_category} → {plan.output_format} lossless"
        
        return CompatibilityResult(
            filepath=filepath,
            metadata=metadata,
            status=status,
            message=message,
            profile_id=self.profile_id,
            profile_name=self.profile.name,
            conversion_plan=plan,
        )

    def _create_conversion_plan(
        self, metadata: AudioMetadata, lossless_source: bool
    ) -> ConversionPlan:
        """Create optimal conversion plan for current profile."""
        sample_rate = metadata.sample_rate or 44100
        bit_depth = metadata.bit_depth or 16
        
        # Determina i target in base al profilo
        max_sr = self.profile.max_sample_rate
        max_bd = self.profile.max_bit_depth
        
        if lossless_source:
            # Per sorgenti lossless, mantieni la massima qualità possibile del profilo
            target_sample_rate = min(sample_rate, max_sr)
            target_bit_depth = min(bit_depth, max_bd) if bit_depth else max_bd
            
            # Arrotonda ai valori supportati
            if target_sample_rate >= 96000 and 96000 in [44100, 48000, 88200, 96000]:
                target_sample_rate = 96000
            elif target_sample_rate >= 88200:
                target_sample_rate = 88200 if max_sr >= 88200 else 48000
            elif target_sample_rate >= 48000:
                target_sample_rate = 48000
            else:
                target_sample_rate = 44100
                
            if target_bit_depth >= 24:
                target_bit_depth = 24
            else:
                target_bit_depth = 16
                
            reason = f"Lossless: {target_bit_depth}bit/{target_sample_rate/1000:.1f}kHz"
        else:
            # Per sorgenti lossy, 16/44.1 è sufficiente
            target_sample_rate = 44100
            target_bit_depth = 16
            reason = "From lossy: 16bit/44.1kHz"
        
        # Scegli formato output (preferisci WAV come standard)
        if metadata.codec and metadata.codec.lower() in ("aiff", "pcm_s16be", "pcm_s24be"):
            output_format = "AIFF"
        else:
            output_format = "WAV"
        
        return ConversionPlan(
            output_format=output_format,
            target_sample_rate=target_sample_rate,
            target_bit_depth=target_bit_depth,
            reason=reason,
        )
