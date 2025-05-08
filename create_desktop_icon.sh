#!/bin/bash

# Create a desktop shortcut directly on the user's desktop and install the icon
echo "Creating Echo Notes Dashboard desktop icon..."

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Install the icon
mkdir -p ${HOME}/.local/share/icons
cp "${SCRIPT_DIR}/Echo-Notes-Icon.png" ${HOME}/.local/share/icons/echo-notes.png
echo "Installed icon to ${HOME}/.local/share/icons/echo-notes.png"

# Get the absolute path to the echo-notes-dashboard executable
DASHBOARD_PATH=$(which echo-notes-dashboard 2>/dev/null)

if [ -z "$DASHBOARD_PATH" ]; then
    echo "Error: echo-notes-dashboard executable not found in PATH."
    echo "Make sure Echo-Notes is properly installed."
    exit 1
fi

# Create the desktop file directly on the desktop
DESKTOP_FILE="$HOME/Desktop/Echo Notes Dashboard.desktop"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes Dashboard
Comment=Monitor and control Echo-Notes daemon
Exec=$DASHBOARD_PATH
Icon=${HOME}/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
EOF

# Make it executable
chmod +x "$DESKTOP_FILE"

echo "Desktop icon created at: $DESKTOP_FILE"
echo "You can now double-click this icon to launch Echo Notes Dashboard."