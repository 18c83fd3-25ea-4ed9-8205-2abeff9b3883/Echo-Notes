#!/bin/bash
# Test script for Echo-Notes one-click installer
# This script tests the one-click installer by downloading it from GitHub

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

# Change to the temporary directory
cd $TEST_DIR
print_color $BLUE "Changed to temporary directory: $TEST_DIR"

# Download the installer
print_color $BLUE "Downloading Echo-Notes one-click installer..."
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/install_echo_notes.py
chmod +x install_echo_notes.py
print_color $GREEN "Downloaded Echo-Notes one-click installer"

# Run the installer
print_color $BLUE "Running Echo-Notes one-click installer..."
print_color $YELLOW "Note: You will be prompted for an installation directory."
print_color $YELLOW "Please enter: $TEST_DIR/Echo-Notes"
./install_echo_notes.py

# Change to the installation directory
cd $TEST_DIR/Echo-Notes
print_color $BLUE "Changed to installation directory: $TEST_DIR/Echo-Notes"

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
./uninstall.sh

# Clean up
print_color $BLUE "Cleaning up temporary directory..."
cd /tmp
rm -rf $TEST_DIR
print_color $GREEN "Cleaned up temporary directory"

print_color $GREEN "All tests completed successfully!"
print_color $GREEN "The one-click installer is working correctly."