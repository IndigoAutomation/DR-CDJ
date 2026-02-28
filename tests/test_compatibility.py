"""Test per CompatibilityEngine con supporto multi-profilo."""

import pytest
from pathlib import Path

from dr_cdj.analyzer import AudioMetadata
from dr_cdj.compatibility import (
    CompatibilityEngine,
    CompatibilityResult,
    CompatibilityStatus,
)


class TestCompatibilityEngine:
    """Test suite per CompatibilityEngine."""

    @pytest.fixture
    def engine(self):
        """Fixture per il motore di compatibilità."""
        return CompatibilityEngine()

    def test_compatible_mp3_320(self, engine):
        """Test MP3 320kbps compatibile."""
        metadata = AudioMetadata(
            filepath=Path("/test/track.mp3"),
            filename="track.mp3",
            format_name="MP3",
            codec="MP3",
            sample_rate=44100,
            bit_depth=None,
            channels=2,
            bitrate=320000,
            duration=300.0,
            is_lossy=True,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        assert result.status == CompatibilityStatus.COMPATIBLE
        assert result.is_compatible is True
        assert result.needs_conversion is False

    def test_compatible_wav_24_48(self, engine):
        """Test WAV 24-bit/48kHz compatibile."""
        metadata = AudioMetadata(
            filepath=Path("/test/track.wav"),
            filename="track.wav",
            format_name="WAV",
            codec="PCM_S24LE",
            sample_rate=48000,
            bit_depth=24,
            channels=2,
            bitrate=None,
            duration=300.0,
            is_lossy=False,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        assert result.status == CompatibilityStatus.COMPATIBLE
        assert "Pronto" in result.message or "Compatibile" in result.message

    def test_convertible_lossless_wav_96khz(self, engine):
        """Test WAV 96kHz convertibile lossless."""
        metadata = AudioMetadata(
            filepath=Path("/test/hires.wav"),
            filename="hires.wav",
            format_name="WAV",
            codec="PCM_S24LE",
            sample_rate=96000,
            bit_depth=24,
            channels=2,
            bitrate=None,
            duration=300.0,
            is_lossy=False,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        assert result.status == CompatibilityStatus.CONVERTIBLE_LOSSLESS
        assert result.needs_conversion is True
        assert result.conversion_plan is not None
        assert result.conversion_plan.target_sample_rate == 48000

    def test_convertible_lossless_wav_float32(self, engine):
        """Test WAV 32-bit float convertibile lossless."""
        metadata = AudioMetadata(
            filepath=Path("/test/float.wav"),
            filename="float.wav",
            format_name="WAV",
            codec="PCM_F32LE",
            sample_rate=48000,
            bit_depth=32,
            channels=2,
            bitrate=None,
            duration=300.0,
            is_lossy=False,
            is_float=True,
        )
        
        result = engine.check(metadata)
        
        assert result.status == CompatibilityStatus.CONVERTIBLE_LOSSLESS
        assert "float" in result.message.lower() or "formato" in result.message.lower()

    def test_flac_convertible_with_cdj_2000_nxs(self, engine):
        """Test FLAC convertibile con CDJ-2000 Nexus (1ª gen non supporta FLAC nativamente ma convertibile)."""
        metadata = AudioMetadata(
            filepath=Path("/test/track.flac"),
            filename="track.flac",
            format_name="FLAC",
            codec="FLAC",
            sample_rate=48000,
            bit_depth=24,
            channels=2,
            bitrate=None,
            duration=300.0,
            is_lossy=False,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        # CDJ-2000 Nexus (default) non supporta FLAC nativamente ma è convertibile lossless
        assert result.status == CompatibilityStatus.CONVERTIBLE_LOSSLESS
        assert result.needs_conversion is True
        assert result.conversion_plan is not None
        assert result.conversion_plan.output_format == "WAV"

    def test_flac_compatible_with_cdj_3000(self):
        """Test FLAC compatibile con CDJ-3000."""
        engine = CompatibilityEngine(profile_id="cdj_3000")
        metadata = AudioMetadata(
            filepath=Path("/test/track.flac"),
            filename="track.flac",
            format_name="FLAC",
            codec="FLAC",
            sample_rate=48000,
            bit_depth=24,
            channels=2,
            bitrate=None,
            duration=300.0,
            is_lossy=False,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        # CDJ-3000 supporta FLAC nativamente
        assert result.status == CompatibilityStatus.COMPATIBLE
        assert result.is_compatible is True

    def test_flac_convertible_with_nxs2(self):
        """Test FLAC compatibile con CDJ-2000 NXS2 (supporta FLAC fino a 96kHz)."""
        engine = CompatibilityEngine(profile_id="cdj_2000_nxs2")
        metadata = AudioMetadata(
            filepath=Path("/test/track.flac"),
            filename="track.flac",
            format_name="FLAC",
            codec="FLAC",
            sample_rate=96000,
            bit_depth=24,
            channels=2,
            bitrate=None,
            duration=300.0,
            is_lossy=False,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        # CDJ-2000 NXS2 supporta FLAC fino a 96kHz, quindi è compatibile
        assert result.status == CompatibilityStatus.COMPATIBLE
        assert result.is_compatible is True
        
    def test_flac_convertible_with_nxs2_high_sample_rate(self):
        """Test FLAC convertibile con CDJ-2000 NXS2 a sample rate troppo alto."""
        engine = CompatibilityEngine(profile_id="cdj_2000_nxs2")
        metadata = AudioMetadata(
            filepath=Path("/test/track.flac"),
            filename="track.flac",
            format_name="FLAC",
            codec="FLAC",
            sample_rate=192000,  # 192kHz non supportato
            bit_depth=24,
            channels=2,
            bitrate=None,
            duration=300.0,
            is_lossy=False,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        # CDJ-2000 NXS2 non supporta 192kHz, quindi è convertibile
        assert result.status == CompatibilityStatus.CONVERTIBLE_LOSSLESS
        assert result.conversion_plan is not None
        assert result.conversion_plan.target_sample_rate == 96000  # Downsample a max supportato

    def test_convertible_lossy_ogg(self, engine):
        """Test OGG convertibile con perdita."""
        metadata = AudioMetadata(
            filepath=Path("/test/track.ogg"),
            filename="track.ogg",
            format_name="OGG",
            codec="VORBIS",
            sample_rate=44100,
            bit_depth=None,
            channels=2,
            bitrate=256000,
            duration=300.0,
            is_lossy=True,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        assert result.status == CompatibilityStatus.CONVERTIBLE_LOSSY
        assert result.conversion_plan is not None
        assert result.conversion_plan.target_sample_rate == 44100
        assert result.conversion_plan.target_bit_depth == 16

    def test_convertible_lossy_opus(self, engine):
        """Test OPUS convertibile con perdita."""
        metadata = AudioMetadata(
            filepath=Path("/test/track.opus"),
            filename="track.opus",
            format_name="OPUS",
            codec="OPUS",
            sample_rate=48000,
            bit_depth=None,
            channels=2,
            bitrate=128000,
            duration=300.0,
            is_lossy=True,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        assert result.status == CompatibilityStatus.CONVERTIBLE_LOSSY
        assert "lossy" in result.message.lower() or "convertibile" in result.message.lower()

    def test_conversion_plan_lossless_source(self, engine):
        """Test piano conversione da sorgente lossless."""
        metadata = AudioMetadata(
            filepath=Path("/test/hires.wav"),
            filename="hires.wav",
            format_name="WAV",
            codec="PCM_S24LE",
            sample_rate=96000,
            bit_depth=24,
            channels=2,
            bitrate=None,
            duration=300.0,
            is_lossy=False,
            is_float=False,
        )
        
        result = engine.check(metadata)
        plan = result.conversion_plan
        
        assert plan is not None
        assert plan.target_sample_rate == 48000  # Downsample a max supportato
        assert plan.target_bit_depth == 24  # Mantiene 24-bit

    def test_conversion_plan_lossy_source(self, engine):
        """Test piano conversione da sorgente lossy."""
        metadata = AudioMetadata(
            filepath=Path("/test/track.ogg"),
            filename="track.ogg",
            format_name="OGG",
            codec="VORBIS",
            sample_rate=44100,
            bit_depth=None,
            channels=2,
            bitrate=256000,
            duration=300.0,
            is_lossy=True,
            is_float=False,
        )
        
        result = engine.check(metadata)
        plan = result.conversion_plan
        
        assert plan is not None
        assert plan.target_sample_rate == 44100  # Non upsamplare
        assert plan.target_bit_depth == 16  # 16-bit sufficiente

    def test_status_icons(self, engine):
        """Test icone di stato."""
        metadata = AudioMetadata(
            filepath=Path("/test/track.mp3"),
            filename="track.mp3",
            format_name="MP3",
            codec="MP3",
            sample_rate=44100,
            bit_depth=None,
            channels=2,
            bitrate=320000,
            duration=300.0,
            is_lossy=True,
            is_float=False,
        )
        
        result = engine.check(metadata)
        
        assert result.status_icon in ["✓", "✅"]
        assert result.status_color is not None

    def test_set_profile(self):
        """Test cambio profilo."""
        engine = CompatibilityEngine()
        
        # Default è CDJ-2000 Nexus
        assert engine.profile_id == "cdj_2000_nxs"
        
        # Cambia a CDJ-3000
        assert engine.set_profile("cdj_3000") is True
        assert engine.profile_id == "cdj_3000"
        
        # Profilo inesistente
        assert engine.set_profile("non_existent") is False
        assert engine.profile_id == "cdj_3000"  # Rimane invariato

    def test_get_available_profiles(self):
        """Test elenco profili disponibili."""
        engine = CompatibilityEngine()
        profiles = engine.get_available_profiles()
        
        assert "cdj_2000_nxs" in profiles
        assert "cdj_3000" in profiles
        assert "name" in profiles["cdj_3000"]
        assert "year" in profiles["cdj_3000"]


class TestCompatibilityResult:
    """Test per CompatibilityResult."""

    def test_is_compatible_property(self):
        """Test proprietà is_compatible."""
        metadata = AudioMetadata(
            filepath=Path("/test.wav"),
            filename="test.wav",
            format_name="WAV",
            codec="PCM",
            sample_rate=44100,
            bit_depth=16,
            channels=2,
            bitrate=None,
            duration=120.0,
            is_lossy=False,
            is_float=False,
        )
        
        compatible = CompatibilityResult(
            filepath=Path("/test.wav"),
            metadata=metadata,
            status=CompatibilityStatus.COMPATIBLE,
            message="OK",
            profile_id="cdj_2000_nxs",
            profile_name="CDJ-2000 Nexus",
        )
        
        assert compatible.is_compatible is True
        assert compatible.needs_conversion is False

    def test_result_includes_profile_info(self):
        """Test che il risultato includa info del profilo."""
        metadata = AudioMetadata(
            filepath=Path("/test.wav"),
            filename="test.wav",
            format_name="WAV",
            codec="PCM",
            sample_rate=44100,
            bit_depth=16,
            channels=2,
            bitrate=None,
            duration=120.0,
            is_lossy=False,
            is_float=False,
        )
        
        result = CompatibilityResult(
            filepath=Path("/test.wav"),
            metadata=metadata,
            status=CompatibilityStatus.COMPATIBLE,
            message="OK",
            profile_id="cdj_3000",
            profile_name="CDJ-3000",
        )
        
        assert result.profile_id == "cdj_3000"
        assert result.profile_name == "CDJ-3000"
