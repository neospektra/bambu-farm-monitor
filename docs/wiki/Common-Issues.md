# Common Issues and Solutions

This guide covers the most frequently encountered issues and their solutions.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Video Stream Issues](#video-stream-issues)
- [Status/MQTT Issues](#statusmqtt-issues)
- [Configuration Issues](#configuration-issues)
- [Performance Issues](#performance-issues)
- [Network Issues](#network-issues)

## Installation Issues

### Cannot Pull Docker Image

**Symptom:** `docker pull` fails with "manifest unknown" or "not found"

**Solutions:**

1. **Verify image name:**
   ```bash
   docker pull neospektra/bambu-farm-monitor:latest
   ```
   Make sure you're using the correct repository name.

2. **Check Docker Hub status:**
   Visit https://hub.docker.com/r/neospektra/bambu-farm-monitor to verify the image exists

3. **Try with explicit registry:**
   ```bash
   docker pull docker.io/neospektra/bambu-farm-monitor:latest
   ```

4. **Check Docker authentication:**
   ```bash
   docker logout
   docker login
   ```

### Port Already in Use

**Symptom:** Error: "bind: address already in use"

**Solutions:**

1. **Find what's using the port:**
   ```bash
   # Linux/Mac
   sudo lsof -i :8080

   # Windows
   netstat -ano | findstr :8080
   ```

2. **Stop conflicting service:**
   ```bash
   sudo systemctl stop <service-name>
   ```

3. **Use different ports:**
   ```bash
   docker run -d \
     -p 8081:8080 \
     -p 1985:1984 \
     -p 5002:5000 \
     -p 5003:5001 \
     neospektra/bambu-farm-monitor:latest
   ```

4. **Check for zombie containers:**
   ```bash
   docker ps -a
   docker rm <container-id>
   ```

### Permission Denied Errors

**Symptom:** "permission denied" when creating volumes or running container

**Solutions:**

1. **Run with sudo (temporary):**
   ```bash
   sudo docker run ...
   ```

2. **Add user to docker group (permanent):**
   ```bash
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

3. **Fix volume permissions:**
   ```bash
   sudo chown -R $USER:$USER ./config
   ```

4. **Use Podman rootless:**
   ```bash
   podman run --user $(id -u):$(id -g) ...
   ```

### Container Keeps Restarting

**Symptom:** Container starts then immediately exits

**Solutions:**

1. **Check logs:**
   ```bash
   docker logs bambu-farm-monitor
   ```

2. **Common causes:**
   - Invalid configuration file
   - Port conflicts
   - Missing dependencies
   - Volume permission issues

3. **Start without restart policy:**
   ```bash
   docker run -d --rm \
     --name bambu-farm-monitor \
     neospektra/bambu-farm-monitor:latest
   docker logs -f bambu-farm-monitor
   ```

## Video Stream Issues

### No Video Streams Showing

**Symptom:** Black screen or loading spinner where video should be

**Solutions:**

1. **Verify printer IP is correct:**
   - Ping the printer: `ping 192.168.1.100`
   - Check printer display for current IP

2. **Check access code:**
   - Verify it's exactly 8 digits
   - Re-generate code if unsure (Settings → Network → MQTT)

3. **Verify firewall allows outbound connections:**
   ```bash
   # Test connection from container
   docker exec bambu-farm-monitor curl -I http://192.168.1.100
   ```

4. **Check go2rtc logs:**
   ```bash
   docker logs bambu-farm-monitor | grep go2rtc
   ```

5. **Try accessing go2rtc directly:**
   Open `http://YOUR_SERVER_IP:1984` in browser

### Video Lags or Stutters

**Symptom:** Video stream is choppy or delayed

**Solutions:**

1. **Check network bandwidth:**
   - Each stream uses ~2-5 Mbps
   - Multiple streams can saturate network

2. **Reduce quality in go2rtc config** (advanced)

3. **Check server CPU usage:**
   ```bash
   docker stats bambu-farm-monitor
   ```

4. **Verify printer Wi-Fi signal strength:**
   - Check printer display: Settings → Network
   - Consider wired Ethernet if available

5. **Close other applications:**
   - Video encoding/decoding is CPU intensive
   - Close unused browser tabs

### Video Stream Shows Error

**Symptom:** "Failed to load" or error message in video player

**Solutions:**

1. **Refresh the page:**
   - Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)

2. **Check browser console:**
   - Press F12 → Console tab
   - Look for error messages

3. **Try different browser:**
   - Chrome/Edge (recommended)
   - Firefox
   - Safari

4. **Disable browser extensions:**
   - Ad blockers can interfere with WebRTC
   - Try incognito/private mode

5. **Clear browser cache:**
   - Settings → Privacy → Clear browsing data

## Status/MQTT Issues

### Status Shows "Loading status..." Forever

**Symptom:** Print status never updates, shows loading spinner

**Solutions:**

1. **Verify serial number is correct:**
   - Check printer: Settings → Device → Serial Number
   - Update in Bambu Farm Monitor settings

2. **Check MQTT is enabled on printer:**
   - Settings → Network → MQTT → ON
   - Access code should be displayed

3. **Test MQTT connection:**
   - Go to Settings in Bambu Farm Monitor
   - Click "Test MQTT Connection" button

4. **Check MQTT logs:**
   ```bash
   docker logs bambu-farm-monitor | grep mqtt
   ```

5. **Reconnect MQTT manually:**
   - Go to Settings
   - Click "Save All Changes" (triggers reconnect)

### Status Shows "Disconnected"

**Symptom:** Red "Disconnected" status even though printer is on

**Solutions:**

1. **Verify printer is on same network:**
   ```bash
   ping 192.168.1.100
   ```

2. **Check if IP changed:**
   - Router DHCP may have reassigned IP
   - Set static IP reservation in router

3. **Restart printer:**
   - Power cycle the printer
   - Wait 30 seconds before checking again

4. **Check firewall rules:**
   - Ensure MQTT port 1883 is not blocked
   - Allow connections from your server

5. **Force MQTT reconnect:**
   ```bash
   curl -X POST http://localhost:5001/api/status/reconnect
   ```

### AMS Colors Not Showing

**Symptom:** No AMS filament colors displayed, or shows "has_ams: false"

**Solutions:**

1. **Verify printer has AMS unit:**
   - Not all models support AMS
   - Check if AMS is physically connected

2. **Check raw MQTT data:**
   ```bash
   curl http://localhost:5001/api/status/raw/1
   ```
   Look for `ams` section

3. **Update to latest version:**
   ```bash
   docker pull neospektra/bambu-farm-monitor:latest
   docker-compose up -d
   ```

4. **Check if AMS is detected by printer:**
   - Printer display → AMS section
   - Should show filament slots

### Temperature Values Are Zero

**Symptom:** Nozzle/bed temps show 0° or don't update

**Solutions:**

1. **Check if printer is in standby:**
   - Temps may be at ambient when not printing
   - This is normal behavior

2. **Verify MQTT connection:**
   - Status should show "Connected"
   - If disconnected, see [Status Shows "Disconnected"](#status-shows-disconnected)

3. **Wait for data:**
   - MQTT updates every 2-5 seconds
   - May take 10-15 seconds after connection

4. **Check printer firmware:**
   - Old firmware may not report temps
   - Update to latest via Bambu Studio

## Configuration Issues

### Cannot Save Printer Settings

**Symptom:** "Save All Changes" button doesn't work or shows error

**Solutions:**

1. **Check volume permissions:**
   ```bash
   docker exec bambu-farm-monitor ls -la /app/config
   ```

2. **Verify volume is mounted:**
   ```bash
   docker inspect bambu-farm-monitor | grep Mounts -A 10
   ```

3. **Check disk space:**
   ```bash
   df -h
   ```

4. **Look for errors in logs:**
   ```bash
   docker logs bambu-farm-monitor | grep -i error
   ```

5. **Restart container:**
   ```bash
   docker restart bambu-farm-monitor
   ```

### Configuration Not Persisting After Restart

**Symptom:** Printers disappear after container restart

**Solutions:**

1. **Verify volume is specified:**
   ```bash
   docker run -d \
     -v bambu-config:/app/config \
     neospektra/bambu-farm-monitor:latest
   ```

2. **Check volume still exists:**
   ```bash
   docker volume ls
   docker volume inspect bambu-config
   ```

3. **Use bind mount instead:**
   ```bash
   docker run -d \
     -v $(pwd)/config:/app/config \
     neospektra/bambu-farm-monitor:latest
   ```

4. **Export configuration as backup:**
   - Settings → Export Configuration
   - Save JSON file externally

### Cannot Delete Printer

**Symptom:** Delete button doesn't work or printer reappears

**Solutions:**

1. **Check version:**
   - Delete feature added in v3.2.0
   - Update to latest version

2. **Check browser console:**
   - F12 → Console
   - Look for JavaScript errors

3. **Clear browser cache:**
   - Ctrl+Shift+Delete
   - Clear cached images and files

4. **Use API instead:**
   ```bash
   curl -X DELETE http://localhost:5000/api/config/printers/1
   ```

## Performance Issues

### Web UI Loads Slowly

**Symptom:** Dashboard takes long time to load or is unresponsive

**Solutions:**

1. **Check CPU usage:**
   ```bash
   docker stats bambu-farm-monitor
   ```

2. **Reduce number of simultaneous streams:**
   - Use layout selector to show fewer printers
   - Close printers you're not actively monitoring

3. **Check network speed:**
   - Multiple HD streams require good bandwidth
   - Consider wired connection for server

4. **Increase container resources:**
   ```bash
   docker update --cpus="2.0" --memory="2g" bambu-farm-monitor
   ```

5. **Restart container:**
   ```bash
   docker restart bambu-farm-monitor
   ```

### High CPU Usage

**Symptom:** Server CPU at 100% constantly

**Solutions:**

1. **Limit video streams:**
   - go2rtc transcoding is CPU-intensive
   - Show only active printers

2. **Check for memory leaks:**
   ```bash
   docker stats bambu-farm-monitor
   ```

3. **Update to latest version:**
   - May include performance improvements
   ```bash
   docker-compose pull && docker-compose up -d
   ```

4. **Use hardware acceleration (advanced):**
   - Requires GPU passthrough to container
   - See go2rtc documentation

### Memory Usage Growing

**Symptom:** Container memory usage increases over time

**Solutions:**

1. **Restart container regularly:**
   ```bash
   # Add to crontab for weekly restart
   0 3 * * 0 docker restart bambu-farm-monitor
   ```

2. **Set memory limits:**
   ```bash
   docker run -d --memory="1g" --memory-swap="1g" \
     neospektra/bambu-farm-monitor:latest
   ```

3. **Monitor for leaks:**
   ```bash
   watch -n 5 'docker stats bambu-farm-monitor --no-stream'
   ```

4. **Report issue:**
   - If memory grows unbounded, report on GitHub
   - Include logs and system info

## Network Issues

### Cannot Access Web UI

**Symptom:** Browser shows "Connection refused" or "Unable to connect"

**Solutions:**

1. **Verify container is running:**
   ```bash
   docker ps | grep bambu-farm-monitor
   ```

2. **Check port mapping:**
   ```bash
   docker port bambu-farm-monitor
   ```

3. **Test from server:**
   ```bash
   curl http://localhost:8080
   ```

4. **Check firewall:**
   ```bash
   # Linux
   sudo ufw status
   sudo ufw allow 8080

   # Windows
   # Control Panel → Windows Defender Firewall → Advanced Settings
   ```

5. **Use correct IP:**
   - Don't use `localhost` from another machine
   - Use server's actual IP: `192.168.1.x`

### CORS Errors in Browser Console

**Symptom:** Console shows "blocked by CORS policy"

**Solutions:**

1. **Update to latest version:**
   - CORS issues fixed in v3.3.9+
   ```bash
   docker pull neospektra/bambu-farm-monitor:latest
   docker-compose up -d
   ```

2. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R

3. **Check nginx configuration:**
   ```bash
   docker exec bambu-farm-monitor cat /etc/nginx/sites-available/default
   ```

### Port Forwarding Not Working

**Symptom:** Can access locally but not remotely

**Solutions:**

1. **Configure router port forwarding:**
   - Forward 8080 → server_ip:8080

2. **Check public IP:**
   ```bash
   curl ifconfig.me
   ```

3. **Verify internal access first:**
   - Must work on local network before remote

4. **Use VPN instead:**
   - More secure than port forwarding
   - WireGuard or Tailscale recommended

5. **Check ISP restrictions:**
   - Some ISPs block common ports
   - Try non-standard port (e.g., 8443)

## Still Having Issues?

If your problem isn't listed here:

1. **Check the logs:**
   ```bash
   docker logs bambu-farm-monitor
   ```

2. **Search existing issues:**
   https://github.com/neospektra/bambu-farm-monitor/issues

3. **Ask in Discussions:**
   https://github.com/neospektra/bambu-farm-monitor/discussions

4. **Open a new issue:**
   https://github.com/neospektra/bambu-farm-monitor/issues/new

   Include:
   - Version number
   - Platform (QNAP, Synology, Docker, etc.)
   - Full error messages
   - Relevant logs
   - Steps to reproduce

## Related Guides

- **[Debugging Guide](Debugging-Guide.md)** - Advanced troubleshooting
- **[Video Stream Issues](Video-Stream-Issues.md)** - Detailed video troubleshooting
- **[MQTT Connection Problems](MQTT-Connection-Problems.md)** - MQTT-specific issues
- **[Performance Optimization](Performance-Optimization.md)** - Improve performance
