# Podman Deployment

Comprehensive guide for deploying Bambu Farm Monitor using Podman.

## Overview

Podman is a daemonless, rootless container engine that's compatible with Docker. It's ideal for NAS systems (QNAP, Synology) and users who prefer rootless containers. This guide covers deployment with Podman.

## Podman vs Docker

### Key Differences

**Podman:**
- ✅ Daemonless (no background service)
- ✅ Rootless by default (better security)
- ✅ Compatible with Docker commands
- ✅ Pod support (group containers)
- ❌ No Docker Compose native support (but podman-compose exists)

**Docker:**
- ✅ More mature ecosystem
- ✅ Native Docker Compose
- ✅ Wide adoption
- ❌ Requires daemon
- ❌ Typically runs as root

### Command Compatibility

Most Docker commands work with Podman:
```bash
# Docker                    # Podman
docker run                  podman run
docker ps                   podman ps
docker logs                 podman logs
docker exec                 podman exec
docker images               podman images
```

**Alias (if desired):**
```bash
alias docker=podman
```

## Prerequisites

### Install Podman

**Linux (Ubuntu/Debian):**
```bash
# Add repository
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:projectatomic/ppa

# Install Podman
sudo apt-get update
sudo apt-get install -y podman

# Verify
podman --version
```

**Linux (RHEL/CentOS/Fedora):**
```bash
# Fedora
sudo dnf install -y podman

# RHEL/CentOS
sudo yum install -y podman

# Verify
podman --version
```

**macOS:**
```bash
# Install via Homebrew
brew install podman

# Initialize Podman machine
podman machine init
podman machine start

# Verify
podman --version
```

**Windows:**
```powershell
# Install via Chocolatey
choco install podman

# Or download installer from:
# https://github.com/containers/podman/releases

# Initialize Podman machine
podman machine init
podman machine start

# Verify
podman --version
```

**QNAP NAS:**
```bash
# SSH into QNAP
ssh admin@QNAP_IP

# Podman usually pre-installed on newer QTS versions
podman --version

# If not installed, install from App Center
```

**Synology NAS:**
```bash
# SSH into Synology
ssh admin@SYNOLOGY_IP

# Install podman (if available)
sudo synopkg install podman

# Or use Docker instead (Container Manager)
```

### System Requirements

Same as Docker deployment:
- 2 GB RAM minimum (4 GB recommended)
- 1 GB disk space
- x86_64 CPU (ARM not supported)

## Basic Deployment

### Method 1: Simple Podman Run

**Pull image:**
```bash
podman pull docker.io/neospektra/bambu-farm-monitor:latest
```

**Run container:**
```bash
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest
```

**Access:**
```
http://localhost:8080
```

**Note:** Explicitly use `docker.io/` registry prefix with Podman.

### Method 2: Rootless Podman (Recommended)

**Run as non-root user:**
```bash
# No sudo needed
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest
```

**Advantages:**
- Better security
- No root privileges needed
- Isolated containers per user

### Method 3: Podman with Bind Mount

**Create config directory:**
```bash
mkdir -p ~/bambu/config
```

**Run container:**
```bash
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v ~/bambu/config:/app/config:Z \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest
```

**Note:** `:Z` flag sets SELinux context (required on RHEL/Fedora/CentOS).

### Method 4: Podman Compose

**Install podman-compose:**
```bash
# Python pip
pip3 install podman-compose

# Or system package
sudo dnf install podman-compose  # Fedora
sudo apt-get install podman-compose  # Debian/Ubuntu
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  bambu-farm-monitor:
    image: docker.io/neospektra/bambu-farm-monitor:latest
    container_name: bambu-farm-monitor
    ports:
      - "8080:8080"
      - "1984:1984"
      - "5000:5000"
      - "5001:5001"
    volumes:
      - bambu-config:/app/config
    restart: unless-stopped
    environment:
      - TZ=America/New_York

volumes:
  bambu-config:
```

**Deploy:**
```bash
podman-compose up -d
```

**View logs:**
```bash
podman-compose logs -f
```

**Stop:**
```bash
podman-compose down
```

## Port Configuration

**Standard ports (same as Docker):**
- 8080 - Web UI
- 1984 - go2rtc streaming
- 5000 - Config API
- 5001 - Status API

**Custom port mapping:**
```bash
podman run -d \
  --name bambu-farm-monitor \
  -p 8081:8080 \
  -p 1985:1984 \
  -p 5002:5000 \
  -p 5003:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest
```

Access at: `http://localhost:8081`

## Volume Management

### Named Volumes

**Create volume:**
```bash
podman volume create bambu-config
```

**List volumes:**
```bash
podman volume ls
```

**Inspect volume:**
```bash
podman volume inspect bambu-config
```

**Remove volume:**
```bash
podman volume rm bambu-config
```

**Backup volume:**
```bash
podman run --rm \
  -v bambu-config:/source:ro \
  -v $(pwd):/backup:Z \
  alpine tar czf /backup/bambu-backup-$(date +%F).tar.gz -C /source .
```

**Restore volume:**
```bash
podman run --rm \
  -v bambu-config:/target \
  -v $(pwd):/backup:Z \
  alpine sh -c "cd /target && tar xzf /backup/bambu-backup-2025-01-11.tar.gz"
```

### Bind Mounts

**With SELinux context:**
```bash
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v ~/bambu/config:/app/config:Z \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest
```

**Without SELinux:**
```bash
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v ~/bambu/config:/app/config \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest
```

## Systemd Integration

### Create Systemd Service

**Generate service file:**
```bash
# As root (system-wide)
podman generate systemd --new --name bambu-farm-monitor > /etc/systemd/system/bambu-farm-monitor.service

# Or as user (rootless)
mkdir -p ~/.config/systemd/user/
podman generate systemd --new --name bambu-farm-monitor > ~/.config/systemd/user/bambu-farm-monitor.service
```

**Enable service:**
```bash
# System-wide
sudo systemctl daemon-reload
sudo systemctl enable bambu-farm-monitor
sudo systemctl start bambu-farm-monitor

# User service
systemctl --user daemon-reload
systemctl --user enable bambu-farm-monitor
systemctl --user start bambu-farm-monitor
systemctl --user enable-linger $(whoami)  # Start on boot without login
```

**Manage service:**
```bash
# Status
systemctl --user status bambu-farm-monitor

# Stop
systemctl --user stop bambu-farm-monitor

# Restart
systemctl --user restart bambu-farm-monitor

# Logs
journalctl --user -u bambu-farm-monitor -f
```

### Auto-Start on Boot

**User service:**
```bash
# Enable linger (start without login)
loginctl enable-linger $(whoami)

# Enable service
systemctl --user enable bambu-farm-monitor
```

**System service:**
```bash
# Enable and start
sudo systemctl enable --now bambu-farm-monitor
```

## Podman Pods

### Create Pod with Container

**Create pod:**
```bash
podman pod create \
  --name bambu-pod \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001
```

**Run container in pod:**
```bash
podman run -d \
  --pod bambu-pod \
  --name bambu-farm-monitor \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest
```

**Advantages:**
- Share network namespace
- Easier port management
- Group related containers

**Manage pod:**
```bash
# List pods
podman pod ls

# Stop pod
podman pod stop bambu-pod

# Start pod
podman pod start bambu-pod

# Remove pod (and containers)
podman pod rm -f bambu-pod
```

## QNAP Specific

### Deploy on QNAP NAS

**Via SSH:**
```bash
# SSH into QNAP
ssh admin@QNAP_IP

# Pull image
podman pull docker.io/neospektra/bambu-farm-monitor:latest

# Run container
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v /share/Container/bambu-config:/app/config \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest

# Verify
podman ps
```

**Auto-start on QNAP:**
```bash
# Generate systemd service
podman generate systemd --new --name bambu-farm-monitor > /etc/systemd/system/bambu-farm-monitor.service

# Enable service
systemctl enable bambu-farm-monitor
systemctl start bambu-farm-monitor
```

### QNAP Container Station

QNAP Container Station uses Docker, not Podman. See [QNAP Installation](QNAP-Installation.md) for Container Station guide.

## Container Management

### Start/Stop Container

```bash
# Start
podman start bambu-farm-monitor

# Stop
podman stop bambu-farm-monitor

# Restart
podman restart bambu-farm-monitor

# Kill (force stop)
podman kill bambu-farm-monitor

# Remove
podman rm bambu-farm-monitor
```

### View Logs

```bash
# View all logs
podman logs bambu-farm-monitor

# Follow logs (real-time)
podman logs -f bambu-farm-monitor

# Last 100 lines
podman logs --tail 100 bambu-farm-monitor

# Since 10 minutes ago
podman logs --since 10m bambu-farm-monitor
```

### Shell Access

```bash
# Enter container shell
podman exec -it bambu-farm-monitor sh

# Run single command
podman exec bambu-farm-monitor ls -la /app/config

# Run as specific user
podman exec --user root bambu-farm-monitor whoami
```

### Inspect Container

```bash
# Full inspection
podman inspect bambu-farm-monitor

# Get specific field
podman inspect --format='{{.State.Status}}' bambu-farm-monitor

# Get IP address
podman inspect --format='{{.NetworkSettings.IPAddress}}' bambu-farm-monitor
```

### Monitor Resources

```bash
# Real-time stats
podman stats bambu-farm-monitor

# One-time stats
podman stats --no-stream bambu-farm-monitor

# All containers
podman stats
```

## Updating

### Update to Latest Version

```bash
# Pull latest image
podman pull docker.io/neospektra/bambu-farm-monitor:latest

# Stop current container
podman stop bambu-farm-monitor

# Remove current container
podman rm bambu-farm-monitor

# Run new container (same command as before)
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest
```

### Update with Systemd

**If using systemd service:**
```bash
# Stop service
systemctl --user stop bambu-farm-monitor

# Pull new image
podman pull docker.io/neospektra/bambu-farm-monitor:latest

# Regenerate service (picks up new image)
podman generate systemd --new --name bambu-farm-monitor > ~/.config/systemd/user/bambu-farm-monitor.service

# Reload and restart
systemctl --user daemon-reload
systemctl --user start bambu-farm-monitor
```

### Update with Podman Compose

```bash
# Pull latest image
podman-compose pull

# Recreate containers
podman-compose up -d

# View logs
podman-compose logs -f
```

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
podman logs bambu-farm-monitor
```

**Common issues:**
- Port already in use
- Volume permission denied
- SELinux blocking access

**Solutions:**
```bash
# Check what's using port
ss -tulpn | grep 8080

# Fix SELinux context
chcon -R -t container_file_t ~/bambu/config

# Or use :Z flag
podman run -d ... -v ~/bambu/config:/app/config:Z ...
```

### SELinux Issues

**Error:** "Permission denied" when accessing volume

**Solutions:**
```bash
# Option 1: Use :Z flag (recommended)
podman run -d ... -v ~/bambu/config:/app/config:Z ...

# Option 2: Change SELinux context
chcon -R -t container_file_t ~/bambu/config

# Option 3: Set SELinux to permissive (not recommended)
sudo setenforce 0
```

### Rootless Port Binding

**Error:** "Permission denied" binding to port <1024

**Solution:** Use port >1024 or enable rootless port binding:
```bash
# Enable binding to privileged ports (root required once)
echo "net.ipv4.ip_unprivileged_port_start=80" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Now can bind to ports 80+
podman run -d ... -p 80:8080 ...
```

### Cannot Access Web UI

**Check container is running:**
```bash
podman ps | grep bambu
```

**Check from inside container:**
```bash
podman exec bambu-farm-monitor curl -I http://localhost:8080
```

**Check firewall:**
```bash
# Open port in firewall
sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --reload
```

### Configuration Not Persisting

**Check volume:**
```bash
podman inspect bambu-farm-monitor | grep -A 10 Mounts
```

**Verify volume mounted correctly:**
- Named volume: `-v bambu-config:/app/config`
- Bind mount: `-v ~/bambu/config:/app/config:Z`

## Best Practices

### Rootless Containers

**Always prefer rootless:**
```bash
# Run as regular user (no sudo)
podman run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  docker.io/neospektra/bambu-farm-monitor:latest
```

**Benefits:**
- Better security
- No root privileges
- User-specific containers

### Use Systemd Integration

**Enable automatic start:**
```bash
# Create service
podman generate systemd --new --name bambu-farm-monitor > ~/.config/systemd/user/bambu-farm-monitor.service

# Enable and start
systemctl --user daemon-reload
systemctl --user enable --now bambu-farm-monitor
systemctl --user enable-linger $(whoami)
```

### Use SELinux :Z Flag

**On RHEL/Fedora/CentOS:**
```bash
# Always use :Z for bind mounts
podman run -d ... -v ~/bambu/config:/app/config:Z ...
```

### Registry Prefix

**Always specify registry:**
```bash
# Explicit registry
podman pull docker.io/neospektra/bambu-farm-monitor:latest

# Not just
podman pull neospektra/bambu-farm-monitor:latest
```

## Advantages of Podman

### Security

- **Rootless by default** - No root daemon
- **SELinux integration** - Better isolation
- **User namespaces** - Enhanced security

### Compatibility

- **Docker-compatible** - Same commands work
- **OCI compliant** - Standard container format
- **Docker Hub** - Pull from Docker Hub

### Features

- **Daemonless** - No background service
- **Pods** - Group containers like Kubernetes
- **Systemd integration** - Native service management

## Related Documentation

- **[Docker Deployment](Docker-Deployment.md)** - Docker alternative
- **[QNAP Installation](QNAP-Installation.md)** - QNAP specific
- **[Environment Variables](Environment-Variables.md)** - Configuration
- **[Performance Optimization](Performance-Optimization.md)** - Resource optimization
