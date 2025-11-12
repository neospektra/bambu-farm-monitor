# Performance Optimization

Guide to optimize Bambu Farm Monitor for best performance with multiple printers.

## Overview

Bambu Farm Monitor can handle multiple concurrent video streams and status updates. This guide helps optimize performance for different hardware configurations and usage scenarios.

## Performance Factors

### Resource Usage

**Per Video Stream:**
- CPU: 5-15% per stream (transcoding)
- RAM: 50-100 MB per stream
- Network: 2-5 Mbps per stream

**Base Application:**
- CPU: 5-10% baseline
- RAM: 200-300 MB baseline
- Disk: ~1 GB (image + config)

**Example Calculations:**

**4 Printers:**
- CPU: 20-60% + 10% base = 30-70%
- RAM: 200-400 MB + 300 MB base = 500-700 MB
- Network: 8-20 Mbps

**8 Printers:**
- CPU: 40-120% + 10% base = 50-130% (multi-core helps)
- RAM: 400-800 MB + 300 MB base = 700-1100 MB
- Network: 16-40 Mbps

## Hardware Recommendations

### Minimum Requirements

**1-2 Printers:**
- CPU: 2 cores @ 2.0 GHz
- RAM: 2 GB
- Network: 10 Mbps

**3-4 Printers:**
- CPU: 2 cores @ 2.5 GHz or 4 cores @ 2.0 GHz
- RAM: 4 GB
- Network: 20 Mbps

**5-8 Printers:**
- CPU: 4 cores @ 2.5 GHz
- RAM: 4-8 GB
- Network: 50 Mbps

**9-12 Printers:**
- CPU: 6+ cores @ 2.5 GHz
- RAM: 8 GB
- Network: 100 Mbps

**13+ Printers:**
- Consider multiple instances
- Or powerful dedicated server

### Recommended Hardware

**NAS Models:**

**QNAP:**
- TS-464, TS-664: Good for 4-6 printers
- TS-873A, TS-1273A: Good for 8-10 printers
- TVS-h674: Excellent for 12+ printers

**Synology:**
- DS920+, DS1520+: Good for 4-6 printers
- DS1821+: Good for 8-10 printers
- RS models: Excellent for 12+ printers

**Unraid:**
- Depends on server hardware
- Intel i5/i7 or Ryzen 5/7 recommended
- 8-16 GB RAM for medium farms

**Raspberry Pi:**
- **Not recommended** (ARM architecture)
- go2rtc requires x86_64

**Dedicated Server:**
- Intel Xeon or AMD EPYC
- 16+ GB RAM
- Can handle 20+ printers

## Container Resource Limits

### Set CPU Limits

**Docker:**
```bash
# Limit to 2 CPUs
docker update --cpus=2 bambu-farm-monitor

# Limit to 50% of system
docker update --cpus=2.5 bambu-farm-monitor  # On 5-core system
```

**Docker Compose:**
```yaml
services:
  bambu-farm-monitor:
    image: neospektra/bambu-farm-monitor:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

**Why set limits:**
- Prevents container hogging all CPU
- Reserves resources for other services
- Better multi-tenant performance

### Set Memory Limits

**Docker:**
```bash
# Limit to 2 GB
docker update --memory=2g bambu-farm-monitor

# With swap limit
docker update --memory=2g --memory-swap=4g bambu-farm-monitor
```

**Docker Compose:**
```yaml
services:
  bambu-farm-monitor:
    mem_limit: 2g
    memswap_limit: 4g
```

**Recommendations:**
- 1-4 printers: 2 GB limit
- 5-8 printers: 4 GB limit
- 9+ printers: 8 GB limit

## Network Optimization

### Use Wired Connections

**Priority:**
1. **Server:** Must be wired (highest priority)
2. **Printers:** Wired preferred, 5GHz WiFi acceptable

**Why:**
- Lower latency
- Higher bandwidth
- More reliable
- Less interference

### Network Topology

**Ideal Setup:**
```
Router (1 Gbps)
  ├─ Switch (1 Gbps)
  │   ├─ Server (wired)
  │   ├─ Printer 1 (wired)
  │   ├─ Printer 2 (wired)
  │   └─ Printer 3 (wired)
  └─ WiFi AP (5GHz)
      ├─ Printer 4 (WiFi)
      └─ Mobile devices
```

**Avoid:**
- Multiple network hops
- WiFi for server
- 2.4GHz WiFi for printers
- Overloaded switches

### VLAN Considerations

**If using VLANs:**
- Put server and printers on same VLAN
- Or configure routing properly
- Test latency between VLANs

**Firewall Rules:**
```bash
# Allow required ports between VLANs
# Printer → Server:
#   - RTSP (322, 554)
#   - MQTT (1883)
# Server → Printer:
#   - MQTT client connection
```

### Quality of Service (QoS)

**Router QoS Configuration:**
1. Prioritize video traffic
2. Set high priority for:
   - Port 322 (RTSP)
   - Port 1984 (go2rtc)
   - Server IP address

**Example (pfSense):**
```
Traffic Shaper
  Priority Queue: Video Streaming
    Ports: 322, 554, 1984
    Priority: High
    Bandwidth: 50% guarantee
```

## Application Optimization

### Use Appropriate Layout

**For Performance:**

**1 Column Layout:**
- Best for 4+ printers
- Scroll to view each
- Browsers pause off-screen videos
- Lowest resource usage

**2 Column Layout:**
- Good for 4-6 printers
- Moderate resource usage

**Auto Grid:**
- Adapts to screen size
- Good for varied usage

**Avoid:**
- 4-column layout with 12+ printers all visible
- All printers visible if not actively monitoring

### Limit Active Streams

**Browser Behavior:**
- Most browsers pause off-screen videos
- Reduces CPU usage automatically
- Use 1-column layout and scroll

**Manual Limiting:**
- Close printers not being watched
- Remove idle printers from dashboard
- Use multiple instances if needed

### Reduce Polling Frequency (Future)

**Current:** Status API polled every 2 seconds

**Future Optimization:**
- Configurable polling interval
- WebSocket for real-time updates
- Reduce polling for idle printers

## Server Optimization

### Operating System Tuning

**Linux Kernel Parameters:**
```bash
# Increase network buffers
sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.wmem_max=26214400

# Increase connection tracking
sudo sysctl -w net.netfilter.nf_conntrack_max=262144

# Make permanent
sudo nano /etc/sysctl.conf
# Add above lines
sudo sysctl -p
```

**Docker Daemon Optimization:**
```json
// /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
```

### Disk I/O

**Use Fast Storage:**
- SSD for Docker images
- SSD for configuration
- NVMe best for high-stream counts

**NAS Specific:**
- Use cache drive for Docker appdata
- Pin to cache (don't use mover)
- Enable SSD trim

**Check I/O Wait:**
```bash
# High I/O wait is bad
iostat -x 1

# %iowait should be <10%
```

### CPU Governor

**Set to Performance:**
```bash
# Check current
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Set to performance
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Or use cpupower
sudo cpupower frequency-set -g performance
```

### Disable Unnecessary Services

**Free up resources:**
```bash
# Check running services
systemctl list-units --type=service --state=running

# Disable unused
sudo systemctl disable bluetooth
sudo systemctl disable cups
# etc.
```

## Browser Optimization

### Use Modern Browser

**Recommended:**
1. **Chrome/Edge:** Best WebRTC support, hardware acceleration
2. **Firefox:** Good support
3. **Safari:** Limited, avoid if possible

**Update regularly** - new versions have performance improvements

### Enable Hardware Acceleration

**Chrome/Edge:**
1. Settings → System
2. Enable **"Use hardware acceleration when available"**
3. Restart browser

**Verify:**
1. Navigate to `chrome://gpu/`
2. Check **"Graphics Feature Status"**
3. Most should say "Hardware accelerated"

### Disable Extensions

**Extensions that hurt performance:**
- Ad blockers (may interfere with WebRTC)
- Privacy extensions (may block media)
- Theme extensions (resource usage)

**Test:**
- Open in incognito/private mode
- If faster, disable extensions one by one

### Clear Browser Cache

**Periodically:**
```bash
# Chrome: Ctrl+Shift+Delete
# Select:
# - Cached images and files
# - Hosted app data
# Time range: All time
# Clear data
```

### Close Unused Tabs

**Each open tab:**
- Uses RAM
- May use CPU
- Network bandwidth

**Best practice:**
- One tab for Bambu Farm Monitor
- Close others when monitoring

## Monitoring Performance

### Container Stats

**Real-time monitoring:**
```bash
# Watch resources
docker stats bambu-farm-monitor

# Output:
# CONTAINER   CPU %   MEM USAGE / LIMIT     MEM %   NET I/O
# bambu-...   45.2%   850MiB / 8GiB        10.4%   12.3MB / 45.6MB
```

**Interpretation:**
- **CPU %**: Should be steady, not spiking
- **MEM %**: Should be <50% of limit
- **NET I/O**: Increases with more streams

### System Monitoring

**Check overall load:**
```bash
# Load average (should be < CPU cores)
uptime

# CPU usage
top
# Press '1' to see per-core

# Memory usage
free -h

# Network usage
iftop  # or nethogs
```

### Application Logs

**Check for errors:**
```bash
# Errors
docker logs bambu-farm-monitor 2>&1 | grep -i error

# Warnings
docker logs bambu-farm-monitor 2>&1 | grep -i warn

# go2rtc performance
docker logs bambu-farm-monitor 2>&1 | grep -i "go2rtc.*performance\|go2rtc.*slow"
```

### go2rtc Stats

**Check stream health:**
```bash
# Get stream statistics
curl http://localhost:1984/api/streams | jq '.[] | {name, state, consumers}'

# Check for issues:
# - state should be "active"
# - consumers should have entries
# - no error fields
```

**Via Web UI:**
1. Navigate to: `http://SERVER_IP:1984`
2. View all streams
3. Check for red/error states

## Scaling Beyond Single Instance

### Multiple Instances

**When to use:**
- 15+ printers
- Server can't handle load
- Geographic distribution

**Setup:**

**Instance 1:**
```bash
docker run -d \
  --name bambu-farm-monitor-1 \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config-1:/app/config \
  neospektra/bambu-farm-monitor:latest
# Printers 1-8
```

**Instance 2:**
```bash
docker run -d \
  --name bambu-farm-monitor-2 \
  -p 8081:8080 -p 1985:1984 -p 5002:5000 -p 5003:5001 \
  -v bambu-config-2:/app/config \
  neospektra/bambu-farm-monitor:latest
# Printers 9-16
```

**Access:**
- Instance 1: `http://SERVER_IP:8080`
- Instance 2: `http://SERVER_IP:8081`

### Load Balancing (Advanced)

**Use nginx to combine instances:**

```nginx
upstream bambu_backend {
    least_conn;
    server localhost:8080;
    server localhost:8081;
}

server {
    listen 80;
    server_name bambu.local;

    location / {
        proxy_pass http://bambu_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Benefits:**
- Single URL for all printers
- Distributes load
- Fault tolerance

### Distributed Monitoring

**Multiple servers in different locations:**
- Server A: Location 1 printers
- Server B: Location 2 printers
- Central dashboard aggregates

**Future Feature:**
- Multi-instance aggregation
- Centralized monitoring

## Troubleshooting Performance Issues

### High CPU Usage

**Diagnosis:**
```bash
# Check CPU usage
docker stats bambu-farm-monitor

# Check per-process inside container
docker exec bambu-farm-monitor top

# Check go2rtc specifically
docker logs bambu-farm-monitor 2>&1 | grep -i "go2rtc.*cpu\|go2rtc.*performance"
```

**Solutions:**
1. Reduce active streams
2. Upgrade server CPU
3. Use multiple instances
4. Close idle printer views

### High Memory Usage

**Diagnosis:**
```bash
# Check memory
docker stats bambu-farm-monitor

# Check for memory leaks
# Run for 24 hours, check if growing continuously
docker stats --no-stream bambu-farm-monitor > mem-check.txt
# Wait 24 hours
docker stats --no-stream bambu-farm-monitor >> mem-check.txt
# Compare
```

**Solutions:**
1. Restart container daily (cron job)
2. Increase memory limit
3. Report if memory leak suspected

### Laggy Video

**Diagnosis:**
```bash
# Check network latency
ping -c 20 PRINTER_IP

# Should be <50ms

# Check packet loss
mtr PRINTER_IP
```

**Solutions:**
1. Use wired connection
2. Reduce stream count
3. Check network congestion
4. Upgrade network equipment

### Browser Performance

**Diagnosis:**
1. Open DevTools (F12)
2. Go to **Performance** tab
3. Click **Record**
4. Monitor for 10 seconds
5. Click **Stop**
6. Analyze timeline

**Look for:**
- Long tasks (>50ms)
- High FPS drops
- Memory allocation spikes

**Solutions:**
1. Close other tabs
2. Disable extensions
3. Enable hardware acceleration
4. Update browser
5. Use different browser

## Best Practices Summary

### Always Do
- ✅ Use wired connection for server
- ✅ Set static IPs
- ✅ Enable hardware acceleration in browser
- ✅ Monitor resource usage
- ✅ Keep software updated

### Avoid
- ❌ WiFi for server
- ❌ All printers visible at once (12+)
- ❌ Running on underpowered hardware
- ❌ Network congestion
- ❌ Outdated browser

### For Large Farms (10+ Printers)
- Use dedicated server (not NAS)
- Separate network for printers
- Multiple instances if needed
- Monitor performance regularly
- Plan for growth

## Next Steps

- **[Network Configuration](Network-Configuration.md)** - Optimize network
- **[Debugging Guide](Debugging-Guide.md)** - Advanced debugging
- **[Common Issues](Common-Issues.md)** - Troubleshooting
- **[Video Stream Issues](Video-Stream-Issues.md)** - Fix streaming problems
