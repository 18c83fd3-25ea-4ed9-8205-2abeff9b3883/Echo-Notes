#!/usr/bin/env python3
"""
Echo Notes Dashboard - A minimal GUI for controlling the Echo-Notes daemon
"""

import sys
import os
import time
import datetime
import signal
import subprocess
import logging
import traceback
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QGroupBox, QSplitter,
    QFrame, QSizePolicy, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot, QSize, pyqtSignal, QObject, QMetaObject, Q_ARG, QThread
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette

# Import Echo-Notes modules
# Import Echo-Notes modules
from echo_notes.shared import config
from echo_notes.shared.config import SCHEDULE_CONFIG

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path.home() / 'Documents' / 'notes' / 'dashboard.log')
    ]
)
logger = logging.getLogger('echo-notes-dashboard')

class WorkerSignals(QObject):
    """Defines the signals available from a running worker thread."""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    update_note_timestamp = pyqtSignal(datetime.datetime)
    update_summary_timestamp = pyqtSignal(datetime.datetime)

class Worker(QThread):
    """Worker thread for background tasks"""
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        """Run the function in the thread"""
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            logger.error(f"Error in worker thread: {e}")
            logger.error(traceback.format_exc())
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()

class LogHandler(logging.Handler):
    """Custom log handler to redirect logs to the GUI"""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget  # Store the text widget
        # Use a custom formatter that only shows date and time (no seconds)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', 
                                           datefmt='%Y-%m-%d %H:%M'))

    def emit(self, record):
        msg = self.format(record)
        # Use invokeMethod to ensure thread safety
        QMetaObject.invokeMethod(self.text_widget, 
                                "append", 
                                Qt.ConnectionType.QueuedConnection,
                                Q_ARG(str, msg))
        # Auto-scroll is handled in the slot

class EchoNotesDashboard(QMainWindow):
    """Main dashboard window for Echo-Notes"""
    def __init__(self):
        super().__init__()

        self.daemon_running = False
        self.last_note_time = None
        self.last_summary_time = None
        self.worker_threads = []  # Keep track of worker threads

        self.init_ui()
        self.setup_log_handler()
        self.setup_signals()

        # Start the update timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)  # Update every second

        # Initial status update
        self.update_status()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Echo Notes')
        self.setMinimumSize(600, 400)
        
        # Set application icon
        icon_path = Path(__file__).parent / "Echo-Notes-Icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
            logger.debug(f"Set application icon from {icon_path}")
        else:
            logger.warning(f"Icon file not found at {icon_path}")

        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Status section
        status_group = QGroupBox("Daemon Status")
        status_layout = QVBoxLayout(status_group)

        self.status_label = QLabel("Status: Checking...")
        self.status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        status_layout.addWidget(self.status_label)

        # Timestamps section
        timestamps_layout = QHBoxLayout()

        self.last_note_label = QLabel("Last Note: Never")
        self.last_summary_label = QLabel("Last Summary: Never")

        timestamps_layout.addWidget(self.last_note_label)
        timestamps_layout.addWidget(self.last_summary_label)
        status_layout.addLayout(timestamps_layout)

        # Notes directory section
        notes_dir_layout = QHBoxLayout()
        self.notes_dir_label = QLabel(f"Notes Directory: {config.NOTES_DIR}")
        self.notes_dir_label.setWordWrap(True)
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_notes_directory)
        notes_dir_layout.addWidget(self.notes_dir_label, 3)
        notes_dir_layout.addWidget(self.browse_btn, 1)
        status_layout.addLayout(notes_dir_layout)

        main_layout.addWidget(status_group)

        # Control buttons section
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)

        self.toggle_daemon_btn = QPushButton("Start Daemon")
        self.toggle_daemon_btn.clicked.connect(self.toggle_daemon)

        self.process_notes_btn = QPushButton("Process Notes Now")
        self.process_notes_btn.clicked.connect(self.process_notes)

        self.generate_summary_btn = QPushButton("Generate Summary Now")
        self.generate_summary_btn.clicked.connect(self.generate_summary)

        controls_layout.addWidget(self.toggle_daemon_btn)
        controls_layout.addWidget(self.process_notes_btn)
        controls_layout.addWidget(self.generate_summary_btn)

        main_layout.addWidget(controls_group)

        # Log display section
        logs_group = QGroupBox("Logs")
        logs_layout = QVBoxLayout(logs_group)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        # Connect textChanged to auto-scroll
        self.log_display.textChanged.connect(self.auto_scroll_logs)

        logs_layout.addWidget(self.log_display)

        main_layout.addWidget(logs_group)

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Set size proportions
        main_layout.setStretch(0, 1)  # Status section
        main_layout.setStretch(1, 1)  # Controls section
        main_layout.setStretch(2, 4)  # Logs section

    def setup_log_handler(self):
        """Set up custom log handler to display logs in the GUI"""
        self.log_handler = LogHandler(self.log_display)
        logger.addHandler(self.log_handler)

        # Also capture root logger to see all Echo-Notes logs
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)

    def setup_signals(self):
        """Set up signal connections for thread-safe UI updates"""
        # These will be connected when workers are created

    def auto_scroll_logs(self):
        """Auto-scroll log display to the bottom"""
        try:
            scrollbar = self.log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        except Exception as e:
            logger.error(f"Error auto-scrolling logs: {e}")

    def update_status(self):
        """Update the daemon status and timestamps"""
        try:
            # Check if daemon is running
            pid_file = Path.home() / 'Documents' / 'notes' / 'echo-notes.pid'
            logger.debug(f"Checking daemon status, PID file: {pid_file}")

            if pid_file.exists():
                try:
                    with open(pid_file, 'r') as f:
                        pid = int(f.read().strip())
                    logger.debug(f"Found PID file with PID: {pid}")

                    # Check if process is actually running
                    try:
                        os.kill(pid, 0)  # This will raise an exception if process doesn't exist
                        self.daemon_running = True
                        self.status_label.setText("Status: Running")
                        self.status_label.setStyleSheet("color: green")
                        self.toggle_daemon_btn.setText("Stop Daemon")
                        logger.debug(f"Daemon process with PID {pid} is running")
                    except OSError:
                        self.daemon_running = False
                        self.status_label.setText("Status: Not Running (Stale PID)")
                        self.status_label.setStyleSheet("color: red")
                        self.toggle_daemon_btn.setText("Start Daemon")
                        # Clean up stale PID file
                        pid_file.unlink(missing_ok=True)
                        logger.debug(f"Daemon process with PID {pid} is not running (stale PID file)")
                except Exception as e:
                    logger.error(f"Error checking daemon status: {e}")
                    logger.error(traceback.format_exc())
                    self.daemon_running = False
                    self.status_label.setText("Status: Error")
                    self.status_label.setStyleSheet("color: orange")
                    self.toggle_daemon_btn.setText("Start Daemon")
            else:
                self.daemon_running = False
                self.status_label.setText("Status: Not Running")
                self.status_label.setStyleSheet("color: red")
                self.toggle_daemon_btn.setText("Start Daemon")
                logger.debug("No PID file found, daemon is not running")

            # Check for last processed note and summary
            self.check_last_processed_times()
        except Exception as e:
            logger.error(f"Unexpected error in update_status: {e}")
            logger.error(traceback.format_exc())

    def check_last_processed_times(self):
        """Check for the last processed note and summary times"""
        try:
            # Check for most recent note file
            notes_dir = config.NOTES_DIR
            logger.debug(f"Checking for notes in directory: {notes_dir}")
            if notes_dir.exists():
                note_files = [f for f in notes_dir.iterdir() if f.suffix == '.md' and not f.name.startswith('Weekly Summary')]
                if note_files:
                    latest_note = max(note_files, key=os.path.getmtime)
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(latest_note))
                    self.last_note_time = mtime
                    self.last_note_label.setText(f"Last Note: {mtime.strftime('%Y-%m-%d %H:%M')}")
                    logger.debug(f"Found latest note: {latest_note.name} from {mtime}")

                # Check for most recent summary file
                summary_files = [f for f in notes_dir.iterdir() if f.suffix == '.md' and f.name.startswith('Weekly Summary')]
                if summary_files:
                    latest_summary = max(summary_files, key=os.path.getmtime)
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(latest_summary))
                    self.last_summary_time = mtime
                    self.last_summary_label.setText(f"Last Summary: {mtime.strftime('%Y-%m-%d %H:%M')}")
                    logger.debug(f"Found latest summary: {latest_summary.name} from {mtime}")
        except Exception as e:
            logger.error(f"Error checking processed times: {e}")
            logger.error(traceback.format_exc())

    @pyqtSlot()
    def toggle_daemon(self):
        """Start or stop the daemon process"""
        try:
            if self.daemon_running:
                self.stop_daemon()
            else:
                self.start_daemon()
        except Exception as e:
            logger.error(f"Error in toggle_daemon: {e}")
            logger.error(traceback.format_exc())

    def start_daemon(self):
        """Start the daemon process"""
        try:
            logger.info("Starting Echo-Notes daemon...")
            
            # Define script_path first to avoid reference before assignment
            script_path = Path(__file__).parent / "echo_notes_daemon.py"
            logger.debug(f"Attempting to start daemon with command: {sys.executable} {script_path} --daemon")

            # Use subprocess to run the daemon script
            subprocess.Popen([sys.executable, str(script_path), "--daemon"])
            logger.debug("subprocess.Popen called for daemon start")

            logger.info("Daemon start command issued")

            # Update will happen on next timer tick
        except Exception as e:
            logger.error(f"Error starting daemon: {e}")
            logger.error(traceback.format_exc())

    def stop_daemon(self):
        """Stop the daemon process"""
        try:
            logger.info("Stopping Echo-Notes daemon...")
            logger.debug("Attempting to stop daemon")

            # Use subprocess to run the daemon script with stop flag
            script_path = Path(__file__).parent / "echo_notes_daemon.py"
            result = subprocess.run([sys.executable, str(script_path), "--stop"], capture_output=True, text=True)
            logger.debug(f"Stop daemon command result: {result.returncode}")
            logger.debug(f"Stop daemon stdout: {result.stdout}")
            logger.debug(f"Stop daemon stderr: {result.stderr}")

            logger.info("Daemon stop command issued")

            # Update will happen on next timer tick
        except Exception as e:
            logger.error(f"Error stopping daemon: {e}")
            logger.error(traceback.format_exc())

    @pyqtSlot()
    def process_notes(self):
        """Manually trigger note processing"""
        try:
            logger.info("Manually triggering note processing...")
            
            # Create worker thread for note processing
            worker = Worker(self._run_process_notes)
            worker.signals.update_note_timestamp.connect(self.update_note_timestamp)
            worker.signals.error.connect(lambda error: logger.error(f"Note processing error: {error}"))
            worker.signals.finished.connect(lambda: logger.debug("Note processing thread finished"))
            
            # Start the worker thread
            self.worker_threads.append(worker)  # Keep reference to prevent garbage collection
            worker.start()
            
            logger.debug(f"Started note processing thread")
        except Exception as e:
            logger.error(f"Error triggering note processing: {e}")
            logger.error(traceback.format_exc())

    def _run_process_notes(self):
        """Run note processing in a separate thread"""
        try:
            # Check if LLM server is available before processing
            import requests
            try:
                logger.debug(f"Checking LLM server availability at {config.LM_URL}")
                response = requests.get(config.LM_URL, timeout=1)
                logger.debug(f"LLM server response status: {response.status_code}")
                
                # LLM server is available, proceed with processing
                from ai_notes_nextcloud import main as process_notes_main
                logger.debug("LLM server available, proceeding with note processing")
                process_notes_main()
                logger.info("Note processing completed successfully")

                # Emit signal to update timestamp safely
                worker = QThread.currentThread()
                if hasattr(worker, 'signals'):
                    worker.signals.update_note_timestamp.emit(datetime.datetime.now())
                else:
                    logger.error("Worker thread does not have signals attribute")

            except requests.exceptions.ConnectionError as ce:
                logger.warning(f"LLM server not available at {config.LM_URL}. Note processing skipped.")
                logger.debug(f"Connection error details: {ce}")
            except requests.exceptions.Timeout as te:
                logger.warning(f"LLM server timeout at {config.LM_URL}. Note processing skipped.")
                logger.debug(f"Timeout error details: {te}")
            except requests.exceptions.RequestException as re:
                logger.warning(f"Request error with LLM server at {config.LM_URL}. Note processing skipped.")
                logger.debug(f"Request error details: {re}")
        except Exception as e:
            logger.error(f"Error in note processing: {e}")
            logger.error(traceback.format_exc())

    @pyqtSlot(datetime.datetime)
    def update_note_timestamp(self, timestamp):
        """Update the note timestamp in a thread-safe way"""
        try:
            self.last_note_time = timestamp
            self.last_note_label.setText(f"Last Note: {timestamp.strftime('%Y-%m-%d %H:%M')}")
            logger.debug(f"Updated note timestamp to {timestamp}")
        except Exception as e:
            logger.error(f"Error updating note timestamp: {e}")
            logger.error(traceback.format_exc())

    @pyqtSlot()
    def generate_summary(self):
        """Manually trigger summary generation"""
        try:
            logger.info("Manually triggering summary generation...")
            
            # Create worker thread for summary generation
            worker = Worker(self._run_generate_summary)
            worker.signals.update_summary_timestamp.connect(self.update_summary_timestamp)
            worker.signals.error.connect(lambda error: logger.error(f"Summary generation error: {error}"))
            worker.signals.finished.connect(lambda: logger.debug("Summary generation thread finished"))
            
            # Start the worker thread
            self.worker_threads.append(worker)  # Keep reference to prevent garbage collection
            worker.start()
            
            logger.debug(f"Started summary generation thread")
        except Exception as e:
            logger.error(f"Error triggering summary generation: {e}")
            logger.error(traceback.format_exc())

    def _run_generate_summary(self):
        """Run summary generation in a separate thread"""
        try:
            # Check if LLM server is available before processing
            import requests
            try:
                logger.debug(f"Checking LLM server availability at {config.LM_URL}")
                response = requests.get(config.LM_URL, timeout=1)
                logger.debug(f"LLM server response status: {response.status_code}")
                
                # LLM server is available, proceed with summary generation
                from ai_weekly_summary import main as generate_summary_main
                logger.debug("LLM server available, proceeding with summary generation")
                generate_summary_main()
                logger.info("Summary generation completed successfully")

                # Emit signal to update timestamp safely
                worker = QThread.currentThread()
                if hasattr(worker, 'signals'):
                    worker.signals.update_summary_timestamp.emit(datetime.datetime.now())
                else:
                    logger.error("Worker thread does not have signals attribute")

            except requests.exceptions.ConnectionError as ce:
                logger.warning(f"LLM server not available at {config.LM_URL}. Summary generation skipped.")
                logger.debug(f"Connection error details: {ce}")
            except requests.exceptions.Timeout as te:
                logger.warning(f"LLM server timeout at {config.LM_URL}. Summary generation skipped.")
                logger.debug(f"Timeout error details: {te}")
            except requests.exceptions.RequestException as re:
                logger.warning(f"Request error with LLM server at {config.LM_URL}. Summary generation skipped.")
                logger.debug(f"Request error details: {re}")
        except Exception as e:
            logger.error(f"Error in summary generation: {e}")
            logger.error(traceback.format_exc())

    @pyqtSlot(datetime.datetime)
    def update_summary_timestamp(self, timestamp):
        """Update the summary timestamp in a thread-safe way"""
        try:
            self.last_summary_time = timestamp
            self.last_summary_label.setText(f"Last Summary: {timestamp.strftime('%Y-%m-%d %H:%M')}")
            logger.debug(f"Updated summary timestamp to {timestamp}")
        except Exception as e:
            logger.error(f"Error updating summary timestamp: {e}")
            logger.error(traceback.format_exc())

    @pyqtSlot()
    def browse_notes_directory(self):
        """Open a folder selection dialog to choose notes directory"""
        try:
            logger.info("Opening folder selection dialog for notes directory")
            
            # Get the current notes directory as the starting point
            current_dir = str(config.NOTES_DIR)
            
            # Open folder selection dialog
            new_dir = QFileDialog.getExistingDirectory(
                self,
                "Select Notes Directory",
                current_dir,
                QFileDialog.Option.ShowDirsOnly
            )
            
            # If user selected a directory (didn't cancel)
            if new_dir:
                new_dir_path = Path(new_dir)
                logger.info(f"User selected new notes directory: {new_dir_path}")
                
                # Update the configuration in memory
                os.environ['ECHO_NOTES_DIR'] = str(new_dir_path)
                config.NOTES_DIR = new_dir_path
                
                # Update the UI
                self.notes_dir_label.setText(f"Notes Directory: {new_dir_path}")
                
                # Create the directory if it doesn't exist
                if not new_dir_path.exists():
                    new_dir_path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created new notes directory: {new_dir_path}")
                
                # Save the configuration to file for persistence
                config.SCHEDULE_CONFIG["notes_directory"] = str(new_dir_path)
                config.save_schedule_config(config.SCHEDULE_CONFIG)
                logger.info(f"Saved notes directory to configuration file: {new_dir_path}")
                
                # Show confirmation message
                QMessageBox.information(
                    self,
                    "Notes Directory Updated",
                    f"Notes directory has been updated to:\n{new_dir_path}\n\nNew notes will be saved to this location."
                )
                
                # Update status to check for notes in the new directory
                self.check_last_processed_times()
        except Exception as e:
            logger.error(f"Error selecting notes directory: {e}")
            logger.error(traceback.format_exc())
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to update notes directory: {str(e)}"
            )

    def closeEvent(self, event):
        """Handle window close event"""
        try:
            logger.info("Closing Echo-Notes Dashboard")
            # Clean up worker threads
            for worker in self.worker_threads:
                if worker.isRunning():
                    worker.quit()
                    worker.wait(1000)  # Wait up to 1 second for thread to finish
            event.accept()
        except Exception as e:
            logger.error(f"Error during application shutdown: {e}")
            logger.error(traceback.format_exc())
            event.accept()  # Accept the close event anyway

def main():
    """Main entry point for the dashboard application"""
    try:
        logger.info("Starting Echo-Notes Dashboard")
        app = QApplication(sys.argv)

        # Set application style
        app.setStyle("Fusion")
        
        # Set application icon
        icon_path = Path(__file__).parent / "Echo-Notes-Icon.png"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
            logger.debug(f"Set application icon from {icon_path}")
        else:
            logger.warning(f"Icon file not found at {icon_path}")

        # Create and show the dashboard
        dashboard = EchoNotesDashboard()
        dashboard.show()

        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()