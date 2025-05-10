from setuptools import setup, find_packages

setup(
    name="echo_notes",
    version="0.5.1",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'python-dateutil>=2.8.2',
        'PyQt6>=6.4.0'
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'process-notes=ai_notes_nextcloud:main',
            'generate-summary=ai_weekly_summary:main',
            'echo-notes-daemon=echo_notes_daemon:main',
            'echo-notes-config=echo_notes_daemon:configure_scheduling',
            'echo-notes-dashboard=echo_notes_dashboard:main'
        ]
    },
    data_files=[
        ('share/applications', ['echo-notes-dashboard.desktop']),
        ('bin', ['install_desktop_shortcut.sh', 'create_windows_shortcut.bat', 'create_macos_shortcut.py', 'launcher.py'])
    ],
)