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
- CLI-first tooling

**Upcoming:**  
- Config file for customizable prompts  
- Optional journaling dashboard  
- Auto-backups to encrypted store

---



## Why This?

This project is designed for users who:
- Want a 100% local, private note-to-AI system
- Use Nextcloud for syncing and note-taking
- Prefer owning their data and workflows end-to-end
- Need voice-to-text logs cleaned up and structured automatically
- Want to focus on the ideas and not the note taking process.

No cloud APIs, no surveillance. Just your own device, your notes, and your LLM.

---

## ⚙How It Works

```text
[Intergrated Keyboard Voice-to-Text Microphone]
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
````

---

## 🗂 Folder Setup

Assumes:

* Your notes are synced to: `~/Documents/notes/log/`
* You run LM Studio locally on your desktop
* LM Studio has developer mode enabled and LLM loaded
* You schedule the script with `cron` to run hourly

---

## 🔁 Cron Job Example

To run every hour, add to crontab with `crontab -e`:

```
0 * * * * /usr/bin/python3 /home/user/Documents/notes/ai_notes_nextcloud.py >> /home/user/Documents/notes/ai_notes_nextcloud.log 2>&1
```

---

## Script Behavior

The script:

* Looks for `.md` files in `~/Documents/notes/log/`
* Skips files already summarized (based on a marker in the text)
* Parses special `AI COMMAND:` lines if included in a note
* Sends the content to your **LM Studio LLM** via REST API
* Overwrites the note with structured output, including:

  * Uppercase sections
  * Timestamp
  * Task checklist
  * Bullet point suggestions

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
* LM Studio running locally with a compatible LLM (e.g. Qwen2.5)
* Nextcloud client for file syncing

Install dependencies:

```bash
pip install requests
```

---

## Files

* `ai_notes_nextcloud.py` — main script
* `ai_notes_nextcloud.log` — cron output (optional)

---

## Example Use

1. Record a voice note in Nextcloud Notes app on your phone
2. Add the tag or category `log`
3. Wait for the sync + cron job to run
4. Note is rewritten into structured format by your local AI

---

## 📜 License

MIT — Use, modify, and share freely.

---

## 🙋 Support

Feel free to fork and adapt. PRs welcome for prompt improvements, new modes, or Nextcloud enhancements.


