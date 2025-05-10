# Testing Echo-Notes Installation

This document provides instructions for testing the Echo-Notes installation process.

## Testing Local Changes

Before pushing your changes to GitHub, you can test them locally using the `test_installation.sh` script:

```bash
./test_installation.sh
```

This script will:
1. Create a temporary directory
2. Copy your local Echo-Notes code to the temporary directory
3. Run the installer
4. Test the daemon and dashboard
5. Test the uninstaller
6. Clean up the temporary directory

If all tests pass, your changes are ready to be committed and pushed to GitHub.

## Testing the Package Structure

You can test the Python package structure using the `test_package.py` script:

```bash
python3 test_package.py
```

This script will attempt to import all the modules in the Echo-Notes package and report any issues.

## Testing the One-Click Installer

After pushing your changes to GitHub, you can test the one-click installer using the `test_one_click_installer.sh` script:

```bash
./test_one_click_installer.sh
```

This script will:
1. Create a temporary directory
2. Download the one-click installer from GitHub
3. Run the installer
4. Test the daemon and dashboard
5. Test the uninstaller
6. Clean up the temporary directory

If all tests pass, the one-click installer is working correctly.

## Manual Testing

You can also test the installation process manually:

1. Download the installer:
   ```bash
   curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/install_echo_notes.py
   chmod +x install_echo_notes.py
   ./install_echo_notes.py
   ```

2. Test the daemon:
   ```bash
   echo-notes-daemon --daemon
   ```

3. Test the dashboard:
   ```bash
   echo-notes-dashboard
   ```

4. Test the uninstaller:
   ```bash
   ./uninstall.sh
   ```

## Troubleshooting

If you encounter any issues during testing, check the following:

1. Make sure all files have the correct permissions
2. Check that the Python package structure is correct
3. Verify that the entry points in setup.py are correct
4. Ensure that the virtual environment is being created correctly