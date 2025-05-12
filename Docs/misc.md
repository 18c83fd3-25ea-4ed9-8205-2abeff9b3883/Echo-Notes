# Misc

## Misc

## Changelog

## [Unreleased]

### Added
- Completed reorganization cleanup by removing legacy and deprecated files
- Added test scripts to verify installation and uninstallation processes

### Changed
- Removed legacy files as per LEGACY_FILES_CLEANUP.md:
  - `ai_notes_nextcloud.py` - Replaced by `echo_notes/notes_nextcloud.py`
  - `ai_weekly_summary.py` - Replaced by `echo_notes/weekly_summary.py`
  - `echo_notes_daemon.py` - Replaced by `echo_notes/daemon.py`
  - `echo_notes_dashboard.py` - Replaced by `echo_notes/dashboard.py`
  - `shared/` directory - Replaced by `echo_notes/shared/`
- Removed deprecated files as per MIGRATION.md:
  - `echo_notes_installer.py` - Replaced by platform-specific installers
  - `install.sh` - Replaced by `install_linux.sh` and `install_macos.sh`
  - `create_macos_shortcut.py` - Functionality integrated into `macos_installer.py`
  - `create_windows_shortcut.bat` - Functionality integrated into `windows_installer.py`
  - `install_desktop_shortcuts.sh` - Functionality integrated into `linux_installer.py`
  - `fix_desktop_icon.sh` - Functionality integrated into `linux_installer.py`

### Added (Previous)
- Proper Python package structure with echo_notes module
- Fixed virtual environment permissions in installer
- Updated uninstaller to remove the echo_notes package directory
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

*Source: Echo-Notes/CHANGELOG.md*

---

## Echo-Notes Cleanup Summary

## Overview

This document summarizes the cleanup actions performed as part of the Echo-Notes reorganization.

## Completed Actions

### 1. Tested Installation and Uninstallation Processes

- ✅ Fixed and tested the installation process on Linux
- ✅ Fixed and tested the uninstallation process
- ✅ Verified that all components are installed and removed correctly

### 2. Verified Shortcuts and Launchers

- ✅ Tested and fixed desktop shortcuts
- ✅ Tested and fixed launcher scripts
- ✅ Ensured all paths are correct

### 3. Followed the Cleanup Plan in LEGACY_FILES_CLEANUP.md

Removed the following legacy files that were replaced by the new structure:
- ✅ `ai_notes_nextcloud.py` - Replaced by `echo_notes/notes_nextcloud.py`
- ✅ `ai_weekly_summary.py` - Replaced by `echo_notes/weekly_summary.py`
- ✅ `echo_notes_daemon.py` - Replaced by `echo_notes/daemon.py`
- ✅ `echo_notes_dashboard.py` - Replaced by `echo_notes/dashboard.py`
- ✅ `shared/` directory - Replaced by `echo_notes/shared/`

### 4. Removed Additional Redundant Files

Removed the following deprecated files as per MIGRATION.md:
- ✅ `echo_notes_installer.py` - Replaced by platform-specific installers
- ✅ `install.sh` - Replaced by `install_linux.sh` and `install_macos.sh`
- ✅ `create_macos_shortcut.py` - Functionality integrated into `macos_installer.py`
- ✅ `create_windows_shortcut.bat` - Functionality integrated into `windows_installer.py`
- ✅ `install_desktop_shortcuts.sh` - Functionality integrated into `linux_installer.py`
- ✅ `fix_desktop_icon.sh` - Functionality integrated into `linux_installer.py`

## Verification

After removing all legacy and deprecated files, we ran the test_installation.sh script to verify that the application still works correctly. All tests passed successfully, confirming that:

1. The installation process works correctly
2. The daemon starts successfully
3. The dashboard starts successfully
4. The uninstallation process works correctly

## Scripts Created

1. `cleanup_legacy_files.sh` - Script to remove legacy files as per LEGACY_FILES_CLEANUP.md
2. `cleanup_deprecated_files.sh` - Script to remove deprecated files as per MIGRATION.md

## Next Steps

1. Update documentation to reflect the new structure
2. Remove references to legacy files in any remaining documentation
3. Continue monitoring for any issues related to the reorganization

*Source: Echo-Notes/CLEANUP_SUMMARY.md*

---

## Scheduling Echo-Notes

# Scheduling Echo-Notes

Echo-Notes supports two main scheduling methods for note processing and summary generation:

---

## 1. Built-in Daemon (Recommended)

The built-in daemon handles background processing and scheduling automatically.

### Commands

```bash
# Start the daemon
echo-notes-daemon --daemon

# Stop the daemon
echo-notes-daemon --stop

# Configure the schedule
echo-notes-daemon --configure

# Launch the dashboard
echo-notes-dashboard

Logs & PID

Logs:

~/Documents/notes/daemon.log

~/Documents/notes/daemon.error.log


PID file:
~/Documents/notes/echo-notes.pid



---

2. Cron Jobs (Traditional)

For systems that prefer cron, use:

Hourly note processing

0 * * * * process-notes >> ~/Documents/notes/processing.log 2>&1

Weekly summary

0 12 * * 0 generate-summary >> ~/Documents/notes/weekly.log 2>&1

Ensure process-notes and generate-summary are in your $PATH or use full paths.


---

3. Running as a systemd Service (Optional)

Create a persistent background service on Linux.

Service File

[Unit]
Description=Echo-Notes Daemon
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
ExecStart=/usr/local/bin/echo-notes-daemon
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target

Setup Commands

sudo nano /etc/systemd/system/echo-notes.service
sudo systemctl enable echo-notes.service
sudo systemctl start echo-notes.service
sudo systemctl status echo-notes.service


---

Scheduling Settings

Configure via shared/schedule_config.json or use echo-notes-config.

Setting	Description	Default

processing_interval	Time between note runs (minutes)	60
summary_interval	Time between summaries (minutes)	10080
summary_day	Day of the week (0=Mon, 6=Sun)	6
summary_hour	Hour of day for weekly summary	12
daemon_enabled	Toggle the daemon on/off	true



---

Troubleshooting

Nothing runs? Check the daemon status or cron logs.

Wrong time? Check your system timezone settings.

Logs empty? Confirm correct paths in config or use full paths in cron jobs.



---

For launcher-related info, see launchers.md.

---

*Source: Echo-Notes/Docs/Scheduling.md*

---

## Echo-Notes Legacy Files Cleanup Plan

This document lists all legacy files in the root directory that can be safely removed once all references are updated to the new project structure.

## Overview

As part of the Echo-Notes reorganization, the project has been restructured from having main Python files in the root directory to a proper Python package structure with modules organized under the `echo_notes` package. This document outlines which files can be safely removed after the reorganization is complete.

## Legacy Files to Remove

The following files in the root directory can be safely removed once all references have been updated:

1. `ai_notes_nextcloud.py` - Replaced by `echo_notes/notes_nextcloud.py`
2. `ai_weekly_summary.py` - Replaced by `echo_notes/weekly_summary.py`
3. `echo_notes_daemon.py` - Replaced by `echo_notes/daemon.py`
4. `echo_notes_dashboard.py` - Replaced by `echo_notes/dashboard.py`
5. `shared/` directory - Replaced by `echo_notes/shared/`

## Dependencies and References

Before removing these files, ensure that all references to them have been updated in:

1. **Installer Scripts**: All installer scripts should reference the new file paths
   - ✅ `Echo-Notes/installers/install_windows.py`
   - ✅ `Echo-Notes/installers/install_macos.sh`
   - ✅ `Echo-Notes/installers/install_linux.sh`
   - ✅ `Echo-Notes/installers/windows/windows_installer.py`
   - ✅ `Echo-Notes/installers/macos/macos_installer.py`
   - ✅ `Echo-Notes/installers/linux/linux_installer.py`

2. **Documentation**: All documentation should reference the new file paths
   - ✅ `Echo-Notes/README.md`
   - ✅ `Echo-Notes/UNINSTALL.md`

3. **Shortcuts and Launchers**: All shortcuts and launchers should point to the new file locations
   - Desktop shortcuts
   - Application menu entries
   - Systemd service files
   - LaunchAgent service files

## Verification Steps

Before removing legacy files, perform the following verification steps:

1. Run the test reorganization script to ensure all imports work correctly:
   ```bash
   python Echo-Notes/test_reorganization.py
   ```

2. Test the installation process on each platform to ensure it works with the new structure:
   ```bash
   python Echo-Notes/installers/test_framework.py --mode install
   ```

3. Test the uninstallation process on each platform:
   ```bash
   python Echo-Notes/installers/test_framework.py --mode uninstall
   ```

4. Manually verify that all shortcuts and launchers work correctly.

## Removal Procedure

Once all verification steps have passed, you can safely remove the legacy files:

```bash
# Remove legacy Python files
rm Echo-Notes/ai_notes_nextcloud.py
rm Echo-Notes/ai_weekly_summary.py
rm Echo-Notes/echo_notes_daemon.py
rm Echo-Notes/echo_notes_dashboard.py

# Remove legacy shared directory (if it's empty)
# If it contains files that haven't been moved, move them first
rm -r Echo-Notes/shared/
```

## Rollback Plan

In case of issues after removing the legacy files, you can restore them from version control:

```bash
git checkout <commit-before-removal> -- Echo-Notes/ai_notes_nextcloud.py Echo-Notes/ai_weekly_summary.py Echo-Notes/echo_notes_daemon.py Echo-Notes/echo_notes_dashboard.py Echo-Notes/shared/
```

Replace `<commit-before-removal>` with the appropriate commit hash.

*Source: Echo-Notes/LEGACY_FILES_CLEANUP.md*

---

## Echo-Notes Installer Migration Guide

This document provides guidance on transitioning from the old Echo-Notes installation system to the new modular installer framework.

## Overview of Changes

The Echo-Notes installation system has been completely redesigned with a modular, cross-platform architecture that provides:

- **Improved reliability** with better error handling and recovery
- **Platform-specific optimizations** for Windows, macOS, and Linux
- **Consistent user experience** across all supported platforms
- **More installation options** with flexible configuration
- **Better uninstallation support** to cleanly remove all components

## Migration Timeline

| Date | Milestone |
|------|-----------|
| May 2025 | New installer framework available (current) |
| June 2025 | Legacy installers deprecated but still functional |
| August 2025 | Legacy installers removed from repository |
| September 2025 | Only new installer framework supported |

## How to Migrate

### Automatic Migration

The easiest way to migrate is to use our migration script:

```bash
python migrate_installers.py
```

This script will:
1. Detect your current Echo-Notes installation
2. Back up your configuration and data
3. Uninstall the old version
4. Install the new version using the appropriate platform-specific installer
5. Restore your configuration and data

### Manual Migration

If you prefer to migrate manually, follow these steps:

#### Step 1: Back Up Your Data

First, make sure to back up your notes and configuration:

```bash
# Back up your notes directory
cp -r "$ECHO_NOTES_DIR" echo_notes_backup/

# Back up your configuration
cp -r ~/.config/echo-notes echo_notes_config_backup/
```

#### Step 2: Uninstall the Old Version

Run the appropriate uninstaller for your platform:

```bash
# Windows
uninstall.bat

# macOS/Linux
./uninstall.sh
```

Use the `--keep-config` option to preserve your configuration files.

#### Step 3: Install the New Version

Run the new platform-specific installer:

```bash
# Windows
python installers/install_windows.py

# macOS
./installers/install_macos.sh

# Linux
./installers/install_linux.sh
```

## Comparison of Old vs. New Installers

### Windows

| Feature | Old Installer | New Installer |
|---------|--------------|---------------|
| Installation Interface | Command-line only | GUI with options + Command-line |
| Desktop Integration | Basic shortcut | Start Menu entry + Desktop shortcut |
| Service Setup | Manual | Automatic with Task Scheduler |
| Uninstallation | Basic script | Full uninstaller with Add/Remove Programs entry |

### macOS

| Feature | Old Installer | New Installer |
|---------|--------------|---------------|
| Installation Interface | Shell script | Shell script with more options |
| Application Bundle | Basic | Full .app bundle with proper structure |
| Service Setup | Manual | Automatic LaunchAgent configuration |
| Symlinks | Manual | Automatic in /usr/local/bin |

### Linux

| Feature | Old Installer | New Installer |
|---------|--------------|---------------|
| Installation Interface | Shell script | Shell script with more options |
| Desktop Integration | Basic | Full desktop entries and icons |
| Service Setup | Manual | Automatic systemd service with fallback |
| Distribution Support | Limited | Broader support for different distributions |

## Files Being Deprecated

The following files will be deprecated and eventually removed:

- `echo_notes_installer.py` - Replaced by platform-specific installers
- `install.sh` - Replaced by `install_linux.sh` and `install_macos.sh`
- `create_macos_shortcut.py` - Functionality integrated into `macos_installer.py`
- `create_windows_shortcut.bat` - Functionality integrated into `windows_installer.py`
- `install_desktop_shortcuts.sh` - Functionality integrated into `linux_installer.py`
- `fix_desktop_icon.sh` - Functionality integrated into `linux_installer.py`

## Troubleshooting Migration Issues

### Configuration Not Migrated

If your configuration wasn't properly migrated:

```bash
# Copy your backed-up configuration
cp -r echo_notes_config_backup/* ~/.config/echo-notes/
```

### Notes Not Found After Migration

If your notes aren't being found after migration:

1. Check the value of `ECHO_NOTES_DIR` environment variable
2. Update the configuration to point to your notes directory
3. Restart the Echo-Notes daemon

### Services Not Starting

If the Echo-Notes daemon service isn't starting after migration:

#### Windows
```bash
# Check Task Scheduler
schtasks /query /tn "Echo-Notes Daemon"

# Manually start the service
schtasks /run /tn "Echo-Notes Daemon"
```

#### macOS
```bash
# Check LaunchAgent status
launchctl list | grep echo-notes

# Manually load the service
launchctl load ~/Library/LaunchAgents/com.echo-notes.daemon.plist
```

#### Linux
```bash
# Check systemd service status
systemctl --user status echo-notes-daemon

# Manually start the service
systemctl --user start echo-notes-daemon
```

## Getting Help

If you encounter any issues during migration, please:

1. Check the logs in `~/.config/echo-notes/logs/`
2. Run the installer with the `--verbose` option for more detailed output
3. Open an issue on our GitHub repository with details about the problem

## Feedback

We welcome your feedback on the new installer framework. Please share your experience and suggestions through our GitHub repository.

*Source: Echo-Notes/MIGRATION.md*

---

## Fix Installation Permission Issues and Improve Package Structure

## Description
This pull request addresses the installation permission issues that users have been experiencing and improves the overall package structure of Echo-Notes.

## Changes Made

### 1. Created Proper Python Package Structure
- Created `echo_notes` directory with `__init__.py`
- Moved Python modules into the package with more standard naming:
  - `echo_notes_daemon.py` → `echo_notes/daemon.py`
  - `echo_notes_dashboard.py` → `echo_notes/dashboard.py`
  - `ai_notes_nextcloud.py` → `echo_notes/notes_nextcloud.py`
  - `ai_weekly_summary.py` → `echo_notes/weekly_summary.py`
- Included `shared` directory in the package with `__init__.py`

### 2. Fixed Virtual Environment Setup
- Enhanced `setup_venv` function in `echo_notes_installer.py` to ensure proper permissions
- Added code to explicitly set executable permissions on Python binaries (chmod 0o755)
- This fixes the `PermissionError: [Errno 13] Permission denied: '/home/j/Echo-Notes/echo_notes_venv/bin/python'` error

### 3. Updated Setup Configuration
- Modified `setup.py` to reference modules in the new package structure
- Updated entry points to use the new module paths

### 4. Updated Uninstaller
- Added new `remove_package_dir` function to remove the echo_notes package directory
- Updated the main uninstallation function to call this new function
- Ensures complete cleanup of all installed files

### 5. Updated Documentation
- Updated `README.md` with information about the new package structure
- Created `echo_notes/README.md` to document the package organization
- Updated `CHANGELOG.md` to record our changes
- Updated installation instructions to reflect the new package structure

### 6. Added Testing
- Created `test_package.py` to verify the package structure works correctly
- Updated existing test files to work with the new package structure

## How to Test
1. Download the installer:
   ```bash
   curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/install_echo_notes.py
   chmod +x install_echo_notes.py
   ./install_echo_notes.py
   ```
2. Verify that the installation completes without permission errors
3. Test the functionality of the application
4. Test the uninstaller to ensure it properly removes all files

## Note to Reviewers
These changes significantly improve the reliability of the installation process and follow Python best practices for package structure. The changes are backward compatible and should not affect existing installations.

*Source: Echo-Notes/PULL_REQUEST.md*

---

## Echo-Notes

### Sync, Process, and Summarize Notes, Files, Emails Privately and automatically with local AI

**A privacy-first voice-to-text, file, and note cleanup pipeline powered by local LLMs.**  
- Type or capture voice-to-text notes on your phone or laptop.
- Sync them to your home computer via Nextcloud, Syncthing, or your method of choice.
- Or Drop emails, files, or articles into the folder.
- Then automatically clean, structure, summarize, or create To Do's with them using a local language model.

---

[![Lint Status](https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/actions/workflows/lint.yml/badge.svg)](https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built With Python](https://img.shields.io/badge/Built%20with-Python-blue)](https://www.python.org/)
[![Local-First](https://img.shields.io/badge/Privacy-Local%20Only-green)](#)

---

### Project Status

- MVP Stable – Actively maintained
- Focus: Local-only automation, modular design
- Recent: GUI Dashboard, Auto Summaries
- Upcoming: Mood tracking, better sync detection

---

## Why Echo-Notes?

For users who want:
- 100% local, private AI-based note and file processing
- Clean, modular architecture
- Zero reliance on cloud services

---

## How It Works

```text
[Voice or Text Input]  → [Daily & Weekly Processing]
       ↓
    [Sync]
       ↓
  [Local LLM] 
       ↓
[Clean Markdown Output]
```

---

## Installation

> **Note:** Echo-Notes has recently migrated to a new modular installer framework. The instructions below use the new installers. For information about migrating from the old installers, see [MIGRATION.md](MIGRATION.md).

### Windows

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/Echo-Notes/installers/install_windows.py

# Run the installer
python install_windows.py
```

Or download and run the installer executable from our releases page.

The Windows installer provides a graphical interface with options to:
- Choose installation directory
- Create desktop shortcuts
- Set up the Echo-Notes daemon service

Command-line options are also available:
```bash
python install_windows.py install --install-dir "C:\Echo-Notes" --no-shortcut --no-service
```

### macOS

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/Echo-Notes/installers/install_macos.sh

# Make it executable
chmod +x install_macos.sh

# Run the installer
./install_macos.sh
```

The macOS installer will:
- Create an application bundle (.app)
- Set up symlinks in /usr/local/bin
- Configure a LaunchAgent service

Command-line options:
```bash
./install_macos.sh --install-dir ~/Applications/Echo-Notes --no-app-bundle --no-symlinks --no-service
```

### Linux

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/Echo-Notes/installers/install_linux.sh

# Make it executable
chmod +x install_linux.sh

# Run the installer
./install_linux.sh
```

The Linux installer will:
- Create desktop shortcuts and application menu entries
- Set up symlinks in ~/.local/bin
- Configure a systemd service (with autostart fallback)
- Update PATH environment variable

Command-line options:
```bash
./install_linux.sh --install-dir ~/echo-notes --no-shortcuts --no-symlinks --no-service
```

For advanced manual setup, see docs/manual_install.md.

### Testing the Installation

You can test the installation process without making any changes to your system using the test framework:

```bash
# Test installation on your platform
python Echo-Notes/installers/test_framework.py --mode install

# Test uninstallation on your platform
python Echo-Notes/installers/test_framework.py --mode uninstall

# Test on a specific platform
python Echo-Notes/installers/test_framework.py --mode install --platform windows|macos|linux
```

This is useful for verifying that the installation will work correctly on your system before actually performing it.

---

## Uninstallation

See [UNINSTALL.md](UNINSTALL.md) for detailed uninstallation instructions.

---

## Features

Daily note cleanup and structuring

Weekly summaries with actionable insights

Custom prompts (see shared/prompts_config.json)

GUI Dashboard: Monitor, trigger, configure

Local LLM processing via LM Studio

Daemon support for background operation


---

## Configuration

You can customize directories and behavior using environment variables:

Variable	Description

ECHO_NOTES_DIR	Location of synced notes
ECHO_APP_DIR	Application directory (optional)


export ECHO_NOTES_DIR="/your/notes/dir"
process-notes
generate-summary


---

## Advanced Scheduling & Launchers

Echo-Notes supports built-in scheduling via a daemon and optional cron or systemd setups.

For full scheduling setup (cron/systemd, dashboard launchers), see docs/scheduling.md.


---

## Dashboard

Features:

Daemon status

Manual trigger buttons

Logs viewer


See docs/dashboard.md for usage and troubleshooting.


---

## Changelog

See CHANGELOG.md


---

## License

MIT – free to use, modify, and share.


---

## Contributing

Open to:

New AI processing modes

UX enhancements

Additional backends


PRs welcome.

*Source: Echo-Notes/README.md*

---

## Echo-Notes Reorganization Summary

## Overview

This document summarizes the changes made during the reorganization of the Echo-Notes project structure. The main goal was to convert the project into a proper Python package structure to improve maintainability and follow best practices.

## Directory Structure Comparison

### Before Reorganization

```
Echo-Notes/
├── ai_notes_nextcloud.py
├── ai_weekly_summary.py
├── echo_notes_daemon.py
├── echo_notes_dashboard.py
├── shared/
│   ├── config.py
│   ├── date_helpers.py
│   ├── file_utils.py
│   ├── llm_client.py
│   ├── prompts_config.json
│   └── schedule_config.json
├── tests/
│   ├── conftest.py
│   ├── test_file_utils.py
│   ├── test_installation.sh
│   ├── test_one_click_installer.sh
│   ├── test_package.py
│   └── test_uninstall.py
└── [other configuration and utility files]
```

### After Reorganization

```
Echo-Notes/
├── echo_notes/
│   ├── __init__.py
│   ├── daemon.py
│   ├── dashboard.py
│   ├── installer.py
│   ├── launcher.py
│   ├── notes_nextcloud.py
│   ├── weekly_summary.py
│   └── shared/
│       ├── __init__.py
│       ├── config.py
│       ├── date_helpers.py
│       ├── file_utils.py
│       ├── llm_client.py
│       ├── prompts_config.json
│       └── schedule_config.json
├── config/
│   ├── pytest.ini
│   └── icons/
│       └── Echo-Notes-Icon.png
├── Docs/
│   ├── dashboard.md
│   ├── launchers.md
│   ├── manual_install.md
│   ├── Scheduling.md
│   └── Uninstall.md
├── tests/
│   ├── conftest.py
│   ├── test_file_utils.py
│   ├── test_installation.sh
│   ├── test_one_click_installer.sh
│   ├── test_package.py
│   └── test_uninstall.py
└── [other configuration and utility files]
```

## Files Moved

1. Core Python modules moved to `echo_notes/` package:
   - `ai_notes_nextcloud.py` → `echo_notes/notes_nextcloud.py`
   - `ai_weekly_summary.py` → `echo_notes/weekly_summary.py`
   - `echo_notes_daemon.py` → `echo_notes/daemon.py`
   - `echo_notes_dashboard.py` → `echo_notes/dashboard.py`
   - `launcher.py` → `echo_notes/launcher.py`

2. Shared utilities moved to `echo_notes/shared/`:
   - `shared/config.py` → `echo_notes/shared/config.py`
   - `shared/date_helpers.py` → `echo_notes/shared/date_helpers.py`
   - `shared/file_utils.py` → `echo_notes/shared/file_utils.py`
   - `shared/llm_client.py` → `echo_notes/shared/llm_client.py`
   - `shared/prompts_config.json` → `echo_notes/shared/prompts_config.json`
   - `shared/schedule_config.json` → `echo_notes/shared/schedule_config.json`

3. Configuration files moved to `config/`:
   - `pytest.ini` → `config/pytest.ini`
   - `Echo-Notes-Icon.png` → `config/icons/Echo-Notes-Icon.png`

4. Documentation moved to `Docs/`:
   - Various documentation files consolidated in the `Docs/` directory

## Fixed Issues

1. Updated import statements in:
   - `echo_notes/dashboard.py`: Changed from `from shared import config` to `from echo_notes.shared import config`
   - `echo_notes/daemon.py`: Changed from `from shared import config` to `from echo_notes.shared import config`

## Potential Issues That Need Attention

1. **Installer Scripts**: Many installer scripts still reference the old file paths (e.g., `echo_notes_dashboard.py` instead of `echo_notes/dashboard.py`). These need to be updated to point to the new file locations.

2. **Entry Points**: The entry points in `setup.py` have been updated to use the new module paths, but any scripts or shortcuts that directly call the Python files need to be updated.

3. **Documentation**: Some documentation may still reference the old file structure and needs to be updated.

4. **Legacy Files**: The old Python files (`ai_notes_nextcloud.py`, `ai_weekly_summary.py`, `echo_notes_daemon.py`, `echo_notes_dashboard.py`) still exist in the root directory. These should be removed once all references to them have been updated.

## Next Steps

1. Update all installer scripts to reference the new file paths
2. Update any documentation that references the old file structure
3. Remove the old Python files from the root directory once all references have been updated
4. Update any shortcuts or launchers to point to the new file locations
5. Consider adding more comprehensive tests to verify the functionality of the reorganized code

*Source: Echo-Notes/REORGANIZATION_SUMMARY.md*

---

## Echo Notes Use Cases

# Echo Notes Use Cases

Echo-Notes isn't just for cleaning up notes. It's a modular, local-first automation system that works with synced files from **Nextcloud**, **Syncthing**, or any other tool that writes to disk.

Below are real-world workflows powered by Echo + local LLMs.

---

## 1. Voice Note to Structured Journal

**Flow**:  
Dictate quick thoughts into a voice-to-text app → synced to Echo folder → Echo cleans grammar, formats into Markdown journal entry, adds tags or todos.

**Prompt Example**:
```json
"Rewrite this voice note into a structured journal entry with headings, todos, and cleaned-up grammar. Use Markdown."
````

**Folder Tip**:
Use a `Journal/YYYY-MM-DD/` folder convention for organized output.

---

## 2. Weekly Summary Generator

**Flow**:
Echo collects daily journal files → generates a weekly summary with bullet points, mood indicators, and highlights.

**Prompt Example**:

```json
"Summarize the following 7 journal entries. Highlight mood trends, major events, and tasks to carry forward."
```

**Output**:
A single weekly `.md` file written to a `Summaries/` folder.

---

## 3. Research Digest

**Flow**:
Drop PDFs, articles, or note dumps into a `Reading` folder → Echo extracts key takeaways and writes a summary with tags.

**Prompt Example**:

```json
"Extract main points, arguments, and useful quotes from this article. Use Markdown with bullet points."
```

---

## 4. Idea Refinement

**Flow**:
Rough ideas or outlines dropped into a synced folder → Echo rewrites them into structured blog posts, Nostr drafts, or polished content.

**Prompt Example**:

```json
"Expand this outline into a 500-word blog post with an intro, body, and conclusion."
```

---

## 5. Code Snippet Commentary

**Flow**:
Save `.py`, `.go`, or `.sh` files to a watched `CodeDrop/` folder → Echo adds comments, refactors, or explains them.

**Prompt Example**:

```json
"Explain this code in plain English. Then suggest improvements or flag potential bugs."
```

---

## 6. Daily To-Do Extraction

**Flow**:
Capture raw daily notes → Echo extracts tasks and writes to `Todos/YYYY-MM-DD.md`.

**Prompt Example**:

```json
"Pull out any action items or todos from this note and reformat them into a checklist."
```

---

## 7. Personal Knowledge Base (PKB) Conversion

**Flow**:
Echo processes longform notes into Zettelkasten-style atomic notes, flashcards, or Q\&A pairs.

**Prompt Example**:

```json
"Split this note into individual concept cards with titles, summaries, and questions."
```

---

## 8. Nostr Draft Automation

**Flow**:
Write a longform note in Markdown → Echo generates short posts, threads, or tag suggestions for Nostr.

**Prompt Example**:

```json
"Turn this journal entry into 3 Nostr posts, each with relevant hashtags."
```

---

## 9. Mood Tracker & Emotional Tagging (WIP)

**Flow**:
Journal entries or memos → Echo scores tone/sentiment → adds metadata to frontmatter.

**Prompt Example**:

```json
"Analyze emotional tone. Tag this entry as positive, neutral, or negative. Add a brief mood summary."
```

---

## 10. Secure PDF Summarizer

**Flow**:
Drop privacy-sensitive PDFs (e.g. contracts, policies, research) into a folder → Echo summarizes offline, privately.

**Prompt Example**:

```json
"Summarize this document in plain English. Highlight key terms, risks, and action items."
```

---

## Tips for Use

* You can create multiple watch folders with different prompt configs.
* Echo is fully local, so your content stays private—no cloud processing.
* Combine with `systemd`, `cron`, or GUI Dashboard to run background jobs.

---

Got your own use case? PRs welcome!

*Source: Echo-Notes/Use_Cases.md*

---

## Echo-Notes Package

This directory contains the main Python package for Echo-Notes.

## Structure

- `__init__.py` - Package initialization
- `daemon.py` - Echo-Notes daemon for background processing
- `dashboard.py` - Echo-Notes dashboard GUI
- `notes_nextcloud.py` - Nextcloud notes integration
- `weekly_summary.py` - Weekly summary generation
- `shared/` - Shared utilities and configuration

## Usage

The package is designed to be installed via pip:

```bash
pip install -e .
```

This will install the following command-line tools:

- `echo-notes-daemon` - Start the Echo-Notes daemon
- `echo-notes-dashboard` - Launch the Echo-Notes dashboard
- `echo-notes-config` - Configure Echo-Notes scheduling
- `process-notes` - Process notes for Nextcloud integration
- `generate-summary` - Generate weekly summaries

*Source: Echo-Notes/echo_notes/README.md*

---

## Echo-Notes Installer Migration PR

## Overview

This PR consolidates the Echo-Notes installers into a modular, cross-platform framework that provides improved reliability, platform-specific optimizations, and a consistent user experience across Windows, macOS, and Linux.

## Changes Made

### Architecture Improvements

- **Modular Design**: Created a structured installer framework with common utilities and platform-specific modules
- **Improved Error Handling**: Added better error detection, reporting, and recovery mechanisms
- **Cross-Platform Consistency**: Unified command-line options and installation flow across all platforms
- **Platform-Specific Optimizations**: Enhanced integration with native OS features

### Platform-Specific Enhancements

#### Windows
- GUI-based installer with desktop integration
- Start Menu entry creation
- Windows service setup via Task Scheduler
- Uninstaller registration in Add/Remove Programs

#### macOS
- Application bundle (.app) creation
- Symlinks in /usr/local/bin
- LaunchAgent service setup

#### Linux
- Desktop shortcuts and application menu entries
- Symlinks in ~/.local/bin
- Systemd service setup with autostart fallback
- PATH environment variable configuration

### Documentation Updates

- Updated README.md with new installation instructions
- Updated UNINSTALL.md with new uninstallation instructions
- Created MIGRATION.md with guidance for transitioning from old to new installers
- Added information about the test framework to user-facing documentation

### Bug Fixes

- Fixed DownloadManager class to properly handle install_dir parameter
- Added dry_run option handling to Linux installer
- Fixed various code quality issues:
  - Removed unnecessary f-strings
  - Fixed bare except clauses
  - Removed unused imports

## Migration Path for Existing Users

Users can migrate to the new installer framework using:

1. **Automatic Migration**: Using the `migrate_installers.py` script
2. **Manual Migration**: Following the step-by-step guide in MIGRATION.md

## Testing Performed

- Tested installation and uninstallation on all supported platforms
- Verified compatibility with existing installations
- Tested migration from old to new installer system
- Validated error handling and recovery mechanisms

## File Changes

### New Files Added
- `installers/__init__.py`
- `installers/README.md`
- `installers/CHANGELOG.md`
- `installers/Project.md`
- `installers/setup.py`
- `installers/test_framework.py`
- `installers/common/__init__.py`
- `installers/common/installer_utils.py`
- `installers/common/download_manager.py`
- `installers/windows/__init__.py`
- `installers/windows/windows_installer.py`
- `installers/windows/windows_uninstaller.py`
- `installers/install_windows.py`
- `installers/macos/__init__.py`
- `installers/macos/macos_installer.py`
- `installers/macos/macos_uninstaller.py`
- `installers/install_macos.sh`
- `installers/linux/__init__.py`
- `installers/linux/linux_installer.py`
- `installers/linux/linux_uninstaller.py`
- `installers/install_linux.sh`
- `installers/tests/__init__.py`
- `installers/tests/test_installers.py`

### Modified Files
- `Echo-Notes/README.md`
- `Echo-Notes/UNINSTALL.md`
- `Echo-Notes/MIGRATION.md`
- `Echo-Notes/migrate_installers.py`

### Deprecated Files (To Be Removed Later)
- `Echo-Notes/echo_notes_installer.py`
- `Echo-Notes/install.sh`
- `Echo-Notes/create_macos_shortcut.py`
- `Echo-Notes/create_windows_shortcut.bat`
- `Echo-Notes/install_desktop_shortcuts.sh`
- `Echo-Notes/fix_desktop_icon.sh`
- `Echo-Notes/uninstall.bat`
- `Echo-Notes/uninstall.py`
- `Echo-Notes/uninstall.sh`

## Known Issues and Future Work

1. **Code Quality**: There are still style issues that should be addressed in a follow-up PR:
   - Whitespace in blank lines
   - Lines exceeding 79 characters
   - Missing newlines at end of files
   - Spacing between functions and classes

2. **Test Coverage**: Additional tests should be added to cover:
   - Edge cases in installation/uninstallation
   - Error handling scenarios
   - Migration from old to new installers

3. **Documentation**: Some additional documentation improvements:
   - More detailed examples for advanced usage
   - Troubleshooting guide for common issues

## Reviewer Notes

Please focus on:
1. The overall architecture and design of the installer framework
2. Platform-specific implementation details
3. Migration path for existing users
4. Documentation clarity and completeness

The code quality issues will be addressed in a follow-up PR.

*Source: PR_DESCRIPTION.md*

---

## Echo-Notes Project Streamlining

This document outlines the streamlining process for the Echo-Notes project, addressing bloat from testing scripts, utility scripts, and documentation files.

## Overview

The Echo-Notes project has grown over time, accumulating various test files, utility scripts, and documentation that may be redundant or only needed during development. This streamlining process aims to:

1. Identify essential files needed for core functionality
2. Consolidate redundant documentation
3. Organize tests into essential and development-only categories
4. Create a minimal viable project structure
5. Provide tools for maintaining a clean project structure

## Streamlining Scripts

The following scripts have been created to help with the streamlining process:

### 1. `streamline_project.py`

The main entry point for the streamlining process. This script orchestrates the entire streamlining process by running the other scripts in sequence.

**Usage:**
```bash
python streamline_project.py [--dry-run] [--skip-step STEP]
```

**Options:**
- `--dry-run`: Show what would be done without making changes
- `--skip-step STEP`: Skip a specific step (analyze, docs, tests, cleanup)

### 2. `identify_essential_files.py`

Analyzes the project structure to identify the minimal set of files needed for the project to function correctly.

**Usage:**
```bash
python identify_essential_files.py [--output OUTPUT_FILE]
```

**Options:**
- `--output OUTPUT_FILE`: Write the results to the specified file (default: essential_files.md)

### 3. `consolidate_docs.py`

Consolidates the documentation files into a more organized structure, merging redundant documentation and creating a comprehensive README.md.

**Usage:**
```bash
python consolidate_docs.py [--dry-run]
```

**Options:**
- `--dry-run`: Show what would be done without making changes

### 4. `analyze_tests.py`

Analyzes the test files to identify which tests are essential for ensuring core functionality and which ones are redundant or only used for development.

**Usage:**
```bash
python analyze_tests.py [--output OUTPUT_FILE] [--dry-run] [--consolidate]
```

**Options:**
- `--output OUTPUT_FILE`: Write the results to the specified file (default: test_analysis.md)
- `--dry-run`: Show what would be done without making changes
- `--consolidate`: Consolidate test files according to the plan

### 5. `cleanup.py`

Cleans up the project by moving development-only files to appropriate directories, consolidating redundant files, and creating a minimal viable project structure.

**Usage:**
```bash
python cleanup.py [--dry-run]
```

**Options:**
- `--dry-run`: Show what would be done without making changes

## Streamlining Process

The streamlining process follows these steps:

1. **Analysis**: Identify essential files, redundant files, and development-only files
2. **Documentation Consolidation**: Merge redundant documentation and create a comprehensive README
3. **Test Consolidation**: Organize tests into essential and development-only categories
4. **Cleanup**: Create a minimal viable project structure and move development-only files to appropriate directories

## Minimal Viable Project Structure

The minimal viable project structure includes:

```
echo_notes/          # Main package directory
├── __init__.py
├── daemon.py        # Daemon for background processing
├── dashboard.py     # GUI dashboard
├── notes_nextcloud.py # Nextcloud integration
├── weekly_summary.py # Weekly summary generation
└── shared/          # Shared utilities
    ├── __init__.py
    ├── config.py    # Configuration handling
    ├── date_helpers.py # Date manipulation utilities
    ├── file_utils.py # File operations
    ├── llm_client.py # LLM integration
    ├── prompts_config.json # LLM prompt templates
    └── schedule_config.json # Scheduling configuration

tests/              # Test directory
├── __init__.py
├── conftest.py     # Pytest configuration
└── test_file_utils.py # Tests for file utilities

Docs/               # Documentation
├── dashboard.md    # Dashboard documentation
├── launchers.md    # Launcher documentation
├── manual_install.md # Manual installation guide
├── Scheduling.md   # Scheduling documentation
└── Uninstall.md    # Uninstallation guide

# Root files
setup.py           # Package setup
requirements.txt   # Dependencies
pytest.ini         # Pytest configuration
LICENSE            # License file
CHANGELOG.md       # Changelog
README.md          # Main documentation
```

## Development Structure

For development purposes, additional directories are created:

```
tools/              # Development tools
├── cleanup/        # Cleanup scripts
├── migration/      # Migration utilities
└── dev_tests/      # Development-only tests

Docs/archive/       # Archived documentation
```

## How to Use

1. **Analyze the project**:
   ```bash
   python identify_essential_files.py
   ```

2. **Consolidate documentation**:
   ```bash
   python consolidate_docs.py
   ```

3. **Analyze and consolidate tests**:
   ```bash
   python analyze_tests.py --consolidate
   ```

4. **Run the complete streamlining process**:
   ```bash
   python streamline_project.py
   ```

5. **Create a clean distribution package**:
   ```bash
   cd dist && python cleanup.py
   ```

## Benefits of Streamlining

1. **Reduced Complexity**: Fewer files and a cleaner structure make the project easier to understand and maintain
2. **Improved Documentation**: Consolidated documentation provides a better user experience
3. **Focused Testing**: Essential tests are separated from development-only tests
4. **Smaller Distribution**: The minimal viable project is smaller and more focused
5. **Better Organization**: Development tools and utilities are properly organized

## Maintenance Guidelines

To maintain a clean project structure:

1. Keep development-only files in the `tools` directory
2. Add new tests to the appropriate directory (`tests` for essential tests, `tools/dev_tests` for development-only tests)
3. Update documentation in the `Docs` directory
4. Run the streamlining process periodically to identify and address new bloat

*Source: STREAMLINING.md*

---

## Echo-Notes Essential Files Report

This report identifies the minimal set of files needed for the Echo-Notes project to function correctly.

## Core Files (Essential)

These files are essential for the basic functionality of Echo-Notes:

- `Echo-Notes/config/pytest.ini`
- `Echo-Notes/echo_notes/__init__.py`
- `Echo-Notes/echo_notes/daemon.py`
- `Echo-Notes/echo_notes/dashboard.py`
- `Echo-Notes/echo_notes/launcher.py`
- `Echo-Notes/echo_notes/notes_nextcloud.py`
- `Echo-Notes/echo_notes/shared/__init__.py`
- `Echo-Notes/echo_notes/shared/config.py`
- `Echo-Notes/echo_notes/shared/date_helpers.py`
- `Echo-Notes/echo_notes/shared/file_utils.py`
- `Echo-Notes/echo_notes/shared/llm_client.py`
- `Echo-Notes/echo_notes/shared/prompts_config.json`
- `Echo-Notes/echo_notes/shared/schedule_config.json`
- `Echo-Notes/echo_notes/weekly_summary.py`
- `Echo-Notes/launcher.py`
- `Echo-Notes/pytest.ini`
- `Echo-Notes/requirements.txt`
- `Echo-Notes/setup.py`
- `identify_essential_files.py`
- `streamline_project.py`


## Installer Files

These files are used for installing Echo-Notes:

- `Echo-Notes/echo_notes/__pycache__/installer.cpython-311.pyc`
- `Echo-Notes/echo_notes/installer.py`
- `Echo-Notes/install_echo_notes.py`
- `Echo-Notes/installers/__init__.py`
- `Echo-Notes/installers/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/installers/common/__init__.py`
- `Echo-Notes/installers/common/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/installers/common/__pycache__/download_manager.cpython-311.pyc`
- `Echo-Notes/installers/common/__pycache__/installer_utils.cpython-311.pyc`
- `Echo-Notes/installers/common/download_manager.py`
- `Echo-Notes/installers/common/installer_utils.py`
- `Echo-Notes/installers/install.py`
- `Echo-Notes/installers/install_linux.sh`
- `Echo-Notes/installers/install_macos.sh`
- `Echo-Notes/installers/install_windows.py`
- `Echo-Notes/installers/linux/__init__.py`
- `Echo-Notes/installers/linux/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/installers/linux/__pycache__/linux_installer.cpython-311.pyc`
- `Echo-Notes/installers/linux/__pycache__/linux_uninstaller.cpython-311.pyc`
- `Echo-Notes/installers/linux/fix_desktop_icon.sh`
- `Echo-Notes/installers/linux/install_desktop_shortcuts.sh`
- `Echo-Notes/installers/linux/linux_installer.py`
- `Echo-Notes/installers/linux/linux_uninstaller.py`
- `Echo-Notes/installers/macos/__init__.py`
- `Echo-Notes/installers/macos/create_shortcut.py`
- `Echo-Notes/installers/macos/macos_installer.py`
- `Echo-Notes/installers/macos/macos_uninstaller.py`
- `Echo-Notes/installers/setup.py`
- `Echo-Notes/installers/uninstall.py`
- `Echo-Notes/installers/uninstall.sh`
- `Echo-Notes/installers/windows/__init__.py`
- `Echo-Notes/installers/windows/create_shortcut.bat`
- `Echo-Notes/installers/windows/uninstall.bat`
- `Echo-Notes/installers/windows/windows_installer.py`
- `Echo-Notes/installers/windows/windows_uninstaller.py`
- `Echo-Notes/uninstall.bat`
- `Echo-Notes/uninstall.py`
- `Echo-Notes/uninstall.sh`


## Documentation Files

These files provide documentation for Echo-Notes:

- `Echo-Notes/CHANGELOG.md`
- `Echo-Notes/CLEANUP_SUMMARY.md`
- `Echo-Notes/Docs/Scheduling.md`
- `Echo-Notes/Docs/Uninstall.md`
- `Echo-Notes/Docs/dashboard.md`
- `Echo-Notes/Docs/launchers.md`
- `Echo-Notes/Docs/manual_install.md`
- `Echo-Notes/LEGACY_FILES_CLEANUP.md`
- `Echo-Notes/MIGRATION.md`
- `Echo-Notes/PULL_REQUEST.md`
- `Echo-Notes/README.md`
- `Echo-Notes/REORGANIZATION_SUMMARY.md`
- `Echo-Notes/TESTING.md`
- `Echo-Notes/UNINSTALL.md`
- `Echo-Notes/Use_Cases.md`
- `Echo-Notes/dashboard_readme.md`
- `Echo-Notes/echo_notes/README.md`
- `Echo-Notes/installers/CHANGELOG.md`
- `Echo-Notes/installers/Project.md`
- `Echo-Notes/installers/README.md`
- `Echo-Notes/testing.md`
- `PR_DESCRIPTION.md`
- `STREAMLINING.md`
- `consolidate_docs.py`


## Test Files

These files are used for testing Echo-Notes:

- `Echo-Notes/installers/test_framework.py`
- `Echo-Notes/installers/tests/__init__.py`
- `Echo-Notes/installers/tests/__pycache__/test_installers.cpython-311.pyc`
- `Echo-Notes/installers/tests/test_installers.py`
- `Echo-Notes/test_installation.sh`
- `Echo-Notes/test_one_click_installer.sh`
- `Echo-Notes/test_package.py`
- `Echo-Notes/test_reorganization.py`
- `Echo-Notes/test_uninstall.py`
- `Echo-Notes/tests/conftest.py`
- `Echo-Notes/tests/test_file_utils.py`
- `Echo-Notes/tests/test_installation.sh`
- `Echo-Notes/tests/test_one_click_installer.sh`
- `Echo-Notes/tests/test_package.py`
- `Echo-Notes/tests/test_uninstall.py`
- `analyze_tests.py`
- `test_streamlined_project.py`


## Development Files

These files are only needed during development:

- `Echo-Notes/Echo-Notes-Icon.png`
- `Echo-Notes/LICENSE`
- `Echo-Notes/cleanup_deprecated_files.sh`
- `Echo-Notes/cleanup_legacy_files.sh`
- `Echo-Notes/config/echo-notes-dashboard.desktop`
- `Echo-Notes/config/icons/Echo-Notes-Icon.png`
- `Echo-Notes/echo-notes-dashboard.desktop`
- `Echo-Notes/echo_notes.egg-info/PKG-INFO`
- `Echo-Notes/echo_notes.egg-info/SOURCES.txt`
- `Echo-Notes/echo_notes.egg-info/dependency_links.txt`
- `Echo-Notes/echo_notes.egg-info/entry_points.txt`
- `Echo-Notes/echo_notes.egg-info/requires.txt`
- `Echo-Notes/echo_notes.egg-info/top_level.txt`
- `Echo-Notes/echo_notes/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/echo_notes/__pycache__/daemon.cpython-311.pyc`
- `Echo-Notes/echo_notes/__pycache__/dashboard.cpython-311.pyc`
- `Echo-Notes/echo_notes/__pycache__/notes_nextcloud.cpython-311.pyc`
- `Echo-Notes/echo_notes/__pycache__/weekly_summary.cpython-311.pyc`
- `Echo-Notes/echo_notes/shared/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/echo_notes/shared/__pycache__/config.cpython-311.pyc`
- `Echo-Notes/echo_notes/shared/__pycache__/date_helpers.cpython-311.pyc`
- `Echo-Notes/echo_notes/shared/__pycache__/file_utils.cpython-311.pyc`
- `Echo-Notes/migrate_installers.py`
- `cleanup.py`


## Summary

- Core Files: 20

- Installer Files: 38

- Documentation Files: 24

- Test Files: 17

- Development Files: 24

- Total Files: 123

## Minimal Viable Project

The minimal viable project consists of:

1. All Core Files

2. Essential Documentation (README.md, LICENSE)

3. Main installer script


All other files can be moved to separate directories or removed for distribution.

*Source: essential_files.md*

---

*Source: Docs/misc.md*

---

## Changelog

## [Unreleased]

### Added
- Completed reorganization cleanup by removing legacy and deprecated files
- Added test scripts to verify installation and uninstallation processes

### Changed
- Removed legacy files as per LEGACY_FILES_CLEANUP.md:
  - `ai_notes_nextcloud.py` - Replaced by `echo_notes/notes_nextcloud.py`
  - `ai_weekly_summary.py` - Replaced by `echo_notes/weekly_summary.py`
  - `echo_notes_daemon.py` - Replaced by `echo_notes/daemon.py`
  - `echo_notes_dashboard.py` - Replaced by `echo_notes/dashboard.py`
  - `shared/` directory - Replaced by `echo_notes/shared/`
- Removed deprecated files as per MIGRATION.md:
  - `echo_notes_installer.py` - Replaced by platform-specific installers
  - `install.sh` - Replaced by `install_linux.sh` and `install_macos.sh`
  - `create_macos_shortcut.py` - Functionality integrated into `macos_installer.py`
  - `create_windows_shortcut.bat` - Functionality integrated into `windows_installer.py`
  - `install_desktop_shortcuts.sh` - Functionality integrated into `linux_installer.py`
  - `fix_desktop_icon.sh` - Functionality integrated into `linux_installer.py`

### Added (Previous)
- Proper Python package structure with echo_notes module
- Fixed virtual environment permissions in installer
- Updated uninstaller to remove the echo_notes package directory
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

*Source: Echo-Notes/CHANGELOG.md*

---

## Echo-Notes Cleanup Summary

## Overview

This document summarizes the cleanup actions performed as part of the Echo-Notes reorganization.

## Completed Actions

### 1. Tested Installation and Uninstallation Processes

- ✅ Fixed and tested the installation process on Linux
- ✅ Fixed and tested the uninstallation process
- ✅ Verified that all components are installed and removed correctly

### 2. Verified Shortcuts and Launchers

- ✅ Tested and fixed desktop shortcuts
- ✅ Tested and fixed launcher scripts
- ✅ Ensured all paths are correct

### 3. Followed the Cleanup Plan in LEGACY_FILES_CLEANUP.md

Removed the following legacy files that were replaced by the new structure:
- ✅ `ai_notes_nextcloud.py` - Replaced by `echo_notes/notes_nextcloud.py`
- ✅ `ai_weekly_summary.py` - Replaced by `echo_notes/weekly_summary.py`
- ✅ `echo_notes_daemon.py` - Replaced by `echo_notes/daemon.py`
- ✅ `echo_notes_dashboard.py` - Replaced by `echo_notes/dashboard.py`
- ✅ `shared/` directory - Replaced by `echo_notes/shared/`

### 4. Removed Additional Redundant Files

Removed the following deprecated files as per MIGRATION.md:
- ✅ `echo_notes_installer.py` - Replaced by platform-specific installers
- ✅ `install.sh` - Replaced by `install_linux.sh` and `install_macos.sh`
- ✅ `create_macos_shortcut.py` - Functionality integrated into `macos_installer.py`
- ✅ `create_windows_shortcut.bat` - Functionality integrated into `windows_installer.py`
- ✅ `install_desktop_shortcuts.sh` - Functionality integrated into `linux_installer.py`
- ✅ `fix_desktop_icon.sh` - Functionality integrated into `linux_installer.py`

## Verification

After removing all legacy and deprecated files, we ran the test_installation.sh script to verify that the application still works correctly. All tests passed successfully, confirming that:

1. The installation process works correctly
2. The daemon starts successfully
3. The dashboard starts successfully
4. The uninstallation process works correctly

## Scripts Created

1. `cleanup_legacy_files.sh` - Script to remove legacy files as per LEGACY_FILES_CLEANUP.md
2. `cleanup_deprecated_files.sh` - Script to remove deprecated files as per MIGRATION.md

## Next Steps

1. Update documentation to reflect the new structure
2. Remove references to legacy files in any remaining documentation
3. Continue monitoring for any issues related to the reorganization

*Source: Echo-Notes/CLEANUP_SUMMARY.md*

---

## Scheduling Echo-Notes

# Scheduling Echo-Notes

Echo-Notes supports two main scheduling methods for note processing and summary generation:

---

## 1. Built-in Daemon (Recommended)

The built-in daemon handles background processing and scheduling automatically.

### Commands

```bash
# Start the daemon
echo-notes-daemon --daemon

# Stop the daemon
echo-notes-daemon --stop

# Configure the schedule
echo-notes-daemon --configure

# Launch the dashboard
echo-notes-dashboard

Logs & PID

Logs:

~/Documents/notes/daemon.log

~/Documents/notes/daemon.error.log


PID file:
~/Documents/notes/echo-notes.pid



---

2. Cron Jobs (Traditional)

For systems that prefer cron, use:

Hourly note processing

0 * * * * process-notes >> ~/Documents/notes/processing.log 2>&1

Weekly summary

0 12 * * 0 generate-summary >> ~/Documents/notes/weekly.log 2>&1

Ensure process-notes and generate-summary are in your $PATH or use full paths.


---

3. Running as a systemd Service (Optional)

Create a persistent background service on Linux.

Service File

[Unit]
Description=Echo-Notes Daemon
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
ExecStart=/usr/local/bin/echo-notes-daemon
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target

Setup Commands

sudo nano /etc/systemd/system/echo-notes.service
sudo systemctl enable echo-notes.service
sudo systemctl start echo-notes.service
sudo systemctl status echo-notes.service


---

Scheduling Settings

Configure via shared/schedule_config.json or use echo-notes-config.

Setting	Description	Default

processing_interval	Time between note runs (minutes)	60
summary_interval	Time between summaries (minutes)	10080
summary_day	Day of the week (0=Mon, 6=Sun)	6
summary_hour	Hour of day for weekly summary	12
daemon_enabled	Toggle the daemon on/off	true



---

Troubleshooting

Nothing runs? Check the daemon status or cron logs.

Wrong time? Check your system timezone settings.

Logs empty? Confirm correct paths in config or use full paths in cron jobs.



---

For launcher-related info, see launchers.md.

---

*Source: Echo-Notes/Docs/Scheduling.md*

---

## Echo-Notes Legacy Files Cleanup Plan

This document lists all legacy files in the root directory that can be safely removed once all references are updated to the new project structure.

## Overview

As part of the Echo-Notes reorganization, the project has been restructured from having main Python files in the root directory to a proper Python package structure with modules organized under the `echo_notes` package. This document outlines which files can be safely removed after the reorganization is complete.

## Legacy Files to Remove

The following files in the root directory can be safely removed once all references have been updated:

1. `ai_notes_nextcloud.py` - Replaced by `echo_notes/notes_nextcloud.py`
2. `ai_weekly_summary.py` - Replaced by `echo_notes/weekly_summary.py`
3. `echo_notes_daemon.py` - Replaced by `echo_notes/daemon.py`
4. `echo_notes_dashboard.py` - Replaced by `echo_notes/dashboard.py`
5. `shared/` directory - Replaced by `echo_notes/shared/`

## Dependencies and References

Before removing these files, ensure that all references to them have been updated in:

1. **Installer Scripts**: All installer scripts should reference the new file paths
   - ✅ `Echo-Notes/installers/install_windows.py`
   - ✅ `Echo-Notes/installers/install_macos.sh`
   - ✅ `Echo-Notes/installers/install_linux.sh`
   - ✅ `Echo-Notes/installers/windows/windows_installer.py`
   - ✅ `Echo-Notes/installers/macos/macos_installer.py`
   - ✅ `Echo-Notes/installers/linux/linux_installer.py`

2. **Documentation**: All documentation should reference the new file paths
   - ✅ `Echo-Notes/README.md`
   - ✅ `Echo-Notes/UNINSTALL.md`

3. **Shortcuts and Launchers**: All shortcuts and launchers should point to the new file locations
   - Desktop shortcuts
   - Application menu entries
   - Systemd service files
   - LaunchAgent service files

## Verification Steps

Before removing legacy files, perform the following verification steps:

1. Run the test reorganization script to ensure all imports work correctly:
   ```bash
   python Echo-Notes/test_reorganization.py
   ```

2. Test the installation process on each platform to ensure it works with the new structure:
   ```bash
   python Echo-Notes/installers/test_framework.py --mode install
   ```

3. Test the uninstallation process on each platform:
   ```bash
   python Echo-Notes/installers/test_framework.py --mode uninstall
   ```

4. Manually verify that all shortcuts and launchers work correctly.

## Removal Procedure

Once all verification steps have passed, you can safely remove the legacy files:

```bash
# Remove legacy Python files
rm Echo-Notes/ai_notes_nextcloud.py
rm Echo-Notes/ai_weekly_summary.py
rm Echo-Notes/echo_notes_daemon.py
rm Echo-Notes/echo_notes_dashboard.py

# Remove legacy shared directory (if it's empty)
# If it contains files that haven't been moved, move them first
rm -r Echo-Notes/shared/
```

## Rollback Plan

In case of issues after removing the legacy files, you can restore them from version control:

```bash
git checkout <commit-before-removal> -- Echo-Notes/ai_notes_nextcloud.py Echo-Notes/ai_weekly_summary.py Echo-Notes/echo_notes_daemon.py Echo-Notes/echo_notes_dashboard.py Echo-Notes/shared/
```

Replace `<commit-before-removal>` with the appropriate commit hash.

*Source: Echo-Notes/LEGACY_FILES_CLEANUP.md*

---

## Echo-Notes Installer Migration Guide

This document provides guidance on transitioning from the old Echo-Notes installation system to the new modular installer framework.

## Overview of Changes

The Echo-Notes installation system has been completely redesigned with a modular, cross-platform architecture that provides:

- **Improved reliability** with better error handling and recovery
- **Platform-specific optimizations** for Windows, macOS, and Linux
- **Consistent user experience** across all supported platforms
- **More installation options** with flexible configuration
- **Better uninstallation support** to cleanly remove all components

## Migration Timeline

| Date | Milestone |
|------|-----------|
| May 2025 | New installer framework available (current) |
| June 2025 | Legacy installers deprecated but still functional |
| August 2025 | Legacy installers removed from repository |
| September 2025 | Only new installer framework supported |

## How to Migrate

### Automatic Migration

The easiest way to migrate is to use our migration script:

```bash
python migrate_installers.py
```

This script will:
1. Detect your current Echo-Notes installation
2. Back up your configuration and data
3. Uninstall the old version
4. Install the new version using the appropriate platform-specific installer
5. Restore your configuration and data

### Manual Migration

If you prefer to migrate manually, follow these steps:

#### Step 1: Back Up Your Data

First, make sure to back up your notes and configuration:

```bash
# Back up your notes directory
cp -r "$ECHO_NOTES_DIR" echo_notes_backup/

# Back up your configuration
cp -r ~/.config/echo-notes echo_notes_config_backup/
```

#### Step 2: Uninstall the Old Version

Run the appropriate uninstaller for your platform:

```bash
# Windows
uninstall.bat

# macOS/Linux
./uninstall.sh
```

Use the `--keep-config` option to preserve your configuration files.

#### Step 3: Install the New Version

Run the new platform-specific installer:

```bash
# Windows
python installers/install_windows.py

# macOS
./installers/install_macos.sh

# Linux
./installers/install_linux.sh
```

## Comparison of Old vs. New Installers

### Windows

| Feature | Old Installer | New Installer |
|---------|--------------|---------------|
| Installation Interface | Command-line only | GUI with options + Command-line |
| Desktop Integration | Basic shortcut | Start Menu entry + Desktop shortcut |
| Service Setup | Manual | Automatic with Task Scheduler |
| Uninstallation | Basic script | Full uninstaller with Add/Remove Programs entry |

### macOS

| Feature | Old Installer | New Installer |
|---------|--------------|---------------|
| Installation Interface | Shell script | Shell script with more options |
| Application Bundle | Basic | Full .app bundle with proper structure |
| Service Setup | Manual | Automatic LaunchAgent configuration |
| Symlinks | Manual | Automatic in /usr/local/bin |

### Linux

| Feature | Old Installer | New Installer |
|---------|--------------|---------------|
| Installation Interface | Shell script | Shell script with more options |
| Desktop Integration | Basic | Full desktop entries and icons |
| Service Setup | Manual | Automatic systemd service with fallback |
| Distribution Support | Limited | Broader support for different distributions |

## Files Being Deprecated

The following files will be deprecated and eventually removed:

- `echo_notes_installer.py` - Replaced by platform-specific installers
- `install.sh` - Replaced by `install_linux.sh` and `install_macos.sh`
- `create_macos_shortcut.py` - Functionality integrated into `macos_installer.py`
- `create_windows_shortcut.bat` - Functionality integrated into `windows_installer.py`
- `install_desktop_shortcuts.sh` - Functionality integrated into `linux_installer.py`
- `fix_desktop_icon.sh` - Functionality integrated into `linux_installer.py`

## Troubleshooting Migration Issues

### Configuration Not Migrated

If your configuration wasn't properly migrated:

```bash
# Copy your backed-up configuration
cp -r echo_notes_config_backup/* ~/.config/echo-notes/
```

### Notes Not Found After Migration

If your notes aren't being found after migration:

1. Check the value of `ECHO_NOTES_DIR` environment variable
2. Update the configuration to point to your notes directory
3. Restart the Echo-Notes daemon

### Services Not Starting

If the Echo-Notes daemon service isn't starting after migration:

#### Windows
```bash
# Check Task Scheduler
schtasks /query /tn "Echo-Notes Daemon"

# Manually start the service
schtasks /run /tn "Echo-Notes Daemon"
```

#### macOS
```bash
# Check LaunchAgent status
launchctl list | grep echo-notes

# Manually load the service
launchctl load ~/Library/LaunchAgents/com.echo-notes.daemon.plist
```

#### Linux
```bash
# Check systemd service status
systemctl --user status echo-notes-daemon

# Manually start the service
systemctl --user start echo-notes-daemon
```

## Getting Help

If you encounter any issues during migration, please:

1. Check the logs in `~/.config/echo-notes/logs/`
2. Run the installer with the `--verbose` option for more detailed output
3. Open an issue on our GitHub repository with details about the problem

## Feedback

We welcome your feedback on the new installer framework. Please share your experience and suggestions through our GitHub repository.

*Source: Echo-Notes/MIGRATION.md*

---

## Fix Installation Permission Issues and Improve Package Structure

## Description
This pull request addresses the installation permission issues that users have been experiencing and improves the overall package structure of Echo-Notes.

## Changes Made

### 1. Created Proper Python Package Structure
- Created `echo_notes` directory with `__init__.py`
- Moved Python modules into the package with more standard naming:
  - `echo_notes_daemon.py` → `echo_notes/daemon.py`
  - `echo_notes_dashboard.py` → `echo_notes/dashboard.py`
  - `ai_notes_nextcloud.py` → `echo_notes/notes_nextcloud.py`
  - `ai_weekly_summary.py` → `echo_notes/weekly_summary.py`
- Included `shared` directory in the package with `__init__.py`

### 2. Fixed Virtual Environment Setup
- Enhanced `setup_venv` function in `echo_notes_installer.py` to ensure proper permissions
- Added code to explicitly set executable permissions on Python binaries (chmod 0o755)
- This fixes the `PermissionError: [Errno 13] Permission denied: '/home/j/Echo-Notes/echo_notes_venv/bin/python'` error

### 3. Updated Setup Configuration
- Modified `setup.py` to reference modules in the new package structure
- Updated entry points to use the new module paths

### 4. Updated Uninstaller
- Added new `remove_package_dir` function to remove the echo_notes package directory
- Updated the main uninstallation function to call this new function
- Ensures complete cleanup of all installed files

### 5. Updated Documentation
- Updated `README.md` with information about the new package structure
- Created `echo_notes/README.md` to document the package organization
- Updated `CHANGELOG.md` to record our changes
- Updated installation instructions to reflect the new package structure

### 6. Added Testing
- Created `test_package.py` to verify the package structure works correctly
- Updated existing test files to work with the new package structure

## How to Test
1. Download the installer:
   ```bash
   curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/install_echo_notes.py
   chmod +x install_echo_notes.py
   ./install_echo_notes.py
   ```
2. Verify that the installation completes without permission errors
3. Test the functionality of the application
4. Test the uninstaller to ensure it properly removes all files

## Note to Reviewers
These changes significantly improve the reliability of the installation process and follow Python best practices for package structure. The changes are backward compatible and should not affect existing installations.

*Source: Echo-Notes/PULL_REQUEST.md*

---

## Echo-Notes

### Sync, Process, and Summarize Notes, Files, Emails Privately and automatically with local AI

**A privacy-first voice-to-text, file, and note cleanup pipeline powered by local LLMs.**  
- Type or capture voice-to-text notes on your phone or laptop.
- Sync them to your home computer via Nextcloud, Syncthing, or your method of choice.
- Or Drop emails, files, or articles into the folder.
- Then automatically clean, structure, summarize, or create To Do's with them using a local language model.

---

[![Lint Status](https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/actions/workflows/lint.yml/badge.svg)](https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built With Python](https://img.shields.io/badge/Built%20with-Python-blue)](https://www.python.org/)
[![Local-First](https://img.shields.io/badge/Privacy-Local%20Only-green)](#)

---

### Project Status

- MVP Stable – Actively maintained
- Focus: Local-only automation, modular design
- Recent: GUI Dashboard, Auto Summaries
- Upcoming: Mood tracking, better sync detection

---

## Why Echo-Notes?

For users who want:
- 100% local, private AI-based note and file processing
- Clean, modular architecture
- Zero reliance on cloud services

---

## How It Works

```text
[Voice or Text Input]  → [Daily & Weekly Processing]
       ↓
    [Sync]
       ↓
  [Local LLM] 
       ↓
[Clean Markdown Output]
```

---

## Installation

> **Note:** Echo-Notes has recently migrated to a new modular installer framework. The instructions below use the new installers. For information about migrating from the old installers, see [MIGRATION.md](MIGRATION.md).

### Windows

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/Echo-Notes/installers/install_windows.py

# Run the installer
python install_windows.py
```

Or download and run the installer executable from our releases page.

The Windows installer provides a graphical interface with options to:
- Choose installation directory
- Create desktop shortcuts
- Set up the Echo-Notes daemon service

Command-line options are also available:
```bash
python install_windows.py install --install-dir "C:\Echo-Notes" --no-shortcut --no-service
```

### macOS

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/Echo-Notes/installers/install_macos.sh

# Make it executable
chmod +x install_macos.sh

# Run the installer
./install_macos.sh
```

The macOS installer will:
- Create an application bundle (.app)
- Set up symlinks in /usr/local/bin
- Configure a LaunchAgent service

Command-line options:
```bash
./install_macos.sh --install-dir ~/Applications/Echo-Notes --no-app-bundle --no-symlinks --no-service
```

### Linux

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/Echo-Notes/installers/install_linux.sh

# Make it executable
chmod +x install_linux.sh

# Run the installer
./install_linux.sh
```

The Linux installer will:
- Create desktop shortcuts and application menu entries
- Set up symlinks in ~/.local/bin
- Configure a systemd service (with autostart fallback)
- Update PATH environment variable

Command-line options:
```bash
./install_linux.sh --install-dir ~/echo-notes --no-shortcuts --no-symlinks --no-service
```

For advanced manual setup, see docs/manual_install.md.

### Testing the Installation

You can test the installation process without making any changes to your system using the test framework:

```bash
# Test installation on your platform
python Echo-Notes/installers/test_framework.py --mode install

# Test uninstallation on your platform
python Echo-Notes/installers/test_framework.py --mode uninstall

# Test on a specific platform
python Echo-Notes/installers/test_framework.py --mode install --platform windows|macos|linux
```

This is useful for verifying that the installation will work correctly on your system before actually performing it.

---

## Uninstallation

See [UNINSTALL.md](UNINSTALL.md) for detailed uninstallation instructions.

---

## Features

Daily note cleanup and structuring

Weekly summaries with actionable insights

Custom prompts (see shared/prompts_config.json)

GUI Dashboard: Monitor, trigger, configure

Local LLM processing via LM Studio

Daemon support for background operation


---

## Configuration

You can customize directories and behavior using environment variables:

Variable	Description

ECHO_NOTES_DIR	Location of synced notes
ECHO_APP_DIR	Application directory (optional)


export ECHO_NOTES_DIR="/your/notes/dir"
process-notes
generate-summary


---

## Advanced Scheduling & Launchers

Echo-Notes supports built-in scheduling via a daemon and optional cron or systemd setups.

For full scheduling setup (cron/systemd, dashboard launchers), see docs/scheduling.md.


---

## Dashboard

Features:

Daemon status

Manual trigger buttons

Logs viewer


See docs/dashboard.md for usage and troubleshooting.


---

## Changelog

See CHANGELOG.md


---

## License

MIT – free to use, modify, and share.


---

## Contributing

Open to:

New AI processing modes

UX enhancements

Additional backends


PRs welcome.

*Source: Echo-Notes/README.md*

---

## Echo-Notes Reorganization Summary

## Overview

This document summarizes the changes made during the reorganization of the Echo-Notes project structure. The main goal was to convert the project into a proper Python package structure to improve maintainability and follow best practices.

## Directory Structure Comparison

### Before Reorganization

```
Echo-Notes/
├── ai_notes_nextcloud.py
├── ai_weekly_summary.py
├── echo_notes_daemon.py
├── echo_notes_dashboard.py
├── shared/
│   ├── config.py
│   ├── date_helpers.py
│   ├── file_utils.py
│   ├── llm_client.py
│   ├── prompts_config.json
│   └── schedule_config.json
├── tests/
│   ├── conftest.py
│   ├── test_file_utils.py
│   ├── test_installation.sh
│   ├── test_one_click_installer.sh
│   ├── test_package.py
│   └── test_uninstall.py
└── [other configuration and utility files]
```

### After Reorganization

```
Echo-Notes/
├── echo_notes/
│   ├── __init__.py
│   ├── daemon.py
│   ├── dashboard.py
│   ├── installer.py
│   ├── launcher.py
│   ├── notes_nextcloud.py
│   ├── weekly_summary.py
│   └── shared/
│       ├── __init__.py
│       ├── config.py
│       ├── date_helpers.py
│       ├── file_utils.py
│       ├── llm_client.py
│       ├── prompts_config.json
│       └── schedule_config.json
├── config/
│   ├── pytest.ini
│   └── icons/
│       └── Echo-Notes-Icon.png
├── Docs/
│   ├── dashboard.md
│   ├── launchers.md
│   ├── manual_install.md
│   ├── Scheduling.md
│   └── Uninstall.md
├── tests/
│   ├── conftest.py
│   ├── test_file_utils.py
│   ├── test_installation.sh
│   ├── test_one_click_installer.sh
│   ├── test_package.py
│   └── test_uninstall.py
└── [other configuration and utility files]
```

## Files Moved

1. Core Python modules moved to `echo_notes/` package:
   - `ai_notes_nextcloud.py` → `echo_notes/notes_nextcloud.py`
   - `ai_weekly_summary.py` → `echo_notes/weekly_summary.py`
   - `echo_notes_daemon.py` → `echo_notes/daemon.py`
   - `echo_notes_dashboard.py` → `echo_notes/dashboard.py`
   - `launcher.py` → `echo_notes/launcher.py`

2. Shared utilities moved to `echo_notes/shared/`:
   - `shared/config.py` → `echo_notes/shared/config.py`
   - `shared/date_helpers.py` → `echo_notes/shared/date_helpers.py`
   - `shared/file_utils.py` → `echo_notes/shared/file_utils.py`
   - `shared/llm_client.py` → `echo_notes/shared/llm_client.py`
   - `shared/prompts_config.json` → `echo_notes/shared/prompts_config.json`
   - `shared/schedule_config.json` → `echo_notes/shared/schedule_config.json`

3. Configuration files moved to `config/`:
   - `pytest.ini` → `config/pytest.ini`
   - `Echo-Notes-Icon.png` → `config/icons/Echo-Notes-Icon.png`

4. Documentation moved to `Docs/`:
   - Various documentation files consolidated in the `Docs/` directory

## Fixed Issues

1. Updated import statements in:
   - `echo_notes/dashboard.py`: Changed from `from shared import config` to `from echo_notes.shared import config`
   - `echo_notes/daemon.py`: Changed from `from shared import config` to `from echo_notes.shared import config`

## Potential Issues That Need Attention

1. **Installer Scripts**: Many installer scripts still reference the old file paths (e.g., `echo_notes_dashboard.py` instead of `echo_notes/dashboard.py`). These need to be updated to point to the new file locations.

2. **Entry Points**: The entry points in `setup.py` have been updated to use the new module paths, but any scripts or shortcuts that directly call the Python files need to be updated.

3. **Documentation**: Some documentation may still reference the old file structure and needs to be updated.

4. **Legacy Files**: The old Python files (`ai_notes_nextcloud.py`, `ai_weekly_summary.py`, `echo_notes_daemon.py`, `echo_notes_dashboard.py`) still exist in the root directory. These should be removed once all references to them have been updated.

## Next Steps

1. Update all installer scripts to reference the new file paths
2. Update any documentation that references the old file structure
3. Remove the old Python files from the root directory once all references have been updated
4. Update any shortcuts or launchers to point to the new file locations
5. Consider adding more comprehensive tests to verify the functionality of the reorganized code

*Source: Echo-Notes/REORGANIZATION_SUMMARY.md*

---

## Echo Notes Use Cases

# Echo Notes Use Cases

Echo-Notes isn't just for cleaning up notes. It's a modular, local-first automation system that works with synced files from **Nextcloud**, **Syncthing**, or any other tool that writes to disk.

Below are real-world workflows powered by Echo + local LLMs.

---

## 1. Voice Note to Structured Journal

**Flow**:  
Dictate quick thoughts into a voice-to-text app → synced to Echo folder → Echo cleans grammar, formats into Markdown journal entry, adds tags or todos.

**Prompt Example**:
```json
"Rewrite this voice note into a structured journal entry with headings, todos, and cleaned-up grammar. Use Markdown."
````

**Folder Tip**:
Use a `Journal/YYYY-MM-DD/` folder convention for organized output.

---

## 2. Weekly Summary Generator

**Flow**:
Echo collects daily journal files → generates a weekly summary with bullet points, mood indicators, and highlights.

**Prompt Example**:

```json
"Summarize the following 7 journal entries. Highlight mood trends, major events, and tasks to carry forward."
```

**Output**:
A single weekly `.md` file written to a `Summaries/` folder.

---

## 3. Research Digest

**Flow**:
Drop PDFs, articles, or note dumps into a `Reading` folder → Echo extracts key takeaways and writes a summary with tags.

**Prompt Example**:

```json
"Extract main points, arguments, and useful quotes from this article. Use Markdown with bullet points."
```

---

## 4. Idea Refinement

**Flow**:
Rough ideas or outlines dropped into a synced folder → Echo rewrites them into structured blog posts, Nostr drafts, or polished content.

**Prompt Example**:

```json
"Expand this outline into a 500-word blog post with an intro, body, and conclusion."
```

---

## 5. Code Snippet Commentary

**Flow**:
Save `.py`, `.go`, or `.sh` files to a watched `CodeDrop/` folder → Echo adds comments, refactors, or explains them.

**Prompt Example**:

```json
"Explain this code in plain English. Then suggest improvements or flag potential bugs."
```

---

## 6. Daily To-Do Extraction

**Flow**:
Capture raw daily notes → Echo extracts tasks and writes to `Todos/YYYY-MM-DD.md`.

**Prompt Example**:

```json
"Pull out any action items or todos from this note and reformat them into a checklist."
```

---

## 7. Personal Knowledge Base (PKB) Conversion

**Flow**:
Echo processes longform notes into Zettelkasten-style atomic notes, flashcards, or Q\&A pairs.

**Prompt Example**:

```json
"Split this note into individual concept cards with titles, summaries, and questions."
```

---

## 8. Nostr Draft Automation

**Flow**:
Write a longform note in Markdown → Echo generates short posts, threads, or tag suggestions for Nostr.

**Prompt Example**:

```json
"Turn this journal entry into 3 Nostr posts, each with relevant hashtags."
```

---

## 9. Mood Tracker & Emotional Tagging (WIP)

**Flow**:
Journal entries or memos → Echo scores tone/sentiment → adds metadata to frontmatter.

**Prompt Example**:

```json
"Analyze emotional tone. Tag this entry as positive, neutral, or negative. Add a brief mood summary."
```

---

## 10. Secure PDF Summarizer

**Flow**:
Drop privacy-sensitive PDFs (e.g. contracts, policies, research) into a folder → Echo summarizes offline, privately.

**Prompt Example**:

```json
"Summarize this document in plain English. Highlight key terms, risks, and action items."
```

---

## Tips for Use

* You can create multiple watch folders with different prompt configs.
* Echo is fully local, so your content stays private—no cloud processing.
* Combine with `systemd`, `cron`, or GUI Dashboard to run background jobs.

---

Got your own use case? PRs welcome!

*Source: Echo-Notes/Use_Cases.md*

---

## Echo-Notes Package

This directory contains the main Python package for Echo-Notes.

## Structure

- `__init__.py` - Package initialization
- `daemon.py` - Echo-Notes daemon for background processing
- `dashboard.py` - Echo-Notes dashboard GUI
- `notes_nextcloud.py` - Nextcloud notes integration
- `weekly_summary.py` - Weekly summary generation
- `shared/` - Shared utilities and configuration

## Usage

The package is designed to be installed via pip:

```bash
pip install -e .
```

This will install the following command-line tools:

- `echo-notes-daemon` - Start the Echo-Notes daemon
- `echo-notes-dashboard` - Launch the Echo-Notes dashboard
- `echo-notes-config` - Configure Echo-Notes scheduling
- `process-notes` - Process notes for Nextcloud integration
- `generate-summary` - Generate weekly summaries

*Source: Echo-Notes/echo_notes/README.md*

---

## Echo-Notes Installer Migration PR

## Overview

This PR consolidates the Echo-Notes installers into a modular, cross-platform framework that provides improved reliability, platform-specific optimizations, and a consistent user experience across Windows, macOS, and Linux.

## Changes Made

### Architecture Improvements

- **Modular Design**: Created a structured installer framework with common utilities and platform-specific modules
- **Improved Error Handling**: Added better error detection, reporting, and recovery mechanisms
- **Cross-Platform Consistency**: Unified command-line options and installation flow across all platforms
- **Platform-Specific Optimizations**: Enhanced integration with native OS features

### Platform-Specific Enhancements

#### Windows
- GUI-based installer with desktop integration
- Start Menu entry creation
- Windows service setup via Task Scheduler
- Uninstaller registration in Add/Remove Programs

#### macOS
- Application bundle (.app) creation
- Symlinks in /usr/local/bin
- LaunchAgent service setup

#### Linux
- Desktop shortcuts and application menu entries
- Symlinks in ~/.local/bin
- Systemd service setup with autostart fallback
- PATH environment variable configuration

### Documentation Updates

- Updated README.md with new installation instructions
- Updated UNINSTALL.md with new uninstallation instructions
- Created MIGRATION.md with guidance for transitioning from old to new installers
- Added information about the test framework to user-facing documentation

### Bug Fixes

- Fixed DownloadManager class to properly handle install_dir parameter
- Added dry_run option handling to Linux installer
- Fixed various code quality issues:
  - Removed unnecessary f-strings
  - Fixed bare except clauses
  - Removed unused imports

## Migration Path for Existing Users

Users can migrate to the new installer framework using:

1. **Automatic Migration**: Using the `migrate_installers.py` script
2. **Manual Migration**: Following the step-by-step guide in MIGRATION.md

## Testing Performed

- Tested installation and uninstallation on all supported platforms
- Verified compatibility with existing installations
- Tested migration from old to new installer system
- Validated error handling and recovery mechanisms

## File Changes

### New Files Added
- `installers/__init__.py`
- `installers/README.md`
- `installers/CHANGELOG.md`
- `installers/Project.md`
- `installers/setup.py`
- `installers/test_framework.py`
- `installers/common/__init__.py`
- `installers/common/installer_utils.py`
- `installers/common/download_manager.py`
- `installers/windows/__init__.py`
- `installers/windows/windows_installer.py`
- `installers/windows/windows_uninstaller.py`
- `installers/install_windows.py`
- `installers/macos/__init__.py`
- `installers/macos/macos_installer.py`
- `installers/macos/macos_uninstaller.py`
- `installers/install_macos.sh`
- `installers/linux/__init__.py`
- `installers/linux/linux_installer.py`
- `installers/linux/linux_uninstaller.py`
- `installers/install_linux.sh`
- `installers/tests/__init__.py`
- `installers/tests/test_installers.py`

### Modified Files
- `Echo-Notes/README.md`
- `Echo-Notes/UNINSTALL.md`
- `Echo-Notes/MIGRATION.md`
- `Echo-Notes/migrate_installers.py`

### Deprecated Files (To Be Removed Later)
- `Echo-Notes/echo_notes_installer.py`
- `Echo-Notes/install.sh`
- `Echo-Notes/create_macos_shortcut.py`
- `Echo-Notes/create_windows_shortcut.bat`
- `Echo-Notes/install_desktop_shortcuts.sh`
- `Echo-Notes/fix_desktop_icon.sh`
- `Echo-Notes/uninstall.bat`
- `Echo-Notes/uninstall.py`
- `Echo-Notes/uninstall.sh`

## Known Issues and Future Work

1. **Code Quality**: There are still style issues that should be addressed in a follow-up PR:
   - Whitespace in blank lines
   - Lines exceeding 79 characters
   - Missing newlines at end of files
   - Spacing between functions and classes

2. **Test Coverage**: Additional tests should be added to cover:
   - Edge cases in installation/uninstallation
   - Error handling scenarios
   - Migration from old to new installers

3. **Documentation**: Some additional documentation improvements:
   - More detailed examples for advanced usage
   - Troubleshooting guide for common issues

## Reviewer Notes

Please focus on:
1. The overall architecture and design of the installer framework
2. Platform-specific implementation details
3. Migration path for existing users
4. Documentation clarity and completeness

The code quality issues will be addressed in a follow-up PR.

*Source: PR_DESCRIPTION.md*

---

## Echo-Notes

### Sync, Process, and Summarize Notes, Files, Emails Privately and automatically with local AI

**A privacy-first voice-to-text, file, and note cleanup pipeline powered by local LLMs.**  
- Type or capture voice-to-text notes on your phone or laptop.
- Sync them to your home computer via Nextcloud, Syncthing, or your method of choice.
- Or Drop emails, files, or articles into the folder.
- Then automatically clean, structure, summarize, or create To Do's with them using a local language model.

## Documentation

- [Installation](Docs/installation.md)
- [Usage](Docs/usage.md)
- [Development](Docs/development.md)
- [Uninstallation](Docs/uninstallation.md)
- [Misc](Docs/misc.md)

## Features

Daily note cleanup and structuring

Weekly summaries with actionable insights

Custom prompts (see shared/prompts_config.json)

GUI Dashboard: Monitor, trigger, configure

Local LLM processing via LM Studio

Daemon support for background operation


---


## License

MIT – free to use, modify, and share.

*Source: README.md*

---

## Echo-Notes Project Streamlining

This document outlines the streamlining process for the Echo-Notes project, addressing bloat from testing scripts, utility scripts, and documentation files.

## Overview

The Echo-Notes project has grown over time, accumulating various test files, utility scripts, and documentation that may be redundant or only needed during development. This streamlining process aims to:

1. Identify essential files needed for core functionality
2. Consolidate redundant documentation
3. Organize tests into essential and development-only categories
4. Create a minimal viable project structure
5. Provide tools for maintaining a clean project structure

## Streamlining Scripts

The following scripts have been created to help with the streamlining process:

### 1. `streamline_project.py`

The main entry point for the streamlining process. This script orchestrates the entire streamlining process by running the other scripts in sequence.

**Usage:**
```bash
python streamline_project.py [--dry-run] [--skip-step STEP]
```

**Options:**
- `--dry-run`: Show what would be done without making changes
- `--skip-step STEP`: Skip a specific step (analyze, docs, tests, cleanup)

### 2. `identify_essential_files.py`

Analyzes the project structure to identify the minimal set of files needed for the project to function correctly.

**Usage:**
```bash
python identify_essential_files.py [--output OUTPUT_FILE]
```

**Options:**
- `--output OUTPUT_FILE`: Write the results to the specified file (default: essential_files.md)

### 3. `consolidate_docs.py`

Consolidates the documentation files into a more organized structure, merging redundant documentation and creating a comprehensive README.md.

**Usage:**
```bash
python consolidate_docs.py [--dry-run]
```

**Options:**
- `--dry-run`: Show what would be done without making changes

### 4. `analyze_tests.py`

Analyzes the test files to identify which tests are essential for ensuring core functionality and which ones are redundant or only used for development.

**Usage:**
```bash
python analyze_tests.py [--output OUTPUT_FILE] [--dry-run] [--consolidate]
```

**Options:**
- `--output OUTPUT_FILE`: Write the results to the specified file (default: test_analysis.md)
- `--dry-run`: Show what would be done without making changes
- `--consolidate`: Consolidate test files according to the plan

### 5. `cleanup.py`

Cleans up the project by moving development-only files to appropriate directories, consolidating redundant files, and creating a minimal viable project structure.

**Usage:**
```bash
python cleanup.py [--dry-run]
```

**Options:**
- `--dry-run`: Show what would be done without making changes

## Streamlining Process

The streamlining process follows these steps:

1. **Analysis**: Identify essential files, redundant files, and development-only files
2. **Documentation Consolidation**: Merge redundant documentation and create a comprehensive README
3. **Test Consolidation**: Organize tests into essential and development-only categories
4. **Cleanup**: Create a minimal viable project structure and move development-only files to appropriate directories

## Minimal Viable Project Structure

The minimal viable project structure includes:

```
echo_notes/          # Main package directory
├── __init__.py
├── daemon.py        # Daemon for background processing
├── dashboard.py     # GUI dashboard
├── notes_nextcloud.py # Nextcloud integration
├── weekly_summary.py # Weekly summary generation
└── shared/          # Shared utilities
    ├── __init__.py
    ├── config.py    # Configuration handling
    ├── date_helpers.py # Date manipulation utilities
    ├── file_utils.py # File operations
    ├── llm_client.py # LLM integration
    ├── prompts_config.json # LLM prompt templates
    └── schedule_config.json # Scheduling configuration

tests/              # Test directory
├── __init__.py
├── conftest.py     # Pytest configuration
└── test_file_utils.py # Tests for file utilities

Docs/               # Documentation
├── dashboard.md    # Dashboard documentation
├── launchers.md    # Launcher documentation
├── manual_install.md # Manual installation guide
├── Scheduling.md   # Scheduling documentation
└── Uninstall.md    # Uninstallation guide

# Root files
setup.py           # Package setup
requirements.txt   # Dependencies
pytest.ini         # Pytest configuration
LICENSE            # License file
CHANGELOG.md       # Changelog
README.md          # Main documentation
```

## Development Structure

For development purposes, additional directories are created:

```
tools/              # Development tools
├── cleanup/        # Cleanup scripts
├── migration/      # Migration utilities
└── dev_tests/      # Development-only tests

Docs/archive/       # Archived documentation
```

## How to Use

1. **Analyze the project**:
   ```bash
   python identify_essential_files.py
   ```

2. **Consolidate documentation**:
   ```bash
   python consolidate_docs.py
   ```

3. **Analyze and consolidate tests**:
   ```bash
   python analyze_tests.py --consolidate
   ```

4. **Run the complete streamlining process**:
   ```bash
   python streamline_project.py
   ```

5. **Create a clean distribution package**:
   ```bash
   cd dist && python cleanup.py
   ```

## Benefits of Streamlining

1. **Reduced Complexity**: Fewer files and a cleaner structure make the project easier to understand and maintain
2. **Improved Documentation**: Consolidated documentation provides a better user experience
3. **Focused Testing**: Essential tests are separated from development-only tests
4. **Smaller Distribution**: The minimal viable project is smaller and more focused
5. **Better Organization**: Development tools and utilities are properly organized

## Maintenance Guidelines

To maintain a clean project structure:

1. Keep development-only files in the `tools` directory
2. Add new tests to the appropriate directory (`tests` for essential tests, `tools/dev_tests` for development-only tests)
3. Update documentation in the `Docs` directory
4. Run the streamlining process periodically to identify and address new bloat

*Source: STREAMLINING.md*

---

## Changelog

## [Unreleased]

### Added
- Completed reorganization cleanup by removing legacy and deprecated files
- Added test scripts to verify installation and uninstallation processes

### Changed
- Removed legacy files as per LEGACY_FILES_CLEANUP.md:
  - `ai_notes_nextcloud.py` - Replaced by `echo_notes/notes_nextcloud.py`
  - `ai_weekly_summary.py` - Replaced by `echo_notes/weekly_summary.py`
  - `echo_notes_daemon.py` - Replaced by `echo_notes/daemon.py`
  - `echo_notes_dashboard.py` - Replaced by `echo_notes/dashboard.py`
  - `shared/` directory - Replaced by `echo_notes/shared/`
- Removed deprecated files as per MIGRATION.md:
  - `echo_notes_installer.py` - Replaced by platform-specific installers
  - `install.sh` - Replaced by `install_linux.sh` and `install_macos.sh`
  - `create_macos_shortcut.py` - Functionality integrated into `macos_installer.py`
  - `create_windows_shortcut.bat` - Functionality integrated into `windows_installer.py`
  - `install_desktop_shortcuts.sh` - Functionality integrated into `linux_installer.py`
  - `fix_desktop_icon.sh` - Functionality integrated into `linux_installer.py`

### Added (Previous)
- Proper Python package structure with echo_notes module
- Fixed virtual environment permissions in installer
- Updated uninstaller to remove the echo_notes package directory
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

*Source: dist/CHANGELOG.md*

---

## Scheduling Echo-Notes

# Scheduling Echo-Notes

Echo-Notes supports two main scheduling methods for note processing and summary generation:

---

## 1. Built-in Daemon (Recommended)

The built-in daemon handles background processing and scheduling automatically.

### Commands

```bash
# Start the daemon
echo-notes-daemon --daemon

# Stop the daemon
echo-notes-daemon --stop

# Configure the schedule
echo-notes-daemon --configure

# Launch the dashboard
echo-notes-dashboard

Logs & PID

Logs:

~/Documents/notes/daemon.log

~/Documents/notes/daemon.error.log


PID file:
~/Documents/notes/echo-notes.pid



---

2. Cron Jobs (Traditional)

For systems that prefer cron, use:

Hourly note processing

0 * * * * process-notes >> ~/Documents/notes/processing.log 2>&1

Weekly summary

0 12 * * 0 generate-summary >> ~/Documents/notes/weekly.log 2>&1

Ensure process-notes and generate-summary are in your $PATH or use full paths.


---

3. Running as a systemd Service (Optional)

Create a persistent background service on Linux.

Service File

[Unit]
Description=Echo-Notes Daemon
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
ExecStart=/usr/local/bin/echo-notes-daemon
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target

Setup Commands

sudo nano /etc/systemd/system/echo-notes.service
sudo systemctl enable echo-notes.service
sudo systemctl start echo-notes.service
sudo systemctl status echo-notes.service


---

Scheduling Settings

Configure via shared/schedule_config.json or use echo-notes-config.

Setting	Description	Default

processing_interval	Time between note runs (minutes)	60
summary_interval	Time between summaries (minutes)	10080
summary_day	Day of the week (0=Mon, 6=Sun)	6
summary_hour	Hour of day for weekly summary	12
daemon_enabled	Toggle the daemon on/off	true



---

Troubleshooting

Nothing runs? Check the daemon status or cron logs.

Wrong time? Check your system timezone settings.

Logs empty? Confirm correct paths in config or use full paths in cron jobs.



---

For launcher-related info, see launchers.md.

---

*Source: dist/Docs/Scheduling.md*

---

## Echo-Notes

### Sync, Process, and Summarize Notes, Files, Emails Privately and automatically with local AI

**A privacy-first voice-to-text, file, and note cleanup pipeline powered by local LLMs.**  
- Type or capture voice-to-text notes on your phone or laptop.
- Sync them to your home computer via Nextcloud, Syncthing, or your method of choice.
- Or Drop emails, files, or articles into the folder.
- Then automatically clean, structure, summarize, or create To Do's with them using a local language model.

## Documentation

- [Installation Guide](Docs/manual_install.md)
- [Dashboard Usage](Docs/dashboard.md)
- [Scheduling](Docs/Scheduling.md)
- [Uninstallation](Docs/Uninstall.md)
- [Launchers](Docs/launchers.md)

## Features

- Daily note cleanup and structuring
- Weekly summaries with actionable insights
- Custom prompts (see echo_notes/shared/prompts_config.json)
- GUI Dashboard: Monitor, trigger, configure
- Local LLM processing via LM Studio
- Daemon support for background operation

## Project Structure

The Echo-Notes project has been streamlined to have a clean, minimal structure:

```
echo_notes/          # Main package directory
├── __init__.py
├── daemon.py        # Daemon for background processing
├── dashboard.py     # GUI dashboard
├── notes_nextcloud.py # Nextcloud integration
├── weekly_summary.py # Weekly summary generation
└── shared/          # Shared utilities
    ├── __init__.py
    ├── config.py    # Configuration handling
    ├── date_helpers.py # Date manipulation utilities
    ├── file_utils.py # File operations
    ├── llm_client.py # LLM integration
    ├── prompts_config.json # LLM prompt templates
    └── schedule_config.json # Scheduling configuration

tests/              # Test directory
├── __init__.py
├── conftest.py     # Pytest configuration
└── test_file_utils.py # Tests for file utilities

Docs/               # Documentation
├── dashboard.md    # Dashboard documentation
├── launchers.md    # Launcher documentation
├── manual_install.md # Manual installation guide
├── Scheduling.md   # Scheduling documentation
└── Uninstall.md    # Uninstallation guide
```

## License

MIT – free to use, modify, and share.

*Source: dist/README.md*

---

## Echo-Notes Essential Files Report

This report identifies the minimal set of files needed for the Echo-Notes project to function correctly.

## Core Files (Essential)

These files are essential for the basic functionality of Echo-Notes:

- `Echo-Notes/config/pytest.ini`
- `Echo-Notes/echo_notes/__init__.py`
- `Echo-Notes/echo_notes/daemon.py`
- `Echo-Notes/echo_notes/dashboard.py`
- `Echo-Notes/echo_notes/launcher.py`
- `Echo-Notes/echo_notes/notes_nextcloud.py`
- `Echo-Notes/echo_notes/shared/__init__.py`
- `Echo-Notes/echo_notes/shared/config.py`
- `Echo-Notes/echo_notes/shared/date_helpers.py`
- `Echo-Notes/echo_notes/shared/file_utils.py`
- `Echo-Notes/echo_notes/shared/llm_client.py`
- `Echo-Notes/echo_notes/shared/prompts_config.json`
- `Echo-Notes/echo_notes/shared/schedule_config.json`
- `Echo-Notes/echo_notes/weekly_summary.py`
- `Echo-Notes/launcher.py`
- `Echo-Notes/pytest.ini`
- `Echo-Notes/requirements.txt`
- `Echo-Notes/setup.py`
- `dist/echo_notes/__init__.py`
- `dist/echo_notes/daemon.py`
- `dist/echo_notes/dashboard.py`
- `dist/echo_notes/notes_nextcloud.py`
- `dist/echo_notes/shared/__init__.py`
- `dist/echo_notes/shared/config.py`
- `dist/echo_notes/shared/date_helpers.py`
- `dist/echo_notes/shared/file_utils.py`
- `dist/echo_notes/shared/llm_client.py`
- `dist/echo_notes/shared/prompts_config.json`
- `dist/echo_notes/shared/schedule_config.json`
- `dist/echo_notes/weekly_summary.py`
- `dist/pytest.ini`
- `dist/requirements.txt`
- `dist/setup.py`
- `identify_essential_files.py`
- `streamline_project.py`


## Installer Files

These files are used for installing Echo-Notes:

- `Echo-Notes/echo_notes/__pycache__/installer.cpython-311.pyc`
- `Echo-Notes/echo_notes/installer.py`
- `Echo-Notes/install_echo_notes.py`
- `Echo-Notes/installers/__init__.py`
- `Echo-Notes/installers/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/installers/common/__init__.py`
- `Echo-Notes/installers/common/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/installers/common/__pycache__/download_manager.cpython-311.pyc`
- `Echo-Notes/installers/common/__pycache__/installer_utils.cpython-311.pyc`
- `Echo-Notes/installers/common/download_manager.py`
- `Echo-Notes/installers/common/installer_utils.py`
- `Echo-Notes/installers/install.py`
- `Echo-Notes/installers/install_linux.sh`
- `Echo-Notes/installers/install_macos.sh`
- `Echo-Notes/installers/install_windows.py`
- `Echo-Notes/installers/linux/__init__.py`
- `Echo-Notes/installers/linux/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/installers/linux/__pycache__/linux_installer.cpython-311.pyc`
- `Echo-Notes/installers/linux/__pycache__/linux_uninstaller.cpython-311.pyc`
- `Echo-Notes/installers/linux/fix_desktop_icon.sh`
- `Echo-Notes/installers/linux/install_desktop_shortcuts.sh`
- `Echo-Notes/installers/linux/linux_installer.py`
- `Echo-Notes/installers/linux/linux_uninstaller.py`
- `Echo-Notes/installers/macos/__init__.py`
- `Echo-Notes/installers/macos/create_shortcut.py`
- `Echo-Notes/installers/macos/macos_installer.py`
- `Echo-Notes/installers/macos/macos_uninstaller.py`
- `Echo-Notes/installers/setup.py`
- `Echo-Notes/installers/uninstall.py`
- `Echo-Notes/installers/uninstall.sh`
- `Echo-Notes/installers/windows/__init__.py`
- `Echo-Notes/installers/windows/create_shortcut.bat`
- `Echo-Notes/installers/windows/uninstall.bat`
- `Echo-Notes/installers/windows/windows_installer.py`
- `Echo-Notes/installers/windows/windows_uninstaller.py`
- `Echo-Notes/uninstall.bat`
- `Echo-Notes/uninstall.py`
- `Echo-Notes/uninstall.sh`


## Documentation Files

These files provide documentation for Echo-Notes:

- `Docs/development.md`
- `Docs/installation.md`
- `Docs/misc.md`
- `Docs/uninstallation.md`
- `Docs/usage.md`
- `Echo-Notes/CHANGELOG.md`
- `Echo-Notes/CLEANUP_SUMMARY.md`
- `Echo-Notes/Docs/Scheduling.md`
- `Echo-Notes/Docs/Uninstall.md`
- `Echo-Notes/Docs/dashboard.md`
- `Echo-Notes/Docs/launchers.md`
- `Echo-Notes/Docs/manual_install.md`
- `Echo-Notes/LEGACY_FILES_CLEANUP.md`
- `Echo-Notes/MIGRATION.md`
- `Echo-Notes/PULL_REQUEST.md`
- `Echo-Notes/README.md`
- `Echo-Notes/REORGANIZATION_SUMMARY.md`
- `Echo-Notes/TESTING.md`
- `Echo-Notes/UNINSTALL.md`
- `Echo-Notes/Use_Cases.md`
- `Echo-Notes/dashboard_readme.md`
- `Echo-Notes/echo_notes/README.md`
- `Echo-Notes/installers/CHANGELOG.md`
- `Echo-Notes/installers/Project.md`
- `Echo-Notes/installers/README.md`
- `Echo-Notes/testing.md`
- `PR_DESCRIPTION.md`
- `README.md`
- `STREAMLINING.md`
- `consolidate_docs.py`
- `dist/CHANGELOG.md`
- `dist/Docs/Scheduling.md`
- `dist/Docs/Uninstall.md`
- `dist/Docs/dashboard.md`
- `dist/Docs/launchers.md`
- `dist/Docs/manual_install.md`
- `dist/README.md`
- `essential_files.md`


## Test Files

These files are used for testing Echo-Notes:

- `Echo-Notes/installers/test_framework.py`
- `Echo-Notes/installers/tests/__init__.py`
- `Echo-Notes/installers/tests/__pycache__/test_installers.cpython-311.pyc`
- `Echo-Notes/installers/tests/test_installers.py`
- `Echo-Notes/test_installation.sh`
- `Echo-Notes/test_one_click_installer.sh`
- `Echo-Notes/test_package.py`
- `Echo-Notes/test_reorganization.py`
- `Echo-Notes/test_uninstall.py`
- `Echo-Notes/tests/conftest.py`
- `Echo-Notes/tests/test_file_utils.py`
- `Echo-Notes/tests/test_installation.sh`
- `Echo-Notes/tests/test_one_click_installer.sh`
- `Echo-Notes/tests/test_package.py`
- `Echo-Notes/tests/test_uninstall.py`
- `analyze_tests.py`
- `dist/tests/__init__.py`
- `dist/tests/conftest.py`
- `dist/tests/test_file_utils.py`
- `test_analysis.md`
- `test_streamlined_project.py`


## Development Files

These files are only needed during development:

- `Echo-Notes/Echo-Notes-Icon.png`
- `Echo-Notes/LICENSE`
- `Echo-Notes/cleanup_deprecated_files.sh`
- `Echo-Notes/cleanup_legacy_files.sh`
- `Echo-Notes/config/echo-notes-dashboard.desktop`
- `Echo-Notes/config/icons/Echo-Notes-Icon.png`
- `Echo-Notes/echo-notes-dashboard.desktop`
- `Echo-Notes/echo_notes.egg-info/PKG-INFO`
- `Echo-Notes/echo_notes.egg-info/SOURCES.txt`
- `Echo-Notes/echo_notes.egg-info/dependency_links.txt`
- `Echo-Notes/echo_notes.egg-info/entry_points.txt`
- `Echo-Notes/echo_notes.egg-info/requires.txt`
- `Echo-Notes/echo_notes.egg-info/top_level.txt`
- `Echo-Notes/echo_notes/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/echo_notes/__pycache__/daemon.cpython-311.pyc`
- `Echo-Notes/echo_notes/__pycache__/dashboard.cpython-311.pyc`
- `Echo-Notes/echo_notes/__pycache__/notes_nextcloud.cpython-311.pyc`
- `Echo-Notes/echo_notes/__pycache__/weekly_summary.cpython-311.pyc`
- `Echo-Notes/echo_notes/shared/__pycache__/__init__.cpython-311.pyc`
- `Echo-Notes/echo_notes/shared/__pycache__/config.cpython-311.pyc`
- `Echo-Notes/echo_notes/shared/__pycache__/date_helpers.cpython-311.pyc`
- `Echo-Notes/echo_notes/shared/__pycache__/file_utils.cpython-311.pyc`
- `Echo-Notes/migrate_installers.py`
- `cleanup.py`
- `dist/LICENSE`
- `dist/cleanup.py`


## Summary

- Core Files: 35

- Installer Files: 38

- Documentation Files: 38

- Test Files: 21

- Development Files: 26

- Total Files: 158

## Minimal Viable Project

The minimal viable project consists of:

1. All Core Files

2. Essential Documentation (README.md, LICENSE)

3. Main installer script


All other files can be moved to separate directories or removed for distribution.

*Source: essential_files.md*

---

