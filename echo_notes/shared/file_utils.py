from pathlib import Path
import logging
from .config import NOTES_DIR, SUMMARY_MARKER
from .file_converters import get_converter_for_file

logger = logging.getLogger(__name__)

def get_note_text(file_path: Path) -> str:
    """Read note content from various file formats"""
    converter = get_converter_for_file(file_path)
    if converter:
        try:
            return converter(file_path)
        except ImportError as e:
            logger.error(f"Failed to convert {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            raise
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

def is_processed_note(text: str) -> bool:
    """Check if note contains summary marker"""
    return SUMMARY_MARKER in text

def write_processed_note(file_path: Path, content: str):
    """Overwrite note with processed content"""
    # For now, we always write back as the same format
    # In the future, we could add options to convert between formats
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)