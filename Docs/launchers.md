
# Echo-Notes Launch Options

Echo-Notes includes several ways to launch the dashboard and start the daemon, depending on your platform.

---

## 1. Cross-Platform: Python Launcher

Works on all platforms:

```bash
python launcher.py

This opens the GUI dashboard directly using your configured environment.


---

2. Desktop Shortcuts

Linux

Create application shortcuts:

./install_desktop_shortcuts.sh

After running, check your desktop or application menu for:

Echo Notes Dashboard

Echo Notes Dashboard (Direct) – more reliable on some systems


If the shortcut doesn't work:

./fix_desktop_icon.sh

This updates paths in .desktop files to point to the correct Python interpreter.


---

Windows

Run:

create_windows_shortcut.bat

This creates a .lnk desktop shortcut to the dashboard. Ensure Python is properly installed and accessible from PATH.


---

macOS

Run:

python create_macos_shortcut.py

This creates a clickable .app bundle in ~/Applications.

You may need to grant it permissions via System Settings > Privacy & Security.


---

3. Terminal Shortcuts

The following commands work after installation:

echo-notes-dashboard    # Open the dashboard
echo-notes-daemon       # Run daemon in foreground
echo-notes-daemon --daemon  # Run as background process
echo-notes-daemon --stop    # Stop background daemon

These are symlinked to your environment by the installer or setup.py.


---

Troubleshooting

If a shortcut doesn’t launch:

Try the “Direct” version

Run ./fix_desktop_icon.sh

Ensure Python is available in PATH

Re-run the installer or create shortcuts again




---

For systemd and cron scheduling, see scheduling.md.
