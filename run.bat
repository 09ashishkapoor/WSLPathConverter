@echo off
:: WSL Path Converter - one-click launcher
:: Finds Python automatically (venv first, then system)

setlocal

set "SCRIPT_DIR=%~dp0"
set "VENV_PYTHON=%SCRIPT_DIR%.venv\Scripts\pythonw.exe"
set "GUI_SCRIPT=%SCRIPT_DIR%wslpath_gui.py"

if exist "%VENV_PYTHON%" (
    start "" "%VENV_PYTHON%" "%GUI_SCRIPT%"
) else (
    :: Fall back to system Python (pythonw to avoid a console window)
    where pythonw >nul 2>&1
    if %errorlevel%==0 (
        start "" pythonw "%GUI_SCRIPT%"
    ) else (
        python "%GUI_SCRIPT%"
    )
)

endlocal
