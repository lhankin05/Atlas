@echo off
cd /d "%~dp0"
start "Atlas server" cmd /k python server.py
timeout /t 2 >nul
start "" http://localhost:8000/atlas.html
