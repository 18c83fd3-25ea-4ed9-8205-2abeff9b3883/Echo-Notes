#!/usr/bin/env python3

import os
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('check-daemon-status')

def check_daemon_status():
    """Check if the daemon is running"""
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
                logger.info(f"Daemon is running with PID: {pid}")
                return True
            except OSError:
                logger.warning(f"Daemon process with PID {pid} is not running (stale PID file)")
                return False
        except Exception as e:
            logger.error(f"Error checking daemon status: {e}")
            return False
    else:
        logger.info("Daemon is not running (no PID file found)")
        return False

def main():
    """Check daemon status repeatedly"""
    logger.info("Starting daemon status check")
    
    for i in range(5):
        logger.info(f"Check #{i+1}")
        is_running = check_daemon_status()
        logger.info(f"Daemon running: {is_running}")
        time.sleep(2)
    
    logger.info("Check complete")

if __name__ == "__main__":
    main()