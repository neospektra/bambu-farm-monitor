# Video Stream Issues

Comprehensive troubleshooting guide for video streaming problems.

## Overview

Bambu Farm Monitor uses go2rtc to proxy RTSP streams from your Bambu Lab printers. This guide helps diagnose and fix video streaming issues.

## How Video Streaming Works

**Architecture:**
```
Printer RTSP → go2rtc (port 1984) → WebRTC/MSE → Browser
```

**Components:**
1. **Printer:** Streams RTSP video on local network
2. **go2rtc:** Receives RTSP, converts to WebRTC/MSE
3. **Browser:** Displays video via HTML5 video element

**Authentication:** Uses printer IP and access code (8-digit MQTT password)

## Common Issues

### Issue 1: Black Screen (No Video)

**Symptoms:**
- Video player shows black screen
- No loading indicator
- May show poster image only

**Causes:**
1. Wrong IP address
2. Wrong access code
3. Printer offline/unreachable
4. Network firewall blocking RTSP
5. go2rtc not running

**Diagnosis:**

```bash
# Test 1: Ping printer
ping PRINTER_IP

# Test 2: Check RTSP port (554)
nc -zv PRINTER_IP 554

# Test 3: Check go2rtc is running
curl http://localhost:1984

# Test 4: Check go2rtc streams
curl http://localhost:1984/api/streams
```

**Solutions:**

**Verify IP Address:**
```bash
# On printer screen:
Settings → Network → Connection Info

# Or find via network scan:
nmap -sn 192.168.1.0/24 | grep -B 2 Bambu
```

**Verify Access Code:**
```bash
# On printer screen:
Settings → Network → MQTT → Access Code

# Test MQTT connection in Settings UI:
Click "Test MQTT Connection" button
```

**Check Printer is Reachable:**
```bash
# From container host:
ping PRINTER_IP

# From inside container:
docker exec bambu-farm-monitor ping PRINTER_IP
```

**Check Firewall Rules:**
```bash
# Ensure port 554 (RTSP) is not blocked
# Disable firewall temporarily to test:
sudo ufw disable  # Ubuntu/Debian
# Or check specific rules:
sudo iptables -L -n | grep 554
```

**Restart go2rtc:**
```bash
# Restart entire container
docker restart bambu-farm-monitor

# Check logs for go2rtc errors
docker logs bambu-farm-monitor | grep go2rtc
```

### Issue 2: Loading Forever (Spinner)

**Symptoms:**
- Loading indicator spins indefinitely
- No video appears
- Browser console shows errors

**Causes:**
1. go2rtc stream not configured
2. RTSP connection timeout
3. Network latency too high
4. Browser blocking WebRTC

**Diagnosis:**

```bash
# Check go2rtc stream configuration
curl http://localhost:1984/api/streams | jq .

# Check go2rtc logs
docker logs bambu-farm-monitor 2>&1 | grep -i stream

# Test RTSP URL manually
ffmpeg -i "rtsps://bblp:ACCESS_CODE@PRINTER_IP:322/streaming/live/1" \
  -frames:v 1 test.jpg
```

**Solutions:**

**Check Stream Configuration:**
```bash
# Go2rtc should auto-configure streams
# Verify in logs:
docker logs bambu-farm-monitor | grep "Stream.*added"
```

**Test Network Latency:**
```bash
# Ping should be <50ms ideally
ping -c 10 PRINTER_IP

# Check for packet loss
mtr PRINTER_IP
```

**Browser Console Check:**
1. Open browser DevTools (F12)
2. Go to **Console** tab
3. Look for WebRTC or network errors
4. Common errors:
   - `Failed to fetch`
   - `WebSocket connection failed`
   - `ICE connection failed`

**Try Different Browser:**
- Chrome/Edge (best WebRTC support)
- Firefox (good)
- Safari (limited support)

**Disable Browser Extensions:**
- Ad blockers may interfere
- Privacy extensions may block WebRTC
- Try incognito/private mode

### Issue 3: Stuttering/Laggy Video

**Symptoms:**
- Video plays but stutters
- Freezes then jumps forward
- Audio/video out of sync (if audio enabled)

**Causes:**
1. Network bandwidth insufficient
2. WiFi interference
3. CPU overload on server
4. Too many concurrent streams

**Diagnosis:**

```bash
# Check CPU usage
docker stats bambu-farm-monitor

# Check network bandwidth
iperf3 -c PRINTER_IP  # If iperf3 server running

# Check WiFi signal (if using WiFi)
# On printer: Settings → Network → WiFi Signal

# Monitor go2rtc performance
curl http://localhost:1984/api/streams | jq '.[] | {name, consumers}'
```

**Solutions:**

**Reduce Number of Streams:**
- Close printers not actively being watched
- Use 1-column layout and scroll
- Most browsers pause off-screen videos automatically

**Improve Network:**
```bash
# Switch printer to wired ethernet (best)
# Or improve WiFi:
# - Move router closer
# - Use 5GHz WiFi instead of 2.4GHz
# - Reduce interference (microwave, Bluetooth)
```

**Optimize Server Resources:**
```bash
# Increase container CPU limit
docker update --cpus=2 bambu-farm-monitor

# Check other containers aren't consuming resources
docker stats
```

**Use Lower Quality (Future Feature):**
Currently all streams are 1080p. Future versions may support quality selection.

### Issue 4: Video Delayed (Not Real-Time)

**Symptoms:**
- Video shows print from 5-30 seconds ago
- Delays increase over time

**Causes:**
1. Network latency
2. Buffer accumulation
3. Transcoding overhead

**Solutions:**

**Refresh Stream:**
- Click away from dashboard
- Return to dashboard
- Stream reconnects with fresh buffer

**Reduce Latency:**
```bash
# Use wired ethernet for printer
# Minimize network hops between server and printer
# Ensure server and printers on same subnet
```

**Check go2rtc Configuration:**
```yaml
# Low-latency go2rtc config (advanced)
# Currently auto-configured, may be customizable in future
```

### Issue 5: Stream Disconnects Randomly

**Symptoms:**
- Video stops unexpectedly
- Shows black screen or loading
- Reconnects after a few seconds

**Causes:**
1. Network instability
2. Printer rebooting
3. Router dropping connections
4. RTSP timeout

**Diagnosis:**

```bash
# Monitor connection stability
ping -i 0.2 PRINTER_IP | while read line; do
  echo "$(date): $line"
done

# Check for network errors
docker logs bambu-farm-monitor 2>&1 | grep -i "disconnect\|timeout\|error"

# Check printer uptime
# On printer: Settings → Device → Uptime
```

**Solutions:**

**Static IP and DHCP Reservation:**
```bash
# Configure static IP on printer
# Or DHCP reservation on router
# Prevents IP changes causing disconnects
```

**Increase RTSP Timeout (Advanced):**
```yaml
# May require go2rtc config customization (future feature)
```

**Check Router:**
- Update router firmware
- Disable SIP ALG (can interfere with RTSP)
- Increase connection timeout settings

**Use Wired Connection:**
- Connect printer via ethernet
- Eliminates WiFi dropouts

### Issue 6: "Not Supported" or Codec Error

**Symptoms:**
- Browser shows "Video format not supported"
- Console shows codec errors

**Causes:**
1. Browser doesn't support codec
2. go2rtc transcoding failed
3. Printer sending unsupported format

**Solutions:**

**Use Supported Browser:**
- **Chrome/Edge:** Best support (H.264, H.265)
- **Firefox:** Good support (H.264)
- **Safari:** Limited support

**Check go2rtc Logs:**
```bash
docker logs bambu-farm-monitor 2>&1 | grep -i "codec\|transcode"
```

**Update Browser:**
- Ensure browser is latest version
- Hardware acceleration enabled

### Issue 7: Video Works on Some Devices, Not Others

**Symptoms:**
- Desktop works, mobile doesn't
- One browser works, another doesn't

**Causes:**
1. Browser compatibility
2. Network differences (WiFi vs wired)
3. Firewall rules per device
4. Hardware acceleration differences

**Solutions:**

**Check Browser Compatibility:**
- Use Chrome/Edge on all devices
- Update browsers to latest version

**Network Test:**
```bash
# From non-working device:
# Open http://SERVER_IP:1984
# Should see go2rtc web interface

# Test stream directly:
# http://SERVER_IP:1984/stream.html?src=printer-1
```

**Clear Browser Cache:**
```bash
# Chrome: Ctrl+Shift+Delete
# Select "Cached images and files"
# Clear
```

### Issue 8: Video Quality is Poor

**Symptoms:**
- Pixelated or blocky video
- Low resolution
- Compression artifacts

**Causes:**
1. Network bandwidth limitation
2. Printer camera quality
3. Transcoding settings

**Current Limitations:**
- Bambu Lab cameras are 1080p
- Quality depends on printer's RTSP stream
- No quality adjustment currently available

**Future Enhancements:**
- Quality selection (High/Medium/Low)
- Bitrate customization
- Resolution options

**Workarounds:**
```bash
# Ensure good network connection
# Use wired ethernet
# Minimize network congestion
```

## Advanced Troubleshooting

### Check go2rtc Stream Status

**Via API:**
```bash
# List all streams
curl http://localhost:1984/api/streams | jq .

# Check specific printer
curl http://localhost:1984/api/streams | jq '.["printer-1"]'

# Expected output:
{
  "name": "printer-1",
  "url": "rtsps://bblp:CODE@IP:322/streaming/live/1",
  "consumers": [
    {
      "url": "webrtc",
      "state": "active"
    }
  ]
}
```

### Test RTSP Stream Directly

**Using VLC:**
1. Open VLC Media Player
2. **Media** → **Open Network Stream**
3. Enter URL:
   ```
   rtsps://bblp:ACCESS_CODE@PRINTER_IP:322/streaming/live/1
   ```
4. Click **Play**

**Should see:**
- Live video from printer
- Proves RTSP stream works

**If VLC fails:**
- Wrong access code
- Printer RTSP disabled
- Network blocking port 322

**Using FFmpeg:**
```bash
# Test stream and save frame
ffmpeg -rtsp_transport tcp \
  -i "rtsps://bblp:ACCESS_CODE@PRINTER_IP:322/streaming/live/1" \
  -frames:v 1 -f image2 test.jpg

# Check test.jpg - should show printer view
```

### Check WebRTC in Browser

**Chrome WebRTC Internals:**
1. Navigate to: `chrome://webrtc-internals/`
2. Start video stream in another tab
3. Check stats:
   - Bytes received
   - Packets lost
   - ICE connection state
   - Codec used

**Look for:**
- High packet loss (>1%)
- Connection state not "connected"
- Bitrate drops

### Network Packet Capture

**Capture RTSP traffic:**
```bash
# Install tcpdump
sudo apt-get install tcpdump

# Capture RTSP packets
sudo tcpdump -i any -n port 322 -w rtsp-capture.pcap

# Analyze in Wireshark
wireshark rtsp-capture.pcap
```

**Look for:**
- TCP retransmissions
- Packet loss
- Connection resets

### Check Container Network

**Verify container can reach printer:**
```bash
# Enter container shell
docker exec -it bambu-farm-monitor sh

# Test connectivity
ping PRINTER_IP
telnet PRINTER_IP 322
curl -v rtsps://bblp:CODE@PRINTER_IP:322/streaming/live/1

# Exit container
exit
```

**Check network mode:**
```bash
docker inspect bambu-farm-monitor | grep NetworkMode

# Should be "bridge" for most setups
```

### Verify Ports are Accessible

**From external device:**
```bash
# Test Web UI port
curl http://SERVER_IP:8080

# Test go2rtc port
curl http://SERVER_IP:1984

# Test if ports are open
nmap -p 8080,1984,5000,5001 SERVER_IP
```

## Prevention Tips

### 1. Use Static IPs

**For both:**
- Server/NAS running Bambu Farm Monitor
- All printers

**Why:**
- Prevents DHCP changes breaking streams
- More reliable long-term

### 2. Wired Connections

**Ethernet vs WiFi:**
- **Wired:** More reliable, lower latency, higher bandwidth
- **WiFi:** Convenient but prone to interference

**Recommendation:**
- Server: Wired (essential)
- Printers: Wired if possible, 5GHz WiFi otherwise

### 3. Network Optimization

**Same Subnet:**
- Keep server and printers on same subnet
- Reduces routing overhead

**Quality of Service (QoS):**
- Configure router to prioritize video traffic
- Assign high priority to ports 322, 1984

**Bandwidth:**
- 10 Mbps per stream recommended
- Monitor total network usage

### 4. Regular Updates

**Keep Updated:**
- Bambu Farm Monitor (docker pull)
- Printer firmware
- Browser

**Check for updates:**
```bash
docker pull neospektra/bambu-farm-monitor:latest
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# Re-create container
```

### 5. Monitor Logs

**Check regularly:**
```bash
docker logs bambu-farm-monitor --tail 100 --follow

# Look for:
# - Stream errors
# - Connection timeouts
# - go2rtc warnings
```

## When to Ask for Help

**Gather this information:**

1. **System details:**
   ```bash
   # Container version
   docker inspect bambu-farm-monitor | grep Image

   # Host OS
   uname -a

   # Docker version
   docker --version
   ```

2. **Network details:**
   ```bash
   # Printer IP and model
   # Server IP
   # Same subnet? (Y/N)
   # Wired or WiFi?
   ```

3. **Logs:**
   ```bash
   # Last 100 lines with errors
   docker logs bambu-farm-monitor 2>&1 | grep -i error | tail -100
   ```

4. **Browser console errors:**
   - Screenshot of F12 Console tab
   - Any red error messages

5. **What you've tried:**
   - List troubleshooting steps already attempted

**Where to ask:**
- [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
- Include all above information
- Be specific about symptoms

## Related Guides

- **[MQTT Connection Problems](MQTT-Connection-Problems.md)** - Status update issues
- **[Network Configuration](Network-Configuration.md)** - Network setup
- **[Common Issues](Common-Issues.md)** - General troubleshooting
- **[Performance Optimization](Performance-Optimization.md)** - Improve streaming performance

## Next Steps

After fixing video issues:
- **[Printer Configuration](Printer-Configuration.md)** - Manage printers
- **[Layout Customization](Layout-Customization.md)** - Arrange your dashboard
- **[Backup and Restore](Backup-and-Restore.md)** - Protect your configuration
