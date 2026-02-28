"""AudioConverter: Converts audio files using FFmpeg with multi-profile support."""

import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from dr_cdj.analyzer import AudioMetadata
from dr_cdj.compatibility import CompatibilityResult, ConversionPlan
from dr_cdj.config import FFMPEG_TIMEOUT, CDJ_PROFILES
from dr_cdj.utils import get_ffmpeg_path


@dataclass
class ConversionResult:
    """Conversion result."""

    source_path: Path
    output_path: Optional[Path]
    success: bool
    message: str
    duration: Optional[float] = None


class AudioConverter:
    """Converts audio files using FFmpeg."""

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

    def _build_output_path(
        self, source_path: Path, plan: ConversionPlan, output_dir: Optional[Path] = None
    ) -> Path:
        """Build output path.
        
        Args:
            source_path: Source file path.
            plan: Conversion plan.
            output_dir: Output directory (default: same as source/CDJ_Ready).
            
        Returns:
            Path for converted file.
        """
        if output_dir is None:
            output_dir = source_path.parent / "CDJ_Ready"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extension based on output format
        if plan.output_format == "AIFF":
            ext = ".aiff"
        else:
            ext = ".wav"
        
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
        plan: ConversionPlan,
    ) -> list[str]:
        """Build ffmpeg arguments.
        
        Args:
            source_path: Source file path.
            output_path: Destination path.
            plan: Conversion plan.
            
        Returns:
            List of arguments for subprocess.
        """
        cmd = [
            self.ffmpeg_path,
            "-y",  # Overwrite existing files
            "-i", str(source_path),  # Input
            "-vn",  # No video
        ]
        
        # Audio codec
        if plan.output_format == "AIFF":
            cmd.extend(["-c:a", "pcm_s16be" if plan.target_bit_depth == 16 else "pcm_s24be"])
        else:  # WAV
            cmd.extend(["-c:a", "pcm_s16le" if plan.target_bit_depth == 16 else "pcm_s24le"])
        
        # Sample rate
        cmd.extend(["-ar", str(plan.target_sample_rate)])
        
        # Bit depth (via sample format)
        if plan.target_bit_depth == 16:
            cmd.extend(["-sample_fmt", "s16"])
        else:
            cmd.extend(["-sample_fmt", "s32"])  # ffmpeg usa s32 per 24-bit packed
        
        # Metadata: copy if possible
        cmd.extend(["-map_metadata", "0"])
        
        # Output
        cmd.append(str(output_path))
        
        return cmd

    def convert(
        self,
        result: CompatibilityResult,
        output_dir: Optional[Path] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> ConversionResult:
        """Convert a single file.
        
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
        
        # If already compatible, don't convert
        if result.is_compatible:
            return ConversionResult(
                source_path=source_path,
                output_path=source_path,
                success=True,
                message="File already compatible, no conversion needed",
            )
        
        try:
            output_path = self._build_output_path(source_path, plan, output_dir)
            cmd = self._build_ffmpeg_args(source_path, output_path, plan)
            
            # Esegui ffmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            
            # Read stderr for progress (optional)
            stderr_output = []
            if process.stderr:
                for line in process.stderr:
                    stderr_output.append(line)
                    # Progress parsing could be done here
                    if progress_callback:
                        pass  # Complex parsing, skip for now
            
            returncode = process.wait(timeout=FFMPEG_TIMEOUT)
            
            if returncode != 0:
                error_msg = "".join(stderr_output[-10:])  # Last 10 lines
                return ConversionResult(
                    source_path=source_path,
                    output_path=None,
                    success=False,
                    message=f"FFmpeg error (code {returncode}): {error_msg[:100]}",
                )
            
            return ConversionResult(
                source_path=source_path,
                output_path=output_path,
                success=True,
                message=f"Converted to {plan.output_format} {plan.target_bit_depth}bit/{plan.target_sample_rate/1000:.1f}kHz",
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            return ConversionResult(
                source_path=source_path,
                output_path=None,
                success=False,
                message="Conversion timeout",
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
