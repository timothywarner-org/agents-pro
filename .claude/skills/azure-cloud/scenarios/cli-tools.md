# Installing Azure CLI Tools

## Auto-Installation Flow

When a CLI tool is missing, follow this sequence:

### 1. Detect Missing Tool

Check for these error patterns:
- `'az' is not recognized` or `az: command not found`
- `'azd' is not recognized` or `azd: command not found`
- `'func' is not recognized` or `func: command not found`
- `'docker' is not recognized` or `docker: command not found`

### 2. Offer One-Click Install

**Use AskUserQuestion to offer installation:**

"I detected that [TOOL] is not installed. Would you like me to install it now?"
- Yes, install it
- No, I'll install it manually

### 3. Run Installation Command

**Windows (preferred - winget):**
```powershell
# Azure CLI
winget install Microsoft.AzureCLI --accept-source-agreements --accept-package-agreements

# Azure Developer CLI
winget install Microsoft.Azd --accept-source-agreements --accept-package-agreements

# Azure Functions Core Tools
winget install Microsoft.Azure.FunctionsCoreTools --accept-source-agreements --accept-package-agreements

# Docker Desktop
winget install Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
```

**macOS:**
```bash
# Azure CLI
brew install azure-cli

# Azure Developer CLI
brew tap azure/azd && brew install azd

# Azure Functions Core Tools
brew tap azure/functions && brew install azure-functions-core-tools@4

# Docker Desktop
brew install --cask docker
```

**Linux (Ubuntu/Debian):**
```bash
# Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Azure Developer CLI
curl -fsSL https://aka.ms/install-azd.sh | bash

# Azure Functions Core Tools
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
sudo apt-get update && sudo apt-get install azure-functions-core-tools-4

# Docker
sudo apt-get install docker.io
sudo systemctl enable docker && sudo systemctl start docker
```

### 4. Verify Installation

```bash
# After installation, verify:
az version
azd version
func --version
docker version
```

### 5. Handle PATH Issues

If command still not found after install:

**Windows:**
- Restart terminal
- Or run: `refreshenv` (if using Chocolatey)
- Or start new PowerShell/CMD window

**macOS/Linux:**
- Run: `source ~/.bashrc` or `source ~/.zshrc`
- Or start new terminal session

## Using MCP Install Tool

The Azure MCP server provides installation guidance:

```
Tool: azure__extension_cli_install
Parameters:
  - cli-type: "az" | "azd" | "func"
```

**Example:**
```
Use azure__extension_cli_install with cli-type: "azd"
```

This returns platform-specific installation instructions.

## Tool Priority

For Azure deployments, install in this order:

| Priority | Tool | Required For |
|----------|------|--------------|
| 1 | `azd` | Application deployments (ALWAYS use this) |
| 2 | `az` | Resource queries, manual operations |
| 3 | `docker` | Container builds, local testing |
| 4 | `func` | Local Functions development |

## Quick Check Script

Run this to check all tools at once:

```bash
echo "=== Azure Tools Check ==="
echo -n "az: " && (az version --query '"azure-cli"' -o tsv 2>/dev/null || echo "NOT INSTALLED")
echo -n "azd: " && (azd version 2>/dev/null || echo "NOT INSTALLED")
echo -n "docker: " && (docker version --format '{{.Server.Version}}' 2>/dev/null || echo "NOT INSTALLED")
echo -n "func: " && (func --version 2>/dev/null || echo "NOT INSTALLED")
```

## Authentication After Installation

### Azure CLI (az)

```bash
# Interactive (opens browser)
az login

# Device code (headless/remote) - use if browser login fails
az login --use-device-code

# Service principal (CI/CD)
az login --service-principal -u APP_ID -p SECRET --tenant TENANT_ID
```

### Azure Developer CLI (azd)

```bash
# Uses Azure CLI credentials by default
# Or explicitly:
azd auth login
```

**Tip:** If device code auth times out repeatedly, run `az login` in a separate terminal window where you can interact with it directly.

## Common Installation Issues

| Issue | Solution |
|-------|----------|
| winget not found | Install App Installer from Microsoft Store |
| brew not found | Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Permission denied | Run as Administrator (Windows) or use sudo (Linux) |
| Old version installed | Run `az upgrade` or `brew upgrade azure-cli` |
| PATH not updated | Restart terminal or source shell config |

## Bulk Install (All Tools)

**Windows:**
```powershell
winget install Microsoft.AzureCLI Microsoft.Azd Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
```

**macOS:**
```bash
brew install azure-cli && brew tap azure/azd && brew install azd && brew install --cask docker
```
