# Echo-Notes Changelog

## [2025-05-23] - Local LLM Integration with Phi-2

### Added
- Integrated Phi-2 as a local LLM option using llama-cpp-python
- Added fallback mechanism to external API when local model is unavailable
- Created models directory structure for storing local model files
- Added USE_LOCAL_MODEL configuration option in config.py
- Added test script (test_phi2.py) to verify local model functionality
- Added automatic Phi-2 model download during installation
- Created model_manager.py to handle downloading and managing the Phi-2 model

### Changed
- Enhanced llm_client.py to support both local model inference and API calls
- Improved error handling with graceful fallback to external API
- Updated dashboard UI to include a dedicated checkbox for enabling/disabling the local Phi-2 model
- Added explanatory text in the model configuration page to clarify the benefits of using the local model
- Modified installer to automatically download the Phi-2 model from Hugging Face
- Updated installation process to install llama-cpp-python with OpenBLAS support when possible

## [2025-05-23] - .docx File Processing Fix

### Fixed
- Fixed issue with .docx files not being processed by the daemon and "Process Notes" button
- Added proper writer functionality for .docx files to preserve binary format
- Fixed LLM server availability check to use /models endpoint instead of GET requests to /chat/completions
- Updated dashboard to recognize and display .docx files in the last processed notes
- Enhanced file_utils.py to use appropriate writer functions based on file extension

### Added
- Added text_to_docx function to convert processed text back to .docx format
- Added get_writer_for_file function to select the appropriate writer based on file extension
- Added unit tests for the new writer functionality

## [2025-05-22] - Multi-Format File Support

### Added
- Added support for processing .txt and .docx files in addition to .md files
- Created new file_converters.py module to handle different file formats
- Added python-docx dependency for processing Word documents
- Added comprehensive documentation in Docs/file_format_support.md
- Added unit tests for file format converters

### Changed
- Updated file_utils.py to use the new file converter system
- Modified notes_nextcloud.py to process multiple file formats
- Updated README.md to mention the new file format support

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
- Added comprehensive debugging output throughout the installer script to diagnose execution flow issues
- Created a wrapper script (install_echo_notes.sh) that ensures uninstaller scripts are created regardless of installer behavior
- Updated uninstallation documentation with correct formatting and instructions

### Added
- Added install_echo_notes.sh wrapper script that downloads and runs the installer, then creates uninstaller scripts

### Added
- Added Docs/quick_install_guide.md with simplified installation instructions and troubleshooting tips
- Added support for multiple icon file locations in Linux installer
- Added standalone shell uninstaller script (uninstall.sh) for Linux
- Added standalone Python uninstaller script (uninstall.py) for cross-platform use
- Added test script for verifying uninstaller functionality

## Previous Changes

See installers/CHANGELOG.md for detailed installer development history.