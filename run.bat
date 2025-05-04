@echo off
SETLOCAL

IF NOT EXIST "%~dp0.venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv "%~dp0.venv"
)

call "%~dp0.venv\Scripts\activate.bat"

REM Install dependencies —
echo Upgrading pip and installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Starting KanjiScanner. Press Ctrl+C to stop.
python kanjiscanner.py

ENDLOCAL
pause