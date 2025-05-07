from pathlib import Path
from echo_notes import file_utils, config  # Adjust if using package layout

def test_note_processing(tmp_path):
    note = tmp_path / "test.md"
    note.write_text("RAW NOTE CONTENT")

    assert file_utils.is_processed_note(note.read_text()) is False

    processed_text = f"PROCESSED CONTENT\n{config.SUMMARY_MARKER}"
    file_utils.write_processed_note(note, processed_text)

    assert file_utils.is_processed_note(note.read_text()) is True
