from pathlib import Path
from .config import NOTES_DIR, SUMMARY_MARKER

def get_note_text(file_path: Path) -> str:
    """Read markdown note content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def is_processed_note(text: str) -> bool:
    """Check if note contains summary marker"""
    return SUMMARY_MARKER in text

def write_processed_note(file_path: Path, content: str):
    """Overwrite note with processed content"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)