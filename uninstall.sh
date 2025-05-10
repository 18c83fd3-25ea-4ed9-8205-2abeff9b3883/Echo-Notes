#!/bin/bash
# Echo-Notes Uninstaller

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Echo-Notes Uninstaller =====${NC}"
echo ""

INSTALL_DIR="/home/j/Documents/CodeProjects/Echo-Notes"
VENV_DIR="/home/j/Documents/CodeProjects/Echo-Notes/echo_notes_venv"

# Stop running processes
echo -e "${BLUE}Stopping Echo-Notes processes...${NC}"
if [ -f "${VENV_DIR}/bin/echo-notes-daemon" ]; then
    "${VENV_DIR}/bin/echo-notes-daemon" --stop
fi
pkill -f "echo_notes_daemon.py" || true
pkill -f "echo_notes_dashboard.py" || true
echo -e "${GREEN}Processes stopped${NC}"

# OS-specific uninstallation
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo -e "${BLUE}Performing macOS-specific uninstallation...${NC}"
    rm -rf ~/Applications/"Echo Notes Dashboard.app"
    rm -f /usr/local/bin/echo-notes-dashboard
    echo -e "${GREEN}Removed application bundle and symlinks${NC}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo -e "${BLUE}Performing Linux-specific uninstallation...${NC}"
    rm -f ~/.local/share/applications/echo-notes.desktop
    rm -f ~/Desktop/"Echo Notes.desktop"
    rm -f ~/.local/share/icons/echo-notes.png
    rm -f ~/.local/bin/echo-notes-dashboard
    echo -e "${GREEN}Removed desktop shortcuts, icons, and symlinks${NC}"
fi

# Ask about notes
echo ""
read -p "Would you like to keep your notes? (Y/n): " KEEP_NOTES
if [[ "$KEEP_NOTES" =~ ^[Nn]$ ]]; then
    echo -e "${RED}Removing notes directory...${NC}"
    NOTES_DIR="${ECHO_NOTES_DIR:-$HOME/Documents/notes/log}"
    rm -rf "$NOTES_DIR"
    echo -e "${RED}Notes directory removed: $NOTES_DIR${NC}"
else
    echo -e "${GREEN}Preserving notes directory${NC}"
fi

echo ""
echo -e "${GREEN}Uninstallation complete!${NC}"
echo "If you want to completely remove Echo-Notes, you can now delete this directory:"
echo "$INSTALL_DIR"
echo ""
