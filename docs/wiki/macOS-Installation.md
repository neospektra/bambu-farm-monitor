# macOS Installation Guide

This guide will help you install and run Bambu Farm Monitor on macOS using Docker Desktop or Podman Desktop.

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

1. **macOS 11 (Big Sur) or later**
2. **Administrator access** on your computer
3. **At least 4GB RAM** available for containers
4. **Network access** to your Bambu Lab printers
5. **Internet connection** for downloading components

### Printer Information Needed

For each printer you want to monitor, gather:
- **IP Address** (e.g., `192.168.1.100`)
- **8-digit Access Code** (from printer's MQTT settings)
- **Serial Number** (optional but recommended, found on printer)
- **Printer Name** (optional, for display purposes)

---

## Automated Installation

We provide a bash script that automates the entire setup process using Homebrew!

### Quick Start

1. **Download the installation script:**
   ```bash
   curl -O https://raw.githubusercontent.com/neospektra/bambu-farm-monitor/main/scripts/install-macos.sh
   chmod +x install-macos.sh
   ```

2. **Run the script:**
   ```bash
   ./install-macos.sh
   ```

3. **The script will automatically:**
   - Check if Homebrew is installed (installs if needed)
   - Check if Docker/Podman is installed
   - Install Docker Desktop via Homebrew if needed (fully automated!)
   - Download the latest Bambu Farm Monitor image
   - Set up and run the container
   - Configure your printers interactively

4. **Access your dashboard:**
   - Open your browser to: http://localhost:8080

That's it! Skip to [First-Time Setup](First-Time-Setup.md) to configure your printers.

---

## Manual Installation

If you prefer to install manually or the automated script doesn't work, follow these steps:

### Option 1: Docker Desktop (Recommended)

#### Step 1: Install Homebrew (if not already installed)

Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**For Apple Silicon Macs (M1/M2/M3):**
After installation, add Homebrew to your PATH:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### Step 2: Install Docker Desktop via Homebrew

```bash
brew install --cask docker
```

Or download manually:
1. Visit: https://www.docker.com/products/docker-desktop/
2. Click **"Download for Mac"** (choose Intel or Apple Silicon)
3. Open the `.dmg` file
4. Drag Docker to Applications

#### Step 3: Start Docker Desktop

1. Open **Docker** from Applications or Spotlight
2. Accept the license agreement if prompted
3. Wait for Docker Engine to start (whale icon in menu bar)
4. You may need to enter your password to grant permissions

#### Step 4: Verify Installation

Open Terminal and run:

```bash
docker --version
docker ps
```

You should see the Docker version and an empty container list.

---

### Option 2: Podman Desktop

Podman is a Docker alternative that's free and doesn't require licensing.

#### Step 1: Install via Homebrew (Easiest)

```bash
brew install --cask podman-desktop
```

**Or download manually:**
1. Visit: https://podman-desktop.io/downloads/macos
2. Download the `.dmg` file
3. Open and drag to Applications

#### Step 2: Start Podman Desktop

1. Open **Podman Desktop** from Applications
2. Click **"Initialize and start"** if prompted
3. Wait for the Podman machine to start

#### Step 3: Verify Installation

Open Terminal and run:

```bash
podman --version
podman ps
```

You should see the Podman version and an empty container list.

---

## Running Bambu Farm Monitor

Once Docker or Podman is installed, you can run Bambu Farm Monitor.

### Method 1: Using Docker Run (Quick)

Open Terminal and run:

```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v bambu-config:/app/config \
  neospektra/bambu-farm-monitor:latest
```

**For Podman users**, replace `docker` with `podman`:

```bash
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v bambu-config:/app/config \
  neospektra/bambu-farm-monitor:latest
```

### Method 2: Using Docker Compose (Recommended)

1. **Create a project folder:**
   ```bash
   mkdir ~/bambu-farm-monitor
   cd ~/bambu-farm-monitor
   ```

2. **Create `docker-compose.yml`:**

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

3. **Start the container:**
   ```bash
   docker compose up -d
   ```

   Or with Podman:
   ```bash
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
```bash
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
```bash
docker ps
# or
podman ps
```

### View Container Logs
```bash
docker logs bambu-farm-monitor
# or
podman logs bambu-farm-monitor
```

### Stop the Container
```bash
docker stop bambu-farm-monitor
# or
podman stop bambu-farm-monitor
```

### Start the Container
```bash
docker start bambu-farm-monitor
# or
podman start bambu-farm-monitor
```

### Restart the Container
```bash
docker restart bambu-farm-monitor
# or
podman restart bambu-farm-monitor
```

### Remove the Container
```bash
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# or
podman stop bambu-farm-monitor
podman rm bambu-farm-monitor
```

### Update to Latest Version
```bash
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
docker pull neospektra/bambu-farm-monitor:latest
# Then run the container again using Method 1 or Method 2
```

---

## Troubleshooting

### Homebrew installation fails

**Error:** Permission denied or "sudo: command not found"
- **Solution:** Ensure you're running the Homebrew install command as shown (it will prompt for password)
- On Apple Silicon, make sure to add Homebrew to your PATH as shown in Step 1

### Docker Desktop won't start

**Error:** "Docker Desktop requires macOS 11.0 or later"
- **Solution:** Update your macOS to Big Sur (11.0) or later

**Docker Desktop stuck on "Starting...":**
- Quit Docker Desktop completely (Cmd+Q)
- Open Activity Monitor and force quit any Docker processes
- Restart Docker Desktop
- If still stuck, try: `rm -rf ~/Library/Group\ Containers/group.com.docker`

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
   ```bash
   docker ps
   ```
   If not listed, check logs:
   ```bash
   docker logs bambu-farm-monitor
   ```

2. **Check macOS Firewall:**
   - System Preferences → Security & Privacy → Firewall
   - Ensure Docker is allowed

3. **Try accessing via IP:**
   - Instead of `localhost`, try `http://127.0.0.1:8080`

### Printers not connecting

1. **Verify printer network connectivity:**
   ```bash
   ping 192.168.1.100
   ```

2. **Check access code:**
   - Verify the 8-digit code from printer's MQTT settings
   - The code is case-sensitive

3. **Check firewall:**
   - Ensure macOS Firewall isn't blocking MQTT (port 1883)

### Container keeps restarting

Check the logs for errors:
```bash
docker logs bambu-farm-monitor
```

Common causes:
- Invalid printer configuration
- Port conflicts
- Insufficient system resources

### Apple Silicon (M1/M2/M3) Issues

**Docker runs but container won't start:**
- Make sure you downloaded the ARM64/Apple Silicon version of Docker Desktop
- Check with: `docker info | grep Architecture`
- Should show: `Architecture: aarch64`

---

## Performance Tips

### Adjust Docker Desktop Resources

If Docker Desktop is using too much memory:

1. Open Docker Desktop
2. Go to **Preferences** (gear icon)
3. Select **Resources**
4. Adjust **Memory** and **CPU** limits
5. Click **Apply & Restart**

### Enable Auto-start

**Docker Desktop:**
- Preferences → General → **"Start Docker Desktop when you log in"**

**Podman Desktop:**
- Preferences → **"Start Podman machine automatically"**

### Reduce Memory Usage

If you want to minimize memory usage:
- Set Docker Desktop to use 2-3GB RAM (in Resources)
- Stop other unused containers: `docker ps -a` then `docker rm <container>`

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
