from setuptools import setup, find_packages

setup(
    name="echo_notes",
    version="0.5.1",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'python-dateutil>=2.8.2',
        'PyQt6>=6.4.0',
        'python-docx>=0.8.11'  # For processing .docx files
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'process-notes=echo_notes.notes_nextcloud:main',
            'generate-summary=echo_notes.weekly_summary:main',
            'echo-notes-daemon=echo_notes.daemon:main',
            'echo-notes-config=echo_notes.daemon:configure_scheduling',
            'echo-notes-dashboard=echo_notes.dashboard:main'
        ]
    },
    data_files=[
        ('share/applications', ['echo-notes-dashboard.desktop']),
        ('bin', ['install_desktop_shortcuts.sh', 'create_windows_shortcut.bat', 'create_macos_shortcut.py', 'launcher.py'])
    ],
)