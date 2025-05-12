#!/usr/bin/env python3
"""
Echo-Notes Uninstaller Script
This script provides a simple way to uninstall Echo-Notes.
"""

import os
import sys
import subprocess
from pathlib import Path

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


def main():
    """Main uninstaller function"""
    print_color(Colors.BLUE, "===== Echo-Notes Uninstaller =====")
    print("")

    # Default installation directory
    default_install_dir = Path.home() / "Echo-Notes"
    install_dir = None
    purge = False

    # Parse command line arguments
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--install-dir" and i + 1 < len(sys.argv):
            install_dir = Path(sys.argv[i + 1])
            i += 2
        elif arg == "--purge":
            purge = True
            i += 1
        elif arg == "--help":
            print("Echo-Notes Uninstaller")
            print("")
            print("Usage: python uninstall.py [options]")
            print("")
            print("Options:")
            print("  --install-dir DIR    Specify installation directory")
            print("  --purge              Remove user notes as well")
            print("  --help               Show this help message")
            return 0
        else:
            print_color(Colors.RED, f"Unknown option: {arg}")
            print("Use --help for usage information.")
            return 1

    # If installation directory not specified, use default or ask user
    if install_dir is None:
        if default_install_dir.exists():
            install_dir = default_install_dir
            print_color(Colors.BLUE, f"Using default installation directory: {install_dir}")
        else:
            print_color(Colors.YELLOW, f"Default installation directory not found: {default_install_dir}")
            print_color(Colors.YELLOW, "Please specify the installation directory using --install-dir")
            return 1

    # Check if the installation directory exists
    if not install_dir.exists():
        print_color(Colors.RED, f"Error: Installation directory not found: {install_dir}")
        return 1

    # Check if the uninstaller module exists
    uninstaller_module = install_dir / "installers" / "linux" / "linux_uninstaller.py"
    if not uninstaller_module.exists():
        print_color(Colors.RED, f"Error: Uninstaller module not found: {uninstaller_module}")
        return 1

    # Confirm uninstallation
    print_color(Colors.YELLOW, f"This will uninstall Echo-Notes from: {install_dir}")
    if purge:
        print_color(Colors.RED, "WARNING: This will also remove all your notes!")

    response = input("Do you want to continue? (y/N) ").strip().lower()
    if response != "y":
        print_color(Colors.YELLOW, "Uninstallation cancelled.")
        return 0

    # Run the uninstaller module
    print_color(Colors.BLUE, "Running uninstaller...")
    cmd = [sys.executable, str(uninstaller_module), str(install_dir)]
    if purge:
        cmd.append("--purge")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print_color(Colors.RED, "Uninstallation failed.")
        return 1

    # Ask if user wants to remove the installation directory
    response = input("Do you want to remove the installation directory? (y/N) ").strip().lower()
    if response == "y":
        try:
            import shutil
            shutil.rmtree(install_dir)
            print_color(Colors.GREEN, f"Installation directory removed: {install_dir}")
        except Exception as e:
            print_color(Colors.RED, f"Error removing installation directory: {e}")
            return 1

    # Remove this uninstaller script
    print_color(Colors.BLUE, "Removing uninstaller scripts...")
    try:
        script_path = Path(__file__).resolve()
        script_path.unlink()
        print_color(Colors.GREEN, f"Uninstaller script removed: {script_path}")

        # Also try to remove the shell script if it exists
        shell_script = Path.home() / "uninstall.sh"
        if shell_script.exists():
            shell_script.unlink()
            print_color(Colors.GREEN, f"Shell uninstaller script removed: {shell_script}")
    except Exception as e:
        print_color(Colors.YELLOW, f"Warning: Could not remove uninstaller script: {e}")

    print_color(Colors.GREEN, "Uninstallation completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())