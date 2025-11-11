# Frequently Asked Questions (FAQ)

Common questions about Bambu Farm Monitor.

## General Questions

### What is Bambu Farm Monitor?

Bambu Farm Monitor is a self-hosted web application that allows you to monitor multiple Bambu Lab 3D printers from a single dashboard. It provides real-time video streams, print progress, temperatures, and AMS filament information.

### Which Bambu Lab printers are supported?

All Bambu Lab printers with network connectivity:
- **P1 Series**: P1P, P1S
- **X1 Series**: X1, X1 Carbon, X1E
- **A1 Series**: A1, A1 Mini
- **Any future models** with MQTT support

### Is this an official Bambu Lab product?

No, this is a community-developed open-source project. It is not affiliated with or endorsed by Bambu Lab.

### Is it safe to use?

Yes. The software only reads data from your printers via MQTT. It does not send commands or modify printer settings. Your printer's access code is stored locally and never transmitted to external servers.

### Does it work offline?

Yes, completely. Bambu Farm Monitor runs entirely on your local network. No internet connection is required after installation.

### How many printers can I monitor?

Unlimited. The software has no hard limit on the number of printers. Performance depends on your server hardware and network bandwidth.

## Installation Questions

### Do I need a dedicated server?

No. Bambu Farm Monitor can run on:
- Your desktop/laptop
- Raspberry Pi (2GB+ RAM recommended)
- NAS (QNAP, Synology, Unraid)
- Any device that can run Docker

### What are the minimum system requirements?

**Minimum:**
- 1 CPU core
- 512 MB RAM
- 100 MB disk space
- Network connectivity

**Recommended:**
- 2 CPU cores
- 1 GB RAM
- 500 MB disk space
- Gigabit ethernet

### Can I run this on Windows/Mac directly without Docker?

Not easily. The application is designed for Docker deployment. While it's technically possible to run the components manually, Docker is strongly recommended.

### Can I install this on a Raspberry Pi?

Yes! Use the Docker or Podman installation method. A Raspberry Pi 3B+ or newer with at least 2GB RAM is recommended.

### Do I need to keep my computer on 24/7?

Only if you want 24/7 monitoring. The container can be stopped and started as needed. If using a NAS, it can run continuously without a dedicated computer.

## Configuration Questions

### Where do I find my printer's IP address?

See the detailed guide: [Finding Printer Information](Finding-Printer-Information.md)

**Quick method:** Check your printer's touchscreen:
- Settings → Network → Connection Info

### What is the access code?

The access code is an 8-digit MQTT password found in:
- Printer Settings → Network → MQTT

If MQTT is disabled, enable it and the code will be displayed.

### Do I need the serial number?

It's recommended but not required. The serial number helps ensure status updates are properly routed. Without it, status may be less reliable.

### Can I use hostnames instead of IP addresses?

Not recommended. IP addresses are more reliable. If you use hostnames, ensure they resolve correctly from inside the Docker container.

### How do I set a static IP for my printer?

Set a DHCP reservation in your router:
1. Find your printer's MAC address
2. Router settings → DHCP → Reservations
3. Reserve the current IP for that MAC address

### Can I monitor printers on different networks?

Yes, but they must be routable from your server. VLANs are fine if routing is configured. Printers on completely separate networks (different sites) would require VPN or port forwarding.

## Feature Questions

### Can I control my printers (pause, cancel, start prints)?

No. Bambu Farm Monitor is read-only. It does not send commands to printers. Use Bambu Studio or Bambu Handy app for printer control.

### Can I upload files to print?

No. This is a monitoring tool only. Use Bambu Studio to slice and send prints to your printers.

### Can I view print history?

Not currently. The application shows real-time status only. Print history may be added in a future version.

### Can I set up notifications?

Not built-in, but you can use the [API](API-Documentation.md) to integrate with notification services like:
- Pushover
- Discord webhooks
- Email (via custom script)
- Home Assistant

### Can I view the camera feed remotely?

Yes, if you:
1. Set up port forwarding on your router (not recommended)
2. Use a VPN (recommended) - WireGuard, Tailscale, or similar
3. Set up a reverse proxy with authentication

**Security warning:** Do not expose the application directly to the internet without authentication.

### Does it support multiple users?

The application itself has no user authentication. If you need multi-user access:
1. Set up a reverse proxy (nginx, Caddy, Traefik)
2. Configure HTTP authentication
3. All users see the same dashboard

### Can I customize the layout?

Yes! Use the layout selector to choose:
- Auto Grid (responsive)
- 1 Column
- 2x2 Grid
- 2 Columns
- 3 Columns
- 4 Columns

Your preference is saved to browser localStorage.

### Can I resize individual printer windows?

Yes. Each printer card has a resize handle in the bottom-right corner. Drag to resize.

## Technical Questions

### What technology stack is used?

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Backend**: Python (Flask)
- **Video Streaming**: go2rtc (WebRTC)
- **Web Server**: nginx
- **MQTT Client**: Python paho-mqtt
- **Container**: Docker/Podman

### What ports does it use?

- **8080** - Web UI (HTTP)
- **1984** - go2rtc WebRTC streaming
- **5000** - Configuration API
- **5001** - Status API

All can be remapped if needed.

### How does video streaming work?

1. BambuSource2Raw captures RTSP stream from printer
2. go2rtc transcodes to WebRTC
3. Browser displays WebRTC stream via MSE (Media Source Extensions)

This provides low-latency live streaming without plugins.

### How does status monitoring work?

1. Python MQTT client connects to each printer
2. Subscribes to `device/{serial}/report` topic
3. Parses JSON messages for status data
4. Exposes data via REST API
5. Frontend polls API every 2 seconds

### Is HTTPS supported?

Not built-in. Use a reverse proxy (nginx, Caddy, Traefik) for HTTPS. See [Reverse Proxy Setup](Reverse-Proxy-Setup.md).

### Can I use this with my existing reverse proxy?

Yes! The application works behind reverse proxies. Make sure to:
1. Proxy all ports (8080, 1984, 5000, 5001)
2. Enable WebSocket support for video streaming
3. Increase proxy timeouts for long-running streams

### Does it support IPv6?

Yes, Docker and the application support IPv6. Your printer must also support IPv6.

### Can I run multiple instances?

Yes, but each instance needs different ports. Use case: separate instances for different printer groups.

## Troubleshooting Questions

### Why is my video stream black?

**Common causes:**
1. Wrong IP address
2. Wrong access code
3. Firewall blocking connections
4. Printer camera is off
5. MQTT disabled on printer

See [Video Stream Issues](Video-Stream-Issues.md) for detailed troubleshooting.

### Why does status show "Loading status..."?

**Common causes:**
1. Missing or incorrect serial number
2. MQTT not enabled on printer
3. Wrong access code
4. Network connectivity issues

See [MQTT Connection Problems](MQTT-Connection-Problems.md).

### Why don't AMS colors show?

**Common causes:**
1. Printer doesn't have AMS
2. Old version (update to v3.3.3+)
3. AMS not detected by printer
4. MQTT connection issue

See [Common Issues](Common-Issues.md#ams-colors-not-showing).

### Can I see the logs?

Yes:
```bash
docker logs bambu-farm-monitor

# Follow logs in real-time
docker logs -f bambu-farm-monitor

# Last 100 lines
docker logs --tail 100 bambu-farm-monitor
```

### How do I reset everything?

**Reset configuration (keeps container):**
```bash
docker exec bambu-farm-monitor rm /app/config/printers.json
docker restart bambu-farm-monitor
```

**Complete reset:**
```bash
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
docker volume rm bambu-config
# Then reinstall
```

### How do I update to the latest version?

```bash
docker pull neospektra/bambu-farm-monitor:latest
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# Run docker run command again (same as installation)
```

Or with Docker Compose:
```bash
docker-compose pull
docker-compose up -d
```

## Performance Questions

### How much bandwidth does it use?

**Per stream:**
- Video: 2-5 Mbps
- Status: < 1 Kbps

**For 4 printers:** ~10-20 Mbps total

### Why is my CPU usage high?

Video transcoding is CPU-intensive. Each active stream uses ~10-20% CPU.

**Solutions:**
- Close printer views you're not watching
- Use the layout selector to show fewer printers
- Upgrade server hardware
- Consider hardware acceleration (advanced)

### Can I reduce video quality to save bandwidth?

Not currently configurable in the UI. Advanced users can modify go2rtc.yaml configuration.

### Does it work on slow internet?

The application runs on your local network and doesn't require internet. However, video streaming requires good WiFi signal to your printers.

## Security Questions

### Is my data sent to the cloud?

No. Everything runs locally. No data is sent to external servers.

### Can others access my cameras?

Only if you:
1. Expose ports to the internet (not recommended)
2. Grant access via VPN or reverse proxy

By default, the application is only accessible on your local network.

### Should I expose this to the internet?

**Not directly.** If you need remote access:
1. **Best:** Use a VPN (WireGuard, Tailscale)
2. **Good:** Reverse proxy with authentication
3. **Bad:** Direct port forwarding (security risk)

See [Security Best Practices](Security-Best-Practices.md).

### Are access codes stored securely?

Access codes are stored in plain text in `/app/config/printers.json`. The file is only accessible inside the container and on the host volume.

For additional security:
1. Restrict access to the config directory
2. Use Docker secrets (advanced)
3. Encrypt the volume (advanced)

### Can someone hack my printers through this?

Extremely unlikely. The application only reads MQTT data. It does not:
- Send commands to printers
- Modify printer firmware
- Open additional ports
- Accept incoming connections

## Support Questions

### Where can I get help?

1. **Documentation:** Start with this wiki
2. **Common Issues:** [Common Issues](Common-Issues.md)
3. **Discussions:** https://github.com/neospektra/bambu-farm-monitor/discussions
4. **Bug Reports:** https://github.com/neospektra/bambu-farm-monitor/issues

### How do I report a bug?

1. Check [Common Issues](Common-Issues.md) first
2. Search [existing issues](https://github.com/neospektra/bambu-farm-monitor/issues)
3. If new, [open an issue](https://github.com/neospektra/bambu-farm-monitor/issues/new)

Include:
- Version number (check footer)
- Platform (Docker, QNAP, Synology, etc.)
- Full error messages
- Steps to reproduce
- Relevant logs

### How do I request a feature?

1. Check if it's already requested in [Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
2. If not, start a new discussion in "Ideas" category
3. Describe the feature and use case

### Can I contribute?

Yes! See [Contributing](Contributing.md) for guidelines.

Contributions welcome:
- Code (features, bug fixes)
- Documentation
- Testing
- Translations
- Bug reports

### Is there a Discord/Slack/forum?

Currently, all community interaction happens on GitHub:
- **Discussions:** General questions, feature requests
- **Issues:** Bug reports, specific problems

## License Questions

### What license is this released under?

MIT License. See [LICENSE](https://github.com/neospektra/bambu-farm-monitor/blob/main/LICENSE) file.

### Can I use this commercially?

Yes. The MIT license allows commercial use.

### Can I modify the code?

Yes. You can modify, fork, and redistribute under the MIT license terms.

### Do I need to credit the original authors?

Not required, but appreciated! Include a link to the GitHub repository if you fork or redistribute.

## Still Have Questions?

- **Search the wiki:** Use the search bar at the top
- **Ask in Discussions:** https://github.com/neospektra/bambu-farm-monitor/discussions
- **Check the issues:** Someone may have asked already
- **Read the docs:** Most questions are answered in the guides

---

**Related Pages:**
- [Installation Guide](Installation-Guide.md)
- [Common Issues](Common-Issues.md)
- [API Documentation](API-Documentation.md)
- [Support](Support.md)
