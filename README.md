# Echo-Notes
### AI Notes with Nextcloud

**A privacy-first voice-to-text and note cleanup pipeline powered by local LLMs.**  
Capture voice notes on your phone, sync them via Nextcloud, and automatically clean or structure them using a local language model.

---

[![Lint Status](https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/actions/workflows/lint.yml/badge.svg)](https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built With Python](https://img.shields.io/badge/Built%20with-Python-blue)](https://www.python.org/)
[![Local-First](https://img.shields.io/badge/Privacy-Local%20Only-green)](#)

---

### Active Project Status: WIP (MVP Stable)

**Focus:**  
- Local-only automation  
- Modular architecture
- Proper Python package structure

## Package Structure

Echo-Notes is now organized as a proper Python package:

```
echo_notes/
├── __init__.py
├── daemon.py
├── dashboard.py
├── notes_nextcloud.py
├── weekly_summary.py
└── shared/
    ├── __init__.py
    ├── config.py
    ├── date_helpers.py
    ├── file_utils.py
    ├── llm_client.py
    ├── prompts_config.json
    └── schedule_config.json
```

This structure allows for proper installation via pip and ensures all components are correctly importable.  
- Privacy-first LLM workflows  
- Auto weekly summaries

**Upcoming:**
- Mood tracking integration
- Sync install check
- NextCloud app intergration???

**Recently Added:**
- GUI Dashboard for daemon control and monitoring

---

## Why This?

This project is designed for users who:
- Want a 100% local, private note-to-AI system
- Use Nextcloud for syncing and note-taking
- Prefer clean architecture with shared modules
- Need automated processing without cloud services
- Want to focus on the idea, not the note taking

---

## ⚙How It Works

```text
[Integrated Voice-to-Text Input]
       ↓
[Nextcloud Notes Sync]
       ↓
[Modular Python Processing]
       ├── Daily Note Cleaning
       └── Weekly Summarization
       ↓
[Local LLM (LM Studio)]
       ↓
[Structured Markdown Outputs]
```

## 🗂 Project Structure
```text
Echo-Notes/
├── shared/               # Core modules
│   ├── config.py        # Paths and settings
│   ├── file_utils.py    # File operations
│   ├── llm_client.py    # AI integration
│   ├── prompts_config.json # Customizable prompts
│   └── date_helpers.py  # Date utilities
├── setup.py             # Installation config
├── requirements.txt     # Dependencies
└── ...                  # Other project files
```


## 🛠 Installation

### Option 1: One-Click Installation (Recommended)
Download and run the one-click installer:

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/install_echo_notes.py

# Make it executable
chmod +x install_echo_notes.py

# Run the installer
./install_echo_notes.py
```

This one-click installer will:
- Download the latest version of Echo-Notes
- Install it to your preferred location
- Set up the environment
- Create desktop shortcuts
- Start the daemon automatically
- Create an uninstaller

### Option 2: Manual Installation
1. Download and extract Echo-Notes
   ```bash
   git clone https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes
   cd Echo-Notes
   ```

2. Run the unified installer
   ```bash
   python echo_notes_installer.py
   ```
   
   This installer will:
   - Check for Python 3
   - Set up a virtual environment
   - Install dependencies
   - Configure the application
   - Create desktop shortcuts
   - Start the daemon automatically
   - Create an uninstaller

3. Start using the application:
   - Launch the dashboard using the desktop shortcut
   - Or run: `echo-notes-dashboard`

### Option 3: Traditional Installation
   ```bash
   # Clone the repository
   git clone https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes
   cd Echo-Notes
   
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install the package
   pip install -e .
   
   # Start the daemon
   echo-notes-daemon --daemon
   
   # Launch the dashboard
   echo-notes-dashboard
   ```
   
   This method installs Echo-Notes as a proper Python package, making all components correctly importable.

## 🗑 Uninstallation

### Option 1: Simplified Uninstallation (Recommended)
If you installed Echo-Notes using the unified installer, simply run the uninstaller:

#### On Windows:
```
uninstall.bat
```

#### On Linux/macOS:
```bash
./uninstall.sh
```

The uninstaller will:
1. Stop any running Echo-Notes processes
2. Remove desktop shortcuts and application menu entries
3. Remove icons and symlinks
4. Ask if you want to keep your notes (preserved by default)

### Option 2: Traditional Uninstallation
Echo-Notes also provides additional uninstallation options:

```bash
# Bash Script (Linux/macOS/Git Bash on Windows)
./uninstall.sh

# Batch File (Windows)
uninstall.bat

# Python Script (All Platforms)
python uninstall.py
```

These scripts support additional options:
- `--help` - Show help information
- `--keep-config` - Uninstall but keep configuration files
- `--purge` - Remove everything including notes (USE WITH CAUTION)

For detailed uninstallation instructions and options, see [UNINSTALL.md](UNINSTALL.md).

You can also run `./test_uninstall.py` to see what would be removed without actually uninstalling anything.

## 🔧 Scheduling Configuration

Echo-Notes now supports two methods for scheduling note processing and summary generation:

### Option 1: Cron Configuration (Traditional)
Hourly processing:

```text
0 * * * * process-notes >> ~/Documents/notes/processing.log 2>&1
```
Weekly summary:

```text
0 12 * * 0 generate-summary >> ~/Documents/notes/weekly.log 2>&1
```

### Option 2: Built-in Daemon (New)
Echo-Notes now includes a built-in daemon that can handle scheduling without cron:

```text
# Configure scheduling settings
echo-notes-config

# Start the daemon in true background mode (detached from terminal)
echo-notes-daemon --daemon

# Stop the daemon
echo-notes-daemon --stop

# Or start with the configuration option directly
echo-notes-daemon --configure

# Launch the GUI dashboard from command line
echo-notes-dashboard
```

### GUI Dashboard Shortcuts

Echo-Notes now includes multiple ways to launch the dashboard without using the command line:

#### Simple Double-Click Launcher (All Platforms):
The easiest way to launch the dashboard is to simply double-click the `launcher.py` file in the Echo-Notes directory. This works on all platforms (Windows, macOS, Linux) and doesn't require any installation.

#### Linux:
```bash
# Install desktop shortcuts
./install_desktop_shortcuts.sh
```
After running this script, you'll find "Echo Notes Dashboard" in your applications menu and on your desktop.

If you encounter issues with the desktop icon not launching the application, try one of these alternatives:

1. Fix desktop icon issues:
```bash
# Fix desktop icon issues
./fix_desktop_icon.sh
```
This script fixes path issues in the desktop shortcut by using absolute paths.

2. Use the launcher script:
```bash
# Run the Python launcher
python launcher.py
```

> **Note:** The desktop icon now directly uses the Python interpreter from the virtual environment, which is more reliable than using bash scripts. If you're upgrading from a previous version and the desktop icon doesn't work, run `./fix_desktop_icon.sh` to update it.
>
> Two desktop icons are created: a standard one and a "Direct" version. If the standard icon doesn't work, try the "Direct" version which is known to work reliably across different desktop environments.

#### Windows:
```bash
# Create desktop shortcut
create_windows_shortcut.bat
```
This will create a shortcut on your desktop that you can double-click to launch the dashboard.

#### macOS:
```bash
# Create macOS application
python create_macos_shortcut.py
```
This will create an application in your ~/Applications folder that you can launch like any other macOS app.

The daemon reads scheduling settings from `shared/schedule_config.json`, which can be modified directly or through the configuration tool.

When run with the `--daemon` flag, the process will:
- Detach completely from the terminal
- Continue running in the background even if you close the terminal
- Write logs to `~/Documents/notes/daemon.log` and `~/Documents/notes/daemon.error.log`
- Create a PID file at `~/Documents/notes/echo-notes.pid` for tracking

#### Running as a Systemd Service

For a more robust setup, you can run the daemon as a systemd service:

1. Create a systemd service file:

```text
sudo nano /etc/systemd/system/echo-notes.service
```

2. Add the following content:

```text
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
```

3. Enable and start the service:

```text
sudo systemctl enable echo-notes.service
sudo systemctl start echo-notes.service
```

4. Check status:

```text
sudo systemctl status echo-notes.service
```

#### Scheduling Options

The following scheduling options can be configured:

| Option | Description | Default |
|--------|-------------|---------|
| `processing_interval` | Minutes between note processing runs | 60 (hourly) |
| `summary_interval` | Minutes between summary generation | 10080 (weekly) |
| `summary_day` | Day of week for summary (0=Monday, 6=Sunday) | 6 (Sunday) |
| `summary_hour` | Hour of day for summary (0-23) | 12 (noon) |
| `daemon_enabled` | Whether the daemon is active | true |

## Core Features
- Daily Processing (process-notes)
- Automatic note cleanup and structuring

- Task extraction with checklists

- Smart date parsing from content

- Error-resilient processing
- Customizable prompts for note processing

### GUI Dashboard
- Monitor daemon status (running/not running)
- View timestamps of last processed note and weekly summary
- Control buttons to start/stop daemon and trigger processing
- Real-time log display
- For details, see [dashboard_readme.md](dashboard_readme.md)

### Weekly Summary (generate-summary)
- Aggregates 7 days of notes

- Identifies key themes and progress

- Generates actionable next steps

- Creates consolidated Markdown report

## Customizable Prompts

Echo-Notes now supports customizable prompts through the `shared/prompts_config.json` file. This allows you to modify how the AI processes your notes without changing any code.

Available prompts:
- `daily_notes_prompt`: Controls how individual notes are processed and structured
- `weekly_summary_prompt`: Defines how weekly summaries are generated

To customize:
1. Edit the `shared/prompts_config.json` file
2. Modify the prompt text while keeping the placeholder variables (e.g., `{now}`, `{combined_text}`)
3. Save the file - changes will be applied on the next processing run

## Configuration

Echo-Notes supports the following environment variables for flexible configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `ECHO_NOTES_DIR` | Location of Nextcloud notes | `~/Documents/notes/log` |
| `ECHO_APP_DIR` | Location of Echo-Notes application | Auto-detected from script location |

Example usage:
```bash
# Use a different notes directory
export ECHO_NOTES_DIR="/path/to/your/notes"

# Run the scripts
process-notes
generate-summary
```

## Changelog
See CHANGELOG.md for full version history.

## License
MIT - Use, modify, and share freely.

## 🙋 Support
Feel free to fork and adapt. PRs welcome for:

- New analysis modes

- Enhanced error handling

- Additional storage backends

- UI integrations
