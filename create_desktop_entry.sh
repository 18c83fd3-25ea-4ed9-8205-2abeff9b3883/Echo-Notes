#!/bin/bash
# Script to create desktop entry for Echo-Notes

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Creating Echo-Notes Desktop Entry =====${NC}"

# Check if Echo-Notes is installed
INSTALL_DIR="$HOME/Echo-Notes"
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${RED}Error: Echo-Notes installation directory not found at: $INSTALL_DIR${NC}"
    exit 1
fi

# Create icons directory if it doesn't exist
ICONS_DIR="$HOME/.local/share/icons"
mkdir -p "$ICONS_DIR"

# Check for icon file
ICON_FOUND=false
ICON_PATHS=(
    "$INSTALL_DIR/config/icons/Echo-Notes-Icon.png"
    "$INSTALL_DIR/Echo-Notes-Icon.png"
    "$INSTALL_DIR/echo_notes/icons/Echo-Notes-Icon.png"
    "$INSTALL_DIR/echo_notes/Echo-Notes-Icon.png"
)

for ICON_PATH in "${ICON_PATHS[@]}"; do
    if [ -f "$ICON_PATH" ]; then
        cp "$ICON_PATH" "$ICONS_DIR/echo-notes.png"
        echo -e "${GREEN}Installed icon from $ICON_PATH to $ICONS_DIR/echo-notes.png${NC}"
        ICON_FOUND=true
        break
    fi
done

if [ "$ICON_FOUND" = false ]; then
    echo -e "${YELLOW}Warning: Icon file not found, desktop entry will use default icon${NC}"
fi

# Create applications directory if it doesn't exist
APPLICATIONS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPLICATIONS_DIR"

# Create desktop entry file
DESKTOP_FILE="$APPLICATIONS_DIR/echo-notes.desktop"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes
Comment=Monitor and control Echo-Notes daemon
Exec=$INSTALL_DIR/echo_notes_venv/bin/python $INSTALL_DIR/echo_notes/dashboard.py
Icon=$HOME/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
EOF

# Make the desktop file executable
chmod +x "$DESKTOP_FILE"
echo -e "${GREEN}Created desktop entry at $DESKTOP_FILE${NC}"

# Create desktop icon if Desktop directory exists
DESKTOP_DIR="$HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    DESKTOP_ICON="$DESKTOP_DIR/Echo Notes.desktop"
    cp "$DESKTOP_FILE" "$DESKTOP_ICON"
    chmod +x "$DESKTOP_ICON"
    echo -e "${GREEN}Created desktop icon at $DESKTOP_ICON${NC}"
fi

# Create symlinks in ~/.local/bin
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

# Create symlinks
SYMLINKS=(
    "echo-notes-dashboard:$INSTALL_DIR/echo_notes/dashboard.py"
    "echo-notes-daemon:$INSTALL_DIR/echo_notes/daemon.py"
    "echo-notes-python:$INSTALL_DIR/echo_notes_venv/bin/python"
)

for SYMLINK in "${SYMLINKS[@]}"; do
    NAME="${SYMLINK%%:*}"
    TARGET="${SYMLINK#*:}"
    
    # Remove existing symlink if it exists
    if [ -L "$BIN_DIR/$NAME" ] || [ -e "$BIN_DIR/$NAME" ]; then
        rm "$BIN_DIR/$NAME"
    fi
    
    # Create new symlink
    ln -s "$TARGET" "$BIN_DIR/$NAME"
    chmod +x "$BIN_DIR/$NAME"
    echo -e "${GREEN}Created symlink: $BIN_DIR/$NAME -> $TARGET${NC}"
done

# Update desktop database if command exists
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$APPLICATIONS_DIR"
fi

echo -e "${GREEN}Desktop entry and symlinks created successfully!${NC}"
echo -e "${YELLOW}You should now be able to find Echo Notes in your application menu.${NC}"
echo -e "${YELLOW}You may need to log out and log back in for the changes to take effect.${NC}"