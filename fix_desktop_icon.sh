#!/bin/bash

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Script directory: $SCRIPT_DIR"

# Install the icon
mkdir -p ${HOME}/.local/share/icons
cp "${SCRIPT_DIR}/Echo-Notes-Icon.png" ${HOME}/.local/share/icons/echo-notes.png
echo "Installed icon to ${HOME}/.local/share/icons/echo-notes.png"

# Create the applications directory if it doesn't exist
mkdir -p ~/.local/share/applications/

# Create the desktop files with absolute paths
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

# Create desktop icons with absolute paths
if [ -d "$HOME/Desktop" ]; then
    # Standard version
    cat > "$HOME/Desktop/Echo Notes.desktop" << EOF
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
    chmod +x "$HOME/Desktop/Echo Notes.desktop"
    echo "Created desktop icon at $HOME/Desktop/Echo Notes.desktop"
    
    # Direct version (known to work reliably)
    cat > "$HOME/Desktop/Echo Notes (Direct).desktop" << EOF
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
    chmod +x "$HOME/Desktop/Echo Notes (Direct).desktop"
    echo "Created direct desktop icon at $HOME/Desktop/Echo Notes (Direct).desktop"
fi

# Update desktop database if command exists
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database ~/.local/share/applications
fi

echo "Echo Notes Desktop icon fixed successfully!"
echo "You can now find 'Echo Notes' in your applications menu or on your desktop."