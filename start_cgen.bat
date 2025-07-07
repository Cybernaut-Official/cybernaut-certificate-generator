@echo off
REM === Batch file to start Redis (in WSL), then Celery and Django (on Windows) ===

REM Change to current directory (where this BAT file is located)
cd /d %~dp0

echo.
echo === Starting Redis inside WSL (Ubuntu) ===
wsl -d Ubuntu bash -c "pgrep redis-server > /dev/null || (echo Starting Redis... && redis-server --daemonize yes)"
echo Redis is ready.
echo.

REM Start Celery worker in a new command prompt window
echo === Starting Celery worker ===
start "Celery Worker" cmd /k "call env\Scripts\activate && celery -A config worker --pool=solo --loglevel=info"

REM Wait a bit to ensure Celery starts up
timeout /t 2 > nul

REM Start Django server in a new command prompt window
echo === Starting Django server ===
start "Django Server" cmd /k "call env\Scripts\activate && python manage.py runserver"

echo.
echo === All systems launched ===
