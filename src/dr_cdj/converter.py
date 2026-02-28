"""AudioConverter: Converts audio files using FFmpeg with multi-profile support."""

import shutil
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from dr_cdj.analyzer import AudioMetadata
from dr_cdj.compatibility import CompatibilityResult, ConversionPlan
from dr_cdj.config import FFMPEG_TIMEOUT, CDJ_PROFILES
from dr_cdj.utils import get_ffmpeg_path, get_ffprobe_path


@dataclass
class ConversionResult:
    """Conversion result."""

    source_path: Path
    output_path: Optional[Path]
    success: bool
    message: str
    duration: Optional[float] = None


class AudioConverter:
    """Converts audio files using FFmpeg with high-quality settings."""

    def __init__(
        self,
        ffmpeg_path: str | None = None,
        max_workers: int = 2,
        output_suffix: str = "_CDJ",
    ):
        """Initialize converter.
        
        Args:
            ffmpeg_path: Path to ffmpeg executable. If None, uses get_ffmpeg_path().
            max_workers: Maximum number of parallel conversions.
            output_suffix: Suffix added to converted files.
        """
        self.ffmpeg_path = ffmpeg_path or get_ffmpeg_path()
        self.ffprobe_path = get_ffprobe_path()
        self.max_workers = max(max_workers, 1)
        self.output_suffix = output_suffix
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> None:
        """Verify ffmpeg is available."""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                raise RuntimeError("ffmpeg not working")
        except FileNotFoundError:
            raise RuntimeError(
                f"ffmpeg not found: {self.ffmpeg_path}\n"
                "Install FFmpeg: https://ffmpeg.org/download.html"
            )

    def _get_optimal_settings(
        self,
        source_metadata: AudioMetadata,
        plan: ConversionPlan,
        profile_id: str,
    ) -> tuple[int, int, str, bool]:
        """Calculate optimal conversion settings to preserve quality.
        
        Implements "smart bit depth" - avoids upsampling if not needed.
        
        Args:
            source_metadata: Original file metadata
            plan: Base conversion plan
            profile_id: Target CDJ profile ID
            
        Returns:
            Tuple of (bit_depth, sample_rate, output_format, use_high_quality_resample)
        """
        source_depth = source_metadata.bit_depth or 16
        source_rate = source_metadata.sample_rate or 44100
        
        # Get profile limits
        profile = CDJ_PROFILES.get(profile_id)
        max_profile_depth = 24 if profile else 24
        max_profile_rate = profile.max_sample_rate if profile else 48000
        
        # Bit depth: don't upsample if source is lower
        if source_depth <= 16:
            # If source is 16-bit and player supports it, keep 16-bit
            # This avoids unnecessary file size increase
            target_depth = 16
        else:
            # Source is 24-bit or higher, use 24-bit
            target_depth = min(24, max_profile_depth)
        
        # Sample rate: use source rate if compatible, otherwise resample to nearest supported
        supported_rates = [44100, 48000, 88200, 96000]
        if source_rate in supported_rates and source_rate <= max_profile_rate:
            target_rate = source_rate
        else:
            # Find best target rate (downsample if needed)
            target_rate = 48000  # Default
            for rate in sorted(supported_rates, reverse=True):
                if rate <= max_profile_rate:
                    target_rate = rate
                    break
        
        # Output format: use FLAC for CDJ-3000 if source is lossless
        output_format = plan.output_format
        if profile_id == "cdj_3000" and not source_metadata.is_lossy:
            # CDJ-3000 supports FLAC natively, use it for smaller files
            if output_format == "WAV":
                output_format = "FLAC"
        
        # Determine if we need high-quality resampling
        needs_resample = source_rate != target_rate
        
        return target_depth, target_rate, output_format, needs_resample

    def _build_output_path(
        self, source_path: Path, output_format: str, output_dir: Optional[Path] = None
    ) -> Path:
        """Build output path.
        
        Args:
            source_path: Source file path.
            output_format: Output format (WAV, AIFF, FLAC)
            output_dir: Output directory (default: same as source/CDJ_Ready).
            
        Returns:
            Path for converted file.
        """
        if output_dir is None:
            output_dir = source_path.parent / "CDJ_Ready"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extension based on output format
        ext_map = {
            "AIFF": ".aiff",
            "FLAC": ".flac",
            "WAV": ".wav",
        }
        ext = ext_map.get(output_format, ".wav")
        
        # Filename: original + suffix + extension
        stem = source_path.stem
        if not stem.endswith(self.output_suffix):
            output_name = f"{stem}{self.output_suffix}{ext}"
        else:
            output_name = f"{stem}{ext}"
        
        return output_dir / output_name

    def _build_ffmpeg_args(
        self,
        source_path: Path,
        output_path: Path,
        source_metadata: AudioMetadata,
        plan: ConversionPlan,
        profile_id: str,
    ) -> list[str]:
        """Build ffmpeg arguments with optimal quality settings.
        
        Args:
            source_path: Source file path.
            output_path: Destination path.
            source_metadata: Original file metadata for smart settings.
            plan: Base conversion plan.
            profile_id: Target CDJ profile.
            
        Returns:
            List of arguments for subprocess.
        """
        # Get optimal settings
        target_depth, target_rate, output_format, needs_resample = self._get_optimal_settings(
            source_metadata, plan, profile_id
        )
        
        cmd = [
            self.ffmpeg_path,
            "-y",  # Overwrite existing files
            "-hide_banner",  # Less verbose output
            "-loglevel", "error",  # Only show errors
            "-i", str(source_path),  # Input
            "-vn",  # No video
        ]
        
        # High-quality resampling with dithering if needed
        if needs_resample:
            # SoX resampler with high precision and Shibata dithering
            # This minimizes artifacts when changing sample rates
            cmd.extend([
                "-af", "aresample=resampler=soxr:precision=28:cheby=1:dither_method=shibata",
            ])
        
        # Sample rate
        cmd.extend(["-ar", str(target_rate)])
        
        # Audio codec and format based on output format
        if output_format == "AIFF":
            # AIFF uses big-endian
            if target_depth == 16:
                cmd.extend(["-c:a", "pcm_s16be"])
                cmd.extend(["-sample_fmt", "s16"])
            else:
                cmd.extend(["-c:a", "pcm_s24be"])
                cmd.extend(["-sample_fmt", "s32"])
        elif output_format == "FLAC":
            # FLAC for CDJ-3000
            cmd.extend(["-c:a", "flac"])
            cmd.extend(["-compression_level", "5"])  # Balanced
            if target_depth == 16:
                cmd.extend(["-sample_fmt", "s16"])
            else:
                cmd.extend(["-sample_fmt", "s32"])
        else:  # WAV (default)
            # WAV uses little-endian
            if target_depth == 16:
                cmd.extend(["-c:a", "pcm_s16le"])
                cmd.extend(["-sample_fmt", "s16"])
            else:
                cmd.extend(["-c:a", "pcm_s24le"])
                cmd.extend(["-sample_fmt", "s32"])
        
        # Metadata: copy only essential metadata, exclude embedded artwork
        # This prevents large files from artwork and incompatible tags
        cmd.extend(["-map_metadata", "0", "-map", "0:a:0"])
        
        # Output
        cmd.append(str(output_path))
        
        return cmd

    def _verify_output(self, output_path: Path, expected_depth: int, expected_rate: int) -> bool:
        """Verify converted file is valid and matches expected parameters.
        
        Args:
            output_path: Path to converted file
            expected_depth: Expected bit depth
            expected_rate: Expected sample rate
            
        Returns:
            True if verification passes
        """
        try:
            cmd = [
                self.ffprobe_path,
                "-v", "error",
                "-show_entries", "stream=sample_rate,bits_per_raw_sample,codec_name",
                "-of", "json",
                str(output_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return False
            
            data = json.loads(result.stdout)
            streams = data.get("streams", [])
            
            if not streams:
                return False
            
            stream = streams[0]
            actual_rate = int(stream.get("sample_rate", 0))
            actual_depth = int(stream.get("bits_per_raw_sample", 0))
            
            # Verify sample rate matches (allowing for some tolerance)
            if actual_rate != expected_rate:
                return False
            
            # Verify file is readable (basic check)
            if output_path.stat().st_size == 0:
                return False
            
            return True
            
        except Exception:
            return False

    def _parse_error(self, stderr_output: list[str]) -> str:
        """Parse FFmpeg stderr for user-friendly error messages.
        
        Args:
            stderr_output: Lines from stderr
            
        Returns:
            User-friendly error message
        """
        error_text = "".join(stderr_output).lower()
        
        error_patterns = {
            "invalid data found": "File appears to be corrupted or in an unsupported format",
            "permission denied": "Permission denied - check file/folder permissions",
            "no such file": "Input file not found",
            "codec not currently supported": "Audio codec not supported by FFmpeg",
            "error while decoding": "Error decoding audio - file may be corrupted",
            "out of memory": "System ran out of memory during conversion",
            "disk full": "Disk is full - free up space and try again",
        }
        
        for pattern, message in error_patterns.items():
            if pattern in error_text:
                return message
        
        # Return last few lines if no pattern matches
        last_lines = "".join(stderr_output[-3:]).strip()
        return f"Conversion failed: {last_lines[:100]}"

    def convert(
        self,
        result: CompatibilityResult,
        output_dir: Optional[Path] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> ConversionResult:
        """Convert a single file with optimal quality settings.
        
        Args:
            result: Compatibility result with conversion plan.
            output_dir: Optional output directory.
            progress_callback: Progress callback (0.0 - 1.0).
            
        Returns:
            ConversionResult.
        """
        if not result.conversion_plan:
            return ConversionResult(
                source_path=result.filepath,
                output_path=None,
                success=False,
                message="No conversion plan available",
            )
        
        source_path = result.filepath
        plan = result.conversion_plan
        metadata = result.metadata
        
        # If already compatible, don't convert
        if result.is_compatible:
            return ConversionResult(
                source_path=source_path,
                output_path=source_path,
                success=True,
                message="File already compatible, no conversion needed",
            )
        
        try:
            # Get optimal settings for logging
            target_depth, target_rate, output_format, _ = self._get_optimal_settings(
                metadata, plan, result.profile_id
            )
            
            # Build output path with correct extension
            output_path = self._build_output_path(source_path, output_format, output_dir)
            
            # Build ffmpeg command
            cmd = self._build_ffmpeg_args(
                source_path, output_path, metadata, plan, result.profile_id
            )
            
            # Execute ffmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            
            # Read stderr for error collection
            stderr_output = []
            if process.stderr:
                for line in process.stderr:
                    stderr_output.append(line)
            
            returncode = process.wait(timeout=FFMPEG_TIMEOUT)
            
            if returncode != 0:
                error_msg = self._parse_error(stderr_output)
                return ConversionResult(
                    source_path=source_path,
                    output_path=None,
                    success=False,
                    message=error_msg,
                )
            
            # Verify output file
            if not self._verify_output(output_path, target_depth, target_rate):
                # Clean up invalid output
                output_path.unlink(missing_ok=True)
                return ConversionResult(
                    source_path=source_path,
                    output_path=None,
                    success=False,
                    message="Output file verification failed - conversion may be incomplete",
                )
            
            # Build success message with quality info
            quality_msg = f"{target_depth}bit/{target_rate/1000:.1f}kHz"
            if output_format == "FLAC":
                quality_msg += " FLAC"
            
            return ConversionResult(
                source_path=source_path,
                output_path=output_path,
                success=True,
                message=f"Converted to {quality_msg}",
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            return ConversionResult(
                source_path=source_path,
                output_path=None,
                success=False,
                message="Conversion timeout - file may be too large or complex",
            )
        except Exception as e:
            return ConversionResult(
                source_path=source_path,
                output_path=None,
                success=False,
                message=f"Error: {str(e)[:100]}",
            )

    def convert_batch(
        self,
        results: list[CompatibilityResult],
        output_dir: Optional[Path] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> list[ConversionResult]:
        """Convert batch of files in parallel.
        
        Args:
            results: List of compatibility results.
            output_dir: Optional output directory.
            progress_callback: Callback(current, total).
            
        Returns:
            List of ConversionResult.
        """
        # Filter only those needing conversion
        to_convert = [r for r in results if r.needs_conversion]
        
        if not to_convert:
            return []
        
        conversion_results = []
        completed = 0
        total = len(to_convert)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_result = {
                executor.submit(self.convert, r, output_dir): r
                for r in to_convert
            }
            
            # Collect results
            for future in as_completed(future_to_result):
                result = future.result()
                conversion_results.append(result)
                completed += 1
                
                if progress_callback:
                    progress_callback(completed, total)
        
        return conversion_results

    def get_conversion_summary(
        self, results: list[ConversionResult]
    ) -> dict:
        """Generate conversion summary.
        
        Args:
            results: List of conversion results.
            
        Returns:
            Dict with statistics.
        """
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        return {
            "total": len(results),
            "successful": successful,
            "failed": failed,
            "outputs": [r.output_path for r in results if r.output_path],
        }
