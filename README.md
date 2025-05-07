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
- Privacy-first LLM workflows  
- Auto weekly summaries

**Upcoming:**
- Optional journaling dashboard
- Mood tracking integration
- Sync install check
- NextCloud app intergration???

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
### Clone repository
```text
git clone https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes

cd Echo-Notes
```
### Install with pip (recommended)
```text
pip install -e .
```
### Alternative: Install requirements only
```text
pip install -r requirements.txt
```
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
```

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
