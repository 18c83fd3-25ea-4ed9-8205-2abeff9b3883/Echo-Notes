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
    cat > "$TEMP_SCRIPT" << 'EOF'
import os
import sys
import tempfile
import urllib.request
import zipfile
import io
import shutil
import ssl
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

def download_echo_notes(install_dir=None):
    """Download Echo-Notes repository"""
    repo_url = "https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes"
    branch = "main"
    
    print_color(Colors.BLUE, "Downloading Echo-Notes...")
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Using temporary directory: {temp_dir}")
    
    try:
        # Construct the download URL
        url = f"{repo_url}/archive/refs/heads/{branch}.zip"
        print_color(Colors.YELLOW, f"Downloading from: {url}")
        
        # Create a context that doesn't verify SSL certificates if needed
        context = ssl._create_unverified_context() if hasattr(ssl, "_create_unverified_context") else None
        
        # Download the zip file
        with urllib.request.urlopen(url, context=context) as response:
            zip_data = response.read()
        
        # Extract the ZIP file
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the extracted directory
        extracted_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))]
        
        if not extracted_dirs:
            print_color(Colors.RED, "Error: Could not find extracted directory.")
            return None
        
        extracted_dir = os.path.join(temp_dir, extracted_dirs[0])
        print_color(Colors.GREEN, f"Downloaded and extracted to: {extracted_dir}")
        
        # If no install_dir provided, use the current directory
        if install_dir is None:
            install_dir = Path.cwd()
        else:
            install_dir = Path(install_dir)
        
        # Copy files to installation directory
        print_color(Colors.YELLOW, f"Copying files to: {install_dir}")
        
        try:
            # Create installation directory if it doesn't exist
            os.makedirs(install_dir, exist_ok=True)
            
            # Copy files to installation directory
            for item in os.listdir(extracted_dir):
                src = os.path.join(extracted_dir, item)
                dst = os.path.join(install_dir, item)
                
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            
            print_color(Colors.GREEN, "Files copied successfully")
            
            # Clean up temporary files
            print_color(Colors.YELLOW, "Cleaning up temporary files...")
            shutil.rmtree(temp_dir, ignore_errors=True)
            print_color(Colors.GREEN, "Temporary files cleaned up")
            
            return install_dir
            
        except Exception as e:
            print_color(Colors.RED, f"Error copying files: {e}")
            return None
            
    except Exception as e:
        print_color(Colors.RED, f"Error downloading Echo-Notes: {e}")
        return None

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
cat > "$TEMP_SCRIPT" << 'EOF'
import os
import sys
import platform
import subprocess
import shutil
import venv
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

def check_python_version(min_version=(3, 7)):
    """Check if the current Python version meets the minimum requirement."""
    if sys.version_info < min_version:
        print_color(Colors.RED, f"Error: Python {min_version[0]}.{min_version[1]} or higher is required.")
        print_color(Colors.RED, f"Current Python version: {sys.version}")
        return False
    print_color(Colors.GREEN, f"Python version check passed: {sys.version}")
    return True

def test_pip(pip_path):
    """Test if pip is working in a virtual environment."""
    try:
        subprocess.run([str(pip_path), "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def create_virtual_environment(install_dir, venv_name="echo_notes_venv"):
    """Create a Python virtual environment."""
    install_dir = Path(install_dir)
    venv_path = install_dir / venv_name
    
    print_color(Colors.BLUE, "Setting up virtual environment...")
    
    # Remove existing virtual environment if it's broken
    if venv_path.exists():
        # Test if pip is working in the existing venv
        os_type = platform.system().lower()
        pip_path = venv_path / ("Scripts" if os_type == "windows" else "bin") / "pip"
        
        if not pip_path.exists() or not test_pip(pip_path):
            print_color(Colors.YELLOW, "Existing virtual environment appears to be broken. Recreating...")
            shutil.rmtree(venv_path, ignore_errors=True)
        else:
            print_color(Colors.YELLOW, "Using existing virtual environment")
            return venv_path
    
    # Create virtual environment if it doesn't exist
    if not venv_path.exists():
        print_color(Colors.BLUE, "Creating new virtual environment...")
        try:
            venv.create(venv_path, with_pip=True)
            print_color(Colors.GREEN, "Created virtual environment")
        except Exception as e:
            print_color(Colors.RED, f"Error creating virtual environment: {e}")
            return None
    
    return venv_path

def install_dependencies(venv_path, requirements_file=None, dev_mode=True):
    """Install dependencies in the virtual environment."""
    print_color(Colors.BLUE, "Installing dependencies...")
    
    os_type = platform.system().lower()
    pip_path = venv_path / ("Scripts" if os_type == "windows" else "bin") / "pip"
    
    # Upgrade pip
    try:
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        print_color(Colors.GREEN, "Pip upgraded successfully")
    except subprocess.SubprocessError as e:
        print_color(Colors.RED, f"Error upgrading pip: {e}")
        return False
    
    # Install required packages
    try:
        subprocess.run([str(pip_path), "install", "requests", "python-dateutil", "PyQt6"], check=True)
        print_color(Colors.GREEN, "Installed core dependencies")
    except subprocess.SubprocessError as e:
        print_color(Colors.RED, f"Error installing core dependencies: {e}")
        return False
    
    # Install from requirements.txt if available
    if requirements_file and Path(requirements_file).exists():
        try:
            subprocess.run([str(pip_path), "install", "-r", str(requirements_file)], check=True)
            print_color(Colors.GREEN, "Installed dependencies from requirements.txt")
        except subprocess.SubprocessError as e:
            print_color(Colors.RED, f"Error installing from requirements.txt: {e}")
            return False
    
    # Install the package in development mode
    if dev_mode:
        try:
            subprocess.run([str(pip_path), "install", "-e", "."], check=True)
            print_color(Colors.GREEN, "Installed Echo-Notes in development mode")
        except subprocess.SubprocessError as e:
            print_color(Colors.RED, f"Error installing in development mode: {e}")
            return False
    
    return True

def configure_application(install_dir):
    """Configure the Echo-Notes application."""
    print_color(Colors.BLUE, "Configuring Echo-Notes...")
    install_dir = Path(install_dir)
    
    # Create default configuration if needed
    config_dir = install_dir / "shared"
    config_file = config_dir / "schedule_config.json"
    
    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
    
    if not config_file.exists():
        default_config = """{
    "processing_interval": 60,
    "summary_interval": 10080,
    "summary_day": 6,
    "summary_hour": 12,
    "daemon_enabled": true
}"""
        try:
            with open(config_file, "w") as f:
                f.write(default_config)
            print_color(Colors.GREEN, "Created default schedule configuration")
        except IOError as e:
            print_color(Colors.RED, f"Error creating configuration file: {e}")
            return False
    
    # Ensure the notes directory exists
    notes_dir = os.environ.get("ECHO_NOTES_DIR", str(Path.home() / "Documents/notes/log"))
    try:
        os.makedirs(notes_dir, exist_ok=True)
        print_color(Colors.GREEN, f"Ensured notes directory exists: {notes_dir}")
    except OSError as e:
        print_color(Colors.RED, f"Error creating notes directory: {e}")
        return False
    
    return True

def create_desktop_shortcuts(install_dir, venv_path):
    """Create Linux desktop shortcuts and application menu entries."""
    print_color(Colors.BLUE, "Creating desktop shortcuts and application menu entries...")
    
    try:
        # Install the icon
        icons_dir = Path.home() / ".local/share/icons"
        os.makedirs(icons_dir, exist_ok=True)
        
        icon_path = install_dir / "Echo-Notes-Icon.png"
        if icon_path.exists():
            shutil.copy(icon_path, icons_dir / "echo-notes.png")
            print_color(Colors.GREEN, f"Installed icon to {icons_dir}/echo-notes.png")
        else:
            print_color(Colors.YELLOW, "Icon file not found, shortcuts will use default icon")
        
        # Create applications directory if it doesn't exist
        applications_dir = Path.home() / ".local/share/applications"
        os.makedirs(applications_dir, exist_ok=True)
        
        # Create desktop entry file
        desktop_file_path = applications_dir / "echo-notes.desktop"
        with open(desktop_file_path, "w") as f:
            f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Notes
Comment=Monitor and control Echo-Notes daemon
Exec={venv_path}/bin/python {install_dir}/echo_notes/dashboard.py
Icon={Path.home()}/.local/share/icons/echo-notes.png
Terminal=false
Categories=Utility;
""")
        
        # Make the desktop file executable
        os.chmod(desktop_file_path, 0o755)
        
        # Create desktop icon if Desktop directory exists
        desktop_dir = Path.home() / "Desktop"
        if desktop_dir.exists():
            desktop_icon_path = desktop_dir / "Echo Notes.desktop"
            shutil.copy(desktop_file_path, desktop_icon_path)
            os.chmod(desktop_icon_path, 0o755)
            print_color(Colors.GREEN, f"Created desktop icon at {desktop_icon_path}")
        
        # Update desktop database if command exists
        try:
            subprocess.run(["update-desktop-database", str(applications_dir)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        
        print_color(Colors.GREEN, "Desktop shortcuts created successfully")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error creating desktop shortcuts: {e}")
        return False

def create_symlinks(install_dir, venv_path):
    """Create symlinks in ~/.local/bin for Echo-Notes executables."""
    print_color(Colors.BLUE, "Creating symlinks in ~/.local/bin...")
    
    try:
        # Create ~/.local/bin if it doesn't exist
        bin_dir = Path.home() / ".local/bin"
        os.makedirs(bin_dir, exist_ok=True)
        
        # Create symlinks
        symlinks = {
            "echo-notes-dashboard": install_dir / "echo_notes/dashboard.py",
            "echo-notes-daemon": install_dir / "echo_notes/daemon.py",
            "echo-notes-python": venv_path / "bin" / "python",
        }
        
        for name, target in symlinks.items():
            symlink_path = bin_dir / name
            
            # Remove existing symlink if it exists
            if symlink_path.exists() or symlink_path.is_symlink():
                os.unlink(symlink_path)
            
            # Create new symlink
            os.symlink(target, symlink_path)
            os.chmod(symlink_path, 0o755)
            print_color(Colors.GREEN, f"Created symlink: {symlink_path} -> {target}")
        
        # Add ~/.local/bin to PATH if not already there
        path_updated = False
        for shell_rc in [".bashrc", ".zshrc", ".profile"]:
            rc_file = Path.home() / shell_rc
            if rc_file.exists():
                with open(rc_file, "r") as f:
                    content = f.read()
                
                if 'PATH="$HOME/.local/bin:$PATH"' not in content and "PATH=$HOME/.local/bin:$PATH" not in content:
                    with open(rc_file, "a") as f:
                        f.write('\n# Added by Echo-Notes installer\nexport PATH="$HOME/.local/bin:$PATH"\n')
                    path_updated = True
        
        if path_updated:
            print_color(Colors.YELLOW, "Added ~/.local/bin to PATH in shell configuration files")
            print_color(Colors.YELLOW, "You may need to restart your terminal or run 'source ~/.bashrc' for changes to take effect")
        
        print_color(Colors.GREEN, "Symlinks created successfully")
        return True
    except Exception as e:
        print_color(Colors.RED, f"Error creating symlinks: {e}")
        return False

def setup_systemd_service(install_dir, venv_path):
    """Set up Echo-Notes daemon as a systemd user service."""
    print_color(Colors.BLUE, "Setting up Echo-Notes daemon service...")
    
    try:
        # Create systemd user directory if it doesn't exist
        systemd_dir = Path.home() / ".config/systemd/user"
        os.makedirs(systemd_dir, exist_ok=True)
        
        # Create service file
        service_file_path = systemd_dir / "echo-notes.service"
        with open(service_file_path, "w") as f:
            f.write(f"""[Unit]
Description=Echo-Notes Daemon Service
After=network.target

[Service]
Type=simple
ExecStart={venv_path}/bin/python {install_dir}/echo_notes/daemon.py --daemon
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
""")
        
        # Enable and start the service
        try:
            subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "--user", "enable", "echo-notes.service"], check=True)
            subprocess.run(["systemctl", "--user", "start", "echo-notes.service"], check=True)
            
            print_color(Colors.GREEN, "Echo-Notes daemon service set up and started")
            return True
        except subprocess.SubprocessError as e:
            print_color(Colors.YELLOW, f"Could not set up systemd service: {e}")
            print_color(Colors.YELLOW, "Setting up alternative startup method...")
            
            # Create autostart directory if it doesn't exist
            autostart_dir = Path.home() / ".config/autostart"
            os.makedirs(autostart_dir, exist_ok=True)
            
            # Create autostart entry
            autostart_file_path = autostart_dir / "echo-notes-daemon.desktop"
            with open(autostart_file_path, "w") as f:
                f.write(f"""[Desktop Entry]
Type=Application
Name=Echo Notes Daemon
Comment=Echo-Notes background service
Exec={venv_path}/bin/python {install_dir}/echo_notes/daemon.py --daemon
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
""")
            
            # Start the daemon now
            try:
                subprocess.Popen([f"{venv_path}/bin/python", f"{install_dir}/echo_notes/daemon.py", "--daemon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print_color(Colors.GREEN, "Echo-Notes daemon started and set to run at login")
                return True
            except Exception as e2:
                print_color(Colors.RED, f"Error starting daemon: {e2}")
                print_color(Colors.YELLOW, "You can start the daemon manually using:")
                print(f"{venv_path}/bin/python {install_dir}/echo_notes/daemon.py --daemon")
                return False
    except Exception as e:
        print_color(Colors.RED, f"Error setting up daemon service: {e}")
        print_color(Colors.YELLOW, "You can start the daemon manually using:")
        print(f"{venv_path}/bin/python {install_dir}/echo_notes/daemon.py --daemon")
        return False

def install_linux(install_dir, options):
    """Perform Linux-specific installation."""
    # Check Python version
    if not check_python_version():
        return False
    
    install_dir = Path(install_dir)
    print_color(Colors.BLUE, f"Installing Echo-Notes to {install_dir}...")
    
    # Create virtual environment
    venv_path = create_virtual_environment(install_dir)
    if not venv_path:
        return False
    
    # Install dependencies
    requirements_file = install_dir / "requirements.txt"
    if not install_dependencies(venv_path, requirements_file):
        return False
    
    # Configure application
    if not configure_application(install_dir):
        return False
    
    # Create desktop shortcuts
    if not options.get("no_shortcuts", False):
        create_desktop_shortcuts(install_dir, venv_path)
    else:
        print_color(Colors.YELLOW, "Skipping desktop shortcuts creation as requested")
    
    # Create symlinks
    if not options.get("no_symlinks", False):
        create_symlinks(install_dir, venv_path)
    else:
        print_color(Colors.YELLOW, "Skipping symlink creation as requested")
    
    # Set up systemd service
    if not options.get("no_service", False):
        setup_systemd_service(install_dir, venv_path)
    else:
        print_color(Colors.YELLOW, "Skipping service setup as requested")
    
    print_color(Colors.GREEN, "Linux installation completed successfully!")
    print("")
    print_color(Colors.BLUE, "=== Getting Started ===")
    print("1. The Echo-Notes daemon has been set up to start automatically at login")
    print("2. Launch the dashboard using the desktop shortcut or application menu")
    print("3. You can also run the dashboard directly with:")
    print(f"   {venv_path}/bin/python {install_dir}/echo_notes/dashboard.py")
    print("")
    
    return True

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