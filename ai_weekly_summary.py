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

def main():
    collected = []
    for fname in os.listdir(config.NOTES_DIR):
        file_path = config.NOTES_DIR / fname
        if file_path.suffix == '.md' and not fname.startswith('Weekly Summary'):
            if date_helpers.is_recent_note(file_path, days=7):
                text = file_utils.get_note_text(file_path)
                collected.append(text)
    
    prompts = load_prompts_from_config()
    summary = llm_client.query_llm("\n\n".join(collected), prompts['weekly_summary_prompt'])
    output_path = config.NOTES_DIR / config.weekly_summary_filename()
    file_utils.write_processed_note(output_path, summary)

if __name__ == "__main__":
    main()