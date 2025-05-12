#!/usr/bin/env python3
"""
Setup script for Echo-Notes Installer package.
This allows the installer to be installed as a Python package.
"""

from setuptools import setup, find_packages
import sys
from pathlib import Path

# Get the current directory
here = Path(__file__).parent.absolute()

# Get the long description from the README file
with open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()

# Get version from CHANGELOG.md
version = "1.0.0"  # Default version
try:
    with open(here / "CHANGELOG.md", encoding="utf-8") as f:
        for line in f:
            if line.startswith("## ["):
                version = line.split("[")[1].split("]")[0]
                break
except (FileNotFoundError, IOError, IndexError):
    # Handle file not found, IO errors, or parsing errors
    pass

# Platform-specific dependencies
platform_deps = []
if sys.platform.startswith("win"):
    platform_deps = ["pywin32>=223"]
elif sys.platform.startswith("darwin"):
    platform_deps = []
elif sys.platform.startswith("linux"):
    platform_deps = []

setup(
    name="echo-notes-installer",
    version=version,
    description="Cross-platform installer for Echo-Notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes",
    author="Echo-Notes Team",
    author_email="echo-notes@example.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="installer, echo-notes, cross-platform",
    packages=find_packages(include=["installers", "installers.*"]),
    python_requires=">=3.8, <4",
    install_requires=[
        "requests>=2.25.0",
        "tqdm>=4.50.0",
    ]
    + platform_deps,
    package_data={
        "installers": ["README.md", "CHANGELOG.md"],
    },
    entry_points={
        "console_scripts": [
            "echo-notes-install-windows=installers.install_windows:main",
            "echo-notes-install-linux=installers.linux.linux_installer:main_cli",
            "echo-notes-install-macos=installers.macos.macos_installer:main_cli",
            "echo-notes-uninstall-windows=installers.windows.windows_uninstaller:main_cli",
            "echo-notes-uninstall-linux=installers.linux.linux_uninstaller:main_cli",
            "echo-notes-uninstall-macos=installers.macos.macos_uninstaller:main_cli",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/issues",
        "Source": "https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes",
    },
)
