# Installation Scripts

This directory contains automated installation scripts for Bambu Farm Monitor.

## macOS Installation Script

### `install-macos.sh`

Automated bash script that installs Docker Desktop (or Podman Desktop) and sets up Bambu Farm Monitor on macOS.

#### Features

- ✅ Checks for existing Docker/Podman installation
- ✅ **Automatically installs Homebrew** (if not present)
- ✅ **Automatically installs Docker Desktop via Homebrew** (no manual download needed!)
- ✅ Alternatively installs Podman Desktop via Homebrew
- ✅ Pulls the latest Bambu Farm Monitor image
- ✅ Interactive printer configuration (up to 4 printers)
- ✅ Choice between Docker Compose or Docker Run deployment
- ✅ Automatic container startup and verification
- ✅ Colored output and progress indicators
- ✅ Comprehensive error handling
- ✅ Works on both Intel and Apple Silicon Macs

#### Usage

**Method 1: Direct Download and Run**

```bash
# Download the script
curl -O https://raw.githubusercontent.com/neospektra/bambu-farm-monitor/main/scripts/install-macos.sh

# Make it executable
chmod +x install-macos.sh

# Run it
./install-macos.sh
```

**Method 2: Clone Repository**

```bash
# Clone the repository
git clone https://github.com/neospektra/bambu-farm-monitor.git
cd bambu-farm-monitor

# Run the script
./scripts/install-macos.sh
```

#### What the Script Does

1. **System Check**
   - Verifies running on macOS
   - Checks for existing Docker or Podman installation

2. **Homebrew Installation** (if needed)
   - Installs Homebrew package manager
   - Configures PATH for Apple Silicon Macs

3. **Container Runtime Installation** (if needed)
   - Offers choice between Docker Desktop and Podman Desktop
   - **Automatically installs via Homebrew** (fully automated!)
   - Opens the application and waits for it to start
   - Verifies installation is working

4. **Image Download**
   - Pulls the latest `neospektra/bambu-farm-monitor:latest` image from Docker Hub

5. **Printer Configuration**
   - Optionally configures up to 4 printers interactively
   - Collects IP address, access code, name, and serial number for each printer

6. **Deployment**
   - Choice 1: Creates `docker-compose.yml` in `~/bambu-farm-monitor`
   - Choice 2: Runs container using `docker run` command
   - Starts the container with all configured printers

7. **Verification**
   - Checks if container is running
   - Provides next steps and useful commands
   - Optionally opens the dashboard in your browser

#### Prerequisites

- macOS 11 (Big Sur) or later
- Internet connection
- Administrator access

#### Troubleshooting

**Script won't run - "Permission denied"**

Make sure the script is executable:
```bash
chmod +x install-macos.sh
```

**Homebrew installation prompts for password**

This is normal. Homebrew needs administrator privileges to install.

**Docker/Podman Desktop won't start**

- Check System Preferences → Security & Privacy
- You may need to approve Docker/Podman to run
- Restart your Mac and try again

**Apple Silicon (M1/M2/M3) specific issues**

- Make sure to download the ARM64 version of Docker Desktop
- Homebrew will automatically handle this
- PATH configuration is handled automatically by the script

**Container fails to start**

Check the logs:
```bash
docker logs bambu-farm-monitor
# or
podman logs bambu-farm-monitor
```

Common causes:
- Port already in use (change ports in docker-compose.yml)
- Invalid printer configuration
- Docker/Podman not fully initialized

---

## Windows Installation Script

### `install-windows.ps1`

Automated PowerShell script that installs Docker Desktop (or Podman Desktop) and sets up Bambu Farm Monitor on Windows.

#### Features

- ✅ Checks for existing Docker/Podman installation
- ✅ **Automatically installs Docker Desktop via winget** (no manual download needed!)
- ✅ Alternatively installs Podman Desktop via winget
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
   - Verifies administrator privileges (recommended for winget)
   - Checks for existing Docker or Podman installation

2. **Installation (if needed)**
   - Offers choice between Docker Desktop and Podman Desktop
   - **Automatically installs via winget** (fully automated!)
   - Falls back to manual installation if winget is unavailable
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
- Administrator access (required for winget installation)

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

**winget not available**

- winget comes pre-installed on Windows 11 and Windows 10 (version 1809+)
- If winget is missing, the script will fall back to manual installation instructions
- Or update Windows to get winget automatically

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
- `install-synology.sh` - Synology NAS installer
- `install-unraid.sh` - Unraid installer

Contributions welcome!
