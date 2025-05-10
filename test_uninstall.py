#!/usr/bin/env python3
"""
Echo-Notes Uninstaller Test Script
This script simulates the uninstallation process without actually removing any files.
It helps users verify what would be removed during the actual uninstallation.
"""

import os
import sys
import platform
from pathlib import Path

# ANSI color codes
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_color(color, message):
    """Print colored message if supported"""
    if sys.platform != "win32" or os.environ.get("TERM") == "xterm":
        print(f"{color}{message}{Colors.NC}")
    else:
        print(message)

def get_script_dir():
    """Get the script directory"""
    return Path(__file__).resolve().parent

def detect_os():
    """Detect the operating system"""
    system = platform.system().lower()
    if system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"

def test_linux_uninstall():
    """Test Linux-specific uninstallation"""
    print_color(Colors.BLUE, "Testing Linux-specific uninstallation...")
    
    home = Path.home()
    files_to_check = [
        home / ".local/share/applications/echo-notes.desktop",
        home / ".local/share/applications/echo-notes-direct.desktop",
        home / "Desktop/Echo Notes.desktop",
        home / "Desktop/Echo Notes (Direct).desktop",
        home / ".local/share/icons/echo-notes.png",
        home / ".local/bin/echo-notes-dashboard",
        home / ".local/bin/echo-notes-daemon",
        home / ".local/bin/echo-notes-config",
        home / ".local/bin/process-notes",
        home / ".local/bin/generate-summary"
    ]
    
    for file_path in files_to_check:
        if file_path.exists():
            print_color(Colors.YELLOW, f"Would remove: {file_path}")
        else:
            print_color(Colors.GREEN, f"Not found (would skip): {file_path}")

def test_macos_uninstall():
    """Test macOS-specific uninstallation"""
    print_color(Colors.BLUE, "Testing macOS-specific uninstallation...")
    
    home = Path.home()
    files_to_check = [
        home / "Applications/Echo Notes Dashboard.app",
        Path("/usr/local/bin/echo-notes-dashboard"),
        Path("/usr/local/bin/echo-notes-daemon"),
        Path("/usr/local/bin/echo-notes-config"),
        Path("/usr/local/bin/process-notes"),
        Path("/usr/local/bin/generate-summary")
    ]
    
    for file_path in files_to_check:
        if file_path.exists():
            print_color(Colors.YELLOW, f"Would remove: {file_path}")
        else:
            print_color(Colors.GREEN, f"Not found (would skip): {file_path}")

def test_windows_uninstall():
    """Test Windows-specific uninstallation"""
    print_color(Colors.BLUE, "Testing Windows-specific uninstallation...")
    
    # Check for desktop shortcut
    import os
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shortcut_path = os.path.join(desktop_path, "Echo Notes Dashboard.lnk")
    
    if os.path.exists(shortcut_path):
        print_color(Colors.YELLOW, f"Would remove: {shortcut_path}")
    else:
        print_color(Colors.GREEN, f"Not found (would skip): {shortcut_path}")

def test_common_uninstall():
    """Test common uninstallation steps"""
    print_color(Colors.BLUE, "Testing common uninstallation steps...")
    
    script_dir = get_script_dir()
    
    # Check virtual environment
    venv_path = script_dir / "echo_notes_venv"
    if venv_path.exists():
        print_color(Colors.YELLOW, f"Would remove: {venv_path}")
    else:
        print_color(Colors.GREEN, f"Not found (would skip): {venv_path}")
    
    # Check configuration file
    config_path = script_dir / "shared/schedule_config.json"
    if config_path.exists():
        print_color(Colors.YELLOW, f"Would remove: {config_path}")
    else:
        print_color(Colors.GREEN, f"Not found (would skip): {config_path}")
    
    # Check notes directory
    notes_dir = os.environ.get("ECHO_NOTES_DIR", str(Path.home() / "Documents/notes/log"))
    notes_path = Path(notes_dir)
    if notes_path.exists():
        print_color(Colors.GREEN, f"Would preserve: {notes_dir}")
        print_color(Colors.RED, f"Would remove with --purge option: {notes_dir}")
    else:
        print_color(Colors.GREEN, f"Notes directory not found: {notes_dir}")

def main():
    """Main test function"""
    print_color(Colors.BLUE, "=== Echo-Notes Uninstaller Test ===")
    print("This script simulates the uninstallation process without removing any files.")
    print("It helps you verify what would be removed during the actual uninstallation.")
    print()
    
    # Detect operating system
    os_type = detect_os()
    print_color(Colors.BLUE, f"Detected operating system: {os_type}")
    
    # Test common uninstallation steps
    test_common_uninstall()
    
    # OS-specific tests
    if os_type == "linux":
        test_linux_uninstall()
    elif os_type == "macos":
        test_macos_uninstall()
    elif os_type == "windows":
        test_windows_uninstall()
    else:
        print_color(Colors.YELLOW, "Unknown operating system. Skipping OS-specific tests.")
    
    print()
    print_color(Colors.GREEN, "Test completed!")
    print("To perform the actual uninstallation, run one of the following:")
    print("  ./uninstall.sh       # For Linux/macOS/Git Bash")
    print("  uninstall.bat        # For Windows")
    print("  python uninstall.py  # For any platform")
    print()

if __name__ == "__main__":
    main()