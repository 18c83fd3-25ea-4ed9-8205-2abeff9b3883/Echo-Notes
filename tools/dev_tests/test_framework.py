#!/usr/bin/env python3
"""
Echo-Notes Installer Framework Test Script
This script tests the basic functionality of the installer framework.
"""

import sys
from pathlib import Path

# Add the parent directory to the Python path to allow importing the installers package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Now that we've modified the path, we can import from installers
from installers.common import (  # noqa: E402
    Colors,
    print_color,
    detect_os,
    check_python_version,
    find_python_executable,
    command_exists,
)


def test_framework():
    """Test the basic functionality of the installer framework."""
    print_color(Colors.BLUE, "=== Echo-Notes Installer Framework Test ===")

    # Test OS detection
    os_type = detect_os()
    print_color(Colors.GREEN, f"Detected operating system: {os_type}")

    # Test Python version check
    python_ok = check_python_version()
    print_color(
        Colors.GREEN if python_ok else Colors.RED,
        f"Python version check: {'Passed' if python_ok else 'Failed'}",
    )

    # Test Python executable finder
    python_exec = find_python_executable()
    print_color(
        Colors.GREEN if python_exec else Colors.RED,
        f"Python executable: {python_exec or 'Not found'}",
    )

    # Test command existence check
    commands = ["python", "pip", "git"]
    for cmd in commands:
        exists = command_exists(cmd)
        print_color(
            Colors.GREEN if exists else Colors.YELLOW,
            f"Command '{cmd}': {'Found' if exists else 'Not found'}",
        )

    print_color(Colors.BLUE, "=== Test Complete ===")
    return True


if __name__ == "__main__":
    test_framework()
