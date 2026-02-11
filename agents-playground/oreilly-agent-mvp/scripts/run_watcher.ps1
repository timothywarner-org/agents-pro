# ============================================================================
# O'Reilly AI Agents MVP - Run Watcher Script (PowerShell)
# ============================================================================
# Starts the folder watcher to automatically process incoming issues.
# Run from the project root: .\scripts\run_watcher.ps1
# Press Ctrl+C to stop.
# ============================================================================

$ErrorActionPreference = "Stop"

# Ensure script runs from the project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir '..')
Set-Location $projectRoot

# Ensure virtual environment exists and use its Python
$venvRoot = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvRoot "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: .venv not found. Run .\scripts\setup.ps1 first." -ForegroundColor Red
    exit 1
}
$env:VIRTUAL_ENV = $venvRoot
$env:PATH = (Join-Path $venvRoot "Scripts") + ";" + $env:PATH

Write-Host "Starting folder watcher..." -ForegroundColor Cyan
Write-Host "Watching: incoming/" -ForegroundColor Gray
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Run the watcher
& $venvPython -m agent_mvp.watcher.folder_watcher

if ($LASTEXITCODE -ne 0) {
    Write-Host "Watcher exited with code: $LASTEXITCODE" -ForegroundColor Yellow
}
