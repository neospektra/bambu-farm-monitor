# QNAP Installation Guide

Complete guide for installing Bambu Farm Monitor on QNAP NAS systems.

## Overview

QNAP NAS devices support Docker and Podman through Container Station. This guide covers both GUI and command-line installation methods.

## Prerequisites

### System Requirements

**Minimum:**
- QNAP NAS with Container Station support
- QTS 4.3.4+ or QuTS hero h4.5.0+
- 2 GB RAM (4 GB recommended)
- 1 GB free disk space

**Recommended Models:**
- TS-x53 series or newer
- TS-x64 series
- TVS series
- Any model with Intel or AMD CPU

**Compatible Container Platforms:**
- Container Station (Docker/LXC)
- Podman (command-line)

### Network Requirements

- QNAP NAS on same network as Bambu printers
- Static IP for NAS (recommended)
- Ports 8080, 1984, 5000, 5001 available

## Method 1: Container Station GUI (Easiest)

### Step 1: Install Container Station

1. Open **App Center** on your QNAP
2. Search for **"Container Station"**
3. Click **Install**
4. Wait for installation to complete
5. Open **Container Station**

### Step 2: Search for Image on Docker Hub

1. In Container Station, click **"Images"** in left sidebar
2. Click **"Pull"** button at top
3. In the search box, enter:
   ```
   neospektra/bambu-farm-monitor
   ```
4. Click **"Pull"** next to the result
5. Select **"latest"** tag
6. Click **"Pull"** to download

The image will download (~500 MB). This may take 5-10 minutes.

### Step 3: Create Container

Once the image is downloaded:

1. Click **"Containers"** in left sidebar
2. Click **"Create"** button
3. Select **"neospektra/bambu-farm-monitor:latest"** from the list
4. Click **"Create Container"**

### Step 4: Configure Container

**Basic Settings:**
- **Name:** `bambu-farm-monitor`
- **CPU Limit:** 2 cores (or leave unlimited)
- **Memory Limit:** 1 GB (or leave unlimited)

**Network:**
- **Network Mode:** Bridge
- **Port Forwarding:** Add these mappings:

| Service Port | Container Port | Protocol |
|--------------|----------------|----------|
| 8080 | 8080 | TCP |
| 1984 | 1984 | TCP |
| 5000 | 5000 | TCP |
| 5001 | 5001 | TCP |

Click **"+"** to add each port.

**Shared Folders (Very Important!):**

1. Click **"Advanced Settings"**
2. Go to **"Shared Folders"** tab
3. Click **"Add"**
4. Configure:
   - **Volume/Shared Folder:** `/Container/bambu-config` (or create new)
   - **Mount Point:** `/app/config`
   - **Permission:** Read/Write

This ensures your configuration persists across container restarts.

**Auto-start:**
- Enable **"Auto start"** checkbox

**Resource Limits (Optional):**
- Set CPU and memory limits if needed

### Step 5: Create and Start

1. Click **"Create"** button
2. Container will be created and started automatically
3. Wait 10-15 seconds for services to initialize

### Step 6: Access Web Interface

Open your browser and navigate to:

```
http://QNAP_IP:8080
```

Replace `QNAP_IP` with your NAS IP address (e.g., `http://192.168.1.50:8080`)

The setup wizard should appear automatically.

## Method 2: Docker Compose (Recommended for Advanced Users)

### Step 1: Enable SSH

1. Go to **Control Panel** → **Network & File Services** → **Telnet / SSH**
2. Enable **"Allow SSH connection"**
3. Click **"Apply"**

### Step 2: Connect via SSH

```bash
ssh admin@QNAP_IP
```

Enter your QNAP admin password.

### Step 3: Create Docker Compose File

```bash
# Create directory for compose file
mkdir -p /share/Container/bambu-monitor
cd /share/Container/bambu-monitor

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
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
    volumes:
      - /share/Container/bambu-config:/app/config
    restart: unless-stopped
EOF
```

### Step 4: Deploy

```bash
docker-compose up -d
```

### Step 5: Verify

```bash
docker-compose logs -f
```

Press `Ctrl+C` to exit logs.

Access at `http://QNAP_IP:8080`

## Method 3: Podman CLI (Alternative)

QNAP also supports Podman for rootless containers.

### Step 1: Enable SSH

Same as Method 2, Step 1.

### Step 2: Connect via SSH

```bash
ssh admin@QNAP_IP
```

### Step 3: Pull Image

```bash
podman pull docker.io/neospektra/bambu-farm-monitor:latest
```

### Step 4: Run Container

```bash
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v /share/Container/bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

### Step 5: Verify

```bash
podman ps
podman logs bambu-farm-monitor
```

Access at `http://QNAP_IP:8080`

## Post-Installation

### Complete Setup Wizard

1. Navigate to `http://QNAP_IP:8080`
2. Follow the setup wizard
3. Enter printer information:
   - Printer name
   - IP address
   - Access code (8 digits)
   - Serial number

See [Finding Printer Information](Finding-Printer-Information.md) if you need help.

### Verify Functionality

Check that everything works:

- ✅ **Video Streams** - Live camera feeds
- ✅ **Status Updates** - Print progress, temps
- ✅ **AMS Colors** - Filament colors (if equipped)

### Create Backup

1. Click Settings icon (⚙️)
2. Click **"Export Configuration"**
3. Save JSON file to a safe location

## QNAP-Specific Tips

### 1. Use Container Station Auto-Start

Enable auto-start in Container Station so the container launches when QNAP boots:

1. Container Station → Containers
2. Right-click container → **"Settings"**
3. Enable **"Auto start"**

### 2. Set Static IP for QNAP

Recommended to prevent IP changes:

1. **Control Panel** → **Network & File Services** → **Network Settings**
2. Select network adapter → **"Edit"**
3. Set **"Use static IP"**
4. Enter IP, subnet, gateway, DNS

### 3. Create Dedicated Shared Folder

For better organization:

1. **Control Panel** → **Shared Folders**
2. Click **"Create"** → **"Shared Folder"**
3. Name: `bambu-config`
4. Use this in volume mount: `/share/bambu-config:/app/config`

### 4. Configure Firewall

If you have QNAP firewall enabled:

1. **Control Panel** → **Security** → **Security Level**
2. Click **"Firewall"** → **"Edit Rules"**
3. Add rules to allow:
   - TCP 8080 (Web UI)
   - TCP 1984 (go2rtc)
   - TCP 5000 (Config API)
   - TCP 5001 (Status API)

### 5. Resource Monitor

Monitor container resource usage:

1. Open **Resource Monitor** app
2. Go to **"Docker"** tab
3. View CPU, memory, network usage

Or via SSH:
```bash
docker stats bambu-farm-monitor
```

### 6. Schedule Automatic Restarts

Create a scheduled task to restart weekly:

1. **Control Panel** → **System** → **Task Scheduler**
2. Click **"Create"** → **"User-defined script"**
3. Configure:
   - **Task Name:** Restart Bambu Monitor
   - **Schedule:** Weekly, Sunday 3:00 AM
   - **Command:**
     ```bash
     docker restart bambu-farm-monitor
     ```

### 7. Snapshot Backup

If using QNAP snapshot feature:

1. Include `/share/Container/bambu-config` in snapshot policy
2. Schedule regular snapshots
3. Easy rollback if needed

## Updating

### Via Container Station GUI

1. Container Station → Images
2. Click **"Pull"** → Search for `neospektra/bambu-farm-monitor`
3. Pull **"latest"** tag
4. Go to Containers → Stop `bambu-farm-monitor`
5. Right-click → **"Recreate"**
6. Select new image → **"Create"**

### Via Docker Compose

```bash
cd /share/Container/bambu-monitor
docker-compose pull
docker-compose up -d
```

### Via Podman CLI

```bash
podman pull docker.io/neospektra/bambu-farm-monitor:latest
podman stop bambu-farm-monitor
podman rm bambu-farm-monitor
# Run the podman run command again
```

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker logs bambu-farm-monitor
# or
podman logs bambu-farm-monitor
```

**Common causes:**
- Port conflicts (another service using 8080)
- Volume permission issues
- Insufficient RAM

**Solutions:**
```bash
# Check what's using port 8080
netstat -tulpn | grep 8080

# Check available RAM
free -h

# Restart Container Station
# Control Panel → Applications → Container Station → Restart
```

### Cannot Access Web UI

**Check container is running:**
```bash
docker ps | grep bambu
```

**Check QNAP firewall:**
- Ensure ports 8080, 1984, 5000, 5001 are allowed

**Try from QNAP itself:**
```bash
curl http://localhost:8080
```

### Video Streams Not Working

**Verify network connectivity:**
```bash
# From QNAP SSH
ping PRINTER_IP

# From inside container
docker exec bambu-farm-monitor ping PRINTER_IP
```

**Check Container Station network mode:**
- Should be "Bridge" not "NAT"

### Configuration Not Persisting

**Verify volume mount:**
```bash
docker inspect bambu-farm-monitor | grep Mounts -A 10
```

**Check folder permissions:**
```bash
ls -la /share/Container/bambu-config
```

**Fix permissions if needed:**
```bash
chmod 777 /share/Container/bambu-config
```

### High CPU Usage

**Normal:** Video transcoding uses 10-20% CPU per stream

**Solutions:**
- Limit active streams (close printers not being watched)
- Upgrade QNAP model with better CPU
- Use Intel QSV hardware acceleration (advanced)

## QNAP Model-Specific Notes

### ARM-Based Models (Not Supported)

Unfortunately, ARM-based QNAP models (TS-x28, TS-x31, etc.) are **not compatible** because:
- go2rtc requires x86_64 architecture
- No ARM builds available

**Supported:** Intel and AMD CPU models only

### Low-RAM Models (<2GB)

Models with less than 2GB RAM may struggle:
- Limit to 1-2 printers maximum
- Set memory limits in Container Station
- Consider upgrading RAM if possible

### QTS vs QuTS hero

Both QTS and QuTS hero support Container Station:
- **QTS:** Standard QNAP OS
- **QuTS hero:** ZFS-based OS

Instructions are the same for both.

## Next Steps

- **[Complete Setup Wizard](First-Time-Setup.md)**
- **[Add More Printers](Printer-Configuration.md)**
- **[Backup Configuration](Backup-and-Restore.md)**
- **[API Documentation](API-Documentation.md)**

## Related Guides

- **[Installation Guide](Installation-Guide.md)** - General installation
- **[Synology Installation](Synology-Installation.md)** - Synology NAS
- **[Common Issues](Common-Issues.md)** - Troubleshooting
- **[Performance Optimization](Performance-Optimization.md)** - Improve performance

## Support

For QNAP-specific issues:
- Check QNAP Container Station logs
- Verify QTS version is up to date
- Ask in [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
