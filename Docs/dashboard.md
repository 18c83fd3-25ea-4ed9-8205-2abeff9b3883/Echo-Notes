
# Echo-Notes Dashboard

The Echo-Notes Dashboard is a graphical interface for controlling and monitoring the app’s behavior.

---

## Features

- Start/stop the daemon
- Trigger note processing or weekly summary manually
- View real-time logs
- Check timestamps of last processed and summarized notes
- Adjust scheduling and config via buttons

---

## Launch the Dashboard

### From Command Line

```bash
echo-notes-dashboard

Or:

python launcher.py

From Desktop

After using the installer or shortcut script:

Linux: Open from app menu or desktop

Windows: Use desktop shortcut (Echo Notes Dashboard)

macOS: Use app in ~/Applications



---

Components Overview

Daemon Status: Shows whether the background process is running.

Trigger Buttons: Run daily cleanup or weekly summaries on-demand.

Log Panel: Real-time feedback pulled from the daemon logs.

Settings Panel (coming soon): In-app configuration instead of editing JSON directly.



---

Troubleshooting

Dashboard won’t launch?

Make sure you’ve activated the virtual environment.

Run via terminal: python launcher.py

Check for missing dependencies with: pip install -r requirements.txt


Daemon isn't running?

Start it manually: echo-notes-daemon --daemon

Check logs at:

~/Documents/notes/daemon.log

~/Documents/notes/daemon.error.log



Desktop icon doesn’t work?

Run ./fix_desktop_icon.sh to repair it.




---

Logs Location

Default log files are stored in:

~/Documents/notes/
  ├── daemon.log
  ├── daemon.error.log
  ├── processing.log
  └── weekly.log

These logs are also viewable directly in the dashboard’s live log view.


---

For shortcut setup, see launchers.md.
For background scheduling, see scheduling.md.

---
