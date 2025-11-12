# Synology Installation Guide

Complete guide for installing Bambu Farm Monitor on Synology NAS systems.

## Overview

Synology NAS devices support Docker through the Container Manager package (formerly Docker package). This guide covers both GUI and command-line installation methods.

## Prerequisites

### System Requirements

**Minimum:**
- Synology NAS with Docker support
- DSM 7.0+ (Container Manager) or DSM 6.0+ (Docker)
- 2 GB RAM (4 GB recommended)
- 1 GB free disk space

**Compatible Models:**
- Plus series (DS920+, DS1520+, DS1821+, etc.)
- Value series with 64-bit CPU (DS220+, DS420+, etc.)
- XS/XS+ series
- RS series (RackStation)

**NOT Compatible:**
- ARM-based models (DS218, DS418, etc.)
- J series (DS218j, DS418j, etc.)
- Models without 64-bit Intel/AMD CPU

**Check Compatibility:**
- Intel or AMD x86_64 CPU required
- Check [Synology Compatibility List](https://www.synology.com/en-us/dsm/packages/Docker)

### Network Requirements

- Synology NAS on same network as Bambu printers
- Static IP for NAS (recommended)
- Ports 8080, 1984, 5000, 5001 available

## Method 1: Container Manager GUI (Easiest)

### Step 1: Install Container Manager

**For DSM 7.0+:**
1. Open **Package Center**
2. Search for **"Container Manager"**
3. Click **Install**
4. Wait for installation to complete
5. Open **Container Manager**

**For DSM 6.x:**
1. Open **Package Center**
2. Search for **"Docker"**
3. Click **Install**
4. Open **Docker**

### Step 2: Create Shared Folder for Configuration

1. Open **Control Panel** → **Shared Folder**
2. Click **Create** → **Create Shared Folder**
3. Configure:
   - **Name:** `docker`
   - **Location:** Select volume (usually volume1)
4. Click **OK**
5. Create subdirectory via File Station:
   - Navigate to `/docker/`
   - Create folder: `bambu-config`

### Step 3: Download Image

**DSM 7.0+ (Container Manager):**
1. Open **Container Manager**
2. Go to **Registry** tab
3. Search for: `bambu-farm-monitor`
4. Find **neospektra/bambu-farm-monitor**
5. Click **Download**
6. Select tag: **latest**
7. Click **Select**

**DSM 6.x (Docker):**
1. Open **Docker**
2. Go to **Registry** tab
3. Search for: `bambu-farm-monitor`
4. Double-click **neospektra/bambu-farm-monitor**
5. Select tag: **latest**
6. Click **Select**

Wait for download to complete (~500 MB). Check **Image** tab to see progress.

### Step 4: Create Container

**After image downloads:**

1. Go to **Image** tab
2. Select **neospektra/bambu-farm-monitor:latest**
3. Click **Launch**

### Step 5: Configure Container

**General Settings:**
- **Container Name:** `bambu-farm-monitor`
- **Enable auto-restart:** ✅ (recommended)

Click **Advanced Settings**

**Port Settings:**

Click **"+"** to add each port:

| Local Port | Container Port | Type |
|------------|---------------|------|
| 8080 | 8080 | TCP |
| 1984 | 1984 | TCP |
| 5000 | 5000 | TCP |
| 5001 | 5001 | TCP |

**Volume Settings:**

Click **Add Folder** for each:

| Folder | Mount Path | Mode |
|--------|-----------|------|
| docker/bambu-config | /app/config | Read/Write |

**Important:** Volume mount is critical for configuration persistence!

**Network:**
- Use **bridge** network (default)

**Environment:**
- No environment variables needed (optional pre-configuration)

**Resource Limits (Optional):**
- **CPU priority:** Medium
- **Memory limit:** 1024 MB (or leave unlimited)

### Step 6: Create and Start

1. Review all settings
2. Click **Apply**
3. Container is created and started automatically
4. Check **Container** tab - status should be **Running**

### Step 7: Access Web Interface

Open your browser and navigate to:

```
http://SYNOLOGY_IP:8080
```

Replace `SYNOLOGY_IP` with your NAS IP address (e.g., `http://192.168.1.50:8080`)

The setup wizard should appear automatically.

## Method 2: Docker Compose (Recommended for Advanced Users)

### Step 1: Enable SSH

1. **Control Panel** → **Terminal & SNMP**
2. Enable **"Enable SSH service"**
3. Set port (default 22)
4. Click **Apply**

### Step 2: Connect via SSH

```bash
ssh admin@SYNOLOGY_IP
```

Enter your Synology admin password.

### Step 3: Create Directory Structure

```bash
# Navigate to docker folder
cd /volume1/docker

# Create directories
mkdir -p bambu-monitor
cd bambu-monitor
mkdir -p config
```

### Step 4: Create Docker Compose File

```bash
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
      - /volume1/docker/bambu-monitor/config:/app/config
    restart: unless-stopped
    environment:
      - TZ=America/New_York  # Optional: Set your timezone
EOF
```

**Adjust paths if needed:**
- If using volume2: `/volume2/docker/bambu-monitor/config`
- Check your volume name: `df -h`

### Step 5: Deploy

```bash
# Pull image
docker-compose pull

# Start container
docker-compose up -d

# Verify running
docker-compose ps
```

### Step 6: Check Logs

```bash
# View logs
docker-compose logs -f

# Press Ctrl+C to exit
```

Access at `http://SYNOLOGY_IP:8080`

## Method 3: Docker CLI

### Step 1: Enable SSH

Same as Method 2, Step 1.

### Step 2: Connect via SSH

```bash
ssh admin@SYNOLOGY_IP
```

### Step 3: Create Configuration Directory

```bash
# Create config directory
sudo mkdir -p /volume1/docker/bambu-config
sudo chmod 777 /volume1/docker/bambu-config
```

### Step 4: Pull Image

```bash
sudo docker pull neospektra/bambu-farm-monitor:latest
```

### Step 5: Run Container

```bash
sudo docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v /volume1/docker/bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

### Step 6: Verify

```bash
# Check container is running
sudo docker ps | grep bambu

# View logs
sudo docker logs bambu-farm-monitor
```

Access at `http://SYNOLOGY_IP:8080`

## Post-Installation

### Complete Setup Wizard

1. Navigate to `http://SYNOLOGY_IP:8080`
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

## Synology-Specific Tips

### 1. Use Task Scheduler for Auto-Backup

**Create scheduled backup:**

1. **Control Panel** → **Task Scheduler**
2. **Create** → **Scheduled Task** → **User-defined script**
3. Configure:
   - **Task:** Bambu Backup Daily
   - **User:** root
   - **Schedule:** Daily, 02:00
   - **User-defined script:**
     ```bash
     docker exec bambu-farm-monitor cat /app/config/printers.json > \
       /volume1/docker/backups/bambu-config-$(date +\%F).json
     ```
4. Click **OK**

**Test task:**
- Right-click task → **Run**
- Check `/volume1/docker/backups/` for backup file

### 2. Set Static IP for Synology

Recommended to prevent IP changes:

1. **Control Panel** → **Network** → **Network Interface**
2. Select network adapter (e.g., LAN 1)
3. Click **Edit**
4. **IPv4** → Select **Use manual configuration**
5. Enter:
   - **IP Address:** `192.168.1.50` (example)
   - **Subnet Mask:** `255.255.255.0`
   - **Gateway:** `192.168.1.1`
   - **DNS Server:** `8.8.8.8` (or your router)
6. Click **OK**

### 3. Configure Firewall Rules

If firewall is enabled:

1. **Control Panel** → **Security** → **Firewall**
2. Click **Edit Rules**
3. Click **Create** → **Select from a list of built-in applications**
4. Or create custom rule:
   - **Ports:** TCP 8080, 1984, 5000, 5001
   - **Source IP:** All or specific subnet
   - **Action:** Allow
5. Click **OK**

### 4. Create Dedicated User (Optional)

For better security:

1. **Control Panel** → **User & Group**
2. **Create** user: `bambu`
3. Assign to `docker` group
4. Set folder permissions: Read/Write on `/docker/bambu-config`

**Update docker-compose.yml:**
```yaml
services:
  bambu-farm-monitor:
    user: "1026:100"  # UID:GID of bambu user
    # ... rest of config
```

### 5. Use Synology DDNS (Optional)

For remote access:

1. **Control Panel** → **External Access** → **DDNS**
2. **Add** → Select **Synology**
3. Configure hostname: `your-name.synology.me`
4. Enable **External Access** for ports 8080

**Security Warning:** Use VPN or reverse proxy with authentication for external access. Don't expose directly to internet.

### 6. Monitor Resource Usage

**Via Container Manager:**
1. Open **Container Manager**
2. Go to **Container** tab
3. Select `bambu-farm-monitor`
4. View CPU, Memory, Network stats in real-time

**Via Resource Monitor:**
1. Open **Resource Monitor**
2. Go to **Performance** tab
3. View overall system usage

### 7. Log Rotation

Configure log rotation to prevent disk usage:

1. **Control Panel** → **Task Scheduler**
2. **Create** → **Scheduled Task** → **User-defined script**
3. Configure:
   - **Task:** Docker Log Cleanup
   - **User:** root
   - **Schedule:** Weekly, Sunday 03:00
   - **Script:**
     ```bash
     docker exec bambu-farm-monitor sh -c "truncate -s 0 /var/log/*.log"
     ```

### 8. Hyper Backup Integration

Include configuration in Hyper Backup:

1. Open **Hyper Backup**
2. Create or edit backup task
3. Include folder: `docker/bambu-config`
4. Schedule regular backups

## Updating

### Via Container Manager GUI

**DSM 7.0+:**
1. **Container Manager** → **Registry**
2. Search for `neospektra/bambu-farm-monitor`
3. Click **Download** → Select **latest**
4. Go to **Container** tab
5. Stop `bambu-farm-monitor`
6. Click **Action** → **Reset**
7. Container restarts with new image

**DSM 6.x:**
1. **Docker** → **Registry**
2. Search and download new image
3. **Container** tab → Stop container
4. **Action** → **Clear** → Restart

### Via Docker Compose

```bash
# SSH into Synology
ssh admin@SYNOLOGY_IP

# Navigate to compose directory
cd /volume1/docker/bambu-monitor

# Pull latest image
sudo docker-compose pull

# Recreate container
sudo docker-compose up -d

# Verify
sudo docker-compose ps
```

### Via Docker CLI

```bash
# SSH into Synology
ssh admin@SYNOLOGY_IP

# Pull latest image
sudo docker pull neospektra/bambu-farm-monitor:latest

# Stop and remove old container
sudo docker stop bambu-farm-monitor
sudo docker rm bambu-farm-monitor

# Run new container (same command as installation)
sudo docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v /volume1/docker/bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
sudo docker logs bambu-farm-monitor
```

**Common causes:**
- Port conflicts
- Volume permission issues
- Insufficient RAM

**Solutions:**
```bash
# Check port usage
sudo netstat -tulpn | grep 8080

# Check volume permissions
sudo ls -la /volume1/docker/bambu-config

# Fix permissions
sudo chmod 777 /volume1/docker/bambu-config

# Check available RAM
free -h
```

### Cannot Access Web UI

**From Synology itself:**
```bash
# SSH into Synology
curl http://localhost:8080
```

**If works locally but not remotely:**
- Check firewall rules
- Verify Synology IP is correct
- Try from device on same network

**Check container is running:**
```bash
sudo docker ps | grep bambu
```

### Video Streams Not Working

**Verify network connectivity:**
```bash
# From Synology
ping PRINTER_IP

# From inside container
sudo docker exec bambu-farm-monitor ping PRINTER_IP
```

**Check container network mode:**
- Should be **bridge** (default)
- If using custom network, ensure printers are reachable

### Configuration Not Persisting

**Verify volume mount:**
```bash
sudo docker inspect bambu-farm-monitor | grep -A 10 Mounts
```

**Should see:**
```json
"Destination": "/app/config",
"Source": "/volume1/docker/bambu-config"
```

**Check folder exists:**
```bash
ls -la /volume1/docker/bambu-config/
```

**Check printers.json:**
```bash
cat /volume1/docker/bambu-config/printers.json
```

### High CPU Usage

**Normal:** Video transcoding uses 10-20% CPU per stream

**If excessive:**
- Check number of active streams
- Verify no errors in logs
- Check for network issues causing retries

**Monitor in real-time:**
```bash
sudo docker stats bambu-farm-monitor
```

### Permission Denied Errors

**Fix volume permissions:**
```bash
# Set ownership to Synology users group
sudo chown -R admin:users /volume1/docker/bambu-config

# Set permissions
sudo chmod -R 755 /volume1/docker/bambu-config
```

## Synology Model-Specific Notes

### Plus Series (Recommended)

Models: DS920+, DS1520+, DS1821+, DS920+, etc.

**Performance:**
- Excellent for 4-8 printers
- Intel CPUs with good transcoding
- 4-8 GB RAM standard

### Value Series

Models: DS220+, DS420+, DS720+

**Performance:**
- Good for 2-4 printers
- Lower-end Intel CPUs
- 2 GB RAM (consider upgrade)

### ARM Models (NOT Supported)

Models: DS218, DS418, DS218play, etc.

**Why not supported:**
- ARM architecture incompatible
- go2rtc requires x86_64
- No ARM builds available

**Check your CPU:**
```bash
uname -m
# Should output: x86_64
```

### DSM 6 vs DSM 7

**DSM 6:**
- Uses **Docker** package
- Older UI
- Works fine with Bambu Farm Monitor

**DSM 7:**
- Uses **Container Manager** package
- Modern UI with better features
- Recommended for new installs

Both versions fully supported.

## Next Steps

- **[Complete Setup Wizard](First-Time-Setup.md)**
- **[Add More Printers](Printer-Configuration.md)**
- **[Backup Configuration](Backup-and-Restore.md)**
- **[API Documentation](API-Documentation.md)**

## Related Guides

- **[Installation Guide](Installation-Guide.md)** - General installation
- **[QNAP Installation](QNAP-Installation.md)** - QNAP NAS
- **[Common Issues](Common-Issues.md)** - Troubleshooting
- **[Performance Optimization](Performance-Optimization.md)** - Improve performance

## Support

For Synology-specific issues:
- Check Container Manager logs
- Verify DSM version is up to date
- Ask in [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
