from pathlib import Path
import sys
import os

# Try different import approaches
try:
    # First try the new package structure
    from echo_notes.shared import file_utils, config
    print("Successfully imported from echo_notes.shared")
except ImportError:
    try:
        # Then try the old structure
        from shared import file_utils, config
        print("Successfully imported from shared")
    except ImportError:
        # If all else fails, try to add the parent directory to sys.path
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        try:
            from echo_notes.shared import file_utils, config
            print("Successfully imported from echo_notes.shared after path adjustment")
        except ImportError:
            from shared import file_utils, config
            print("Successfully imported from shared after path adjustment")

def test_note_processing(tmp_path):
    note = tmp_path / "test.md"
    note.write_text("RAW NOTE CONTENT")

    assert file_utils.is_processed_note(note.read_text()) is False

    processed_text = f"PROCESSED CONTENT\n{config.SUMMARY_MARKER}"
    file_utils.write_processed_note(note, processed_text)

    assert file_utils.is_processed_note(note.read_text()) is True
