from setuptools import setup, find_packages

setup(
    name="echo_notes",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'python-dateutil>=2.8.2'
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'process-notes=ai_notes_nextcloud:main',
            'generate-summary=ai_weekly_summary:main',
            'echo-notes-daemon=echo_notes_daemon:main',
            'echo-notes-config=echo_notes_daemon:configure_scheduling'
        ]
    },
)