#!/usr/bin/env python3

from pathlib import Path
import os
import json
from shared import (
    config,
    file_utils,
    date_helpers,
    llm_client
)

def load_prompts_from_config():
    with open(config.PROMPTS_CONFIG_PATH, 'r') as f:
        prompts = json.load(f)
    return prompts

def process_note(file_path: Path):
    text = file_utils.get_note_text(file_path)
    if file_utils.is_processed_note(text):
        return
    
    # ... rest of processing logic ...
    prompts = load_prompts_from_config()
    processed = llm_client.query_llm(text, prompts['daily_notes_prompt'])
    file_utils.write_processed_note(file_path, processed)

def main():
    for fname in os.listdir(config.NOTES_DIR):
        file_path = config.NOTES_DIR / fname
        if file_path.suffix == '.md':
            process_note(file_path)

if __name__ == "__main__":
    main()