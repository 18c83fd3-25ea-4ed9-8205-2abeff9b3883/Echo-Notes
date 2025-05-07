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
- Voice-to-text journaling  
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
- Prefer owning their data and workflows end-to-end
- Need voice-to-text logs cleaned up and structured automatically
- Want automated weekly reflections without cloud services

---

## ⚙How It Works

```text
[Integrated Keyboard Voice-to-Text Microphone]
       ↓
[Nextcloud Notes App]
       ↓
[Synced to Desktop via Nextcloud Client]
       ↓
[Python script parses any note with "log" category]
       ↓
[Sends raw note text to local LLM in LM Studio]
       ↓
[LLM returns cleaned + structured result → overwrites note]
       ↓
[Weekly script aggregates summaries → generates reflection]
```

---

## 🗂 Folder Setup

Assumes:
* Your notes are synced to: `~/Documents/notes/log/`
* You run LM Studio locally on your desktop
* LM Studio has developer mode enabled and LLM loaded
* Scheduled scripts via `cron`

---

## 🔁 Cron Job Examples

**Hourly processing** (add to crontab with `crontab -e`):
```bash
0 * * * * /usr/bin/python3 /home/user/Documents/notes/ai_notes_nextcloud.py >> /home/user/Documents/notes/processing.log 2>&1
```

**Weekly summary** (every Sunday at noon):
```bash
0 12 * * 0 /usr/bin/python3 /home/user/Documents/notes/ai_weekly_summary.py >> /home/user/Documents/notes/weekly.log 2>&1
```

---

## Script Behavior

**Main Script (`ai_notes_nextcloud.py`)**:
* Processes `.md` files in `~/Documents/notes/log/`
* Skips already summarized notes
* Parses special `AI COMMAND:` instructions
* Generates structured output with:
  - Uppercase sections
  - Timestamp
  - Task checklist
  - Bullet point suggestions

**Weekly Summary Script (`weekly-summary-nextcloud.py`)**:
* Runs every Sunday
* Collects all summaries from past 7 days
* Generates consolidated report with:
  - Weekly reflection
  - Main themes
  - Completed tasks
  - Pending issues
  - Next week's priorities
* Creates new `Weekly Summary - YYYY-MM-DD.md` file

---

## Prompt Design (Structured Mode)

```text
You are an AI assistant. I will give you raw voice-to-text notes.
Please:
 1. Fix grammar, spelling, and sentence structure.
 2. Organize into clear UPPERCASE sections (e.g., GOALS, IDEAS).
 3. Extract tasks as a checklist with '[ ] '.
 4. Suggest next steps as bullet points.

Then output in this format:

SUMMARY (timestamp)

CLEANED & STRUCTURED NOTES
...your sections here...

TASKS
[ ] Task 1
[ ] Task 2

SUGGESTIONS / NEXT STEPS
• Suggestion 1
```

---

## Requirements

* Python 3.7+
* `requests` library
* LM Studio running locally with compatible LLM (e.g. Qwen2.5)
* Nextcloud client for file syncing

Install dependencies:
```bash
pip install requests
```

---

## Files

* `ai_notes_nextcloud.py` - Main processing script
* `ai_weekly_summary.py` - Weekly aggregation script
* `processing.log` - Hourly script output (optional)
* `weekly.log` - Summary generation logs (optional)

---

## Example Use

1. Record voice note in Nextcloud Notes app
2. Add `log` category/tag
3. Wait for sync + hourly processing
4. Note is rewritten into structured format
5. Weekly summary auto-generated every Sunday noon

---

## License

MIT - Use, modify, and share freely.

---

## 🙋 Support

Feel free to fork and adapt. PRs welcome for:
- Prompt improvements
- New analysis modes
- Nextcloud integration enhancements
- Visualization features
```
