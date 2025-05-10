
# Manual Installation Guide

Use this method if you prefer to install and run Echo-Notes manually, without using the one-click installer.

---

## 1. Clone the Repository

```bash
git clone https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes
cd Echo-Notes


---

2. Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


---

3. Install Dependencies

pip install -r requirements.txt

Or install the project as a package:

pip install -e .


---

4. Run Echo-Notes Tools

Start the daemon:

echo-notes-daemon --daemon

Launch the GUI dashboard:

echo-notes-dashboard

Run note processing manually:

process-notes

Generate a weekly summary:

generate-summary


---

5. Optional: Create Shortcuts

To create desktop shortcuts and launchers, see launchers.md.


---

6. Deactivation and Cleanup

To deactivate your environment:

deactivate

To remove it:

rm -rf venv/


---

For scheduling, see scheduling.md.
For uninstall steps, see uninstall.md.

---
