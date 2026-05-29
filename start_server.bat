@echo off
REM Double-click launcher for the Agentic AI Engine app server.
REM Runs start_server.ps1 with execution policy bypass so it works on any machine.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_server.ps1"
echo.
echo Server stopped. Press any key to close this window.
pause >nul
