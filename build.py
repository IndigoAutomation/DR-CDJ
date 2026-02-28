#!/usr/bin/env python3
"""
Build script for Dr. CDJ using PyInstaller.
Automatically downloads and bundles FFmpeg for standalone operation.
"""

import platform
import shutil
import subprocess
import sys
from pathlib import Path


def check_pyinstaller():
    """Verify PyInstaller is installed."""
    if not shutil.which("pyinstaller"):
        print("❌ PyInstaller not found.")
        print("Install with: pip install pyinstaller")
        sys.exit(1)
    print("✅ PyInstaller found")


def download_ffmpeg():
    """Download FFmpeg binaries for bundling."""
    script_path = Path(__file__).parent / "scripts" / "download-ffmpeg.py"
    
    if not script_path.exists():
        print(f"❌ Download script not found: {script_path}")
        return False
    
    print("\n📦 Downloading FFmpeg for bundling...")
    result = subprocess.run([sys.executable, str(script_path)])
    
    if result.returncode != 0:
        print("⚠️  FFmpeg download failed, will rely on runtime auto-download")
        return False
    
    return True


def clean_dist():
    """Clean previous build artifacts."""
    print("\n🧹 Cleaning previous builds...")
    
    dirs_to_clean = ["dist", "build"]
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   Removed {dir_name}/")
    
    # Remove .spec files except Dr-CDJ.spec
    for spec in Path(".").glob("*.spec"):
        if spec.name != "Dr-CDJ.spec":
            spec.unlink()
            print(f"   Removed {spec.name}")


def build_macos():
    """Build for macOS (.app bundle)."""
    print("\n🍎 Building for macOS...")
    
    # Download FFmpeg first
    download_ffmpeg()
    
    # Use the spec file for building
    spec_file = Path("Dr-CDJ.spec")
    if not spec_file.exists():
        print(f"❌ Spec file not found: {spec_file}")
        print("Using direct pyinstaller command...")
        
        # Fallback to direct command
        cmd = [
            "pyinstaller",
            "--name", "Dr-CDJ",
            "--windowed",
            "--onedir",
            "--clean",
            "--noconfirm",
            "--osx-bundle-identifier", "com.dr-cdj.app",
            "--add-data", "src/dr_cdj/bin:bin",
            "src/dr_cdj/main.py",
        ]
    else:
        cmd = ["pyinstaller", str(spec_file), "--clean", "--noconfirm"]
    
    print(f"\nRunning: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print("\n❌ Build failed!")
        sys.exit(1)
    
    print("\n✅ Build completed!")
    
    # Report app size
    app_path = Path("dist/Dr-CDJ.app")
    if app_path.exists():
        size = sum(f.stat().st_size for f in app_path.rglob('*') if f.is_file())
        size_mb = size / (1024 * 1024)
        print(f"📦 App bundle size: {size_mb:.1f} MB")
        print(f"   Location: {app_path.absolute()}")


def build_windows():
    """Build for Windows (.exe)."""
    print("\n🪟 Building for Windows...")
    
    cmd = [
        "pyinstaller",
        "--name", "Dr-CDJ",
        "--windowed",
        "--onedir",
        "--clean",
        "--noconfirm",
        "--add-data", "src/dr_cdj/bin;bin",
        "src/dr_cdj/main.py",
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print("\n❌ Build failed!")
        sys.exit(1)
    
    print("\n✅ Build completed!")
    print("Output: dist/Dr-CDJ/")


def build_linux():
    """Build for Linux (executable)."""
    print("\n🐧 Building for Linux...")
    
    cmd = [
        "pyinstaller",
        "--name", "Dr-CDJ",
        "--windowed",
        "--onedir",
        "--clean",
        "--noconfirm",
        "--add-data", "src/dr_cdj/bin:bin",
        "src/dr_cdj/main.py",
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print("\n❌ Build failed!")
        sys.exit(1)
    
    print("\n✅ Build completed!")
    print("Output: dist/Dr-CDJ/")


def main():
    """Entry point."""
    print("=" * 50)
    print("🔧 Dr. CDJ Build System")
    print("=" * 50)
    
    check_pyinstaller()
    clean_dist()
    
    system = platform.system()
    
    if system == "Darwin":
        build_macos()
    elif system == "Windows":
        build_windows()
    elif system == "Linux":
        build_linux()
    else:
        print(f"❌ Unsupported operating system: {system}")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Build completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
