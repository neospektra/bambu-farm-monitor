# Bambu Farm Monitor - Windows Automated Installation Script
# This script will install Docker Desktop (if needed) and set up Bambu Farm Monitor

#Requires -Version 5.1

# Script configuration
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Color functions for better UX
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✓ $Message" "Green"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "✗ $Message" "Red"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠ $Message" "Yellow"
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ $Message" "Cyan"
}

function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-ColorOutput "═══════════════════════════════════════════════════════════" "Magenta"
    Write-ColorOutput "  $Message" "Magenta"
    Write-ColorOutput "═══════════════════════════════════════════════════════════" "Magenta"
    Write-Host ""
}

# Check if running as Administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check if WSL 2 is installed
function Test-WSL2 {
    try {
        $wslVersion = wsl --status 2>&1
        return $wslVersion -match "Default Version: 2"
    }
    catch {
        return $false
    }
}

# Check if Docker is installed and running
function Test-Docker {
    try {
        $null = docker --version 2>&1
        $null = docker ps 2>&1
        return $true
    }
    catch {
        return $false
    }
}

# Check if Podman is installed and running
function Test-Podman {
    try {
        $null = podman --version 2>&1
        $null = podman ps 2>&1
        return $true
    }
    catch {
        return $false
    }
}

# Install WSL 2
function Install-WSL2 {
    Write-Header "Installing WSL 2"
    Write-Info "Installing Windows Subsystem for Linux..."

    try {
        wsl --install --no-distribution
        Write-Success "WSL 2 installation initiated"
        Write-Warning "You will need to restart your computer after this script completes"
        return $true
    }
    catch {
        Write-Error "Failed to install WSL 2: $_"
        return $false
    }
}

# Install Docker Desktop
function Install-DockerDesktop {
    Write-Header "Docker Desktop Installation"
    Write-Info "Docker Desktop needs to be installed manually."
    Write-Host ""
    Write-ColorOutput "Please follow these steps:" "Yellow"
    Write-Host "1. Visit: https://www.docker.com/products/docker-desktop/"
    Write-Host "2. Click 'Download for Windows'"
    Write-Host "3. Run the installer"
    Write-Host "4. Enable 'Use WSL 2 instead of Hyper-V' (recommended)"
    Write-Host "5. Complete the installation and restart if prompted"
    Write-Host "6. Start Docker Desktop and wait for it to fully initialize"
    Write-Host ""

    $response = Read-Host "Press Enter when Docker Desktop is installed and running, or type 'skip' to try Podman instead"

    return $response -ne "skip"
}

# Install Podman Desktop
function Install-PodmanDesktop {
    Write-Header "Podman Desktop Installation"
    Write-Info "Podman Desktop is a free alternative to Docker Desktop."
    Write-Host ""
    Write-ColorOutput "Please follow these steps:" "Yellow"
    Write-Host "1. Visit: https://podman-desktop.io/downloads/windows"
    Write-Host "2. Download the latest Windows installer"
    Write-Host "3. Run the installer"
    Write-Host "4. Start Podman Desktop"
    Write-Host "5. Click 'Initialize and start' if prompted"
    Write-Host "6. Wait for the Podman machine to start"
    Write-Host ""

    $response = Read-Host "Press Enter when Podman Desktop is installed and running, or type 'cancel' to exit"

    return $response -ne "cancel"
}

# Get printer information from user
function Get-PrinterInfo {
    param([int]$PrinterNumber)

    Write-Host ""
    Write-ColorOutput "═══ Printer $PrinterNumber Configuration ═══" "Cyan"

    $ip = Read-Host "Printer IP Address (e.g., 192.168.1.100)"
    if ([string]::IsNullOrWhiteSpace($ip)) {
        return $null
    }

    $code = Read-Host "8-digit Access Code (from MQTT settings)"
    if ([string]::IsNullOrWhiteSpace($code) -or $code.Length -ne 8) {
        Write-Warning "Access code must be exactly 8 digits"
        return $null
    }

    $name = Read-Host "Printer Name (optional, press Enter to skip)"
    $serial = Read-Host "Serial Number (optional, press Enter to skip)"

    return @{
        Number = $PrinterNumber
        IP = $ip
        Code = $code
        Name = $name
        Serial = $serial
    }
}

# Create docker-compose.yml
function New-DockerComposeFile {
    param(
        [string]$Path,
        [array]$Printers
    )

    $composeContent = @"
version: '3.8'
services:
  bambu-farm-monitor:
    image: neospektra/bambu-farm-monitor:latest
    container_name: bambu-farm-monitor
    ports:
      - "8080:8080"   # Web UI
      - "1984:1984"   # go2rtc WebRTC
      - "5000:5000"   # Config API
      - "5001:5001"   # Status API
"@

    if ($Printers.Count -gt 0) {
        $composeContent += "`n    environment:"

        foreach ($printer in $Printers) {
            $composeContent += "`n      - PRINTER$($printer.Number)_IP=$($printer.IP)"
            $composeContent += "`n      - PRINTER$($printer.Number)_CODE=$($printer.Code)"

            if (![string]::IsNullOrWhiteSpace($printer.Name)) {
                $composeContent += "`n      - PRINTER$($printer.Number)_NAME=$($printer.Name)"
            }

            if (![string]::IsNullOrWhiteSpace($printer.Serial)) {
                $composeContent += "`n      - PRINTER$($printer.Number)_SERIAL=$($printer.Serial)"
            }
        }
    }

    $composeContent += @"

    volumes:
      - bambu-config:/app/config
    restart: unless-stopped

volumes:
  bambu-config:
"@

    Set-Content -Path $Path -Value $composeContent -Encoding UTF8
}

# Main installation process
function Start-Installation {
    Write-Header "Bambu Farm Monitor - Windows Installation"
    Write-ColorOutput "Version 3.3.9" "Gray"
    Write-Host ""
    Write-Info "This script will help you install and configure Bambu Farm Monitor"
    Write-Host ""

    # Check administrator privileges
    if (-not (Test-Administrator)) {
        Write-Warning "This script should be run as Administrator for best results."
        $continue = Read-Host "Continue anyway? (y/n)"
        if ($continue -ne "y") {
            Write-Info "Please right-click the script and select 'Run as Administrator'"
            exit 1
        }
    }

    # Determine which container runtime to use
    $useDocker = $false
    $usePodman = $false
    $needsRestart = $false

    Write-Header "Checking System Requirements"

    # Check for existing Docker installation
    if (Test-Docker) {
        Write-Success "Docker is installed and running"
        $useDocker = $true
    }
    # Check for existing Podman installation
    elseif (Test-Podman) {
        Write-Success "Podman is installed and running"
        $usePodman = $true
    }
    # Neither installed - need to install one
    else {
        Write-Warning "Neither Docker nor Podman is installed"
        Write-Host ""
        Write-ColorOutput "Choose your container runtime:" "Yellow"
        Write-Host "1. Docker Desktop (recommended, requires WSL 2)"
        Write-Host "2. Podman Desktop (free alternative)"
        Write-Host ""

        $choice = Read-Host "Enter your choice (1 or 2)"

        if ($choice -eq "1") {
            # Check WSL 2
            if (-not (Test-WSL2)) {
                Write-Warning "WSL 2 is not installed"
                $installWSL = Read-Host "Install WSL 2 now? (y/n)"

                if ($installWSL -eq "y") {
                    if (Install-WSL2) {
                        $needsRestart = $true
                    }
                    else {
                        Write-Error "Failed to install WSL 2. Please install manually."
                        exit 1
                    }
                }
            }
            else {
                Write-Success "WSL 2 is already installed"
            }

            # Install Docker Desktop
            if (Install-DockerDesktop) {
                if (Test-Docker) {
                    Write-Success "Docker Desktop is ready!"
                    $useDocker = $true
                }
                else {
                    Write-Error "Docker Desktop is not running. Please start it and run this script again."
                    exit 1
                }
            }
            else {
                Write-Info "Switching to Podman Desktop installation..."
                if (Install-PodmanDesktop) {
                    if (Test-Podman) {
                        Write-Success "Podman Desktop is ready!"
                        $usePodman = $true
                    }
                    else {
                        Write-Error "Podman Desktop is not running. Please start it and run this script again."
                        exit 1
                    }
                }
                else {
                    Write-Error "Installation cancelled"
                    exit 1
                }
            }
        }
        elseif ($choice -eq "2") {
            if (Install-PodmanDesktop) {
                if (Test-Podman) {
                    Write-Success "Podman Desktop is ready!"
                    $usePodman = $true
                }
                else {
                    Write-Error "Podman Desktop is not running. Please start it and run this script again."
                    exit 1
                }
            }
            else {
                Write-Error "Installation cancelled"
                exit 1
            }
        }
        else {
            Write-Error "Invalid choice"
            exit 1
        }
    }

    # If restart is needed, inform user and exit
    if ($needsRestart) {
        Write-Header "Restart Required"
        Write-Warning "Your computer needs to be restarted to complete WSL 2 installation"
        Write-Info "After restart, install Docker Desktop and run this script again"
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 0
    }

    # Set command based on runtime
    $containerCmd = if ($useDocker) { "docker" } else { "podman" }

    # Pull the latest image
    Write-Header "Downloading Bambu Farm Monitor"
    Write-Info "Pulling latest image from Docker Hub..."

    try {
        & $containerCmd pull neospektra/bambu-farm-monitor:latest
        Write-Success "Image downloaded successfully"
    }
    catch {
        Write-Error "Failed to pull image: $_"
        exit 1
    }

    # Configure printers
    Write-Header "Printer Configuration"
    Write-Info "You can configure up to 4 printers now (or add them later via web UI)"
    Write-Host ""

    $configurePrinters = Read-Host "Configure printers now? (y/n)"
    $printers = @()

    if ($configurePrinters -eq "y") {
        for ($i = 1; $i -le 4; $i++) {
            Write-Host ""
            $addPrinter = Read-Host "Add Printer $i? (y/n)"

            if ($addPrinter -eq "y") {
                $printer = Get-PrinterInfo -PrinterNumber $i
                if ($printer) {
                    $printers += $printer
                    Write-Success "Printer $i configured"
                }
                else {
                    Write-Warning "Printer $i skipped"
                }
            }
            else {
                break
            }
        }
    }

    # Choose deployment method
    Write-Header "Deployment Configuration"
    Write-Host ""
    Write-ColorOutput "Choose deployment method:" "Yellow"
    Write-Host "1. Docker Compose (recommended - easier to manage)"
    Write-Host "2. Docker Run (simple - single command)"
    Write-Host ""

    $deployChoice = Read-Host "Enter your choice (1 or 2)"

    if ($deployChoice -eq "1") {
        # Docker Compose method
        $installPath = "$env:USERPROFILE\bambu-farm-monitor"

        # Create directory
        if (-not (Test-Path $installPath)) {
            New-Item -ItemType Directory -Path $installPath -Force | Out-Null
            Write-Success "Created directory: $installPath"
        }

        # Create docker-compose.yml
        $composePath = Join-Path $installPath "docker-compose.yml"
        New-DockerComposeFile -Path $composePath -Printers $printers
        Write-Success "Created docker-compose.yml"

        # Start container
        Write-Header "Starting Bambu Farm Monitor"
        Write-Info "Starting container..."

        try {
            Set-Location $installPath
            & $containerCmd compose up -d
            Write-Success "Container started successfully!"
        }
        catch {
            Write-Error "Failed to start container: $_"
            exit 1
        }
    }
    else {
        # Docker Run method
        Write-Header "Starting Bambu Farm Monitor"
        Write-Info "Starting container..."

        $runCmd = "$containerCmd run -d --name bambu-farm-monitor " +
                  "-p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 "

        # Add environment variables for printers
        foreach ($printer in $printers) {
            $runCmd += "-e PRINTER$($printer.Number)_IP=$($printer.IP) "
            $runCmd += "-e PRINTER$($printer.Number)_CODE=$($printer.Code) "

            if (![string]::IsNullOrWhiteSpace($printer.Name)) {
                $runCmd += "-e PRINTER$($printer.Number)_NAME='$($printer.Name)' "
            }

            if (![string]::IsNullOrWhiteSpace($printer.Serial)) {
                $runCmd += "-e PRINTER$($printer.Number)_SERIAL=$($printer.Serial) "
            }
        }

        $runCmd += "-v bambu-config:/app/config neospektra/bambu-farm-monitor:latest"

        try {
            Invoke-Expression $runCmd
            Write-Success "Container started successfully!"
        }
        catch {
            Write-Error "Failed to start container: $_"
            exit 1
        }
    }

    # Wait for container to be ready
    Write-Info "Waiting for services to initialize..."
    Start-Sleep -Seconds 5

    # Check if container is running
    $containerStatus = & $containerCmd ps --filter "name=bambu-farm-monitor" --format "{{.Status}}"

    if ($containerStatus -match "Up") {
        Write-Success "Bambu Farm Monitor is running!"
    }
    else {
        Write-Warning "Container may not be running properly"
        Write-Info "Check logs with: $containerCmd logs bambu-farm-monitor"
    }

    # Show completion message
    Write-Header "Installation Complete!"
    Write-Host ""
    Write-Success "Bambu Farm Monitor is now running!"
    Write-Host ""
    Write-ColorOutput "Access your dashboard at:" "Green"
    Write-ColorOutput "  http://localhost:8080" "Cyan"
    Write-Host ""

    if ($printers.Count -eq 0) {
        Write-Info "Since you didn't configure printers, you'll need to add them via the web UI"
        Write-Info "Click 'Add Printer' button and follow the setup wizard"
    }

    Write-Host ""
    Write-ColorOutput "Useful commands:" "Yellow"
    Write-Host "  View logs:       $containerCmd logs bambu-farm-monitor"
    Write-Host "  Stop container:  $containerCmd stop bambu-farm-monitor"
    Write-Host "  Start container: $containerCmd start bambu-farm-monitor"
    Write-Host "  Restart:         $containerCmd restart bambu-farm-monitor"
    Write-Host ""
    Write-Info "For more information, visit: https://github.com/neospektra/bambu-farm-monitor"
    Write-Host ""

    # Open browser
    $openBrowser = Read-Host "Open dashboard in browser now? (y/n)"
    if ($openBrowser -eq "y") {
        Start-Process "http://localhost:8080"
    }

    Write-Host ""
    Write-ColorOutput "Press Enter to exit..." "Gray"
    Read-Host
}

# Run the installation
try {
    Start-Installation
}
catch {
    Write-Error "An unexpected error occurred: $_"
    Write-Host ""
    Write-Info "Please report this issue at: https://github.com/neospektra/bambu-farm-monitor/issues"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
