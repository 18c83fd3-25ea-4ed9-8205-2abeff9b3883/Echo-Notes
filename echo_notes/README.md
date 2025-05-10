# Echo-Notes Package

This directory contains the main Python package for Echo-Notes.

## Structure

- `__init__.py` - Package initialization
- `daemon.py` - Echo-Notes daemon for background processing
- `dashboard.py` - Echo-Notes dashboard GUI
- `notes_nextcloud.py` - Nextcloud notes integration
- `weekly_summary.py` - Weekly summary generation
- `shared/` - Shared utilities and configuration

## Usage

The package is designed to be installed via pip:

```bash
pip install -e .
```

This will install the following command-line tools:

- `echo-notes-daemon` - Start the Echo-Notes daemon
- `echo-notes-dashboard` - Launch the Echo-Notes dashboard
- `echo-notes-config` - Configure Echo-Notes scheduling
- `process-notes` - Process notes for Nextcloud integration
- `generate-summary` - Generate weekly summaries