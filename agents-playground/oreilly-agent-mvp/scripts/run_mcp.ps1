# Run the MCP server for O'Reilly Agent MVP

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Set-Location $ProjectRoot

# Ensure virtual environment exists and use its Python
$venvRoot = Join-Path $ProjectRoot ".venv"
$venvPython = Join-Path $venvRoot "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: .venv not found. Run .\scripts\setup.ps1 first." -ForegroundColor Red
    exit 1
}
$env:VIRTUAL_ENV = $venvRoot
$env:PATH = (Join-Path $venvRoot "Scripts") + ";" + $env:PATH

Write-Host "Starting O'Reilly Agent MVP MCP Server..."
Write-Host "Project root: $ProjectRoot"
Write-Host ""
Write-Host "The server will listen on stdio for MCP client connections."
Write-Host "Press Ctrl+C to stop."
Write-Host ""

& $venvPython -m agent_mvp.mcp_server
