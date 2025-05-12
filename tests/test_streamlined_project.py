#!/usr/bin/env python3
"""
Echo-Notes Streamlined Project Test Script

This script tests the streamlined Echo-Notes project to ensure it still functions correctly.
It verifies that:
1. The package can be imported
2. Core modules are accessible
3. Basic functionality works

Usage:
    python test_streamlined_project.py [--dist-dir DIST_DIR]

Options:
    --dist-dir DIST_DIR    Path to the streamlined project directory (default: ./dist)
"""

import os
import sys
import argparse
import importlib.util
import subprocess
from pathlib import Path


class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_color(color, message):
    """Print colored message if supported"""
    if sys.platform != "win32" or os.environ.get("TERM") == "xterm":
        print(f"{color}{message}{Colors.NC}")
    else:
        print(message)


def import_module_from_path(module_name, file_path):
    """Import a module from a file path"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print_color(Colors.RED, f"Error importing {module_name} from {file_path}: {e}")
        return None


def test_package_structure(dist_dir):
    """Test that the package structure is correct"""
    print_color(Colors.BLUE, "Testing package structure...")
    
    # Check that essential directories exist
    essential_dirs = [
        "echo_notes",
        "echo_notes/shared",
        "tests",
        "Docs",
    ]
    
    for directory in essential_dirs:
        dir_path = os.path.join(dist_dir, directory)
        if os.path.isdir(dir_path):
            print_color(Colors.GREEN, f"✓ Directory exists: {directory}")
        else:
            print_color(Colors.RED, f"✗ Directory missing: {directory}")
            return False
    
    # Check that essential files exist
    essential_files = [
        "echo_notes/__init__.py",
        "echo_notes/daemon.py",
        "echo_notes/dashboard.py",
        "echo_notes/notes_nextcloud.py",
        "echo_notes/weekly_summary.py",
        "echo_notes/shared/__init__.py",
        "echo_notes/shared/config.py",
        "echo_notes/shared/date_helpers.py",
        "echo_notes/shared/file_utils.py",
        "setup.py",
        "requirements.txt",
        "README.md",
    ]
    
    for file in essential_files:
        file_path = os.path.join(dist_dir, file)
        if os.path.isfile(file_path):
            print_color(Colors.GREEN, f"✓ File exists: {file}")
        else:
            print_color(Colors.RED, f"✗ File missing: {file}")
            return False
    
    return True


def test_module_imports(dist_dir):
    """Test that modules can be imported"""
    print_color(Colors.BLUE, "Testing module imports...")
    
    # Add the dist directory to the Python path
    sys.path.insert(0, dist_dir)
    
    # Try to import the echo_notes package
    try:
        import echo_notes
        print_color(Colors.GREEN, "✓ Successfully imported echo_notes package")
    except ImportError as e:
        print_color(Colors.RED, f"✗ Failed to import echo_notes package: {e}")
        return False
    
    # Try to import specific modules
    modules = [
        "echo_notes.daemon",
        "echo_notes.dashboard",
        "echo_notes.notes_nextcloud",
        "echo_notes.weekly_summary",
        "echo_notes.shared.config",
        "echo_notes.shared.date_helpers",
        "echo_notes.shared.file_utils",
    ]
    
    for module_name in modules:
        try:
            module = importlib.import_module(module_name)
            print_color(Colors.GREEN, f"✓ Successfully imported {module_name}")
        except ImportError as e:
            print_color(Colors.RED, f"✗ Failed to import {module_name}: {e}")
            return False
    
    return True


def test_basic_functionality(dist_dir):
    """Test basic functionality of the package"""
    print_color(Colors.BLUE, "Testing basic functionality...")
    
    # Add the dist directory to the Python path
    sys.path.insert(0, dist_dir)
    
    # Test file_utils functionality
    try:
        from echo_notes.shared import file_utils
        
        # Create a test file
        test_file = os.path.join(dist_dir, "test_file.txt")
        with open(test_file, "w") as f:
            f.write("Test content")
        
        # Test file operations
        if os.path.exists(test_file):
            print_color(Colors.GREEN, "✓ Successfully created test file")
        else:
            print_color(Colors.RED, "✗ Failed to create test file")
            return False
        
        # Clean up
        os.remove(test_file)
        if not os.path.exists(test_file):
            print_color(Colors.GREEN, "✓ Successfully removed test file")
        else:
            print_color(Colors.RED, "✗ Failed to remove test file")
            return False
        
    except Exception as e:
        print_color(Colors.RED, f"✗ Error testing file_utils: {e}")
        return False
    
    # Test date_helpers functionality
    try:
        from echo_notes.shared import date_helpers
        
        # Test date functions if they exist
        if hasattr(date_helpers, "get_current_date"):
            date = date_helpers.get_current_date()
            print_color(Colors.GREEN, f"✓ Successfully called get_current_date(): {date}")
        
    except Exception as e:
        print_color(Colors.RED, f"✗ Error testing date_helpers: {e}")
        return False
    
    return True


def test_package_installation(dist_dir):
    """Test that the package can be installed"""
    print_color(Colors.BLUE, "Testing package installation...")
    
    # Run pip install in development mode
    cmd = [sys.executable, "-m", "pip", "install", "-e", dist_dir]
    print_color(Colors.BLUE, f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print_color(Colors.GREEN, "✓ Successfully installed package in development mode")
        return True
    except subprocess.CalledProcessError as e:
        print_color(Colors.RED, f"✗ Failed to install package: {e}")
        print_color(Colors.RED, f"STDOUT: {e.stdout}")
        print_color(Colors.RED, f"STDERR: {e.stderr}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Echo-Notes Streamlined Project Test Script")
    parser.add_argument("--dist-dir", default="./dist", help="Path to the streamlined project directory")
    args = parser.parse_args()
    
    dist_dir = os.path.abspath(args.dist_dir)
    print_color(Colors.BLUE, f"Testing streamlined project in: {dist_dir}")
    
    if not os.path.isdir(dist_dir):
        print_color(Colors.RED, f"Error: Directory not found: {dist_dir}")
        print_color(Colors.YELLOW, "Have you run streamline_project.py first?")
        return 1
    
    # Run tests
    tests = [
        ("Package Structure", test_package_structure),
        ("Module Imports", test_module_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Package Installation", test_package_installation),
    ]
    
    all_passed = True
    for name, test_func in tests:
        print_color(Colors.BLUE, f"\n=== Testing: {name} ===")
        if test_func(dist_dir):
            print_color(Colors.GREEN, f"✓ {name} tests passed!")
        else:
            print_color(Colors.RED, f"✗ {name} tests failed!")
            all_passed = False
    
    print()
    if all_passed:
        print_color(Colors.GREEN, "✓ All tests passed! The streamlined project works correctly.")
        return 0
    else:
        print_color(Colors.RED, "✗ Some tests failed. Please check the output for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())