"""Test per AudioAnalyzer."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from cdj_check.analyzer import AudioAnalyzer, AudioMetadata


class TestAudioAnalyzer:
    """Test suite per AudioAnalyzer."""

    def test_init_checks_ffprobe(self):
        """Test che l'inizializzazione verifichi ffprobe."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            analyzer = AudioAnalyzer()
            mock_run.assert_called_once()
    
    def test_init_raises_on_missing_ffprobe(self):
        """Test che mancante ffprobe sollevi errore."""
        with patch("subprocess.run", side_effect=FileNotFoundError()):
            with pytest.raises(RuntimeError, match="ffprobe non trovato"):
                AudioAnalyzer()

    def test_parse_metadata_mp3(self):
        """Test parsing metadati MP3."""
        analyzer = MagicMock(spec=AudioAnalyzer)
        analyzer._parse_metadata = AudioAnalyzer._parse_metadata.__get__(analyzer)
        
        mock_data = {
            "format": {
                "format_name": "mp3",
                "duration": "300.5",
                "bit_rate": "320000",
            },
            "streams": [{
                "codec_type": "audio",
                "codec_name": "mp3",
                "sample_rate": "44100",
                "channels": 2,
            }]
        }
        
        filepath = Path("/test/track.mp3")
        metadata = analyzer._parse_metadata(filepath, mock_data)
        
        assert metadata.filename == "track.mp3"
        assert metadata.codec == "MP3"
        assert metadata.sample_rate == 44100
        assert metadata.is_lossy is True
        assert metadata.duration == 300.5
        assert metadata.bitrate == 320000

    def test_parse_metadata_wav_24bit(self):
        """Test parsing metadati WAV 24-bit."""
        analyzer = MagicMock(spec=AudioAnalyzer)
        analyzer._parse_metadata = AudioAnalyzer._parse_metadata.__get__(analyzer)
        
        mock_data = {
            "format": {
                "format_name": "wav",
                "duration": "180.0",
            },
            "streams": [{
                "codec_type": "audio",
                "codec_name": "pcm_s24le",
                "sample_rate": "48000",
                "channels": 2,
                "bits_per_sample": 24,
            }]
        }
        
        filepath = Path("/test/track.wav")
        metadata = analyzer._parse_metadata(filepath, mock_data)
        
        assert metadata.codec == "PCM_S24LE"
        assert metadata.sample_rate == 48000
        assert metadata.bit_depth == 24
        assert metadata.is_lossy is False
        assert metadata.is_float is False

    def test_parse_metadata_float32(self):
        """Test parsing metadati WAV 32-bit float."""
        analyzer = MagicMock(spec=AudioAnalyzer)
        analyzer._parse_metadata = AudioAnalyzer._parse_metadata.__get__(analyzer)
        
        mock_data = {
            "format": {
                "format_name": "wav",
            },
            "streams": [{
                "codec_type": "audio",
                "codec_name": "pcm_f32le",
                "sample_rate": "96000",
                "sample_fmt": "flt",
                "channels": 2,
            }]
        }
        
        filepath = Path("/test/float.wav")
        metadata = analyzer._parse_metadata(filepath, mock_data)
        
        assert metadata.sample_rate == 96000
        assert metadata.is_float is True
        assert metadata.bit_depth == 32


class TestAudioMetadata:
    """Test per AudioMetadata."""

    def test_sample_rate_khz(self):
        """Test conversione sample rate in kHz."""
        metadata = AudioMetadata(
            filepath=Path("/test.wav"),
            filename="test.wav",
            format_name="WAV",
            codec="PCM",
            sample_rate=48000,
            bit_depth=24,
            channels=2,
            bitrate=None,
            duration=120.0,
            is_lossy=False,
            is_float=False,
        )
        assert metadata.sample_rate_khz == 48.0

    def test_duration_formatted(self):
        """Test formattazione durata."""
        metadata = AudioMetadata(
            filepath=Path("/test.wav"),
            filename="test.wav",
            format_name="WAV",
            codec="PCM",
            sample_rate=44100,
            bit_depth=16,
            channels=2,
            bitrate=None,
            duration=125.5,
            is_lossy=False,
            is_float=False,
        )
        assert metadata.duration_formatted == "02:05"

    def test_duration_formatted_none(self):
        """Test formattazione durata None."""
        metadata = AudioMetadata(
            filepath=Path("/test.wav"),
            filename="test.wav",
            format_name="WAV",
            codec="PCM",
            sample_rate=44100,
            bit_depth=16,
            channels=2,
            bitrate=None,
            duration=None,
            is_lossy=False,
            is_float=False,
        )
        assert metadata.duration_formatted == "--:--"
