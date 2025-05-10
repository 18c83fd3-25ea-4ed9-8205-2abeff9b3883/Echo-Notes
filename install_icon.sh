#!/bin/bash
# Script to install the Echo-Notes icon to the user's local icon directory

# Create the icons directory if it doesn't exist
mkdir -p ${HOME}/.local/share/icons

# Copy the icon to the icons directory
cp "$(dirname "$0")/Echo-Notes-Icon.png" ${HOME}/.local/share/icons/echo-notes.png

echo "Icon installed to ${HOME}/.local/share/icons/echo-notes.png"