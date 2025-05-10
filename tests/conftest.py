"""
Pytest configuration file for Echo-Notes tests.
This file helps with importing the package during tests.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing the package
sys.path.insert(0, str(Path(__file__).parent.parent))

# Print debugging information
print(f"Python version: {sys.version}")
print(f"sys.path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")
if os.path.exists('echo_notes'):
    print(f"echo_notes directory contents: {os.listdir('echo_notes')}")
else:
    print("echo_notes directory not found!")