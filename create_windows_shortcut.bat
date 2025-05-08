@echo off
echo Creating Echo Notes Dashboard shortcut...

:: Get the current directory
set SCRIPT_DIR=%~dp0

:: Create a shortcut on the desktop
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Echo Notes Dashboard.lnk'); $Shortcut.TargetPath = 'cmd.exe'; $Shortcut.Arguments = '/c echo-notes-dashboard'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = '%SCRIPT_DIR%\Echo-Notes-Icon.png'; $Shortcut.Save()"

echo Shortcut created on your desktop!
echo You can now launch Echo Notes Dashboard by double-clicking the shortcut.
pause