# Echo-Notes Installer Project

## Overview
This project provides a cross-platform installation system for Echo-Notes, with specialized installers for Windows, macOS, and Linux.

## Architecture
The installer system follows a modular architecture:

- **Common Utilities**: Shared functionality used across all platforms
  - `installer_utils.py`: Core installation utilities
  - `download_manager.py`: Repository download functionality

- **Platform-Specific Modules**:
  - **Windows**: GUI-based installer with desktop integration
  - **macOS**: Shell script entry point with application bundle creation
  - **Linux**: Shell script entry point with desktop and service integration

## Components

### Common
- `installers/common/installer_utils.py`: Core installation utilities
- `installers/common/download_manager.py`: Repository download functionality

### Windows
- `installers/windows/windows_installer.py`: Windows-specific installation logic
- `installers/windows/windows_uninstaller.py`: Windows uninstallation logic
- `installers/install_windows.py`: Main entry point with GUI

### macOS
- `installers/macos/macos_installer.py`: macOS-specific installation logic
- `installers/macos/macos_uninstaller.py`: macOS uninstallation logic
- `installers/install_macos.sh`: Main entry point shell script

### Linux
- `installers/linux/linux_installer.py`: Linux-specific installation logic
- `installers/linux/linux_uninstaller.py`: Linux uninstallation logic
- `installers/install_linux.sh`: Main entry point shell script

### Documentation and Migration
- `Echo-Notes/README.md`: Updated with new installation instructions
- `Echo-Notes/UNINSTALL.md`: Updated with new uninstallation instructions
- `Echo-Notes/MIGRATION.md`: Guide for transitioning from old to new installers
- `Echo-Notes/migrate_installers.py`: Script to automate migration process
- `installers/setup.py`: Package setup for installable installer package
- `installers/tests/`: Test framework for verifying installer functionality

## Features

### Common Features
- Python version checking
- Virtual environment creation
- Dependency installation
- Application configuration

### Windows-Specific Features
- Desktop shortcut creation
- Start Menu entry creation
- Uninstaller registration in Add/Remove Programs
- Windows service setup via Task Scheduler

### macOS-Specific Features
- Application bundle (.app) creation
- Symlinks in /usr/local/bin
- LaunchAgent service setup

### Linux-Specific Features
- Desktop shortcuts and application menu entries
- Symlinks in ~/.local/bin
- Systemd service setup with autostart fallback
- PATH environment variable configuration

## Project Status

### Completed
- Phase 1: Common Utilities
- Phase 2A: Windows Installer Implementation
- Phase 2B: macOS Installer Implementation
- Phase 2C: Linux Installer Implementation
- Phase 3: Documentation and Transition
  - Updated documentation
  - Migration tools
  - Package setup
  - Testing framework

### Next Steps
- Phase 4: Maintenance and Enhancements
  - User feedback incorporation
  - Performance optimizations
  - Additional platform support
  - Automated build and release pipeline

## Usage

### Windows
```
python install_windows.py [options]
```

### macOS
```
./install_macos.sh [options]
```

### Linux
```
./install_linux.sh [options]
```

## Options

### Common Options
- `--install-dir DIR`: Specify installation directory
- `--download-only`: Only download Echo-Notes, don't install

### Windows-Specific Options
- `--no-shortcut`: Skip desktop shortcut creation
- `--no-service`: Skip service setup

### macOS-Specific Options
- `--no-app-bundle`: Skip application bundle creation
- `--no-symlinks`: Skip symlink creation
- `--no-service`: Skip service setup

### Linux-Specific Options
- `--no-shortcuts`: Skip desktop shortcuts creation
- `--no-symlinks`: Skip symlink creation
- `--no-service`: Skip service setup

## Migration
To migrate from the old installer to the new framework:

```
python migrate_installers.py [options]
```

Options:
- `--verbose`: Show verbose output
- `--force`: Force migration even if no old installation is detected
- `--skip-backup`: Skip backing up data
- `--skip-uninstall`: Skip uninstalling old version

## Testing
To run the installer tests:

```
python -m unittest discover -s installers/tests
```

Or use the test framework for simulating installation/uninstallation:

```
python installers/test_framework.py --mode install|uninstall --platform windows|macos|linux