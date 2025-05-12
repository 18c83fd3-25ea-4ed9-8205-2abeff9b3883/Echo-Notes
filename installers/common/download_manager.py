#!/usr/bin/env python3
"""
Echo-Notes Download Manager
This module provides functionality for downloading the Echo-Notes repository.
"""

import os
import sys
import tempfile
import urllib.request
import zipfile
import io
import shutil
from pathlib import Path
import time
import ssl

# Import from installer_utils.py
from .installer_utils import Colors, print_color


class DownloadManager:
    """
    Manages downloading and extracting the Echo-Notes repository.
    """

    def __init__(self, repo_url=None, branch="main", install_dir=None):
        """
        Initialize the download manager.

        Args:
            repo_url (str or Path, optional): URL to the repository or installation directory.
                                             If Path, it's treated as install_dir.
            branch (str, optional): Branch to download. Defaults to "main".
            install_dir (Path, optional): Installation directory.
        """
        # Handle the case where repo_url is actually a Path object (for backward compatibility with tests)
        if isinstance(repo_url, Path):
            self.install_dir = repo_url
            self.repo_url = (
                "https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes"
            )
        else:
            self.repo_url = (
                repo_url
                or "https://github.com/18c83fd3-25ea-4ed9-8205-2abeff9b3883/Echo-Notes"
            )
            self.install_dir = install_dir

        self.branch = branch
        self.temp_dir = None
        self.extracted_dir = None

    def download(self, show_progress=True):
        """
        Download the Echo-Notes repository.

        Args:
            show_progress (bool): Whether to show download progress

        Returns:
            str: Path to the extracted directory, or None if download failed
        """
        print_color(Colors.BLUE, "Downloading Echo-Notes...")

        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()
        print(f"Using temporary directory: {self.temp_dir}")

        try:
            # Construct the download URL
            url = f"{self.repo_url}/archive/refs/heads/{self.branch}.zip"
            print_color(Colors.YELLOW, f"Downloading from: {url}")

            # Download with progress reporting if requested
            if show_progress:
                self._download_with_progress(url)
            else:
                self._download_simple(url)

            # Find the extracted directory
            extracted_dirs = [
                d
                for d in os.listdir(self.temp_dir)
                if os.path.isdir(os.path.join(self.temp_dir, d))
            ]

            if not extracted_dirs:
                print_color(Colors.RED, "Error: Could not find extracted directory.")
                return None

            self.extracted_dir = os.path.join(self.temp_dir, extracted_dirs[0])
            print_color(
                Colors.GREEN, f"Downloaded and extracted to: {self.extracted_dir}"
            )

            return self.extracted_dir

        except Exception as e:
            print_color(Colors.RED, f"Error downloading Echo-Notes: {e}")
            self.cleanup()
            return None

    def _download_simple(self, url):
        """
        Download and extract the repository without progress reporting.

        Args:
            url (str): URL to download from
        """
        # Create a context that doesn't verify SSL certificates if needed
        context = (
            ssl._create_unverified_context()
            if hasattr(ssl, "_create_unverified_context")
            else None
        )

        with urllib.request.urlopen(url, context=context) as response:
            zip_data = response.read()

        # Extract the ZIP file
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
            zip_ref.extractall(self.temp_dir)

    def _download_with_progress(self, url):
        """
        Download and extract the repository with progress reporting.

        Args:
            url (str): URL to download from
        """
        # Create a context that doesn't verify SSL certificates if needed
        context = (
            ssl._create_unverified_context()
            if hasattr(ssl, "_create_unverified_context")
            else None
        )

        # Open the URL
        with urllib.request.urlopen(url, context=context) as response:
            # Get the total size if available
            total_size = int(response.headers.get("content-length", 0))

            # Initialize variables for progress tracking
            downloaded = 0
            chunk_size = 8192
            start_time = time.time()

            # Create a BytesIO object to store the downloaded data
            data = io.BytesIO()

            # Download the data in chunks
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break

                # Update downloaded size and write chunk to BytesIO
                downloaded += len(chunk)
                data.write(chunk)

                # Calculate and display progress
                if total_size > 0:
                    percent = int(downloaded * 100 / total_size)
                    elapsed = time.time() - start_time
                    speed = downloaded / elapsed / 1024 if elapsed > 0 else 0

                    # Clear line and print progress
                    sys.stdout.write("\r")
                    sys.stdout.write(
                        f"Progress: {percent}% ({downloaded}/{total_size} bytes) {speed:.1f} KB/s"
                    )
                    sys.stdout.flush()

            # Print newline after progress display
            if total_size > 0:
                sys.stdout.write("\n")

            # Extract the ZIP file
            data.seek(0)
            with zipfile.ZipFile(data) as zip_ref:
                zip_ref.extractall(self.temp_dir)

    def copy_to_install_dir(self, install_dir):
        """
        Copy the downloaded files to the installation directory.

        Args:
            install_dir (str or Path): Installation directory

        Returns:
            bool: True if copy was successful, False otherwise
        """
        if not self.extracted_dir:
            print_color(Colors.RED, "Error: No downloaded files to copy.")
            return False

        install_dir = Path(install_dir)
        print_color(Colors.YELLOW, f"Copying files to: {install_dir}")

        try:
            # Create installation directory if it doesn't exist
            os.makedirs(install_dir, exist_ok=True)

            # Copy files to installation directory
            for item in os.listdir(self.extracted_dir):
                src = os.path.join(self.extracted_dir, item)
                dst = os.path.join(install_dir, item)

                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

            print_color(Colors.GREEN, "Files copied successfully")
            return True

        except Exception as e:
            print_color(Colors.RED, f"Error copying files: {e}")
            return False

    def cleanup(self):
        """
        Clean up temporary files.

        Returns:
            bool: True if cleanup was successful, False otherwise
        """
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                print_color(Colors.YELLOW, "Cleaning up temporary files...")
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                print_color(Colors.GREEN, "Temporary files cleaned up")
                return True
            except Exception as e:
                print_color(Colors.RED, f"Error cleaning up temporary files: {e}")
                return False
        return True


def download_echo_notes(install_dir=None, repo_url=None, branch="main", cleanup=True):
    """
    Convenience function to download and install Echo-Notes.

    Args:
        install_dir (str or Path, optional): Installation directory
        repo_url (str, optional): URL to the repository
        branch (str, optional): Branch to download
        cleanup (bool): Whether to clean up temporary files after installation

    Returns:
        Path or None: Path to the installation directory if successful, None otherwise
    """
    # Create download manager
    manager = DownloadManager(repo_url, branch)

    # Download repository
    extracted_dir = manager.download()
    if not extracted_dir:
        return None

    # If no install_dir provided, use the current directory
    if install_dir is None:
        install_dir = Path.cwd()
    else:
        install_dir = Path(install_dir)

    # Copy files to installation directory
    if not manager.copy_to_install_dir(install_dir):
        return None

    # Clean up temporary files if requested
    if cleanup:
        manager.cleanup()

    return install_dir
