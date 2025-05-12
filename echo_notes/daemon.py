#!/usr/bin/env python3

import time
import datetime
import logging
import os
import sys
import signal
import argparse
import subprocess
import atexit
from pathlib import Path

from echo_notes.shared import config
from echo_notes.shared.config import SCHEDULE_CONFIG

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path.home() / 'Documents' / 'notes' / 'daemon.log')
    ]
)
logger = logging.getLogger('echo-notes-daemon')

# Global flag to control daemon execution
running = True

def signal_handler(sig, frame):
    """Handle termination signals gracefully"""
    global running
    logger.info("Received termination signal. Shutting down...")
    running = False

def setup_signal_handlers():
    """Set up signal handlers for graceful termination"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def should_process_notes(last_run):
    """Check if it's time to process notes based on the configured interval"""
    if last_run is None:
        return True
    
    interval_minutes = SCHEDULE_CONFIG.get('processing_interval', 60)
    elapsed = (datetime.datetime.now() - last_run).total_seconds() / 60
    return elapsed >= interval_minutes

def should_generate_summary(last_run):
    """Check if it's time to generate a weekly summary based on the configured interval and day/hour"""
    if last_run is None:
        # Check if it's the right day and hour for the first run
        now = datetime.datetime.now()
        target_day = SCHEDULE_CONFIG.get('summary_day', 6)  # Default: Sunday (6)
        target_hour = SCHEDULE_CONFIG.get('summary_hour', 12)  # Default: 12:00 PM
        
        # Convert to Python's day of week (0 = Monday, 6 = Sunday)
        current_day = now.weekday()
        if current_day == target_day and now.hour == target_hour:
            return True
        return False
    
    interval_minutes = SCHEDULE_CONFIG.get('summary_interval', 10080)  # Default: 1 week
    elapsed = (datetime.datetime.now() - last_run).total_seconds() / 60
    
    # If using weekly interval with specific day/hour
    if interval_minutes == 10080:  # If it's set to exactly one week
        now = datetime.datetime.now()
        target_day = SCHEDULE_CONFIG.get('summary_day', 6)  # Default: Sunday (6)
        target_hour = SCHEDULE_CONFIG.get('summary_hour', 12)  # Default: 12:00 PM
        
        # Convert to Python's day of week (0 = Monday, 6 = Sunday)
        current_day = now.weekday()
        
        # Check if it's the right day and hour and at least a week has passed
        if current_day == target_day and now.hour == target_hour and elapsed >= 10080:
            return True
        return False
    
    # For custom intervals not tied to specific day/hour
    return elapsed >= interval_minutes

def run_process_notes():
    """Run the note processing script"""
    logger.info("Running note processing...")
    try:
        from ai_notes_nextcloud import main as process_notes_main
        process_notes_main()
        logger.info("Note processing completed successfully")
        return datetime.datetime.now()
    except Exception as e:
        logger.error(f"Error processing notes: {e}")
        return None

def run_generate_summary():
    """Run the summary generation script"""
    logger.info("Running summary generation...")
    try:
        from ai_weekly_summary import main as generate_summary_main
        generate_summary_main()
        logger.info("Summary generation completed successfully")
        return datetime.datetime.now()
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return None

def daemon_loop():
    """Main daemon loop that checks and runs tasks at scheduled intervals"""
    last_process_run = None
    last_summary_run = None
    
    logger.info("Starting Echo-Notes daemon...")
    logger.info(f"Current schedule configuration: {SCHEDULE_CONFIG}")
    
    while running:
        # Reload config in case it was changed
        config.SCHEDULE_CONFIG = config.load_schedule_config()
        
        # Check if daemon is enabled
        if not config.SCHEDULE_CONFIG.get('daemon_enabled', True):
            logger.info("Daemon is disabled in configuration. Exiting...")
            break
        
        # Check if it's time to process notes
        if should_process_notes(last_process_run):
            last_process_run = run_process_notes()
        
        # Check if it's time to generate summary
        if should_generate_summary(last_summary_run):
            last_summary_run = run_generate_summary()
        
        # Sleep for a minute before checking again
        for _ in range(60):  # Check every second if we should stop
            if not running:
                break
            time.sleep(1)

def start_daemon():
    """Start the daemon process"""
    setup_signal_handlers()
    daemon_loop()

def daemonize():
    """Detach from the terminal and run as a daemon process"""
    # First fork
    try:
        pid = os.fork()
        if pid > 0:
            # Exit first parent
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork #1 failed: {e}")
        sys.exit(1)
    
    # Decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)
    
    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            # Exit from second parent
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork #2 failed: {e}")
        sys.exit(1)
    
    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    
    si = open(os.devnull, 'r')
    so = open(os.path.join(os.path.expanduser('~'), 'Documents', 'notes', 'daemon.log'), 'a+')
    se = open(os.path.join(os.path.expanduser('~'), 'Documents', 'notes', 'daemon.error.log'), 'a+')
    
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    
    # Write PID file
    pid_file = os.path.join(os.path.expanduser('~'), 'Documents', 'notes', 'echo-notes.pid')
    with open(pid_file, 'w+') as f:
        f.write(str(os.getpid()))
    
    # Register function to clean up PID file on exit
    atexit.register(lambda: os.remove(pid_file) if os.path.exists(pid_file) else None)
    
    logger.info(f"Daemon started with PID {os.getpid()}")

def main():
    """Main entry point with command line argument parsing"""
    parser = argparse.ArgumentParser(description='Echo-Notes Daemon')
    parser.add_argument('--configure', action='store_true', help='Configure scheduling settings')
    parser.add_argument('--daemon', action='store_true', help='Run as a daemon (detached from terminal)')
    parser.add_argument('--stop', action='store_true', help='Stop the running daemon')
    args = parser.parse_args()
    
    if args.configure:
        configure_scheduling()
    elif args.stop:
        stop_daemon()
    else:
        if args.daemon:
            daemonize()
        start_daemon()

def stop_daemon():
    """Stop the running daemon process"""
    pid_file = os.path.join(os.path.expanduser('~'), 'Documents', 'notes', 'echo-notes.pid')
    if not os.path.exists(pid_file):
        print("Daemon is not running (PID file not found)")
        return
    
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        # Send SIGTERM to the daemon process
        os.kill(pid, signal.SIGTERM)
        print(f"Sent termination signal to daemon process (PID: {pid})")
        
        # Wait for the process to terminate
        import time
        for _ in range(10):  # Wait up to 10 seconds
            try:
                os.kill(pid, 0)  # Check if process exists
                time.sleep(1)
            except OSError:
                # Process has terminated
                print("Daemon stopped successfully")
                return
        
        print("Daemon did not stop within timeout, may need to be killed manually")
    except Exception as e:
        print(f"Error stopping daemon: {e}")

def configure_scheduling():
    """Interactive configuration for scheduling settings"""
    print("\nEcho-Notes Scheduling Configuration")
    print("==================================\n")
    
    current_config = config.load_schedule_config()
    
    print(f"Current configuration:")
    print(f"  Process notes every {current_config.get('processing_interval')} minutes")
    print(f"  Generate summary every {current_config.get('summary_interval')} minutes")
    print(f"  Summary day: {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][current_config.get('summary_day', 6)]}")
    print(f"  Summary hour: {current_config.get('summary_hour')}:00")
    print(f"  Daemon enabled: {current_config.get('daemon_enabled', True)}\n")
    
    try:
        # Processing interval
        processing_interval = input(f"Enter processing interval in minutes [{current_config.get('processing_interval')}]: ")
        if processing_interval.strip():
            current_config['processing_interval'] = int(processing_interval)
        
        # Summary interval
        summary_interval = input(f"Enter summary interval in minutes [{current_config.get('summary_interval')}]: ")
        if summary_interval.strip():
            current_config['summary_interval'] = int(summary_interval)
        
        # Summary day
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_day = days[current_config.get('summary_day', 6)]
        day_input = input(f"Enter summary day [{current_day}]: ")
        if day_input.strip():
            try:
                day_index = days.index(day_input.capitalize())
                current_config['summary_day'] = day_index
            except ValueError:
                print(f"Invalid day. Using current value: {current_day}")
        
        # Summary hour
        hour_input = input(f"Enter summary hour (0-23) [{current_config.get('summary_hour')}]: ")
        if hour_input.strip():
            hour = int(hour_input)
            if 0 <= hour <= 23:
                current_config['summary_hour'] = hour
            else:
                print(f"Invalid hour. Using current value: {current_config.get('summary_hour')}")
        
        # Daemon enabled
        daemon_enabled = input(f"Enable daemon (yes/no) [{current_config.get('daemon_enabled', True)}]: ")
        if daemon_enabled.strip().lower() in ['yes', 'y', 'true', 't']:
            current_config['daemon_enabled'] = True
        elif daemon_enabled.strip().lower() in ['no', 'n', 'false', 'f']:
            current_config['daemon_enabled'] = False
        
        # Save configuration
        config.save_schedule_config(current_config)
        print("\nConfiguration saved successfully!")
        
    except Exception as e:
        print(f"Error during configuration: {e}")
        print("Configuration not saved.")

if __name__ == "__main__":
    main()