#!/usr/bin/env python3
"""
Echo-Notes Installer Migration Script

This script helps users transition from the old Echo-Notes installation
to the new modular installer framework.

It performs the following steps:
1. Detects the current Echo-Notes installation
2. Backs up configuration and data
3. Uninstalls the old version
4. Installs the new version using the appropriate platform-specific installer
5. Restores configuration and data
"""

import os
import sys
import shutil
import subprocess
import platform
import argparse
import tempfile
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("echo_notes_migration.log")
    ]
)
logger = logging.getLogger("echo_notes_migration")

# ANSI color codes for terminal output
class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color

def print_color(color, message):
    """Print a message with color."""
    print(f"{color}{message}{Colors.NC}")

def detect_os():
    """Detect the operating system."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def detect_installation():
    """
    Detect the current Echo-Notes installation.
    Returns a dictionary with installation details.
    """
    installation = {
        "found": False,
        "path": None,
        "version": "unknown",
        "notes_dir": None,
        "config_dir": None,
        "old_installer": False
    }
    
    # Check common installation paths
    potential_paths = [
        Path.home() / "Echo-Notes",
        Path.home() / "echo-notes",
        Path.home() / "Documents" / "Echo-Notes",
        Path("/opt/echo-notes"),
        Path("/usr/local/echo-notes")
    ]
    
    # On Windows, also check Program Files
    if detect_os() == "windows":
        potential_paths.extend([
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "Echo-Notes",
            Path(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")) / "Echo-Notes"
        ])
    
    # Check environment variable
    if "ECHO_APP_DIR" in os.environ:
        potential_paths.insert(0, Path(os.environ["ECHO_APP_DIR"]))
    
    # Check each path
    for path in potential_paths:
        if (path / "echo_notes_dashboard.py").exists():
            installation["found"] = True
            installation["path"] = path
            
            # Check if it's an old installation
            if (path / "echo_notes_installer.py").exists() and not (path / "installers").exists():
                installation["old_installer"] = True
            
            # Try to determine version
            try:
                with open(path / "CHANGELOG.md", "r") as f:
                    first_line = f.readline().strip()
                    if "version" in first_line.lower():
                        installation["version"] = first_line.split()[-1]
            except:
                pass
            
            break
    
    # Find notes directory
    if installation["found"]:
        # Check environment variable
        if "ECHO_NOTES_DIR" in os.environ:
            notes_dir = Path(os.environ["ECHO_NOTES_DIR"])
            if notes_dir.exists():
                installation["notes_dir"] = notes_dir
        
        # Check default locations
        if not installation["notes_dir"]:
            potential_notes_dirs = [
                Path.home() / "Documents" / "notes" / "log",
                Path.home() / "notes" / "log",
                installation["path"] / "notes" / "log"
            ]
            
            for path in potential_notes_dirs:
                if path.exists() and path.is_dir():
                    installation["notes_dir"] = path
                    break
        
        # Find config directory
        os_type = detect_os()
        if os_type == "windows":
            config_dir = Path(os.environ.get("APPDATA", "")) / "echo-notes"
        elif os_type == "macos":
            config_dir = Path.home() / "Library" / "Application Support" / "echo-notes"
        else:  # Linux
            config_dir = Path.home() / ".config" / "echo-notes"
        
        if config_dir.exists():
            installation["config_dir"] = config_dir
    
    return installation

def backup_data(installation):
    """
    Back up configuration and data.
    Returns the backup directory path.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"echo_notes_backup_{timestamp}")
    backup_dir.mkdir(exist_ok=True)
    
    logger.info(f"Creating backup in {backup_dir}")
    
    # Back up configuration
    if installation["config_dir"]:
        config_backup = backup_dir / "config"
        shutil.copytree(installation["config_dir"], config_backup)
        logger.info(f"Configuration backed up to {config_backup}")
    
    # Back up notes
    if installation["notes_dir"]:
        notes_backup = backup_dir / "notes"
        shutil.copytree(installation["notes_dir"], notes_backup)
        logger.info(f"Notes backed up to {notes_backup}")
    
    # Save installation details
    with open(backup_dir / "installation_details.txt", "w") as f:
        f.write(f"Installation path: {installation['path']}\n")
        f.write(f"Version: {installation['version']}\n")
        f.write(f"Notes directory: {installation['notes_dir']}\n")
        f.write(f"Config directory: {installation['config_dir']}\n")
        f.write(f"Old installer: {installation['old_installer']}\n")
        f.write(f"Backup created: {timestamp}\n")
    
    return backup_dir

def uninstall_old_version(installation):
    """
    Uninstall the old version of Echo-Notes.
    Returns True if successful, False otherwise.
    """
    logger.info("Uninstalling old version of Echo-Notes")
    
    os_type = detect_os()
    success = False
    
    try:
        if os_type == "windows":
            if (installation["path"] / "uninstall.bat").exists():
                cmd = [str(installation["path"] / "uninstall.bat"), "--keep-config"]
                subprocess.run(cmd, check=True)
                success = True
            else:
                logger.warning("Uninstall script not found")
        else:  # macOS or Linux
            if (installation["path"] / "uninstall.sh").exists():
                cmd = ["bash", str(installation["path"] / "uninstall.sh"), "--keep-config"]
                subprocess.run(cmd, check=True)
                success = True
            else:
                logger.warning("Uninstall script not found")
    except subprocess.SubprocessError as e:
        logger.error(f"Error during uninstallation: {e}")
        return False
    
    return success

def install_new_version(installation, backup_dir):
    """
    Install the new version of Echo-Notes using the appropriate platform-specific installer.
    Returns True if successful, False otherwise.
    """
    logger.info("Installing new version of Echo-Notes")
    
    os_type = detect_os()
    install_dir = installation["path"]
    success = False
    
    # Create a temporary directory for the new installer
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Clone or download the repository
        try:
            print_color(Colors.BLUE, "Downloading Echo-Notes repository...")
            subprocess.run(
                ["git", "clone", "https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes.git", str(temp_path)],
                check=True
            )
        except subprocess.SubprocessError:
            try:
                # Fallback to downloading a zip file
                import urllib.request
                import zipfile
                
                print_color(Colors.YELLOW, "Git clone failed, downloading zip file...")
                zip_path = temp_path / "echo-notes.zip"
                urllib.request.urlretrieve(
                    "https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/archive/main.zip",
                    zip_path
                )
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                # Find the extracted directory
                for item in temp_path.iterdir():
                    if item.is_dir() and "Echo-Notes" in item.name:
                        temp_path = item
                        break
            except Exception as e:
                logger.error(f"Failed to download repository: {e}")
                return False
        
        # Run the appropriate installer
        try:
            if os_type == "windows":
                installer_path = temp_path / "installers" / "install_windows.py"
                cmd = [sys.executable, str(installer_path), "install", "--install-dir", str(install_dir)]
                subprocess.run(cmd, check=True)
                success = True
            elif os_type == "macos":
                installer_path = temp_path / "installers" / "install_macos.sh"
                os.chmod(installer_path, 0o755)  # Make executable
                cmd = [str(installer_path), "--install-dir", str(install_dir)]
                subprocess.run(cmd, check=True)
                success = True
            elif os_type == "linux":
                installer_path = temp_path / "installers" / "install_linux.sh"
                os.chmod(installer_path, 0o755)  # Make executable
                cmd = [str(installer_path), "--install-dir", str(install_dir)]
                subprocess.run(cmd, check=True)
                success = True
            else:
                logger.error(f"Unsupported OS: {os_type}")
                return False
        except subprocess.SubprocessError as e:
            logger.error(f"Error during installation: {e}")
            return False
    
    return success

def restore_configuration(installation, backup_dir):
    """
    Restore configuration and data from backup.
    Returns True if successful, False otherwise.
    """
    logger.info("Restoring configuration and data")
    
    try:
        # Restore configuration
        config_backup = backup_dir / "config"
        if config_backup.exists() and installation["config_dir"]:
            # Only copy files that don't exist in the new installation
            for src_path in config_backup.rglob("*"):
                if src_path.is_file():
                    rel_path = src_path.relative_to(config_backup)
                    dst_path = installation["config_dir"] / rel_path
                    
                    if not dst_path.exists():
                        dst_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_path, dst_path)
                        logger.info(f"Restored {rel_path}")
        
        # Restore environment variables
        with open(backup_dir / "installation_details.txt", "r") as f:
            details = f.read()
            
            # Extract notes directory
            if "Notes directory:" in details and not os.environ.get("ECHO_NOTES_DIR"):
                for line in details.split("\n"):
                    if line.startswith("Notes directory:"):
                        notes_dir = line.split(":", 1)[1].strip()
                        if notes_dir != "None" and Path(notes_dir).exists():
                            print_color(Colors.YELLOW, f"Please set ECHO_NOTES_DIR environment variable to: {notes_dir}")
                            break
    except Exception as e:
        logger.error(f"Error restoring configuration: {e}")
        return False
    
    return True

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Echo-Notes Installer Migration Script")
    parser.add_argument("--verbose", action="store_true", help="Show verbose output")
    parser.add_argument("--force", action="store_true", help="Force migration even if no old installation is detected")
    parser.add_argument("--skip-backup", action="store_true", help="Skip backing up data")
    parser.add_argument("--skip-uninstall", action="store_true", help="Skip uninstalling old version")
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    print_color(Colors.BLUE, "===== Echo-Notes Installer Migration =====")
    print("")
    
    # Detect OS
    os_type = detect_os()
    print_color(Colors.BLUE, f"Detected OS: {os_type}")
    
    if os_type == "unknown":
        print_color(Colors.RED, "Error: Unsupported operating system")
        return 1
    
    # Detect current installation
    print_color(Colors.BLUE, "Detecting current Echo-Notes installation...")
    installation = detect_installation()
    
    if not installation["found"] and not args.force:
        print_color(Colors.RED, "Error: Echo-Notes installation not found")
        print_color(Colors.YELLOW, "If you want to proceed anyway, use the --force option")
        return 1
    
    if installation["found"]:
        print_color(Colors.GREEN, f"Found Echo-Notes installation at: {installation['path']}")
        print_color(Colors.GREEN, f"Version: {installation['version']}")
        
        if installation["notes_dir"]:
            print_color(Colors.GREEN, f"Notes directory: {installation['notes_dir']}")
        
        if installation["config_dir"]:
            print_color(Colors.GREEN, f"Configuration directory: {installation['config_dir']}")
        
        if not installation["old_installer"]:
            print_color(Colors.YELLOW, "This installation already uses the new installer framework")
            print_color(Colors.YELLOW, "Do you want to continue anyway? (y/N)")
            response = input().strip().lower()
            if response != "y":
                print_color(Colors.BLUE, "Migration cancelled")
                return 0
    
    # Back up data
    if not args.skip_backup:
        print_color(Colors.BLUE, "Backing up configuration and data...")
        backup_dir = backup_data(installation)
        print_color(Colors.GREEN, f"Backup created in: {backup_dir}")
    else:
        backup_dir = None
        print_color(Colors.YELLOW, "Skipping backup as requested")
    
    # Uninstall old version
    if not args.skip_uninstall and installation["found"]:
        print_color(Colors.BLUE, "Uninstalling old version...")
        if uninstall_old_version(installation):
            print_color(Colors.GREEN, "Old version uninstalled successfully")
        else:
            print_color(Colors.RED, "Failed to uninstall old version")
            print_color(Colors.YELLOW, "Do you want to continue anyway? (y/N)")
            response = input().strip().lower()
            if response != "y":
                print_color(Colors.BLUE, "Migration cancelled")
                return 1
    elif args.skip_uninstall:
        print_color(Colors.YELLOW, "Skipping uninstallation as requested")
    
    # Install new version
    print_color(Colors.BLUE, "Installing new version...")
    if install_new_version(installation, backup_dir):
        print_color(Colors.GREEN, "New version installed successfully")
    else:
        print_color(Colors.RED, "Failed to install new version")
        return 1
    
    # Restore configuration
    if backup_dir and not args.skip_backup:
        print_color(Colors.BLUE, "Restoring configuration...")
        if restore_configuration(installation, backup_dir):
            print_color(Colors.GREEN, "Configuration restored successfully")
        else:
            print_color(Colors.YELLOW, "Some issues occurred during configuration restoration")
            print_color(Colors.YELLOW, f"Please check the backup directory: {backup_dir}")
    
    print("")
    print_color(Colors.GREEN, "===== Migration Completed Successfully =====")
    print_color(Colors.GREEN, "Echo-Notes has been migrated to the new installer framework")
    print("")
    print_color(Colors.BLUE, "Next steps:")
    print_color(Colors.BLUE, "1. Verify that Echo-Notes is working correctly")
    print_color(Colors.BLUE, "2. Check that your notes are accessible")
    print_color(Colors.BLUE, "3. Start the Echo-Notes daemon if needed")
    print("")
    print_color(Colors.YELLOW, "For more information, see MIGRATION.md")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())