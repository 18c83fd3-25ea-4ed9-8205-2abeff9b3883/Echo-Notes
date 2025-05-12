#!/usr/bin/env python3
"""
Echo-Notes macOS Installer
This module provides macOS-specific installation functionality for Echo-Notes.
"""

import os
import subprocess
import tempfile
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


def create_macos_app_bundle(install_dir, venv_path, app_name="Echo Notes Dashboard"):
    """
    Create a macOS application bundle (.app) for Echo Notes Dashboard.

    Args:
        install_dir (Path): Installation directory
        venv_path (Path): Virtual environment path
        app_name (str): Name of the application

    Returns:
        Path: Path to the created application bundle, or None if creation failed
    """
    print_color(Colors.BLUE, "Creating macOS application bundle...")

    try:
        # Get the user's Applications folder
        applications_dir = Path.home() / "Applications"
        app_dir = applications_dir / f"{app_name}.app"

        # Create the directory structure
        os.makedirs(app_dir / "Contents" / "MacOS", exist_ok=True)
        os.makedirs(app_dir / "Contents" / "Resources", exist_ok=True)

        # Copy the icon file
        icon_path = install_dir / "Echo-Notes-Icon.png"
        if icon_path.exists():
            resources_icon_path = app_dir / "Contents" / "Resources" / "echo-notes.png"
            shutil.copy(icon_path, resources_icon_path)
            print_color(Colors.GREEN, f"Copied icon to {resources_icon_path}")

        # Create the Info.plist file
        info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>echo-notes-launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.echo-notes.dashboard</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleDisplayName</key>
    <string>{app_name}</string>
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
"""

        with open(app_dir / "Contents" / "Info.plist", "w") as f:
            f.write(info_plist)

        # Create the launcher script that points to the actual executable in the venv
        launcher_script = f"""#!/bin/bash
# Launch Echo Notes Dashboard from the virtual environment
"{venv_path}/bin/python" "{install_dir}/echo_notes/dashboard.py"
"""

        launcher_path = app_dir / "Contents" / "MacOS" / "echo-notes-launcher"
        with open(launcher_path, "w") as f:
            f.write(launcher_script)

        # Make the launcher script executable
        os.chmod(launcher_path, 0o755)

        print_color(Colors.GREEN, f"Application bundle created at: {app_dir}")
        return app_dir

    except Exception as e:
        print_color(Colors.RED, f"Error creating macOS application bundle: {e}")
        return None


def create_symlinks(venv_path, install_dir):
    """
    Create symlinks in /usr/local/bin for Echo-Notes executables.

    Args:
        venv_path (Path): Virtual environment path
        install_dir (Path): Installation directory

    Returns:
        bool: True if symlinks were created successfully, False otherwise
    """
    print_color(Colors.BLUE, "Creating symlinks in /usr/local/bin...")

    try:
        # Check if /usr/local/bin exists and is writable
        bin_dir = Path("/usr/local/bin")
        if not bin_dir.exists():
            print_color(
                Colors.YELLOW,
                "/usr/local/bin does not exist. Skipping symlink creation.",
            )
            return False

        if not os.access(bin_dir, os.W_OK):
            print_color(
                Colors.YELLOW, "/usr/local/bin is not writable. Attempting with sudo..."
            )

            # Create a temporary script to create symlinks with sudo
            script = tempfile.NamedTemporaryFile(delete=False, suffix=".sh")
            script_path = Path(script.name)

            with open(script_path, "w") as f:
                f.write(
                    f"""#!/bin/bash
# Create symlinks for Echo-Notes executables
ln -sf "{venv_path}/bin/python" "{bin_dir}/echo-notes-python"
ln -sf "{install_dir}/echo_notes/dashboard.py" "{bin_dir}/echo-notes-dashboard"
ln -sf "{install_dir}/echo_notes/daemon.py" "{bin_dir}/echo-notes-daemon"
echo "Symlinks created in {bin_dir}"
"""
                )

            # Make the script executable
            os.chmod(script_path, 0o755)

            # Run the script with sudo
            print_color(Colors.YELLOW, "Please enter your password to create symlinks:")
            result = subprocess.run(["sudo", str(script_path)], check=False)

            # Clean up the temporary script
            os.unlink(script_path)

            if result.returncode != 0:
                print_color(Colors.RED, "Failed to create symlinks with sudo.")
                return False

            print_color(Colors.GREEN, "Symlinks created with sudo.")
            return True

        # If /usr/local/bin is writable, create symlinks directly
        os.symlink(venv_path / "bin" / "python", bin_dir / "echo-notes-python")
        os.symlink(
            install_dir / "echo_notes/dashboard.py", bin_dir / "echo-notes-dashboard"
        )
        os.symlink(install_dir / "echo_notes/daemon.py", bin_dir / "echo-notes-daemon")

        print_color(Colors.GREEN, "Symlinks created in /usr/local/bin")
        return True

    except Exception as e:
        print_color(Colors.RED, f"Error creating symlinks: {e}")
        print_color(Colors.YELLOW, "Continuing installation without symlinks.")
        return False


def setup_launchd_service(install_dir, venv_path):
    """
    Set up Echo-Notes daemon as a launchd service.

    Args:
        install_dir (Path): Installation directory
        venv_path (Path): Virtual environment path

    Returns:
        bool: True if service setup was successful, False otherwise
    """
    print_color(Colors.BLUE, "Setting up Echo-Notes daemon service...")

    try:
        # Create the launchd plist file
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.echo-notes.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>{venv_path}/bin/python</string>
        <string>{install_dir}/echo_notes/daemon.py</string>
        <string>--daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{install_dir}/daemon.log</string>
    <key>StandardErrorPath</key>
    <string>{install_dir}/daemon.err</string>
</dict>
</plist>
"""

        # Write the plist file to the user's LaunchAgents directory
        launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
        os.makedirs(launch_agents_dir, exist_ok=True)

        plist_path = launch_agents_dir / "com.echo-notes.daemon.plist"
        with open(plist_path, "w") as f:
            f.write(plist_content)

        # Load the service
        subprocess.run(["launchctl", "load", str(plist_path)], check=True)

        print_color(Colors.GREEN, "Echo-Notes daemon service set up and started")
        return True

    except Exception as e:
        print_color(Colors.RED, f"Error setting up launchd service: {e}")
        print_color(Colors.YELLOW, "You can still start the daemon manually using:")
        print(f'"{venv_path}/bin/python" "{install_dir}/echo_notes/daemon.py" --daemon')
        return False


def install_macos(install_dir=None, options=None):
    """
    Perform macOS-specific installation.

    Args:
        install_dir (Path, optional): Installation directory
        options (dict, optional): Installation options

    Returns:
        bool: True if installation was successful, False otherwise
    """
    if options is None:
        options = {}

    # Check Python version
    if not check_python_version():
        return False

    # Get installation directory if not provided
    if install_dir is None:
        install_dir = get_installation_directory()
    else:
        install_dir = Path(install_dir)

    print_color(Colors.BLUE, f"Installing Echo-Notes to {install_dir}...")

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

    # Create macOS application bundle
    if not options.get("no_app_bundle", False):
        app_bundle = create_macos_app_bundle(install_dir, venv_path)
        if not app_bundle:
            print_color(
                Colors.YELLOW,
                "Failed to create application bundle, continuing installation...",
            )
    else:
        print_color(Colors.YELLOW, "Skipping application bundle creation as requested")

    # Create symlinks
    if not options.get("no_symlinks", False):
        create_symlinks(venv_path, install_dir)
    else:
        print_color(Colors.YELLOW, "Skipping symlink creation as requested")

    # Set up launchd service
    if not options.get("no_service", False):
        setup_launchd_service(install_dir, venv_path)
    else:
        print_color(Colors.YELLOW, "Skipping service setup as requested")

    print_color(Colors.GREEN, "macOS installation completed successfully!")
    print("")
    print_color(Colors.BLUE, "=== Getting Started ===")
    print("1. The Echo-Notes daemon has been set up to start automatically at login")
    print("2. Launch the dashboard using the application in your Applications folder")
    print("3. You can also run the dashboard directly with:")
    print(f'   "{venv_path}/bin/python" "{install_dir}/echo_notes/dashboard.py"')
    print("")

    return True


if __name__ == "__main__":
    # This allows the module to be run directly for testing
    install_macos()
