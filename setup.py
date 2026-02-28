#!/usr/bin/env python3
"""
CDJ-Check Setup
===============
Script di setup per lo sviluppo e la distribuzione.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cdj-check",
    version="1.0.0",
    author="CDJ-Check Team",
    author_email="",
    description="Audio Compatibility Checker & Converter per Pioneer CDJ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuousername/cdj-check",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "customtkinter>=5.2.0",
        "tkinterdnd2>=0.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.0.0",
            "ruff>=0.2.0",
            "pyinstaller>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cdj-check=cdj_check.main:main",
            "cdj-check-gui=cdj_check.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cdj_check": ["*.icns", "*.png"],
    },
)
