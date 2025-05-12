# Echo-Notes

### Sync, Process, and Summarize Notes, Files, Emails Privately and automatically with local AI

**A privacy-first voice-to-text, file, and note cleanup pipeline powered by local LLMs.**  
- Type or capture voice-to-text notes on your phone or laptop.
- Sync them to your home computer via Nextcloud, Syncthing, or your method of choice.
- Or Drop emails, files, or articles into the folder.
- Then automatically clean, structure, summarize, or create To Do's with them using a local language model..

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
