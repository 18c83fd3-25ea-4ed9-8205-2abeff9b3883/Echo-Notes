#!/bin/bash
# Test script for the standalone Linux installer

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "Testing standalone Linux installer in $TEMP_DIR"

# Download the installer
echo "Downloading installer..."
curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/installers/install_linux.sh

# Make it executable
chmod +x install_linux.sh

# Run the installer with download-only option to test the download functionality
echo "Running installer with --download-only option..."
./install_linux.sh --download-only

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "Download test passed!"
else
    echo "Download test failed!"
    exit 1
fi

# Clean up
cd -
rm -rf "$TEMP_DIR"

echo "Test completed successfully!"