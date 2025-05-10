#!/bin/bash
# Test script for Echo-Notes installation
# This script creates a temporary directory and tests the installation process

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_color() {
    echo -e "${1}${2}${NC}"
}

# Create a temporary directory
print_color $BLUE "Creating temporary test directory..."
TEST_DIR=$(mktemp -d)
print_color $GREEN "Created temporary directory: $TEST_DIR"

# Get the current directory (where the Echo-Notes code is)
CURRENT_DIR=$(pwd)
print_color $BLUE "Current directory: $CURRENT_DIR"

# Copy the Echo-Notes code to the temporary directory
print_color $BLUE "Copying Echo-Notes code to temporary directory..."
cp -r $CURRENT_DIR/* $TEST_DIR/
print_color $GREEN "Copied Echo-Notes code to temporary directory"

# Change to the temporary directory
cd $TEST_DIR
print_color $BLUE "Changed to temporary directory: $TEST_DIR"

# Create a test installation directory
print_color $BLUE "Creating test installation directory..."
INSTALL_DIR="$TEST_DIR/test_install"
mkdir -p $INSTALL_DIR
print_color $GREEN "Created test installation directory: $INSTALL_DIR"

# Run the installer
print_color $BLUE "Running Echo-Notes installer..."
python3 echo_notes_installer.py
print_color $GREEN "Installation completed successfully!"

# Test the installation
print_color $BLUE "Testing the installation..."
print_color $YELLOW "1. Testing daemon startup..."
echo_notes_venv/bin/echo-notes-daemon --daemon
print_color $GREEN "Daemon started successfully!"

print_color $YELLOW "2. Testing dashboard startup (will be terminated after 5 seconds)..."
echo_notes_venv/bin/echo-notes-dashboard &
DASHBOARD_PID=$!
sleep 5
kill $DASHBOARD_PID
print_color $GREEN "Dashboard started successfully!"

# Test the uninstaller
print_color $BLUE "Testing the uninstaller..."
python3 uninstall.py --keep-config

# Clean up
print_color $BLUE "Cleaning up temporary directory..."
cd $CURRENT_DIR
rm -rf $TEST_DIR
print_color $GREEN "Cleaned up temporary directory"

print_color $GREEN "All tests completed successfully!"
print_color $YELLOW "You can now commit and push your changes to GitHub."