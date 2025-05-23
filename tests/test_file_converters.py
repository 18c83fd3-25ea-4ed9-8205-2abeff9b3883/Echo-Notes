"""
Test file converters for different file formats.
"""

import os
import sys
import unittest
from pathlib import Path

# Add the parent directory to the path so we can import the echo_notes package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from echo_notes.shared import file_converters
except ImportError:
    from shared import file_converters

class TestFileConverters(unittest.TestCase):
    """Test file converters for different file formats."""
    
    def setUp(self):
        """Set up test files."""
        self.test_dir = Path(__file__).parent / 'test_files'
        self.test_dir.mkdir(exist_ok=True)
        
        # Create a test .txt file
        self.txt_file = self.test_dir / 'test.txt'
        with open(self.txt_file, 'w', encoding='utf-8') as f:
            f.write('This is a test text file.\nIt has multiple lines.\n')
        
        # Create a test .md file
        self.md_file = self.test_dir / 'test.md'
        with open(self.md_file, 'w', encoding='utf-8') as f:
            f.write('# Test Markdown\n\nThis is a test markdown file.\n')
        
        # We don't create a .docx file here because it's binary
        # and would require python-docx to create
        
    def tearDown(self):
        """Clean up test files."""
        if self.txt_file.exists():
            self.txt_file.unlink()
        if self.md_file.exists():
            self.md_file.unlink()
        if self.test_dir.exists():
            try:
                self.test_dir.rmdir()
            except OSError:
                # Directory not empty, that's fine
                pass
    
    def test_txt_to_text(self):
        """Test converting .txt file to text."""
        text = file_converters.txt_to_text(self.txt_file)
        self.assertEqual(text, 'This is a test text file.\nIt has multiple lines.\n')
    
    def test_md_to_text(self):
        """Test converting .md file to text."""
        # We use the txt_to_text converter for .md files
        text = file_converters.txt_to_text(self.md_file)
        self.assertEqual(text, '# Test Markdown\n\nThis is a test markdown file.\n')
    
    def test_get_converter_for_file(self):
        """Test getting the appropriate converter for a file."""
        txt_converter = file_converters.get_converter_for_file(self.txt_file)
        self.assertEqual(txt_converter, file_converters.txt_to_text)
        
        md_converter = file_converters.get_converter_for_file(self.md_file)
        self.assertEqual(md_converter, file_converters.txt_to_text)
        
        # Test with a .docx file (we don't need an actual file for this test)
        docx_file = Path('test.docx')
        docx_converter = file_converters.get_converter_for_file(docx_file)
        self.assertEqual(docx_converter, file_converters.docx_to_text)
        
        # Test with an unsupported file format
        unsupported_file = Path('test.xyz')
        unsupported_converter = file_converters.get_converter_for_file(unsupported_file)
        self.assertIsNone(unsupported_converter)

if __name__ == '__main__':
    unittest.main()