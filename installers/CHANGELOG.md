# Echo-Notes Installer Changelog

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