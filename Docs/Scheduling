
# Scheduling Echo-Notes

Echo-Notes supports two main scheduling methods for note processing and summary generation:

---

## 1. Built-in Daemon (Recommended)

The built-in daemon handles background processing and scheduling automatically.

### Commands

```bash
# Start the daemon
echo-notes-daemon --daemon

# Stop the daemon
echo-notes-daemon --stop

# Configure the schedule
echo-notes-daemon --configure

# Launch the dashboard
echo-notes-dashboard

Logs & PID

Logs:

~/Documents/notes/daemon.log

~/Documents/notes/daemon.error.log


PID file:
~/Documents/notes/echo-notes.pid



---

2. Cron Jobs (Traditional)

For systems that prefer cron, use:

Hourly note processing

0 * * * * process-notes >> ~/Documents/notes/processing.log 2>&1

Weekly summary

0 12 * * 0 generate-summary >> ~/Documents/notes/weekly.log 2>&1

Ensure process-notes and generate-summary are in your $PATH or use full paths.


---

3. Running as a systemd Service (Optional)

Create a persistent background service on Linux.

Service File

[Unit]
Description=Echo-Notes Daemon
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
ExecStart=/usr/local/bin/echo-notes-daemon
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target

Setup Commands

sudo nano /etc/systemd/system/echo-notes.service
sudo systemctl enable echo-notes.service
sudo systemctl start echo-notes.service
sudo systemctl status echo-notes.service


---

Scheduling Settings

Configure via shared/schedule_config.json or use echo-notes-config.

Setting	Description	Default

processing_interval	Time between note runs (minutes)	60
summary_interval	Time between summaries (minutes)	10080
summary_day	Day of the week (0=Mon, 6=Sun)	6
summary_hour	Hour of day for weekly summary	12
daemon_enabled	Toggle the daemon on/off	true



---

Troubleshooting

Nothing runs? Check the daemon status or cron logs.

Wrong time? Check your system timezone settings.

Logs empty? Confirm correct paths in config or use full paths in cron jobs.



---

For launcher-related info, see launchers.md.

---

