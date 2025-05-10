
# Echo-Notes

### Sync, Process, and Summarize Notes Privately and automatically with local AI

**A privacy-first voice-to-text and note cleanup pipeline powered by local LLMs.**  
Type or capture voice-to-text notes on your phone or laptop.
Sync them to your home computer via Nextcloud, Syncthing, or your method of choice. Then automatically clean, structure, and create To Do's with them using a local language model.

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
- 100% local, private AI-based note processing
- Nextcloud integration
- Clean, modular Python architecture
- Zero reliance on cloud services

---

## How It Works

```text
[Voice Input] → [Nextcloud Sync] → [Daily & Weekly Processing]
       ↓               ↓
    [Local LLM] → [Clean Markdown Output]
```

---

## Installation

Option 1: One-Click Installer (Recommended)
```bash
curl -O https://raw.githubusercontent.com/.../install_echo_notes.py
chmod +x install_echo_notes.py
./install_echo_notes.py
```
Installs the app, configures environment, sets up daemon and shortcuts.

Option 2: Manual Installation
```bash
git clone https://github.com/.../Echo-Notes
cd Echo-Notes
python echo_notes_installer.py
```
Sets up environment, dependencies, and optional daemon.

For advanced manual setup, see docs/manual_install.md.


---

## Uninstallation

Run the generated uninstaller:

Windows: uninstall.bat

macOS/Linux: ./uninstall.sh


For full options and manual steps, see docs/uninstall.md.


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
