#!/bin/bash

# Create a desktop shortcut directly on the user's desktop and install the icon
echo "Creating Echo Notes Dashboard desktop icon..."

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

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

# Create the desktop file directly on the desktop
DESKTOP_FILE="$HOME/Desktop/Echo Notes.desktop"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes
Comment=Monitor and control Echo-Notes daemon
Exec=bash -c "cd \$(dirname %k) && source echo_notes_venv/bin/activate && python echo_notes_dashboard.py"
Icon=\$HOME/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
EOF

# Make it executable
chmod +x "$DESKTOP_FILE"

echo "Desktop icon created at: $DESKTOP_FILE"
echo "You can now double-click this icon to launch Echo Notes."