#!/bin/bash
# Test script for Echo-Notes installer and uninstaller

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Echo-Notes Installer/Uninstaller Test =====${NC}"
echo ""

# Create a temporary test directory
TEST_DIR=$(mktemp -d)
echo -e "${BLUE}Using temporary test directory: ${TEST_DIR}${NC}"

# Copy the uninstaller scripts to the test directory
echo -e "${BLUE}Copying uninstaller scripts...${NC}"
cp uninstall.sh "${TEST_DIR}/"
cp uninstall.py "${TEST_DIR}/"

# Make the scripts executable
chmod +x "${TEST_DIR}/uninstall.sh"
chmod +x "${TEST_DIR}/uninstall.py"

# Set the installation directory
INSTALL_DIR="${TEST_DIR}/Echo-Notes"

# Test the installer
echo -e "${BLUE}Testing installer...${NC}"
./installers/install_linux.sh --install-dir "${INSTALL_DIR}" --no-shortcuts --no-symlinks --no-service

# Check if uninstaller scripts were copied to the home directory
echo -e "${BLUE}Checking if uninstaller scripts were copied...${NC}"
if [ -f "${HOME}/uninstall.sh" ]; then
    echo -e "${GREEN}Shell uninstaller script found: ${HOME}/uninstall.sh${NC}"
else
    echo -e "${RED}Shell uninstaller script not found!${NC}"
fi

if [ -f "${HOME}/uninstall.py" ]; then
    echo -e "${GREEN}Python uninstaller script found: ${HOME}/uninstall.py${NC}"
else
    echo -e "${RED}Python uninstaller script not found!${NC}"
fi

# Test the shell uninstaller
echo -e "${BLUE}Testing shell uninstaller...${NC}"
if [ -f "${HOME}/uninstall.sh" ]; then
    # Run the uninstaller non-interactively
    echo "y" | "${HOME}/uninstall.sh" --install-dir "${TEST_DIR}/Echo-Notes"
    echo "y" # For the "remove installation directory" prompt
    
    # Check if the installation directory was removed
    if [ ! -d "${TEST_DIR}/Echo-Notes" ]; then
        echo -e "${GREEN}Shell uninstaller successfully removed the installation directory${NC}"
    else
        echo -e "${RED}Shell uninstaller failed to remove the installation directory!${NC}"
    fi
else
    echo -e "${YELLOW}Skipping shell uninstaller test (script not found)${NC}"
fi

# Clean up
echo -e "${BLUE}Cleaning up...${NC}"
rm -rf "${TEST_DIR}"

# Reinstall for Python uninstaller test
echo -e "${BLUE}Reinstalling for Python uninstaller test...${NC}"
./installers/install_linux.sh --install-dir "${INSTALL_DIR}" --no-shortcuts --no-symlinks --no-service

# Test the Python uninstaller
echo -e "${BLUE}Testing Python uninstaller...${NC}"
if [ -f "${HOME}/uninstall.py" ]; then
    # Run the uninstaller non-interactively
    echo "y" | python3 "${HOME}/uninstall.py" --install-dir "${TEST_DIR}/Echo-Notes"
    echo "y" # For the "remove installation directory" prompt
    
    # Check if the installation directory was removed
    if [ ! -d "${TEST_DIR}/Echo-Notes" ]; then
        echo -e "${GREEN}Python uninstaller successfully removed the installation directory${NC}"
    else
        echo -e "${RED}Python uninstaller failed to remove the installation directory!${NC}"
    fi
else
    echo -e "${YELLOW}Skipping Python uninstaller test (script not found)${NC}"
fi

# Final cleanup
echo -e "${BLUE}Final cleanup...${NC}"
rm -rf "${TEST_DIR}"

echo -e "${GREEN}Test completed!${NC}"