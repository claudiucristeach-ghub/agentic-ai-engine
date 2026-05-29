# Starts the Agentic AI Engine app server for local development.
#
# Usage:
#   - Double-click  start_server.bat   (easiest), or
#   - From a PowerShell terminal in the project root:  .\start_server.ps1
#
# The server runs with --reload, so your code changes under app\ are picked up
# automatically. Press Ctrl+C in this window to stop it.

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Host "ERROR: .venv not found at $python" -ForegroundColor Red
    Write-Host "Create the virtual environment first (see README sections 3-4)." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Warn if something is already listening on port 8000
$inUse = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($inUse) {
    $pid8000 = ($inUse | Select-Object -First 1).OwningProcess
    Write-Host "Port 8000 is already in use (PID $pid8000)." -ForegroundColor Yellow
    Write-Host "The app may already be running - open http://127.0.0.1:8000/" -ForegroundColor Yellow
    Write-Host "Or stop that process and re-run this script." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "  Agentic AI Engine -> http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "  (auto-reloads on changes under app\ ; press Ctrl+C to stop)" -ForegroundColor DarkGray
Write-Host ""

& $python -m uvicorn agentic_ai_main:app --reload --reload-dir app --port 8000
