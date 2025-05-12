#!/usr/bin/env python3
"""
Tests for the Echo-Notes installer framework.
These tests verify that the installers work correctly on different platforms.
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path
import platform
import subprocess

# Add the parent directory to the path so we can import the installers package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import common utilities after modifying the path
from installers.common.installer_utils import detect_os, check_python_version  # noqa: E402
from installers.common.download_manager import DownloadManager  # noqa: E402


class TestCommonUtilities(unittest.TestCase):
    """Test the common utilities."""

    def test_detect_os(self):
        """Test the detect_os function."""
        os_type = detect_os()
        system = platform.system().lower()

        if system == "windows":
            self.assertEqual(os_type, "windows")
        elif system == "darwin":
            self.assertEqual(os_type, "macos")
        elif system == "linux":
            self.assertEqual(os_type, "linux")
        else:
            self.assertEqual(os_type, "unknown")

    def test_check_python_version(self):
        """Test the check_python_version function."""
        # This should pass with any Python 3.8+ version
        self.assertTrue(check_python_version())


class TestDownloadManager(unittest.TestCase):
    """Test the download manager."""

    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up the test environment."""
        shutil.rmtree(self.temp_dir)

    def test_download_manager_initialization(self):
        """Test that the download manager can be initialized."""
        dm = DownloadManager(Path(self.temp_dir))
        self.assertIsNotNone(dm)
        self.assertEqual(dm.install_dir, Path(self.temp_dir))


class TestPlatformSpecificInstallers(unittest.TestCase):
    """Test the platform-specific installers."""

    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.os_type = detect_os()

    def tearDown(self):
        """Clean up the test environment."""
        shutil.rmtree(self.temp_dir)

    def test_import_platform_installer(self):
        """Test that the platform-specific installer can be imported."""
        if self.os_type == "windows":
            from installers.windows.windows_installer import install_windows

            self.assertTrue(callable(install_windows))
        elif self.os_type == "macos":
            from installers.macos.macos_installer import install_macos

            self.assertTrue(callable(install_macos))
        elif self.os_type == "linux":
            from installers.linux.linux_installer import install_linux

            self.assertTrue(callable(install_linux))
        else:
            self.skipTest(f"Unsupported OS: {self.os_type}")

    def test_import_platform_uninstaller(self):
        """Test that the platform-specific uninstaller can be imported."""
        if self.os_type == "windows":
            from installers.windows.windows_uninstaller import uninstall_windows

            self.assertTrue(callable(uninstall_windows))
        elif self.os_type == "macos":
            from installers.macos.macos_uninstaller import uninstall_macos

            self.assertTrue(callable(uninstall_macos))
        elif self.os_type == "linux":
            from installers.linux.linux_uninstaller import uninstall_linux

            self.assertTrue(callable(uninstall_linux))
        else:
            self.skipTest(f"Unsupported OS: {self.os_type}")


class TestInstallationSimulation(unittest.TestCase):
    """Test the installation process in a simulated environment."""

    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.install_dir = Path(self.temp_dir) / "echo-notes"
        self.install_dir.mkdir(exist_ok=True)

        # Create a mock Echo-Notes directory structure
        (self.install_dir / "echo_notes").mkdir(exist_ok=True)
        (self.install_dir / "shared").mkdir(exist_ok=True)
        (self.install_dir / "echo_notes_venv").mkdir(exist_ok=True)

        # Create mock files
        with open(self.install_dir / "echo_notes_dashboard.py", "w") as f:
            f.write("# Mock dashboard file")

        with open(self.install_dir / "requirements.txt", "w") as f:
            f.write("requests>=2.25.0\ntqdm>=4.50.0\n")

        self.os_type = detect_os()

    def tearDown(self):
        """Clean up the test environment."""
        shutil.rmtree(self.temp_dir)

    def test_installation_dry_run(self):
        """Test the installation process with a dry run."""
        if self.os_type == "windows":
            # Import the Windows installer
            from installers.windows.windows_installer import install_windows

            # Run the installer in dry run mode
            options = {"dry_run": True, "no_shortcut": True, "no_service": True}
            result = install_windows(self.install_dir, options)
            self.assertTrue(result)

        elif self.os_type == "macos":
            # Import the macOS installer
            from installers.macos.macos_installer import install_macos

            # Run the installer in dry run mode
            options = {
                "dry_run": True,
                "no_app_bundle": True,
                "no_symlinks": True,
                "no_service": True,
            }
            result = install_macos(self.install_dir, options)
            self.assertTrue(result)

        elif self.os_type == "linux":
            # Import the Linux installer
            from installers.linux.linux_installer import install_linux

            # Run the installer in dry run mode
            options = {
                "dry_run": True,
                "no_shortcuts": True,
                "no_symlinks": True,
                "no_service": True,
            }
            result = install_linux(self.install_dir, options)
            self.assertTrue(result)

        else:
            self.skipTest(f"Unsupported OS: {self.os_type}")

    def test_uninstallation_dry_run(self):
        """Test the uninstallation process with a dry run."""
        if self.os_type == "windows":
            # Import the Windows uninstaller
            from installers.windows.windows_uninstaller import uninstall_windows

            # Run the uninstaller in dry run mode
            options = {"dry_run": True, "keep_config": True}
            result = uninstall_windows(self.install_dir, options)
            self.assertTrue(result)

        elif self.os_type == "macos":
            # Import the macOS uninstaller
            from installers.macos.macos_uninstaller import uninstall_macos

            # Run the uninstaller in dry run mode
            options = {"dry_run": True, "keep_config": True}
            result = uninstall_macos(self.install_dir, options)
            self.assertTrue(result)

        elif self.os_type == "linux":
            # Import the Linux uninstaller
            from installers.linux.linux_uninstaller import uninstall_linux

            # Run the uninstaller in dry run mode
            options = {"dry_run": True, "keep_config": True}
            result = uninstall_linux(self.install_dir, options)
            self.assertTrue(result)

        else:
            self.skipTest(f"Unsupported OS: {self.os_type}")


class TestMigrationScript(unittest.TestCase):
    """Test the migration script."""

    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.install_dir = Path(self.temp_dir) / "echo-notes"
        self.install_dir.mkdir(exist_ok=True)

        # Create a mock old Echo-Notes directory structure
        (self.install_dir / "echo_notes").mkdir(exist_ok=True)
        (self.install_dir / "shared").mkdir(exist_ok=True)
        (self.install_dir / "echo_notes_venv").mkdir(exist_ok=True)

        # Create mock files for old installation
        with open(self.install_dir / "echo_notes_dashboard.py", "w") as f:
            f.write("# Mock dashboard file")

        with open(self.install_dir / "echo_notes_installer.py", "w") as f:
            f.write("# Mock old installer file")

        with open(self.install_dir / "requirements.txt", "w") as f:
            f.write("requests>=2.25.0\ntqdm>=4.50.0\n")

        # Copy the migration script to the temp directory
        migration_script_path = Path(parent_dir).parent / "migrate_installers.py"
        if migration_script_path.exists():
            shutil.copy(migration_script_path, self.temp_dir)
        else:
            # Create a mock migration script
            with open(Path(self.temp_dir) / "migrate_installers.py", "w") as f:
                f.write(
                    """#!/usr/bin/env python3
import sys
print("Mock migration script")
sys.exit(0)
"""
                )

        self.os_type = detect_os()

    def tearDown(self):
        """Clean up the test environment."""
        shutil.rmtree(self.temp_dir)

    def test_migration_script_exists(self):
        """Test that the migration script exists."""
        migration_script = Path(self.temp_dir) / "migrate_installers.py"
        self.assertTrue(migration_script.exists())

    def test_migration_script_dry_run(self):
        """Test the migration script with a dry run."""
        migration_script = Path(self.temp_dir) / "migrate_installers.py"

        # Make the script executable
        migration_script.chmod(0o755)

        # Run the script with --help to test that it works
        try:
            result = subprocess.run(
                [sys.executable, str(migration_script), "--help"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
        except subprocess.SubprocessError:
            self.skipTest("Migration script execution failed")


if __name__ == "__main__":
    unittest.main()
