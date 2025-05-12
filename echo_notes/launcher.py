#!/usr/bin/env python3
"""
Simple launcher for Echo Notes Dashboard
This file can be double-clicked to launch the dashboard without using the command line
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def main():
    """Launch the Echo Notes Dashboard"""
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent.parent.absolute()
        
        # Path to the dashboard script
        dashboard_script = script_dir / "echo_notes/dashboard.py"
        
        if not dashboard_script.exists():
            print(f"Error: Dashboard script not found at {dashboard_script}")
            input("Press Enter to exit...")
            return
        
        # Check for icon file
        icon_path = script_dir / "config/icons/Echo-Notes-Icon.png"
        if not icon_path.exists():
            print(f"Warning: Icon file not found at {icon_path}")
        else:
            print(f"Found icon file at {icon_path}")
        
        # Launch the dashboard
        print(f"Launching Echo Notes Dashboard from {dashboard_script}")
        
        # Use subprocess to launch the dashboard in a new process
        # This allows this launcher to exit while the dashboard continues running
        if sys.platform == "win32":
            # On Windows, use pythonw.exe to avoid showing a console window
            subprocess.Popen([sys.executable, str(dashboard_script)],
                            creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            # On Linux/macOS
            env = os.environ.copy()
            # Set environment variables that might help with icon display on some desktop environments
            if icon_path.exists():
                env["ICON_PATH"] = str(icon_path)
            subprocess.Popen([sys.executable, str(dashboard_script)], env=env)
            
        print("Dashboard launched successfully!")
        
    except Exception as e:
        print(f"Error launching dashboard: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()