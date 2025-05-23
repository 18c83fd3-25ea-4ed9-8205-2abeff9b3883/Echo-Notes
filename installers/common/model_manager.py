#!/usr/bin/env python3
"""
Echo-Notes Model Manager
This module provides functionality for downloading and managing the Phi-2 model.
"""

import os
import sys
import urllib.request
import ssl
import time
from pathlib import Path

# Import from installer_utils.py
from .installer_utils import Colors, print_color

class ModelManager:
    """
    Manages downloading and installing the Phi-2 model.
    """

    def __init__(self, install_dir=None):
        """
        Initialize the model manager.

        Args:
            install_dir (Path, optional): Installation directory.
        """
        self.install_dir = Path(install_dir) if install_dir else None
        self.model_url = "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf"
        self.model_filename = "phi-2.Q4_K_M.gguf"
        
    def get_model_path(self):
        """
        Get the path where the model should be installed.
        
        Returns:
            Path: Path to the model file
        """
        if not self.install_dir:
            return None
            
        return self.install_dir / "echo_notes" / "models" / self.model_filename
        
    def check_model_exists(self):
        """
        Check if the model file already exists.
        
        Returns:
            bool: True if the model exists, False otherwise
        """
        model_path = self.get_model_path()
        if not model_path:
            return False
            
        return model_path.exists()
        
    def create_model_directory(self):
        """
        Create the models directory if it doesn't exist.
        
        Returns:
            bool: True if directory exists or was created, False otherwise
        """
        if not self.install_dir:
            return False
            
        model_dir = self.install_dir / "echo_notes" / "models"
        try:
            model_dir.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print_color(Colors.RED, f"Error creating model directory: {e}")
            return False
            
    def download_model(self, show_progress=True):
        """
        Download the Phi-2 model.
        
        Args:
            show_progress (bool): Whether to show download progress
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        if not self.create_model_directory():
            return False
            
        model_path = self.get_model_path()
        if not model_path:
            return False
            
        print_color(Colors.BLUE, f"Downloading Phi-2 model from {self.model_url}")
        print_color(Colors.YELLOW, f"This is a large file (~1.7GB) and may take some time to download")
        
        try:
            # Create a context that doesn't verify SSL certificates if needed
            context = ssl._create_unverified_context() if hasattr(ssl, "_create_unverified_context") else None
            
            if show_progress:
                self._download_with_progress(self.model_url, model_path, context)
            else:
                self._download_simple(self.model_url, model_path, context)
                
            print_color(Colors.GREEN, f"Model downloaded successfully to {model_path}")
            return True
            
        except Exception as e:
            print_color(Colors.RED, f"Error downloading model: {e}")
            # Remove partial download if it exists
            if model_path.exists():
                try:
                    model_path.unlink()
                except:
                    pass
            return False
            
    def _download_simple(self, url, output_path, context=None):
        """
        Download the model without progress reporting.
        
        Args:
            url (str): URL to download from
            output_path (Path): Path to save the model
            context (ssl.SSLContext, optional): SSL context
        """
        with urllib.request.urlopen(url, context=context) as response:
            with open(output_path, 'wb') as out_file:
                out_file.write(response.read())
                
    def _download_with_progress(self, url, output_path, context=None):
        """
        Download the model with progress reporting.
        
        Args:
            url (str): URL to download from
            output_path (Path): Path to save the model
            context (ssl.SSLContext, optional): SSL context
        """
        # Open the URL
        with urllib.request.urlopen(url, context=context) as response:
            # Get the total size if available
            total_size = int(response.headers.get("content-length", 0))
            
            # Initialize variables for progress tracking
            downloaded = 0
            chunk_size = 8192
            start_time = time.time()
            
            # Open the output file
            with open(output_path, 'wb') as out_file:
                # Download the data in chunks
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                        
                    # Update downloaded size and write chunk to file
                    downloaded += len(chunk)
                    out_file.write(chunk)
                    
                    # Calculate and display progress
                    if total_size > 0:
                        percent = int(downloaded * 100 / total_size)
                        elapsed = time.time() - start_time
                        speed = downloaded / elapsed / 1024 / 1024 if elapsed > 0 else 0  # MB/s
                        
                        # Calculate ETA
                        if speed > 0:
                            eta = (total_size - downloaded) / (speed * 1024 * 1024)
                            eta_str = f"ETA: {int(eta // 60)}m {int(eta % 60)}s"
                        else:
                            eta_str = "ETA: calculating..."
                        
                        # Clear line and print progress
                        sys.stdout.write("\r")
                        sys.stdout.write(
                            f"Progress: {percent}% ({downloaded/1024/1024:.1f}/{total_size/1024/1024:.1f} MB) {speed:.2f} MB/s {eta_str}"
                        )
                        sys.stdout.flush()
                        
            # Print newline after progress display
            if total_size > 0:
                sys.stdout.write("\n")
                
    def ensure_model_available(self, show_progress=True):
        """
        Ensure the model is available, downloading it if necessary.
        
        Args:
            show_progress (bool): Whether to show download progress
            
        Returns:
            bool: True if model is available, False otherwise
        """
        if self.check_model_exists():
            print_color(Colors.GREEN, f"Phi-2 model already exists at {self.get_model_path()}")
            return True
            
        print_color(Colors.YELLOW, "Phi-2 model not found, downloading...")
        return self.download_model(show_progress)


def ensure_model_available(install_dir, show_progress=True):
    """
    Convenience function to ensure the Phi-2 model is available.
    
    Args:
        install_dir (str or Path): Installation directory
        show_progress (bool): Whether to show download progress
        
    Returns:
        bool: True if model is available, False otherwise
    """
    manager = ModelManager(install_dir)
    return manager.ensure_model_available(show_progress)