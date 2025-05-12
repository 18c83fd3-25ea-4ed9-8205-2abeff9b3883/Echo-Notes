#!/bin/bash
# Echo-Notes Uninstaller Script

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Echo-Notes Uninstaller =====${NC}"
echo ""

# Default installation directory
DEFAULT_INSTALL_DIR="$HOME/Echo-Notes"
INSTALL_DIR=""

# Parse command line arguments
PURGE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --install-dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        --purge)
            PURGE=true
            shift
            ;;
        --help)
            echo "Echo-Notes Uninstaller"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --install-dir DIR    Specify installation directory"
            echo "  --purge              Remove user notes as well"
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

# If installation directory not specified, use default or ask user
if [ -z "$INSTALL_DIR" ]; then
    if [ -d "$DEFAULT_INSTALL_DIR" ]; then
        INSTALL_DIR="$DEFAULT_INSTALL_DIR"
        echo -e "${BLUE}Using default installation directory: ${INSTALL_DIR}${NC}"
    else
        echo -e "${YELLOW}Default installation directory not found: ${DEFAULT_INSTALL_DIR}${NC}"
        echo -e "${YELLOW}Please specify the installation directory using --install-dir${NC}"
        exit 1
    fi
fi

# Check if the installation directory exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${RED}Error: Installation directory not found: ${INSTALL_DIR}${NC}"
    exit 1
fi

# Check if Python 3 is installed
echo -e "${BLUE}Checking for Python 3...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}Python 3 found: $(python3 --version)${NC}"
else
    echo -e "${RED}Error: Python 3 is required but not found.${NC}"
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if the uninstaller module exists
UNINSTALLER_MODULE="$INSTALL_DIR/installers/linux/linux_uninstaller.py"
if [ ! -f "$UNINSTALLER_MODULE" ]; then
    echo -e "${RED}Error: Uninstaller module not found: ${UNINSTALLER_MODULE}${NC}"
    exit 1
fi

# Confirm uninstallation
echo -e "${YELLOW}This will uninstall Echo-Notes from: ${INSTALL_DIR}${NC}"
if [ "$PURGE" = true ]; then
    echo -e "${RED}WARNING: This will also remove all your notes!${NC}"
fi

read -p "Do you want to continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Uninstallation cancelled.${NC}"
    exit 0
fi

# Run the uninstaller module
echo -e "${BLUE}Running uninstaller...${NC}"
if [ "$PURGE" = true ]; then
    "$PYTHON_CMD" "$UNINSTALLER_MODULE" "$INSTALL_DIR" --purge
else
    "$PYTHON_CMD" "$UNINSTALLER_MODULE" "$INSTALL_DIR"
fi

# Check if uninstallation was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Echo-Notes has been successfully uninstalled.${NC}"
    
    # Ask if user wants to remove the installation directory
    read -p "Do you want to remove the installation directory? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$INSTALL_DIR"
        echo -e "${GREEN}Installation directory removed: ${INSTALL_DIR}${NC}"
    else
        echo -e "${YELLOW}Installation directory preserved: ${INSTALL_DIR}${NC}"
    fi
    
    # Remove this uninstaller script
    echo -e "${BLUE}Removing uninstaller script...${NC}"
    rm -f "$0"
    echo -e "${GREEN}Uninstaller script removed.${NC}"
    
    echo -e "${GREEN}Uninstallation completed successfully!${NC}"
else
    echo -e "${RED}Uninstallation failed.${NC}"
    exit 1
fi