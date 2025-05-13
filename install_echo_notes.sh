#!/bin/bash
# Echo-Notes Installer Wrapper Script

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Echo-Notes Installer Wrapper =====${NC}"
echo ""

# Download the installer script
echo -e "${BLUE}Downloading Echo-Notes installer...${NC}"
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/installers/install_linux.sh

# Make it executable
chmod +x install_linux.sh

# Run the installer
echo -e "${BLUE}Running Echo-Notes installer...${NC}"
./install_linux.sh
INSTALL_RESULT=$?

echo -e "${YELLOW}Installer exited with code: $INSTALL_RESULT${NC}"
echo -e "${YELLOW}This may be normal - continuing with uninstaller script creation...${NC}"

# Always create uninstaller scripts, regardless of installer exit code
if [ -d "$HOME/Echo-Notes" ]; then
    echo -e "${GREEN}Echo-Notes installation directory found at: $HOME/Echo-Notes${NC}"
    echo -e "${GREEN}Proceeding with uninstaller script creation...${NC}"
    
    # Create uninstaller scripts
    echo -e "${BLUE}Creating uninstaller scripts...${NC}"
    
    # Create shell uninstaller script
    echo -e "${BLUE}Creating shell uninstaller script...${NC}"
    cat > "$HOME/uninstall.sh" << 'EOF'
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

# If installation directory not specified, use default
if [ -z "$INSTALL_DIR" ]; then
    INSTALL_DIR="$DEFAULT_INSTALL_DIR"
    echo -e "${BLUE}Using default installation directory: ${INSTALL_DIR}${NC}"
fi

# Check if the installation directory exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${RED}Error: Installation directory not found: ${INSTALL_DIR}${NC}"
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

# Stop running processes
echo -e "${BLUE}Stopping Echo-Notes processes...${NC}"
systemctl --user stop echo-notes.service 2>/dev/null || true
systemctl --user disable echo-notes.service 2>/dev/null || true
pkill -f "echo_notes/daemon.py" 2>/dev/null || true
pkill -f "echo_notes/dashboard.py" 2>/dev/null || true
echo -e "${GREEN}Echo-Notes processes stopped${NC}"

# Remove desktop shortcuts
echo -e "${BLUE}Removing desktop shortcuts...${NC}"
rm -f "$HOME/.local/share/applications/echo-notes.desktop" 2>/dev/null || true
rm -f "$HOME/Desktop/Echo Notes.desktop" 2>/dev/null || true
rm -f "$HOME/.local/share/icons/echo-notes.png" 2>/dev/null || true
echo -e "${GREEN}Desktop shortcuts removed${NC}"

# Remove symlinks
echo -e "${BLUE}Removing symlinks...${NC}"
rm -f "$HOME/.local/bin/echo-notes-dashboard" 2>/dev/null || true
rm -f "$HOME/.local/bin/echo-notes-daemon" 2>/dev/null || true
rm -f "$HOME/.local/bin/echo-notes-python" 2>/dev/null || true
echo -e "${GREEN}Symlinks removed${NC}"

# Remove systemd service
echo -e "${BLUE}Removing systemd service...${NC}"
rm -f "$HOME/.config/systemd/user/echo-notes.service" 2>/dev/null || true
systemctl --user daemon-reload 2>/dev/null || true
rm -f "$HOME/.config/autostart/echo-notes-daemon.desktop" 2>/dev/null || true
echo -e "${GREEN}Service configuration removed${NC}"

# Remove virtual environment
echo -e "${BLUE}Removing virtual environment...${NC}"
rm -rf "$INSTALL_DIR/echo_notes_venv" 2>/dev/null || true
echo -e "${GREEN}Virtual environment removed${NC}"

# Remove user data if requested
if [ "$PURGE" = true ]; then
    echo -e "${RED}Removing user notes...${NC}"
    NOTES_DIR="${ECHO_NOTES_DIR:-$HOME/Documents/notes/log}"
    rm -rf "$NOTES_DIR" 2>/dev/null || true
    echo -e "${RED}User notes removed${NC}"
else
    echo -e "${YELLOW}Preserving user notes${NC}"
    NOTES_DIR="${ECHO_NOTES_DIR:-$HOME/Documents/notes/log}"
    echo -e "${YELLOW}Your notes are still available at: $NOTES_DIR${NC}"
fi

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
rm -f "$HOME/uninstall.py" 2>/dev/null || true
echo -e "${GREEN}Uninstaller script removed.${NC}"

echo -e "${GREEN}Uninstallation completed successfully!${NC}"
EOF
    chmod +x "$HOME/uninstall.sh"
    echo -e "${GREEN}Shell uninstaller script created at: $HOME/uninstall.sh${NC}"
    
    # Create Python uninstaller script
    echo -e "${BLUE}Creating Python uninstaller script...${NC}"
    cat > "$HOME/uninstall.py" << 'EOF'
#!/usr/bin/env python3
"""
Echo-Notes Uninstaller Script
This script provides a simple way to uninstall Echo-Notes.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# ANSI color codes
class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color

def print_color(color, message):
    """Print colored message if supported"""
    if sys.platform != "win32" or os.environ.get("TERM") == "xterm":
        print(f"{color}{message}{Colors.NC}")
    else:
        print(message)

def main():
    """Main uninstaller function"""
    print_color(Colors.BLUE, "===== Echo-Notes Uninstaller =====")
    print("")

    # Default installation directory
    default_install_dir = Path.home() / "Echo-Notes"
    install_dir = None
    purge = False

    # Parse command line arguments
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--install-dir" and i + 1 < len(sys.argv):
            install_dir = Path(sys.argv[i + 1])
            i += 2
        elif arg == "--purge":
            purge = True
            i += 1
        elif arg == "--help":
            print("Echo-Notes Uninstaller")
            print("")
            print("Usage: python uninstall.py [options]")
            print("")
            print("Options:")
            print("  --install-dir DIR    Specify installation directory")
            print("  --purge              Remove user notes as well")
            print("  --help               Show this help message")
            return 0
        else:
            print_color(Colors.RED, f"Unknown option: {arg}")
            print("Use --help for usage information.")
            return 1

    # If installation directory not specified, use default
    if install_dir is None:
        install_dir = default_install_dir
        print_color(Colors.BLUE, f"Using default installation directory: {install_dir}")

    # Check if the installation directory exists
    if not install_dir.exists():
        print_color(Colors.RED, f"Error: Installation directory not found: {install_dir}")
        return 1

    # Confirm uninstallation
    print_color(Colors.YELLOW, f"This will uninstall Echo-Notes from: {install_dir}")
    if purge:
        print_color(Colors.RED, "WARNING: This will also remove all your notes!")

    response = input("Do you want to continue? (y/N) ").strip().lower()
    if response != "y":
        print_color(Colors.YELLOW, "Uninstallation cancelled.")
        return 0

    # Stop running processes
    print_color(Colors.BLUE, "Stopping Echo-Notes processes...")
    try:
        subprocess.run(["systemctl", "--user", "stop", "echo-notes.service"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["systemctl", "--user", "disable", "echo-notes.service"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    
    try:
        subprocess.run(["pkill", "-f", "echo_notes/daemon.py"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "echo_notes/dashboard.py"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    
    print_color(Colors.GREEN, "Echo-Notes processes stopped")

    # Remove desktop shortcuts
    print_color(Colors.BLUE, "Removing desktop shortcuts...")
    desktop_file = Path.home() / ".local/share/applications/echo-notes.desktop"
    if desktop_file.exists():
        desktop_file.unlink()
    
    desktop_icon = Path.home() / "Desktop/Echo Notes.desktop"
    if desktop_icon.exists():
        desktop_icon.unlink()
    
    icon_file = Path.home() / ".local/share/icons/echo-notes.png"
    if icon_file.exists():
        icon_file.unlink()
    
    print_color(Colors.GREEN, "Desktop shortcuts removed")

    # Remove symlinks
    print_color(Colors.BLUE, "Removing symlinks...")
    bin_dir = Path.home() / ".local/bin"
    symlinks = ["echo-notes-python", "echo-notes-dashboard", "echo-notes-daemon"]
    
    for symlink in symlinks:
        symlink_path = bin_dir / symlink
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink(missing_ok=True)
    
    print_color(Colors.GREEN, "Symlinks removed")

    # Remove systemd service
    print_color(Colors.BLUE, "Removing systemd service...")
    service_file = Path.home() / ".config/systemd/user/echo-notes.service"
    if service_file.exists():
        service_file.unlink()
        try:
            subprocess.run(["systemctl", "--user", "daemon-reload"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    
    autostart_file = Path.home() / ".config/autostart/echo-notes-daemon.desktop"
    if autostart_file.exists():
        autostart_file.unlink()
    
    print_color(Colors.GREEN, "Service configuration removed")

    # Remove virtual environment
    print_color(Colors.BLUE, "Removing virtual environment...")
    venv_path = install_dir / "echo_notes_venv"
    if venv_path.exists():
        shutil.rmtree(venv_path)
    print_color(Colors.GREEN, "Virtual environment removed")

    # Remove user data if requested
    if purge:
        print_color(Colors.RED, "Removing user notes...")
        notes_dir = os.environ.get("ECHO_NOTES_DIR")
        if not notes_dir:
            notes_dir = Path.home() / "Documents/notes/log"
        else:
            notes_dir = Path(notes_dir)
        
        if notes_dir.exists():
            shutil.rmtree(notes_dir)
            print_color(Colors.RED, f"User notes removed: {notes_dir}")
    else:
        print_color(Colors.YELLOW, "Preserving user notes")
        notes_dir = os.environ.get("ECHO_NOTES_DIR", str(Path.home() / "Documents/notes/log"))
        print_color(Colors.YELLOW, f"Your notes are still available at: {notes_dir}")

    # Ask if user wants to remove the installation directory
    response = input("Do you want to remove the installation directory? (y/N) ").strip().lower()
    if response == "y":
        try:
            shutil.rmtree(install_dir)
            print_color(Colors.GREEN, f"Installation directory removed: {install_dir}")
        except Exception as e:
            print_color(Colors.RED, f"Error removing installation directory: {e}")
            return 1
    else:
        print_color(Colors.YELLOW, f"Installation directory preserved: {install_dir}")

    # Remove uninstaller scripts
    print_color(Colors.BLUE, "Removing uninstaller scripts...")
    try:
        shell_script = Path.home() / "uninstall.sh"
        if shell_script.exists():
            shell_script.unlink()
            print_color(Colors.GREEN, "Shell uninstaller script removed")
    except Exception:
        pass

    print_color(Colors.GREEN, "Uninstallation completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF
    chmod +x "$HOME/uninstall.py"
    echo -e "${GREEN}Python uninstaller script created at: $HOME/uninstall.py${NC}"
    
    # Provide uninstallation instructions
    echo -e "${YELLOW}To uninstall Echo-Notes, you can run either:${NC}"
    echo -e "${YELLOW}  - ./uninstall.sh${NC}"
    echo -e "${YELLOW}  - python3 uninstall.py${NC}"
    
    # Check if uninstaller scripts exist
    echo -e "${BLUE}Checking if uninstaller scripts exist:${NC}"
    echo -e "${BLUE}uninstall.sh exists: $([ -f "$HOME/uninstall.sh" ] && echo "Yes" || echo "No")${NC}"
    echo -e "${BLUE}uninstall.py exists: $([ -f "$HOME/uninstall.py" ] && echo "Yes" || echo "No")${NC}"
else
    echo -e "${YELLOW}Warning: Echo-Notes installation directory not found at: $HOME/Echo-Notes${NC}"
    echo -e "${YELLOW}Checking for alternative installation locations...${NC}"
    
    # Try to find the Echo-Notes installation directory
    if [ -d "$HOME/echo-notes" ]; then
        echo -e "${GREEN}Found Echo-Notes at: $HOME/echo-notes${NC}"
    elif [ -d "/opt/Echo-Notes" ]; then
        echo -e "${GREEN}Found Echo-Notes at: /opt/Echo-Notes${NC}"
    else
        echo -e "${RED}Could not find Echo-Notes installation directory.${NC}"
        echo -e "${RED}Creating uninstaller scripts anyway, but you will need to specify the installation directory when running them.${NC}"
    fi
    
    # Create uninstaller scripts anyway
    echo -e "${BLUE}Creating uninstaller scripts...${NC}"
    
    # Create shell uninstaller script (same as above)
    echo -e "${BLUE}Creating shell uninstaller script...${NC}"
    cat > "$HOME/uninstall.sh" << 'EOF'
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

# If installation directory not specified, use default
if [ -z "$INSTALL_DIR" ]; then
    INSTALL_DIR="$DEFAULT_INSTALL_DIR"
    echo -e "${BLUE}Using default installation directory: ${INSTALL_DIR}${NC}"
fi

# Check if the installation directory exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${RED}Error: Installation directory not found: ${INSTALL_DIR}${NC}"
    echo -e "${YELLOW}Please specify the correct installation directory using --install-dir${NC}"
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

# Stop running processes
echo -e "${BLUE}Stopping Echo-Notes processes...${NC}"
systemctl --user stop echo-notes.service 2>/dev/null || true
systemctl --user disable echo-notes.service 2>/dev/null || true
pkill -f "echo_notes/daemon.py" 2>/dev/null || true
pkill -f "echo_notes/dashboard.py" 2>/dev/null || true
echo -e "${GREEN}Echo-Notes processes stopped${NC}"

# Remove desktop shortcuts
echo -e "${BLUE}Removing desktop shortcuts...${NC}"
rm -f "$HOME/.local/share/applications/echo-notes.desktop" 2>/dev/null || true
rm -f "$HOME/Desktop/Echo Notes.desktop" 2>/dev/null || true
rm -f "$HOME/.local/share/icons/echo-notes.png" 2>/dev/null || true
echo -e "${GREEN}Desktop shortcuts removed${NC}"

# Remove symlinks
echo -e "${BLUE}Removing symlinks...${NC}"
rm -f "$HOME/.local/bin/echo-notes-dashboard" 2>/dev/null || true
rm -f "$HOME/.local/bin/echo-notes-daemon" 2>/dev/null || true
rm -f "$HOME/.local/bin/echo-notes-python" 2>/dev/null || true
echo -e "${GREEN}Symlinks removed${NC}"

# Remove systemd service
echo -e "${BLUE}Removing systemd service...${NC}"
rm -f "$HOME/.config/systemd/user/echo-notes.service" 2>/dev/null || true
systemctl --user daemon-reload 2>/dev/null || true
rm -f "$HOME/.config/autostart/echo-notes-daemon.desktop" 2>/dev/null || true
echo -e "${GREEN}Service configuration removed${NC}"

# Remove virtual environment
echo -e "${BLUE}Removing virtual environment...${NC}"
rm -rf "$INSTALL_DIR/echo_notes_venv" 2>/dev/null || true
echo -e "${GREEN}Virtual environment removed${NC}"

# Remove user data if requested
if [ "$PURGE" = true ]; then
    echo -e "${RED}Removing user notes...${NC}"
    NOTES_DIR="${ECHO_NOTES_DIR:-$HOME/Documents/notes/log}"
    rm -rf "$NOTES_DIR" 2>/dev/null || true
    echo -e "${RED}User notes removed${NC}"
else
    echo -e "${YELLOW}Preserving user notes${NC}"
    NOTES_DIR="${ECHO_NOTES_DIR:-$HOME/Documents/notes/log}"
    echo -e "${YELLOW}Your notes are still available at: $NOTES_DIR${NC}"
fi

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
rm -f "$HOME/uninstall.py" 2>/dev/null || true
echo -e "${GREEN}Uninstaller script removed.${NC}"

echo -e "${GREEN}Uninstallation completed successfully!${NC}"
EOF
    chmod +x "$HOME/uninstall.sh"
    echo -e "${GREEN}Shell uninstaller script created at: $HOME/uninstall.sh${NC}"
    
    # Create Python uninstaller script (same as above)
    echo -e "${BLUE}Creating Python uninstaller script...${NC}"
    cat > "$HOME/uninstall.py" << 'EOF'
#!/usr/bin/env python3
"""
Echo-Notes Uninstaller Script
This script provides a simple way to uninstall Echo-Notes.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# ANSI color codes
class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color

def print_color(color, message):
    """Print colored message if supported"""
    if sys.platform != "win32" or os.environ.get("TERM") == "xterm":
        print(f"{color}{message}{Colors.NC}")
    else:
        print(message)

def main():
    """Main uninstaller function"""
    print_color(Colors.BLUE, "===== Echo-Notes Uninstaller =====")
    print("")

    # Default installation directory
    default_install_dir = Path.home() / "Echo-Notes"
    install_dir = None
    purge = False

    # Parse command line arguments
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--install-dir" and i + 1 < len(sys.argv):
            install_dir = Path(sys.argv[i + 1])
            i += 2
        elif arg == "--purge":
            purge = True
            i += 1
        elif arg == "--help":
            print("Echo-Notes Uninstaller")
            print("")
            print("Usage: python uninstall.py [options]")
            print("")
            print("Options:")
            print("  --install-dir DIR    Specify installation directory")
            print("  --purge              Remove user notes as well")
            print("  --help               Show this help message")
            return 0
        else:
            print_color(Colors.RED, f"Unknown option: {arg}")
            print("Use --help for usage information.")
            return 1

    # If installation directory not specified, use default
    if install_dir is None:
        install_dir = default_install_dir
        print_color(Colors.BLUE, f"Using default installation directory: {install_dir}")

    # Check if the installation directory exists
    if not install_dir.exists():
        print_color(Colors.RED, f"Error: Installation directory not found: {install_dir}")
        print_color(Colors.YELLOW, "Please specify the correct installation directory using --install-dir")
        return 1

    # Confirm uninstallation
    print_color(Colors.YELLOW, f"This will uninstall Echo-Notes from: {install_dir}")
    if purge:
        print_color(Colors.RED, "WARNING: This will also remove all your notes!")

    response = input("Do you want to continue? (y/N) ").strip().lower()
    if response != "y":
        print_color(Colors.YELLOW, "Uninstallation cancelled.")
        return 0

    # Stop running processes
    print_color(Colors.BLUE, "Stopping Echo-Notes processes...")
    try:
        subprocess.run(["systemctl", "--user", "stop", "echo-notes.service"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["systemctl", "--user", "disable", "echo-notes.service"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    
    try:
        subprocess.run(["pkill", "-f", "echo_notes/daemon.py"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "echo_notes/dashboard.py"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    
    print_color(Colors.GREEN, "Echo-Notes processes stopped")

    # Remove desktop shortcuts
    print_color(Colors.BLUE, "Removing desktop shortcuts...")
    desktop_file = Path.home() / ".local/share/applications/echo-notes.desktop"
    if desktop_file.exists():
        desktop_file.unlink()
    
    desktop_icon = Path.home() / "Desktop/Echo Notes.desktop"
    if desktop_icon.exists():
        desktop_icon.unlink()
    
    icon_file = Path.home() / ".local/share/icons/echo-notes.png"
    if icon_file.exists():
        icon_file.unlink()
    
    print_color(Colors.GREEN, "Desktop shortcuts removed")

    # Remove symlinks
    print_color(Colors.BLUE, "Removing symlinks...")
    bin_dir = Path.home() / ".local/bin"
    symlinks = ["echo-notes-python", "echo-notes-dashboard", "echo-notes-daemon"]
    
    for symlink in symlinks:
        symlink_path = bin_dir / symlink
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink(missing_ok=True)
    
    print_color(Colors.GREEN, "Symlinks removed")

    # Remove systemd service
    print_color(Colors.BLUE, "Removing systemd service...")
    service_file = Path.home() / ".config/systemd/user/echo-notes.service"
    if service_file.exists():
        service_file.unlink()
        try:
            subprocess.run(["systemctl", "--user", "daemon-reload"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    
    autostart_file = Path.home() / ".config/autostart/echo-notes-daemon.desktop"
    if autostart_file.exists():
        autostart_file.unlink()
    
    print_color(Colors.GREEN, "Service configuration removed")

    # Remove virtual environment
    print_color(Colors.BLUE, "Removing virtual environment...")
    venv_path = install_dir / "echo_notes_venv"
    if venv_path.exists():
        shutil.rmtree(venv_path)
    print_color(Colors.GREEN, "Virtual environment removed")

    # Remove user data if requested
    if purge:
        print_color(Colors.RED, "Removing user notes...")
        notes_dir = os.environ.get("ECHO_NOTES_DIR")
        if not notes_dir:
            notes_dir = Path.home() / "Documents/notes/log"
        else:
            notes_dir = Path(notes_dir)
        
        if notes_dir.exists():
            shutil.rmtree(notes_dir)
            print_color(Colors.RED, f"User notes removed: {notes_dir}")
    else:
        print_color(Colors.YELLOW, "Preserving user notes")
        notes_dir = os.environ.get("ECHO_NOTES_DIR", str(Path.home() / "Documents/notes/log"))
        print_color(Colors.YELLOW, f"Your notes are still available at: {notes_dir}")

    # Ask if user wants to remove the installation directory
    response = input("Do you want to remove the installation directory? (y/N) ").strip().lower()
    if response == "y":
        try:
            shutil.rmtree(install_dir)
            print_color(Colors.GREEN, f"Installation directory removed: {install_dir}")
        except Exception as e:
            print_color(Colors.RED, f"Error removing installation directory: {e}")
            return 1
    else:
        print_color(Colors.YELLOW, f"Installation directory preserved: {install_dir}")

    # Remove uninstaller scripts
    print_color(Colors.BLUE, "Removing uninstaller scripts...")
    try:
        shell_script = Path.home() / "uninstall.sh"
        if shell_script.exists():
            shell_script.unlink()
            print_color(Colors.GREEN, "Shell uninstaller script removed")
    except Exception:
        pass

    print_color(Colors.GREEN, "Uninstallation completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF
    chmod +x "$HOME/uninstall.py"
    echo -e "${GREEN}Python uninstaller script created at: $HOME/uninstall.py${NC}"
    
    # Provide uninstallation instructions
    echo -e "${YELLOW}To uninstall Echo-Notes, you can run either:${NC}"
    echo -e "${YELLOW}  - ./uninstall.sh${NC}"
    echo -e "${YELLOW}  - python3 uninstall.py${NC}"
    
    # Check if uninstaller scripts exist
    echo -e "${BLUE}Checking if uninstaller scripts exist:${NC}"
    echo -e "${BLUE}uninstall.sh exists: $([ -f "$HOME/uninstall.sh" ] && echo "Yes" || echo "No")${NC}"
    echo -e "${BLUE}uninstall.py exists: $([ -f "$HOME/uninstall.py" ] && echo "Yes" || echo "No")${NC}"
fi

echo -e "${GREEN}Uninstaller scripts created successfully!${NC}"
echo -e "${GREEN}You can now uninstall Echo-Notes using:${NC}"
echo -e "${GREEN}  - ./uninstall.sh${NC}"
echo -e "${GREEN}  - python3 uninstall.py${NC}"