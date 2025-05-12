# Echo-Notes Changelog

## [2025-05-12] - Installer and Uninstaller Improvements

### Fixed
- Corrected installer download URLs in README.md that were causing 404 errors
- Fixed paths for Windows, macOS, and Linux installers by removing extra "Echo-Notes/" directory in URLs
- Fixed a bug in the Linux installer script where shell boolean values weren't properly converted to Python boolean values
- Fixed desktop icon issue in Linux installer by searching for the icon file in multiple locations
- Fixed uninstaller functionality by creating standalone uninstaller scripts that are copied to the user's home directory
- Fixed installation directory variable handling in Linux installer to properly set and pass the installation directory
- Fixed environment variable handling in the Python download script to correctly use the installation directory
- Enhanced the installer to create uninstaller scripts on-the-fly if they're not found in the repository
- Improved uninstaller script search to look in multiple locations
- Added debugging output to help diagnose uninstaller script creation issues
- Updated uninstallation documentation with correct formatting and instructions

### Added
- Added Docs/quick_install_guide.md with simplified installation instructions and troubleshooting tips
- Added support for multiple icon file locations in Linux installer
- Added standalone shell uninstaller script (uninstall.sh) for Linux
- Added standalone Python uninstaller script (uninstall.py) for cross-platform use
- Added test script for verifying uninstaller functionality

## Previous Changes

See installers/CHANGELOG.md for detailed installer development history.