# Support

Get help with Bambu Farm Monitor.

## Quick Links

- 📖 **[Documentation Home](Home.md)** - Complete documentation
- 🐛 **[Report Bug](https://github.com/neospektra/bambu-farm-monitor/issues/new)** - File a bug report
- 💬 **[Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)** - Ask questions
- ❓ **[FAQ](FAQ.md)** - Frequently asked questions
- 🔧 **[Common Issues](Common-Issues.md)** - Troubleshooting guide

## Before Asking for Help

### 1. Check Documentation

**Start here:**
- **[Quick Start](Quick-Start.md)** - Basic setup
- **[Common Issues](Common-Issues.md)** - Known problems
- **[FAQ](FAQ.md)** - Frequently asked questions
- **[Video Stream Issues](Video-Stream-Issues.md)** - Streaming problems
- **[MQTT Connection Problems](MQTT-Connection-Problems.md)** - Status issues

### 2. Search Existing Issues

**Check if already reported:**
1. Go to [GitHub Issues](https://github.com/neospektra/bambu-farm-monitor/issues)
2. Use search bar
3. Check both open and closed issues
4. Look for similar problems

### 3. Search Discussions

**Check community discussions:**
1. Go to [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
2. Search for keywords
3. Browse categories:
   - Q&A
   - Show and Tell
   - General

### 4. Update to Latest Version

**Check version:**
```bash
# Current version
docker inspect bambu-farm-monitor | grep -i version

# Latest available
docker pull neospektra/bambu-farm-monitor:latest
```

**Update if old:**
```bash
docker pull neospektra/bambu-farm-monitor:latest
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# Run container again
```

### 5. Gather Information

**Collect this before asking:**
- System details (OS, Docker version)
- Bambu Farm Monitor version
- Printer models and firmware
- Network configuration
- Error messages
- Logs
- What you've tried

## Getting Support

### GitHub Discussions (Best for Questions)

**When to use:**
- General questions
- How-to questions
- Setup help
- Best practices
- Sharing configurations
- Show and tell

**How to ask:**
1. Go to [Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
2. Click **"New discussion"**
3. Select category:
   - **Q&A** - Questions and answers
   - **General** - General discussion
   - **Show and tell** - Share your setup
   - **Ideas** - Feature suggestions
4. Write clear title
5. Provide details
6. Click **"Start discussion"**

**Discussion Template:**
```markdown
**Question**
Clear question here?

**Context**
What I'm trying to do...

**Environment**
- OS: Ubuntu 22.04
- Docker: 24.0.5
- Bambu Farm Monitor: 3.3.9
- Printers: 2x P1S

**What I've tried**
- Tried X
- Tried Y
- etc.

**Logs/Screenshots**
[paste here]
```

### GitHub Issues (For Bugs Only)

**When to use:**
- Something is broken
- Error messages
- Crashes
- Incorrect behavior
- Security issues

**NOT for:**
- Questions (use Discussions)
- Feature requests (use Discussions Ideas)
- Support requests (use Discussions)

**How to report:**
1. Go to [Issues](https://github.com/neospektra/bambu-farm-monitor/issues)
2. Click **"New issue"**
3. Choose template (if available)
4. Fill in all sections
5. Click **"Submit new issue"**

**Bug Report Template:**
```markdown
## Describe the bug
Clear description of what's wrong.

## To Reproduce
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

## Expected behavior
What should happen.

## Actual behavior
What actually happens.

## Environment
- OS: [Ubuntu 22.04, Windows 11, macOS 13, etc.]
- Docker version: [24.0.5]
- Bambu Farm Monitor version: [3.3.9]
- Browser: [Chrome 120]
- Printer model(s): [P1S, X1C, etc.]
- Printer firmware: [1.2.3.4]

## Logs
```
[paste logs here]
docker logs bambu-farm-monitor 2>&1 | tail -100
```

## Screenshots
[attach screenshots]

## Additional context
Any other relevant information.

## Checklist
- [ ] I searched existing issues
- [ ] I checked Common Issues page
- [ ] I'm using latest version
- [ ] I included logs
- [ ] I removed sensitive information
```

### Community Forums

**Other places to get help:**

**Reddit:**
- r/BambuLab - Bambu Lab community
- r/3Dprinting - General 3D printing
- r/homelab - If running on homelab

**Discord:**
- Bambu Lab Official Discord
- 3D Printing communities

**Note:** These are not official support channels. Responses may vary.

## What Information to Include

### Always Include

**1. System Information:**
```bash
# Operating System
uname -a

# Docker version
docker --version

# Container version
docker inspect bambu-farm-monitor | grep "Image\|Created"

# Resource usage
docker stats --no-stream bambu-farm-monitor
```

**2. Network Details:**
```bash
# Server IP
hostname -I

# Printer IPs (remove last octet for privacy if posting publicly)
# Example: 192.168.1.xxx instead of 192.168.1.100

# Same subnet? Y/N
# Wired or WiFi?
# Any VLANs?
```

**3. Configuration:**
```bash
# Export config (REMOVE access codes before sharing!)
curl http://localhost:5000/api/config/export | jq .

# Replace access codes with XXXXXXXX
# Replace serial numbers if concerned about privacy
```

**4. Logs:**
```bash
# Last 100 lines
docker logs bambu-farm-monitor 2>&1 | tail -100

# Errors only
docker logs bambu-farm-monitor 2>&1 | grep -i error

# MQTT related
docker logs bambu-farm-monitor 2>&1 | grep -i mqtt

# go2rtc related
docker logs bambu-farm-monitor 2>&1 | grep -i go2rtc
```

**5. Browser Console:**
1. Open DevTools (F12)
2. Go to **Console** tab
3. Copy any red error messages
4. Screenshot if helpful

### For Video Issues

**Include:**
- Video shows black screen? Loading forever? Stuttering?
- All printers affected or just some?
- Browser used
- Network speed test results
- Ping to printer: `ping PRINTER_IP`
- RTSP test (if possible)

**Test RTSP directly:**
```bash
# VLC: Open Network Stream
rtsps://bblp:ACCESS_CODE@PRINTER_IP:322/streaming/live/1

# Or with FFmpeg:
ffmpeg -rtsp_transport tcp \
  -i "rtsps://bblp:ACCESS_CODE@PRINTER_IP:322/streaming/live/1" \
  -frames:v 1 test.jpg
```

### For MQTT Issues

**Include:**
- Status shows "Loading status..." or "Disconnected"?
- All printers affected or just some?
- MQTT enabled on printer? (Settings → Network → MQTT → ON)
- Access code correct?
- Serial number correct?

**Test MQTT:**
```bash
# Test port
nc -zv PRINTER_IP 1883

# Test connection via Settings UI
# Click "Test MQTT Connection" button

# Or via API
curl -X POST http://localhost:5001/api/status/mqtt-test/PRINTER_ID
```

### For Performance Issues

**Include:**
- How many printers?
- Server specs (CPU, RAM)
- CPU usage: `docker stats bambu-farm-monitor`
- Network bandwidth available
- Browser performance (DevTools → Performance)

### What NOT to Share

**Keep private:**
- ❌ Access codes (8-digit MQTT password)
- ❌ Serial numbers (if privacy concerned)
- ❌ External IP addresses
- ❌ Passwords or credentials
- ❌ Personal information

**Before sharing config:**
```bash
# Replace sensitive data
sed 's/"access_code": "[^"]*"/"access_code": "XXXXXXXX"/g' config.json
```

## Response Times

**What to expect:**

**GitHub Discussions:**
- Community responses: Hours to days
- Maintainer responses: 1-3 days

**GitHub Issues:**
- Initial triage: 1-3 days
- Bug fixes: Varies by complexity
- Critical bugs: Priority handling

**Note:**
- This is an open-source project
- Responses are best-effort
- Be patient and kind

## Self-Service Troubleshooting

### Quick Fixes

**Try these first:**

**1. Restart Container:**
```bash
docker restart bambu-farm-monitor
```

**2. Check Logs:**
```bash
docker logs bambu-farm-monitor 2>&1 | grep -i error
```

**3. Verify Network:**
```bash
ping PRINTER_IP
curl http://localhost:8080
```

**4. Update to Latest:**
```bash
docker pull neospektra/bambu-farm-monitor:latest
# Recreate container
```

**5. Clear Browser Cache:**
```bash
# Chrome: Ctrl+Shift+Delete
# Select "Cached images and files"
# Clear data
```

### Common Quick Fixes

**Problem: Can't access web UI**
```bash
# Check container running
docker ps | grep bambu

# Check ports
netstat -tulpn | grep 8080

# Try localhost vs IP
curl http://localhost:8080
curl http://SERVER_IP:8080
```

**Problem: Video not loading**
```bash
# Verify printer IP
ping PRINTER_IP

# Check access code
# Settings → Edit printer → Correct code?

# Test go2rtc
curl http://localhost:1984
```

**Problem: Status not updating**
```bash
# Check MQTT enabled on printer
# Settings → Network → MQTT → ON

# Verify serial number
# Settings → Edit printer → Correct serial?

# Test MQTT connection
# Settings → Test MQTT Connection
```

### Debugging Tools

**Container shell access:**
```bash
# Enter container
docker exec -it bambu-farm-monitor sh

# Test network from inside
ping PRINTER_IP
curl http://localhost:5000

# Check files
ls -la /app/config/

# Exit
exit
```

**API testing:**
```bash
# Config API
curl http://localhost:5000/api/config/printers | jq .

# Status API
curl http://localhost:5001/api/status/printers/1 | jq .

# go2rtc API
curl http://localhost:1984/api/streams | jq .
```

**Network testing:**
```bash
# Latency
ping -c 10 PRINTER_IP

# Traceroute
traceroute PRINTER_IP

# Port check
nc -zv PRINTER_IP 322   # RTSP
nc -zv PRINTER_IP 1883  # MQTT
```

## Getting Better Help

### Write Good Questions

**Good question:**
```markdown
Video stream works for Printer 1 but shows black screen for Printer 2.

Environment:
- Ubuntu 22.04, Docker 24.0.5
- Bambu Farm Monitor 3.3.9
- 2x P1S printers on same network
- Both wired ethernet

What I've tried:
1. Verified both IPs are correct (can ping)
2. Verified access codes match (tested in Bambu Studio)
3. Restarted container
4. Checked logs - no errors for Printer 2

Logs:
[relevant logs]

Screenshots:
[showing Printer 1 working, Printer 2 black]
```

**Bad question:**
```markdown
It doesn't work, help!
```

### Be Responsive

**If someone asks for info:**
- Respond promptly
- Provide requested details
- Test suggested solutions
- Report results

**Update your issue/discussion:**
- Mark as solved if fixed
- Share solution for others
- Close if no longer relevant

### Help Others

**Pay it forward:**
- Answer questions if you know
- Share your solutions
- Write tutorials
- Improve documentation

## Emergency Support

**Critical security issues:**
- Email: [security email if available]
- Include "SECURITY" in subject
- Provide details privately
- DO NOT post publicly first

**Urgent production issues:**
- Post in Discussions with [URGENT] tag
- Include impact description
- Provide all requested info
- Be specific about urgency reason

**Note:** "Urgent" should be rare. Most issues can wait for normal support.

## Contributing Support

**You can help by:**
- Answering questions in Discussions
- Improving documentation
- Reporting bugs clearly
- Testing beta versions
- Sharing your setup
- Writing tutorials

See [Contributing](Contributing.md) for details.

## Related Resources

**Documentation:**
- **[Home](Home.md)** - Documentation index
- **[Quick Start](Quick-Start.md)** - Get started fast
- **[Installation Guide](Installation-Guide.md)** - Detailed installation
- **[Common Issues](Common-Issues.md)** - Troubleshooting
- **[FAQ](FAQ.md)** - Frequently asked questions

**Troubleshooting Guides:**
- **[Video Stream Issues](Video-Stream-Issues.md)**
- **[MQTT Connection Problems](MQTT-Connection-Problems.md)**
- **[Performance Optimization](Performance-Optimization.md)**
- **[Debugging Guide](Debugging-Guide.md)**

**Platform-Specific:**
- **[QNAP Installation](QNAP-Installation.md)**
- **[Synology Installation](Synology-Installation.md)**
- **[Unraid Installation](Unraid-Installation.md)**

## Thank You!

Thank you for using Bambu Farm Monitor! We appreciate your:
- Patience with support
- Detailed bug reports
- Feature suggestions
- Community contributions
- Positive feedback

**Happy printing!** 🎉
