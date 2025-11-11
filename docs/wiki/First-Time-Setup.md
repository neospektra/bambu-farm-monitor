# First-Time Setup

Complete walkthrough of the setup wizard for new installations.

## Overview

When you first access Bambu Farm Monitor, the setup wizard automatically launches to help you configure your printers. This guide walks through each step in detail.

## Accessing the Setup Wizard

### Automatic Launch

The wizard launches automatically when:
- No printers are configured
- You access the application for the first time
- Configuration file is missing or empty

### Manual Launch

If you need to re-run the wizard:
1. Delete the configuration file
2. Restart the container
3. Access the web UI

```bash
docker exec bambu-farm-monitor rm /app/config/printers.json
docker restart bambu-farm-monitor
```

## Setup Wizard Steps

### Step 1: Welcome Screen

**What You'll See:**
- Welcome message
- Brief overview of features
- Option to import existing configuration

**Actions:**
- Click **"Start Setup"** to begin
- Or click **"Import Configuration"** if you have a backup

### Step 2: Number of Printers

**What You'll See:**
- Dropdown to select number of printers (1-10+)

**Choose:**
- Select how many printers you want to monitor initially
- You can add more later in Settings

**Recommendation:**
- Start with your primary printers
- Add others after verifying the first ones work

### Step 3: Printer Details

For each printer, you'll enter four pieces of information:

#### Printer Name

**What to Enter:**
- Any friendly name you choose
- Examples:
  - "Farm P1S #1"
  - "Shop X1 Carbon"
  - "Basement Printer"
  - "Office A1 Mini"

**Tips:**
- Use descriptive names if you have multiple
- Include location or purpose
- Keep it short (displays in small spaces)

#### IP Address

**What to Enter:**
- Local network IP address
- Format: `192.168.1.100`

**How to Find:**

**Method 1: Printer Display (Easiest)**
```
Printer → Settings → Network → Connection Info
```

**Method 2: Router**
- Check DHCP client list
- Look for "Bambu" devices

**Method 3: Network Scanner**
- Use Fing app (iOS/Android)
- Or `nmap -sn 192.168.1.0/24` (Linux/Mac)

**Common Mistakes:**
- ❌ Using hostname instead of IP
- ❌ Wrong subnet (192.168.0.x vs 192.168.1.x)
- ❌ Typos in numbers

See [Finding Printer Information](Finding-Printer-Information.md) for detailed instructions.

#### Access Code

**What to Enter:**
- 8-digit MQTT password
- Example: `12345678`

**How to Find:**
```
Printer → Settings → Network → MQTT → Access Code
```

**Important Notes:**
- ⚠️ MQTT must be enabled
- ⚠️ Case sensitive (though it's only numbers)
- ⚠️ Exactly 8 digits
- ⚠️ Write it down - you won't see it again

**If You Lost It:**
1. Disable MQTT on printer
2. Re-enable MQTT
3. New code will be generated
4. Update in Bambu Farm Monitor

#### Serial Number (Recommended)

**What to Enter:**
- Printer serial number
- Format: `01P00A411800001`

**How to Find:**
```
Printer → Settings → Device → Serial Number
```

**Is This Required?**
- Not strictly required
- Highly recommended for reliable status updates
- Without it, status may not display correctly

**Common Mistakes:**
- ❌ Confusing with model number
- ❌ Including spaces or dashes
- ❌ Wrong case (use uppercase)

### Step 4: Review Configuration

**What You'll See:**
- Summary of all printers
- Name, IP, access code preview, serial number
- Edit and delete buttons

**Actions:**
- Review each printer
- Click **"Edit"** to modify any details
- Click **"Delete"** to remove a printer
- Click **"Add Another"** to add more printers

**Verification Checklist:**
- ✅ Printer names are descriptive
- ✅ IP addresses are correct
- ✅ Access codes are 8 digits
- ✅ Serial numbers match printer

### Step 5: Complete Setup

**What Happens:**
1. Configuration is saved to `/app/config/printers.json`
2. go2rtc streams are initialized
3. MQTT connections are established
4. You're redirected to the dashboard

**Initial Connection:**
- May take 10-15 seconds
- Video streams load first
- Status updates follow

## What to Expect After Setup

### Immediate (0-5 seconds)

**Dashboard Loads:**
- Printer cards appear
- Layout is set to "Auto" by default
- Loading indicators for video and status

### Within 15 seconds

**Video Streams:**
- Live camera feeds appear
- May show loading briefly
- Black screen if connection fails

**Status Updates:**
- Print progress (if currently printing)
- Temperatures (nozzle and bed)
- Connection status indicator

### Within 30 seconds

**AMS Information (if equipped):**
- Filament colors display
- Active tray indicator
- Humidity percentage

## Verification Steps

### 1. Check Video Streams

**Expected:**
- ✅ Live camera feed from each printer
- ✅ Smooth video without lag
- ✅ Clear image quality

**If Problems:**
- Black screen → Wrong IP or access code
- Loading forever → Network/firewall issue
- Laggy video → Bandwidth or WiFi signal

See [Video Stream Issues](Video-Stream-Issues.md) for troubleshooting.

### 2. Check Status Updates

**Expected:**
- ✅ "Connected" status indicator (green dot)
- ✅ Current temperatures displayed
- ✅ Print progress if currently printing
- ✅ AMS colors if equipped

**If Problems:**
- "Disconnected" → MQTT connection failed
- "Loading status..." → Wrong serial number or MQTT disabled
- No AMS colors → Check printer has AMS, update to v3.3.3+

See [MQTT Connection Problems](MQTT-Connection-Problems.md) for troubleshooting.

### 3. Test Layout Controls

**Try:**
- Click different layout buttons (1x1, 2x2, 2x1, 3x1, 4x1)
- Layouts should change immediately
- Selection is highlighted in green

**If Problems:**
- Layouts don't change → Hard refresh (Ctrl+Shift+R)
- Buttons not visible → Browser compatibility issue

### 4. Test Resizing

**Try:**
- Drag resize handle (↘) on bottom-right of printer card
- Window should resize smoothly
- Other windows adjust automatically

### 5. Test Fullscreen

**Try:**
- Click fullscreen button (⛶) on video
- Should enter fullscreen mode
- Press Esc to exit

## Post-Setup Recommendations

### 1. Create a Backup

**Immediately after successful setup:**
1. Click Settings icon (⚙️)
2. Click "Export Configuration"
3. Save JSON file to safe location

**Why:**
- Easy recovery if configuration is lost
- Migrate to new server
- Share configuration across instances

See [Backup and Restore](Backup-and-Restore.md) for details.

### 2. Set Static IPs for Printers

**Recommended to prevent IP changes:**
1. Log into your router
2. Find DHCP Reservations or Static IP settings
3. Reserve current IPs for printer MAC addresses

**Why:**
- Prevents connection loss if IP changes
- No need to reconfigure after router reboot
- More reliable long-term

### 3. Bookmark the Dashboard

**Add to browser bookmarks:**
```
http://YOUR_SERVER_IP:8080
```

**For mobile devices:**
- iOS: Add to Home Screen
- Android: Add to Home Screen

### 4. Test Connection from Other Devices

**Try accessing from:**
- Other computers on network
- Mobile phones/tablets
- Different rooms to test WiFi coverage

### 5. Customize Your Layout

**Choose a layout that fits your needs:**
- **Auto**: Responsive, adapts to screen size
- **1x1**: Single large view, focus on one printer
- **2x2**: Four printers in grid
- **2x1**: Two printers side-by-side
- **3x1**: Three columns
- **4x1**: Four columns

See [Layout Customization](Layout-Customization.md) for details.

## Common Setup Issues

### Issue: Setup Wizard Doesn't Appear

**Symptoms:**
- Dashboard shows "No printers configured"
- No wizard pops up

**Solutions:**
1. Clear browser cache
2. Hard refresh (Ctrl+Shift+R)
3. Navigate directly to `/setup.html`
4. Check browser console for errors

### Issue: Cannot Save Configuration

**Symptoms:**
- "Complete Setup" button does nothing
- Error message appears

**Solutions:**
1. Check all fields are filled
2. Verify access codes are 8 digits
3. Check browser console for errors
4. Verify volume is writable:
   ```bash
   docker exec bambu-farm-monitor ls -la /app/config
   ```

### Issue: Video Streams Don't Load

**Symptoms:**
- Black screens after setup
- Loading indicators forever

**Solutions:**
1. Verify printer IPs are correct (ping them)
2. Check access codes (exactly 8 digits)
3. Ensure printers are powered on
4. Check firewall isn't blocking ports
5. Wait 30 seconds for initial connection

See [Video Stream Issues](Video-Stream-Issues.md) for detailed troubleshooting.

### Issue: Status Shows "Loading status..."

**Symptoms:**
- Video works but status doesn't update
- Shows "Loading status..." indefinitely

**Solutions:**
1. Verify serial numbers are correct
2. Check MQTT is enabled on printers
3. Test MQTT connection in Settings
4. Check printer firmware is up to date

See [MQTT Connection Problems](MQTT-Connection-Problems.md) for detailed troubleshooting.

### Issue: Some Printers Work, Others Don't

**Symptoms:**
- Mixed success
- Some video streams work, others don't

**Solutions:**
1. Check each printer individually:
   - Ping the IP
   - Verify access code
   - Check MQTT status
2. Common cause: Copy-paste errors in configuration
3. Use "Test MQTT Connection" for each printer

## Re-Running Setup

### When to Re-Run

**Good reasons:**
- Want to start over with clean configuration
- Made mistakes during initial setup
- Testing different configurations

**Bad reasons:**
- Minor changes (use Settings instead)
- Adding one printer (use Add Printer button)

### How to Re-Run

**Method 1: Delete and Restart**
```bash
docker exec bambu-farm-monitor rm /app/config/printers.json
docker restart bambu-farm-monitor
```

**Method 2: Import Existing Configuration**
1. Settings → Export Configuration
2. Edit JSON file
3. Setup → Import Configuration

**Method 3: Full Reset**
```bash
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
docker volume rm bambu-config
# Then reinstall
```

## Importing Existing Configuration

### From JSON File

**If you have a backup:**
1. Setup wizard → "Import Configuration"
2. Select JSON file
3. Review printers
4. Click "Complete Setup"

**JSON Format:**
```json
{
  "printers": [
    {
      "name": "Farm P1S #1",
      "ip": "192.168.1.100",
      "access_code": "12345678",
      "serial_number": "01P00A411800001"
    }
  ]
}
```

### From Another Instance

**To clone configuration:**
1. Export from original instance
2. Copy JSON file to new server
3. Import during setup on new instance

## Next Steps

After successful setup:

1. **[Layout Customization](Layout-Customization.md)** - Arrange your dashboard
2. **[Printer Configuration](Printer-Configuration.md)** - Add/edit printers
3. **[Backup and Restore](Backup-and-Restore.md)** - Protect your configuration
4. **[Common Issues](Common-Issues.md)** - Troubleshoot problems

## Support

If you encounter issues during setup:
- Check [Common Issues](Common-Issues.md)
- Search [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
- Ask for help in [Support](Support.md)
