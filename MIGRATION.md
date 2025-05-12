# Echo-Notes Installer Migration Guide

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