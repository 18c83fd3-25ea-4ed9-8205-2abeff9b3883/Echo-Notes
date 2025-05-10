

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
