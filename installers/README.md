# Echo-Notes Installer Framework

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