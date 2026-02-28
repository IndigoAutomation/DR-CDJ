"""AudioConverter: converte file audio usando FFmpeg con supporto multi-profilo."""

import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from cdj_check.analyzer import AudioMetadata
from cdj_check.compatibility import CompatibilityResult, ConversionPlan
from cdj_check.config import FFMPEG_TIMEOUT, CDJ_PROFILES
from cdj_check.utils import get_ffmpeg_path


@dataclass
class ConversionResult:
    """Risultato di una conversione."""

    source_path: Path
    output_path: Optional[Path]
    success: bool
    message: str
    duration: Optional[float] = None


class AudioConverter:
    """Converte file audio usando FFmpeg."""

    def __init__(
        self,
        ffmpeg_path: str | None = None,
        max_workers: int = 2,
        output_suffix: str = "_CDJ",
    ):
        """Inizializza il converter.
        
        Args:
            ffmpeg_path: Path all'eseguibile ffmpeg. Se None, usa get_ffmpeg_path().
            max_workers: Numero massimo di conversioni parallele.
            output_suffix: Suffix aggiunto ai file convertiti.
        """
        self.ffmpeg_path = ffmpeg_path or get_ffmpeg_path()
        self.max_workers = max(max_workers, 1)
        self.output_suffix = output_suffix
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> None:
        """Verifica che ffmpeg sia disponibile."""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                raise RuntimeError("ffmpeg non funzionante")
        except FileNotFoundError:
            raise RuntimeError(
                f"ffmpeg non trovato: {self.ffmpeg_path}\n"
                "Installa FFmpeg: https://ffmpeg.org/download.html"
            )

    def _build_output_path(
        self, source_path: Path, plan: ConversionPlan, output_dir: Optional[Path] = None
    ) -> Path:
        """Costruisce il path di output.
        
        Args:
            source_path: Path del file sorgente.
            plan: Piano di conversione.
            output_dir: Directory di output (default: stessa del sorgente/CDJ_Ready).
            
        Returns:
            Path per il file convertito.
        """
        if output_dir is None:
            output_dir = source_path.parent / "CDJ_Ready"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Estensione basata sul formato output
        if plan.output_format == "AIFF":
            ext = ".aiff"
        else:
            ext = ".wav"
        
        # Nome file: originale + suffix + estensione
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
        """Costruisce gli argomenti per ffmpeg.
        
        Args:
            source_path: Path del file sorgente.
            output_path: Path di destinazione.
            plan: Piano di conversione.
            
        Returns:
            Lista di argomenti per subprocess.
        """
        cmd = [
            self.ffmpeg_path,
            "-y",  # Sovrascrivi file esistenti
            "-i", str(source_path),  # Input
            "-vn",  # No video
        ]
        
        # Codec audio
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
        
        # Metadati: copia se possibile
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
        """Converte un singolo file.
        
        Args:
            result: Risultato compatibilità con piano di conversione.
            output_dir: Directory di output opzionale.
            progress_callback: Callback per progresso (0.0 - 1.0).
            
        Returns:
            ConversionResult.
        """
        if not result.conversion_plan:
            return ConversionResult(
                source_path=result.filepath,
                output_path=None,
                success=False,
                message="Nessun piano di conversione disponibile",
            )
        
        source_path = result.filepath
        plan = result.conversion_plan
        
        # Se è già compatibile, non convertire
        if result.is_compatible:
            return ConversionResult(
                source_path=source_path,
                output_path=source_path,
                success=True,
                message="File già compatibile, nessuna conversione necessaria",
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
            
            # Leggi stderr per progresso (opzionale)
            stderr_output = []
            if process.stderr:
                for line in process.stderr:
                    stderr_output.append(line)
                    # Qui si potrebbe parsare il progresso
                    if progress_callback:
                        pass  # Parsing complesso, skip per ora
            
            returncode = process.wait(timeout=FFMPEG_TIMEOUT)
            
            if returncode != 0:
                error_msg = "".join(stderr_output[-10:])  # Ultime 10 linee
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
                message=f"Convertito in {plan.output_format} {plan.target_bit_depth}bit/{plan.target_sample_rate/1000:.1f}kHz",
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            return ConversionResult(
                source_path=source_path,
                output_path=None,
                success=False,
                message="Timeout durante la conversione",
            )
        except Exception as e:
            return ConversionResult(
                source_path=source_path,
                output_path=None,
                success=False,
                message=f"Errore: {str(e)[:100]}",
            )

    def convert_batch(
        self,
        results: list[CompatibilityResult],
        output_dir: Optional[Path] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> list[ConversionResult]:
        """Converte batch di file in parallelo.
        
        Args:
            results: Lista di risultati compatibilità.
            output_dir: Directory di output opzionale.
            progress_callback: Callback(current, total).
            
        Returns:
            Lista di ConversionResult.
        """
        # Filtra solo quelli che necessitano conversione
        to_convert = [r for r in results if r.needs_conversion]
        
        if not to_convert:
            return []
        
        conversion_results = []
        completed = 0
        total = len(to_convert)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tutti i task
            future_to_result = {
                executor.submit(self.convert, r, output_dir): r
                for r in to_convert
            }
            
            # Raccogli risultati
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
        """Genera riepilogo conversioni.
        
        Args:
            results: Lista di risultati conversione.
            
        Returns:
            Dict con statistiche.
        """
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        return {
            "total": len(results),
            "successful": successful,
            "failed": failed,
            "outputs": [r.output_path for r in results if r.output_path],
        }
