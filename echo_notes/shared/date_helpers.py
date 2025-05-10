from datetime import datetime, timedelta
import re
from pathlib import Path
import os
from shared import file_utils

def extract_summary_timestamp(text: str) -> datetime:
    """Extract embedded timestamp from note content"""
    match = re.search(r"SUMMARY\s*\((\d{4}-\d{2}-\d{2} \d{2}:\d{2})\)", text)
    if match:
        try:
            return datetime.strptime(match.group(1), '%Y-%m-%d %H:%M')
        except ValueError:
            pass
    return None

def get_note_date(file_path: Path) -> datetime:
    """Get note date from content or filesystem"""
    text = file_utils.get_note_text(file_path)
    ts = extract_summary_timestamp(text)
    return ts or datetime.fromtimestamp(os.path.getmtime(file_path))

def is_recent_note(file_path: Path, days=7) -> bool:
    """Check if note is within date threshold"""
    note_date = get_note_date(file_path)
    return note_date > (datetime.now() - timedelta(days=days))