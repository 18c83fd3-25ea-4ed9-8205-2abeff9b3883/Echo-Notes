

# Uninstalling Echo-Notes

Echo-Notes supports multiple uninstallation methods depending on how you installed it..

---

## 1. One-Click Installer or Unified Installer

If you used the installer script or the wrapper script, uninstaller scripts should be available in your home directory.

### Run the uninstaller:

#### On Linux/macOS:
```bash
./uninstall.sh
```

Or use the Python uninstaller:
```bash
python3 uninstall.py
```

> **Note:** If you don't see the uninstaller scripts in your home directory after using the standard installer, try using our wrapper script instead:
> ```bash
> curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/install_echo_notes.sh
> chmod +x install_echo_notes.sh
> ./install_echo_notes.sh
> ```
> This wrapper script ensures that uninstaller scripts are properly created in your home directory.

#### On Windows:
```
uninstall.bat
```

The uninstaller will:
- Stop Echo-Notes processes
- Remove desktop shortcuts and icons
- Remove systemd service or startup entries
- Ask whether to keep your notes (default: yes)
- Ask whether to remove the installation directory

---

## 2. Python-Based Uninstallation (All Platforms)

You can also run the platform-independent Python script:

```bash
python uninstall.py
```

Options:
- `--help`: Show help message
- `--install-dir DIR`: Specify installation directory
- `--purge`: Remove everything including your notes (USE WITH CAUTION)

---

## 3. Manual Cleanup

If needed, remove the following manually:

- Virtual environment folder (e.g., `echo_notes_venv/`)
- Desktop shortcut files
- Installed Echo-Notes files in your preferred directory
- Any symbolic links in `~/.local/bin` or similar
- Systemd service files in `~/.config/systemd/user/`
- Autostart entries in `~/.config/autostart/`

---

## Resetting Notes or Configuration

If you want to reset just the configuration without uninstalling:

```bash
rm -rf ~/.config/echo-notes/
```

Or delete `shared/schedule_config.json` to restore schedule defaults.

---

For reinstall instructions, see [manual_install.md](manual_install.md).

---
