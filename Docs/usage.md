# Usage

## Usage

## Echo-Notes Dashboard

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

*Source: Echo-Notes/Docs/dashboard.md*

---

## Echo-Notes Launch Options

# Echo-Notes Launch Options

Echo-Notes includes several ways to launch the dashboard and start the daemon, depending on your platform.

---

## 1. Cross-Platform: Python Launcher

Works on all platforms:

```bash
python launcher.py

This opens the GUI dashboard directly using your configured environment.


---

2. Desktop Shortcuts

Linux

Create application shortcuts:

./install_desktop_shortcuts.sh

After running, check your desktop or application menu for:

Echo Notes Dashboard

Echo Notes Dashboard (Direct) – more reliable on some systems


If the shortcut doesn't work:

./fix_desktop_icon.sh

This updates paths in .desktop files to point to the correct Python interpreter.


---

Windows

Run:

create_windows_shortcut.bat

This creates a .lnk desktop shortcut to the dashboard. Ensure Python is properly installed and accessible from PATH.


---

macOS

Run:

python create_macos_shortcut.py

This creates a clickable .app bundle in ~/Applications.

You may need to grant it permissions via System Settings > Privacy & Security.


---

3. Terminal Shortcuts

The following commands work after installation:

echo-notes-dashboard    # Open the dashboard
echo-notes-daemon       # Run daemon in foreground
echo-notes-daemon --daemon  # Run as background process
echo-notes-daemon --stop    # Stop background daemon

These are symlinked to your environment by the installer or setup.py.


---

Troubleshooting

If a shortcut doesn’t launch:

Try the “Direct” version

Run ./fix_desktop_icon.sh

Ensure Python is available in PATH

Re-run the installer or create shortcuts again




---

For systemd and cron scheduling, see scheduling.md.

*Source: Echo-Notes/Docs/launchers.md*

---

## Echo-Notes Dashboard

A minimal, responsive GUI dashboard for monitoring and controlling the Echo-Notes daemon.

## Features

- Display daemon status (running/not running)
- Show timestamps of last processed note and weekly summary
- Control buttons to:
  - Start/stop the daemon
  - Manually trigger note processing
  - Manually trigger weekly summary generation
- Real-time log display

## Installation

Make sure you have all the required dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage

### Simple Double-Click Launcher (Recommended)

The easiest way to launch the dashboard is to simply double-click the `launcher.py` file in the Echo-Notes directory. This works on all platforms (Windows, macOS, Linux) and doesn't require any installation.

### Command Line Launch

To launch the dashboard from the command line:

```bash
# If installed via pip
echo-notes-dashboard

# Or directly from the project directory
python Echo-Notes/echo_notes_dashboard.py
```

### Desktop Shortcuts

You can also create desktop shortcuts to launch the dashboard without using the command line:

#### Linux:
```bash
# Install desktop shortcut
./install_desktop_shortcut.sh
```
After running this script, you'll find "Echo Notes Dashboard" in your applications menu.

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

## Dashboard Overview

### Status Section
Shows whether the daemon is running and displays timestamps of the last processed note and weekly summary.

### Controls Section
- **Start/Stop Daemon**: Toggle the daemon process on/off
- **Process Notes Now**: Manually trigger the note processing
- **Generate Summary Now**: Manually trigger the weekly summary generation

### Logs Section
Displays real-time logs from the Echo-Notes system, including daemon status updates and processing information.

## Requirements

- PyQt6 for the GUI components
- A running LLM server at the URL specified in `shared/config.py` (default: http://localhost:8080/v1/chat/completions) for note processing and summary generation
  - If the LLM server is not available, the dashboard will display a warning message and skip the processing

### Note on LLM Server
The dashboard checks for the availability of the LLM server before attempting to process notes or generate summaries. If the server is not available, it will log a warning message and skip the processing, allowing you to still use the dashboard for monitoring and controlling the daemon.

## Technical Details

The dashboard communicates with the Echo-Notes daemon using the same mechanisms as the command-line interface. It:

1. Checks for the PID file to determine if the daemon is running
2. Uses subprocess to start/stop the daemon
3. Directly calls the note processing and summary generation functions for manual triggers
4. Monitors the notes directory for changes to update timestamps

All operations that might block the UI are run in separate threads to keep the interface responsive.

*Source: Echo-Notes/dashboard_readme.md*

---

*Source: Docs/usage.md*

---

## Echo-Notes Dashboard

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

*Source: Echo-Notes/Docs/dashboard.md*

---

## Echo-Notes Launch Options

# Echo-Notes Launch Options

Echo-Notes includes several ways to launch the dashboard and start the daemon, depending on your platform.

---

## 1. Cross-Platform: Python Launcher

Works on all platforms:

```bash
python launcher.py

This opens the GUI dashboard directly using your configured environment.


---

2. Desktop Shortcuts

Linux

Create application shortcuts:

./install_desktop_shortcuts.sh

After running, check your desktop or application menu for:

Echo Notes Dashboard

Echo Notes Dashboard (Direct) – more reliable on some systems


If the shortcut doesn't work:

./fix_desktop_icon.sh

This updates paths in .desktop files to point to the correct Python interpreter.


---

Windows

Run:

create_windows_shortcut.bat

This creates a .lnk desktop shortcut to the dashboard. Ensure Python is properly installed and accessible from PATH.


---

macOS

Run:

python create_macos_shortcut.py

This creates a clickable .app bundle in ~/Applications.

You may need to grant it permissions via System Settings > Privacy & Security.


---

3. Terminal Shortcuts

The following commands work after installation:

echo-notes-dashboard    # Open the dashboard
echo-notes-daemon       # Run daemon in foreground
echo-notes-daemon --daemon  # Run as background process
echo-notes-daemon --stop    # Stop background daemon

These are symlinked to your environment by the installer or setup.py.


---

Troubleshooting

If a shortcut doesn’t launch:

Try the “Direct” version

Run ./fix_desktop_icon.sh

Ensure Python is available in PATH

Re-run the installer or create shortcuts again




---

For systemd and cron scheduling, see scheduling.md.

*Source: Echo-Notes/Docs/launchers.md*

---

## Echo-Notes Dashboard

A minimal, responsive GUI dashboard for monitoring and controlling the Echo-Notes daemon.

## Features

- Display daemon status (running/not running)
- Show timestamps of last processed note and weekly summary
- Control buttons to:
  - Start/stop the daemon
  - Manually trigger note processing
  - Manually trigger weekly summary generation
- Real-time log display

## Installation

Make sure you have all the required dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage

### Simple Double-Click Launcher (Recommended)

The easiest way to launch the dashboard is to simply double-click the `launcher.py` file in the Echo-Notes directory. This works on all platforms (Windows, macOS, Linux) and doesn't require any installation.

### Command Line Launch

To launch the dashboard from the command line:

```bash
# If installed via pip
echo-notes-dashboard

# Or directly from the project directory
python Echo-Notes/echo_notes_dashboard.py
```

### Desktop Shortcuts

You can also create desktop shortcuts to launch the dashboard without using the command line:

#### Linux:
```bash
# Install desktop shortcut
./install_desktop_shortcut.sh
```
After running this script, you'll find "Echo Notes Dashboard" in your applications menu.

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

## Dashboard Overview

### Status Section
Shows whether the daemon is running and displays timestamps of the last processed note and weekly summary.

### Controls Section
- **Start/Stop Daemon**: Toggle the daemon process on/off
- **Process Notes Now**: Manually trigger the note processing
- **Generate Summary Now**: Manually trigger the weekly summary generation

### Logs Section
Displays real-time logs from the Echo-Notes system, including daemon status updates and processing information.

## Requirements

- PyQt6 for the GUI components
- A running LLM server at the URL specified in `shared/config.py` (default: http://localhost:8080/v1/chat/completions) for note processing and summary generation
  - If the LLM server is not available, the dashboard will display a warning message and skip the processing

### Note on LLM Server
The dashboard checks for the availability of the LLM server before attempting to process notes or generate summaries. If the server is not available, it will log a warning message and skip the processing, allowing you to still use the dashboard for monitoring and controlling the daemon.

## Technical Details

The dashboard communicates with the Echo-Notes daemon using the same mechanisms as the command-line interface. It:

1. Checks for the PID file to determine if the daemon is running
2. Uses subprocess to start/stop the daemon
3. Directly calls the note processing and summary generation functions for manual triggers
4. Monitors the notes directory for changes to update timestamps

All operations that might block the UI are run in separate threads to keep the interface responsive.

*Source: Echo-Notes/dashboard_readme.md*

---

## Echo-Notes Dashboard

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

*Source: dist/Docs/dashboard.md*

---

## Echo-Notes Launch Options

# Echo-Notes Launch Options

Echo-Notes includes several ways to launch the dashboard and start the daemon, depending on your platform.

---

## 1. Cross-Platform: Python Launcher

Works on all platforms:

```bash
python launcher.py

This opens the GUI dashboard directly using your configured environment.


---

2. Desktop Shortcuts

Linux

Create application shortcuts:

./install_desktop_shortcuts.sh

After running, check your desktop or application menu for:

Echo Notes Dashboard

Echo Notes Dashboard (Direct) – more reliable on some systems


If the shortcut doesn't work:

./fix_desktop_icon.sh

This updates paths in .desktop files to point to the correct Python interpreter.


---

Windows

Run:

create_windows_shortcut.bat

This creates a .lnk desktop shortcut to the dashboard. Ensure Python is properly installed and accessible from PATH.


---

macOS

Run:

python create_macos_shortcut.py

This creates a clickable .app bundle in ~/Applications.

You may need to grant it permissions via System Settings > Privacy & Security.


---

3. Terminal Shortcuts

The following commands work after installation:

echo-notes-dashboard    # Open the dashboard
echo-notes-daemon       # Run daemon in foreground
echo-notes-daemon --daemon  # Run as background process
echo-notes-daemon --stop    # Stop background daemon

These are symlinked to your environment by the installer or setup.py.


---

Troubleshooting

If a shortcut doesn’t launch:

Try the “Direct” version

Run ./fix_desktop_icon.sh

Ensure Python is available in PATH

Re-run the installer or create shortcuts again




---

For systemd and cron scheduling, see scheduling.md.

*Source: dist/Docs/launchers.md*

---

