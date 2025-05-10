# Changelog

## [Unreleased]

### Added
- File browser button in the UI to allow users to choose a custom folder location for notes
- Persistent storage of the selected notes directory in the configuration file
- Automatic creation of the selected directory if it doesn't exist
- Unified uninstaller scripts for all platforms (bash, batch, and Python versions)
- Support for preserving user notes during uninstallation
- Command-line options for uninstaller (--keep-config, --purge)
- Simplified unified installer (echo_notes_installer.py) that works across all platforms
- One-click installer script (install_echo_notes.py) that downloads and installs Echo-Notes
- Automatic desktop shortcut creation during installation
- Automatic daemon startup during installation

### Fixed
- Desktop icon launcher issues with variable expansion in .desktop files
- Fixed paths in desktop shortcut creation scripts to ensure they work across different installations
- Improved desktop icon launcher to directly use the virtual environment Python interpreter instead of using bash scripts

### Changed
- Consolidated desktop shortcut scripts into a single `install_desktop_shortcuts.sh` script
- Removed redundant scripts (`run-echo-notes.sh` and `install_icon.sh`)
- Simplified installation process
- Added "Direct" version of desktop icons that are known to work reliably across different desktop environments

## [1.0.0] - 2023-01-01

### Added
- Initial release of Echo Notes
- Dashboard UI for controlling the Echo-Notes daemon
- Automatic note processing and weekly summary generation
- Configuration for scheduling note processing and summary generation
