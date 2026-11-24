@echo off
cd /d "%~dp0"
python -m venv .venv || goto :fail
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt || goto :fail
.venv\Scripts\python -m pip install --no-deps pyremoteplay pyps4-2ndscreen || goto :fail
echo Done. Start the app with run.bat
pause
exit /b 0
:fail
echo Setup failed.
pause
exit /b 1
