# Echo-Notes Dashboard

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