"""
Echo-Notes Installer Common Utilities
This package provides common utilities for the Echo-Notes installer.
"""

from .installer_utils import (
    Colors,
    print_color,
    detect_os,
    check_python_version,
    find_python_executable,
    command_exists,
    create_virtual_environment,
    install_dependencies,
    configure_application,
    get_installation_directory,
)

from .download_manager import DownloadManager, download_echo_notes

__all__ = [
    "Colors",
    "print_color",
    "detect_os",
    "check_python_version",
    "find_python_executable",
    "command_exists",
    "create_virtual_environment",
    "install_dependencies",
    "configure_application",
    "get_installation_directory",
    "DownloadManager",
    "download_echo_notes",
]
