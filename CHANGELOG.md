# Changelog

All notable changes to this project will be documented in this file..

## [0.5.1] - 2025-05-08

### Added

- Added simple cross-platform `launcher.py` script for double-click launching on all platforms
- Added desktop shortcut creation scripts for Linux, Windows, and macOS
- Added `echo-notes-dashboard.desktop` file for Linux desktop integration
- Added `install_desktop_shortcut.sh` script for Linux shortcut installation
- Added `create_windows_shortcut.bat` script for Windows desktop shortcut creation
- Added `create_macos_shortcut.py` script for macOS application creation
- Updated documentation with instructions for GUI launching without command line

## [0.5.0] - 2024-05-08

### Added

- Added GUI dashboard for monitoring and controlling the Echo-Notes daemon
- Added real-time status display showing daemon running state
- Added timestamps for last processed note and weekly summary
- Added control buttons to start/stop daemon and trigger processing
- Added real-time log display in the dashboard
- Added `echo-notes-dashboard` command to launch the GUI
- Added PyQt6 dependency for the GUI components

### Changed

- Updated setup.py with new dashboard entry point
- Updated README.md with dashboard documentation
- Added detailed dashboard_readme.md with usage instructions

## [0.4.0] - 2024-05-07

### Added

- Added built-in daemon for scheduling without cron
- Added customizable scheduling intervals through configuration
- Added `echo-notes-daemon` command to run the scheduling daemon
- Added `echo-notes-config` command for interactive scheduling configuration
- Added support for running as a systemd service
- Added `schedule_config.json` for storing scheduling preferences
- Added true daemonization support with `--daemon` flag to run detached from terminal
- Added daemon process management with `--stop` flag to terminate the daemon

### Changed

- Updated setup.py with new entry points
- Enhanced configuration system with scheduling options
- Improved documentation with daemon setup instructions

## [0.3.0] - 2024-05-07

### Added

-   Added `prompts_config.json` to store customizable prompts for daily note processing and weekly summaries.
-   Extracted hard-coded prompts from scripts into the config file for easier customization.
-   Modified `ai_weekly_summary.py` and `ai_notes_nextcloud.py` to load prompts from the config file.
-   Added environment variable support for configurable paths:
    - `ECHO_NOTES_DIR`: Location of Nextcloud notes (default: ~/Documents/notes/log)
    - `ECHO_APP_DIR`: Location of Echo-Notes application (default: auto-detected)

- Modular architecture with shared components
- Python package installation support
- Console entry points for commands
- Comprehensive setup.py configuration
- Project structure documentation

### Changed
- Restructured codebase for maintainability
- Unified configuration system
- Updated installation instructions
- Improved error logging
- Simplified cron job configuration

### Fixed
- Path handling across different environments
- Version compatibility issues
- Documentation inaccuracies

## [0.2.0] - 2024-05-07

### Added
- Weekly summary generation system
- Dual cron job support
- Timestamp fallback system

## [0.1.0] - 2024-05-06

### Added
- Initial note processing system
- Basic voice-to-text cleanup
- Hourly cron integration
