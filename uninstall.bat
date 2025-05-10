@echo off
:: Echo-Notes Uninstallation Script for Windows
:: This script removes Echo-Notes while preserving user notes

echo ===== Echo-Notes Uninstaller =====
echo.

:: Get the script directory
set SCRIPT_DIR=%~dp0
cd "%SCRIPT_DIR%"

echo Uninstallation directory: %SCRIPT_DIR%

:: Verify we're in the correct directory
if not exist "echo_notes_dashboard.py" (
    echo Error: Could not find echo_notes_dashboard.py in the current directory.
    echo This script must be run from the Echo-Notes directory.
    echo Current directory: %CD%
    echo Files in current directory:
    dir
    echo.
    echo Please run this script from the Echo-Notes directory.
    pause
    exit /b 1
)

:: Parse command line arguments
set KEEP_CONFIG=false
set PURGE=false

:parse_args
if "%~1"=="" goto :end_parse_args
if /i "%~1"=="--help" goto :show_help
if /i "%~1"=="-h" goto :show_help
if /i "%~1"=="--keep-config" set KEEP_CONFIG=true
if /i "%~1"=="--purge" set PURGE=true
shift
goto :parse_args

:show_help
echo Echo-Notes Unified Uninstaller
echo This script removes Echo-Notes while preserving user notes.
echo.
echo Usage: uninstall.bat [OPTIONS]
echo.
echo Options:
echo   --help, -h       Show this help message and exit
echo   --keep-config    Keep configuration files
echo   --purge          Remove everything including notes (USE WITH CAUTION)
echo.
echo Examples:
echo   uninstall.bat                # Standard uninstallation
echo   uninstall.bat --keep-config  # Uninstall but keep configuration
echo.
pause
exit /b 0

:end_parse_args

:: Ask for confirmation
echo This will uninstall Echo-Notes from your system.
echo Your notes will be preserved.
if "%PURGE%"=="true" (
    echo WARNING: --purge option selected. This will also remove your notes!
)
echo.

set /p CONFIRM=Do you want to continue? (y/N): 
if /i not "%CONFIRM%"=="y" (
    echo Uninstallation cancelled.
    pause
    exit /b 0
)

:: Stop running processes
echo Stopping Echo-Notes processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Echo-Notes*" > nul 2>&1
echo Processes stopped.

:: Remove desktop shortcut
echo Removing desktop shortcut...
powershell -Command "Remove-Item -Path ([Environment]::GetFolderPath('Desktop') + '\Echo Notes Dashboard.lnk') -Force -ErrorAction SilentlyContinue"
echo Desktop shortcut removed.

:: Remove virtual environment
echo Removing virtual environment...
if exist "echo_notes_venv" (
    rmdir /s /q echo_notes_venv
    echo Virtual environment removed.
) else (
    echo Virtual environment not found.
)

:: Remove configuration files if not keeping them
if "%KEEP_CONFIG%"=="false" (
    echo Removing configuration files...
    if exist "shared\schedule_config.json" del /f /q shared\schedule_config.json
    echo Configuration files removed.
) else (
    echo Keeping configuration files as requested.
)

:: Remove notes if purging
if "%PURGE%"=="true" (
    echo Removing notes directory...
    set NOTES_DIR=%USERPROFILE%\Documents\notes\log
    if defined ECHO_NOTES_DIR set NOTES_DIR=%ECHO_NOTES_DIR%
    
    if exist "%NOTES_DIR%" (
        rmdir /s /q "%NOTES_DIR%"
        echo Removed notes directory: %NOTES_DIR%
    ) else (
        echo Notes directory not found: %NOTES_DIR%
    )
) else (
    echo Preserved notes directory.
)

echo.
echo Uninstallation complete!
echo.
echo === Notes Location ===
echo Your notes are still available at: %USERPROFILE%\Documents\notes\log
if defined ECHO_NOTES_DIR echo Your notes are still available at: %ECHO_NOTES_DIR%
echo.
echo If you want to completely remove Echo-Notes, you can now delete this directory:
echo %SCRIPT_DIR%
echo.

pause