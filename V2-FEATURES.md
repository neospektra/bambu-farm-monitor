# Bambu Labs Farm Monitor v2.0 - New Features

Version 2.0 adds powerful new features for managing your printer farm!

## 🎉 What's New in v2.0

### 1. ⚙️ Configuration Management

**Dynamic Printer Configuration** - No more rebuilding containers to change printer IPs or access codes!

- **Settings Page**: Click the ⚙️ button in the header to access the new settings page
- **Live Updates**: Edit printer IPs and access codes through the web UI
- **Auto-Reload**: Streams automatically reconnect with new settings
- **Persistent Config**: Settings are saved and persist across container restarts

**Perfect for dynamic IPs!** When your printer IPs change (DHCP), simply update them in the settings page instead of rebuilding the container.

**How to Use:**
1. Click the ⚙️ settings button in the top-right of the main page
2. Edit printer name, IP address, or access code
3. Click "Save All Changes"
4. Streams will automatically reconnect

### 2. 📊 Real-Time Job Status

**Live Print Job Information** - See what's printing on each camera!

When a printer is actively printing, a status overlay appears at the bottom of the camera feed showing:

- **📄 File Name**: Current print job file name
- **📈 Progress Bar**: Visual progress with percentage
- **🔢 Layer Info**: Current layer / Total layers
- **⏰ Time Remaining**: Estimated time to completion
- **🌡️ Temperatures**:
  - Nozzle temperature (current / target)
  - Bed temperature (current / target)

**Auto-hiding**: The overlay only appears when a print job is active and automatically hides when idle.

**Real-time Updates**: Status updates every 2 seconds via MQTT connection to your printers.

---

## 📸 Screenshots

### Main View with Job Status
When printing, you'll see real-time status overlays:
```
┌─────────────────────────────┐
│  Camera Feed                │
│                             │
│  [Status Overlay]           │
│  ├─ filename.gcode          │
│  ├─ Progress: ▓▓▓░░ 60%     │
│  ├─ Layer: 120/200          │
│  ├─ Remaining: 2h 15m       │
│  └─ 🔥 210°C  🛏️ 60°C       │
└─────────────────────────────┘
```

### Settings Page
```
⚙️ Printer Configuration

┌─────────────────────────────────┐
│ Farm P1S AMS-1      [Printer 1] │
├─────────────────────────────────┤
│ Name: [Farm P1S AMS-1        ]  │
│ IP:   [192.168.7.192         ]  │
│ Code: [32086612              ]  │
└─────────────────────────────────┘

[💾 Save All Changes]  [🔄 Reload]
```

---

## 🔧 Technical Details

### New APIs

**Configuration API** (Port 5000)
- `GET /api/config/printers` - Get all printer configs
- `PUT /api/config/printers/{id}` - Update printer config
- `POST /api/config/reload` - Reload go2rtc configuration

**Status API** (Port 5001)
- `GET /api/status/printers` - Get all printer statuses
- `GET /api/status/printers/{id}` - Get specific printer status

### MQTT Integration

The status API connects to each Bambu printer via MQTT to retrieve:
- Print progress and layer information
- Temperature data (nozzle, bed, chamber)
- Fan speeds
- Print file name and time estimates
- Print state (idle, printing, paused)

**Connection Details:**
- Protocol: MQTT over TLS (port 8883)
- Authentication: Access code as password
- Auto-reconnect on connection loss

### Architecture Updates

**New Services:**
- `config-api`: Flask API for configuration management
- `status-api`: Flask API with MQTT client for status monitoring

**Enhanced Components:**
- Nginx: Routes API calls to appropriate backend services
- Supervisor: Manages all 4 services (go2rtc, nginx, config-api, status-api)

---

## 🚀 Deployment

### Docker Compose (Updated for v2)

```yaml
version: '3.8'

services:
  bambu-farm-monitor:
    image: bambu-farm-monitor:v2
    container_name: bambu-farm-monitor
    ports:
      - "8080:8080"   # Web UI
      - "1984:1984"   # go2rtc API
      - "5000:5000"   # Configuration API
      - "5001:5001"   # Status API
    environment:
      # Printer configuration (can be changed via Settings UI)
      - PRINTER1_IP=192.168.7.192
      - PRINTER1_CODE=32086612
      - PRINTER1_NAME=Farm P1S AMS-1
      - PRINTER2_IP=192.168.4.151
      - PRINTER2_CODE=33699089
      - PRINTER2_NAME=Farm P1S AMS-2
      - PRINTER3_IP=192.168.7.140
      - PRINTER3_CODE=50741585
      - PRINTER3_NAME=Farm P1S AMS-3A
      - PRINTER4_IP=192.168.4.245
      - PRINTER4_CODE=36644208
      - PRINTER4_NAME=Farm P1S AMS-4
    volumes:
      # Optional: persist configuration across restarts
      - ./config:/app/config
    restart: unless-stopped
```

### Manual Docker Run

```bash
docker run -d \
  --name bambu-farm-monitor \
  --restart unless-stopped \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v $(pwd)/config:/app/config \
  -e PRINTER1_IP=192.168.7.192 \
  -e PRINTER1_CODE=32086612 \
  bambu-farm-monitor:v2
```

---

## 💡 Usage Tips

### Managing Dynamic IPs

If your printers get IPs via DHCP and they change frequently:

**Option 1: Use Settings Page**
- Simply update IPs via the Settings page when they change
- No container restart required

**Option 2: Static DHCP Reservations** (Recommended)
- Configure your router to assign static IPs to printers based on MAC address
- Update once in Settings, never worry again

### Monitoring Print Progress

The status overlay provides at-a-glance information:

- **Green progress bar**: Print is proceeding normally
- **Layer count**: Shows how far through the print you are
- **Time remaining**: Helps you plan when to check back
- **Temperatures**: Ensure everything is heating properly

### Troubleshooting Status

If status overlays aren't showing:

1. **Check MQTT connections**:
   - Visit http://localhost:5001/api/status/printers
   - Look for `"connected": true` for each printer

2. **Verify printer network access**:
   - Printers must be accessible from the container
   - Firewall may block MQTT port 8883

3. **Check access codes**:
   - Incorrect access codes will prevent MQTT connection
   - Update in Settings if needed

4. **View status API logs**:
   ```bash
   docker logs bambu-farm-monitor | grep status-api
   ```

---

## 🔐 Security Notes

- **Access Codes**: Stored in configuration file at `/app/config/printers.json`
- **Persistent Storage**: Mount `/app/config` volume to persist configuration
- **Network Security**: APIs run on localhost only, proxied through nginx
- **MQTT**: Uses TLS encryption for printer communication

---

## 🆙 Upgrading from v1

### What Changes

- **New Ports**: Added 5000 (config API) and 5001 (status API)
- **Settings Management**: Can now change printer config via UI
- **Status Overlays**: New feature showing print job information

### Migration Steps

1. **Stop v1 container**:
   ```bash
   docker stop bambu-farm-monitor
   docker rm bambu-farm-monitor
   ```

2. **Pull/Build v2 image**:
   ```bash
   docker build -t bambu-farm-monitor:v2 .
   ```

3. **Run v2 with new ports**:
   ```bash
   docker run ... -p 5000:5000 -p 5001:5001 ... bambu-farm-monitor:v2
   ```

4. **Optional: Mount config volume** for persistence:
   ```bash
   -v ./config:/app/config
   ```

### Backward Compatibility

- All v1 features still work exactly the same
- Environment variables still set initial configuration
- Camera feeds, fullscreen, and UI unchanged
- Port 8080 and 1984 remain the same

---

## 📦 What's Included

### v2 File Structure

```
bambu-qnap-viewer/
├── api/
│   ├── config_api.py       # Configuration management API
│   ├── status_api.py       # MQTT status monitoring API
│   └── requirements.txt    # Python dependencies
├── www/
│   ├── index.html          # Main camera grid (updated with overlays)
│   ├── style.css           # Styles (updated with overlay styles)
│   ├── settings.html       # NEW: Settings page
│   ├── settings.css        # NEW: Settings styles
│   └── settings.js         # NEW: Settings JavaScript
├── Dockerfile              # Updated with Python/Flask
├── supervisord.conf        # Updated with new APIs
├── nginx.conf              # Updated with API proxying
└── ... (other files)
```

---

## 🎯 Future Enhancements

Potential features for future versions:

- 📊 Historical print statistics
- 📧 Email/push notifications when prints complete
- 🔔 Alert system for failed prints
- 📷 Snapshot capture and timelapse creation
- 🗂️ Print queue management
- 🎨 Customizable overlay themes
- 📱 Mobile app integration

---

## 🙏 Credits

- **Flask**: Configuration and status APIs
- **paho-mqtt**: MQTT client for Bambu printer communication
- **go2rtc**: Video streaming (from v1)
- **nginx**: Reverse proxy and static file serving

---

**Enjoy the enhanced monitoring experience with v2!** 🎉
