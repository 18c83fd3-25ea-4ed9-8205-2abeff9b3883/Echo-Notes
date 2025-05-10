#!/usr/bin/env python3
"""
Echo-Notes Unified Installer
A simplified installer that works across platforms (Windows, macOS, Linux)
"""

import os
import sys
import shutil
import platform
import subprocess
import argparse
from pathlib import Path
import tempfile
import zipfile
import json

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

def check_python():
    """Check Python version"""
    if sys.version_info < (3, 7):
        print_color(Colors.RED, "Error: Python 3.7 or higher is required.")
        sys.exit(1)
    return True

def setup_venv(install_dir):
    """Set up virtual environment"""
    print_color(Colors.BLUE, "Setting up virtual environment...")
    
    venv_dir = install_dir / "echo_notes_venv"
    
    # Remove existing virtual environment if it's broken
    if venv_dir.exists():
        try:
            if detect_os() == "windows":
                subprocess.run([str(venv_dir / "Scripts/python"), "--version"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            else:
                subprocess.run([str(venv_dir / "bin/python"), "--version"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            print_color(Colors.YELLOW, "Existing virtual environment appears to be broken. Recreating...")
            shutil.rmtree(venv_dir)
    
    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print_color(Colors.BLUE, "Creating new virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        
        # Ensure Python executables have proper permissions
        if detect_os() != "windows":
            bin_dir = venv_dir / "bin"
            for executable in ["python", "python3", "pip", "pip3"]:
                exec_path = bin_dir / executable
                if exec_path.exists():
                    os.chmod(str(exec_path), 0o755)
        
        print_color(Colors.GREEN, "Created virtual environment")
    
    # Upgrade pip
    pip_cmd = str(venv_dir / ("Scripts/pip" if detect_os() == "windows" else "bin/pip"))
    subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
    
    # Install dependencies
    print_color(Colors.BLUE, "Installing dependencies...")
    subprocess.run([pip_cmd, "install", "requests", "python-dateutil", "PyQt6"], check=True)
    
    # Install the package in development mode
    os.chdir(install_dir)
    subprocess.run([pip_cmd, "install", "-e", "."], check=True)
    
    print_color(Colors.GREEN, "Dependencies installed successfully")
    return venv_dir

def create_desktop_shortcut(install_dir, venv_dir):
    """Create desktop shortcut based on platform"""
    os_type = detect_os()
    
    if os_type == "linux":
        create_linux_shortcut(install_dir, venv_dir)
    elif os_type == "macos":
        create_macos_shortcut(install_dir, venv_dir)
    elif os_type == "windows":
        create_windows_shortcut(install_dir, venv_dir)
    else:
        print_color(Colors.YELLOW, "Unknown operating system. Skipping desktop shortcut creation.")

def create_linux_shortcut(install_dir, venv_dir):
    """Create Linux desktop shortcut"""
    print_color(Colors.BLUE, "Creating Linux desktop shortcut...")
    
    home = Path.home()
    
    # Install the icon
    icons_dir = home / ".local/share/icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(install_dir / "Echo-Notes-Icon.png", icons_dir / "echo-notes.png")
    
    # Create symlink in ~/.local/bin
    bin_dir = home / ".local/bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    dashboard_symlink = bin_dir / "echo-notes-dashboard"
    if dashboard_symlink.exists() or dashboard_symlink.is_symlink():
        dashboard_symlink.unlink()
    
    dashboard_symlink.symlink_to(install_dir / "echo_notes_dashboard.py")
    os.chmod(install_dir / "echo_notes_dashboard.py", 0o755)
    
    # Create applications directory
    apps_dir = home / ".local/share/applications"
    apps_dir.mkdir(parents=True, exist_ok=True)
    
    # Create desktop file
    desktop_file = apps_dir / "echo-notes.desktop"
    with open(desktop_file, "w") as f:
        f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes
Comment=Monitor and control Echo-Notes daemon
Exec={venv_dir}/bin/python {install_dir}/echo_notes_dashboard.py
Icon={home}/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
""")
    
    # Make desktop file executable
    os.chmod(desktop_file, 0o755)
    
    # Create desktop icon if Desktop directory exists
    desktop_dir = home / "Desktop"
    if desktop_dir.exists():
        desktop_icon = desktop_dir / "Echo Notes.desktop"
        shutil.copy(desktop_file, desktop_icon)
        os.chmod(desktop_icon, 0o755)
    
    # Update desktop database if command exists
    try:
        subprocess.run(["update-desktop-database", str(apps_dir)], 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    except FileNotFoundError:
        pass
    
    print_color(Colors.GREEN, "Linux desktop shortcut created successfully")

def create_macos_shortcut(install_dir, venv_dir):
    """Create macOS application shortcut"""
    print_color(Colors.BLUE, "Creating macOS application shortcut...")
    
    home = Path.home()
    
    # Create app bundle
    app_dir = home / "Applications/Echo Notes Dashboard.app"
    os.makedirs(app_dir / "Contents/MacOS", exist_ok=True)
    os.makedirs(app_dir / "Contents/Resources", exist_ok=True)
    
    # Copy icon
    shutil.copy(install_dir / "Echo-Notes-Icon.png", app_dir / "Contents/Resources/echo-notes.png")
    
    # Create Info.plist
    with open(app_dir / "Contents/Info.plist", "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>echo-notes-launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.echo-notes.dashboard</string>
    <key>CFBundleName</key>
    <string>Echo Notes Dashboard</string>
    <key>CFBundleDisplayName</key>
    <string>Echo Notes Dashboard</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleIconFile</key>
    <string>echo-notes.png</string>
</dict>
</plist>
""")
    
    # Create launcher script
    with open(app_dir / "Contents/MacOS/echo-notes-launcher", "w") as f:
        f.write(f"""#!/bin/bash
# Echo Notes Launcher
"{venv_dir}/bin/python" "{install_dir}/echo_notes_dashboard.py"
""")
    
    # Make launcher executable
    os.chmod(app_dir / "Contents/MacOS/echo-notes-launcher", 0o755)
    
    # Create symlink in /usr/local/bin if it exists and is writable
    try:
        usr_local_bin = Path("/usr/local/bin")
        if usr_local_bin.exists() and os.access(usr_local_bin, os.W_OK):
            symlink_path = usr_local_bin / "echo-notes-dashboard"
            if symlink_path.exists() or symlink_path.is_symlink():
                symlink_path.unlink()
            symlink_path.symlink_to(install_dir / "echo_notes_dashboard.py")
            os.chmod(install_dir / "echo_notes_dashboard.py", 0o755)
            print_color(Colors.GREEN, f"Created symlink at {symlink_path}")
    except (PermissionError, OSError):
        print_color(Colors.YELLOW, "Note: Could not create symlink in /usr/local/bin (permission denied)")
    
    print_color(Colors.GREEN, "macOS application shortcut created successfully")

def create_windows_shortcut(install_dir, venv_dir):
    """Create Windows desktop shortcut"""
    print_color(Colors.BLUE, "Creating Windows desktop shortcut...")
    
    try:
        # Create a PowerShell script to create the shortcut
        ps_script = tempfile.NamedTemporaryFile(suffix=".ps1", delete=False)
        ps_script_path = Path(ps_script.name)
        
        with open(ps_script_path, "w") as f:
            f.write(f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\\Echo Notes Dashboard.lnk')
$Shortcut.TargetPath = '{venv_dir / "Scripts/pythonw.exe"}'
$Shortcut.Arguments = '"{install_dir / "echo_notes_dashboard.py"}"'
$Shortcut.WorkingDirectory = '{install_dir}'
$Shortcut.IconLocation = '{install_dir / "Echo-Notes-Icon.png"}'
$Shortcut.Save()
""")
        
        # Execute the PowerShell script
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script_path)], check=True)
        
        # Clean up the temporary script
        ps_script_path.unlink()
        
        print_color(Colors.GREEN, "Windows desktop shortcut created successfully")
    except Exception as e:
        print_color(Colors.RED, f"Error creating Windows shortcut: {e}")

def configure_app(install_dir):
    """Configure the application"""
    print_color(Colors.BLUE, "Configuring Echo-Notes...")
    
    # Create default configuration if needed
    config_file = install_dir / "shared/schedule_config.json"
    if not config_file.exists():
        with open(config_file, "w") as f:
            f.write("""{
    "processing_interval": 60,
    "summary_interval": 10080,
    "summary_day": 6,
    "summary_hour": 12,
    "daemon_enabled": true
}
""")
        print_color(Colors.GREEN, "Created default schedule configuration")
    
    # Ensure the notes directory exists
    notes_dir = os.environ.get("ECHO_NOTES_DIR", str(Path.home() / "Documents/notes/log"))
    os.makedirs(notes_dir, exist_ok=True)
    print_color(Colors.GREEN, f"Ensured notes directory exists: {notes_dir}")

def create_uninstaller(install_dir, venv_dir):
    """Create uninstaller script"""
    print_color(Colors.BLUE, "Creating uninstaller...")
    
    os_type = detect_os()
    
    if os_type == "windows":
        uninstaller_path = install_dir / "uninstall.bat"
        with open(uninstaller_path, "w") as f:
            f.write(f"""@echo off
echo ===== Echo-Notes Uninstaller =====
echo.

set INSTALL_DIR={install_dir}
set VENV_DIR={venv_dir}

echo Stopping Echo-Notes processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Echo-Notes*" > nul 2>&1
echo Processes stopped.

echo Removing desktop shortcut...
powershell -Command "Remove-Item -Path ([Environment]::GetFolderPath('Desktop') + '\\Echo Notes Dashboard.lnk') -Force -ErrorAction SilentlyContinue"
echo Desktop shortcut removed.

echo.
set /p KEEP_NOTES=Would you like to keep your notes? (Y/n): 
if /i "%KEEP_NOTES%"=="n" (
    echo Removing notes directory...
    set NOTES_DIR=%USERPROFILE%\\Documents\\notes\\log
    if defined ECHO_NOTES_DIR set NOTES_DIR=%ECHO_NOTES_DIR%
    rmdir /s /q "%NOTES_DIR%"
    echo Notes directory removed.
) else (
    echo Preserving notes directory.
)

echo.
echo Uninstallation complete!
echo If you want to completely remove Echo-Notes, you can now delete this directory:
echo %INSTALL_DIR%
echo.

pause
""")
    else:
        uninstaller_path = install_dir / "uninstall.sh"
        with open(uninstaller_path, "w") as f:
            f.write(f"""#!/bin/bash
# Echo-Notes Uninstaller

# Color codes for output
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
RED='\\033[0;31m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

echo -e "${{BLUE}}===== Echo-Notes Uninstaller =====${{NC}}"
echo ""

INSTALL_DIR="{install_dir}"
VENV_DIR="{venv_dir}"

# Stop running processes
echo -e "${{BLUE}}Stopping Echo-Notes processes...${{NC}}"
if [ -f "${{VENV_DIR}}/bin/echo-notes-daemon" ]; then
    "${{VENV_DIR}}/bin/echo-notes-daemon" --stop
fi
pkill -f "echo_notes_daemon.py" || true
pkill -f "echo_notes_dashboard.py" || true
echo -e "${{GREEN}}Processes stopped${{NC}}"

# OS-specific uninstallation
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo -e "${{BLUE}}Performing macOS-specific uninstallation...${{NC}}"
    rm -rf ~/Applications/"Echo Notes Dashboard.app"
    rm -f /usr/local/bin/echo-notes-dashboard
    echo -e "${{GREEN}}Removed application bundle and symlinks${{NC}}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo -e "${{BLUE}}Performing Linux-specific uninstallation...${{NC}}"
    rm -f ~/.local/share/applications/echo-notes.desktop
    rm -f ~/Desktop/"Echo Notes.desktop"
    rm -f ~/.local/share/icons/echo-notes.png
    rm -f ~/.local/bin/echo-notes-dashboard
    echo -e "${{GREEN}}Removed desktop shortcuts, icons, and symlinks${{NC}}"
fi

# Ask about notes
echo ""
read -p "Would you like to keep your notes? (Y/n): " KEEP_NOTES
if [[ "$KEEP_NOTES" =~ ^[Nn]$ ]]; then
    echo -e "${{RED}}Removing notes directory...${{NC}}"
    NOTES_DIR="${{ECHO_NOTES_DIR:-$HOME/Documents/notes/log}}"
    rm -rf "$NOTES_DIR"
    echo -e "${{RED}}Notes directory removed: $NOTES_DIR${{NC}}"
else
    echo -e "${{GREEN}}Preserving notes directory${{NC}}"
fi

echo ""
echo -e "${{GREEN}}Uninstallation complete!${{NC}}"
echo "If you want to completely remove Echo-Notes, you can now delete this directory:"
echo "$INSTALL_DIR"
echo ""
""")
        os.chmod(uninstaller_path, 0o755)
    
    print_color(Colors.GREEN, f"Uninstaller created at {uninstaller_path}")

def start_daemon(venv_dir):
    """Start the Echo-Notes daemon"""
    print_color(Colors.BLUE, "Starting Echo-Notes daemon...")
    
    try:
        if detect_os() == "windows":
            daemon_cmd = str(venv_dir / "Scripts/echo-notes-daemon")
        else:
            daemon_cmd = str(venv_dir / "bin/echo-notes-daemon")
        
        subprocess.run([daemon_cmd, "--daemon"], check=True)
        print_color(Colors.GREEN, "Echo-Notes daemon started successfully")
    except Exception as e:
        print_color(Colors.RED, f"Error starting daemon: {e}")

def main():
    """Main installation function"""
    parser = argparse.ArgumentParser(description="Echo-Notes Unified Installer")
    parser.add_argument("--no-shortcut", action="store_true", help="Skip desktop shortcut creation")
    parser.add_argument("--no-daemon", action="store_true", help="Skip starting the daemon")
    args = parser.parse_args()
    
    print_color(Colors.BLUE, "=== Echo-Notes Unified Installer ===")
    
    # Check Python version
    check_python()
    
    # Get installation directory
    install_dir = get_script_dir()
    print(f"Installation directory: {install_dir}")
    
    # Set up virtual environment
    venv_dir = setup_venv(install_dir)
    
    # Configure the application
    configure_app(install_dir)
    
    # Create desktop shortcut
    if not args.no_shortcut:
        create_desktop_shortcut(install_dir, venv_dir)
    else:
        print_color(Colors.YELLOW, "Skipping desktop shortcut creation as requested")
    
    # Create uninstaller
    create_uninstaller(install_dir, venv_dir)
    
    # Start the daemon
    if not args.no_daemon:
        start_daemon(venv_dir)
    else:
        print_color(Colors.YELLOW, "Skipping daemon startup as requested")
    
    print_color(Colors.GREEN, "Installation complete!")
    print("")
    print_color(Colors.BLUE, "=== Getting Started ===")
    print("1. Start the daemon: echo-notes-daemon --daemon")
    print("2. Launch the dashboard: echo-notes-dashboard")
    print("   Or use the desktop shortcut/icon created during installation")
    print("")
    print_color(Colors.BLUE, "=== Uninstallation ===")
    if detect_os() == "windows":
        print("To uninstall, run uninstall.bat in the Echo-Notes directory")
    else:
        print("To uninstall, run ./uninstall.sh in the Echo-Notes directory")
    print("")

if __name__ == "__main__":
    main()