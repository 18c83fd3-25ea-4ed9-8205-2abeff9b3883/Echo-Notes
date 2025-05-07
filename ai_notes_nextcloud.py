#!/usr/bin/env python3

from pathlib import Path
import os
from shared import (
    config,
    file_utils,
    date_helpers,
    llm_client
)

def process_note(file_path: Path):
    text = file_utils.get_note_text(file_path)
    if file_utils.is_processed_note(text):
        return
    
    # ... rest of processing logic ...
    processed = llm_client.query_llm(text, system_prompt)
    file_utils.write_processed_note(file_path, processed)

def main():
    for fname in os.listdir(config.NOTES_DIR):
        file_path = config.NOTES_DIR / fname
        if file_path.suffix == '.md':
            process_note(file_path)

if __name__ == "__main__":
    main()