#!/usr/bin/env python3

from pathlib import Path
import os
import json
try:
    # Try the correct import path first
    from echo_notes.shared import (
        config,
        file_utils,
        date_helpers,
        llm_client
    )
    print("Successfully imported from echo_notes.shared")
except ImportError:
    # Fall back to the old import path
    from shared import (
        config,
        file_utils,
        date_helpers,
        llm_client
    )
    print("Falling back to import from shared")

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
    print(f"NOTES_NEXTCLOUD: Processing notes from directory: {config.NOTES_DIR}")
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('notes_nextcloud')
    logger.debug(f"Processing notes from directory: {config.NOTES_DIR}")
    
    for fname in os.listdir(config.NOTES_DIR):
        file_path = config.NOTES_DIR / fname
        logger.debug(f"Checking file: {file_path}")
        if file_path.suffix == '.md':
            process_note(file_path)

if __name__ == "__main__":
    main()