# Docker Deployment

Comprehensive guide for deploying Bambu Farm Monitor using Docker.

## Overview

Bambu Farm Monitor is distributed as a Docker container image, making it easy to deploy on any platform that supports Docker. This guide covers deployment methods, configuration, and best practices.

## Prerequisites

### Docker Installation

**Linux (Ubuntu/Debian):**
```bash
# Update packages
sudo apt-get update

# Install dependencies
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Verify installation
docker --version
sudo docker run hello-world
```

**Linux (RHEL/CentOS/Fedora):**
```bash
# Install Docker
sudo dnf install -y docker

# Or for older versions
sudo yum install -y docker

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify
docker --version
```

**macOS:**
```bash
# Download Docker Desktop from:
# https://www.docker.com/products/docker-desktop/

# Or use Homebrew
brew install --cask docker

# Launch Docker Desktop
open -a Docker

# Verify
docker --version
```

**Windows:**
```powershell
# Download Docker Desktop from:
# https://www.docker.com/products/docker-desktop/

# Or use Chocolatey
choco install docker-desktop

# Launch Docker Desktop
# Verify in PowerShell:
docker --version
```

### System Requirements

**Minimum:**
- Docker 20.10+
- 2 GB RAM
- 1 GB disk space
- x86_64 CPU (ARM not supported)

**Recommended:**
- Docker 24.0+
- 4 GB RAM
- 10 GB disk space
- Multi-core CPU

## Image Information

### Docker Hub Repository

**Official Image:**
```
neospektra/bambu-farm-monitor:latest
```

**Docker Hub URL:**
https://hub.docker.com/r/neospektra/bambu-farm-monitor

### Available Tags

**`:latest`** - Most recent stable release
```bash
docker pull neospektra/bambu-farm-monitor:latest
```

**`:3.3.9`** - Specific version
```bash
docker pull neospektra/bambu-farm-monitor:3.3.9
```

**`:dev`** - Development builds (not recommended for production)
```bash
docker pull neospektra/bambu-farm-monitor:dev
```

### Image Details

**Base Image:** Alpine Linux
**Size:** ~500 MB
**Architecture:** amd64/x86_64
**Includes:**
- Python 3.11
- Flask (APIs)
- React (Frontend)
- go2rtc (Video streaming)
- paho-mqtt (MQTT client)

## Deployment Methods

### Method 1: Basic Docker Run

**Pull image:**
```bash
docker pull neospektra/bambu-farm-monitor:latest
```

**Run container:**
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

**Access:**
```
http://localhost:8080
```

### Method 2: Docker Run with Bind Mount

**Create config directory:**
```bash
mkdir -p ./config
```

**Run container:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v $(pwd)/config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Advantage:** Configuration accessible on host at `./config/printers.json`

### Method 3: Docker Compose (Recommended)

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  bambu-farm-monitor:
    image: neospektra/bambu-farm-monitor:latest
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
      - TZ=America/New_York  # Optional: Set timezone

volumes:
  bambu-config:
```

**Deploy:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop:**
```bash
docker-compose down
```

### Method 4: Docker Compose with Bind Mount

**Create directory:**
```bash
mkdir -p ./config
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  bambu-farm-monitor:
    image: neospektra/bambu-farm-monitor:latest
    container_name: bambu-farm-monitor
    ports:
      - "8080:8080"
      - "1984:1984"
      - "5000:5000"
      - "5001:5001"
    volumes:
      - ./config:/app/config
    restart: unless-stopped
    environment:
      - TZ=America/New_York
```

**Deploy:**
```bash
docker-compose up -d
```

### Method 5: Docker Stack (Swarm Mode)

**Create `stack.yml`:**
```yaml
version: '3.8'

services:
  bambu-farm-monitor:
    image: neospektra/bambu-farm-monitor:latest
    ports:
      - "8080:8080"
      - "1984:1984"
      - "5000:5000"
      - "5001:5001"
    volumes:
      - bambu-config:/app/config
    deploy:
      replicas: 1
      restart_policy:
        condition: any
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

volumes:
  bambu-config:
```

**Deploy:**
```bash
docker stack deploy -c stack.yml bambu
```

**Check:**
```bash
docker stack services bambu
docker service logs bambu_bambu-farm-monitor
```

**Remove:**
```bash
docker stack rm bambu
```

## Port Configuration

### Required Ports

**8080 (TCP)** - Web UI
- Access dashboard
- Settings interface
- Main application

**1984 (TCP)** - go2rtc Streaming
- WebRTC video streams
- Video player connections
- Stream management API

**5000 (TCP)** - Configuration API
- Printer configuration
- Settings management
- Export/import config

**5001 (TCP)** - Status API
- Real-time printer status
- MQTT data exposure
- Progress updates

### Custom Port Mapping

**Change web UI port:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8081:8080 \
  -p 1984:1984 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

Access at: `http://localhost:8081`

**Change all ports:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 9080:8080 \
  -p 9984:1984 \
  -p 9000:5000 \
  -p 9001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

## Volume Management

### Named Volumes (Recommended)

**Create volume:**
```bash
docker volume create bambu-config
```

**Use in container:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Inspect volume:**
```bash
docker volume inspect bambu-config
```

**Backup volume:**
```bash
docker run --rm \
  -v bambu-config:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/bambu-backup-$(date +%F).tar.gz -C /source .
```

**Restore volume:**
```bash
docker run --rm \
  -v bambu-config:/target \
  -v $(pwd):/backup \
  alpine sh -c "cd /target && tar xzf /backup/bambu-backup-2025-01-11.tar.gz"
```

### Bind Mounts

**Relative path:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v ./config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Absolute path:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v /home/user/bambu/config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Permissions:**
```bash
# Ensure directory is writable
mkdir -p ./config
chmod 777 ./config
```

## Network Configuration

### Bridge Network (Default)

**Automatic:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

Container gets its own IP on default bridge network.

### Custom Bridge Network

**Create network:**
```bash
docker network create bambu-net
```

**Run container:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  --network bambu-net \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

### Host Network

**Use host network (Linux only):**
```bash
docker run -d \
  --name bambu-farm-monitor \
  --network host \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Note:** Port mapping not needed with host network. Container uses host's network directly.

### macvlan Network (Advanced)

**Create macvlan network:**
```bash
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  bambu-macvlan
```

**Run container:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  --network bambu-macvlan \
  --ip 192.168.1.200 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

Container gets its own MAC address and appears as separate device on network.

## Resource Limits

### Set CPU Limits

**Limit to 2 CPUs:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  --cpus=2.0 \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Set CPU shares (relative weight):**
```bash
docker run -d \
  --name bambu-farm-monitor \
  --cpu-shares=1024 \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

### Set Memory Limits

**Limit to 2 GB:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  --memory=2g \
  --memory-swap=4g \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

### Combined Resource Limits

**Docker Compose:**
```yaml
version: '3.8'

services:
  bambu-farm-monitor:
    image: neospektra/bambu-farm-monitor:latest
    container_name: bambu-farm-monitor
    ports:
      - "8080:8080"
      - "1984:1984"
      - "5000:5000"
      - "5001:5001"
    volumes:
      - bambu-config:/app/config
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

volumes:
  bambu-config:
```

## Container Management

### Start/Stop Container

```bash
# Start
docker start bambu-farm-monitor

# Stop
docker stop bambu-farm-monitor

# Restart
docker restart bambu-farm-monitor

# Pause (suspend)
docker pause bambu-farm-monitor

# Unpause
docker unpause bambu-farm-monitor
```

### View Logs

```bash
# View all logs
docker logs bambu-farm-monitor

# Follow logs (real-time)
docker logs -f bambu-farm-monitor

# Last 100 lines
docker logs --tail 100 bambu-farm-monitor

# Logs with timestamps
docker logs -t bambu-farm-monitor

# Logs since 10 minutes ago
docker logs --since 10m bambu-farm-monitor
```

### Container Shell Access

```bash
# Enter container shell
docker exec -it bambu-farm-monitor sh

# Run single command
docker exec bambu-farm-monitor ls -la /app/config

# Run as specific user
docker exec -u root bambu-farm-monitor whoami
```

### Inspect Container

```bash
# Full inspection
docker inspect bambu-farm-monitor

# Get specific field
docker inspect --format='{{.State.Status}}' bambu-farm-monitor

# Get IP address
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' bambu-farm-monitor
```

### Monitor Resource Usage

```bash
# Real-time stats
docker stats bambu-farm-monitor

# One-time stats
docker stats --no-stream bambu-farm-monitor

# All containers
docker stats
```

## Updating

### Update to Latest Version

```bash
# Pull latest image
docker pull neospektra/bambu-farm-monitor:latest

# Stop current container
docker stop bambu-farm-monitor

# Remove current container
docker rm bambu-farm-monitor

# Run new container (same command as before)
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Note:** Configuration persists in volume.

### Update with Docker Compose

```bash
# Pull latest image
docker-compose pull

# Recreate containers
docker-compose up -d

# View logs
docker-compose logs -f
```

### Rollback to Previous Version

```bash
# Stop current
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor

# Run specific version
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:3.3.8
```

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker logs bambu-farm-monitor
```

**Common issues:**
- Port already in use
- Volume permission denied
- Insufficient resources

**Solutions:**
```bash
# Check what's using port
sudo netstat -tulpn | grep 8080

# Fix volume permissions
chmod 777 ./config

# Check available resources
docker system df
```

### Cannot Access Web UI

**Check container is running:**
```bash
docker ps | grep bambu
```

**Check from inside container:**
```bash
docker exec bambu-farm-monitor curl -I http://localhost:8080
```

**Check port mapping:**
```bash
docker port bambu-farm-monitor
```

### High Resource Usage

**Check stats:**
```bash
docker stats bambu-farm-monitor
```

**Apply limits:**
```bash
docker update --cpus=2 --memory=2g bambu-farm-monitor
```

### Configuration Not Persisting

**Check volume:**
```bash
docker inspect bambu-farm-monitor | grep -A 10 Mounts
```

**Ensure volume mounted:**
- Named volume: `-v bambu-config:/app/config`
- Bind mount: `-v $(pwd)/config:/app/config`

## Best Practices

### Always Use

- ✅ Named volumes or bind mounts for persistence
- ✅ `--restart unless-stopped` for auto-start
- ✅ Latest stable tag (or specific version)
- ✅ Resource limits in production
- ✅ Docker Compose for easier management

### Avoid

- ❌ Running without volume (loses config on restart)
- ❌ Using `:latest` in production without testing
- ❌ Excessive resource limits (causes performance issues)
- ❌ Host network mode unless necessary
- ❌ Running as privileged unless required

## Related Documentation

- **[Podman Deployment](Podman-Deployment.md)** - Podman alternative
- **[Environment Variables](Environment-Variables.md)** - Configuration via env vars
- **[Installation Guide](Installation-Guide.md)** - General installation
- **[Performance Optimization](Performance-Optimization.md)** - Resource optimization
