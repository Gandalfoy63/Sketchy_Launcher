@echo off
echo Installing Python dependencies for Sketchy Launcher...

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install required packages
pip install customtkinter pillow requests pywin32 winshell

echo.
echo All dependencies installed.
pause
