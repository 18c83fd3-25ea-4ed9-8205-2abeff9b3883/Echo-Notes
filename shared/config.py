from pathlib import Path
from datetime import datetime

# Core Configuration
NOTES_DIR = Path.home() / 'Documents' / 'notes' / 'log'
LM_URL = 'http://localhost:8080/v1/chat/completions'
SUMMARY_MARKER = 'CLEANED & STRUCTURED NOTES'
LLM_MODEL = "qwen2.5-7b-instruct-1m"

# Derived Values
def weekly_summary_filename():
    return f"Weekly Summary - {datetime.now().strftime('%Y-%m-%d')}.md"