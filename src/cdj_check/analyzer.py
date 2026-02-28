"""AudioAnalyzer: estrae metadati dai file audio usando ffprobe."""

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from cdj_check.config import FFPROBE_TIMEOUT
from cdj_check.utils import get_ffprobe_path


@dataclass
class AudioMetadata:
    """Metadati estratti da un file audio."""

    filepath: Path
    filename: str
    format_name: str
    codec: str
    sample_rate: Optional[int]
    bit_depth: Optional[int]
    channels: int
    bitrate: Optional[int]
    duration: Optional[float]
    is_lossy: bool
    is_float: bool

    @property
    def sample_rate_khz(self) -> Optional[float]:
        """Restituisce il sample rate in kHz."""
        if self.sample_rate:
            return self.sample_rate / 1000
        return None

    @property
    def sample_rate_formatted(self) -> str:
        """Restituisce il sample rate formattato."""
        if self.sample_rate:
            return f"{self.sample_rate / 1000:.1f} kHz"
        return "-"

    @property
    def bit_depth_formatted(self) -> str:
        """Restituisce il bit depth formattato."""
        if self.bit_depth:
            return f"{self.bit_depth}-bit"
        if self.is_float:
            return "32f-bit"
        return "-"

    @property
    def duration_formatted(self) -> str:
        """Restituisce la durata formattata come MM:SS."""
        if self.duration is None:
            return "--:--"
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes:02d}:{seconds:02d}"

    @property
    def codec_formatted(self) -> str:
        """Restituisce il codec formattato per la UI."""
        codec_map = {
            "MP3": "MP3",
            "AAC": "AAC",
            "PCM_S16LE": "PCM 16",
            "PCM_S24LE": "PCM 24",
            "PCM_S16BE": "PCM 16",
            "PCM_S24BE": "PCM 24",
            "PCM_F32LE": "PCM 32f",
            "PCM_F64LE": "PCM 64f",
            "FLAC": "FLAC",
            "VORBIS": "Vorbis",
            "OPUS": "Opus",
            "WMAV2": "WMA",
            "WMA": "WMA",
            "ALAC": "ALAC",
        }
        return codec_map.get(self.codec.upper(), self.codec.upper())


class AudioAnalyzer:
    """Analizza file audio usando ffprobe."""

    def __init__(self, ffprobe_path: str | None = None):
        """Inizializza l'analyzer.
        
        Args:
            ffprobe_path: Path all'eseguibile ffprobe. Se None, usa get_ffprobe_path().
        """
        self.ffprobe_path = ffprobe_path or get_ffprobe_path()
        self._check_ffprobe()

    def _check_ffprobe(self) -> None:
        """Verifica che ffprobe sia disponibile."""
        try:
            result = subprocess.run(
                [self.ffprobe_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                raise RuntimeError("ffprobe non funzionante")
        except FileNotFoundError:
            raise RuntimeError(
                f"ffprobe non trovato: {self.ffprobe_path}\n"
                "Installa FFmpeg: https://ffmpeg.org/download.html"
            )

    def analyze(self, filepath: Path) -> AudioMetadata:
        """Analizza un file audio e restituisce i metadati.
        
        Args:
            filepath: Path al file audio.
            
        Returns:
            AudioMetadata con tutti i metadati estratti.
            
        Raises:
            RuntimeError: Se l'analisi fallisce.
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File non trovato: {filepath}")
        
        cmd = [
            self.ffprobe_path,
            "-v", "error",
            "-show_format",
            "-show_streams",
            "-of", "json",
            str(filepath),
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=FFPROBE_TIMEOUT,
            )
            
            if result.returncode != 0:
                stderr = result.stderr.strip() if result.stderr else "Errore sconosciuto"
                raise RuntimeError(f"ffprobe: {stderr[:100]}")
            
            if not result.stdout.strip():
                raise RuntimeError("Nessun output da ffprobe")
            
            data = json.loads(result.stdout)
            return self._parse_metadata(filepath, data)
            
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Timeout analizzando {filepath.name}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Dati non validi da ffprobe: {str(e)[:50]}")
        except Exception as e:
            if "Errore" in str(e):
                raise
            raise RuntimeError(f"Errore analisi: {str(e)[:50]}")

    def _parse_metadata(self, filepath: Path, data: dict) -> AudioMetadata:
        """Estrae i metadati dal JSON di ffprobe.
        
        Args:
            filepath: Path al file.
            data: Dati JSON da ffprobe.
            
        Returns:
            AudioMetadata estratto.
        """
        format_info = data.get("format", {}) if data else {}
        streams = data.get("streams", []) if data else []
        
        # Trova il primo stream audio
        audio_stream = None
        for stream in streams:
            if stream and stream.get("codec_type") == "audio":
                audio_stream = stream
                break
        
        if not audio_stream:
            raise RuntimeError("Nessuno stream audio trovato")
        
        # Estrai codec e formato
        codec = (audio_stream.get("codec_name", "unknown") or "unknown").upper()
        format_name = (format_info.get("format_name", "unknown") or "unknown").upper()
        
        # Sample rate
        sample_rate = None
        sample_rate_str = audio_stream.get("sample_rate")
        if sample_rate_str:
            try:
                sample_rate = int(sample_rate_str)
            except (ValueError, TypeError):
                sample_rate = None
        
        # Bit depth - con gestione robusta degli errori
        bit_depth = None
        try:
            # Prova bits_per_sample
            bps = audio_stream.get("bits_per_sample")
            if bps and bps != 0:
                bit_depth = int(bps)
            
            # Se non trovato, prova bits_per_raw_sample
            if bit_depth is None:
                bprs = audio_stream.get("bits_per_raw_sample")
                if bprs and bprs != 0:
                    bit_depth = int(bprs)
            
            # Per FLAC e altri formati lossless, estrai da sample_fmt
            if bit_depth is None:
                sample_fmt = audio_stream.get("sample_fmt", "") or ""
                sample_fmt = str(sample_fmt).lower()
                
                if "s16" in sample_fmt:
                    bit_depth = 16
                elif "s24" in sample_fmt:
                    bit_depth = 24
                elif "s32" in sample_fmt:
                    bit_depth = 24  # 24-bit packed in 32
                elif "s8" in sample_fmt:
                    bit_depth = 8
                elif "flt" in sample_fmt or "dbl" in sample_fmt:
                    bit_depth = 32  # Float
        except (ValueError, TypeError, AttributeError):
            bit_depth = None
        
        # Canali
        channels = 2
        try:
            ch = audio_stream.get("channels")
            if ch is not None:
                channels = int(ch)
        except (ValueError, TypeError):
            channels = 2
        
        # Bitrate
        bitrate = None
        try:
            br = audio_stream.get("bit_rate") or format_info.get("bit_rate")
            if br:
                bitrate = int(br)
        except (ValueError, TypeError):
            bitrate = None
        
        # Durata
        duration = None
        try:
            dur = format_info.get("duration") or audio_stream.get("duration")
            if dur:
                duration = float(dur)
        except (ValueError, TypeError):
            duration = None
        
        # Verifica se è float
        is_float = False
        try:
            sample_fmt = audio_stream.get("sample_fmt", "") or ""
            is_float = "flt" in str(sample_fmt).lower() or "dbl" in str(sample_fmt).lower()
        except (AttributeError, TypeError):
            pass
        
        # Verifica se è lossy (basato sul codec)
        lossy_codecs = {"MP3", "AAC", "VORBIS", "OPUS", "WMAV2", "WMA", "WMAPRO"}
        is_lossy = codec in lossy_codecs
        if not is_lossy:
            codec_lower = codec.lower()
            is_lossy = any(c in codec_lower for c in ["mp3", "aac", "vorbis", "opus", "wma"])
        
        return AudioMetadata(
            filepath=filepath,
            filename=filepath.name,
            format_name=format_name,
            codec=codec,
            sample_rate=sample_rate,
            bit_depth=bit_depth,
            channels=channels,
            bitrate=bitrate,
            duration=duration,
            is_lossy=is_lossy,
            is_float=is_float,
        )

    def analyze_batch(self, filepaths: list[Path]) -> list[tuple[Path, Optional[AudioMetadata], Optional[str]]]:
        """Analizza batch di file.
        
        Args:
            filepaths: Lista di path ai file.
            
        Returns:
            Lista di tuple (path, metadata, error_message).
        """
        results = []
        for filepath in filepaths:
            try:
                metadata = self.analyze(filepath)
                results.append((filepath, metadata, None))
            except Exception as e:
                results.append((filepath, None, str(e)))
        return results
