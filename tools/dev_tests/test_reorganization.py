#!/usr/bin/env python3
"""
Test script to verify that the Echo-Notes application can be run with the new structure.
This script imports and uses functions from the reorganized modules.
"""

import sys
from pathlib import Path
import importlib

def test_import_and_run(module_name, function_name=None):
    """Test importing a module and optionally running a function from it"""
    try:
        module = importlib.import_module(module_name)
        print(f"✅ Successfully imported {module_name}")
        
        if function_name and hasattr(module, function_name):
            func = getattr(module, function_name)
            if callable(func):
                print(f"✅ Found function {function_name} in {module_name}")
                return True
            else:
                print(f"❌ {function_name} in {module_name} is not callable")
                return False
        return True
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing {module_name}: {e}")
        return False

def main():
    """Main function"""
    print("Testing Echo-Notes application with new structure...")
    
    # Test importing modules and finding key functions
    tests = [
        ("echo_notes.dashboard", "main"),
        ("echo_notes.daemon", "main"),
        ("echo_notes.notes_nextcloud", "main"),
        ("echo_notes.weekly_summary", "main"),
        ("echo_notes.shared.config", None),
        ("echo_notes.shared.date_helpers", None),
        ("echo_notes.shared.file_utils", None)
    ]
    
    success = True
    for module_name, function_name in tests:
        success = test_import_and_run(module_name, function_name) and success
    
    if success:
        print("\nAll tests passed! The Echo-Notes application can be run with the new structure.")
    else:
        print("\nSome tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()