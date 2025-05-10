#!/usr/bin/env python3
"""
Echo-Notes One-Click Installer
This script downloads and installs Echo-Notes with a single command.
"""

import os
import sys
import shutil
import platform
import subprocess
import tempfile
from pathlib import Path
import urllib.request
import zipfile
import io

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

def check_python():
    """Check Python version"""
    if sys.version_info < (3, 7):
        print_color(Colors.RED, "Error: Python 3.7 or higher is required.")
        sys.exit(1)
    return True

def download_echo_notes():
    """Download Echo-Notes from GitHub"""
    print_color(Colors.BLUE, "Downloading Echo-Notes...")
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Using temporary directory: {temp_dir}")
    
    try:
        # Download the latest version from GitHub
        url = "https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/archive/refs/heads/main.zip"
        print_color(Colors.YELLOW, f"Downloading from: {url}")
        
        with urllib.request.urlopen(url) as response:
            zip_data = response.read()
        
        # Extract the ZIP file
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the extracted directory
        extracted_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))]
        if not extracted_dirs:
            print_color(Colors.RED, "Error: Could not find extracted directory.")
            sys.exit(1)
        
        extracted_dir = os.path.join(temp_dir, extracted_dirs[0])
        print_color(Colors.GREEN, f"Downloaded and extracted to: {extracted_dir}")
        
        return extracted_dir
    except Exception as e:
        print_color(Colors.RED, f"Error downloading Echo-Notes: {e}")
        sys.exit(1)

def install_echo_notes(source_dir):
    """Install Echo-Notes"""
    print_color(Colors.BLUE, "Installing Echo-Notes...")
    
    # Determine installation directory
    home_dir = Path.home()
    install_dir = home_dir / "Echo-Notes"
    
    # Ask user for installation directory
    print(f"Default installation directory: {install_dir}")
    custom_dir = input("Press Enter to use default or specify a different directory: ").strip()
    if custom_dir:
        install_dir = Path(custom_dir)
    
    # Create installation directory if it doesn't exist
    os.makedirs(install_dir, exist_ok=True)
    
    # Copy files to installation directory
    print_color(Colors.YELLOW, f"Copying files to: {install_dir}")
    for item in os.listdir(source_dir):
        src = os.path.join(source_dir, item)
        dst = os.path.join(install_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
    
    # Run the installer
    print_color(Colors.BLUE, "Running Echo-Notes installer...")
    installer_script = os.path.join(install_dir, "echo_notes_installer.py")
    
    if not os.path.exists(installer_script):
        print_color(Colors.RED, f"Error: Installer script not found at {installer_script}")
        sys.exit(1)
    
    # Make the installer executable
    os.chmod(installer_script, 0o755)
    
    # Run the installer
    os.chdir(install_dir)
    subprocess.run([sys.executable, installer_script], check=True)
    
    print_color(Colors.GREEN, "Echo-Notes installed successfully!")
    return install_dir

def main():
    """Main function"""
    print_color(Colors.BLUE, "=== Echo-Notes One-Click Installer ===")
    
    # Check Python version
    check_python()
    
    # Download Echo-Notes
    source_dir = download_echo_notes()
    
    # Install Echo-Notes
    install_dir = install_echo_notes(source_dir)
    
    # Clean up temporary files
    print_color(Colors.YELLOW, "Cleaning up temporary files...")
    shutil.rmtree(os.path.dirname(source_dir), ignore_errors=True)
    
    print_color(Colors.GREEN, "Installation complete!")
    print("")
    print_color(Colors.BLUE, "=== Getting Started ===")
    print(f"Echo-Notes is installed at: {install_dir}")
    print("You can launch Echo-Notes using the desktop shortcut or by running:")
    print("  echo-notes-dashboard")
    print("")
    print_color(Colors.BLUE, "=== Uninstallation ===")
    if platform.system().lower() == "windows":
        print(f"To uninstall, run: {install_dir}\\uninstall.bat")
    else:
        print(f"To uninstall, run: {install_dir}/uninstall.sh")
    print("")

if __name__ == "__main__":
    main()