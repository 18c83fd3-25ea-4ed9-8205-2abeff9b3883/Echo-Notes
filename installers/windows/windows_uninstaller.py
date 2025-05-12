#!/usr/bin/env python3
"""
Echo-Notes Windows Uninstaller
This module provides Windows-specific uninstallation functionality for Echo-Notes.
"""

import os
import sys
import subprocess
import tempfile
import winreg
import ctypes
from pathlib import Path
import shutil

# Import common utilities
from ..common.installer_utils import Colors, print_color


def is_admin():
    """
    Check if the script is running with administrator privileges.

    Returns:
        bool: True if running as admin, False otherwise
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def stop_running_processes():
    """
    Stop all running Echo-Notes processes.

    Returns:
        bool: True if processes were stopped successfully, False otherwise
    """
    print_color(Colors.BLUE, "Stopping Echo-Notes processes...")

    try:
        # Try to stop the daemon gracefully first
        subprocess.run(
            [
                "taskkill",
                "/F",
                "/IM",
                "python.exe",
                "/FI",
                "WINDOWTITLE eq Echo-Notes*",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Kill any remaining Python processes that might be running Echo-Notes
        subprocess.run(
            [
                "taskkill",
                "/F",
                "/IM",
                "pythonw.exe",
                "/FI",
                "WINDOWTITLE eq Echo-Notes*",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print_color(Colors.GREEN, "Echo-Notes processes stopped")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error stopping processes: {e}")
        return False


def remove_shortcuts():
    """
    Remove desktop shortcuts and Start Menu entries.

    Returns:
        bool: True if shortcuts were removed successfully, False otherwise
    """
    print_color(Colors.BLUE, "Removing shortcuts...")

    try:
        # Create a PowerShell script to remove shortcuts
        ps_script = tempfile.NamedTemporaryFile(suffix=".ps1", delete=False)
        ps_script_path = Path(ps_script.name)

        with open(ps_script_path, "w") as f:
            f.write(
                """
# Remove desktop shortcut
$desktopShortcut = [Environment]::GetFolderPath('Desktop') + '\\Echo Notes Dashboard.lnk'
if (Test-Path $desktopShortcut) {
    Remove-Item -Path $desktopShortcut -Force
}

# Remove Start Menu shortcuts
$startMenuFolder = [Environment]::GetFolderPath('StartMenu') + '\\Programs\\Echo Notes'
if (Test-Path $startMenuFolder) {
    Remove-Item -Path $startMenuFolder -Recurse -Force
}
"""
            )

        # Execute the PowerShell script
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script_path)],
            check=True,
        )

        # Clean up the temporary script
        ps_script_path.unlink()

        print_color(Colors.GREEN, "Shortcuts removed successfully")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing shortcuts: {e}")
        return False


def remove_scheduled_task():
    """
    Remove the Echo-Notes daemon scheduled task.

    Returns:
        bool: True if task was removed successfully, False otherwise
    """
    print_color(Colors.BLUE, "Removing scheduled task...")

    try:
        # Delete the scheduled task
        subprocess.run(
            ["schtasks", "/delete", "/tn", "EchoNotesDaemon", "/f"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print_color(Colors.GREEN, "Scheduled task removed")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing scheduled task: {e}")
        return False


def unregister_uninstaller():
    """
    Remove the uninstaller from Windows Add/Remove Programs.

    Returns:
        bool: True if unregistration was successful, False otherwise
    """
    print_color(Colors.BLUE, "Unregistering from Add/Remove Programs...")

    try:
        # Try to delete from HKCU first (non-admin)
        try:
            winreg.DeleteKey(
                winreg.HKEY_CURRENT_USER,
                "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\EchoNotes",
            )
            print_color(Colors.GREEN, "Unregistered from Add/Remove Programs (user)")
            return True
        except FileNotFoundError:
            # Key doesn't exist in HKCU, try HKLM
            pass
        except Exception as e:
            print_color(Colors.YELLOW, f"Warning: Could not unregister from HKCU: {e}")

        # Try to delete from HKLM (requires admin)
        if is_admin():
            try:
                winreg.DeleteKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\EchoNotes",
                )
                print_color(
                    Colors.GREEN, "Unregistered from Add/Remove Programs (system)"
                )
                return True
            except FileNotFoundError:
                print_color(Colors.YELLOW, "Registry key not found in HKLM")
            except Exception as e:
                print_color(Colors.RED, f"Error unregistering from HKLM: {e}")
        else:
            # Try with administrator privileges
            print_color(
                Colors.YELLOW,
                "Attempting to unregister with administrator privileges...",
            )

            # Create a temporary script to unregister
            reg_script = tempfile.NamedTemporaryFile(suffix=".ps1", delete=False)
            reg_script_path = Path(reg_script.name)

            with open(reg_script_path, "w") as f:
                f.write(
                    """
$regPath = 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\EchoNotes'
if (Test-Path $regPath) {
    Remove-Item -Path $regPath -Force
}
"""
                )

            # Execute the PowerShell script with administrator privileges
            try:
                subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        f"Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File {reg_script_path}' -Verb RunAs -Wait",
                    ],
                    check=True,
                )

                # Clean up the temporary script
                reg_script_path.unlink()

                print_color(
                    Colors.GREEN, "Unregistered from Add/Remove Programs (system)"
                )
                return True
            except Exception as e2:
                print_color(
                    Colors.RED,
                    f"Error unregistering with administrator privileges: {e2}",
                )
                reg_script_path.unlink()

        print_color(
            Colors.YELLOW, "Could not fully unregister from Add/Remove Programs"
        )
        return False
    except Exception as e:
        print_color(Colors.RED, f"Error unregistering: {e}")
        return False


def remove_virtual_environment(install_dir):
    """
    Remove the Python virtual environment.

    Args:
        install_dir (Path): Installation directory

    Returns:
        bool: True if removal was successful, False otherwise
    """
    print_color(Colors.BLUE, "Removing virtual environment...")

    venv_path = install_dir / "echo_notes_venv"
    if not venv_path.exists():
        print_color(Colors.YELLOW, "Virtual environment not found")
        return True

    try:
        shutil.rmtree(venv_path)
        print_color(Colors.GREEN, "Virtual environment removed")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing virtual environment: {e}")
        return False


def remove_user_data(purge=False):
    """
    Remove user data if requested.

    Args:
        purge (bool): Whether to remove user notes

    Returns:
        bool: True if removal was successful, False otherwise
    """
    if not purge:
        print_color(Colors.YELLOW, "Preserving user notes")
        return True

    print_color(Colors.RED, "Removing user notes...")

    try:
        # Determine notes directory
        notes_dir = os.environ.get("ECHO_NOTES_DIR")
        if not notes_dir:
            notes_dir = Path.home() / "Documents/notes/log"
        else:
            notes_dir = Path(notes_dir)

        if notes_dir.exists():
            shutil.rmtree(notes_dir)
            print_color(Colors.RED, f"Removed notes directory: {notes_dir}")
        else:
            print_color(Colors.YELLOW, f"Notes directory not found: {notes_dir}")

        return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing user data: {e}")
        return False


def uninstall_windows(install_dir, options=None):
    """
    Perform Windows-specific uninstallation.

    Args:
        install_dir (Path): Installation directory
        options (dict, optional): Uninstallation options

    Returns:
        bool: True if uninstallation was successful, False otherwise
    """
    if options is None:
        options = {}

    install_dir = Path(install_dir)
    print_color(Colors.BLUE, f"Uninstalling Echo-Notes from {install_dir}...")

    # Stop running processes
    stop_running_processes()

    # Remove shortcuts
    remove_shortcuts()

    # Remove scheduled task
    remove_scheduled_task()

    # Unregister uninstaller
    unregister_uninstaller()

    # Remove virtual environment
    remove_virtual_environment(install_dir)

    # Remove user data if requested
    purge = options.get("purge", False)
    remove_user_data(purge)

    print_color(Colors.GREEN, "Windows uninstallation completed successfully!")
    print("")
    if not purge:
        print_color(Colors.BLUE, "=== Notes Location ===")
        notes_dir = os.environ.get(
            "ECHO_NOTES_DIR", str(Path.home() / "Documents/notes/log")
        )
        print(f"Your notes are still available at: {notes_dir}")
        print("")

    print_color(
        Colors.YELLOW,
        "To complete the uninstallation, you can now delete the Echo-Notes directory:",
    )
    print(f"{install_dir}")
    print("")

    return True


if __name__ == "__main__":
    # This allows the module to be run directly for testing
    if len(sys.argv) > 1:
        install_dir = Path(sys.argv[1])
    else:
        install_dir = Path.home() / "Echo-Notes"

    purge = "--purge" in sys.argv
    uninstall_windows(install_dir, {"purge": purge})
