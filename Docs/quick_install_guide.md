# Echo-Notes Quick Installation Guide

This guide provides simple instructions for installing Echo-Notes using our one-click installers.

## Linux Installation

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/installers/install_linux.sh

# Make it executable
chmod +x install_linux.sh

# Run the installer
./install_linux.sh
```

Alternatively, you can use our wrapper script which ensures uninstaller scripts are properly created:

```bash
# Download the wrapper script
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/install_echo_notes.sh

# Make it executable
chmod +x install_echo_notes.sh

# Run the wrapper script
./install_echo_notes.sh
```

The Linux installer will:
- Create desktop shortcuts and application menu entries
- Set up symlinks in ~/.local/bin
- Configure a systemd service (with autostart fallback)
- Update PATH environment variable

### Command-line options

```bash
./install_linux.sh --install-dir ~/echo-notes --no-shortcuts --no-symlinks --no-service
```

## macOS Installation

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/installers/install_macos.sh

# Make it executable
chmod +x install_macos.sh

# Run the installer
./install_macos.sh
```

The macOS installer will:
- Create an application bundle (.app)
- Set up symlinks in /usr/local/bin
- Configure a LaunchAgent service

### Command-line options

```bash
./install_macos.sh --install-dir ~/Applications/Echo-Notes --no-app-bundle --no-symlinks --no-service
```

## Windows Installation

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/installers/install_windows.py

# Run the installer
python install_windows.py
```

The Windows installer provides a graphical interface with options to:
- Choose installation directory
- Create desktop shortcuts
- Set up the Echo-Notes daemon service

### Command-line options

```bash
python install_windows.py install --install-dir "C:\Echo-Notes" --no-shortcut --no-service
```

## Troubleshooting

If you encounter any issues during installation:

1. **404 Not Found Error**: Make sure you're using the correct URL for downloading the installer.

2. **Permission Denied**: Make sure you've made the installer executable with `chmod +x install_*.sh`.

3. **Python Not Found**: Ensure Python 3.6+ is installed on your system.

4. **Missing Dependencies**: The installer will check for required dependencies and prompt you to install them if needed.

5. **Installation Directory Issues**: If you're having trouble with the default installation directory, specify a custom one using the `--install-dir` option.

For more detailed installation instructions, see [installation.md](installation.md) or [manual_install.md](manual_install.md).