"""Entry point principale per CDJ-Check."""

import argparse
import sys
from pathlib import Path


def run_gui():
    """Avvia l'interfaccia grafica."""
    from cdj_check.gui import main as gui_main
    gui_main()


def run_cli():
    """Avvia la modalità CLI."""
    parser = argparse.ArgumentParser(
        description="CDJ-Check — Audio Compatibility Checker per Pioneer CDJ-2000 Nexus",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s --gui                          # Avvia GUI
  %(prog)s check file.mp3                 # Verifica un file
  %(prog)s check folder/                  # Verifica tutta una cartella
  %(prog)s convert file.flac              # Converte un file
  %(prog)s convert folder/ --output dir/  # Converte con output specifico
        """,
    )
    
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Avvia l'interfaccia grafica (default se nessun comando)",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandi disponibili")
    
    # Comando check
    check_parser = subparsers.add_parser(
        "check",
        help="Verifica compatibilità file audio",
    )
    check_parser.add_argument(
        "path",
        type=Path,
        help="File o cartella da verificare",
    )
    check_parser.add_argument(
        "--json",
        action="store_true",
        help="Output in formato JSON",
    )
    
    # Comando convert
    convert_parser = subparsers.add_parser(
        "convert",
        help="Converte file non compatibili",
    )
    convert_parser.add_argument(
        "path",
        type=Path,
        help="File o cartella da convertire",
    )
    convert_parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Cartella di output (default: CDJ_Ready/)",
    )
    convert_parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="Numero di thread paralleli (default: 2, max: 4)",
    )
    
    args = parser.parse_args()
    
    # Default: GUI
    if args.gui or args.command is None:
        run_gui()
        return
    
    # Esegui comando
    if args.command == "check":
        cli_check(args)
    elif args.command == "convert":
        cli_convert(args)
    else:
        parser.print_help()


def cli_check(args):
    """Comando check per CLI."""
    import json
    
    from cdj_check.analyzer import AudioAnalyzer
    from cdj_check.compatibility import CompatibilityEngine
    
    analyzer = AudioAnalyzer()
    engine = CompatibilityEngine()
    
    # Raccogli file
    files = []
    if args.path.is_file():
        files = [args.path]
    elif args.path.is_dir():
        for ext in [".mp3", ".m4a", ".wav", ".aiff", ".aif", ".flac", ".ogg", ".opus", ".wma"]:
            files.extend(args.path.glob(f"*{ext}"))
            files.extend(args.path.glob(f"*{ext.upper()}"))
    else:
        print(f"Errore: percorso non trovato: {args.path}")
        sys.exit(1)
    
    # Analizza
    results = []
    for f in files:
        try:
            metadata = analyzer.analyze(f)
            result = engine.check(metadata)
            results.append(result)
        except Exception as e:
            print(f"❌ Errore analizzando {f.name}: {e}")
    
    # Output
    if args.json:
        # JSON output
        data = []
        for r in results:
            data.append({
                "file": r.filepath.name,
                "status": r.status.value,
                "message": r.message,
                "codec": r.metadata.codec if r.metadata else None,
                "sample_rate": r.metadata.sample_rate if r.metadata else None,
                "bit_depth": r.metadata.bit_depth if r.metadata else None,
            })
        print(json.dumps(data, indent=2))
    else:
        # Human readable
        print(f"\n{'=' * 60}")
        print(f"CDJ-Check Report — {len(results)} file analizzati")
        print(f"{'=' * 60}\n")
        
        compatible = sum(1 for r in results if r.is_compatible)
        convertible = sum(1 for r in results if r.needs_conversion)
        errors = len(results) - compatible - convertible
        
        for r in results:
            icon = r.status_icon
            print(f"{icon} {r.filepath.name[:40]:<40} {r.status.value}")
            if not r.is_compatible:
                print(f"   └─ {r.message}")
        
        print(f"\n{'=' * 60}")
        print(f"✅ Compatibili: {compatible}")
        print(f"⚠️  Da convertire: {convertible}")
        if errors:
            print(f"❌ Errori: {errors}")
        print(f"{'=' * 60}")


def cli_convert(args):
    """Comando convert per CLI."""
    from cdj_check.analyzer import AudioAnalyzer
    from cdj_check.compatibility import CompatibilityEngine
    from cdj_check.converter import AudioConverter
    
    analyzer = AudioAnalyzer()
    engine = CompatibilityEngine()
    converter = AudioConverter(max_workers=min(args.workers, 4))
    
    # Raccogli file
    files = []
    if args.path.is_file():
        files = [args.path]
    elif args.path.is_dir():
        for ext in [".mp3", ".m4a", ".wav", ".aiff", ".aif", ".flac", ".ogg", ".opus", ".wma"]:
            files.extend(args.path.glob(f"*{ext}"))
            files.extend(args.path.glob(f"*{ext.upper()}"))
    else:
        print(f"Errore: percorso non trovato: {args.path}")
        sys.exit(1)
    
    print(f"🔍 Analisi di {len(files)} file...")
    
    # Analizza
    results = []
    for f in files:
        try:
            metadata = analyzer.analyze(f)
            result = engine.check(metadata)
            results.append(result)
        except Exception as e:
            print(f"❌ Errore analizzando {f.name}: {e}")
    
    to_convert = [r for r in results if r.needs_conversion]
    
    if not to_convert:
        print("✅ Tutti i file sono già compatibili!")
        return
    
    print(f"⚙️  Conversione di {len(to_convert)} file...")
    
    # Converti
    def on_progress(done: int, total: int):
        pct = int(100 * done / total)
        print(f"\r  Progresso: {pct}% ({done}/{total})", end="", flush=True)
    
    conversion_results = converter.convert_batch(to_convert, args.output, on_progress)
    print()  # Newline dopo progress
    
    # Riepilogo
    summary = converter.get_conversion_summary(conversion_results)
    print(f"\n{'=' * 60}")
    print(f"✅ Completati: {summary['successful']}")
    if summary['failed']:
        print(f"❌ Falliti: {summary['failed']}")
    print(f"{'=' * 60}")
    
    if summary['failed'] > 0:
        sys.exit(1)


def main():
    """Entry point."""
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\n👋 Interrotto dall'utente")
        sys.exit(130)
    except RuntimeError as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
