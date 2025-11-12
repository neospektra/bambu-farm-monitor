# MQTT Connection Problems

Comprehensive troubleshooting guide for MQTT connectivity and status update issues.

## Overview

Bambu Farm Monitor uses MQTT to receive real-time status updates from your printers. This guide helps diagnose and fix MQTT connection problems.

## How MQTT Works

**Architecture:**
```
Printer MQTT Broker → Bambu Farm Monitor → Status API → Web UI
```

**Components:**
1. **Printer:** Runs MQTT broker on port 1883 (local) or 8883 (TLS)
2. **Bambu Farm Monitor:** Subscribes to printer topics
3. **Status API:** Exposes status via REST API (port 5001)
4. **Web UI:** Polls Status API and displays information

**Authentication:** Uses 8-digit access code (same as video streaming)

## Common Issues

### Issue 1: Status Shows "Loading status..."

**Symptoms:**
- Status area shows "Loading status..." indefinitely
- Video stream works fine
- No status updates appear

**Causes:**
1. MQTT not enabled on printer
2. Wrong access code
3. Wrong serial number
4. Network blocking MQTT port
5. MQTT client not connected

**Diagnosis:**

```bash
# Test 1: Check MQTT port
nc -zv PRINTER_IP 1883

# Test 2: Check container logs for MQTT
docker logs bambu-farm-monitor 2>&1 | grep -i mqtt

# Test 3: Check Status API
curl http://localhost:5001/api/status/printers/1
```

**Solutions:**

**Enable MQTT on Printer:**
1. On printer touchscreen: **Settings → Network → MQTT**
2. Toggle **MQTT** to **ON**
3. Note the 8-digit **Access Code**
4. Click **OK**

**Verify Access Code:**
```bash
# Access code must be exactly 8 digits
# Get from printer: Settings → Network → MQTT → Access Code

# Update in Bambu Farm Monitor:
# Settings → Edit printer → Enter correct access code
```

**Verify Serial Number:**
```bash
# Get from printer: Settings → Device → Serial Number
# Format: 01P00A411800001 (15 characters)

# Update in Bambu Farm Monitor:
# Settings → Edit printer → Enter correct serial number
```

**Check Network Connectivity:**
```bash
# Ping printer
ping PRINTER_IP

# Test MQTT port (1883)
telnet PRINTER_IP 1883
# Should connect (press Ctrl+] then 'quit')

# If timeout, check firewall
```

**Check Container Logs:**
```bash
# Look for MQTT connection errors
docker logs bambu-farm-monitor 2>&1 | grep -i "mqtt.*error\|mqtt.*failed"

# Look for successful connections
docker logs bambu-farm-monitor 2>&1 | grep -i "mqtt.*connected"
```

### Issue 2: Status Shows "Disconnected"

**Symptoms:**
- Status explicitly shows "Disconnected" with red dot
- Was working before
- Video stream may still work

**Causes:**
1. MQTT connection lost
2. Printer rebooted
3. Network interruption
4. Access code changed
5. MQTT disabled on printer

**Diagnosis:**

```bash
# Check printer is reachable
ping PRINTER_IP

# Check MQTT port
nc -zv PRINTER_IP 1883

# Check when last connected
docker logs bambu-farm-monitor 2>&1 | grep "MQTT.*disconnect" | tail -5

# Test MQTT connection manually
docker exec bambu-farm-monitor python3 << 'EOF'
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        print("✅ MQTT connection successful")
    else:
        print(f"❌ Connection failed with code {rc}")
    client.disconnect()

client = mqtt.Client()
client.username_pw_set("bblp", "YOUR_ACCESS_CODE")
client.on_connect = on_connect
client.connect("PRINTER_IP", 1883, 60)
client.loop_start()
time.sleep(5)
EOF
```

**Solutions:**

**Reconnect via Settings:**
1. Click **Settings** (⚙️)
2. Find the printer
3. Click **"Test MQTT Connection"**
4. Should show success or error
5. Click **"Save All Changes"** to force reconnect

**Restart Container:**
```bash
# Quick fix - restart container
docker restart bambu-farm-monitor

# Check logs after restart
docker logs -f bambu-farm-monitor
```

**Verify MQTT is Still Enabled:**
```bash
# On printer: Settings → Network → MQTT
# Should be ON

# If OFF:
# - Turn ON
# - Note new access code (may change)
# - Update in Bambu Farm Monitor
```

**Check for IP Change:**
```bash
# Verify printer IP hasn't changed
ping PRINTER_IP

# If changed, update in Settings
# Or set static IP on printer/router
```

### Issue 3: Some Status Updates Missing

**Symptoms:**
- Temperature updates but progress doesn't
- Progress updates but AMS colors don't show
- Partial status information

**Causes:**
1. Incomplete MQTT message parsing
2. Printer not sending all topics
3. Network packet loss
4. Firmware differences

**Diagnosis:**

```bash
# Check Status API response
curl http://localhost:5001/api/status/printers/1 | jq .

# Should include:
# - status (idle, printing, paused, etc.)
# - nozzle_temp, bed_temp
# - layer_num, total_layer_num
# - mc_percent (progress)
# - ams data (if equipped)

# Check MQTT messages in logs
docker logs bambu-farm-monitor 2>&1 | grep "MQTT message"
```

**Solutions:**

**Force Status Refresh:**
```bash
# Reconnect MQTT
curl -X POST http://localhost:5001/api/status/reconnect

# Check status again
curl http://localhost:5001/api/status/printers/1 | jq .
```

**Update to Latest Version:**
```bash
# Newer versions have better MQTT parsing
docker pull neospektra/bambu-farm-monitor:latest
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# Recreate container
```

**Check Printer Firmware:**
```bash
# On printer: Settings → Device → Firmware Version
# Ensure firmware is up to date
# Older firmware may send different MQTT format
```

### Issue 4: AMS Filament Colors Not Showing

**Symptoms:**
- Status updates work
- Temperatures show
- But AMS section is empty or shows "No AMS"

**Causes:**
1. Printer doesn't have AMS
2. AMS not sending MQTT data
3. AMS disconnected from printer
4. Old version of Bambu Farm Monitor

**Diagnosis:**

```bash
# Check if printer has AMS
# Physical check - AMS unit connected?

# Check Status API for AMS data
curl http://localhost:5001/api/status/printers/1 | jq '.ams'

# Should show:
{
  "tray_now": "0",  # Active tray
  "tray": [
    {
      "id": "0",
      "name": "PLA",
      "color": "FF0000FF",
      "type": "PLA"
    },
    # ... more trays
  ]
}

# Check logs for AMS messages
docker logs bambu-farm-monitor 2>&1 | grep -i "ams"
```

**Solutions:**

**Verify AMS is Connected:**
1. Check physical connection between printer and AMS
2. On printer: Settings → AMS
3. Should show AMS status

**Force MQTT Reconnect:**
```bash
# Reconnect to get fresh AMS data
curl -X POST http://localhost:5001/api/status/reconnect
```

**Update Version:**
```bash
# AMS support added in v3.3.3+
# Check version
docker inspect bambu-farm-monitor | grep -i version

# Update if old
docker pull neospektra/bambu-farm-monitor:latest
```

**Check AMS MQTT Topic:**
```bash
# Advanced: Subscribe to MQTT directly to verify AMS data
# Install mosquitto-clients:
# apt-get install mosquitto-clients

# Subscribe to printer
mosquitto_sub -h PRINTER_IP -p 1883 \
  -u bblp -P ACCESS_CODE \
  -t "device/SERIAL_NUMBER/report" \
  -v

# Should see JSON messages including AMS data
```

### Issue 5: Temperature Always Shows 0°C

**Symptoms:**
- Status connected
- Progress updates work
- But nozzle_temp and bed_temp show 0

**Causes:**
1. Printer idle (not heating)
2. MQTT message parsing issue
3. Temperature not in MQTT payload

**Diagnosis:**

```bash
# Check if printer is actually idle
# Idle printers don't heat

# Check Status API
curl http://localhost:5001/api/status/printers/1 | jq '{nozzle_temp, bed_temp}'

# Expected output:
{
  "nozzle_temp": 220,
  "bed_temp": 60
}

# If 0, check MQTT messages
docker logs bambu-farm-monitor 2>&1 | grep "nozzle_temp\|bed_temp"
```

**Solutions:**

**Start a Print:**
- Temperatures only reported during heating/printing
- When idle, temperatures may be 0 or ambient

**Check MQTT Topics:**
```bash
# Temperature in 'report' topic
# Verify subscription
docker logs bambu-farm-monitor 2>&1 | grep "Subscribed to.*report"
```

**If Always 0 During Print:**
- Report as bug with logs
- May be firmware-specific issue

### Issue 6: Print Progress Not Updating

**Symptoms:**
- Progress stuck at 0% or old value
- Layer count doesn't increment
- Print is actually running

**Causes:**
1. MQTT not receiving progress updates
2. Print started before MQTT connected
3. Serial number mismatch

**Diagnosis:**

```bash
# Check current status
curl http://localhost:5001/api/status/printers/1 | jq '{status, mc_percent, layer_num, total_layer_num}'

# Expected during print:
{
  "status": "printing",
  "mc_percent": 45,
  "layer_num": 150,
  "total_layer_num": 300
}

# Check MQTT logs for progress messages
docker logs bambu-farm-monitor 2>&1 | grep "mc_percent"
```

**Solutions:**

**Reconnect MQTT:**
```bash
# Force reconnect to get fresh state
curl -X POST http://localhost:5001/api/status/reconnect

# Refresh browser
# Progress should update
```

**Verify Serial Number:**
```bash
# Wrong serial = subscribes to wrong MQTT topic
# Get from printer: Settings → Device → Serial Number
# Update in Bambu Farm Monitor if wrong
```

**Restart Print Monitoring:**
```bash
# Pause and resume print
# Or restart container
docker restart bambu-farm-monitor
```

### Issue 7: MQTT Connects Then Disconnects

**Symptoms:**
- Brief connection shown
- Immediately disconnects
- Loops repeatedly

**Causes:**
1. Wrong access code
2. Certificate validation issues (if using TLS)
3. Network instability
4. Too many MQTT clients

**Diagnosis:**

```bash
# Watch connection attempts
docker logs -f bambu-farm-monitor 2>&1 | grep -i mqtt

# Look for pattern:
# "MQTT connected"
# "MQTT disconnected" (immediately after)

# Check MQTT return code
# 0 = success
# 1 = protocol version mismatch
# 4 = bad username/password
# 5 = not authorized
```

**Solutions:**

**Regenerate Access Code:**
1. On printer: Settings → Network → MQTT
2. Toggle OFF then ON
3. New access code generated
4. Update in Bambu Farm Monitor
5. Click "Save All Changes"

**Check MQTT Client Limit:**
- Bambu printers may limit concurrent MQTT connections
- Disconnect other MQTT clients (Bambu Studio, Handy, etc.)
- Try again

**Use Local MQTT (Not Cloud):**
```bash
# Bambu Farm Monitor uses local MQTT (port 1883)
# Not cloud MQTT
# Ensure printer is on local network
```

### Issue 8: Multiple Printers, Only One Works

**Symptoms:**
- Printer 1 status works fine
- Printer 2,3,4... don't update

**Causes:**
1. Network/firewall blocking some printers
2. Different firmware versions
3. Configuration errors
4. Resource limits

**Diagnosis:**

```bash
# Check each printer individually
for id in 1 2 3 4; do
  echo "Printer $id:"
  curl -s http://localhost:5001/api/status/printers/$id | jq '{status, connected}'
done

# Test MQTT connection for each
for ip in 192.168.1.100 192.168.1.101 192.168.1.102; do
  echo "Testing $ip:"
  nc -zv $ip 1883
done

# Check logs for all printers
docker logs bambu-farm-monitor 2>&1 | grep "Printer.*MQTT"
```

**Solutions:**

**Test Each Printer:**
1. Settings → Each printer → "Test MQTT Connection"
2. Note which succeed/fail
3. Focus on failed ones

**Verify Configuration:**
```bash
# Check all printers configured correctly
curl http://localhost:5000/api/config/printers | jq '.[] | {id, name, ip, serial_number}'

# Each should have unique:
# - IP address
# - Serial number
# - Access code (if different)
```

**Check Network:**
```bash
# Ensure all printers reachable
for ip in 192.168.1.100 192.168.1.101 192.168.1.102; do
  ping -c 3 $ip
done

# Check for VLAN separation
# All printers should be on same subnet as server
```

## Advanced Troubleshooting

### Direct MQTT Connection Test

**Using mosquitto_sub:**
```bash
# Install MQTT client
sudo apt-get install mosquitto-clients

# Subscribe to printer
mosquitto_sub -h PRINTER_IP -p 1883 \
  -u bblp -P ACCESS_CODE \
  -t "device/SERIAL_NUMBER/report" \
  -F "@Y-@m-@d @H:@M:@S %t %p"

# Should see messages every 1-2 seconds
# If not:
# - Wrong access code
# - Wrong serial number
# - MQTT disabled
# - Firewall blocking
```

### Check MQTT Message Format

**Sample report message:**
```json
{
  "print": {
    "gcode_state": "RUNNING",
    "mc_percent": 45,
    "layer_num": 150,
    "total_layer_num": 300,
    "nozzle_temp": 220,
    "bed_temp": 60,
    "ams": {
      "tray_now": "0",
      "tray": [
        {
          "id": "0",
          "remain": 100,
          "k": 0.03,
          "n": "1",
          "color": "FF0000FF"
        }
      ]
    }
  }
}
```

### Monitor MQTT Traffic

**Using tcpdump:**
```bash
# Capture MQTT packets
sudo tcpdump -i any -n -A port 1883 -w mqtt-capture.pcap

# View in Wireshark
wireshark mqtt-capture.pcap

# Filter for MQTT
# Display Filter: mqtt
```

### Check Status API Directly

**Full status check:**
```bash
# Get all status data
curl http://localhost:5001/api/status/printers/1 | jq .

# Expected fields:
{
  "printer_id": 1,
  "name": "Farm P1S #1",
  "status": "printing",  # or idle, paused, etc.
  "connected": true,
  "nozzle_temp": 220,
  "bed_temp": 60,
  "mc_percent": 45,
  "layer_num": 150,
  "total_layer_num": 300,
  "print_error": null,
  "gcode_state": "RUNNING",
  "subtask_name": "model.3mf",
  "ams": {
    // AMS data if equipped
  },
  "last_update": "2025-01-11T10:30:00Z"
}
```

### Check Container Environment

**Verify network access from container:**
```bash
# Enter container
docker exec -it bambu-farm-monitor sh

# Test printer reachable
ping -c 3 PRINTER_IP

# Test MQTT port
nc -zv PRINTER_IP 1883

# Check if MQTT client installed
which mosquitto_sub

# Exit
exit
```

## Prevention Tips

### 1. Use Static IPs

**Set on printer or router:**
- Prevents IP changes
- More reliable MQTT connections
- Easier troubleshooting

### 2. Document Access Codes

**Create spreadsheet:**
| Printer | IP | Access Code | Serial | Last Updated |
|---------|-------------|-------------|---------|--------------|
| Farm P1S #1 | 192.168.1.100 | 12345678 | 01P00... | 2025-01-11 |

**Why:**
- Easy reference during troubleshooting
- Track code changes
- Quick recovery if config lost

### 3. Enable MQTT Persistently

**On printer:**
- Leave MQTT enabled always
- Don't toggle on/off unnecessarily
- Regenerating code breaks connections

### 4. Monitor Connection Health

**Check regularly:**
```bash
# Quick health check
curl http://localhost:5001/api/status/printers/all | jq '.[] | {name, connected}'

# Should all show "connected": true
```

### 5. Keep Firmware Updated

**Printer firmware:**
- Updates may fix MQTT issues
- Check: Settings → Device → Check for updates
- Test after updating

### 6. Backup Configuration

**After getting everything working:**
```bash
# Export configuration
curl -o bambu-backup.json http://localhost:5000/api/config/export

# Store safely
# Easy restore if needed
```

## When to Ask for Help

**Gather this information:**

1. **Printer details:**
   ```bash
   # Model (P1P, P1S, X1C, etc.)
   # Firmware version
   # AMS? (Y/N)
   ```

2. **Network details:**
   ```bash
   # Printer IP
   # Server IP
   # Same subnet? (Y/N)
   # Wired or WiFi?
   ```

3. **MQTT test:**
   ```bash
   # Result of:
   nc -zv PRINTER_IP 1883

   # And:
   mosquitto_sub -h PRINTER_IP -p 1883 \
     -u bblp -P ACCESS_CODE \
     -t "device/SERIAL/#" -v
   ```

4. **Logs:**
   ```bash
   docker logs bambu-farm-monitor 2>&1 | grep -i mqtt | tail -50
   ```

5. **Status API response:**
   ```bash
   curl http://localhost:5001/api/status/printers/1 | jq .
   ```

**Where to ask:**
- [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
- Include all above information
- Be specific about what's not working

## Related Guides

- **[Video Stream Issues](Video-Stream-Issues.md)** - Video streaming problems
- **[Network Configuration](Network-Configuration.md)** - Network setup
- **[Common Issues](Common-Issues.md)** - General troubleshooting
- **[Debugging Guide](Debugging-Guide.md)** - Advanced debugging

## Next Steps

After fixing MQTT:
- **[Printer Configuration](Printer-Configuration.md)** - Manage printers
- **[Layout Customization](Layout-Customization.md)** - Arrange dashboard
- **[Performance Optimization](Performance-Optimization.md)** - Optimize performance
