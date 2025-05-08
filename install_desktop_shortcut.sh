#!/bin/bash

# Create the applications directory if it doesn't exist
mkdir -p ~/.local/share/applications/

# Copy the desktop file to the applications directory
cp "$(dirname "$0")/echo-notes-dashboard.desktop" ~/.local/share/applications/

# Make the desktop file executable
chmod +x ~/.local/share/applications/echo-notes-dashboard.desktop

echo "Echo Notes Dashboard shortcut installed successfully!"
echo "You can now find 'Echo Notes Dashboard' in your applications menu."