# Development

## Development

## Testing Echo-Notes Installation

This document provides instructions for testing the Echo-Notes installation process.

## Testing Local Changes

Before pushing your changes to GitHub, you can test them locally using the `test_installation.sh` script:

```bash
./test_installation.sh
```

This script will:
1. Create a temporary directory
2. Copy your local Echo-Notes code to the temporary directory
3. Run the installer
4. Test the daemon and dashboard
5. Test the uninstaller
6. Clean up the temporary directory

If all tests pass, your changes are ready to be committed and pushed to GitHub.

## Testing the Package Structure

You can test the Python package structure using the `test_package.py` script:

```bash
python3 test_package.py
```

This script will attempt to import all the modules in the Echo-Notes package and report any issues.

## Testing the One-Click Installer

After pushing your changes to GitHub, you can test the one-click installer using the `test_one_click_installer.sh` script:

```bash
./test_one_click_installer.sh
```

This script will:
1. Create a temporary directory
2. Download the one-click installer from GitHub
3. Run the installer
4. Test the daemon and dashboard
5. Test the uninstaller
6. Clean up the temporary directory

If all tests pass, the one-click installer is working correctly.

## Manual Testing

You can also test the installation process manually:

1. Download the installer:
   ```bash
   curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/install_echo_notes.py
   chmod +x install_echo_notes.py
   ./install_echo_notes.py
   ```

2. Test the daemon:
   ```bash
   echo-notes-daemon --daemon
   ```

3. Test the dashboard:
   ```bash
   echo-notes-dashboard
   ```

4. Test the uninstaller:
   ```bash
   ./uninstall.sh
   ```

## Troubleshooting

If you encounter any issues during testing, check the following:

1. Make sure all files have the correct permissions
2. Check that the Python package structure is correct
3. Verify that the entry points in setup.py are correct
4. Ensure that the virtual environment is being created correctly

*Source: Echo-Notes/TESTING.md*

---

## In clean environment

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
from echo_notes.shared import file_utils, config

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

*Source: Echo-Notes/testing.md*

---

*Source: Docs/development.md*

---

## Testing Echo-Notes Installation

This document provides instructions for testing the Echo-Notes installation process.

## Testing Local Changes

Before pushing your changes to GitHub, you can test them locally using the `test_installation.sh` script:

```bash
./test_installation.sh
```

This script will:
1. Create a temporary directory
2. Copy your local Echo-Notes code to the temporary directory
3. Run the installer
4. Test the daemon and dashboard
5. Test the uninstaller
6. Clean up the temporary directory

If all tests pass, your changes are ready to be committed and pushed to GitHub.

## Testing the Package Structure

You can test the Python package structure using the `test_package.py` script:

```bash
python3 test_package.py
```

This script will attempt to import all the modules in the Echo-Notes package and report any issues.

## Testing the One-Click Installer

After pushing your changes to GitHub, you can test the one-click installer using the `test_one_click_installer.sh` script:

```bash
./test_one_click_installer.sh
```

This script will:
1. Create a temporary directory
2. Download the one-click installer from GitHub
3. Run the installer
4. Test the daemon and dashboard
5. Test the uninstaller
6. Clean up the temporary directory

If all tests pass, the one-click installer is working correctly.

## Manual Testing

You can also test the installation process manually:

1. Download the installer:
   ```bash
   curl -O https://raw.githubusercontent.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/main/install_echo_notes.py
   chmod +x install_echo_notes.py
   ./install_echo_notes.py
   ```

2. Test the daemon:
   ```bash
   echo-notes-daemon --daemon
   ```

3. Test the dashboard:
   ```bash
   echo-notes-dashboard
   ```

4. Test the uninstaller:
   ```bash
   ./uninstall.sh
   ```

## Troubleshooting

If you encounter any issues during testing, check the following:

1. Make sure all files have the correct permissions
2. Check that the Python package structure is correct
3. Verify that the entry points in setup.py are correct
4. Ensure that the virtual environment is being created correctly

*Source: Echo-Notes/TESTING.md*

---

## In clean environment

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
from echo_notes.shared import file_utils, config

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

*Source: Echo-Notes/testing.md*

---

## Echo-Notes Test Analysis Report

This report analyzes the test files in the Echo-Notes project and categorizes them as essential, development-only, or redundant.

## Essential Tests

These tests are essential for ensuring core functionality:

- `Echo-Notes/tests/conftest.py` (0 test functions)
- `Echo-Notes/tests/test_file_utils.py` (1 test functions)
- `analyze_tests.py` (8 test functions)
- `test_streamlined_project.py` (4 test functions)


## Development-Only Tests

These tests are only used during development and could be moved to a separate directory:

- `Echo-Notes/installers/test_framework.py`
- `Echo-Notes/installers/tests/__init__.py`
- `Echo-Notes/installers/tests/test_installers.py`
- `Echo-Notes/test_installation.sh`
- `Echo-Notes/test_one_click_installer.sh`
- `Echo-Notes/test_package.py`
- `Echo-Notes/test_reorganization.py`
- `Echo-Notes/test_uninstall.py`


## Redundant Tests

These tests are redundant and could be removed or consolidated:

- `Echo-Notes/tests/test_installation.sh`
- `Echo-Notes/tests/test_one_click_installer.sh`
- `Echo-Notes/tests/test_package.py`
- `Echo-Notes/tests/test_uninstall.py`


## Test Consolidation Plan

### 1. Move Essential Tests to tests/ Directory

- Move `Echo-Notes/tests/conftest.py` to `tests/conftest.py`
- Move `Echo-Notes/tests/test_file_utils.py` to `tests/test_file_utils.py`
- Move `analyze_tests.py` to `tests/analyze_tests.py`
- Move `test_streamlined_project.py` to `tests/test_streamlined_project.py`


### 2. Move Development-Only Tests to tools/dev_tests/ Directory

- Move `Echo-Notes/installers/test_framework.py` to `tools/dev_tests/test_framework.py`
- Move `Echo-Notes/installers/tests/__init__.py` to `tools/dev_tests/__init__.py`
- Move `Echo-Notes/installers/tests/test_installers.py` to `tools/dev_tests/test_installers.py`
- Move `Echo-Notes/test_installation.sh` to `tools/dev_tests/test_installation.sh`
- Move `Echo-Notes/test_one_click_installer.sh` to `tools/dev_tests/test_one_click_installer.sh`
- Move `Echo-Notes/test_package.py` to `tools/dev_tests/test_package.py`
- Move `Echo-Notes/test_reorganization.py` to `tools/dev_tests/test_reorganization.py`
- Move `Echo-Notes/test_uninstall.py` to `tools/dev_tests/test_uninstall.py`


### 3. Remove or Archive Redundant Tests

- Remove `Echo-Notes/tests/test_installation.sh`
- Remove `Echo-Notes/tests/test_one_click_installer.sh`
- Remove `Echo-Notes/tests/test_package.py`
- Remove `Echo-Notes/tests/test_uninstall.py`


## Summary

- Essential Tests: 4

- Development-Only Tests: 8

- Redundant Tests: 4

- Total Tests: 16

*Source: test_analysis.md*

---

