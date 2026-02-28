#!/usr/bin/env python3
"""
Dr. CDJ Setup
===============
Script di setup per lo sviluppo e la distribuzione.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dr-cdj",
    version="1.0.1",
    author="Dr. CDJ Team",
    author_email="",
    description="Dr. CDJ - Audio Compatibility Checker & Converter per Pioneer CDJ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IndigoAutomation/Dr-CDJ",
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
            "dr-cdj=dr_cdj.main:main",
            "dr-cdj-gui=dr_cdj.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "dr_cdj": ["*.icns", "*.png"],
    },
)
