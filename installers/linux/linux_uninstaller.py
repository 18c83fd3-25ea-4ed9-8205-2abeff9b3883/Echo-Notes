#!/usr/bin/env python3
"""
Echo-Notes Linux Uninstaller
This module provides Linux-specific uninstallation functionality for Echo-Notes.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Import common utilities
from ..common.installer_utils import Colors, print_color


def stop_running_processes():
    """
    Stop all running Echo-Notes processes.

    Returns:
        bool: True if processes were stopped successfully, False otherwise
    """
    print_color(Colors.BLUE, "Stopping Echo-Notes processes...")

    try:
        # Try to stop the systemd service if it exists
        try:
            subprocess.run(
                ["systemctl", "--user", "stop", "echo-notes.service"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["systemctl", "--user", "disable", "echo-notes.service"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass

        # Kill any remaining processes
        subprocess.run(
            ["pkill", "-f", "echo_notes/daemon.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["pkill", "-f", "echo_notes/dashboard.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print_color(Colors.GREEN, "Echo-Notes processes stopped")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error stopping processes: {e}")
        return False


def remove_desktop_shortcuts():
    """
    Remove desktop shortcuts and application menu entries.

    Returns:
        bool: True if shortcuts were removed successfully, False otherwise
    """
    print_color(
        Colors.BLUE, "Removing desktop shortcuts and application menu entries..."
    )

    try:
        # Remove desktop entry
        desktop_file = Path.home() / ".local/share/applications/echo-notes.desktop"
        if desktop_file.exists():
            os.unlink(desktop_file)
            print_color(Colors.GREEN, f"Removed application menu entry: {desktop_file}")

        # Remove desktop icon
        desktop_icon = Path.home() / "Desktop/Echo Notes.desktop"
        if desktop_icon.exists():
            os.unlink(desktop_icon)
            print_color(Colors.GREEN, f"Removed desktop icon: {desktop_icon}")

        # Remove icon
        icon_file = Path.home() / ".local/share/icons/echo-notes.png"
        if icon_file.exists():
            os.unlink(icon_file)
            print_color(Colors.GREEN, f"Removed icon: {icon_file}")

        # Update desktop database if command exists
        try:
            subprocess.run(
                [
                    "update-desktop-database",
                    str(Path.home() / ".local/share/applications"),
                ],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass

        print_color(Colors.GREEN, "Desktop shortcuts removed successfully")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing desktop shortcuts: {e}")
        return False


def remove_symlinks():
    """
    Remove Echo-Notes symlinks from ~/.local/bin.

    Returns:
        bool: True if removal was successful, False otherwise
    """
    print_color(Colors.BLUE, "Removing symlinks...")

    try:
        bin_dir = Path.home() / ".local/bin"
        symlinks = ["echo-notes-python", "echo-notes-dashboard", "echo-notes-daemon"]

        for symlink in symlinks:
            symlink_path = bin_dir / symlink
            if symlink_path.exists() or symlink_path.is_symlink():
                os.unlink(symlink_path)
                print_color(Colors.GREEN, f"Removed symlink: {symlink_path}")

        print_color(Colors.GREEN, "Symlinks removed")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing symlinks: {e}")
        return False


def remove_systemd_service():
    """
    Remove the Echo-Notes systemd service.

    Returns:
        bool: True if removal was successful, False otherwise
    """
    print_color(Colors.BLUE, "Removing systemd service...")

    try:
        # Stop and disable the service
        try:
            subprocess.run(
                ["systemctl", "--user", "stop", "echo-notes.service"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["systemctl", "--user", "disable", "echo-notes.service"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass

        # Remove service file
        service_file = Path.home() / ".config/systemd/user/echo-notes.service"
        if service_file.exists():
            os.unlink(service_file)
            print_color(Colors.GREEN, f"Removed service file: {service_file}")

            # Reload systemd
            try:
                subprocess.run(
                    ["systemctl", "--user", "daemon-reload"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass

        # Remove autostart entry
        autostart_file = Path.home() / ".config/autostart/echo-notes-daemon.desktop"
        if autostart_file.exists():
            os.unlink(autostart_file)
            print_color(Colors.GREEN, f"Removed autostart entry: {autostart_file}")

        print_color(Colors.GREEN, "Service configuration removed")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing service configuration: {e}")
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


def uninstall_linux(install_dir, options=None):
    """
    Perform Linux-specific uninstallation.

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

    # Remove desktop shortcuts
    remove_desktop_shortcuts()

    # Remove symlinks
    remove_symlinks()

    # Remove systemd service
    remove_systemd_service()

    # Remove virtual environment
    remove_virtual_environment(install_dir)

    # Remove user data if requested
    purge = options.get("purge", False)
    remove_user_data(purge)

    print_color(Colors.GREEN, "Linux uninstallation completed successfully!")
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
    uninstall_linux(install_dir, {"purge": purge})
