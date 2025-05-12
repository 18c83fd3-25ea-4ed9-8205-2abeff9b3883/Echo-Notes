#!/usr/bin/env python3
"""
Create a macOS application shortcut for Echo Notes Dashboard
"""

import os
import sys
import subprocess
from pathlib import Path

def create_macos_app():
    """Create a macOS .app bundle for Echo Notes Dashboard"""
    
    # Get the user's Applications folder
    applications_dir = Path.home() / "Applications"
    app_dir = applications_dir / "Echo Notes Dashboard.app"
    
    # Create the directory structure
    os.makedirs(app_dir / "Contents" / "MacOS", exist_ok=True)
    os.makedirs(app_dir / "Contents" / "Resources", exist_ok=True)
    
    # Copy the icon file
    script_dir = Path(__file__).parent.parent.parent
    icon_path = script_dir / "config/icons/Echo-Notes-Icon.png"
    if icon_path.exists():
        import shutil
        resources_icon_path = app_dir / "Contents" / "Resources" / "echo-notes.png"
        shutil.copy(icon_path, resources_icon_path)
        print(f"Copied icon to {resources_icon_path}")
    
    # Create the Info.plist file
    info_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>echo-notes-launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.echo-notes.dashboard</string>
    <key>CFBundleName</key>
    <string>Echo Notes Dashboard</string>
    <key>CFBundleDisplayName</key>
    <string>Echo Notes Dashboard</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleIconFile</key>
    <string>echo-notes.png</string>
</dict>
</plist>
"""
    
    with open(app_dir / "Contents" / "Info.plist", "w") as f:
        f.write(info_plist)
    
    # Create the launcher script
    launcher_script = """#!/bin/bash
echo-notes-dashboard
"""
    
    launcher_path = app_dir / "Contents" / "MacOS" / "echo-notes-launcher"
    with open(launcher_path, "w") as f:
        f.write(launcher_script)
    
    # Make the launcher script executable
    os.chmod(launcher_path, 0o755)
    
    print(f"Echo Notes Dashboard app created at: {app_dir}")
    print("You can now launch it from your Applications folder.")

if __name__ == "__main__":
    try:
        create_macos_app()
    except Exception as e:
        print(f"Error creating macOS app: {e}")
        sys.exit(1)