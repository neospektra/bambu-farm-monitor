# Quick Start Guide

Get up and running with Bambu Farm Monitor in 5 minutes.

## Prerequisites

- Docker installed on your system
- At least one Bambu Lab printer on your network
- Printer's IP address and access code (see below if you don't have these)

## Step 1: Pull the Docker Image

```bash
docker pull neospektra/bambu-farm-monitor:latest
```

This downloads the latest version from Docker Hub (~500 MB).

## Step 2: Run the Container

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

**What this does:**
- `-d` - Runs in background
- `--name` - Names the container
- `-p` - Maps ports to your host
- `-v` - Creates persistent storage
- `--restart` - Auto-starts on reboot

## Step 3: Access the Web Interface

Open your browser and navigate to:

```
http://localhost:8080
```

Or from another device on your network:

```
http://YOUR_SERVER_IP:8080
```

Replace `YOUR_SERVER_IP` with your server's IP address (e.g., `192.168.1.50`).

## Step 4: Complete Setup Wizard

The setup wizard launches automatically on first run.

### 4.1 Select Number of Printers

Choose how many printers you want to monitor (you can add more later).

### 4.2 Enter Printer Information

For each printer, you'll need:

#### Printer Name
Any friendly name you want (e.g., "Farm P1S #1", "Shop X1C")

#### IP Address
**How to find:**
1. On your printer's touchscreen: **Settings → Network → Connection Info**
2. Or check your router's DHCP client list

**Example:** `192.168.1.100`

#### Access Code
**How to find:**
1. On your printer's touchscreen: **Settings → Network → MQTT**
2. If MQTT is off, turn it ON
3. Note the 8-digit code displayed

**Example:** `12345678`

**Important:** Write this down! You won't see it again without resetting.

#### Serial Number (Recommended)
**How to find:**
1. On your printer's touchscreen: **Settings → Device**
2. Look for "Serial Number" or "SN"

**Example:** `01P00A411800001`

**Note:** This is optional but recommended for reliable status updates.

### 4.3 Complete Setup

Click **"Complete Setup"** button.

The system will:
1. Save your configuration
2. Initialize video streams
3. Connect to MQTT for status updates
4. Redirect you to the dashboard

## Step 5: Verify Everything Works

### Check Video Streams ✅

You should see live camera feeds from each printer.

**If video is black:**
- Verify IP address is correct
- Check access code is correct
- Ensure printer is on and connected to network

### Check Status Updates ✅

You should see:
- Print progress (if printing)
- Temperatures (nozzle and bed)
- AMS filament colors (if equipped)
- Layer count and time remaining

**If status shows "Loading status...":**
- Verify serial number is correct
- Check MQTT is enabled on printer
- Wait 10-15 seconds for initial connection

### Check Layout Controls ✅

Try clicking different layout icons:
- Auto Grid
- 1 Column
- 2x2 Grid
- 2 Columns
- 3 Columns
- 4 Columns

Your selection is saved automatically.

## Next Steps

### Customize Your Dashboard

**Resize Windows:**
- Drag the resize handle (↘) in bottom-right corner of each printer

**Change Layout:**
- Use the layout selector buttons in the header

**Fullscreen Mode:**
- Click the fullscreen button (⛶) on any video stream

### Add More Printers

1. Click the **Settings** icon (⚙️) in the header
2. Click **"➕ Add Printer"**
3. Fill in printer details
4. Click **"💾 Save All Changes"**

### Backup Your Configuration

1. Go to Settings (⚙️)
2. Click **"📥 Export Configuration"**
3. Save the JSON file somewhere safe

You can import this file later to restore your configuration or migrate to a new system.

### Access from Other Devices

The dashboard works on:
- Desktop computers
- Tablets
- Smartphones

Just navigate to `http://YOUR_SERVER_IP:8080` from any device on your network.

### Set Up Remote Access (Optional)

If you want to access from outside your home network:

**Option 1: VPN (Recommended)**
- Set up WireGuard or Tailscale
- Connect to VPN, then access normally

**Option 2: Reverse Proxy**
- Set up nginx with authentication
- Use HTTPS with Let's Encrypt

See [Reverse Proxy Setup](Reverse-Proxy-Setup.md) for details.

## Common First-Time Issues

### "Connection Refused" Error

**Problem:** Can't access http://localhost:8080

**Solutions:**
1. Check container is running:
   ```bash
   docker ps | grep bambu
   ```

2. Check logs for errors:
   ```bash
   docker logs bambu-farm-monitor
   ```

3. Try accessing via IP instead of localhost

### Video Stream Not Loading

**Problem:** Black screen where video should be

**Solutions:**
1. Verify printer IP is correct (ping it)
2. Check access code is exactly 8 digits
3. Ensure MQTT is enabled on printer
4. Wait 30 seconds for initial connection

See [Video Stream Issues](Video-Stream-Issues.md) for more.

### Status Not Updating

**Problem:** Shows "Loading status..." forever

**Solutions:**
1. Verify serial number is correct
2. Check MQTT is enabled: Settings → Network → MQTT → ON
3. Click "Test MQTT Connection" in Settings
4. Check logs for MQTT errors

See [MQTT Connection Problems](MQTT-Connection-Problems.md) for more.

### Port Already in Use

**Problem:** Error about port 8080 in use

**Solution:** Use different ports:
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8081:8080 \
  -p 1985:1984 \
  -p 5002:5000 \
  -p 5003:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

Then access at `http://localhost:8081`

## Quick Reference Commands

### View Logs
```bash
docker logs bambu-farm-monitor
```

### Follow Logs in Real-Time
```bash
docker logs -f bambu-farm-monitor
```

### Restart Container
```bash
docker restart bambu-farm-monitor
```

### Stop Container
```bash
docker stop bambu-farm-monitor
```

### Start Container
```bash
docker start bambu-farm-monitor
```

### Remove Container (Keeps Configuration)
```bash
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# Config is preserved in bambu-config volume
```

### Update to Latest Version
```bash
docker pull neospektra/bambu-farm-monitor:latest
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# Run the docker run command again
```

## That's It!

You now have a fully functional print farm monitoring system.

**Enjoy monitoring your prints!** 🎉

## Learn More

- **[Installation Guide](Installation-Guide.md)** - Detailed installation options
- **[Finding Printer Information](Finding-Printer-Information.md)** - How to locate printer details
- **[Common Issues](Common-Issues.md)** - Troubleshooting guide
- **[API Documentation](API-Documentation.md)** - Automate with the REST API
- **[FAQ](FAQ.md)** - Frequently asked questions

## Need Help?

- **Documentation:** Browse the wiki
- **Common Issues:** [Common Issues](Common-Issues.md)
- **Discussions:** https://github.com/neospektra/bambu-farm-monitor/discussions
- **Bug Reports:** https://github.com/neospektra/bambu-farm-monitor/issues
