#!/usr/bin/env python3
"""
Echo-Notes Linux Installer
This module provides Linux-specific installation functionality for Echo-Notes.
"""

import os
import subprocess
import shutil
from pathlib import Path

# Import common utilities
from ..common.installer_utils import (
    Colors,
    print_color,
    check_python_version,
    create_virtual_environment,
    install_dependencies,
    configure_application,
    get_installation_directory,
)


def create_desktop_shortcuts(install_dir, venv_path):
    """
    Create Linux desktop shortcuts and application menu entries.

    Args:
        install_dir (Path): Installation directory
        venv_path (Path): Virtual environment path

    Returns:
        bool: True if shortcuts were created successfully, False otherwise
    """
    print_color(
        Colors.BLUE, "Creating desktop shortcuts and application menu entries..."
    )

    try:
        # Install the icon
        icons_dir = Path.home() / ".local/share/icons"
        os.makedirs(icons_dir, exist_ok=True)

        icon_path = install_dir / "Echo-Notes-Icon.png"
        if icon_path.exists():
            shutil.copy(icon_path, icons_dir / "echo-notes.png")
            print_color(Colors.GREEN, f"Installed icon to {icons_dir}/echo-notes.png")
        else:
            print_color(
                Colors.YELLOW, "Icon file not found, shortcuts will use default icon"
            )

        # Create applications directory if it doesn't exist
        applications_dir = Path.home() / ".local/share/applications"
        os.makedirs(applications_dir, exist_ok=True)

        # Create desktop entry file
        desktop_file_path = applications_dir / "echo-notes.desktop"
        with open(desktop_file_path, "w") as f:
            f.write(
                f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes
Comment=Monitor and control Echo-Notes daemon
Exec={venv_path}/bin/python {install_dir}/echo_notes/dashboard.py
Icon={Path.home()}/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
"""
            )

        # Make the desktop file executable
        os.chmod(desktop_file_path, 0o755)

        # Create desktop icon if Desktop directory exists
        desktop_dir = Path.home() / "Desktop"
        if desktop_dir.exists():
            desktop_icon_path = desktop_dir / "Echo Notes.desktop"
            shutil.copy(desktop_file_path, desktop_icon_path)
            os.chmod(desktop_icon_path, 0o755)
            print_color(Colors.GREEN, f"Created desktop icon at {desktop_icon_path}")

        # Update desktop database if command exists
        try:
            subprocess.run(
                ["update-desktop-database", str(applications_dir)],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass

        print_color(Colors.GREEN, "Desktop shortcuts created successfully")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error creating desktop shortcuts: {e}")
        return False


def create_symlinks(install_dir, venv_path):
    """
    Create symlinks in ~/.local/bin for Echo-Notes executables.

    Args:
        install_dir (Path): Installation directory
        venv_path (Path): Virtual environment path

    Returns:
        bool: True if symlinks were created successfully, False otherwise
    """
    print_color(Colors.BLUE, "Creating symlinks in ~/.local/bin...")

    try:
        # Create ~/.local/bin if it doesn't exist
        bin_dir = Path.home() / ".local/bin"
        os.makedirs(bin_dir, exist_ok=True)

        # Create symlinks
        symlinks = {
            "echo-notes-dashboard": install_dir / "echo_notes/dashboard.py",
            "echo-notes-daemon": install_dir / "echo_notes/daemon.py",
            "echo-notes-python": venv_path / "bin" / "python",
        }

        for name, target in symlinks.items():
            symlink_path = bin_dir / name

            # Remove existing symlink if it exists
            if symlink_path.exists() or symlink_path.is_symlink():
                os.unlink(symlink_path)

            # Create new symlink
            os.symlink(target, symlink_path)
            os.chmod(symlink_path, 0o755)
            print_color(Colors.GREEN, f"Created symlink: {symlink_path} -> {target}")

        # Add ~/.local/bin to PATH if not already there
        path_updated = False
        for shell_rc in [".bashrc", ".zshrc", ".profile"]:
            rc_file = Path.home() / shell_rc
            if rc_file.exists():
                with open(rc_file, "r") as f:
                    content = f.read()

                if (
                    'PATH="$HOME/.local/bin:$PATH"' not in content
                    and "PATH=$HOME/.local/bin:$PATH" not in content
                ):
                    with open(rc_file, "a") as f:
                        f.write(
                            '\n# Added by Echo-Notes installer\nexport PATH="$HOME/.local/bin:$PATH"\n'
                        )
                    path_updated = True

        if path_updated:
            print_color(
                Colors.YELLOW, "Added ~/.local/bin to PATH in shell configuration files"
            )
            print_color(
                Colors.YELLOW,
                "You may need to restart your terminal or run 'source ~/.bashrc' for changes to take effect",
            )

        print_color(Colors.GREEN, "Symlinks created successfully")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error creating symlinks: {e}")
        return False


def setup_systemd_service(install_dir, venv_path):
    """
    Set up Echo-Notes daemon as a systemd user service.

    Args:
        install_dir (Path): Installation directory
        venv_path (Path): Virtual environment path

    Returns:
        bool: True if service setup was successful, False otherwise
    """
    print_color(Colors.BLUE, "Setting up Echo-Notes daemon service...")

    try:
        # Create systemd user directory if it doesn't exist
        systemd_dir = Path.home() / ".config/systemd/user"
        os.makedirs(systemd_dir, exist_ok=True)

        # Create service file
        service_file_path = systemd_dir / "echo-notes.service"
        with open(service_file_path, "w") as f:
            f.write(
                f"""[Unit]
Description=Echo-Notes Daemon Service
After=network.target

[Service]
Type=simple
ExecStart={venv_path}/bin/python {install_dir}/echo_notes/daemon.py --daemon
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
"""
            )

        # Enable and start the service
        try:
            subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
            subprocess.run(
                ["systemctl", "--user", "enable", "echo-notes.service"], check=True
            )
            subprocess.run(
                ["systemctl", "--user", "start", "echo-notes.service"], check=True
            )

            print_color(Colors.GREEN, "Echo-Notes daemon service set up and started")
            return True
        except subprocess.SubprocessError as e:
            print_color(Colors.YELLOW, f"Could not set up systemd service: {e}")
            print_color(Colors.YELLOW, "Setting up alternative startup method...")

            # Create autostart directory if it doesn't exist
            autostart_dir = Path.home() / ".config/autostart"
            os.makedirs(autostart_dir, exist_ok=True)

            # Create autostart entry
            autostart_file_path = autostart_dir / "echo-notes-daemon.desktop"
            with open(autostart_file_path, "w") as f:
                f.write(
                    f"""[Desktop Entry]
Type=Application
Name=Echo Notes Daemon
Comment=Echo-Notes background service
Exec={venv_path}/bin/python {install_dir}/echo_notes/daemon.py --daemon
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
"""
                )

            # Start the daemon now
            try:
                subprocess.Popen(
                    [
                        f"{venv_path}/bin/python",
                        f"{install_dir}/echo_notes/daemon.py",
                        "--daemon",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                print_color(
                    Colors.GREEN, "Echo-Notes daemon started and set to run at login"
                )
                return True
            except Exception as e2:
                print_color(Colors.RED, f"Error starting daemon: {e2}")
                print_color(Colors.YELLOW, "You can start the daemon manually using:")
                print(
                    f"{venv_path}/bin/python {install_dir}/echo_notes/daemon.py --daemon"
                )
                return False
    except Exception as e:
        print_color(Colors.RED, f"Error setting up daemon service: {e}")
        print_color(Colors.YELLOW, "You can start the daemon manually using:")
        print(f"{venv_path}/bin/python {install_dir}/echo_notes/daemon.py --daemon")
        return False


def install_linux(install_dir=None, options=None):
    """
    Perform Linux-specific installation.

    Args:
        install_dir (Path, optional): Installation directory
        options (dict, optional): Installation options including:
            - dry_run (bool): If True, only simulate installation
            - no_shortcuts (bool): If True, skip desktop shortcuts creation
            - no_symlinks (bool): If True, skip symlink creation
            - no_service (bool): If True, skip service setup

    Returns:
        bool: True if installation was successful, False otherwise
    """
    if options is None:
        options = {}

    # Check for dry run mode
    dry_run = options.get("dry_run", False)
    if dry_run:
        print_color(
            Colors.YELLOW, "Performing dry run installation (simulation only)..."
        )

    # Check Python version
    if not check_python_version():
        return False

    # Get installation directory if not provided
    if install_dir is None:
        install_dir = get_installation_directory()
    else:
        install_dir = Path(install_dir)

    print_color(Colors.BLUE, f"Installing Echo-Notes to {install_dir}...")

    # If dry run, skip actual installation steps
    if dry_run:
        print_color(Colors.YELLOW, "Dry run: Would create virtual environment")
        print_color(Colors.YELLOW, "Dry run: Would install dependencies")
        print_color(Colors.YELLOW, "Dry run: Would configure application")

        if not options.get("no_shortcuts", False):
            print_color(Colors.YELLOW, "Dry run: Would create desktop shortcuts")

        if not options.get("no_symlinks", False):
            print_color(Colors.YELLOW, "Dry run: Would create symlinks")

        if not options.get("no_service", False):
            print_color(Colors.YELLOW, "Dry run: Would set up systemd service")

        print_color(Colors.GREEN, "Dry run completed successfully")
        return True

    # Create virtual environment
    venv_path = create_virtual_environment(install_dir)
    if not venv_path:
        return False

    # Install dependencies
    requirements_file = install_dir / "requirements.txt"
    if not install_dependencies(venv_path, requirements_file):
        return False

    # Configure application
    if not configure_application(install_dir):
        return False

    # Create desktop shortcuts
    if not options.get("no_shortcuts", False):
        create_desktop_shortcuts(install_dir, venv_path)
    else:
        print_color(Colors.YELLOW, "Skipping desktop shortcuts creation as requested")

    # Create symlinks
    if not options.get("no_symlinks", False):
        create_symlinks(install_dir, venv_path)
    else:
        print_color(Colors.YELLOW, "Skipping symlink creation as requested")

    # Set up systemd service
    if not options.get("no_service", False):
        setup_systemd_service(install_dir, venv_path)
    else:
        print_color(Colors.YELLOW, "Skipping service setup as requested")

    print_color(Colors.GREEN, "Linux installation completed successfully!")
    print("")
    print_color(Colors.BLUE, "=== Getting Started ===")
    print("1. The Echo-Notes daemon has been set up to start automatically at login")
    print("2. Launch the dashboard using the desktop shortcut or application menu")
    print("3. You can also run the dashboard directly with:")
    print(f"   {venv_path}/bin/python {install_dir}/echo_notes/dashboard.py")
    print("")

    return True


if __name__ == "__main__":
    # This allows the module to be run directly for testing
    install_linux()
