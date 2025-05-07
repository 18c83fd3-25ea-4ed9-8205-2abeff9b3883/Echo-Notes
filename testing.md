Here's a comprehensive testing plan for any updates to Echo-Notes:

### 1. Installation Testing
```bash
# In clean environment
git clone your-repo-url
cd Echo-Notes
python3 -m venv venv
source venv/bin/activate
pip install -e .  # Test package installation
which process-notes  # Should show path in venv
which generate-summary  # Verify entry points
```

### 2. Unit Testing (Add tests/ folder)
Create basic test structure:
```python
# tests/test_file_utils.py
from pathlib import Path
from shared import file_utils, config

def test_note_processing(tmp_path):
    test_note = tmp_path / "test.md"
    test_note.write_text("RAW NOTE CONTENT")
    
    # Test processing workflow
    assert file_utils.is_processed_note(test_note.read_text()) == False
    processed = "PROCESSED CONTENT\n" + config.SUMMARY_MARKER
    file_utils.write_processed_note(test_note, processed)
    assert file_utils.is_processed_note(test_note.read_text()) == True
```

### 3. Integration Testing
```bash
# Create test environment
mkdir -p ~/Documents/notes-test/log
export NOTES_DIR=~/Documents/notes-test/log

# Create test notes
for i in {1..3}; do
    echo "Test note $i $(date)" > ~/Documents/notes-test/log/test$i.md
done

# Test daily processing
process-notes --dry-run  # Should show processing of 3 notes
process-notes  # Actual run

# Verify outputs
grep -R "SUMMARY" ~/Documents/notes-test/log/*.md
```

### 4. Weekly Summary Test
```bash
# Force weekly summary with test data
generate-summary --test-mode  # Hypothetical flag
ls -l ~/Documents/notes-test/log/Weekly*.md

# Or manipulate dates
find ~/Documents/notes-test/log -name "*.md" -exec touch -d "2 days ago" {} \;
generate-summary
```

### 5. Error Scenario Testing
```bash
# Test with stopped LM Studio
pkill -f "lm-studio"
process-notes  # Should show error handling

# Test invalid notes
echo "INVALID CONTENT" > ~/Documents/notes-test/log/broken.md
process-notes  # Should skip or handle gracefully
```

### 6. Manual Verification Checklist
1. **Note Processing**:
```bash
# Create test note
echo "AI COMMAND: Make this urgent" > ~/Documents/notes-test/log/manual-test.md
process-notes
cat ~/Documents/notes-test/log/manual-test.md  # Verify structure
```

2. **Weekly Summary**:
```bash
generate-summary
cat ~/Documents/notes-test/log/Weekly*.md  # Check sections exist
```

3. **Edge Cases**:
```bash
# Empty note test
touch ~/Documents/notes-test/log/empty.md
process-notes  # Should skip or mark as error

# Large note test
dd if=/dev/urandom bs=1M count=10 | base64 > ~/Documents/notes-test/log/big.md
process-notes  # Test truncation handling
```

### 7. Cleanup
```bash
# After testing
rm -rf ~/Documents/notes-test
deactivate  # Leave venv
```

### Key Test Areas:
1. **File Operations**:
   - New notes get processed
   - Processed notes are skipped
   - Weekly summary creates new file

2. **Date Handling**:
   - Notes older than 7 days excluded
   - Embedded timestamps preferred
   - Fallback to file mtime

3. **LLM Integration**:
   - Proper prompt formatting
   - Error handling for offline LLM
   - Response parsing

4. **Packaging**:
   - CLI commands work after install
   - Shared modules accessible
   - Config paths resolve correctly

After testing:
```bash
# Check for leftover files
tree ~/Documents/notes-test  # Should be removed
```