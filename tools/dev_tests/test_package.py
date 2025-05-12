#!/usr/bin/env python3
"""
Test script to verify that the Echo-Notes package structure works correctly.
"""

import sys
import importlib

def test_import(module_name):
    """Test importing a module"""
    try:
        module = importlib.import_module(module_name)
        print(f"✅ Successfully imported {module_name}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        return False

def main():
    """Main function"""
    print("Testing Echo-Notes package structure...")
    
    # Test importing the main package
    success = test_import("echo_notes")
    
    # Test importing the modules
    modules = [
        "echo_notes.daemon",
        "echo_notes.dashboard",
        "echo_notes.notes_nextcloud",
        "echo_notes.weekly_summary",
        "echo_notes.shared",
        "echo_notes.shared.config",
        "echo_notes.shared.file_utils",
        "echo_notes.shared.date_helpers"
    ]
    
    for module in modules:
        success = test_import(module) and success
    
    if success:
        print("\nAll imports successful! The package structure is working correctly.")
    else:
        print("\nSome imports failed. Please check the package structure.")
        sys.exit(1)

if __name__ == "__main__":
    main()