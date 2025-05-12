# Installation

## Installation

## Manual Installation Guide

# Manual Installation Guide

Use this method if you prefer to install and run Echo-Notes manually, without using the one-click installer.

---

## 1. Clone the Repository

```bash
git clone https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes
cd Echo-Notes


---

2. Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


---

3. Install Dependencies

pip install -r requirements.txt

Or install the project as a package:

pip install -e .


---

4. Run Echo-Notes Tools

Start the daemon:

echo-notes-daemon --daemon

Launch the GUI dashboard:

echo-notes-dashboard

Run note processing manually:

process-notes

Generate a weekly summary:

generate-summary


---

5. Optional: Create Shortcuts

To create desktop shortcuts and launchers, see launchers.md.


---

6. Deactivation and Cleanup

To deactivate your environment:

deactivate

To remove it:

rm -rf venv/


---

For scheduling, see scheduling.md.
For uninstall steps, see uninstall.md.

---

*Source: Echo-Notes/Docs/manual_install.md*

---

## Echo-Notes Installer Changelog

## [2025-05-12] - Phase 3: Documentation and Transition

### Added
- Comprehensive documentation updates:
  - Updated main README.md with platform-specific installation instructions
  - Updated UNINSTALL.md with new uninstallation procedures
  - Created MIGRATION.md guide for transitioning from old to new installers
- Migration script (`migrate_installers.py`) to help users transition from old installers
- Package setup with `setup.py` for installable installer package
- Test framework for verifying installer functionality:
  - Unit tests for common utilities
  - Platform-specific installer tests
  - Migration script tests
- Dry-run mode for all installers to preview changes without applying them

### Improved
- Error handling and recovery mechanisms
- Cross-platform compatibility
- User feedback during installation and uninstallation
- Documentation clarity and completeness

### Changed
- Installation workflow to be more user-friendly
- Uninstallation process to be more thorough and reliable
- Configuration handling to preserve user settings during migration

## [2025-05-12] - Phase 2C: Linux Installer Implementation

### Added
- Linux-specific installer module (`installers/linux/linux_installer.py`)
  - Desktop shortcuts and application menu entries creation
  - Symlinks creation in ~/.local/bin
  - Systemd service setup with fallback to autostart
  - PATH environment variable configuration
- Linux-specific uninstaller module (`installers/linux/linux_uninstaller.py`)
  - Process termination
  - Desktop shortcuts and application menu entries removal
  - Symlinks removal
  - Systemd service removal
  - Optional user data removal
- Linux installer shell script entry point (`installers/install_linux.sh`)
  - Command-line argument parsing
  - Dependency checking
  - Repository download functionality
  - Integration with the Linux installer module

### Improved
- Modular architecture following the pattern established in Phase 1
- Comprehensive error handling and user feedback
- Support for various Linux distributions through flexible service setup

## [2025-05-05] - Phase 2B: macOS Installer Implementation

### Added
- macOS-specific installer module
- macOS-specific uninstaller module
- macOS installer shell script entry point

## [2025-04-28] - Phase 2A: Windows Installer Implementation

### Added
- Windows-specific installer module
- Windows-specific uninstaller module
- Windows installer Python entry point with GUI

## [2025-04-21] - Phase 1: Common Utilities

### Added
- Common installer utilities
- Download manager for repository content
- Cross-platform installation framework

*Source: Echo-Notes/installers/CHANGELOG.md*

---

## Echo-Notes Installer Project

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

*Source: Echo-Notes/installers/Project.md*

---

## Echo-Notes Installer Framework

This directory contains the new modular installer framework for Echo-Notes. The framework is designed to provide a consistent installation experience across different operating systems while maintaining platform-specific functionality where needed.

## Directory Structure

- `common/`: Shared utilities and functionality used by all installers
  - `installer_utils.py`: Common utility functions for checking Python version, creating virtual environments, installing dependencies, and configuring application settings
  - `download_manager.py`: Repository download functionality with error handling
  
- `windows/`: Windows-specific installer files
- `macos/`: macOS-specific installer files
- `linux/`: Linux-specific installer files

## Common Utilities

### installer_utils.py

This module provides shared utility functions for the Echo-Notes installer:

- `detect_os()`: Detect the operating system
- `check_python_version()`: Check if the current Python version meets the minimum requirement
- `find_python_executable()`: Find the appropriate Python executable
- `create_virtual_environment()`: Create a Python virtual environment
- `install_dependencies()`: Install dependencies in the virtual environment
- `configure_application()`: Configure the Echo-Notes application
- `get_installation_directory()`: Ask the user for the installation directory

### download_manager.py

This module provides functionality for downloading the Echo-Notes repository:

- `DownloadManager`: Class for managing the download and extraction of the repository
  - `download()`: Download the repository
  - `copy_to_install_dir()`: Copy the downloaded files to the installation directory
  - `cleanup()`: Clean up temporary files
- `download_echo_notes()`: Convenience function to download and install Echo-Notes

## Usage

The installer framework is designed to be used by platform-specific installer scripts. Each platform-specific installer should import the common utilities and implement any platform-specific functionality.

Example:

```python
from installers.common import (
    detect_os,
    check_python_version,
    download_echo_notes,
    create_virtual_environment,
    install_dependencies,
    configure_application
)

def main():
    # Check Python version
    if not check_python_version():
        return False
    
    # Download Echo-Notes
    install_dir = download_echo_notes()
    if not install_dir:
        return False
    
    # Create virtual environment
    venv_path = create_virtual_environment(install_dir)
    if not venv_path:
        return False
    
    # Install dependencies
    if not install_dependencies(venv_path, install_dir / "requirements.txt"):
        return False
    
    # Configure application
    if not configure_application(install_dir):
        return False
    
    # Platform-specific installation
    os_type = detect_os()
    if os_type == "windows":
        # Windows-specific installation
        pass
    elif os_type == "macos":
        # macOS-specific installation
        pass
    elif os_type == "linux":
        # Linux-specific installation
        pass
    
    return True

if __name__ == "__main__":
    main()
```

## Future Development

In future phases, platform-specific installers will be implemented in their respective directories.

*Source: Echo-Notes/installers/README.md*

---

*Source: Docs/installation.md*

---

## Manual Installation Guide

# Manual Installation Guide

Use this method if you prefer to install and run Echo-Notes manually, without using the one-click installer.

---

## 1. Clone the Repository

```bash
git clone https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes
cd Echo-Notes


---

2. Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


---

3. Install Dependencies

pip install -r requirements.txt

Or install the project as a package:

pip install -e .


---

4. Run Echo-Notes Tools

Start the daemon:

echo-notes-daemon --daemon

Launch the GUI dashboard:

echo-notes-dashboard

Run note processing manually:

process-notes

Generate a weekly summary:

generate-summary


---

5. Optional: Create Shortcuts

To create desktop shortcuts and launchers, see launchers.md.


---

6. Deactivation and Cleanup

To deactivate your environment:

deactivate

To remove it:

rm -rf venv/


---

For scheduling, see scheduling.md.
For uninstall steps, see uninstall.md.

---

*Source: Echo-Notes/Docs/manual_install.md*

---

## Echo-Notes Installer Changelog

## [2025-05-12] - Phase 3: Documentation and Transition

### Added
- Comprehensive documentation updates:
  - Updated main README.md with platform-specific installation instructions
  - Updated UNINSTALL.md with new uninstallation procedures
  - Created MIGRATION.md guide for transitioning from old to new installers
- Migration script (`migrate_installers.py`) to help users transition from old installers
- Package setup with `setup.py` for installable installer package
- Test framework for verifying installer functionality:
  - Unit tests for common utilities
  - Platform-specific installer tests
  - Migration script tests
- Dry-run mode for all installers to preview changes without applying them

### Improved
- Error handling and recovery mechanisms
- Cross-platform compatibility
- User feedback during installation and uninstallation
- Documentation clarity and completeness

### Changed
- Installation workflow to be more user-friendly
- Uninstallation process to be more thorough and reliable
- Configuration handling to preserve user settings during migration

## [2025-05-12] - Phase 2C: Linux Installer Implementation

### Added
- Linux-specific installer module (`installers/linux/linux_installer.py`)
  - Desktop shortcuts and application menu entries creation
  - Symlinks creation in ~/.local/bin
  - Systemd service setup with fallback to autostart
  - PATH environment variable configuration
- Linux-specific uninstaller module (`installers/linux/linux_uninstaller.py`)
  - Process termination
  - Desktop shortcuts and application menu entries removal
  - Symlinks removal
  - Systemd service removal
  - Optional user data removal
- Linux installer shell script entry point (`installers/install_linux.sh`)
  - Command-line argument parsing
  - Dependency checking
  - Repository download functionality
  - Integration with the Linux installer module

### Improved
- Modular architecture following the pattern established in Phase 1
- Comprehensive error handling and user feedback
- Support for various Linux distributions through flexible service setup

## [2025-05-05] - Phase 2B: macOS Installer Implementation

### Added
- macOS-specific installer module
- macOS-specific uninstaller module
- macOS installer shell script entry point

## [2025-04-28] - Phase 2A: Windows Installer Implementation

### Added
- Windows-specific installer module
- Windows-specific uninstaller module
- Windows installer Python entry point with GUI

## [2025-04-21] - Phase 1: Common Utilities

### Added
- Common installer utilities
- Download manager for repository content
- Cross-platform installation framework

*Source: Echo-Notes/installers/CHANGELOG.md*

---

## Echo-Notes Installer Project

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

*Source: Echo-Notes/installers/Project.md*

---

## Echo-Notes Installer Framework

This directory contains the new modular installer framework for Echo-Notes. The framework is designed to provide a consistent installation experience across different operating systems while maintaining platform-specific functionality where needed.

## Directory Structure

- `common/`: Shared utilities and functionality used by all installers
  - `installer_utils.py`: Common utility functions for checking Python version, creating virtual environments, installing dependencies, and configuring application settings
  - `download_manager.py`: Repository download functionality with error handling
  
- `windows/`: Windows-specific installer files
- `macos/`: macOS-specific installer files
- `linux/`: Linux-specific installer files

## Common Utilities

### installer_utils.py

This module provides shared utility functions for the Echo-Notes installer:

- `detect_os()`: Detect the operating system
- `check_python_version()`: Check if the current Python version meets the minimum requirement
- `find_python_executable()`: Find the appropriate Python executable
- `create_virtual_environment()`: Create a Python virtual environment
- `install_dependencies()`: Install dependencies in the virtual environment
- `configure_application()`: Configure the Echo-Notes application
- `get_installation_directory()`: Ask the user for the installation directory

### download_manager.py

This module provides functionality for downloading the Echo-Notes repository:

- `DownloadManager`: Class for managing the download and extraction of the repository
  - `download()`: Download the repository
  - `copy_to_install_dir()`: Copy the downloaded files to the installation directory
  - `cleanup()`: Clean up temporary files
- `download_echo_notes()`: Convenience function to download and install Echo-Notes

## Usage

The installer framework is designed to be used by platform-specific installer scripts. Each platform-specific installer should import the common utilities and implement any platform-specific functionality.

Example:

```python
from installers.common import (
    detect_os,
    check_python_version,
    download_echo_notes,
    create_virtual_environment,
    install_dependencies,
    configure_application
)

def main():
    # Check Python version
    if not check_python_version():
        return False
    
    # Download Echo-Notes
    install_dir = download_echo_notes()
    if not install_dir:
        return False
    
    # Create virtual environment
    venv_path = create_virtual_environment(install_dir)
    if not venv_path:
        return False
    
    # Install dependencies
    if not install_dependencies(venv_path, install_dir / "requirements.txt"):
        return False
    
    # Configure application
    if not configure_application(install_dir):
        return False
    
    # Platform-specific installation
    os_type = detect_os()
    if os_type == "windows":
        # Windows-specific installation
        pass
    elif os_type == "macos":
        # macOS-specific installation
        pass
    elif os_type == "linux":
        # Linux-specific installation
        pass
    
    return True

if __name__ == "__main__":
    main()
```

## Future Development

In future phases, platform-specific installers will be implemented in their respective directories.

*Source: Echo-Notes/installers/README.md*

---

## Manual Installation Guide

# Manual Installation Guide

Use this method if you prefer to install and run Echo-Notes manually, without using the one-click installer.

---

## 1. Clone the Repository

```bash
git clone https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes
cd Echo-Notes


---

2. Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


---

3. Install Dependencies

pip install -r requirements.txt

Or install the project as a package:

pip install -e .


---

4. Run Echo-Notes Tools

Start the daemon:

echo-notes-daemon --daemon

Launch the GUI dashboard:

echo-notes-dashboard

Run note processing manually:

process-notes

Generate a weekly summary:

generate-summary


---

5. Optional: Create Shortcuts

To create desktop shortcuts and launchers, see launchers.md.


---

6. Deactivation and Cleanup

To deactivate your environment:

deactivate

To remove it:

rm -rf venv/


---

For scheduling, see scheduling.md.
For uninstall steps, see uninstall.md.

---

*Source: dist/Docs/manual_install.md*

---

