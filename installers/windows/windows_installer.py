#!/usr/bin/env python3
"""
Echo-Notes Windows Installer
This module provides Windows-specific installation functionality for Echo-Notes.
"""

import sys
import subprocess
import tempfile
import winreg
import ctypes
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


def create_windows_shortcut(
    install_dir, venv_path, shortcut_name="Echo Notes Dashboard"
):
    """
    Create a Windows desktop shortcut.

    Args:
        install_dir (Path): Installation directory
        venv_path (Path): Virtual environment path
        shortcut_name (str): Name of the shortcut

    Returns:
        bool: True if shortcut was created successfully, False otherwise
    """
    print_color(Colors.BLUE, "Creating Windows desktop shortcut...")

    try:
        # Create a PowerShell script to create the shortcut
        ps_script = tempfile.NamedTemporaryFile(suffix=".ps1", delete=False)
        ps_script_path = Path(ps_script.name)

        with open(ps_script_path, "w") as f:
            f.write(
                f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\\{shortcut_name}.lnk')
$Shortcut.TargetPath = '{venv_path / "Scripts/pythonw.exe"}'
$Shortcut.Arguments = '"{install_dir / "echo_notes/dashboard.py"}"'
$Shortcut.WorkingDirectory = '{install_dir}'
$Shortcut.IconLocation = '{install_dir / "Echo-Notes-Icon.png"}'
$Shortcut.Save()

# Create Start Menu shortcut
$StartMenuPath = [Environment]::GetFolderPath('StartMenu') + '\\Programs\\Echo Notes'
if (!(Test-Path $StartMenuPath)) {{
    New-Item -Path $StartMenuPath -ItemType Directory -Force
}}
$StartMenuShortcut = $WshShell.CreateShortcut("$StartMenuPath\\{shortcut_name}.lnk")
$StartMenuShortcut.TargetPath = '{venv_path / "Scripts/pythonw.exe"}'
$StartMenuShortcut.Arguments = '"{install_dir / "echo_notes/dashboard.py"}"'
$StartMenuShortcut.WorkingDirectory = '{install_dir}'
$StartMenuShortcut.IconLocation = '{install_dir / "Echo-Notes-Icon.png"}'
$StartMenuShortcut.Save()
"""
            )

        # Execute the PowerShell script
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script_path)],
            check=True,
        )

        # Clean up the temporary script
        ps_script_path.unlink()

        print_color(Colors.GREEN, "Windows shortcuts created successfully")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error creating Windows shortcuts: {e}")
        return False


def register_uninstaller(
    install_dir, venv_path, display_name="Echo Notes", display_version="1.0"
):
    """
    Register the uninstaller in Windows Add/Remove Programs.

    Args:
        install_dir (Path): Installation directory
        venv_path (Path): Virtual environment path
        display_name (str): Display name in Add/Remove Programs
        display_version (str): Version to display

    Returns:
        bool: True if registration was successful, False otherwise
    """
    print_color(Colors.BLUE, "Registering uninstaller in Add/Remove Programs...")

    try:
        # Create uninstaller path
        uninstaller_path = install_dir / "installers/install_windows.py"
        if not uninstaller_path.exists():
            print_color(
                Colors.YELLOW, f"Warning: Uninstaller not found at {uninstaller_path}"
            )
            uninstaller_path = install_dir / "uninstall.bat"

        # Prepare registry values
        reg_path = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\EchoNotes"
        reg_values = {
            "DisplayName": (winreg.REG_SZ, display_name),
            "DisplayVersion": (winreg.REG_SZ, display_version),
            "Publisher": (winreg.REG_SZ, "Echo Notes Team"),
            "UninstallString": (
                winreg.REG_SZ,
                f'"{sys.executable}" "{uninstaller_path}" --uninstall',
            ),
            "DisplayIcon": (winreg.REG_SZ, str(install_dir / "Echo-Notes-Icon.png")),
            "InstallLocation": (winreg.REG_SZ, str(install_dir)),
            "NoModify": (winreg.REG_DWORD, 1),
            "NoRepair": (winreg.REG_DWORD, 1),
        }

        # Create registry key
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path) as reg_key:
                for name, (type_id, value) in reg_values.items():
                    winreg.SetValueEx(reg_key, name, 0, type_id, value)
            print_color(Colors.GREEN, "Registered uninstaller in Add/Remove Programs")
            return True
        except Exception as e:
            print_color(Colors.RED, f"Error creating registry key: {e}")

            # Try with administrator privileges if not already running as admin
            if not is_admin():
                print_color(
                    Colors.YELLOW,
                    "Attempting to register with administrator privileges...",
                )

                # Create a temporary script to register the uninstaller
                reg_script = tempfile.NamedTemporaryFile(suffix=".ps1", delete=False)
                reg_script_path = Path(reg_script.name)

                with open(reg_script_path, "w") as f:
                    f.write(
                        f"""
$regPath = 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\EchoNotes'
New-Item -Path $regPath -Force | Out-Null
New-ItemProperty -Path $regPath -Name 'DisplayName' -Value '{display_name}' -PropertyType String -Force | Out-Null
New-ItemProperty -Path $regPath -Name 'DisplayVersion' -Value '{display_version}' -PropertyType String -Force | Out-Null
New-ItemProperty -Path $regPath -Name 'Publisher' -Value 'Echo Notes Team' -PropertyType String -Force | Out-Null
New-ItemProperty -Path $regPath -Name 'UninstallString' -Value '"{sys.executable}" "{uninstaller_path}" --uninstall' -PropertyType String -Force | Out-Null
New-ItemProperty -Path $regPath -Name 'DisplayIcon' -Value '{install_dir / "Echo-Notes-Icon.png"}' -PropertyType String -Force | Out-Null
New-ItemProperty -Path $regPath -Name 'InstallLocation' -Value '{install_dir}' -PropertyType String -Force | Out-Null
New-ItemProperty -Path $regPath -Name 'NoModify' -Value 1 -PropertyType DWord -Force | Out-Null
New-ItemProperty -Path $regPath -Name 'NoRepair' -Value 1 -PropertyType DWord -Force | Out-Null
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
                        Colors.GREEN,
                        "Registered uninstaller in Add/Remove Programs (system-wide)",
                    )
                    return True
                except Exception as e2:
                    print_color(
                        Colors.RED,
                        f"Error registering with administrator privileges: {e2}",
                    )
                    reg_script_path.unlink()
                    return False

            return False
    except Exception as e:
        print_color(Colors.RED, f"Error registering uninstaller: {e}")
        return False


def setup_windows_service(install_dir, venv_path):
    """
    Set up Echo-Notes as a Windows service.

    Args:
        install_dir (Path): Installation directory
        venv_path (Path): Virtual environment path

    Returns:
        bool: True if service setup was successful, False otherwise
    """
    print_color(Colors.BLUE, "Setting up Echo-Notes daemon service...")

    try:
        # Create a batch file to start the daemon
        service_script = install_dir / "start_daemon.bat"
        with open(service_script, "w") as f:
            f.write(
                f"""@echo off
"{venv_path / "Scripts/python.exe"}" "{install_dir / "echo_notes/daemon.py"}" --daemon
"""
            )

        # Create a scheduled task to run at startup
        task_name = "EchoNotesDaemon"
        task_cmd = [
            "schtasks",
            "/create",
            "/tn",
            task_name,
            "/tr",
            f'"{service_script}"',
            "/sc",
            "onlogon",
            "/ru",
            "SYSTEM",
            "/f",  # Force overwrite if task exists
        ]

        try:
            subprocess.run(task_cmd, check=True)
            print_color(Colors.GREEN, "Created scheduled task for Echo-Notes daemon")
        except subprocess.CalledProcessError:
            # Try without SYSTEM privileges if that fails
            task_cmd = [
                "schtasks",
                "/create",
                "/tn",
                task_name,
                "/tr",
                f'"{service_script}"',
                "/sc",
                "onlogon",
                "/f",  # Force overwrite if task exists
            ]
            subprocess.run(task_cmd, check=True)
            print_color(
                Colors.GREEN, "Created user-level scheduled task for Echo-Notes daemon"
            )

        # Start the service now
        subprocess.run(
            [
                str(venv_path / "Scripts/python.exe"),
                str(install_dir / "echo_notes/daemon.py"),
                "--daemon",
            ],
            check=True,
        )
        print_color(Colors.GREEN, "Echo-Notes daemon started")

        return True
    except Exception as e:
        print_color(Colors.RED, f"Error setting up Windows service: {e}")
        print_color(Colors.YELLOW, "You can still start the daemon manually using:")
        print(
            f'"{venv_path / "Scripts/python.exe"}" "{install_dir / "echo_notes/daemon.py"}" --daemon'
        )
        return False


def install_windows(install_dir=None, options=None):
    """
    Perform Windows-specific installation.

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

    # Create desktop shortcut
    if not options.get("no_shortcut", False):
        create_windows_shortcut(install_dir, venv_path)
    else:
        print_color(Colors.YELLOW, "Skipping desktop shortcut creation as requested")

    # Register uninstaller
    register_uninstaller(install_dir, venv_path)

    # Set up Windows service
    if not options.get("no_service", False):
        setup_windows_service(install_dir, venv_path)
    else:
        print_color(Colors.YELLOW, "Skipping service setup as requested")

    print_color(Colors.GREEN, "Windows installation completed successfully!")
    print("")
    print_color(Colors.BLUE, "=== Getting Started ===")
    print("1. The Echo-Notes daemon has been set up to start automatically at login")
    print("2. Launch the dashboard using the desktop shortcut or Start Menu entry")
    print("3. You can also run the dashboard directly with:")
    print(
        f'   "{venv_path / "Scripts/python.exe"}" "{install_dir / "echo_notes/dashboard.py"}"'
    )
    print("")

    return True


if __name__ == "__main__":
    # This allows the module to be run directly for testing
    install_windows()
