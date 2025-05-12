#!/usr/bin/env python3
"""
Echo-Notes macOS Uninstaller
This module provides macOS-specific uninstallation functionality for Echo-Notes.
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
        # Try to stop the daemon gracefully through launchctl
        subprocess.run(
            [
                "launchctl",
                "unload",
                str(Path.home() / "Library/LaunchAgents/com.echo-notes.daemon.plist"),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Kill any remaining processes
        subprocess.run(
            ["pkill", "-f", "echo_notes_daemon.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["pkill", "-f", "echo_notes_dashboard.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print_color(Colors.GREEN, "Echo-Notes processes stopped")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error stopping processes: {e}")
        return False


def remove_application_bundle():
    """
    Remove the Echo Notes Dashboard application bundle from the Applications folder.

    Returns:
        bool: True if removal was successful, False otherwise
    """
    print_color(Colors.BLUE, "Removing application bundle...")

    try:
        app_path = Path.home() / "Applications/Echo Notes Dashboard.app"
        if app_path.exists():
            shutil.rmtree(app_path)
            print_color(Colors.GREEN, f"Removed application bundle: {app_path}")
            return True
        else:
            print_color(Colors.YELLOW, "Application bundle not found")
            return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing application bundle: {e}")
        return False


def remove_symlinks():
    """
    Remove Echo-Notes symlinks from /usr/local/bin.

    Returns:
        bool: True if removal was successful, False otherwise
    """
    print_color(Colors.BLUE, "Removing symlinks...")

    try:
        bin_dir = Path("/usr/local/bin")
        symlinks = ["echo-notes-python", "echo-notes-dashboard", "echo-notes-daemon"]

        for symlink in symlinks:
            symlink_path = bin_dir / symlink
            if symlink_path.exists() or symlink_path.is_symlink():
                # Check if we have write permission
                if os.access(bin_dir, os.W_OK):
                    os.unlink(symlink_path)
                    print_color(Colors.GREEN, f"Removed symlink: {symlink_path}")
                else:
                    # Try with sudo
                    print_color(
                        Colors.YELLOW, f"Need sudo to remove symlink: {symlink_path}"
                    )
                    subprocess.run(["sudo", "rm", "-f", str(symlink_path)], check=False)

        print_color(Colors.GREEN, "Symlinks removed")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing symlinks: {e}")
        return False


def remove_launchd_service():
    """
    Remove the Echo-Notes launchd service.

    Returns:
        bool: True if removal was successful, False otherwise
    """
    print_color(Colors.BLUE, "Removing launchd service...")

    try:
        plist_path = Path.home() / "Library/LaunchAgents/com.echo-notes.daemon.plist"

        if plist_path.exists():
            # Unload the service first
            subprocess.run(
                ["launchctl", "unload", str(plist_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # Remove the plist file
            os.unlink(plist_path)
            print_color(Colors.GREEN, f"Removed launchd service: {plist_path}")
        else:
            print_color(Colors.YELLOW, "Launchd service not found")

        return True
    except Exception as e:
        print_color(Colors.RED, f"Error removing launchd service: {e}")
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


def uninstall_macos(install_dir, options=None):
    """
    Perform macOS-specific uninstallation.

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

    # Remove application bundle
    remove_application_bundle()

    # Remove symlinks
    remove_symlinks()

    # Remove launchd service
    remove_launchd_service()

    # Remove virtual environment
    remove_virtual_environment(install_dir)

    # Remove user data if requested
    purge = options.get("purge", False)
    remove_user_data(purge)

    print_color(Colors.GREEN, "macOS uninstallation completed successfully!")
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
    uninstall_macos(install_dir, {"purge": purge})
