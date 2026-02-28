#!/usr/bin/env python3
"""
Download FFmpeg static binaries for macOS during build.
This ensures the app is completely standalone.
"""

import os
import sys
import ssl
import urllib.request
import zipfile
import tarfile
import platform
from pathlib import Path

# FFmpeg static builds from evermeet.cx (same source as the runtime downloader)
# These are x86_64 binaries that run natively on Intel and via Rosetta 2 on Apple Silicon.
# eugeneware/ffmpeg-static arm64 builds are incompatible with macOS 14+.
FFMPEG_URLS = {
    "Darwin-x86_64": "https://evermeet.cx/ffmpeg/ffmpeg-6.1.1.zip",
    "Darwin-arm64":  "https://evermeet.cx/ffmpeg/ffmpeg-6.1.1.zip",
    "Darwin-FFPROBE-x86_64": "https://evermeet.cx/ffmpeg/ffprobe-6.1.1.zip",
    "Darwin-FFPROBE-arm64":  "https://evermeet.cx/ffmpeg/ffprobe-6.1.1.zip",
}
# These are zip archives; the binary inside is extracted automatically below.


def get_system_info():
    """Get current system architecture."""
    system = platform.system()
    machine = platform.machine()
    
    # On Apple Silicon, machine can be 'arm64' or 'x86_64' (if running under Rosetta)
    if system == "Darwin":
        # Check if we're actually on Apple Silicon
        import subprocess
        try:
            result = subprocess.run(["uname", "-m"], capture_output=True, text=True)
            machine = result.stdout.strip()
        except:
            pass
    
    return system, machine


def download_file(url: str, dest: Path, chunk_size: int = 8192) -> bool:
    """Download a file with progress."""
    print(f"Downloading: {url}")
    print(f"Destination: {dest}")
    
    # Create SSL context that doesn't verify certificates (some CI environments need this)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=120) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            
            with open(dest, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  Progress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='', flush=True)
        
        print()  # New line after progress
        return True
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        if dest.exists():
            dest.unlink()
        return False


def make_executable(path: Path):
    """Make file executable."""
    current_mode = path.stat().st_mode
    path.chmod(current_mode | 0o755)
    print(f"✅ Made executable: {path}")


def download_ffmpeg_for_build():
    """Download FFmpeg binaries for bundling with the app."""
    system, machine = get_system_info()
    print(f"🔧 Build system: {system} {machine}")
    
    if system != "Darwin":
        print(f"⚠️  FFmpeg bundling only supported on macOS during build")
        print(f"   Current system: {system}")
        return False
    
    # Create bundled bin directory
    bin_dir = Path(__file__).parent.parent / "src" / "dr_cdj" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    # Map machine to download key
    arch_key = f"{system}-{machine}"
    ffmpeg_key = f"{system}-{machine}"
    ffprobe_key = f"{system}-FFPROBE-{machine}"
    
    if ffmpeg_key not in FFMPEG_URLS:
        print(f"❌ Unsupported architecture: {arch_key}")
        print(f"   Supported: {list(FFMPEG_URLS.keys())}")
        return False
    
    success = True

    def fetch_binary(url: str, dest: Path, name: str) -> bool:
        """Download a binary, handling both raw files and .zip archives."""
        if dest.exists():
            print(f"✅ {name} already exists: {dest}")
            return True

        if url.endswith(".zip"):
            import tempfile, zipfile as zf
            tmp = Path(tempfile.mktemp(suffix=".zip"))
            if not download_file(url, tmp):
                return False
            print(f"  Extracting {name} from zip...")
            with zf.ZipFile(tmp, "r") as z:
                # evermeet.cx zips contain a single binary named after the tool
                members = [m for m in z.namelist() if not m.startswith("__MACOSX")]
                if not members:
                    print(f"❌ Empty zip for {name}")
                    tmp.unlink(missing_ok=True)
                    return False
                binary_name = members[0]
                data = z.read(binary_name)
                dest.write_bytes(data)
            tmp.unlink(missing_ok=True)
        else:
            if not download_file(url, dest):
                return False

        make_executable(dest)
        return True

    # Download ffmpeg
    success = fetch_binary(FFMPEG_URLS[ffmpeg_key],  bin_dir / "ffmpeg",  "ffmpeg")  and success
    # Download ffprobe
    success = fetch_binary(FFMPEG_URLS[ffprobe_key], bin_dir / "ffprobe", "ffprobe") and success
    
    # Verify binaries work
    if success:
        print("\n🔍 Verifying binaries...")
        try:
            import subprocess
            
            result = subprocess.run(
                [str(ffmpeg_dest), "-version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print(f"✅ FFmpeg OK: {version[:50]}...")
            else:
                print(f"⚠️  FFmpeg test failed: {result.stderr}")
                success = False
            
            result = subprocess.run(
                [str(ffprobe_dest), "-version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print(f"✅ FFprobe OK: {version[:50]}...")
            else:
                print(f"⚠️  FFprobe test failed: {result.stderr}")
                success = False
                
        except Exception as e:
            print(f"⚠️  Verification failed: {e}")
            success = False
    
    # Report sizes
    if success:
        ffmpeg_size = ffmpeg_dest.stat().st_size / (1024 * 1024)
        ffprobe_size = ffprobe_dest.stat().st_size / (1024 * 1024)
        total_size = ffmpeg_size + ffprobe_size
        print(f"\n📦 Binary sizes:")
        print(f"   ffmpeg:  {ffmpeg_size:.1f} MB")
        print(f"   ffprobe: {ffprobe_size:.1f} MB")
        print(f"   total:   {total_size:.1f} MB")
        print(f"\n✅ FFmpeg bundled successfully!")
        print(f"   Location: {bin_dir}")
    
    return success


if __name__ == "__main__":
    success = download_ffmpeg_for_build()
    sys.exit(0 if success else 1)
