#!/bin/bash
# Echo-Notes Unified Installation Script
# This script installs Echo-Notes, its dependencies, and creates desktop shortcuts
# Compatible with Linux, macOS, and Windows (via Git Bash or WSL)

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory and handle potential nested directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Handle potential nested directory structure
if [ -d "Echo-Notes" ]; then
    # Check if this is a nested clone (Echo-Notes/Echo-Notes)
    if [ -f "Echo-Notes/echo_notes_dashboard.py" ]; then
        echo -e "${YELLOW}Detected nested Echo-Notes directory. Using it for installation.${NC}"
        cd "Echo-Notes"
        SCRIPT_DIR="$PWD"
    # Check if this is a fresh clone with no files in the current directory
    elif [ ! -f "echo_notes_dashboard.py" ] && [ "$(ls -A | grep -v 'Echo-Notes')" = "" ]; then
        echo -e "${YELLOW}Detected Echo-Notes directory with no files in parent. Using nested directory.${NC}"
        cd "Echo-Notes"
        SCRIPT_DIR="$PWD"
    fi
fi

echo -e "${BLUE}=== Echo-Notes Unified Installer ===${NC}"
echo "Installation directory: $SCRIPT_DIR"

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
        echo -e "${YELLOW}Please cd to one of these directories and run the installer again.${NC}"
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

# Check Python version
check_python() {
    if command -v python3 &>/dev/null; then
        PYTHON="python3"
    elif command -v python &>/dev/null; then
        # Check if python is Python 3
        PY_VERSION=$(python --version 2>&1)
        if [[ $PY_VERSION == *"Python 3"* ]]; then
            PYTHON="python"
        else
            echo -e "${RED}Error: Python 3 is required but not found.${NC}"
            echo "Please install Python 3 and try again."
            exit 1
        fi
    else
        echo -e "${RED}Error: Python 3 is required but not found.${NC}"
        echo "Please install Python 3 and try again."
        exit 1
    fi

    echo -e "${GREEN}Using Python: $($PYTHON --version)${NC}"
    return 0
}

# Create and activate virtual environment
setup_venv() {
    echo -e "${BLUE}Setting up virtual environment...${NC}"
    
    # Remove existing virtual environment if it's broken
    if [ -d "echo_notes_venv" ]; then
        # Test if pip is working in the existing venv
        if [[ "$OS" == "windows" ]]; then
            if [ ! -f "echo_notes_venv/Scripts/pip" ] || ! echo_notes_venv/Scripts/pip --version &>/dev/null; then
                echo -e "${YELLOW}Existing virtual environment appears to be broken. Recreating...${NC}"
                rm -rf echo_notes_venv
            else
                echo -e "${YELLOW}Using existing virtual environment${NC}"
            fi
        else
            if [ ! -f "echo_notes_venv/bin/pip" ] || ! echo_notes_venv/bin/pip --version &>/dev/null; then
                echo -e "${YELLOW}Existing virtual environment appears to be broken. Recreating...${NC}"
                rm -rf echo_notes_venv
            else
                echo -e "${YELLOW}Using existing virtual environment${NC}"
            fi
        fi
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "echo_notes_venv" ]; then
        echo -e "${BLUE}Creating new virtual environment...${NC}"
        $PYTHON -m venv echo_notes_venv
        echo -e "${GREEN}Created virtual environment${NC}"
    fi
    
    # Activate virtual environment
    if [[ "$OS" == "windows" ]]; then
        source echo_notes_venv/Scripts/activate
    else
        source echo_notes_venv/bin/activate
    fi
    
    echo -e "${GREEN}Virtual environment activated${NC}"
    
    # Ensure pip is installed and working
    if ! command -v pip &>/dev/null; then
        echo -e "${YELLOW}Pip not found in virtual environment. Installing...${NC}"
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        $PYTHON get-pip.py
        rm get-pip.py
    fi
    
    # Upgrade pip
    pip install --upgrade pip
    echo -e "${GREEN}Pip upgraded to $(pip --version)${NC}"
    
    return 0
}

# Install dependencies
install_dependencies() {
    echo -e "${BLUE}Installing dependencies...${NC}"
    
    # Install required packages
    pip install requests python-dateutil PyQt6
    
    # Install development dependencies if available
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        echo -e "${GREEN}Installed dependencies from requirements.txt${NC}"
    fi
    
    # Install the package in development mode
    pip install -e .
    echo -e "${GREEN}Installed Echo-Notes in development mode${NC}"
    
    return 0
}

# Linux-specific installation
install_linux() {
    echo -e "${BLUE}Performing Linux-specific installation...${NC}"
    
    # Use the consolidated script to install desktop shortcuts
    bash "${SCRIPT_DIR}/install_desktop_shortcuts.sh"
    
    echo -e "${GREEN}Created desktop shortcuts${NC}"
    echo -e "${YELLOW}Note: Make sure ~/.local/bin is in your PATH${NC}"
    
    return 0
}

# macOS-specific installation
install_macos() {
    echo -e "${BLUE}Performing macOS-specific installation...${NC}"
    
    # Run the macOS shortcut creation script
    $PYTHON create_macos_shortcut.py
    
    # Create symlink in /usr/local/bin if it exists and is writable
    if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
        ln -sf "${SCRIPT_DIR}/echo_notes_dashboard.py" /usr/local/bin/echo-notes-dashboard
        chmod +x /usr/local/bin/echo-notes-dashboard
        echo -e "${GREEN}Created symlink at /usr/local/bin/echo-notes-dashboard${NC}"
    else
        echo -e "${YELLOW}Note: Could not create symlink in /usr/local/bin${NC}"
        echo "You may need to manually add the Echo-Notes directory to your PATH"
    fi
    
    return 0
}

# Windows-specific installation
install_windows() {
    echo -e "${BLUE}Performing Windows-specific installation...${NC}"
    
    # Check if we're in Git Bash or similar
    if command -v cmd.exe &>/dev/null; then
        # Run the Windows shortcut creation script
        cmd.exe /c create_windows_shortcut.bat
        echo -e "${GREEN}Created Windows desktop shortcut${NC}"
    else
        echo -e "${YELLOW}Warning: cmd.exe not found. Running in WSL?${NC}"
        echo "Please run create_windows_shortcut.bat manually from Windows."
    fi
    
    return 0
}

# Configure the application
configure_app() {
    echo -e "${BLUE}Configuring Echo-Notes...${NC}"
    
    # Create default configuration if needed
    if [ ! -f "shared/schedule_config.json" ]; then
        cat > shared/schedule_config.json << EOF
{
    "processing_interval": 60,
    "summary_interval": 10080,
    "summary_day": 6,
    "summary_hour": 12,
    "daemon_enabled": true
}
EOF
        echo -e "${GREEN}Created default schedule configuration${NC}"
    fi
    
    # Ensure the notes directory exists
    NOTES_DIR="${ECHO_NOTES_DIR:-$HOME/Documents/notes/log}"
    mkdir -p "$NOTES_DIR"
    echo -e "${GREEN}Ensured notes directory exists: $NOTES_DIR${NC}"
    
    return 0
}

# Display help information
show_help() {
    echo -e "${BLUE}Echo-Notes Unified Installer${NC}"
    echo "This script installs Echo-Notes, its dependencies, and creates desktop shortcuts."
    echo ""
    echo "Usage: ./install.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --help, -h       Show this help message and exit"
    echo "  --no-desktop     Skip desktop shortcut/icon creation"
    echo "  --no-venv        Skip virtual environment creation (not recommended)"
    echo "  --verbose        Show more detailed output"
    echo ""
    echo "Examples:"
    echo "  ./install.sh                 # Standard installation"
    echo "  ./install.sh --no-desktop    # Install without desktop shortcuts"
    echo ""
    exit 0
}

# Parse command line arguments
parse_args() {
    NO_DESKTOP=false
    NO_VENV=false
    VERBOSE=false
    
    for arg in "$@"; do
        case $arg in
            --help|-h)
                show_help
                ;;
            --no-desktop)
                NO_DESKTOP=true
                ;;
            --no-venv)
                NO_VENV=true
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

# Main installation process
main() {
    echo -e "${BLUE}Starting Echo-Notes installation...${NC}"
    
    check_python
    
    if [ "$NO_VENV" = false ]; then
        setup_venv
    else
        echo -e "${YELLOW}Skipping virtual environment creation as requested${NC}"
    fi
    
    install_dependencies
    configure_app
    
    # OS-specific installation
    if [ "$NO_DESKTOP" = false ]; then
        case "$OS" in
            linux)
                install_linux
                ;;
            macos)
                install_macos
                ;;
            windows)
                install_windows
                ;;
            *)
                echo -e "${YELLOW}Warning: Unknown operating system. Skipping OS-specific installation.${NC}"
                ;;
        esac
    else
        echo -e "${YELLOW}Skipping desktop shortcut/icon creation as requested${NC}"
    fi
    
    echo -e "${GREEN}Installation complete!${NC}"
    echo ""
    echo -e "${BLUE}=== Getting Started ===${NC}"
    echo "1. Start the daemon: echo-notes-daemon --daemon"
    echo "2. Launch the dashboard: echo-notes-dashboard"
    echo "   Or use the desktop shortcut/icon created during installation"
    echo ""
    echo -e "${BLUE}=== Documentation ===${NC}"
    echo "For more information, see the README.md file or visit:"
    echo "https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes"
    echo ""
    
    return 0
}

# Parse command line arguments
parse_args "$@"

# Run the main installation process
main