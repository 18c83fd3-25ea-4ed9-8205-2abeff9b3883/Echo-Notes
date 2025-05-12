#!/usr/bin/env python3
"""
Echo-Notes Windows Installer Entry Point
This script is the main entry point for the Windows installer.
It will be compiled to an executable (.exe) file.
"""

import os
import sys
import argparse
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

# Add the parent directory to the path so we can import the installers package
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)

# Import the Windows installer and uninstaller
from installers.windows.windows_installer import install_windows  # noqa: E402
from installers.windows.windows_uninstaller import uninstall_windows  # noqa: E402
from installers.common.download_manager import download_echo_notes  # noqa: E402
from installers.common.installer_utils import Colors, print_color, detect_os  # noqa: E402


class RedirectText:
    """
    Redirect stdout to a tkinter Text widget.
    """

    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""

    def write(self, string):
        self.buffer += string
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass


class InstallerGUI:
    """
    GUI for the Echo-Notes Windows installer.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Echo-Notes Installer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Set icon if available
        try:
            icon_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "Echo-Notes-Icon.png"
            )
            if os.path.exists(icon_path):
                self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
        except Exception:
            pass

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            header_frame, text="Echo-Notes Installer", font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT)

        # Create tabs
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True)

        # Install tab
        self.install_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.install_tab, text="Install")
        self.setup_install_tab()

        # Uninstall tab
        self.uninstall_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.uninstall_tab, text="Uninstall")
        self.setup_uninstall_tab()

        # About tab
        self.about_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.about_tab, text="About")
        self.setup_about_tab()

        # Create footer
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(footer_frame, text="Echo-Notes © 2025", font=("Arial", 8)).pack(
            side=tk.RIGHT
        )

        # Initialize variables
        self.install_dir = tk.StringVar(value=str(Path.home() / "Echo-Notes"))
        self.create_shortcut = tk.BooleanVar(value=True)
        self.start_service = tk.BooleanVar(value=True)
        self.purge_data = tk.BooleanVar(value=False)

        # Set up console redirection
        self.original_stdout = sys.stdout

    def setup_install_tab(self):
        """Set up the install tab."""
        # Create frames
        options_frame = ttk.LabelFrame(
            self.install_tab, text="Installation Options", padding="10"
        )
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        # Installation directory
        dir_frame = ttk.Frame(options_frame)
        dir_frame.pack(fill=tk.X, pady=5)

        ttk.Label(dir_frame, text="Installation Directory:").pack(side=tk.LEFT)
        ttk.Entry(dir_frame, textvariable=self.install_dir, width=40).pack(
            side=tk.LEFT, padx=5, fill=tk.X, expand=True
        )
        ttk.Button(dir_frame, text="Browse...", command=self.browse_install_dir).pack(
            side=tk.LEFT
        )

        # Checkboxes
        ttk.Checkbutton(
            options_frame, text="Create desktop shortcut", variable=self.create_shortcut
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            options_frame,
            text="Start Echo-Notes daemon service",
            variable=self.start_service,
        ).pack(anchor=tk.W, pady=2)

        # Console output
        console_frame = ttk.LabelFrame(
            self.install_tab, text="Installation Progress", padding="10"
        )
        console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.install_console = tk.Text(
            console_frame, wrap=tk.WORD, state="disabled", height=10
        )
        self.install_console.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            self.install_console, command=self.install_console.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.install_console.config(yscrollcommand=scrollbar.set)

        # Buttons
        button_frame = ttk.Frame(self.install_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.install_button = ttk.Button(
            button_frame, text="Install", command=self.start_installation
        )
        self.install_button.pack(side=tk.RIGHT)

    def setup_uninstall_tab(self):
        """Set up the uninstall tab."""
        # Create frames
        options_frame = ttk.LabelFrame(
            self.uninstall_tab, text="Uninstallation Options", padding="10"
        )
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        # Checkboxes
        ttk.Checkbutton(
            options_frame,
            text="Remove all data including notes (USE WITH CAUTION)",
            variable=self.purge_data,
        ).pack(anchor=tk.W, pady=2)

        # Console output
        console_frame = ttk.LabelFrame(
            self.uninstall_tab, text="Uninstallation Progress", padding="10"
        )
        console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.uninstall_console = tk.Text(
            console_frame, wrap=tk.WORD, state="disabled", height=10
        )
        self.uninstall_console.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            self.uninstall_console, command=self.uninstall_console.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.uninstall_console.config(yscrollcommand=scrollbar.set)

        # Buttons
        button_frame = ttk.Frame(self.uninstall_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.uninstall_button = ttk.Button(
            button_frame, text="Uninstall", command=self.start_uninstallation
        )
        self.uninstall_button.pack(side=tk.RIGHT)

    def setup_about_tab(self):
        """Set up the about tab."""
        about_frame = ttk.Frame(self.about_tab, padding="20")
        about_frame.pack(fill=tk.BOTH, expand=True)

        # Logo or icon
        try:
            icon_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "Echo-Notes-Icon.png"
            )
            if os.path.exists(icon_path):
                logo = tk.PhotoImage(file=icon_path)
                logo_label = ttk.Label(about_frame, image=logo)
                logo_label.image = logo  # Keep a reference
                logo_label.pack(pady=(0, 20))
        except Exception:
            pass

        # App name and version
        ttk.Label(about_frame, text="Echo-Notes", font=("Arial", 16, "bold")).pack()

        ttk.Label(about_frame, text="Version 1.0", font=("Arial", 10)).pack()

        # Description
        ttk.Label(
            about_frame,
            text="\nEcho-Notes is a note-taking and summarization tool\n"
            "that helps you organize and process your daily notes.",
            justify=tk.CENTER,
            wraplength=400,
        ).pack(pady=10)

        # Copyright
        ttk.Label(
            about_frame,
            text="© 2025 Echo-Notes Team\nAll rights reserved.",
            justify=tk.CENTER,
        ).pack(pady=10)

        # Website link
        website_frame = ttk.Frame(about_frame)
        website_frame.pack(pady=5)

        ttk.Label(website_frame, text="Website:").pack(side=tk.LEFT)
        website_link = ttk.Label(
            website_frame,
            text="https://echo-notes.example.com",
            foreground="blue",
            cursor="hand2",
        )
        website_link.pack(side=tk.LEFT, padx=5)
        website_link.bind(
            "<Button-1>", lambda e: self.open_url("https://echo-notes.example.com")
        )

    def browse_install_dir(self):
        """Open a directory browser dialog."""
        directory = filedialog.askdirectory(initialdir=self.install_dir.get())
        if directory:
            self.install_dir.set(directory)

    def open_url(self, url):
        """Open a URL in the default browser."""
        try:
            import webbrowser

            webbrowser.open(url)
        except Exception:
            pass

    def start_installation(self):
        """Start the installation process in a separate thread."""
        # Disable the install button
        self.install_button.configure(state="disabled")

        # Clear the console
        self.install_console.configure(state="normal")
        self.install_console.delete(1.0, tk.END)
        self.install_console.configure(state="disabled")

        # Redirect stdout to the console
        sys.stdout = RedirectText(self.install_console)

        # Start installation in a separate thread
        threading.Thread(target=self.perform_installation, daemon=True).start()

    def perform_installation(self):
        """Perform the actual installation."""
        try:
            # Get installation options
            install_dir = Path(self.install_dir.get())
            options = {
                "no_shortcut": not self.create_shortcut.get(),
                "no_service": not self.start_service.get(),
            }

            # Check if we need to download Echo-Notes
            if not (install_dir / "echo_notes" / "dashboard.py").exists():
                print_color(Colors.BLUE, "Downloading Echo-Notes...")
                download_dir = download_echo_notes(install_dir)
                if not download_dir:
                    print_color(Colors.RED, "Error: Failed to download Echo-Notes.")
                    messagebox.showerror(
                        "Installation Error", "Failed to download Echo-Notes."
                    )
                    self.install_button.configure(state="normal")
                    sys.stdout = self.original_stdout
                    return

            # Perform installation
            success = install_windows(install_dir, options)

            # Show result
            if success:
                print_color(Colors.GREEN, "Installation completed successfully!")
                messagebox.showinfo(
                    "Installation Complete",
                    "Echo-Notes has been installed successfully!\n\n"
                    "You can now launch Echo-Notes using the desktop shortcut.",
                )
            else:
                print_color(Colors.RED, "Installation failed.")
                messagebox.showerror(
                    "Installation Error",
                    "Failed to install Echo-Notes.\n\n"
                    "Please check the installation log for details.",
                )
        except Exception as e:
            print_color(Colors.RED, f"Error during installation: {e}")
            messagebox.showerror(
                "Installation Error", f"An unexpected error occurred:\n{e}"
            )
        finally:
            # Re-enable the install button
            self.install_button.configure(state="normal")

            # Restore stdout
            sys.stdout = self.original_stdout

    def start_uninstallation(self):
        """Start the uninstallation process in a separate thread."""
        # Confirm uninstallation
        if not messagebox.askyesno(
            "Confirm Uninstallation",
            "Are you sure you want to uninstall Echo-Notes?\n\n"
            "This will remove the application and its components.",
        ):
            return

        # Confirm data removal if purge is selected
        if self.purge_data.get():
            if not messagebox.askyesno(
                "Confirm Data Removal",
                "WARNING: You have selected to remove all data including notes.\n\n"
                "This action cannot be undone. Are you sure you want to continue?",
                icon="warning",
            ):
                return

        # Disable the uninstall button
        self.uninstall_button.configure(state="disabled")

        # Clear the console
        self.uninstall_console.configure(state="normal")
        self.uninstall_console.delete(1.0, tk.END)
        self.uninstall_console.configure(state="disabled")

        # Redirect stdout to the console
        sys.stdout = RedirectText(self.uninstall_console)

        # Start uninstallation in a separate thread
        threading.Thread(target=self.perform_uninstallation, daemon=True).start()

    def perform_uninstallation(self):
        """Perform the actual uninstallation."""
        try:
            # Get uninstallation options
            install_dir = Path(self.install_dir.get())
            options = {"purge": self.purge_data.get()}

            # Check if Echo-Notes is installed
            if (
                not install_dir.exists()
                or not (install_dir / "echo_notes" / "dashboard.py").exists()
            ):
                print_color(Colors.YELLOW, f"Echo-Notes not found at {install_dir}")

                # Ask user if they want to browse for the installation directory
                if messagebox.askyesno(
                    "Installation Not Found",
                    f"Echo-Notes was not found at {install_dir}.\n\n"
                    "Would you like to browse for the installation directory?",
                ):
                    # Switch back to the main thread to show the dialog
                    self.root.after(0, self.browse_for_uninstall)
                    return
                else:
                    print_color(Colors.RED, "Uninstallation cancelled.")
                    self.uninstall_button.configure(state="normal")
                    sys.stdout = self.original_stdout
                    return

            # Perform uninstallation
            success = uninstall_windows(install_dir, options)

            # Show result
            if success:
                print_color(Colors.GREEN, "Uninstallation completed successfully!")
                messagebox.showinfo(
                    "Uninstallation Complete",
                    "Echo-Notes has been uninstalled successfully!",
                )
            else:
                print_color(Colors.RED, "Uninstallation failed.")
                messagebox.showerror(
                    "Uninstallation Error",
                    "Failed to uninstall Echo-Notes.\n\n"
                    "Please check the uninstallation log for details.",
                )
        except Exception as e:
            print_color(Colors.RED, f"Error during uninstallation: {e}")
            messagebox.showerror(
                "Uninstallation Error", f"An unexpected error occurred:\n{e}"
            )
        finally:
            # Re-enable the uninstall button
            self.uninstall_button.configure(state="normal")

            # Restore stdout
            sys.stdout = self.original_stdout

    def browse_for_uninstall(self):
        """Browse for the Echo-Notes installation directory for uninstallation."""
        directory = filedialog.askdirectory(initialdir=self.install_dir.get())
        if directory:
            self.install_dir.set(directory)
            # Restart uninstallation
            self.start_uninstallation()


def run_gui():
    """Run the installer GUI."""
    root = tk.Tk()
    app = InstallerGUI(root)
    root.mainloop()


def run_cli():
    """Run the installer in command-line mode."""
    parser = argparse.ArgumentParser(description="Echo-Notes Windows Installer")

    # Common arguments
    parser.add_argument("--install-dir", type=str, help="Installation directory")

    # Subparsers for install and uninstall
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install Echo-Notes")
    install_parser.add_argument(
        "--no-shortcut", action="store_true", help="Skip desktop shortcut creation"
    )
    install_parser.add_argument(
        "--no-service", action="store_true", help="Skip service setup"
    )

    # Uninstall command
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall Echo-Notes")
    uninstall_parser.add_argument(
        "--purge", action="store_true", help="Remove all data including notes"
    )

    args = parser.parse_args()

    # Set installation directory
    if args.install_dir:
        install_dir = Path(args.install_dir)
    else:
        install_dir = Path.home() / "Echo-Notes"

    # Execute command
    if args.command == "install":
        # Check if we need to download Echo-Notes
        if not (install_dir / "echo_notes_dashboard.py").exists():
            print_color(Colors.BLUE, "Downloading Echo-Notes...")
            download_dir = download_echo_notes(install_dir)
            if not download_dir:
                print_color(Colors.RED, "Error: Failed to download Echo-Notes.")
                return 1

        # Perform installation
        options = {"no_shortcut": args.no_shortcut, "no_service": args.no_service}
        success = install_windows(install_dir, options)
        return 0 if success else 1

    elif args.command == "uninstall":
        # Perform uninstallation
        options = {"purge": args.purge}
        success = uninstall_windows(install_dir, options)
        return 0 if success else 1

    else:
        # No command specified, show help
        parser.print_help()
        return 0


def main():
    """Main entry point."""
    # Check if we're running on Windows
    if detect_os() != "windows":
        print_color(Colors.RED, "Error: This installer is for Windows only.")
        print_color(Colors.RED, f"Detected OS: {detect_os()}")
        return 1

    # Check if we're running with arguments
    if len(sys.argv) > 1:
        return run_cli()
    else:
        # No arguments, run GUI
        run_gui()
        return 0


if __name__ == "__main__":
    sys.exit(main())
