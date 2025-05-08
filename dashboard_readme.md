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

To launch the dashboard:

```bash
python Echo-Notes/echo_notes_dashboard.py
```

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