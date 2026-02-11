# Quick MCP Server Launcher
# PowerShell 7+ - Start MCP server directly

#Requires -Version 7.0

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Set-Location $ProjectRoot

# Activate venv if available
$venvPath = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
}

Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              O'Reilly Agent MVP - MCP Server         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting MCP server with stdio transport..." -ForegroundColor Yellow
Write-Host "Use with Claude Desktop or VS Code Copilot" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor DarkGray
Write-Host ""

python -m agent_mvp.mcp_server
