# Installation Guide

This comprehensive guide covers all installation methods for Bambu Farm Monitor.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Docker Installation](#docker-installation)
- [Docker Compose Installation](#docker-compose-installation)
- [Podman Installation](#podman-installation)
- [Platform-Specific Guides](#platform-specific-guides)
- [Post-Installation](#post-installation)

## Prerequisites

Before installing Bambu Farm Monitor, ensure you have:

### Required
- Docker or Podman installed on your system
- Network access to your Bambu Lab printer(s)
- One or more Bambu Lab printers (P1S, X1C, A1, etc.)

### Printer Information Needed
For each printer, you'll need:
- **IP Address** - Local network IP of the printer
- **Access Code** - 8-digit MQTT access code (found in printer settings)
- **Serial Number** - Printer serial number (recommended for status monitoring)

See [Finding Printer Information](Finding-Printer-Information.md) for details on locating this information.

## Docker Installation

### Step 1: Pull the Image

```bash
docker pull neospektra/bambu-farm-monitor:latest
```

### Step 2: Create Volume (Optional but Recommended)

```bash
docker volume create bambu-config
```

This creates a persistent volume to store your printer configuration.

### Step 3: Run the Container

```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Port Mapping Explained:**
- `8080` - Web UI
- `1984` - go2rtc WebRTC streaming
- `5000` - Configuration API
- `5001` - Status API (MQTT data)

### Step 4: Access the Web Interface

Open your browser and navigate to:
```
http://YOUR_SERVER_IP:8080
```

The setup wizard will automatically launch on first run.

## Docker Compose Installation

Docker Compose is recommended for production deployments as it provides better configuration management.

### Step 1: Create Docker Compose File

Create a file named `docker-compose.yml`:

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
      - ./config:/app/config
    restart: unless-stopped
    environment:
      # Optional: Pre-configure printers (see Environment Variables guide)
      # - PRINTER1_IP=192.168.1.100
      # - PRINTER1_CODE=12345678
      # - PRINTER1_NAME=Farm P1S #1
      # - PRINTER1_SERIAL=01P00A411800001
```

### Step 2: Start the Container

```bash
docker-compose up -d
```

### Step 3: View Logs (Optional)

```bash
docker-compose logs -f
```

Press `Ctrl+C` to exit log view.

### Step 4: Access the Web Interface

Navigate to `http://YOUR_SERVER_IP:8080`

## Podman Installation

Podman is ideal for rootless containers and is commonly used on QNAP and Synology NAS systems.

### Step 1: Pull the Image

```bash
podman pull docker.io/neospektra/bambu-farm-monitor:latest
```

Note: Podman requires the full registry path `docker.io/`

### Step 2: Run the Container

```bash
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

### Step 3: Enable Auto-Start (Optional)

Generate a systemd service file:

```bash
podman generate systemd --name bambu-farm-monitor --files --new
```

This creates a `.service` file that can be used with systemd.

## Platform-Specific Guides

For detailed platform-specific instructions, see:

- **[QNAP Installation](QNAP-Installation.md)** - Container Station and CLI methods
- **[Synology Installation](Synology-Installation.md)** - Docker app and Container Manager
- **[Unraid Installation](Unraid-Installation.md)** - Community Applications and templates

## Post-Installation

### 1. Complete Setup Wizard

On first access, you'll be greeted with the setup wizard:

1. Select the number of printers
2. Enter printer details (name, IP, access code, serial number)
3. Click "Complete Setup"
4. MQTT connections initialize automatically

See [First Time Setup](First-Time-Setup.md) for detailed instructions.

### 2. Verify Functionality

Check that all components are working:

- ✅ **Video Streams** - You should see live camera feeds
- ✅ **Status Updates** - Print status, temperatures, and progress display
- ✅ **AMS Colors** - Filament colors and active tray indicator (if applicable)

### 3. Customize Layout

Use the layout selector to arrange your printer views:
- Auto Grid (default)
- 1 Column
- 2x2 Grid
- 2 Columns
- 3 Columns
- 4 Columns

See [Layout Customization](Layout-Customization.md) for details.

### 4. Backup Configuration

Once configured, create a backup:

1. Go to Settings (⚙️ icon)
2. Click "Export Configuration"
3. Save the JSON file in a safe location

See [Backup and Restore](Backup-and-Restore.md) for more information.

## Updating

### Docker

```bash
docker pull neospektra/bambu-farm-monitor:latest
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# Run the docker run command again
```

### Docker Compose

```bash
docker-compose pull
docker-compose up -d
```

### Podman

```bash
podman pull docker.io/neospektra/bambu-farm-monitor:latest
podman stop bambu-farm-monitor
podman rm bambu-farm-monitor
# Run the podman run command again
```

## Troubleshooting

If you encounter issues during installation:

- **Port conflicts**: See [Network Configuration](Network-Configuration.md)
- **Permission errors**: Check volume mount permissions
- **Can't access web UI**: Verify firewall settings
- **Video streams not working**: See [Video Stream Issues](Video-Stream-Issues.md)

For more help, see [Common Issues](Common-Issues.md) or [Debugging Guide](Debugging-Guide.md).

## Next Steps

- **[First Time Setup](First-Time-Setup.md)** - Configure your printers
- **[Printer Configuration](Printer-Configuration.md)** - Add or modify printers
- **[Finding Printer Information](Finding-Printer-Information.md)** - Locate printer details
