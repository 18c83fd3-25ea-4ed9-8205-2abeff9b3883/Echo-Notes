# Uninstallation

## Uninstallation

## Uninstalling Echo-Notes

# Uninstalling Echo-Notes

Echo-Notes supports multiple uninstallation methods depending on how you installed it.

---

## 1. One-Click Installer or Unified Installer

If you used `install_echo_notes.py` or `echo_notes_installer.py`, an uninstaller script was automatically created.

### Run the uninstaller:

#### On Linux/macOS:
```bash
./uninstall.sh

On Windows:

uninstall.bat

The uninstaller will:

Stop Echo-Notes processes

Remove desktop shortcuts and icons

Ask whether to keep your notes (default: yes)



---

2. Python-Based Uninstallation (All Platforms)

You can also run the platform-independent Python script:

python uninstall.py

Options:

--help: Show help message

--keep-config: Keep config files and prompts

--purge: Remove everything including your notes (USE WITH CAUTION)



---

3. Dry Run (Test Mode)

To preview what would be removed without deleting anything:

python test_uninstall.py


---

4. Manual Cleanup

If needed, remove the following manually:

Virtual environment folder (e.g. venv/)

Desktop shortcut files

Installed Echo-Notes files in your preferred directory

Any symbolic links in /usr/local/bin or similar



---

Resetting Notes or Configuration

If you want to reset just the configuration without uninstalling:

rm -rf ~/.config/echo-notes/

Or delete shared/prompts_config.json and shared/schedule_config.json to restore prompt/schedule defaults.


---

For reinstall instructions, see manual_install.md.

---

*Source: Echo-Notes/Docs/Uninstall.md*

---

## Echo-Notes Uninstallation Guide

This document provides detailed information about uninstalling Echo-Notes from your system while preserving your notes.

## Uninstallation Options

Echo-Notes provides multiple uninstallation options to accommodate different platforms and preferences:

### Windows

#### Option 1: GUI Uninstaller
Run the installer application and select the "Uninstall" tab:
```
python Echo-Notes/installers/install_windows.py
```

#### Option 2: Command Line
```bash
python Echo-Notes/installers/install_windows.py uninstall [options]
```

Available options:
- `--install-dir DIR`: Specify the installation directory
- `--purge`: Remove all data including notes (USE WITH CAUTION)

#### Option 3: Legacy Batch File
```bash
uninstall.bat
```

### macOS

#### Option 1: macOS Uninstaller Script
```bash
./Echo-Notes/installers/install_macos.sh uninstall
```

#### Option 2: Legacy Shell Script
```bash
./uninstall.sh
```

### Linux

#### Option 1: Linux Uninstaller Script
```bash
./Echo-Notes/installers/install_linux.sh uninstall
```

#### Option 2: Legacy Shell Script
```bash
./uninstall.sh
```

### Cross-Platform Python Script (All Platforms)
```bash
python Echo-Notes/uninstall.py
```

## Command-Line Options

All uninstallers support the following options:

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Show help information and exit |
| `--keep-config` | Keep configuration files during uninstallation |
| `--purge` | Remove everything including notes (USE WITH CAUTION) |
| `--verbose` | Show more detailed output during uninstallation |

Examples:
```bash
# Standard uninstallation
./Echo-Notes/installers/install_linux.sh uninstall

# Uninstall but keep configuration files
./Echo-Notes/installers/install_linux.sh uninstall --keep-config

# Remove everything including notes (CAUTION!)
./Echo-Notes/installers/install_linux.sh uninstall --purge

# Show help information
./Echo-Notes/installers/install_linux.sh uninstall --help
```

## Testing the Uninstaller

If you want to see what would be removed without actually uninstalling anything, you can use the test script:

```bash
python Echo-Notes/installers/test_framework.py --mode uninstall
```

This script will simulate the uninstallation process and show you what files would be removed, without actually removing anything.

## What Gets Removed

The uninstaller will remove the following components:

### On All Platforms
- Virtual environment (`echo_notes_venv/`)
- Configuration files (unless `--keep-config` is specified)
- Entry points and command-line tools

### On Windows
- Desktop shortcut
- Start Menu entry
- Windows Task Scheduler tasks
- Registry entries for uninstaller

### On macOS
- Application bundle in `~/Applications/`
- Symlinks in `/usr/local/bin/`
- LaunchAgent service files

### On Linux
- Desktop shortcuts in `~/.local/share/applications/`
- Desktop icons on the desktop
- Application icon in `~/.local/share/icons/`
- Symlinks in `~/.local/bin/`
- Systemd service files

## What Gets Preserved

By default, the uninstaller preserves:
- Your notes directory (typically `~/Documents/notes/log` or the location specified by `ECHO_NOTES_DIR`)
- The Echo-Notes directory itself (you'll be prompted to delete it manually if desired)

If you use the `--purge` option, your notes directory will also be removed. Use this option with caution!

## Manual Cleanup

After running the uninstaller, you may want to:
1. Delete the Echo-Notes directory if you no longer need it
2. Remove any environment variables you may have set (e.g., `ECHO_NOTES_DIR`)
3. Remove any systemd services if you set them up manually

## Troubleshooting

If you encounter any issues during uninstallation:

1. **Permission Denied**: Try running the uninstaller with elevated privileges (e.g., `sudo ./Echo-Notes/installers/linux/linux_uninstaller.py` on Linux/macOS)
2. **Files Not Removed**: Some files may be in use. Try stopping all Echo-Notes processes before uninstalling.
3. **Script Not Found**: Make sure you're running the uninstaller from the Echo-Notes directory.

## Reinstallation

If you want to reinstall Echo-Notes after uninstallation:

1. If you kept the Echo-Notes directory, simply run the appropriate installer for your platform again
2. If you deleted the directory, download the installer again and run it

Your notes will still be available if you didn't use the `--purge` option during uninstallation.

*Source: Echo-Notes/UNINSTALL.md*

---

*Source: Docs/uninstallation.md*

---

## Uninstalling Echo-Notes

# Uninstalling Echo-Notes

Echo-Notes supports multiple uninstallation methods depending on how you installed it.

---

## 1. One-Click Installer or Unified Installer

If you used `install_echo_notes.py` or `echo_notes_installer.py`, an uninstaller script was automatically created.

### Run the uninstaller:

#### On Linux/macOS:
```bash
./uninstall.sh

On Windows:

uninstall.bat

The uninstaller will:

Stop Echo-Notes processes

Remove desktop shortcuts and icons

Ask whether to keep your notes (default: yes)



---

2. Python-Based Uninstallation (All Platforms)

You can also run the platform-independent Python script:

python uninstall.py

Options:

--help: Show help message

--keep-config: Keep config files and prompts

--purge: Remove everything including your notes (USE WITH CAUTION)



---

3. Dry Run (Test Mode)

To preview what would be removed without deleting anything:

python test_uninstall.py


---

4. Manual Cleanup

If needed, remove the following manually:

Virtual environment folder (e.g. venv/)

Desktop shortcut files

Installed Echo-Notes files in your preferred directory

Any symbolic links in /usr/local/bin or similar



---

Resetting Notes or Configuration

If you want to reset just the configuration without uninstalling:

rm -rf ~/.config/echo-notes/

Or delete shared/prompts_config.json and shared/schedule_config.json to restore prompt/schedule defaults.


---

For reinstall instructions, see manual_install.md.

---

*Source: Echo-Notes/Docs/Uninstall.md*

---

## Echo-Notes Uninstallation Guide

This document provides detailed information about uninstalling Echo-Notes from your system while preserving your notes.

## Uninstallation Options

Echo-Notes provides multiple uninstallation options to accommodate different platforms and preferences:

### Windows

#### Option 1: GUI Uninstaller
Run the installer application and select the "Uninstall" tab:
```
python Echo-Notes/installers/install_windows.py
```

#### Option 2: Command Line
```bash
python Echo-Notes/installers/install_windows.py uninstall [options]
```

Available options:
- `--install-dir DIR`: Specify the installation directory
- `--purge`: Remove all data including notes (USE WITH CAUTION)

#### Option 3: Legacy Batch File
```bash
uninstall.bat
```

### macOS

#### Option 1: macOS Uninstaller Script
```bash
./Echo-Notes/installers/install_macos.sh uninstall
```

#### Option 2: Legacy Shell Script
```bash
./uninstall.sh
```

### Linux

#### Option 1: Linux Uninstaller Script
```bash
./Echo-Notes/installers/install_linux.sh uninstall
```

#### Option 2: Legacy Shell Script
```bash
./uninstall.sh
```

### Cross-Platform Python Script (All Platforms)
```bash
python Echo-Notes/uninstall.py
```

## Command-Line Options

All uninstallers support the following options:

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Show help information and exit |
| `--keep-config` | Keep configuration files during uninstallation |
| `--purge` | Remove everything including notes (USE WITH CAUTION) |
| `--verbose` | Show more detailed output during uninstallation |

Examples:
```bash
# Standard uninstallation
./Echo-Notes/installers/install_linux.sh uninstall

# Uninstall but keep configuration files
./Echo-Notes/installers/install_linux.sh uninstall --keep-config

# Remove everything including notes (CAUTION!)
./Echo-Notes/installers/install_linux.sh uninstall --purge

# Show help information
./Echo-Notes/installers/install_linux.sh uninstall --help
```

## Testing the Uninstaller

If you want to see what would be removed without actually uninstalling anything, you can use the test script:

```bash
python Echo-Notes/installers/test_framework.py --mode uninstall
```

This script will simulate the uninstallation process and show you what files would be removed, without actually removing anything.

## What Gets Removed

The uninstaller will remove the following components:

### On All Platforms
- Virtual environment (`echo_notes_venv/`)
- Configuration files (unless `--keep-config` is specified)
- Entry points and command-line tools

### On Windows
- Desktop shortcut
- Start Menu entry
- Windows Task Scheduler tasks
- Registry entries for uninstaller

### On macOS
- Application bundle in `~/Applications/`
- Symlinks in `/usr/local/bin/`
- LaunchAgent service files

### On Linux
- Desktop shortcuts in `~/.local/share/applications/`
- Desktop icons on the desktop
- Application icon in `~/.local/share/icons/`
- Symlinks in `~/.local/bin/`
- Systemd service files

## What Gets Preserved

By default, the uninstaller preserves:
- Your notes directory (typically `~/Documents/notes/log` or the location specified by `ECHO_NOTES_DIR`)
- The Echo-Notes directory itself (you'll be prompted to delete it manually if desired)

If you use the `--purge` option, your notes directory will also be removed. Use this option with caution!

## Manual Cleanup

After running the uninstaller, you may want to:
1. Delete the Echo-Notes directory if you no longer need it
2. Remove any environment variables you may have set (e.g., `ECHO_NOTES_DIR`)
3. Remove any systemd services if you set them up manually

## Troubleshooting

If you encounter any issues during uninstallation:

1. **Permission Denied**: Try running the uninstaller with elevated privileges (e.g., `sudo ./Echo-Notes/installers/linux/linux_uninstaller.py` on Linux/macOS)
2. **Files Not Removed**: Some files may be in use. Try stopping all Echo-Notes processes before uninstalling.
3. **Script Not Found**: Make sure you're running the uninstaller from the Echo-Notes directory.

## Reinstallation

If you want to reinstall Echo-Notes after uninstallation:

1. If you kept the Echo-Notes directory, simply run the appropriate installer for your platform again
2. If you deleted the directory, download the installer again and run it

Your notes will still be available if you didn't use the `--purge` option during uninstallation.

*Source: Echo-Notes/UNINSTALL.md*

---

## Uninstalling Echo-Notes

# Uninstalling Echo-Notes

Echo-Notes supports multiple uninstallation methods depending on how you installed it.

---

## 1. One-Click Installer or Unified Installer

If you used `install_echo_notes.py` or `echo_notes_installer.py`, an uninstaller script was automatically created.

### Run the uninstaller:

#### On Linux/macOS:
```bash
./uninstall.sh

On Windows:

uninstall.bat

The uninstaller will:

Stop Echo-Notes processes

Remove desktop shortcuts and icons

Ask whether to keep your notes (default: yes)



---

2. Python-Based Uninstallation (All Platforms)

You can also run the platform-independent Python script:

python uninstall.py

Options:

--help: Show help message

--keep-config: Keep config files and prompts

--purge: Remove everything including your notes (USE WITH CAUTION)



---

3. Dry Run (Test Mode)

To preview what would be removed without deleting anything:

python test_uninstall.py


---

4. Manual Cleanup

If needed, remove the following manually:

Virtual environment folder (e.g. venv/)

Desktop shortcut files

Installed Echo-Notes files in your preferred directory

Any symbolic links in /usr/local/bin or similar



---

Resetting Notes or Configuration

If you want to reset just the configuration without uninstalling:

rm -rf ~/.config/echo-notes/

Or delete shared/prompts_config.json and shared/schedule_config.json to restore prompt/schedule defaults.


---

For reinstall instructions, see manual_install.md.

---

*Source: dist/Docs/Uninstall.md*

---

