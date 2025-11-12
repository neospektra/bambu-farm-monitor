# Unraid Installation Guide

Complete guide for installing Bambu Farm Monitor on Unraid servers.

## Overview

Unraid has excellent Docker support through its Community Applications (CA) system. This guide covers both the Unraid web UI method and command-line installation.

## Prerequisites

### System Requirements

**Minimum:**
- Unraid 6.8+ (6.10+ recommended)
- 2 GB RAM (4 GB recommended)
- 1 GB free disk space on Docker image location

**Recommended:**
- Unraid 6.11+ or 6.12+
- Community Applications plugin installed
- Intel or AMD x86_64 CPU (ARM not supported)

### Network Requirements

- Unraid server on same network as Bambu printers
- Static IP for Unraid (recommended)
- Ports 8080, 1984, 5000, 5001 available

### Install Community Applications

If not already installed:

1. Go to **Plugins** tab
2. Click **Install Plugin**
3. Enter: `https://raw.githubusercontent.com/Squidly271/community.applications/master/plugins/community.applications.plg`
4. Click **Install**
5. Wait for installation to complete

## Method 1: Community Applications (Easiest)

**Note:** Template may not be available yet in CA. Use Method 2 (Template URL) or Method 3 (Command Line) instead.

### Step 1: Search Community Applications

1. Click **Apps** tab
2. Search for: `bambu farm monitor`
3. Look for **Bambu Farm Monitor** by neospektra
4. Click on the application

### Step 2: Configure Template

**Basic Settings:**
- **Name:** `bambu-farm-monitor` (or customize)
- **Repository:** `neospektra/bambu-farm-monitor:latest`
- **Network Type:** `bridge`

**Port Mappings:**

| Host Port | Container Port | Description |
|-----------|---------------|-------------|
| 8080 | 8080 | Web UI |
| 1984 | 1984 | go2rtc streaming |
| 5000 | 5000 | Config API |
| 5001 | 5001 | Status API |

**Path Mappings:**

| Host Path | Container Path | Access Mode |
|-----------|---------------|-------------|
| `/mnt/user/appdata/bambu-farm-monitor` | `/app/config` | Read/Write |

**Auto-start:**
- Enable **Autostart** (recommended)

### Step 3: Apply and Start

1. Click **Apply**
2. Unraid pulls the Docker image
3. Container starts automatically
4. Check **Docker** tab - status should be **Started**

### Step 4: Access Web Interface

```
http://UNRAID_IP:8080
```

Replace `UNRAID_IP` with your Unraid server IP (e.g., `http://192.168.1.50:8080`)

## Method 2: Custom Template URL

If not in CA yet, add via custom template:

### Step 1: Add Custom Template

1. Go to **Docker** tab
2. At bottom, click **Add Container**
3. Select **Template Repository:** (leave default)
4. Or manually configure:

**Name:** `bambu-farm-monitor`

**Overview:**
```
Monitor multiple Bambu Lab 3D printers with live video streams,
real-time status updates, and AMS filament tracking.
```

**Repository:** `neospektra/bambu-farm-monitor:latest`

**Docker Hub URL:** `https://hub.docker.com/r/neospektra/bambu-farm-monitor`

**Icon URL:**
```
https://raw.githubusercontent.com/neospektra/bambu-farm-monitor/main/frontend/public/logo192.png
```

**Network Type:** `bridge`

**Console Shell:** `bash`

### Step 2: Add Ports

Click **Add another Path, Port, Variable, Label or Device**

Select **Port:**

**Config Type:** Port
**Name:** Web UI
**Container Port:** 8080
**Host Port:** 8080
**Protocol:** TCP

Repeat for:
- go2rtc: 1984 → 1984 TCP
- Config API: 5000 → 5000 TCP
- Status API: 5001 → 5001 TCP

### Step 3: Add Volume

**Config Type:** Path
**Name:** Config
**Container Path:** `/app/config`
**Host Path:** `/mnt/user/appdata/bambu-farm-monitor`
**Access Mode:** Read/Write

### Step 4: Apply

1. Click **Apply**
2. Wait for image download
3. Container starts automatically

## Method 3: Docker Command Line (Advanced)

### Step 1: Open Terminal

**Via Web UI:**
1. Click **Terminal** icon in top-right
2. Opens web-based terminal

**Via SSH:**
```bash
ssh root@UNRAID_IP
```

### Step 2: Create Configuration Directory

```bash
# Create appdata directory
mkdir -p /mnt/user/appdata/bambu-farm-monitor

# Set permissions
chmod 777 /mnt/user/appdata/bambu-farm-monitor
```

### Step 3: Pull Image

```bash
docker pull neospektra/bambu-farm-monitor:latest
```

### Step 4: Run Container

```bash
docker run -d \
  --name=bambu-farm-monitor \
  --net=bridge \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v /mnt/user/appdata/bambu-farm-monitor:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

### Step 5: Verify

```bash
# Check container is running
docker ps | grep bambu

# View logs
docker logs bambu-farm-monitor
```

The container should now appear in the **Docker** tab.

## Post-Installation

### Complete Setup Wizard

1. Navigate to `http://UNRAID_IP:8080`
2. Follow the setup wizard
3. Enter printer information:
   - Printer name
   - IP address
   - Access code (8 digits)
   - Serial number

See [Finding Printer Information](Finding-Printer-Information.md) if you need help.

### Verify Functionality

- ✅ **Video Streams** - Live camera feeds
- ✅ **Status Updates** - Print progress, temps
- ✅ **AMS Colors** - Filament colors (if equipped)

### Create Backup

1. Click Settings icon (⚙️)
2. Click **"Export Configuration"**
3. Save JSON file to a safe location

## Unraid-Specific Tips

### 1. Use User Scripts for Automated Backups

**Install User Scripts plugin:**
1. **Plugins** → **Install Plugin**
2. Enter: `https://raw.githubusercontent.com/Squidly271/user.scripts/master/plugins/user.scripts.plg`
3. Click **Install**

**Create backup script:**
1. **Settings** → **User Scripts**
2. Click **Add New Script**
3. Name: `Backup Bambu Config`
4. Click **Edit Script**
5. Add:
```bash
#!/bin/bash
BACKUP_DIR="/mnt/user/backups/bambu"
DATE=$(date +%F)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Export configuration via API
curl -s -o "$BACKUP_DIR/bambu-config-$DATE.json" \
  http://localhost:5000/api/config/export

# Or copy file directly
cp /mnt/user/appdata/bambu-farm-monitor/printers.json \
  "$BACKUP_DIR/bambu-config-direct-$DATE.json"

# Delete backups older than 30 days
find "$BACKUP_DIR" -name "bambu-config-*.json" -mtime +30 -delete

echo "Backup completed: $DATE"
```

**Schedule:**
- Click **Schedule** dropdown
- Select **Daily** or **Weekly**
- Choose time (e.g., 2:00 AM)
- Click **Apply**

**Test:**
- Click **Run Script**
- Check `/mnt/user/backups/bambu/` for backup file

### 2. Set Static IP for Unraid

**Via Network Settings:**
1. **Settings** → **Network Settings**
2. Select **eth0** (or your interface)
3. **IPv4 address assignment:** Static
4. Enter:
   - **IPv4 address:** `192.168.1.50`
   - **IPv4 subnet mask:** `255.255.255.0`
   - **IPv4 gateway:** `192.168.1.1`
   - **DNS server:** `8.8.8.8` or your router
5. Click **Apply**

### 3. Configure Reverse Proxy with Nginx Proxy Manager

**Install Nginx Proxy Manager:**
1. **Apps** → Search for **Nginx Proxy Manager**
2. Install from Community Applications
3. Configure at `http://UNRAID_IP:81`

**Add Proxy Host:**
1. Default credentials: `admin@example.com` / `changeme`
2. **Proxy Hosts** → **Add Proxy Host**
3. Configure:
   - **Domain Names:** `bambu.yourdomain.com`
   - **Scheme:** http
   - **Forward Hostname:** `UNRAID_IP`
   - **Forward Port:** 8080
   - **Enable WebSockets:** ✅
4. **SSL** tab → Request SSL certificate

**Access via domain:**
```
https://bambu.yourdomain.com
```

See [Reverse Proxy Setup](Reverse-Proxy-Setup.md) for details.

### 4. Pin Docker Image Version

**To prevent auto-updates breaking things:**

1. **Docker** tab
2. Click container icon → **Edit**
3. Change repository from:
   ```
   neospektra/bambu-farm-monitor:latest
   ```
   to specific version:
   ```
   neospektra/bambu-farm-monitor:3.3.9
   ```
4. Click **Apply**

**When ready to update:**
- Change back to `:latest`
- Click **Force Update**

### 5. Use Fix Common Problems Plugin

**Install plugin:**
1. **Plugins** → **Install Plugin**
2. Search for **Fix Common Problems**
3. Install and run

**Benefits:**
- Detects port conflicts
- Checks Docker image updates
- Identifies permission issues
- Monitors array health

### 6. Monitor Resource Usage

**Via Unraid UI:**
1. **Dashboard** tab
2. View CPU, RAM, Network in real-time
3. **Docker** tab shows per-container stats

**Via Statistics plugin (if installed):**
- Detailed graphs and history
- Per-container resource tracking

**Via command line:**
```bash
# Real-time stats
docker stats bambu-farm-monitor

# Check memory usage
free -h

# Check CPU usage
top
```

### 7. Use Appdata Backup Plugin

**Backup entire appdata:**
1. Install **CA Backup / Restore Appdata** plugin
2. **Settings** → **CA Backup / Restore Appdata**
3. Schedule backups of `/mnt/user/appdata/`
4. Includes `bambu-farm-monitor` automatically

### 8. Create Custom Dashboard Tile

**Using Dashboard plugin:**
1. Install **Homepage Dashboard** or **Organizr**
2. Add custom tile for Bambu Farm Monitor
3. Set URL: `http://UNRAID_IP:8080`
4. Add icon and description

## Updating

### Via Docker Tab

1. **Docker** tab
2. Find `bambu-farm-monitor`
3. Click **Check for Updates** (top right)
4. If update available, click container icon → **Force Update**
5. Container restarts with new image

**Or manually:**
1. Click container icon → **Edit**
2. Toggle **Force Update** = ON
3. Click **Apply**

### Via Command Line

```bash
# Pull latest image
docker pull neospektra/bambu-farm-monitor:latest

# Stop container
docker stop bambu-farm-monitor

# Remove container
docker rm bambu-farm-monitor

# Recreate with same settings (or use Web UI)
docker run -d \
  --name=bambu-farm-monitor \
  --net=bridge \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v /mnt/user/appdata/bambu-farm-monitor:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Or via Web UI:**
- The container should reappear in Docker tab
- Click **Start**

## Troubleshooting

### Container Won't Start

**Check logs:**
1. **Docker** tab
2. Click container icon → **Logs**
3. Look for error messages

**Via command line:**
```bash
docker logs bambu-farm-monitor
```

**Common causes:**
- Port conflicts (another container using 8080)
- Volume permission issues
- Insufficient RAM
- Wrong network mode

**Solutions:**
```bash
# Check port usage
netstat -tulpn | grep 8080

# Check volume permissions
ls -la /mnt/user/appdata/bambu-farm-monitor/

# Fix permissions
chmod 777 /mnt/user/appdata/bambu-farm-monitor/

# Check available RAM
free -h
```

### Cannot Access Web UI

**Check container status:**
1. **Docker** tab
2. Status should be **Started** (green)

**Test from Unraid itself:**
```bash
curl http://localhost:8080
```

**If works locally but not remotely:**
- Check firewall/VPN settings
- Verify Unraid IP is correct
- Ensure you're on same network

**Check container logs:**
```bash
docker logs bambu-farm-monitor | grep error
```

### Video Streams Not Working

**Network connectivity test:**
```bash
# From Unraid
ping PRINTER_IP

# From inside container
docker exec bambu-farm-monitor ping PRINTER_IP
```

**Check network mode:**
1. **Docker** tab → Click container → **Edit**
2. **Network Type** should be **bridge** (default)

**Common issues:**
- VLANs separating Unraid from printers
- Wrong printer IP address
- Firewall blocking access
- MQTT not enabled on printer

### Configuration Not Persisting

**Check volume mount:**
```bash
docker inspect bambu-farm-monitor | grep -A 10 Mounts
```

**Should see:**
```json
"Destination": "/app/config",
"Source": "/mnt/user/appdata/bambu-farm-monitor"
```

**Verify directory exists:**
```bash
ls -la /mnt/user/appdata/bambu-farm-monitor/
```

**Check config file:**
```bash
cat /mnt/user/appdata/bambu-farm-monitor/printers.json
```

**If directory empty after setup:**
- Volume may not be mounted correctly
- Recreate container with proper volume mapping

### High CPU/RAM Usage

**Normal behavior:**
- 10-20% CPU per active video stream
- 200-400 MB RAM baseline
- Spikes during transcoding

**If excessive:**
```bash
# Monitor in real-time
docker stats bambu-farm-monitor

# Check for errors
docker logs bambu-farm-monitor | grep -i error
```

**Solutions:**
- Limit number of simultaneous streams
- Close idle printer windows
- Increase RAM allocation if available
- Check network isn't causing retries

### Port Conflicts

**Error:** "port is already allocated"

**Find what's using the port:**
```bash
netstat -tulpn | grep 8080
```

**Solutions:**
1. Stop conflicting container
2. Or use different host port:
   - Edit container
   - Change host port 8080 → 8081
   - Access at `http://UNRAID_IP:8081`

## Unraid-Specific Features

### Array Management

**Configuration persists across:**
- Array stops/starts
- Server reboots
- Docker image location changes

**Location:** `/mnt/user/appdata/` is part of user shares, protected by parity.

### Docker Image Location

**By default:** `/mnt/user/system/docker/docker.img`

**To change:**
1. **Settings** → **Docker**
2. Stop Docker service
3. Change **Docker vDisk location**
4. Start Docker service

**Bambu config unaffected** - stored in appdata, separate from Docker image.

### VMs and Docker Networking

**If running VMs:**
- Ensure bridge (br0) is configured properly
- VMs and Docker can coexist
- May need custom network if complex setup

**Check bridge:**
```bash
ip addr show br0
```

### Mover and Cache

**If using cache drive:**
- Appdata typically on cache for performance
- Mover runs nightly to move to array
- Config is small, stays on cache

**Pin appdata to cache:**
1. **Shares** tab
2. Select **appdata** share
3. **Use cache:** Yes or Prefer
4. **Mover:** Use cache (don't move to array)

## Template XML (For CA Submission)

If you want to submit to Community Applications:

```xml
<?xml version="1.0"?>
<Container version="2">
  <Name>bambu-farm-monitor</Name>
  <Repository>neospektra/bambu-farm-monitor:latest</Repository>
  <Registry>https://hub.docker.com/r/neospektra/bambu-farm-monitor</Registry>
  <Network>bridge</Network>
  <Shell>bash</Shell>
  <Privileged>false</Privileged>
  <Support>https://github.com/neospektra/bambu-farm-monitor/discussions</Support>
  <Project>https://github.com/neospektra/bambu-farm-monitor</Project>
  <Overview>Monitor multiple Bambu Lab 3D printers with live video streams, real-time status updates, and AMS filament tracking. Simple web interface for managing your print farm.</Overview>
  <Category>Tools: Productivity: Status:Stable</Category>
  <WebUI>http://[IP]:[PORT:8080]</WebUI>
  <Icon>https://raw.githubusercontent.com/neospektra/bambu-farm-monitor/main/frontend/public/logo192.png</Icon>
  <Config Name="Web UI" Target="8080" Default="8080" Mode="tcp" Description="Web interface" Type="Port" Display="always" Required="true" Mask="false">8080</Config>
  <Config Name="go2rtc" Target="1984" Default="1984" Mode="tcp" Description="Video streaming" Type="Port" Display="always" Required="true" Mask="false">1984</Config>
  <Config Name="Config API" Target="5000" Default="5000" Mode="tcp" Description="Configuration API" Type="Port" Display="always" Required="true" Mask="false">5000</Config>
  <Config Name="Status API" Target="5001" Default="5001" Mode="tcp" Description="Status API" Type="Port" Display="always" Required="true" Mask="false">5001</Config>
  <Config Name="Config" Target="/app/config" Default="/mnt/user/appdata/bambu-farm-monitor" Mode="rw" Description="Configuration storage" Type="Path" Display="always" Required="true" Mask="false">/mnt/user/appdata/bambu-farm-monitor</Config>
</Container>
```

Save as `bambu-farm-monitor.xml` and submit to CA repository.

## Next Steps

- **[Complete Setup Wizard](First-Time-Setup.md)**
- **[Add More Printers](Printer-Configuration.md)**
- **[Backup Configuration](Backup-and-Restore.md)**
- **[API Documentation](API-Documentation.md)**

## Related Guides

- **[Installation Guide](Installation-Guide.md)** - General installation
- **[QNAP Installation](QNAP-Installation.md)** - QNAP NAS
- **[Synology Installation](Synology-Installation.md)** - Synology NAS
- **[Common Issues](Common-Issues.md)** - Troubleshooting

## Support

For Unraid-specific issues:
- Check Docker logs in Web UI
- Verify Docker service is enabled
- Ask in [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
- Or Unraid forums (Docker Support section)
