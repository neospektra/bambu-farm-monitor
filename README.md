# Bambu Farm Monitor

A comprehensive web-based monitoring solution for multiple Bambu Lab 3D printers. Monitor your entire print farm from a single dashboard with real-time video streams and MQTT status updates.

![Version](https://img.shields.io/badge/version-3.3.9-blue.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/neospektra/bambu-farm-monitor)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### Video & Streaming
- 🎥 **Real-time Video Streams** - Live camera feeds from all your Bambu Lab printers using WebRTC via go2rtc
- 📐 **Resizable Windows** - Customize printer window sizes to your preference with drag handles
- 🖼️ **Layout Options** - Choose from multiple grid layouts (1 column, 2x2, 2 columns, 3 columns, 4 columns)
- 🎯 **Visual Layout Selector** - Icon-based layout buttons with active state highlighting
- 🔄 **Layout Persistence** - Your preferred layout is saved and restored on page reload

### Status & Monitoring
- 📊 **MQTT Status Monitoring** - Real-time print progress, temperatures, layer info, and time remaining
- 🎨 **AMS Color Display** - Visual display of loaded filament colors with active tray indicator
- 💧 **AMS Humidity** - Shows humidity percentage for AMS units
- 🌡️ **Temperature Tracking** - Real-time nozzle and bed temperatures with target values
- ⏱️ **Print Progress** - Live progress bar with layer count and time remaining

### Configuration & Management
- ⚡ **Dynamic Printer Management** - Add or remove printers on the fly (no restart required)
- 💾 **Backup & Restore** - Export and import printer configurations for easy backup or migration
- 🎯 **Setup Wizard** - Easy first-run configuration with optional config file import
- 🔄 **Auto-reconnect** - Automatic MQTT reconnection after configuration changes
- 🧪 **Test Connection** - Verify MQTT connectivity before saving

### Deployment & Platform
- 🐳 **Single Container** - All-in-one Docker container for easy deployment
- 🔧 **No External Dependencies** - Fully self-contained with bundled assets
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices
- 🏢 **NAS Compatible** - Tested on QNAP, Synology, Unraid with Docker/Podman
- 🌐 **Generic Branding** - Works with all Bambu Lab printer models (P1S, X1C, A1, etc.)

## 🚀 Quick Start

### Prerequisites

- Docker or Podman installed on your system
- Bambu Lab printer(s) on your local network
- Printer access codes and serial numbers (found in printer settings)

### Docker Hub

**All images are hosted on Docker Hub:** https://hub.docker.com/r/neospektra/bambu-farm-monitor

The image name `neospektra/bambu-farm-monitor:latest` automatically pulls from Docker Hub.

### Windows Automated Installation 🪟

**Windows users**: We have an automated installer that makes setup super easy!

```powershell
# Download and run the automated installer
.\scripts\install-windows.ps1
```

The script will:
- ✅ Check and install Docker Desktop or Podman Desktop via winget
- ✅ Download the latest image
- ✅ Configure your printers interactively
- ✅ Start the container automatically

**See the [Windows Installation Guide](docs/wiki/Windows-Installation.md) for detailed instructions.**

### Installation

#### Option 1: Docker Run (Recommended for Testing)

```bash
# Pull from Docker Hub
docker pull neospektra/bambu-farm-monitor:latest

# Run the container
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

#### Option 2: Docker Compose (Recommended for Production)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  bambu-farm-monitor:
    image: neospektra/bambu-farm-monitor:latest  # From Docker Hub
    container_name: bambu-farm-monitor
    ports:
      - "8080:8080"   # Web UI
      - "1984:1984"   # go2rtc WebRTC
      - "5000:5000"   # Config API
      - "5001:5001"   # Status API
    volumes:
      - ./config:/app/config  # Persistent config storage
    restart: unless-stopped
```

Then run:

```bash
docker-compose up -d
```

#### Option 3: Podman (for QNAP, Synology, or rootless containers)

```bash
# Pull from Docker Hub (Podman also uses Docker Hub by default)
podman pull docker.io/neospektra/bambu-farm-monitor:latest

# Run the container
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

### First-Time Setup

1. Open your browser and navigate to `http://YOUR_SERVER_IP:8080`
2. The setup wizard will automatically launch
3. Select the number of printers you want to monitor (1-N)
4. For each printer, enter:
   - **Printer Name**: Friendly name for identification
   - **IP Address**: Local network IP (e.g., `192.168.1.100`)
   - **Access Code**: 8-digit MQTT access code from printer settings
   - **Serial Number**: Printer serial number (recommended for status monitoring)
5. Click "Complete Setup" - MQTT connections will initialize automatically
6. Your dashboard will load with live streams and status updates

## 🔧 Configuration

### Finding Your Printer Information

**IP Address:**
- Check your router's DHCP client list
- Use the Bambu Studio/Handy app to view printer IP
- Assign a static IP in your router for reliability

**Access Code:**
1. On printer screen: Settings → Network → MQTT
2. Enable MQTT and note the 8-digit access code
3. Or use Bambu Studio: Printer Settings → Network

**Serial Number:**
1. Printer screen: Settings → Device
2. Or check the label on the printer
3. Format: `01P00A411800001` (typically starts with `01`)

### Managing Printers After Setup

Access the Settings page (⚙️ icon in header):
- **Add Printer**: Click "➕ Add Printer" button
- **Edit Printer**: Modify IP, access code, or serial number
- **Remove Printer**: Click "🗑️ Remove" button on any printer
- **Test Connection**: Use "🔌 Test MQTT Connection" to verify settings
- **Save Changes**: Click "💾 Save All Changes" (auto-reconnects MQTT)

### Environment Variables (Optional)

Pre-configure printers using environment variables:

```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -e PRINTER1_IP="192.168.1.100" \
  -e PRINTER1_CODE="12345678" \
  -e PRINTER1_NAME="Farm P1S #1" \
  -e PRINTER1_SERIAL="01P00A411800001" \
  -e PRINTER2_IP="192.168.1.101" \
  -e PRINTER2_CODE="87654321" \
  -e PRINTER2_NAME="Farm P1S #2" \
  -e PRINTER2_SERIAL="01P00A411800002" \
  neospektra/bambu-farm-monitor:latest
```

## 🏢 Platform-Specific Deployment

### Windows 🪟

**See the comprehensive [Windows Installation Guide](docs/wiki/Windows-Installation.md)**

**Quick automated install:**
```powershell
.\scripts\install-windows.ps1
```

The automated script handles:
- Docker Desktop or Podman Desktop installation via winget
- Image download and container configuration
- Interactive printer setup

**Manual installation:** Follow the [Windows Installation Guide](docs/wiki/Windows-Installation.md) for step-by-step Docker Desktop or Podman Desktop setup.

### QNAP NAS

1. **Container Station Method:**
   - Open Container Station
   - Go to "Images" → Search for `neospektra/bambu-farm-monitor` on Docker Hub
   - Download the `latest` tag
   - Or click "Create" → "Create Application" and paste the Docker Compose configuration above

2. **Command Line Method (SSH):**
   ```bash
   # Pull from Docker Hub
   podman pull docker.io/neospektra/bambu-farm-monitor:latest
   podman run -d \
     --name bambu-farm-monitor \
     -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
     -v /share/Container/bambu-config:/app/config \
     neospektra/bambu-farm-monitor:latest
   ```

### Synology NAS

1. Open Docker app (or Container Manager on DSM 7.2+)
2. Go to "Registry" tab
3. Search for `neospektra/bambu-farm-monitor` (searches Docker Hub by default)
4. Select the image and click "Download"
5. Choose the `latest` tag
6. Go to "Image" tab → Select the downloaded image → Click "Launch"
7. Configure port mappings:
   - Container Port 8080 → Local Port 8080
   - Container Port 1984 → Local Port 1984
   - Container Port 5000 → Local Port 5000
   - Container Port 5001 → Local Port 5001
6. Add volume: `/app/config` → `/docker/bambu-config`
7. Start the container

### Unraid

1. Go to Docker tab
2. Click "Add Container"
3. Fill in the template:
   - Repository: `neospektra/bambu-farm-monitor:latest` (pulls from Docker Hub)
   - Name: `bambu-farm-monitor`
   - Port: `8080` → `8080`
   - Port: `1984` → `1984`
   - Port: `5000` → `5000`
   - Port: `5001` → `5001`
   - Path: `/mnt/user/appdata/bambu-farm-monitor` → `/app/config`

## 📡 Ports Explained

| Port | Service | Purpose |
|------|---------|---------|
| 8080 | Web UI | Main dashboard and settings interface |
| 1984 | go2rtc | WebRTC streaming and API |
| 5000 | Config API | Printer configuration management |
| 5001 | Status API | Real-time MQTT status updates |

## 🔍 Troubleshooting

### Video streams not loading
- Verify printer IPs are correct and reachable
- Check firewall allows outbound connections from container
- Ensure access codes are correct (8 digits)
- Try refreshing the page

### Status showing "Loading status..." forever
- Verify serial numbers are entered correctly
- Check MQTT is enabled on printer
- Use "Test MQTT Connection" in Settings
- If recently added printers, status should auto-connect (v3.2+)

### Cannot delete printer
- Make sure you're running v3.2 or later
- Check browser console for errors
- Try refreshing and attempting again

### Configuration not persisting
- Ensure volume is properly mounted (`-v` flag)
- Check volume permissions
- Verify `/app/config` directory is writable

### Port conflicts
If ports are already in use, remap them:
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8081:8080 \
  -p 1985:1984 \
  -p 5002:5000 \
  -p 5003:5001 \
  neospektra/bambu-farm-monitor:latest
```

## 🔒 Security Considerations

- This application is designed for **local network use only**
- Do not expose ports directly to the internet without proper security
- Use a VPN (WireGuard, Tailscale) for remote access
- Consider using a reverse proxy (nginx, Caddy) with authentication
- Keep your printer access codes private
- Regularly update to the latest version

## 🛠️ Advanced Configuration

### Using with Reverse Proxy (nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name bambu.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Backup and Restore

**Backup:**
```bash
docker cp bambu-farm-monitor:/app/config/printers.json ./printers-backup.json
```

**Restore:**
```bash
docker cp ./printers-backup.json bambu-farm-monitor:/app/config/printers.json
docker restart bambu-farm-monitor
```

## 📝 API Documentation

### Configuration API (Port 5000)

- `GET /api/config/printers` - Get all printers
- `POST /api/config/printers` - Add new printer
- `PUT /api/config/printers/<id>` - Update printer
- `DELETE /api/config/printers/<id>` - Delete printer
- `POST /api/config/printers/bulk` - Bulk create/update printers
- `GET /api/config/setup-required` - Check if setup needed

### Status API (Port 5001)

- `GET /api/status/printers` - Get all printer statuses
- `GET /api/status/printers/<id>` - Get specific printer status
- `POST /api/status/reconnect` - Reconnect all MQTT clients
- `POST /api/status/mqtt-test/<id>` - Test MQTT connection
- `GET /api/health` - Health check

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas that need help:
- Testing on different NAS platforms
- UI/UX improvements
- Additional printer model support
- Documentation improvements
- Translations

## 📋 Changelog

### v3.3.9 (Latest)
- ✅ Added nginx sub_filter to replace go2rtc's hardcoded GitHub manifest URL with local copy
- ✅ Proxied content now references /manifest.json instead of external GitHub URL
- ✅ Eliminates CORS errors from go2rtc stream viewer

### v3.3.8
- ✅ Fixed nginx config to serve manifest.json from /var/www/html
- ✅ Added manifest.json to nginx static file whitelist

### v3.3.7
- ✅ Fixed CSS layout grid with !important flags to ensure styles apply
- ✅ Added manifest.json to resolve CORS errors from go2rtc stream
- ✅ Enhanced debug logging to show computed grid styles
- ✅ Force browser reflow after layout change
- ✅ Set default grid-template-columns on base container

### v3.3.6
- ✅ Replaced dropdown with visual icon buttons for layout selection
- ✅ Active layout highlighted with green glow effect
- ✅ Fixed layout switching functionality with proper class application
- ✅ Added console logging for debugging layout changes
- ✅ Improved mobile responsive design for layout controls

### v3.3.5
- ✅ Layout selector with multiple grid options (1 column, 2x2, 2 columns, 3 columns, 4 columns)
- ✅ Reset layout button to restore default view
- ✅ Layout preference saved to browser localStorage
- ✅ Removed overlapping window drag feature (replaced with clean grid layouts)
- ✅ Responsive layout controls that adapt to screen size

### v3.3.4
- ✅ Draggable printer windows (drag by header to reposition)
- ✅ Flexbox layout for auto-adjusting printer cards when resized
- ✅ Generic branding (removed P1S-specific references)
- ✅ Fixed AMS humidity display

### v3.3.3
- ✅ Fixed AMS color parsing to use correct MQTT structure
- ✅ Added AMS humidity percentage display with water droplet icon
- ✅ Fixed resize handle placement for better usability

### v3.3.2
- ✅ Added debug endpoint for raw MQTT data inspection
- ✅ Enhanced AMS parsing with multiple fallback attempts

### v3.3.1
- ✅ Fixed resize handle positioning
- ✅ Added debug logging for AMS data

### v3.3.0
- ✅ AMS filament color display with active tray indicator
- ✅ Backup & restore configuration (export/import JSON)
- ✅ Import configuration option in setup wizard
- ✅ Visual AMS tray status in both printing and idle states

### v3.2.0
- ✅ Fixed delete printer endpoint
- ✅ Auto MQTT reconnect in setup wizard
- ✅ Status updates now work immediately after setup

### v3.1.0
- ✅ Dynamic printer management (add/remove)
- ✅ Resizable printer windows
- ✅ Auto-reconnect MQTT after config changes
- ✅ Removed 4-printer limit

### v3.0.0
- ✅ Fixed nginx routing for index.html
- ✅ Improved setup wizard flow

### v2.0.0
- ✅ Initial public release
- ✅ Setup wizard
- ✅ MQTT status monitoring
- ✅ Multi-printer support

## 🐛 Known Issues

- Resizing windows on mobile is disabled (by design)
- Initial MQTT connection may take 5-10 seconds
- Some printers may require serial number for status monitoring

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [go2rtc](https://github.com/AlexxIT/go2rtc) - Excellent WebRTC streaming solution
- [BambuSource2Raw](https://github.com/hisptoot/BambuSource2Raw) - Bambu camera streaming protocol
- Bambu Lab community for documentation and support

## 📧 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/neospektra/bambu-farm-monitor/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/neospektra/bambu-farm-monitor/wiki)

## ⭐ Show Your Support

If you find this project useful, please consider:
- Giving it a ⭐ on GitHub
- Sharing it with other Bambu Lab users
- Contributing improvements or bug fixes
- Reporting issues to help improve the project

---

**Made with ❤️ for the 3D printing community**

## 🔗 Links

- 🐳 **Docker Hub**: https://hub.docker.com/r/neospektra/bambu-farm-monitor
- 💻 **GitHub Repository**: https://github.com/neospektra/bambu-farm-monitor
- 📖 **Documentation**: [Wiki](https://github.com/neospektra/bambu-farm-monitor/wiki)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/neospektra/bambu-farm-monitor/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
