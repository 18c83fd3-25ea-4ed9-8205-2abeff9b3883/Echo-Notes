# Echo-Notes
### AI Notes with Nextcloud

**A privacy-first voice-to-text and note cleanup pipeline powered by local LLMs.**  
Capture voice notes on your phone, sync them via Nextcloud, and automatically clean or structure them using a local language model.

---

[![Lint Status](https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/actions/workflows/lint.yml/badge.svg)](https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built With Python](https://img.shields.io/badge/Built%20with-Python-blue)](https://www.python.org/)
[![Local-First](https://img.shields.io/badge/Privacy-Local%20Only-green)](#)

---

### Active Project Status: WIP (MVP Stable)

**Focus:**  
- Local-only automation  
- Modular architecture  
- Privacy-first LLM workflows  
- Auto weekly summaries

**Upcoming:**  
- Config file for customizable prompts  
- Optional journaling dashboard  
- Mood tracking integration

---

## Why This?

This project is designed for users who:
- Want a 100% local, private note-to-AI system
- Use Nextcloud for syncing and note-taking
- Prefer clean architecture with shared modules
- Need automated processing without cloud services
- Value easy installation via Python packaging

---

## ⚙How It Works

```text
[Integrated Voice-to-Text Input]
       ↓
[Nextcloud Notes Sync]
       ↓
[Modular Python Processing]
       ├── Daily Note Cleaning
       └── Weekly Summarization
       ↓
[Local LLM (LM Studio)]
       ↓
[Structured Markdown Outputs]
🗂 Project Structure
Echo-Notes/
├── shared/               # Core modules
│   ├── config.py        # Paths and settings
│   ├── file_utils.py    # File operations
│   └── llm_client.py    # AI integration
├── setup.py             # Installation config
├── requirements.txt     # Dependencies
└── ...                  # Other project files
🛠 Installation
bash
# Clone repository
git clone https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes
cd Echo-Notes

# Install with pip (recommended)
pip install -e .

# Alternative: Install requirements only
pip install -r requirements.txt
🔧 Cron Configuration
Hourly processing:

bash
0 * * * * process-notes >> ~/Documents/notes/processing.log 2>&1
Weekly summary:

bash
0 12 * * 0 generate-summary >> ~/Documents/notes/weekly.log 2>&1
Core Features
Daily Processing (process-notes)
Automatic note cleanup and structuring

Task extraction with checklists

Smart date parsing from content

Error-resilient processing

Weekly Summary (generate-summary)
Aggregates 7 days of notes

Identifies key themes and progress

Generates actionable next steps

Creates consolidated Markdown report

📜 Changelog
See CHANGELOG.md for full version history.

License
MIT - Use, modify, and share freely.

🙋 Support
Feel free to fork and adapt. PRs welcome for:

New analysis modes

Enhanced error handling

Additional storage backends

UI integrations