# Start the interactive menu for the O'Reilly Agent MVP

Write-Host "Starting O'Reilly Agent MVP Interactive Menu..." -ForegroundColor Cyan
Write-Host ""

# Ensure virtual environment exists and use its Python
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir '..')
Set-Location $projectRoot

$venvRoot = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvRoot "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: .venv not found. Run .\scripts\setup.ps1 first." -ForegroundColor Red
    exit 1
}
$env:VIRTUAL_ENV = $venvRoot
$env:PATH = (Join-Path $venvRoot "Scripts") + ";" + $env:PATH

# Run the menu
& $venvPython -m agent_mvp.cli.interactive_menu
