# Echo Notes File Format Support

Echo Notes now supports multiple file formats for note processing:

## Supported Formats

- **Markdown (.md)**: The original format supported by Echo Notes.
- **Plain Text (.txt)**: Simple text files are now supported.
- **Microsoft Word (.docx)**: Word documents can now be processed.

## Requirements

To process .docx files, you need to install the `python-docx` package:

```bash
pip install python-docx
```

This dependency is automatically installed if you install Echo Notes using pip:

```bash
pip install -e .
```

## How It Works

Echo Notes uses a file converter system to handle different file formats:

1. When a file is detected in your notes directory, Echo Notes checks if its extension is supported.
2. If supported, it uses the appropriate converter to extract text from the file.
3. The extracted text is then processed by the LLM in the same way as markdown files.
4. The processed content is written back to the original file.

## Adding New File Formats

To add support for additional file formats:

1. Add a new converter function in `echo_notes/shared/file_converters.py`
2. Update the `get_converter_for_file` function to include the new format
3. Add any required dependencies to `setup.py` and `requirements.txt`

## Limitations

- When writing processed content back to files, the original formatting may be lost.
- For .docx files, tables and other complex formatting may not be preserved.
- Images and other non-text content in documents are not processed.

## Future Improvements

- Option to preserve original formatting
- Support for more file formats (PDF, RTF, etc.)
- Better handling of complex document structures