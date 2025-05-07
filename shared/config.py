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

# Scheduling Configuration
# Default intervals in minutes (can be overridden in config file)
DEFAULT_PROCESSING_INTERVAL = 60  # Process notes every 60 minutes (hourly)
DEFAULT_SUMMARY_INTERVAL = 10080  # Generate summary every 10080 minutes (weekly)
DEFAULT_SUMMARY_DAY = 6  # Sunday (0 = Monday, 6 = Sunday)
DEFAULT_SUMMARY_HOUR = 12  # 12:00 PM

# Path to the scheduling configuration file
SCHEDULE_CONFIG_PATH = Path(__file__).parent / 'schedule_config.json'

# Load scheduling configuration from file if it exists, otherwise use defaults
def load_schedule_config():
    if SCHEDULE_CONFIG_PATH.exists():
        try:
            import json
            with open(SCHEDULE_CONFIG_PATH, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading schedule config: {e}")
            return get_default_schedule_config()
    else:
        # Create default config file if it doesn't exist
        config = get_default_schedule_config()
        save_schedule_config(config)
        return config

def get_default_schedule_config():
    return {
        "processing_interval": DEFAULT_PROCESSING_INTERVAL,
        "summary_interval": DEFAULT_SUMMARY_INTERVAL,
        "summary_day": DEFAULT_SUMMARY_DAY,
        "summary_hour": DEFAULT_SUMMARY_HOUR,
        "daemon_enabled": True
    }

def save_schedule_config(config):
    import json
    with open(SCHEDULE_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

# Load schedule config
SCHEDULE_CONFIG = load_schedule_config()

# Derived Values
def weekly_summary_filename():
    return f"Weekly Summary - {datetime.now().strftime('%Y-%m-%d')}.md"