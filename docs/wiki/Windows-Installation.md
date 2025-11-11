# Windows Installation Guide

This guide will help you install and run Bambu Farm Monitor on Windows using Docker Desktop or Podman Desktop.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Automated Installation](#automated-installation)
- [Manual Installation](#manual-installation)
  - [Option 1: Docker Desktop (Recommended)](#option-1-docker-desktop-recommended)
  - [Option 2: Podman Desktop](#option-2-podman-desktop)
- [Running Bambu Farm Monitor](#running-bambu-farm-monitor)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

1. **Windows 10/11 (64-bit)** with latest updates
2. **Administrator access** on your computer
3. **WSL 2** (Windows Subsystem for Linux) - Required for Docker Desktop
4. **Virtualization enabled** in BIOS/UEFI
5. **At least 4GB RAM** available for containers
6. **Network access** to your Bambu Lab printers

### Printer Information Needed

For each printer you want to monitor, gather:
- **IP Address** (e.g., `192.168.1.100`)
- **8-digit Access Code** (from printer's MQTT settings)
- **Serial Number** (optional but recommended, found on printer)
- **Printer Name** (optional, for display purposes)

---

## Automated Installation

We provide a PowerShell script that automates the entire setup process!

### Quick Start

1. **Download the installation script:**
   - Download [`install-windows.ps1`](https://raw.githubusercontent.com/neospektra/bambu-farm-monitor/main/scripts/install-windows.ps1)
   - Or clone this repository

2. **Run the script:**
   - Right-click `install-windows.ps1` and select **"Run with PowerShell"**
   - Or open PowerShell as Administrator and run:
     ```powershell
     cd path\to\bambu-farm-monitor
     .\scripts\install-windows.ps1
     ```

3. **Follow the prompts:**
   - The script will check if Docker/Podman is installed
   - Guide you through installation if needed
   - Set up and run Bambu Farm Monitor
   - Configure your printers interactively

4. **Access your dashboard:**
   - Open your browser to: http://localhost:8080

That's it! Skip to [First-Time Setup](First-Time-Setup.md) to configure your printers.

---

## Manual Installation

If you prefer to install manually or the automated script doesn't work, follow these steps:

### Option 1: Docker Desktop (Recommended)

#### Step 1: Install WSL 2

Docker Desktop requires WSL 2. Open PowerShell as Administrator and run:

```powershell
wsl --install
```

**Restart your computer** when prompted.

#### Step 2: Download Docker Desktop

1. Visit: https://www.docker.com/products/docker-desktop/
2. Click **"Download for Windows"**
3. Run the installer (`Docker Desktop Installer.exe`)
4. Follow the installation wizard:
   - ✅ Enable **"Use WSL 2 instead of Hyper-V"** (recommended)
   - ✅ Enable **"Add shortcut to desktop"** (optional)

#### Step 3: Start Docker Desktop

1. Launch **Docker Desktop** from the Start menu
2. Accept the license agreement
3. Wait for Docker Engine to start (icon in system tray will stop animating)
4. You may need to sign in or skip sign-in

#### Step 4: Verify Installation

Open PowerShell and run:

```powershell
docker --version
docker ps
```

You should see the Docker version and an empty container list.

---

### Option 2: Podman Desktop

Podman is a Docker alternative that doesn't require Docker Desktop licensing.

#### Step 1: Download Podman Desktop

1. Visit: https://podman-desktop.io/downloads/windows
2. Download the latest Windows installer
3. Run the installer and follow the wizard

#### Step 2: Start Podman Desktop

1. Launch **Podman Desktop** from the Start menu
2. Click **"Initialize and start"** if prompted
3. Wait for the Podman machine to start

#### Step 3: Verify Installation

Open PowerShell and run:

```powershell
podman --version
podman ps
```

You should see the Podman version and an empty container list.

---

## Running Bambu Farm Monitor

Once Docker or Podman is installed, you can run Bambu Farm Monitor.

### Method 1: Using Docker Run (Quick)

Open PowerShell and run:

```powershell
docker run -d `
  --name bambu-farm-monitor `
  -p 8080:8080 `
  -p 1984:1984 `
  -p 5000:5000 `
  -p 5001:5001 `
  -v bambu-config:/app/config `
  neospektra/bambu-farm-monitor:latest
```

**For Podman users**, replace `docker` with `podman`:

```powershell
podman run -d `
  --name bambu-farm-monitor `
  -p 8080:8080 `
  -p 1984:1984 `
  -p 5000:5000 `
  -p 5001:5001 `
  -v bambu-config:/app/config `
  neospektra/bambu-farm-monitor:latest
```

### Method 2: Using Docker Compose (Recommended)

1. **Create a project folder:**
   ```powershell
   mkdir C:\bambu-farm-monitor
   cd C:\bambu-farm-monitor
   ```

2. **Download docker-compose.yml:**
   - Download from: https://raw.githubusercontent.com/neospektra/bambu-farm-monitor/main/docker-compose.yml
   - Or create the file manually (see below)

3. **Create `docker-compose.yml`:**

   ```yaml
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
       volumes:
         - bambu-config:/app/config
       restart: unless-stopped

   volumes:
     bambu-config:
   ```

4. **Start the container:**
   ```powershell
   docker compose up -d
   ```

   Or with Podman:
   ```powershell
   podman compose up -d
   ```

### Method 3: Pre-configuring Printers with Environment Variables

You can configure up to 4 printers using environment variables in docker-compose.yml:

```yaml
version: '3.8'
services:
  bambu-farm-monitor:
    image: neospektra/bambu-farm-monitor:latest
    container_name: bambu-farm-monitor
    ports:
      - "8080:8080"
      - "1984:1984"
      - "5000:5000"
      - "5001:5001"
    environment:
      - PRINTER1_IP=192.168.1.100
      - PRINTER1_CODE=12345678
      - PRINTER1_NAME=P1S Office
      - PRINTER1_SERIAL=01S00A123456789

      - PRINTER2_IP=192.168.1.101
      - PRINTER2_CODE=87654321
      - PRINTER2_NAME=X1C Workshop
      - PRINTER2_SERIAL=01X00B987654321
    volumes:
      - bambu-config:/app/config
    restart: unless-stopped

volumes:
  bambu-config:
```

Then run:
```powershell
docker compose up -d
```

---

## Access the Dashboard

Open your web browser and navigate to:

**http://localhost:8080**

You should see the Bambu Farm Monitor dashboard!

If you didn't pre-configure printers, click **"Add Printer"** to set them up via the web UI. See [First-Time Setup](First-Time-Setup.md) for detailed instructions.

---

## Useful Commands

### Check Container Status
```powershell
docker ps
# or
podman ps
```

### View Container Logs
```powershell
docker logs bambu-farm-monitor
# or
podman logs bambu-farm-monitor
```

### Stop the Container
```powershell
docker stop bambu-farm-monitor
# or
podman stop bambu-farm-monitor
```

### Start the Container
```powershell
docker start bambu-farm-monitor
# or
podman start bambu-farm-monitor
```

### Restart the Container
```powershell
docker restart bambu-farm-monitor
# or
podman restart bambu-farm-monitor
```

### Remove the Container
```powershell
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# or
podman stop bambu-farm-monitor
podman rm bambu-farm-monitor
```

### Update to Latest Version
```powershell
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
docker pull neospektra/bambu-farm-monitor:latest
# Then run the container again using Method 1 or Method 2
```

---

## Troubleshooting

### Docker Desktop won't start

**Error:** "WSL 2 installation is incomplete"
- **Solution:** Open PowerShell as Admin and run:
  ```powershell
  wsl --install
  wsl --update
  ```
  Then restart your computer.

**Error:** "Hardware assisted virtualization is not enabled"
- **Solution:** Enable virtualization in your BIOS/UEFI settings:
  1. Restart computer and enter BIOS (usually F2, F10, or Delete key)
  2. Look for "Virtualization Technology", "Intel VT-x", or "AMD-V"
  3. Enable it and save settings

### Port conflicts

**Error:** "port is already allocated"
- **Solution:** Another application is using the port. Change ports in docker-compose.yml:
  ```yaml
  ports:
    - "8081:8080"  # Changed from 8080 to 8081
    - "1985:1984"  # Changed from 1984 to 1985
  ```

### Can't access the dashboard

1. **Check if container is running:**
   ```powershell
   docker ps
   ```
   If not listed, check logs:
   ```powershell
   docker logs bambu-farm-monitor
   ```

2. **Check Windows Firewall:**
   - Open Windows Defender Firewall
   - Allow Docker Desktop or Podman Desktop through the firewall

3. **Try accessing via IP:**
   - Instead of `localhost`, try `http://127.0.0.1:8080`

### Printers not connecting

1. **Verify printer network connectivity:**
   ```powershell
   ping 192.168.1.100
   ```

2. **Check access code:**
   - Verify the 8-digit code from printer's MQTT settings
   - The code is case-sensitive

3. **Check firewall:**
   - Ensure Windows Firewall isn't blocking MQTT (port 1883)

### Container keeps restarting

Check the logs for errors:
```powershell
docker logs bambu-farm-monitor
```

Common causes:
- Invalid printer configuration
- Port conflicts
- Insufficient system resources

---

## Performance Tips

### Adjust WSL 2 Memory (Docker Desktop)

If Docker Desktop is using too much memory, create/edit `C:\Users\YourUsername\.wslconfig`:

```ini
[wsl2]
memory=4GB
processors=2
```

Restart Docker Desktop after making changes.

### Enable Auto-start

**Docker Desktop:**
- Settings → General → **"Start Docker Desktop when you log in"**

**Podman Desktop:**
- Settings → **"Start Podman machine automatically"**

---

## Next Steps

✅ **Installation complete!**

Now proceed to:
- [First-Time Setup](First-Time-Setup.md) - Configure your printers
- [Printer Configuration](Printer-Configuration.md) - Add/remove printers
- [Layout Customization](Layout-Customization.md) - Customize your dashboard
- [Common Issues](Common-Issues.md) - Troubleshooting guide

---

## Need Help?

- Check the [FAQ](FAQ.md)
- Review [Common Issues](Common-Issues.md)
- Open an issue on GitHub: https://github.com/neospektra/bambu-farm-monitor/issues
