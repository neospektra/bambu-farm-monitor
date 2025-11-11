# Troubleshooting Guide - Bambu Farm Monitor v2

## Known Issues

### MQTT Connection Failure (Status Overlays Not Appearing)

**Symptom:** Camera streams work perfectly, but real-time status overlays (temperatures, print progress, etc.) do not appear on the feeds.

**Root Cause:** The Status API cannot maintain MQTT connections to Bambu printers. Connections establish briefly but immediately disconnect with error code 7 (authentication/authorization failure).

**Evidence:**
```
Printer 1 MQTT connected with code: 0
Printer 1 subscribed to device/+/report
Printer 1 MQTT disconnected unexpectedly with code: 7
```

**Why This Happens:**
Bambu Labs printers require specific MQTT authentication that may involve:
- Device serial numbers in the topic subscription path
- Additional authentication beyond just the access code
- Specific client ID requirements
- Different username/password combinations

**Current Implementation:**
```python
# status_api.py
client.username_pw_set(username="bblp", password=access_code)
client.subscribe("device/+/report")
```

This approach works for some Bambu integrations but appears to fail for persistent connections.

---

## Workarounds

### Option 1: Test Endpoint (Demonstration Only)

A test endpoint has been created to verify the overlay functionality works correctly:

**Endpoint:** `http://localhost:8081/api/status/test`

**Test Page:** `http://localhost:8081/test.html`

This demonstrates that:
- The overlay CSS and HTML are correct
- The JavaScript update logic works
- The UI properly displays status information
- The issue is purely with the MQTT data source

**Using the Test Page:**
1. Navigate to `http://localhost:8081/test.html`
2. You'll see hardcoded status overlays on Printers 1 and 3
3. This shows exactly how the overlays will look when MQTT is working

### Option 2: Alternative Status Sources

**Potential Solutions to Investigate:**

1. **Bambu Cloud API** - Some users report Bambu has a cloud API that might provide status without direct MQTT

2. **Serial Number Discovery** - The MQTT topic may need the actual printer serial:
   ```python
   client.subscribe(f"device/{printer_serial}/report")
   ```
   Serial numbers can often be found on the printer's network settings page

3. **Bambu Studio Integration** - The BambuNetworkEngine.conf file suggests Bambu Studio has working MQTT code that could be examined

4. **Community Resources** - Check:
   - Bambu Labs Discord/Forums
   - Home Assistant Bambu integration (they solved this)
   - OpenBambuAPI project

---

## Verification Steps

### Check Status API Health

```bash
curl http://localhost:8081/api/health
```

Expected output:
```json
{"status": "ok", "mqtt_clients": 4}
```

### Check Status API Logs

```bash
podman logs bambu-farm-monitor | grep "status-api"
```

Look for connection attempts and error codes.

### Test Configuration API

```bash
curl http://localhost:8081/api/config/printers
```

Should return your printer configuration. If this works, the API layer is functioning correctly.

### Verify Network Connectivity

```bash
# From inside the container
podman exec bambu-farm-monitor nc -zv 192.168.7.192 8883
```

Should show connection to MQTT port succeeds.

---

## What's Working

✅ **Camera Streams** - All 4 cameras streaming perfectly via go2rtc
✅ **Configuration Management** - Settings page allows IP/access code updates
✅ **Web UI** - Responsive grid layout with fullscreen capability
✅ **Overlay Rendering** - CSS and JavaScript work correctly (verified via test page)
✅ **APIs** - Config API (port 5000) and Status API (port 5001) are running
✅ **Multi-service Management** - Supervisor properly manages all 4 services

---

## What Needs Fixing

❌ **MQTT Authentication** - Cannot maintain persistent connections to printers
❌ **Real-time Status** - Overlays don't populate with live data

---

## Recommended Next Steps

1. **Investigate Printer Serial Numbers**
   - Check printer web interface or LCD for serial number
   - Update status_api.py to use serial in topic path
   - Test with: `device/{actual_serial}/report`

2. **Research Home Assistant Integration**
   - Home Assistant has a working Bambu integration
   - Their code: https://github.com/home-assistant/core/tree/dev/homeassistant/components/bambu_lab
   - May reveal proper authentication method

3. **Enable Debug Logging**
   Edit status_api.py to add more verbose MQTT logging:
   ```python
   client.enable_logger()
   ```

4. **Test Alternative Approaches**
   - Try HTTP polling instead of MQTT
   - Use Bambu Cloud API if available
   - Investigate FTP status file monitoring (some printers support this)

---

## Deployment Status

The container is fully built and deployable. All features work except the MQTT-dependent status overlays.

**Can be deployed now with:**
- ✅ All 4 camera streams
- ✅ Fullscreen capability
- ✅ Configuration management
- ✅ Settings page

**Will work after MQTT fix:**
- ⏳ Real-time print progress
- ⏳ Temperature monitoring
- ⏳ Layer information
- ⏳ Time remaining estimates

---

## Getting Help

If you solve the MQTT authentication issue, please update status_api.py with the working configuration and document it here for others!

**Useful Resources:**
- Bambu Labs Developer Resources (if available)
- Home Assistant Bambu Lab Integration
- OpenBambuAPI GitHub repository
- Bambu Labs Discord/Reddit communities
