# ============================================================================
# O'Reilly AI Agents MVP - Setup Script (PowerShell)
# ============================================================================
# This script sets up the Python virtual environment and installs dependencies.
# Run from the project root: .\scripts\setup.ps1
# ============================================================================

$ErrorActionPreference = "Stop"

# Ensure script runs from the project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir '..')
Set-Location $projectRoot

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  O'Reilly AI Agents MVP - Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/5] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.11+." -ForegroundColor Red
    exit 1
}
Write-Host "  Found: $pythonVersion" -ForegroundColor Green

# Create virtual environment
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "  Virtual environment already exists, skipping creation." -ForegroundColor Gray
} else {
    python -m venv .venv
    Write-Host "  Created .venv" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "[4/5] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host "[5/5] Installing dependencies..." -ForegroundColor Yellow
pip install -e ".[dev]" --quiet

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Setup Complete\!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Copy .env.example to .env and add your API keys"
Write-Host "  2. Run: .\scripts\run_once.ps1"
Write-Host "  3. Or start the watcher: .\scripts\run_watcher.ps1"
Write-Host ""
Write-Host "To activate the venv manually: .\.venv\Scripts\Activate.ps1"
