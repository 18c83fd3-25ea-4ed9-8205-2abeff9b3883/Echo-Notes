# Echo-Notes Desktop Entry Fix

This script fixes the issue where Echo-Notes doesn't appear in your application menu after installation.

## Problem

The standard Linux installer and wrapper script successfully download and extract the Echo-Notes files, but they fail to properly create:
1. Desktop shortcuts and application menu entries
2. Symlinks in ~/.local/bin
3. Proper executable permissions for Python scripts

## Solution

The `create_desktop_entry.sh` script fixes these issues by:
1. Creating desktop shortcuts and application menu entries
2. Setting up symlinks in ~/.local/bin
3. Making sure all necessary files are executable

## Usage

1. Make sure Echo-Notes is installed in your home directory (`~/Echo-Notes`)
2. Run the script:
   ```bash
   chmod +x create_desktop_entry.sh
   ./create_desktop_entry.sh
   ```
3. You should now be able to find Echo Notes in your application menu
4. You may need to log out and log back in for the changes to take effect

## Verification

After running the script, you should have:
- A desktop entry file at `~/.local/share/applications/echo-notes.desktop`
- A desktop icon at `~/Desktop/Echo Notes.desktop` (if you have a Desktop directory)
- Symlinks in `~/.local/bin` for:
  - `echo-notes-dashboard`
  - `echo-notes-daemon`
  - `echo-notes-python`

## Troubleshooting

If Echo-Notes still doesn't appear in your application menu:
1. Try logging out and logging back in
2. Check if the desktop entry file exists: `ls -la ~/.local/share/applications/echo-notes.desktop`
3. Try running Echo-Notes directly: `~/Echo-Notes/echo_notes_venv/bin/python ~/Echo-Notes/echo_notes/dashboard.py`

If you get a "Permission denied" error, make sure the files are executable:
```bash
chmod +x ~/Echo-Notes/echo_notes_venv/bin/python
chmod +x ~/Echo-Notes/echo_notes/dashboard.py
chmod +x ~/Echo-Notes/echo_notes/daemon.py
```

If you get a "ModuleNotFoundError" for PyQt6, install it:
```bash
chmod +x ~/Echo-Notes/echo_notes_venv/bin/pip
~/Echo-Notes/echo_notes_venv/bin/pip install PyQt6