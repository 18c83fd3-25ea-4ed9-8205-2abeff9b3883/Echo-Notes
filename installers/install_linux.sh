#!/bin/bash
# Echo-Notes Linux Installer Entry Point

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Echo-Notes Linux Installer =====${NC}"
echo ""

# Determine script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if Python 3 is installed
echo -e "${BLUE}Checking for Python 3...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}Python 3 found: $(python3 --version)${NC}"
else
    echo -e "${RED}Error: Python 3 is required but not found.${NC}"
    echo "Please install Python 3 and try again."
    echo "You can install it using your distribution's package manager:"
    echo "  For Debian/Ubuntu: sudo apt install python3 python3-pip python3-venv"
    echo "  For Fedora: sudo dnf install python3 python3-pip"
    echo "  For Arch Linux: sudo pacman -S python python-pip"
    exit 1
fi

# Parse command line arguments
INSTALL_DIR=""
NO_SHORTCUTS=false
NO_SYMLINKS=false
NO_SERVICE=false
DOWNLOAD_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --install-dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        --no-shortcuts)
            NO_SHORTCUTS=true
            shift
            ;;
        --no-symlinks)
            NO_SYMLINKS=true
            shift
            ;;
        --no-service)
            NO_SERVICE=true
            shift
            ;;
        --download-only)
            DOWNLOAD_ONLY=true
            shift
            ;;
        --help)
            echo "Echo-Notes Linux Installer"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --install-dir DIR    Specify installation directory"
            echo "  --no-shortcuts       Skip creating desktop shortcuts"
            echo "  --no-symlinks        Skip creating symlinks"
            echo "  --no-service         Skip setting up daemon service"
            echo "  --download-only      Only download Echo-Notes, don't install"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information."
            exit 1
            ;;
    esac
done

# Add the parent directory to PYTHONPATH
export PYTHONPATH="$PARENT_DIR:$PYTHONPATH"

# Check if we're running from the repository or need to download it
if [ -f "$SCRIPT_DIR/../echo_notes/dashboard.py" ]; then
    echo -e "${GREEN}Running from Echo-Notes repository${NC}"
    REPO_DIR="$SCRIPT_DIR/.."
else
    echo -e "${BLUE}Need to download Echo-Notes repository${NC}"
    
    # Create a temporary Python script to download the repository
    TEMP_SCRIPT=$(mktemp)
    cat > "$TEMP_SCRIPT" << EOF
import sys
import os
from pathlib import Path

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from installers.common.download_manager import download_echo_notes

# Download Echo-Notes
install_dir = "${INSTALL_DIR}" if "${INSTALL_DIR}" else None
download_dir = download_echo_notes(install_dir)

if download_dir:
    print(f"DOWNLOAD_SUCCESS:{download_dir}")
else:
    print("DOWNLOAD_FAILED")
EOF

    # Run the download script
    DOWNLOAD_RESULT=$("$PYTHON_CMD" "$TEMP_SCRIPT")
    rm "$TEMP_SCRIPT"
    
    if [[ "$DOWNLOAD_RESULT" == DOWNLOAD_FAILED* ]]; then
        echo -e "${RED}Failed to download Echo-Notes repository${NC}"
        exit 1
    elif [[ "$DOWNLOAD_RESULT" == DOWNLOAD_SUCCESS* ]]; then
        REPO_DIR="${DOWNLOAD_RESULT#DOWNLOAD_SUCCESS:}"
        echo -e "${GREEN}Downloaded Echo-Notes to: $REPO_DIR${NC}"
    else
        echo -e "${RED}Unexpected download result: $DOWNLOAD_RESULT${NC}"
        exit 1
    fi
    
    # If download-only flag is set, exit here
    if [ "$DOWNLOAD_ONLY" = true ]; then
        echo -e "${GREEN}Download completed. Exiting as requested.${NC}"
        exit 0
    fi
fi

# Set installation directory if not provided
if [ -z "$INSTALL_DIR" ]; then
    INSTALL_DIR="$REPO_DIR"
fi

# Check for required dependencies
echo -e "${BLUE}Checking for required dependencies...${NC}"
MISSING_DEPS=false

# Check for pip and venv
if ! "$PYTHON_CMD" -c "import pip" &>/dev/null; then
    echo -e "${YELLOW}Python pip is not installed${NC}"
    MISSING_DEPS=true
fi

if ! "$PYTHON_CMD" -c "import venv" &>/dev/null; then
    echo -e "${YELLOW}Python venv module is not installed${NC}"
    MISSING_DEPS=true
fi

# If dependencies are missing, suggest installation commands
if [ "$MISSING_DEPS" = true ]; then
    echo -e "${YELLOW}Some required dependencies are missing.${NC}"
    echo "Please install them using your distribution's package manager:"
    echo "  For Debian/Ubuntu: sudo apt install python3-pip python3-venv"
    echo "  For Fedora: sudo dnf install python3-pip python3-venv"
    echo "  For Arch Linux: sudo pacman -S python-pip"
    
    # Ask if user wants to continue anyway
    read -p "Do you want to continue anyway? (y/N): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        echo -e "${RED}Installation aborted.${NC}"
        exit 1
    fi
fi

# Create a temporary Python script to run the installer
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << EOF
import sys
import os
from pathlib import Path

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from installers.linux.linux_installer import install_linux

# Set up options
options = {
    "no_shortcuts": True if "${NO_SHORTCUTS}" == "true" else False,
    "no_symlinks": True if "${NO_SYMLINKS}" == "true" else False,
    "no_service": True if "${NO_SERVICE}" == "true" else False
}

# Run the installer
success = install_linux("${INSTALL_DIR}", options)
sys.exit(0 if success else 1)
EOF

# Run the installer script
"$PYTHON_CMD" "$TEMP_SCRIPT"
INSTALL_RESULT=$?
rm "$TEMP_SCRIPT"

if [ $INSTALL_RESULT -eq 0 ]; then
    echo -e "${GREEN}Installation completed successfully!${NC}"
    
    # Remind about PATH if symlinks were created
    if [ "$NO_SYMLINKS" = false ]; then
        echo -e "${YELLOW}Note: If this is your first time installing Echo-Notes, you may need to restart your terminal"
        echo -e "or run 'source ~/.bashrc' for the PATH changes to take effect.${NC}"
    fi
    
    exit 0
else
    echo -e "${RED}Installation failed with error code: $INSTALL_RESULT${NC}"
    exit 1
fi