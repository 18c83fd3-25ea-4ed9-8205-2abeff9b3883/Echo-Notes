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
    QFrame, QSizePolicy, QFileDialog, QMessageBox, QDialog,
    QMenu
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
    format='%(asctime)s - %(name)s - %(message)s',  # Removed levelname from format
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
        # Use a custom formatter that only shows date and time (no seconds) and no log level
        self.setFormatter(logging.Formatter('%(asctime)s - %(message)s',
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

        # Status section with hamburger menu
        status_group = QGroupBox("Daemon Status")
        status_layout = QVBoxLayout(status_group)
        
        # Add hamburger menu button to status header
        status_header = QHBoxLayout()
        
        self.status_label = QLabel("Status: Checking...")
        self.status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        status_header.addWidget(self.status_label)
        
        # Add spacer to push hamburger button to the right
        status_header.addStretch()
        
        # Create hamburger menu button
        self.menu_button = QPushButton("≡")
        self.menu_button.setFixedSize(30, 30)
        self.menu_button.setFont(QFont("Arial", 14))
        self.menu_button.clicked.connect(self.show_menu)
        status_header.addWidget(self.menu_button)
        
        status_layout.addLayout(status_header)

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
                # Look for .md, .txt, and .docx files
                note_files = [f for f in notes_dir.iterdir()
                             if f.suffix in ['.md', '.txt', '.docx']
                             and not f.name.startswith('Weekly Summary')]
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
            # Use the correct path to the daemon.py script
            old_script_path = Path(__file__).parent / "echo_notes_daemon.py"
            script_path = Path(__file__).parent / "daemon.py"  # This is the correct path
            logger.debug(f"Old daemon path (doesn't exist): {old_script_path}")
            logger.debug(f"New daemon path (should exist): {script_path}")
            logger.debug(f"Current file location: {Path(__file__)}")
            logger.debug(f"Parent directory: {Path(__file__).parent}")
            logger.debug(f"Attempting to start daemon with command: {sys.executable} {script_path} --daemon")

            # Check if the script exists
            if not script_path.exists():
                logger.error(f"Daemon script not found at {script_path}")
                # Try to find the daemon script
                possible_paths = [
                    Path(__file__).parent.parent / "daemon.py",
                    Path.cwd() / "daemon.py",
                    Path.cwd() / "echo_notes" / "daemon.py",
                    Path(__file__).parent.parent / "echo_notes" / "daemon.py"
                ]
                for path in possible_paths:
                    logger.debug(f"Checking alternative path: {path}")
                    if path.exists():
                        logger.info(f"Found daemon script at {path}")
                        script_path = path
                        break
            
            # Use subprocess to run the daemon script
            logger.debug(f"Final daemon path: {script_path}")
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
            # Use the correct path to the daemon.py script
            old_script_path = Path(__file__).parent / "echo_notes_daemon.py"
            script_path = Path(__file__).parent / "daemon.py"  # This is the correct path
            logger.debug(f"Old daemon path (doesn't exist): {old_script_path}")
            logger.debug(f"New daemon path (should exist): {script_path}")
            logger.debug(f"Current file location: {Path(__file__)}")
            logger.debug(f"Parent directory: {Path(__file__).parent}")
            
            # Check if the script exists
            if not script_path.exists():
                logger.error(f"Daemon script not found at {script_path}")
                # Try to find the daemon script
                possible_paths = [
                    Path(__file__).parent.parent / "daemon.py",
                    Path.cwd() / "daemon.py",
                    Path.cwd() / "echo_notes" / "daemon.py",
                    Path(__file__).parent.parent / "echo_notes" / "daemon.py"
                ]
                for path in possible_paths:
                    logger.debug(f"Checking alternative path: {path}")
                    if path.exists():
                        logger.info(f"Found daemon script at {path}")
                        script_path = path
                        break
            
            logger.debug(f"Final daemon path: {script_path}")
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
                # Use models endpoint to check server availability instead of chat completions
                server_url = config.LM_URL.rsplit('/', 2)[0]  # Remove '/chat/completions'
                models_url = f"{server_url}/models"
                logger.debug(f"Checking LLM server availability at {models_url}")
                response = requests.get(models_url, timeout=1)
                logger.debug(f"LLM server response status: {response.status_code}")
                
                # LLM server is available, proceed with processing
                try:
                    from echo_notes.notes_nextcloud import main as process_notes_main
                    logger.debug("Successfully imported from echo_notes.notes_nextcloud")
                except ImportError:
                    try:
                        from ai_notes_nextcloud import main as process_notes_main
                        logger.debug("Successfully imported from ai_notes_nextcloud")
                    except ImportError:
                        from notes_nextcloud import main as process_notes_main
                        logger.debug("Successfully imported from notes_nextcloud")
                
                logger.debug(f"LLM server available, proceeding with note processing. Using NOTES_DIR: {config.NOTES_DIR}")
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
                # Use models endpoint to check server availability instead of chat completions
                server_url = config.LM_URL.rsplit('/', 2)[0]  # Remove '/chat/completions'
                models_url = f"{server_url}/models"
                logger.debug(f"Checking LLM server availability at {models_url}")
                response = requests.get(models_url, timeout=1)
                logger.debug(f"LLM server response status: {response.status_code}")
                
                # LLM server is available, proceed with summary generation
                try:
                    from echo_notes.weekly_summary import main as generate_summary_main
                    logger.debug("Successfully imported from echo_notes.weekly_summary")
                except ImportError:
                    try:
                        from ai_weekly_summary import main as generate_summary_main
                        logger.debug("Successfully imported from ai_weekly_summary")
                    except ImportError:
                        from weekly_summary import main as generate_summary_main
                        logger.debug("Successfully imported from weekly_summary")
                
                logger.debug(f"LLM server available, proceeding with summary generation. Using NOTES_DIR: {config.NOTES_DIR}")
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
                
                # If daemon is running, ask user if they want to restart it
                if self.daemon_running:
                    restart = QMessageBox.question(
                        self,
                        "Restart Daemon?",
                        "The notes directory has been updated. Do you want to restart the daemon to apply this change?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.Yes
                    )
                    
                    if restart == QMessageBox.StandardButton.Yes:
                        logger.info("Restarting daemon to apply new notes directory...")
                        self.stop_daemon()
                        # Wait a moment for the daemon to fully stop
                        QTimer.singleShot(2000, self.start_daemon)
                
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

    def show_menu(self):
        """Show the popup menu when hamburger button is clicked"""
        try:
            # Create popup menu
            menu = QMenu(self)
            
            # Add menu items
            config_action = menu.addAction('Config')
            model_action = menu.addAction('Model')
            about_action = menu.addAction('About')
            
            # Connect menu items to handlers
            config_action.triggered.connect(self.open_config_page)
            model_action.triggered.connect(self.open_model_page)
            about_action.triggered.connect(self.open_about_page)
            
            # Show menu at button position
            menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))
            
            logger.debug("Hamburger menu shown")
        except Exception as e:
            logger.error(f"Error showing hamburger menu: {e}")
            logger.error(traceback.format_exc())
    
    def open_config_page(self):
        """Open the configuration page"""
        try:
            logger.info("Opening configuration page")
            dialog = QDialog(self)
            dialog.setWindowTitle("Scheduling Configuration")
            dialog.setMinimumSize(500, 400)
            
            # Create layout
            layout = QVBoxLayout(dialog)
            
            # Import required widgets
            from PyQt6.QtWidgets import QSpinBox, QComboBox, QFormLayout, QCheckBox, QHBoxLayout
            
            # Create form layout for scheduling settings
            form_layout = QFormLayout()
            
            # Processing interval (in hours)
            processing_interval_combo = QComboBox()
            processing_intervals = [
                ("Hourly", 60),           # 60 minutes
                ("Every 6 hours", 360),   # 6 * 60 minutes
                ("Every 12 hours", 720),  # 12 * 60 minutes
                ("Daily", 1440)           # 24 * 60 minutes
            ]
            
            for label, minutes in processing_intervals:
                processing_interval_combo.addItem(label, minutes)
            
            # Set current value
            current_interval = config.SCHEDULE_CONFIG.get("processing_interval", config.DEFAULT_PROCESSING_INTERVAL)
            # Find closest match
            closest_index = 0
            min_diff = float('inf')
            for i, (_, minutes) in enumerate(processing_intervals):
                diff = abs(minutes - current_interval)
                if diff < min_diff:
                    min_diff = diff
                    closest_index = i
            
            processing_interval_combo.setCurrentIndex(closest_index)
            form_layout.addRow("Process Notes Interval:", processing_interval_combo)
            
            # Summary interval (in weeks)
            summary_interval_combo = QComboBox()
            summary_intervals = [
                ("Weekly", 10080),        # 7 * 24 * 60 minutes
                ("Bi-weekly", 20160),     # 14 * 24 * 60 minutes
                ("Every 4 weeks", 40320)  # 28 * 24 * 60 minutes
            ]
            
            for label, minutes in summary_intervals:
                summary_interval_combo.addItem(label, minutes)
            
            # Set current value
            current_summary = config.SCHEDULE_CONFIG.get("summary_interval", config.DEFAULT_SUMMARY_INTERVAL)
            # Find closest match
            closest_summary_index = 0
            min_summary_diff = float('inf')
            for i, (_, minutes) in enumerate(summary_intervals):
                diff = abs(minutes - current_summary)
                if diff < min_summary_diff:
                    min_summary_diff = diff
                    closest_summary_index = i
            
            summary_interval_combo.setCurrentIndex(closest_summary_index)
            form_layout.addRow("Summary Generation Interval:", summary_interval_combo)
            
            # Summary day
            summary_day_combo = QComboBox()
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for day in days:
                summary_day_combo.addItem(day)
            current_day = config.SCHEDULE_CONFIG.get("summary_day", config.DEFAULT_SUMMARY_DAY)
            summary_day_combo.setCurrentIndex(current_day)
            form_layout.addRow("Summary Day:", summary_day_combo)
            
            # Summary hour
            summary_hour_spin = QSpinBox()
            summary_hour_spin.setRange(0, 23)
            summary_hour_spin.setValue(config.SCHEDULE_CONFIG.get("summary_hour", config.DEFAULT_SUMMARY_HOUR))
            form_layout.addRow("Summary Hour:", summary_hour_spin)
            
            # Daemon enabled
            daemon_enabled_check = QCheckBox()
            daemon_enabled_check.setChecked(config.SCHEDULE_CONFIG.get("daemon_enabled", True))
            form_layout.addRow("Daemon Enabled:", daemon_enabled_check)
            
            # Add form layout to main layout
            layout.addLayout(form_layout)
            
            # Add buttons
            button_layout = QHBoxLayout()
            save_button = QPushButton("Save")
            close_button = QPushButton("Close")
            
            button_layout.addWidget(save_button)
            button_layout.addWidget(close_button)
            layout.addLayout(button_layout)
            
            # Connect buttons
            close_button.clicked.connect(dialog.close)
            
            # Save button handler
            def save_config():
                try:
                    # Save scheduling config
                    schedule_config = config.SCHEDULE_CONFIG.copy()
                    # Get the minutes value from the combo box's current item data
                    schedule_config["processing_interval"] = processing_interval_combo.currentData()
                    schedule_config["summary_interval"] = summary_interval_combo.currentData()
                    schedule_config["summary_day"] = summary_day_combo.currentIndex()
                    schedule_config["summary_hour"] = summary_hour_spin.value()
                    schedule_config["daemon_enabled"] = daemon_enabled_check.isChecked()
                    
                    # Save to file
                    config.save_schedule_config(schedule_config)
                    
                    # Update in-memory config
                    config.SCHEDULE_CONFIG = schedule_config
                    
                    # Show success message
                    from PyQt6.QtWidgets import QMessageBox
                    QMessageBox.information(dialog, "Success", "Scheduling configuration saved successfully!")
                    
                    # Close dialog
                    dialog.accept()
                    
                    # If daemon is running, ask if user wants to restart
                    if self.daemon_running:
                        restart = QMessageBox.question(
                            self,
                            "Restart Daemon?",
                            "Scheduling configuration has been updated. Do you want to restart the daemon to apply these changes?",
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                            QMessageBox.StandardButton.Yes
                        )
                        
                        if restart == QMessageBox.StandardButton.Yes:
                            logger.info("Restarting daemon to apply new configuration...")
                            self.stop_daemon()
                            # Wait a moment for the daemon to fully stop
                            QTimer.singleShot(2000, self.start_daemon)
                    
                except Exception as e:
                    logger.error(f"Error saving configuration: {e}")
                    logger.error(traceback.format_exc())
                    QMessageBox.warning(dialog, "Error", f"Failed to save configuration: {str(e)}")
            
            save_button.clicked.connect(save_config)
            
            dialog.exec()
        except Exception as e:
            logger.error(f"Error opening configuration page: {e}")
            logger.error(traceback.format_exc())
    
    def open_model_page(self):
        """Open the model page"""
        try:
            logger.info("Opening model page")
            dialog = QDialog(self)
            dialog.setWindowTitle("Model Configuration")
            dialog.setMinimumSize(500, 400)
            
            # Create layout
            layout = QVBoxLayout(dialog)
            
            # Import required widgets
            from PyQt6.QtWidgets import QLineEdit, QFormLayout, QTextEdit, QHBoxLayout, QMessageBox, QLabel, QComboBox
            
            # Create form layout for model settings
            form_layout = QFormLayout()
            
            # Model selection
            model_combo = QComboBox()
            # Add some common models
            models = ["qwen2.5-7b-instruct-1m", "llama3-8b-instruct", "mistral-7b-instruct", "gemma-7b-instruct"]
            for model in models:
                model_combo.addItem(model)
            
            # Set current model
            current_model_index = model_combo.findText(config.LLM_MODEL)
            if current_model_index >= 0:
                model_combo.setCurrentIndex(current_model_index)
            else:
                # If current model is not in the list, add it
                model_combo.addItem(config.LLM_MODEL)
                model_combo.setCurrentIndex(model_combo.count() - 1)
                
            form_layout.addRow("LLM Model:", model_combo)
            
            # LLM URL
            llm_url_input = QLineEdit(config.LM_URL)
            form_layout.addRow("LLM Server URL:", llm_url_input)
            
            # Load prompts from file
            import json
            try:
                with open(config.PROMPTS_CONFIG_PATH, 'r') as f:
                    prompts_config = json.load(f)
            except Exception as e:
                logger.error(f"Error loading prompts config: {e}")
                prompts_config = {}
            
            # Daily notes prompt
            form_layout.addRow("Daily Notes Prompt:", QLabel(""))  # Empty label as spacer
            daily_prompt_edit = QTextEdit()
            daily_prompt_edit.setPlainText(prompts_config.get("daily_notes_prompt", ""))
            daily_prompt_edit.setMinimumHeight(150)
            form_layout.addRow("", daily_prompt_edit)
            
            # Weekly summary prompt
            form_layout.addRow("Weekly Summary Prompt:", QLabel(""))  # Empty label as spacer
            weekly_prompt_edit = QTextEdit()
            weekly_prompt_edit.setPlainText(prompts_config.get("weekly_summary_prompt", ""))
            weekly_prompt_edit.setMinimumHeight(150)
            form_layout.addRow("", weekly_prompt_edit)
            
            # Add form layout to main layout
            layout.addLayout(form_layout)
            
            # Add buttons
            button_layout = QHBoxLayout()
            save_button = QPushButton("Save")
            close_button = QPushButton("Close")
            
            button_layout.addWidget(save_button)
            button_layout.addWidget(close_button)
            layout.addLayout(button_layout)
            
            # Connect buttons
            close_button.clicked.connect(dialog.close)
            
            # Save button handler
            def save_model_config():
                try:
                    # Update model settings in memory
                    config.LLM_MODEL = model_combo.currentText()
                    config.LM_URL = llm_url_input.text()
                    
                    # Save prompts config
                    prompts_config = {
                        "daily_notes_prompt": daily_prompt_edit.toPlainText(),
                        "weekly_summary_prompt": weekly_prompt_edit.toPlainText()
                    }
                    
                    with open(config.PROMPTS_CONFIG_PATH, 'w') as f:
                        json.dump(prompts_config, f, indent=2)
                    
                    # Show success message
                    QMessageBox.information(dialog, "Success", "Model configuration saved successfully!")
                    
                    # Close dialog
                    dialog.accept()
                    
                except Exception as e:
                    logger.error(f"Error saving model configuration: {e}")
                    logger.error(traceback.format_exc())
                    QMessageBox.warning(dialog, "Error", f"Failed to save model configuration: {str(e)}")
            
            save_button.clicked.connect(save_model_config)
            
            dialog.exec()
        except Exception as e:
            logger.error(f"Error opening model page: {e}")
            logger.error(traceback.format_exc())
    
    def open_about_page(self):
        """Open the about page"""
        try:
            logger.info("Opening about page")
            dialog = QDialog(self)
            dialog.setWindowTitle("About")
            dialog.setMinimumSize(500, 400)
            
            # Create layout
            layout = QVBoxLayout(dialog)
            layout.addWidget(QLabel("About Page"))
            
            # Add close button
            close_button = QPushButton("Close")
            close_button.clicked.connect(dialog.close)
            layout.addWidget(close_button)
            
            dialog.exec()
        except Exception as e:
            logger.error(f"Error opening about page: {e}")
            logger.error(traceback.format_exc())

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