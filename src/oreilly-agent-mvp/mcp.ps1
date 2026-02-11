# Quick MCP Server Launcher
# PowerShell 7+ - Start MCP server directly

#Requires -Version 7.0

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

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

Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              O'Reilly Agent MVP - MCP Server         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting MCP server with stdio transport..." -ForegroundColor Yellow
Write-Host "Use with Claude Desktop or VS Code Copilot" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor DarkGray
Write-Host ""

& $venvPython -m agent_mvp.mcp_server
