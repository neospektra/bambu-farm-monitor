# Bambu Farm Monitor

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/neospektra/bambu-farm-monitor)
![Version](https://img.shields.io/badge/version-2.0-green.svg)

A unified web-based monitoring solution for Bambu Labs 3D printers with real-time video streaming and MQTT status integration.

## Features

- **Live Video Streaming**: Low-latency WebRTC streams from up to 4 printers via go2rtc
- **Real-time Status Monitoring**: MQTT integration for live print status, temperatures, progress, and layer information
- **Setup Wizard**: Easy first-time configuration with guided setup
- **Dynamic Configuration**: Web-based interface to manage printer settings without rebuilding
- **Fullscreen Support**: Individual fullscreen capability for each camera feed
- **Persistent Configuration**: Settings persist across container restarts via volume mounts
- **Modern Responsive UI**: Clean interface with icons, gradients, and mobile support

## Quick Start

### Docker Hub (Recommended)

```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v /path/to/config:/app/config \
  neospektra/bambu-farm-monitor:latest
```

Then navigate to `http://localhost:8080` and follow the setup wizard!

### Docker Compose

```yaml
version: '3'
services:
  bambu-monitor:
    image: neospektra/bambu-farm-monitor:latest
    container_name: bambu-farm-monitor
    ports:
      - "8080:8080"  # Web UI
      - "1984:1984"  # go2rtc API
      - "5000:5000"  # Config API
      - "5001:5001"  # Status API
    volumes:
      - ./config:/app/config
    restart: unless-stopped
```

## Setup Wizard

On first run, you'll be greeted with a setup wizard that guides you through:

1. **Select Number of Printers** (1-4)
2. **Configure Each Printer**:
   - Printer Name
   - IP Address
   - MQTT Access Code
   - Serial Number (optional, required for status monitoring)
3. **Complete** - Redirects to dashboard

### Finding Your Printer Information

- **IP Address**: Check your printer's screen or router's DHCP table
- **Access Code**: Printer Settings → Network → LAN Mode → MQTT (8-digit code)
- **Serial Number**: Printer Settings → Device → Device Info (starts with 01P)

## Architecture

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       v
┌──────────────────────────┐
│   nginx (Port 8080)      │
│   - Web UI               │
│   - Reverse Proxy        │
└──────┬───────────────────┘
       │
       ├──> go2rtc (Port 1984)  ──> BambuP1SCam ──> Printer Camera
       ├──> Config API (5000)   ──> printers.json
       └──> Status API (5001)   ──> MQTT Clients ──> Printer Status
```

### Services

The container runs 4 services managed by Supervisor:

1. **go2rtc**: WebRTC streaming server for low-latency video
2. **nginx**: Web server serving UI and proxying APIs
3. **config-api** (Flask): REST API for printer configuration management
4. **status-api** (Flask): MQTT client for real-time print status

## Configuration

### Environment Variables (Optional)

Pre-configure printers using environment variables:

```bash
-e PRINTER1_IP=192.168.1.100
-e PRINTER1_CODE=12345678
-e PRINTER1_SERIAL=01P00A411800001
-e PRINTER1_NAME="My Printer"
```

Repeat for PRINTER2_, PRINTER3_, PRINTER4_

### Volume Mount

Mount `/app/config` to persist your configuration:

```bash
-v /path/to/config:/app/config
```

This stores `printers.json` which contains all your printer settings.

### Manual Configuration

You can also manually edit `/app/config/printers.json`:

```json
{
  "printers": [
    {
      "id": 1,
      "name": "Printer 1",
      "ip": "192.168.1.100",
      "access_code": "12345678",
      "serial": "01P00A411800001"
    }
  ]
}
```

## API Endpoints

### Config API (Port 5000)

- `GET /api/config/printers` - Get all printer configurations
- `PUT /api/config/printers/<id>` - Update specific printer
- `POST /api/config/printers` - Add new printer
- `POST /api/config/printers/bulk` - Bulk update (used by setup wizard)
- `GET /api/config/setup-required` - Check if setup wizard is needed
- `POST /api/config/reload` - Reload go2rtc configuration

### Status API (Port 5001)

- `GET /api/status/printers` - Get status for all printers
- `GET /api/status/printers/<id>` - Get status for specific printer
- `POST /api/status/mqtt-test/<id>` - Test MQTT connection
- `GET /api/health` - Health check

## Building from Source

```bash
git clone https://github.com/yourusername/bambu-farm-monitor.git
cd bambu-farm-monitor

docker build -t bambu-farm-monitor:latest .

docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v $(pwd)/config:/app/config \
  bambu-farm-monitor:latest
```

## Troubleshooting

### Setup Wizard Not Appearing

The wizard only appears if no printers are configured. To reset:

```bash
docker exec bambu-farm-monitor rm /app/config/printers.json
docker restart bambu-farm-monitor
```

### Camera Feeds Not Loading

1. Verify printer IPs are correct
2. Check access codes match printer settings
3. Ensure printers are on the same network as the container
4. Check container logs: `docker logs bambu-farm-monitor`

### Status Information Not Showing

1. Serial numbers are required for status monitoring
2. Use the **Test Connection** button in settings
3. Common MQTT error codes:
   - Code 4: Incorrect access code
   - Code 7: Missing/incorrect serial number
   - Timeout: Can't reach printer

### Status Flickering

This should be fixed in v2.0 with smart caching. If you still see it:
- Ensure you're running the latest version
- Check `/api/status/printers` returns consistent data

## QNAP Container Station

See [QNAP-DEPLOYMENT.md](QNAP-DEPLOYMENT.md) for detailed instructions on deploying to QNAP NAS.

## Technology Stack

- **[go2rtc](https://github.com/AlexxIT/go2rtc)**: WebRTC streaming server
- **[BambuSource2Raw](https://github.com/hisptoot/BambuSource2Raw)**: Bambu camera stream connector
- **Flask**: Python web framework for REST APIs
- **paho-mqtt**: MQTT client for printer status
- **nginx**: Web server and reverse proxy
- **Supervisor**: Process manager

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- **[AlexxIT](https://github.com/AlexxIT)** for go2rtc
- **[hisptoot](https://github.com/hisptoot)** for BambuSource2Raw
- **Bambu Lab** for making great printers

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Note**: This is an unofficial community project and is not affiliated with Bambu Lab.
