#!/usr/bin/env python3
"""
Echo-Notes Installer Utilities
This module provides shared utility functions for the Echo-Notes installer.
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
import venv


# ANSI color codes
class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def print_color(color, message):
    """Print colored message if supported"""
    if sys.platform != "win32" or os.environ.get("TERM") == "xterm":
        print(f"{color}{message}{Colors.NC}")
    else:
        print(message)


def detect_os():
    """
    Detect the operating system.

    Returns:
        str: One of 'linux', 'macos', 'windows', or 'unknown'
    """
    system = platform.system().lower()
    if system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"


def check_python_version(min_version=(3, 7)):
    """
    Check if the current Python version meets the minimum requirement.

    Args:
        min_version (tuple): Minimum required Python version as (major, minor)

    Returns:
        bool: True if the Python version is sufficient, False otherwise
    """
    if sys.version_info < min_version:
        print_color(
            Colors.RED,
            f"Error: Python {min_version[0]}.{min_version[1]} or higher is required.",
        )
        print_color(Colors.RED, f"Current Python version: {sys.version}")
        return False

    print_color(Colors.GREEN, f"Python version check passed: {sys.version}")
    return True


def find_python_executable():
    """
    Find the appropriate Python executable.

    Returns:
        str: Path to the Python executable
    """
    if command_exists("python3"):
        return "python3"
    elif command_exists("python"):
        # Check if python is Python 3
        try:
            version = subprocess.check_output(
                ["python", "--version"],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
            if "Python 3" in version:
                return "python"
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    print_color(Colors.RED, "Error: Python 3 is required but not found.")
    print_color(Colors.RED, "Please install Python 3 and try again.")
    return None


def command_exists(cmd):
    """
    Check if a command exists in the system PATH.

    Args:
        cmd (str): Command to check

    Returns:
        bool: True if the command exists, False otherwise
    """
    return shutil.which(cmd) is not None


def create_virtual_environment(install_dir, venv_name="echo_notes_venv"):
    """
    Create a Python virtual environment.

    Args:
        install_dir (str or Path): Installation directory
        venv_name (str): Name of the virtual environment directory

    Returns:
        Path: Path to the created virtual environment
    """
    install_dir = Path(install_dir)
    venv_path = install_dir / venv_name

    print_color(Colors.BLUE, "Setting up virtual environment...")

    # Remove existing virtual environment if it's broken
    if venv_path.exists():
        # Test if pip is working in the existing venv
        os_type = detect_os()
        pip_path = venv_path / ("Scripts" if os_type == "windows" else "bin") / "pip"

        if not pip_path.exists() or not test_pip(pip_path):
            print_color(
                Colors.YELLOW,
                "Existing virtual environment appears to be broken. Recreating...",
            )
            shutil.rmtree(venv_path, ignore_errors=True)
        else:
            print_color(Colors.YELLOW, "Using existing virtual environment")
            return venv_path

    # Create virtual environment if it doesn't exist
    if not venv_path.exists():
        print_color(Colors.BLUE, "Creating new virtual environment...")
        try:
            venv.create(venv_path, with_pip=True)
            print_color(Colors.GREEN, "Created virtual environment")
        except Exception as e:
            print_color(Colors.RED, f"Error creating virtual environment: {e}")
            return None

    return venv_path


def test_pip(pip_path):
    """
    Test if pip is working in a virtual environment.

    Args:
        pip_path (Path): Path to pip executable

    Returns:
        bool: True if pip is working, False otherwise
    """
    try:
        subprocess.run(
            [str(pip_path), "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def install_dependencies(venv_path, requirements_file=None, dev_mode=True):
    """
    Install dependencies in the virtual environment.

    Args:
        venv_path (Path): Path to the virtual environment
        requirements_file (str or Path, optional): Path to requirements.txt
        dev_mode (bool): Whether to install the package in development mode

    Returns:
        bool: True if installation was successful, False otherwise
    """
    print_color(Colors.BLUE, "Installing dependencies...")

    os_type = detect_os()
    pip_path = venv_path / ("Scripts" if os_type == "windows" else "bin") / "pip"

    # Upgrade pip
    try:
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        print_color(Colors.GREEN, "Pip upgraded successfully")
    except subprocess.SubprocessError as e:
        print_color(Colors.RED, f"Error upgrading pip: {e}")
        return False

    # Install required packages
    try:
        subprocess.run(
            [str(pip_path), "install", "requests", "python-dateutil", "PyQt6"],
            check=True,
        )
        print_color(Colors.GREEN, "Installed core dependencies")
    except subprocess.SubprocessError as e:
        print_color(Colors.RED, f"Error installing core dependencies: {e}")
        return False

    # Install from requirements.txt if available
    if requirements_file and Path(requirements_file).exists():
        try:
            subprocess.run(
                [str(pip_path), "install", "-r", str(requirements_file)], check=True
            )
            print_color(Colors.GREEN, "Installed dependencies from requirements.txt")
        except subprocess.SubprocessError as e:
            print_color(Colors.RED, f"Error installing from requirements.txt: {e}")
            return False

    # Install the package in development mode
    if dev_mode:
        try:
            subprocess.run([str(pip_path), "install", "-e", "."], check=True)
            print_color(Colors.GREEN, "Installed Echo-Notes in development mode")
        except subprocess.SubprocessError as e:
            print_color(Colors.RED, f"Error installing in development mode: {e}")
            return False

    return True


def configure_application(install_dir):
    """
    Configure the Echo-Notes application.

    Args:
        install_dir (str or Path): Installation directory

    Returns:
        bool: True if configuration was successful, False otherwise
    """
    print_color(Colors.BLUE, "Configuring Echo-Notes...")
    install_dir = Path(install_dir)

    # Create default configuration if needed
    config_dir = install_dir / "shared"
    config_file = config_dir / "schedule_config.json"

    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)

    if not config_file.exists():
        default_config = """{
    "processing_interval": 60,
    "summary_interval": 10080,
    "summary_day": 6,
    "summary_hour": 12,
    "daemon_enabled": true
}"""
        try:
            with open(config_file, "w") as f:
                f.write(default_config)
            print_color(Colors.GREEN, "Created default schedule configuration")
        except IOError as e:
            print_color(Colors.RED, f"Error creating configuration file: {e}")
            return False

    # Ensure the notes directory exists
    notes_dir = os.environ.get(
        "ECHO_NOTES_DIR", str(Path.home() / "Documents/notes/log")
    )
    try:
        os.makedirs(notes_dir, exist_ok=True)
        print_color(Colors.GREEN, f"Ensured notes directory exists: {notes_dir}")
    except OSError as e:
        print_color(Colors.RED, f"Error creating notes directory: {e}")
        return False

    return True


def get_installation_directory(default_dir=None):
    """
    Ask the user for the installation directory.

    Args:
        default_dir (str or Path, optional): Default installation directory

    Returns:
        Path: Selected installation directory
    """
    if default_dir is None:
        default_dir = Path.home() / "Echo-Notes"
    else:
        default_dir = Path(default_dir)

    print(f"Default installation directory: {default_dir}")
    custom_dir = input(
        "Press Enter to use default or specify a different directory: "
    ).strip()

    if custom_dir:
        install_dir = Path(custom_dir)
    else:
        install_dir = default_dir

    # Create installation directory if it doesn't exist
    os.makedirs(install_dir, exist_ok=True)

    return install_dir
