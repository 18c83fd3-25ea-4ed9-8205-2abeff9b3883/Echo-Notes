#!/bin/bash

# Use absolute path to the virtual environment
source "/home/j/Documents/CodeProjects/Echo-Notes/Echo-Notes/echo_notes_venv/bin/activate"

# Set any environment variables that might be needed
export PYTHONPATH="/home/j/Documents/CodeProjects/Echo-Notes:$PYTHONPATH"

# Run the dashboard
echo-notes-dashboard

# Deactivate the virtual environment when done
deactivate