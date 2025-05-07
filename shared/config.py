import os
from pathlib import Path
from datetime import datetime

# Core Configuration
# Default paths that can be overridden by environment variables
DEFAULT_NOTES_DIR = Path.home() / 'Documents' / 'notes' / 'log'
DEFAULT_APP_DIR = Path(__file__).parent.parent  # Echo-Notes directory

# Use environment variables if set, otherwise use defaults
NOTES_DIR = Path(os.environ.get('ECHO_NOTES_DIR', DEFAULT_NOTES_DIR))
APP_DIR = Path(os.environ.get('ECHO_APP_DIR', DEFAULT_APP_DIR))

# Other configuration
LM_URL = 'http://localhost:8080/v1/chat/completions'
SUMMARY_MARKER = 'CLEANED & STRUCTURED NOTES'
LLM_MODEL = "qwen2.5-7b-instruct-1m"

# Path to the prompts configuration file
# This uses the APP_DIR to locate prompts_config.json
PROMPTS_CONFIG_PATH = Path(__file__).parent / 'prompts_config.json'

# Derived Values
def weekly_summary_filename():
    return f"Weekly Summary - {datetime.now().strftime('%Y-%m-%d')}.md"