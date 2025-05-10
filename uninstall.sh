#!/bin/bash
# Echo-Notes Unified Uninstallation Script
# This script removes Echo-Notes while preserving user notes

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Handle potential nested directory structure
if [ -d "Echo-Notes" ]; then
    # Check if this is a nested clone (Echo-Notes/Echo-Notes)
    if [ -f "Echo-Notes/echo_notes_dashboard.py" ]; then
        echo -e "${YELLOW}Detected nested Echo-Notes directory. Using it for uninstallation.${NC}"
        cd "Echo-Notes"
        SCRIPT_DIR="$PWD"
    # Check if this is a fresh clone with no files in the current directory
    elif [ ! -f "echo_notes_dashboard.py" ] && [ "$(ls -A | grep -v 'Echo-Notes')" = "" ]; then
        echo -e "${YELLOW}Detected Echo-Notes directory with no files in parent. Using nested directory.${NC}"
        cd "Echo-Notes"
        SCRIPT_DIR="$PWD"
    fi
fi

echo -e "${BLUE}=== Echo-Notes Unified Uninstaller ===${NC}"
echo "Uninstallation directory: $SCRIPT_DIR"

# Verify we're in the correct directory
if [ ! -f "echo_notes_dashboard.py" ]; then
    echo -e "${RED}Error: Could not find echo_notes_dashboard.py in the current directory.${NC}"
    echo "This script must be run from the Echo-Notes directory."
    echo "Current directory: $PWD"
    echo "Files in current directory:"
    ls -la
    
    # Try to find the correct directory
    POSSIBLE_DIRS=$(find . -name "echo_notes_dashboard.py" -type f | sed 's|/echo_notes_dashboard.py$||')
    if [ ! -z "$POSSIBLE_DIRS" ]; then
        echo -e "${YELLOW}Found possible Echo-Notes directories:${NC}"
        echo "$POSSIBLE_DIRS"
        echo -e "${YELLOW}Please cd to one of these directories and run the uninstaller again.${NC}"
    fi
    
    exit 1
fi

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo -e "${BLUE}Detected operating system: ${YELLOW}$OS${NC}"

# Stop running processes
stop_processes() {
    echo -e "${BLUE}Stopping Echo-Notes processes...${NC}"
    
    # Try to stop the daemon gracefully
    if command -v echo-notes-daemon &>/dev/null; then
        echo -e "${YELLOW}Stopping Echo-Notes daemon...${NC}"
        echo-notes-daemon --stop || true
    fi
    
    # Kill any remaining processes (platform-specific)
    case "$OS" in
        linux|macos)
            echo -e "${YELLOW}Checking for remaining processes...${NC}"
            pkill -f "echo_notes_daemon.py" || true
            pkill -f "echo_notes_dashboard.py" || true
            ;;
        windows)
            echo -e "${YELLOW}Checking for remaining processes...${NC}"
            taskkill /F /IM python.exe /FI "WINDOWTITLE eq Echo-Notes*" > /dev/null 2>&1 || true
            ;;
    esac
    
    echo -e "${GREEN}Processes stopped${NC}"
    return 0
}

# Linux-specific uninstallation
uninstall_linux() {
    echo -e "${BLUE}Performing Linux-specific uninstallation...${NC}"
    
    # Remove desktop shortcuts
    rm -f ~/.local/share/applications/echo-notes.desktop
    rm -f ~/.local/share/applications/echo-notes-direct.desktop
    echo -e "${GREEN}Removed application menu entries${NC}"
    
    # Remove desktop icons
    rm -f "$HOME/Desktop/Echo Notes.desktop"
    rm -f "$HOME/Desktop/Echo Notes (Direct).desktop"
    echo -e "${GREEN}Removed desktop icons${NC}"
    
    # Remove icon
    rm -f ${HOME}/.local/share/icons/echo-notes.png
    echo -e "${GREEN}Removed icon${NC}"
    
    # Remove symlinks
    rm -f ~/.local/bin/echo-notes-dashboard
    rm -f ~/.local/bin/echo-notes-daemon
    rm -f ~/.local/bin/echo-notes-config
    rm -f ~/.local/bin/process-notes
    rm -f ~/.local/bin/generate-summary
    echo -e "${GREEN}Removed symlinks${NC}"
    
    # Update desktop database if command exists
    if command -v update-desktop-database &>/dev/null; then
        update-desktop-database ~/.local/share/applications
    fi
    
    return 0
}

# macOS-specific uninstallation
uninstall_macos() {
    echo -e "${BLUE}Performing macOS-specific uninstallation...${NC}"
    
    # Remove app bundle
    rm -rf ~/Applications/"Echo Notes Dashboard.app"
    echo -e "${GREEN}Removed application bundle${NC}"
    
    # Remove symlinks
    rm -f /usr/local/bin/echo-notes-dashboard
    rm -f /usr/local/bin/echo-notes-daemon
    rm -f /usr/local/bin/echo-notes-config
    rm -f /usr/local/bin/process-notes
    rm -f /usr/local/bin/generate-summary
    echo -e "${GREEN}Removed symlinks${NC}"
    
    return 0
}

# Windows-specific uninstallation
uninstall_windows() {
    echo -e "${BLUE}Performing Windows-specific uninstallation...${NC}"
    
    # Remove desktop shortcut
    if command -v powershell.exe &>/dev/null; then
        powershell.exe -Command "Remove-Item -Path ([Environment]::GetFolderPath('Desktop') + '\Echo Notes Dashboard.lnk') -Force -ErrorAction SilentlyContinue"
        echo -e "${GREEN}Removed desktop shortcut${NC}"
    else
        echo -e "${YELLOW}Warning: powershell.exe not found. Running in WSL?${NC}"
        echo "Please manually remove the 'Echo Notes Dashboard' shortcut from your Windows desktop."
    fi
    
    return 0
}

# Remove virtual environment
remove_venv() {
    echo -e "${BLUE}Removing virtual environment...${NC}"
    
    if [ -d "echo_notes_venv" ]; then
        rm -rf echo_notes_venv
        echo -e "${GREEN}Removed virtual environment${NC}"
    else
        echo -e "${YELLOW}Virtual environment not found${NC}"
    fi
    
    return 0
}

# Display help information
show_help() {
    echo -e "${BLUE}Echo-Notes Unified Uninstaller${NC}"
    echo "This script removes Echo-Notes while preserving user notes."
    echo ""
    echo "Usage: ./uninstall.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --help, -h       Show this help message and exit"
    echo "  --keep-config    Keep configuration files"
    echo "  --purge          Remove everything including notes (USE WITH CAUTION)"
    echo "  --verbose        Show more detailed output"
    echo ""
    echo "Examples:"
    echo "  ./uninstall.sh                # Standard uninstallation"
    echo "  ./uninstall.sh --keep-config  # Uninstall but keep configuration"
    echo ""
    exit 0
}

# Parse command line arguments
parse_args() {
    KEEP_CONFIG=false
    PURGE=false
    VERBOSE=false
    
    for arg in "$@"; do
        case $arg in
            --help|-h)
                show_help
                ;;
            --keep-config)
                KEEP_CONFIG=true
                ;;
            --purge)
                PURGE=true
                ;;
            --verbose)
                VERBOSE=true
                ;;
            *)
                echo -e "${YELLOW}Warning: Unknown option: $arg${NC}"
                ;;
        esac
    done
}

# Main uninstallation process
main() {
    echo -e "${BLUE}Starting Echo-Notes uninstallation...${NC}"
    
    # Ask for confirmation
    echo -e "${YELLOW}This will uninstall Echo-Notes from your system.${NC}"
    echo -e "${GREEN}Your notes will be preserved.${NC}"
    if [ "$PURGE" = true ]; then
        echo -e "${RED}WARNING: --purge option selected. This will also remove your notes!${NC}"
    fi
    
    read -p "Do you want to continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Uninstallation cancelled.${NC}"
        exit 0
    fi
    
    # Stop running processes
    stop_processes
    
    # OS-specific uninstallation
    case "$OS" in
        linux)
            uninstall_linux
            ;;
        macos)
            uninstall_macos
            ;;
        windows)
            uninstall_windows
            ;;
        *)
            echo -e "${YELLOW}Warning: Unknown operating system. Skipping OS-specific uninstallation.${NC}"
            ;;
    esac
    
    # Remove virtual environment
    remove_venv
    
    # Remove configuration files if not keeping them
    if [ "$KEEP_CONFIG" = false ]; then
        echo -e "${BLUE}Removing configuration files...${NC}"
        rm -f shared/schedule_config.json
        echo -e "${GREEN}Removed configuration files${NC}"
    else
        echo -e "${YELLOW}Keeping configuration files as requested${NC}"
    fi
    
    # Remove notes if purging
    if [ "$PURGE" = true ]; then
        echo -e "${RED}Removing notes directory...${NC}"
        NOTES_DIR="${ECHO_NOTES_DIR:-$HOME/Documents/notes/log}"
        rm -rf "$NOTES_DIR"
        echo -e "${RED}Removed notes directory: $NOTES_DIR${NC}"
    else
        echo -e "${GREEN}Preserved notes directory${NC}"
    fi
    
    echo -e "${GREEN}Uninstallation complete!${NC}"
    echo ""
    echo -e "${BLUE}=== Notes Location ===${NC}"
    echo "Your notes are still available at: ${ECHO_NOTES_DIR:-$HOME/Documents/notes/log}"
    echo ""
    echo -e "${YELLOW}If you want to completely remove Echo-Notes, you can now delete this directory:${NC}"
    echo "$SCRIPT_DIR"
    echo ""
    
    return 0
}

# Parse command line arguments
parse_args "$@"

# Run the main uninstallation process
main