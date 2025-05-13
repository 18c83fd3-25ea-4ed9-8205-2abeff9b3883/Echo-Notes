# Fix Echo-Notes Linux Installation Issues

## Problem

Users have reported that after installing Echo-Notes using either the standard Linux installer or the wrapper script, the application doesn't appear in their application menu. This is due to several issues:

1. The `install_echo_notes.sh` script has a malformed shebang line that starts with `git #!/bin/bash` instead of just `#!/bin/bash`, causing the git command to execute and show its help message.
2. The installation process downloads the repository files but fails to properly create desktop shortcuts and application menu entries.
3. The installation doesn't set the proper executable permissions for Python scripts.

## Solution

This PR includes:

1. A fix for the malformed shebang line in `install_echo_notes.sh`
2. A new script `create_desktop_entry.sh` that creates desktop shortcuts and application menu entries
3. Documentation in `README_DESKTOP_ENTRY.md` explaining how to use the script

## Changes

- Fixed the shebang line in `install_echo_notes.sh` from `git #!/bin/bash` to `#!/bin/bash`
- Added `create_desktop_entry.sh` script to create desktop shortcuts and application menu entries
- Added `README_DESKTOP_ENTRY.md` with documentation on how to use the script

## Testing

The fix has been tested on a Linux system where Echo-Notes was installed but not appearing in the application menu. After running the `create_desktop_entry.sh` script, the application appeared in the menu and could be launched successfully.

## Screenshots

N/A

## Related Issues

This fixes the issue where Echo-Notes doesn't appear in the application menu after installation.