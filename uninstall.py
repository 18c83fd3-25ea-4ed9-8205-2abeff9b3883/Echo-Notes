#!/usr/bin/env python3
"""
Echo-Notes Unified Uninstallation Script
This script removes Echo-Notes while preserving user notes
"""

import os
import sys
import shutil
import argparse
import subprocess
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

def verify_directory():
    """Verify we're in the correct directory"""
    script_dir = get_script_dir()
    dashboard_path = script_dir / "echo_notes_dashboard.py"
    
    if not dashboard_path.exists():
        print_color(Colors.RED, "Error: Could not find echo_notes_dashboard.py in the current directory.")
        print("This script must be run from the Echo-Notes directory.")
        print(f"Current directory: {script_dir}")
        print("Files in current directory:")
        for item in script_dir.iterdir():
            print(f"  {item.name}")
        
        # Try to find the correct directory
        possible_dirs = list(script_dir.glob("**/echo_notes_dashboard.py"))
        if possible_dirs:
            print_color(Colors.YELLOW, "Found possible Echo-Notes directories:")
            for path in possible_dirs:
                print(f"  {path.parent}")
            print_color(Colors.YELLOW, "Please run the uninstaller from one of these directories.")
        
        sys.exit(1)
    
    return script_dir

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

def stop_processes(os_type):
    """Stop running Echo-Notes processes"""
    print_color(Colors.BLUE, "Stopping Echo-Notes processes...")
    
    try:
        # Try to stop the daemon gracefully
        subprocess.run(["echo-notes-daemon", "--stop"], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=False)
    except FileNotFoundError:
        pass
    
    # Kill any remaining processes (platform-specific)
    if os_type in ["linux", "macos"]:
        try:
            subprocess.run(["pkill", "-f", "echo_notes_daemon.py"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL, 
                          check=False)
            subprocess.run(["pkill", "-f", "echo_notes_dashboard.py"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL, 
                          check=False)
        except FileNotFoundError:
            pass
    elif os_type == "windows":
        try:
            subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/FI", "WINDOWTITLE eq Echo-Notes*"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL, 
                          check=False)
        except FileNotFoundError:
            pass
    
    print_color(Colors.GREEN, "Processes stopped")

def uninstall_linux():
    """Perform Linux-specific uninstallation"""
    print_color(Colors.BLUE, "Performing Linux-specific uninstallation...")
    
    home = Path.home()
    
    # Remove desktop shortcuts
    (home / ".local/share/applications/echo-notes.desktop").unlink(missing_ok=True)
    (home / ".local/share/applications/echo-notes-direct.desktop").unlink(missing_ok=True)
    print_color(Colors.GREEN, "Removed application menu entries")
    
    # Remove desktop icons
    (home / "Desktop/Echo Notes.desktop").unlink(missing_ok=True)
    (home / "Desktop/Echo Notes (Direct).desktop").unlink(missing_ok=True)
    print_color(Colors.GREEN, "Removed desktop icons")
    
    # Remove icon
    (home / ".local/share/icons/echo-notes.png").unlink(missing_ok=True)
    print_color(Colors.GREEN, "Removed icon")
    
    # Remove symlinks
    (home / ".local/bin/echo-notes-dashboard").unlink(missing_ok=True)
    (home / ".local/bin/echo-notes-daemon").unlink(missing_ok=True)
    (home / ".local/bin/echo-notes-config").unlink(missing_ok=True)
    (home / ".local/bin/process-notes").unlink(missing_ok=True)
    (home / ".local/bin/generate-summary").unlink(missing_ok=True)
    print_color(Colors.GREEN, "Removed symlinks")
    
    # Update desktop database if command exists
    try:
        subprocess.run(["update-desktop-database", str(home / ".local/share/applications")], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=False)
    except FileNotFoundError:
        pass

def uninstall_macos():
    """Perform macOS-specific uninstallation"""
    print_color(Colors.BLUE, "Performing macOS-specific uninstallation...")
    
    home = Path.home()
    
    # Remove app bundle
    app_path = home / "Applications/Echo Notes Dashboard.app"
    if app_path.exists():
        shutil.rmtree(app_path, ignore_errors=True)
    print_color(Colors.GREEN, "Removed application bundle")
    
    # Remove symlinks
    for symlink in ["/usr/local/bin/echo-notes-dashboard", 
                   "/usr/local/bin/echo-notes-daemon", 
                   "/usr/local/bin/echo-notes-config", 
                   "/usr/local/bin/process-notes", 
                   "/usr/local/bin/generate-summary"]:
        try:
            Path(symlink).unlink(missing_ok=True)
        except (PermissionError, OSError):
            print_color(Colors.YELLOW, f"Warning: Could not remove {symlink} (permission denied)")
    
    print_color(Colors.GREEN, "Removed symlinks")

def uninstall_windows():
    """Perform Windows-specific uninstallation"""
    print_color(Colors.BLUE, "Performing Windows-specific uninstallation...")
    
    # Remove desktop shortcut using PowerShell
    try:
        ps_command = "Remove-Item -Path ([Environment]::GetFolderPath('Desktop') + '\\Echo Notes Dashboard.lnk') -Force -ErrorAction SilentlyContinue"
        subprocess.run(["powershell", "-Command", ps_command], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=False)
        print_color(Colors.GREEN, "Removed desktop shortcut")
    except FileNotFoundError:
        print_color(Colors.YELLOW, "Warning: PowerShell not found. Please manually remove the shortcut.")

def remove_venv(script_dir):
    """Remove the virtual environment"""
    print_color(Colors.BLUE, "Removing virtual environment...")
    
    venv_path = script_dir / "echo_notes_venv"
    if venv_path.exists():
        shutil.rmtree(venv_path, ignore_errors=True)
        print_color(Colors.GREEN, "Removed virtual environment")
    else:
        print_color(Colors.YELLOW, "Virtual environment not found")

def remove_package_dir(script_dir):
    """Remove the echo_notes package directory"""
    print_color(Colors.BLUE, "Removing echo_notes package directory...")
    
    package_path = script_dir / "echo_notes"
    if package_path.exists():
        shutil.rmtree(package_path, ignore_errors=True)
        print_color(Colors.GREEN, "Removed echo_notes package directory")
    else:
        print_color(Colors.YELLOW, "echo_notes package directory not found")

def main():
    """Main uninstallation process"""
    parser = argparse.ArgumentParser(description="Echo-Notes Unified Uninstaller")
    parser.add_argument("--keep-config", action="store_true", help="Keep configuration files")
    parser.add_argument("--purge", action="store_true", help="Remove everything including notes (USE WITH CAUTION)")
    args = parser.parse_args()
    
    print_color(Colors.BLUE, "=== Echo-Notes Unified Uninstaller ===")
    
    # Verify we're in the correct directory
    script_dir = verify_directory()
    print(f"Uninstallation directory: {script_dir}")
    
    # Detect operating system
    os_type = detect_os()
    print_color(Colors.BLUE, f"Detected operating system: {os_type}")
    
    # Ask for confirmation
    print_color(Colors.YELLOW, "This will uninstall Echo-Notes from your system.")
    print_color(Colors.GREEN, "Your notes will be preserved.")
    if args.purge:
        print_color(Colors.RED, "WARNING: --purge option selected. This will also remove your notes!")
    
    confirm = input("Do you want to continue? (y/N) ")
    if not confirm.lower().startswith('y'):
        print_color(Colors.YELLOW, "Uninstallation cancelled.")
        return
    
    # Stop running processes
    stop_processes(os_type)
    
    # OS-specific uninstallation
    if os_type == "linux":
        uninstall_linux()
    elif os_type == "macos":
        uninstall_macos()
    elif os_type == "windows":
        uninstall_windows()
    else:
        print_color(Colors.YELLOW, "Warning: Unknown operating system. Skipping OS-specific uninstallation.")
    
    # Remove virtual environment
    remove_venv(script_dir)
    
    # Remove echo_notes package directory
    remove_package_dir(script_dir)
    
    # Remove configuration files if not keeping them
    if not args.keep_config:
        print_color(Colors.BLUE, "Removing configuration files...")
        config_path = script_dir / "shared/schedule_config.json"
        if config_path.exists():
            config_path.unlink()
        print_color(Colors.GREEN, "Removed configuration files")
    else:
        print_color(Colors.YELLOW, "Keeping configuration files as requested")
    
    # Remove notes if purging
    if args.purge:
        print_color(Colors.RED, "Removing notes directory...")
        notes_dir = os.environ.get("ECHO_NOTES_DIR", str(Path.home() / "Documents/notes/log"))
        notes_path = Path(notes_dir)
        if notes_path.exists():
            shutil.rmtree(notes_path, ignore_errors=True)
            print_color(Colors.RED, f"Removed notes directory: {notes_dir}")
        else:
            print_color(Colors.YELLOW, f"Notes directory not found: {notes_dir}")
    else:
        print_color(Colors.GREEN, "Preserved notes directory")
    
    print_color(Colors.GREEN, "Uninstallation complete!")
    print()
    print_color(Colors.BLUE, "=== Notes Location ===")
    notes_dir = os.environ.get("ECHO_NOTES_DIR", str(Path.home() / "Documents/notes/log"))
    print(f"Your notes are still available at: {notes_dir}")
    print()
    print_color(Colors.YELLOW, "If you want to completely remove Echo-Notes, you can now delete this directory:")
    print(script_dir)
    print()

if __name__ == "__main__":
    main()