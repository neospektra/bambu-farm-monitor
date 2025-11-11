# Installation Scripts

This directory contains automated installation scripts for Bambu Farm Monitor.

## Windows Installation Script

### `install-windows.ps1`

Automated PowerShell script that installs Docker Desktop (or Podman Desktop) and sets up Bambu Farm Monitor on Windows.

#### Features

- ✅ Checks for existing Docker/Podman installation
- ✅ Guides through Docker Desktop or Podman Desktop installation
- ✅ Installs WSL 2 if needed (for Docker Desktop)
- ✅ Pulls the latest Bambu Farm Monitor image
- ✅ Interactive printer configuration (up to 4 printers)
- ✅ Choice between Docker Compose or Docker Run deployment
- ✅ Automatic container startup and verification
- ✅ Colored output and progress indicators
- ✅ Comprehensive error handling

#### Usage

**Method 1: Right-click (Easiest)**

1. Download or clone this repository
2. Navigate to the `scripts` folder
3. Right-click `install-windows.ps1`
4. Select **"Run with PowerShell"**
5. Follow the on-screen prompts

**Method 2: PowerShell**

1. Open PowerShell as Administrator (recommended)
2. Navigate to the repository:
   ```powershell
   cd C:\path\to\bambu-farm-monitor
   ```
3. Run the script:
   ```powershell
   .\scripts\install-windows.ps1
   ```
4. Follow the on-screen prompts

**Method 3: Download and Run Directly**

```powershell
# Download the script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/neospektra/bambu-farm-monitor/main/scripts/install-windows.ps1" -OutFile "$env:TEMP\install-windows.ps1"

# Run it
& "$env:TEMP\install-windows.ps1"
```

#### What the Script Does

1. **System Check**
   - Verifies administrator privileges (recommended but not required)
   - Checks for existing Docker or Podman installation

2. **Installation (if needed)**
   - Offers choice between Docker Desktop and Podman Desktop
   - Installs WSL 2 if Docker Desktop is chosen and WSL isn't installed
   - Guides through Docker/Podman Desktop installation
   - Verifies installation is working

3. **Image Download**
   - Pulls the latest `neospektra/bambu-farm-monitor:latest` image from Docker Hub

4. **Configuration**
   - Optionally configures up to 4 printers interactively
   - Collects IP address, access code, name, and serial number for each printer

5. **Deployment**
   - Choice 1: Creates `docker-compose.yml` in `%USERPROFILE%\bambu-farm-monitor`
   - Choice 2: Runs container using `docker run` command
   - Starts the container with all configured printers

6. **Verification**
   - Checks if container is running
   - Provides next steps and useful commands
   - Optionally opens the dashboard in your browser

#### Prerequisites

- Windows 10/11 (64-bit)
- PowerShell 5.1 or later (pre-installed on Windows 10/11)
- Internet connection
- Administrator access (recommended)

#### Troubleshooting

**Script won't run - "Execution Policy" error**

PowerShell may block scripts by default. To allow it:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run the script again.

**"Docker/Podman not found" after installation**

- Make sure Docker Desktop or Podman Desktop is fully started
- Check the system tray for Docker/Podman icon
- Wait for it to finish initializing (may take 1-2 minutes)
- Restart your terminal/PowerShell window
- Run the script again

**WSL 2 installation requires restart**

If WSL 2 is installed during the script:
1. Restart your computer
2. Install Docker Desktop manually or wait for the script to guide you
3. Run the script again to complete the setup

**Container fails to start**

Check the logs:
```powershell
docker logs bambu-farm-monitor
# or
podman logs bambu-farm-monitor
```

Common causes:
- Port already in use (change ports in docker-compose.yml)
- Invalid printer configuration
- Docker/Podman not fully initialized

#### After Installation

Once the script completes:

1. **Access the dashboard**: http://localhost:8080
2. If you didn't configure printers during installation, click **"Add Printer"** in the web UI
3. Follow the [First-Time Setup](../docs/wiki/First-Time-Setup.md) guide
4. Customize your dashboard with [Layout Customization](../docs/wiki/Layout-Customization.md)

#### Useful Commands

After installation, manage your container with:

```powershell
# View running containers
docker ps
# or
podman ps

# View logs
docker logs bambu-farm-monitor
# or
podman logs bambu-farm-monitor

# Stop the container
docker stop bambu-farm-monitor
# or
podman stop bambu-farm-monitor

# Start the container
docker start bambu-farm-monitor
# or
podman start bambu-farm-monitor

# Restart the container
docker restart bambu-farm-monitor
# or
podman restart bambu-farm-monitor

# Update to latest version
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
docker pull neospektra/bambu-farm-monitor:latest
# Then run the script again or start manually
```

#### Configuration Files

**Docker Compose Installation:**
- Location: `%USERPROFILE%\bambu-farm-monitor\docker-compose.yml`
- Edit this file to change ports, add/remove printers, or modify settings
- After changes, run: `docker compose down && docker compose up -d`

**Docker Run Installation:**
- No configuration file - settings are in the `docker run` command
- To change settings, stop and remove the container, then create a new one with updated parameters

#### Support

For issues or questions:
- See the [Windows Installation Guide](../docs/wiki/Windows-Installation.md)
- Check [Common Issues](../docs/wiki/Common-Issues.md)
- Review the [FAQ](../docs/wiki/FAQ.md)
- Open an issue: https://github.com/neospektra/bambu-farm-monitor/issues

---

## Future Scripts

Additional installation scripts for other platforms may be added here:
- `install-linux.sh` - Linux automated installer
- `install-macos.sh` - macOS automated installer
- `install-synology.sh` - Synology NAS installer
- `install-unraid.sh` - Unraid installer

Contributions welcome!
