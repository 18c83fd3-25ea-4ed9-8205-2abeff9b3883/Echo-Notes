#!/bin/bash

# Consolidated script to install desktop shortcuts for Echo Notes
# This script creates both a desktop icon and an application menu entry

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Script directory: $SCRIPT_DIR"

# Install the icon
mkdir -p ${HOME}/.local/share/icons
cp "${SCRIPT_DIR}/Echo-Notes-Icon.png" ${HOME}/.local/share/icons/echo-notes.png
echo "Installed icon to ${HOME}/.local/share/icons/echo-notes.png"

# Check if echo-notes-dashboard is in PATH
DASHBOARD_PATH=$(which echo-notes-dashboard 2>/dev/null)

if [ -z "$DASHBOARD_PATH" ]; then
    echo "echo-notes-dashboard executable not found in PATH."
    echo "Creating symlink in ~/.local/bin/"
    
    # Create ~/.local/bin if it doesn't exist
    mkdir -p ~/.local/bin
    
    # Create symlink to the dashboard script
    ln -sf "${SCRIPT_DIR}/echo_notes_dashboard.py" ~/.local/bin/echo-notes-dashboard
    chmod +x ~/.local/bin/echo-notes-dashboard
    
    echo "Created symlink at ~/.local/bin/echo-notes-dashboard"
    echo "Make sure ~/.local/bin is in your PATH"
fi

# Create the applications directory if it doesn't exist
mkdir -p ~/.local/share/applications/

# Create the desktop files in applications menu
# Standard version
cat > ~/.local/share/applications/echo-notes.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes
Comment=Monitor and control Echo-Notes daemon
Exec=${SCRIPT_DIR}/echo_notes_venv/bin/python ${SCRIPT_DIR}/echo_notes_dashboard.py
Icon=${HOME}/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
EOF

# Direct version (known to work reliably)
cat > ~/.local/share/applications/echo-notes-direct.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes (Direct)
Comment=Monitor and control Echo-Notes daemon
Exec=${SCRIPT_DIR}/echo_notes_venv/bin/python ${SCRIPT_DIR}/echo_notes_dashboard.py
Icon=${HOME}/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
EOF

# Make the desktop files executable
chmod +x ~/.local/share/applications/echo-notes.desktop
chmod +x ~/.local/share/applications/echo-notes-direct.desktop

# Update desktop database if command exists
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database ~/.local/share/applications
fi

echo "Application menu entry created successfully!"

# Create desktop icons if Desktop directory exists
if [ -d "$HOME/Desktop" ]; then
    # Standard version
    DESKTOP_FILE="$HOME/Desktop/Echo Notes.desktop"
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes
Comment=Monitor and control Echo-Notes daemon
Exec=${SCRIPT_DIR}/echo_notes_venv/bin/python ${SCRIPT_DIR}/echo_notes_dashboard.py
Icon=${HOME}/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
EOF
    chmod +x "$DESKTOP_FILE"
    echo "Desktop icon created at: $DESKTOP_FILE"
    
    # Direct version (known to work reliably)
    DESKTOP_FILE_DIRECT="$HOME/Desktop/Echo Notes (Direct).desktop"
    cat > "$DESKTOP_FILE_DIRECT" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes (Direct)
Comment=Monitor and control Echo-Notes daemon
Exec=${SCRIPT_DIR}/echo_notes_venv/bin/python ${SCRIPT_DIR}/echo_notes_dashboard.py
Icon=${HOME}/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
EOF
    chmod +x "$DESKTOP_FILE_DIRECT"
    echo "Direct desktop icon created at: $DESKTOP_FILE_DIRECT"
fi

echo "Echo Notes shortcuts installed successfully!"
echo "You can now find 'Echo Notes' in your applications menu and on your desktop (if available)."