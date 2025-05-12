# Echo-Notes Changelog

## [2025-05-12] - Installer Improvements

### Fixed
- Corrected installer download URLs in README.md that were causing 404 errors
- Fixed paths for Windows, macOS, and Linux installers by removing extra "Echo-Notes/" directory in URLs
- Fixed a bug in the Linux installer script where shell boolean values weren't properly converted to Python boolean values
- Fixed desktop icon issue in Linux installer by searching for the icon file in multiple locations
- Created a quick installation guide with correct URLs and troubleshooting tips

### Added
- Added Docs/quick_install_guide.md with simplified installation instructions and troubleshooting tips
- Added support for multiple icon file locations in Linux installer

## Previous Changes

See installers/CHANGELOG.md for detailed installer development history.