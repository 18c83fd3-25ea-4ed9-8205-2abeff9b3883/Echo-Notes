#!/usr/bin/env python3

import os
import re
from pathlib import Path
from datetime import datetime, timedelta
import requests

# === CONFIGURATION ===
NOTES_DIR = Path.home() / 'Documents' / 'notes' / 'log'
WEEKLY_SUMMARY_NAME = f"Weekly Summary - {datetime.now().strftime('%Y-%m-%d')}.md"
LM_URL = 'http://localhost:8080/v1/chat/completions'
SUMMARY_MARKER = 'CLEANED & STRUCTURED NOTES'

# === UTILITIES ===

def get_note_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def extract_summary_timestamp(text):
    match = re.search(r"SUMMARY\s*\((\d{4}-\d{2}-\d{2} \d{2}:\d{2})\)", text)
    if match:
        try:
            return datetime.strptime(match.group(1), '%Y-%m-%d %H:%M')
        except ValueError:
            pass
    return None

def get_note_date(path):
    text = get_note_text(path)
    ts = extract_summary_timestamp(text)
    if ts: return ts
    return datetime.fromtimestamp(os.path.getmtime(path))

# === CORE FUNCTIONALITY ===

def generate_weekly_summary(summaries):
    now_date = datetime.now().strftime('%Y-%m-%d')
    
    # Fix: Move the newline joins outside the f-string
    combined_text = "\n\n".join(summaries)
    
    prompt = f"""
You are an AI assistant helping to generate a weekly summary. Below are notes from the past week:

{combined_text}

Your task:
1. Start with exactly: '# Weekly Summary - {now_date}'
2. Follow with these sections:
   - WEEKLY REFLECTION
   - MAIN THEMES
   - COMPLETED TASKS
   - PENDING ISSUES
   - NEXT WEEK'S PRIORITIES
3. Use Markdown format
4. Write in clear, professional tone
"""
    payload = {
        "model": "qwen2.5-7b-instruct-1m",
        "messages": [{"role": "system", "content": prompt}]
    }
    
    response = requests.post(LM_URL, json=payload, timeout=180)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def create_weekly_file(content):
    output_path = NOTES_DIR / WEEKLY_SUMMARY_NAME
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created weekly summary: {output_path}")

# === MAIN PROCESS ===

def run_weekly_summary():
    print(f"Generating weekly summary from notes in: {NOTES_DIR}")
    one_week_ago = datetime.now() - timedelta(days=7)
    collected = []

    for fname in os.listdir(NOTES_DIR):
        if fname.endswith('.md') and not fname.startswith('Weekly Summary'):
            file_path = NOTES_DIR / fname
            try:
                note_date = get_note_date(file_path)
                if note_date > one_week_ago:
                    text = get_note_text(file_path)
                    if SUMMARY_MARKER in text:
                        collected.append(text)
                        print(f"Included: {fname}")
            except Exception as e:
                print(f"Error processing {fname}: {e}")

    if not collected:
        print("No recent summaries found")
        return

    summary_content = generate_weekly_summary(collected)
    create_weekly_file(summary_content)

if __name__ == "__main__":
    run_weekly_summary()