#!/usr/bin/env python3

import os
import requests
from pathlib import Path
from datetime import datetime

# === CONFIGURATION ===
# Folder where Nextcloud syncs your notes
NOTES_DIR = Path.home() / 'Documents' / 'notes' / 'log'

# Your local LM Studio endpoint (adjust if needed)
LM_URL = 'http://localhost:8080/v1/chat/completions'

# Marker to detect already-processed notes
SUMMARY_MARKER = 'CLEANED & STRUCTURED NOTES'

# === UTILITIES ===

def get_note_text(filename):
    """Read the content of the Markdown note."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def replace_note_text(filename, new_text):
    """Replace the content of the note with processed output."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(new_text)

def extract_commands_and_body(raw_text):
    """
    Split note into optional 'AI COMMAND:' instructions and body content.
    """
    parts = raw_text.split('AI COMMAND:', 1)
    body = parts[0].strip()
    extra = parts[1].strip() if len(parts) > 1 else ''
    return extra, body

def make_system_prompt(extra_instructions: str):
    """
    Build the LLM system prompt for structured note cleanup.
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    base = (
        f"You are an AI assistant. I will give you raw voice-to-text notes.\n"
        f"Please:\n"
        f" 1. Fix grammar, spelling, and sentence structure.\n"
        f" 2. Organize into clear UPPERCASE sections (e.g., GOALS, IDEAS).\n"
        f" 3. Extract tasks as a checklist with '[ ] '.\n"
        f" 4. Suggest next steps as bullet points.\n"
        f"Then output in this format:\n\n"
        f"SUMMARY ({now})\n\n"
        f"CLEANED & STRUCTURED NOTES\n"
        f"...your sections here...\n\n"
        f"TASKS\n"
        f"[ ] Task 1\n"
        f"[ ] Task 2\n\n"
        f"SUGGESTIONS / NEXT STEPS\n"
        f"• Suggestion 1\n"
    )

    if extra_instructions:
        base += f"\nADDITIONAL INSTRUCTIONS:\n{extra_instructions}\n"

    return base

def summarize_note(raw_text):
    """
    Send the note to the local LLM for summarization.
    """
    extra, body = extract_commands_and_body(raw_text)
    system_prompt = make_system_prompt(extra)

    payload = {
        "model": "qwen2.5-7b-instruct-1m",  # Adjust to match your local model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": body}
        ]
    }

    response = requests.post(LM_URL, json=payload, timeout=120)
    response.raise_for_status()

    return response.json()['choices'][0]['message']['content']

# === MAIN ===

def process_local_notes():
    """Scan and process all unsummarized notes."""
    print(f"[INFO] Scanning notes folder: {NOTES_DIR}")

    for fname in os.listdir(NOTES_DIR):
        if fname.endswith('.md'):
            file_path = NOTES_DIR / fname
            print(f"[INFO] Checking: {file_path}")

            try:
                text = get_note_text(file_path)

                if SUMMARY_MARKER in text:
                    print(" → Skipped (already summarized).")
                    continue

                summary = summarize_note(text)
                replace_note_text(file_path, summary)
                print(f" ✔ Updated: {fname}")

            except Exception as e:
                print(f" ✖ Error processing {fname}: {e}")

# === ENTRY POINT ===

if __name__ == "__main__":
    process_local_notes()
