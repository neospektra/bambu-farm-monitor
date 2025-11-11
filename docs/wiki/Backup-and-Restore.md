# Backup and Restore

Complete guide for backing up and restoring your Bambu Farm Monitor configuration.

## Overview

Your printer configuration is stored in `/app/config/printers.json` inside the container. This guide covers multiple methods to backup, restore, and migrate your configuration.

## Why Backup?

**Protect Against:**
- Accidental deletion of configuration
- Container corruption or failure
- Hardware failure
- Configuration mistakes
- System migrations

**Recovery Scenarios:**
- Restore after container rebuild
- Migrate to new server
- Clone configuration to multiple instances
- Recover from misconfiguration

## What Gets Backed Up

### Included in Backup

**Configuration Data:**
- Printer names
- IP addresses
- Access codes
- Serial numbers
- Printer IDs and order

### NOT Included in Backup

**Runtime Data:**
- Video streams (dynamic)
- Current print status (live from MQTT)
- go2rtc stream configurations (auto-generated)
- Temporary files
- Logs

**Note:** Backups only include configuration, not live data or logs.

## Method 1: Export via Web UI (Easiest)

### Export Configuration

1. Click **Settings** icon (⚙️) in the header
2. Scroll to **Configuration Management** section
3. Click **"📥 Export Configuration"** button
4. Browser downloads `bambu-config-YYYY-MM-DD.json`
5. Save file to safe location

**File Format:**
```json
{
  "printers": [
    {
      "id": 1,
      "name": "Farm P1S #1",
      "ip": "192.168.1.100",
      "access_code": "12345678",
      "serial_number": "01P00A411800001"
    }
  ]
}
```

### Import Configuration

**From Setup Wizard:**
1. Delete existing configuration (if re-initializing)
2. Restart container
3. Setup wizard appears
4. Click **"Import Configuration"**
5. Select backup JSON file
6. Review printers
7. Click **"Complete Setup"**

**From Settings:**
1. Click **Settings** icon (⚙️)
2. Click **"📤 Import Configuration"**
3. Select backup JSON file
4. Printers are added/merged with existing
5. Click **"💾 Save All Changes"**

**Import Behavior:**
- Replaces all existing printers
- Assigns new IDs if conflicts
- Validates all fields
- Errors shown if invalid JSON

## Method 2: API Export/Import

### Export via API

```bash
# Export configuration
curl -o bambu-backup-$(date +%F).json \
  http://localhost:5000/api/config/export

# View exported file
cat bambu-backup-*.json
```

**Response:**
```json
{
  "printers": [...],
  "exported_at": "2025-01-11T10:30:00Z",
  "version": "3.3.9"
}
```

### Import via API

```bash
# Import configuration
curl -X POST http://localhost:5000/api/config/import \
  -H "Content-Type: application/json" \
  -d @bambu-backup-2025-01-11.json

# Verify import
curl http://localhost:5000/api/config/printers
```

**Response:**
```json
{
  "success": true,
  "printers_imported": 4,
  "message": "Configuration imported successfully"
}
```

## Method 3: Direct File Copy

### Backup Configuration File

**Docker with named volume:**
```bash
# Copy from container to host
docker cp bambu-farm-monitor:/app/config/printers.json \
  ./bambu-backup-$(date +%F).json

# Verify backup
cat bambu-backup-*.json
```

**Docker with bind mount:**
```bash
# Configuration is already on host
cp ./config/printers.json \
  ./backups/bambu-backup-$(date +%F).json
```

**Podman:**
```bash
# Copy from container to host
podman cp bambu-farm-monitor:/app/config/printers.json \
  ./bambu-backup-$(date +%F).json
```

### Restore Configuration File

**Docker with named volume:**
```bash
# Stop container
docker stop bambu-farm-monitor

# Copy backup to container
docker cp bambu-backup-2025-01-11.json \
  bambu-farm-monitor:/app/config/printers.json

# Start container
docker start bambu-farm-monitor
```

**Docker with bind mount:**
```bash
# Stop container
docker stop bambu-farm-monitor

# Restore file on host
cp ./backups/bambu-backup-2025-01-11.json \
  ./config/printers.json

# Start container
docker start bambu-farm-monitor
```

**Podman:**
```bash
# Stop container
podman stop bambu-farm-monitor

# Copy backup to container
podman cp bambu-backup-2025-01-11.json \
  bambu-farm-monitor:/app/config/printers.json

# Start container
podman start bambu-farm-monitor
```

## Method 4: Volume Backup

### Backup Docker Volume

**Complete volume backup:**
```bash
# Create backup directory
mkdir -p ./bambu-backups

# Backup entire volume
docker run --rm \
  -v bambu-config:/source:ro \
  -v $(pwd)/bambu-backups:/backup \
  alpine tar czf /backup/bambu-volume-$(date +%F).tar.gz -C /source .

# Verify backup
ls -lh ./bambu-backups/
```

### Restore Docker Volume

**Restore from volume backup:**
```bash
# Stop container
docker stop bambu-farm-monitor

# Restore volume
docker run --rm \
  -v bambu-config:/target \
  -v $(pwd)/bambu-backups:/backup \
  alpine sh -c "cd /target && tar xzf /backup/bambu-volume-2025-01-11.tar.gz"

# Start container
docker start bambu-farm-monitor
```

## Automated Backups

### Daily Backup Script

**Create script:**
```bash
cat > /usr/local/bin/backup-bambu.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/backups/bambu"
DATE=$(date +%F)
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Export configuration via API
curl -s -o "$BACKUP_DIR/bambu-config-$DATE.json" \
  http://localhost:5000/api/config/export

# Verify backup was created
if [ -f "$BACKUP_DIR/bambu-config-$DATE.json" ]; then
    echo "✅ Backup created: bambu-config-$DATE.json"

    # Delete backups older than retention period
    find "$BACKUP_DIR" -name "bambu-config-*.json" \
      -mtime +$RETENTION_DAYS -delete

    echo "✅ Cleaned up backups older than $RETENTION_DAYS days"
else
    echo "❌ Backup failed"
    exit 1
fi
EOF

# Make executable
chmod +x /usr/local/bin/backup-bambu.sh
```

### Schedule with Cron

**Add to crontab:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /usr/local/bin/backup-bambu.sh >> /var/log/bambu-backup.log 2>&1
```

**Test manually:**
```bash
/usr/local/bin/backup-bambu.sh
```

### Schedule on QNAP

**Via Task Scheduler:**
1. **Control Panel** → **System** → **Task Scheduler**
2. Click **"Create"** → **"User-defined script"**
3. Configure:
   - **Task Name:** Bambu Backup
   - **User:** admin
   - **Schedule:** Daily, 2:00 AM
   - **Command:**
     ```bash
     docker exec bambu-farm-monitor cat /app/config/printers.json > \
       /share/Backups/bambu-config-$(date +\%F).json
     ```

### Schedule on Synology

**Via Task Scheduler:**
1. **Control Panel** → **Task Scheduler**
2. **Create** → **Scheduled Task** → **User-defined script**
3. Configure:
   - **Task:** Bambu Backup
   - **User:** root
   - **Schedule:** Daily 02:00
   - **Script:**
     ```bash
     docker exec bambu-farm-monitor cat /app/config/printers.json > \
       /volume1/docker/backups/bambu-config-$(date +\%F).json
     ```

## Migration Scenarios

### Migrate to New Server

**Steps:**
1. **On old server:**
   ```bash
   # Export configuration
   curl -o bambu-config.json http://localhost:5000/api/config/export
   ```

2. **Transfer file:**
   ```bash
   # SCP to new server
   scp bambu-config.json user@new-server:/tmp/
   ```

3. **On new server:**
   ```bash
   # Install Bambu Farm Monitor
   docker pull neospektra/bambu-farm-monitor:latest

   # Run container
   docker run -d \
     --name bambu-farm-monitor \
     -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
     -v bambu-config:/app/config \
     --restart unless-stopped \
     neospektra/bambu-farm-monitor:latest

   # Wait for startup
   sleep 10

   # Import configuration
   curl -X POST http://localhost:5000/api/config/import \
     -H "Content-Type: application/json" \
     -d @/tmp/bambu-config.json
   ```

4. **Verify:**
   - Access web UI: `http://new-server:8080`
   - Check all printers appear
   - Verify video streams work

### Clone to Multiple Instances

**Scenario:** Run multiple monitoring instances with same printers

**Steps:**
1. Export from primary instance
2. Deploy new instance on different server
3. Import same configuration
4. Both instances monitor same printers independently

**Use Cases:**
- Redundancy
- Different viewing locations
- Development/testing
- Remote access setup

### Upgrade Container

**During major version upgrade:**
```bash
# 1. Backup current configuration
docker cp bambu-farm-monitor:/app/config/printers.json \
  ./bambu-backup-before-upgrade.json

# 2. Pull new version
docker pull neospektra/bambu-farm-monitor:latest

# 3. Stop and remove old container
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor

# 4. Run new version (same volume mount)
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest

# 5. Verify configuration persisted
curl http://localhost:5000/api/config/printers
```

**Configuration should persist automatically with volume mount.**

## Backup Best Practices

### 1. Multiple Backup Locations

**Recommended:**
- Local copy on server
- Network share (NAS)
- Cloud storage (encrypted)
- USB drive (offline)

**3-2-1 Rule:**
- **3** copies of data
- **2** different storage types
- **1** off-site backup

### 2. Regular Backup Schedule

**Frequency:**
- **Daily:** Production farms with many printers
- **Weekly:** Home setups with 1-4 printers
- **After changes:** When adding/modifying printers

**Automated is better:**
- Set up cron job
- Use NAS scheduled tasks
- Cloud sync service

### 3. Verify Backups

**Test restoration:**
```bash
# Export backup
curl -o test-backup.json http://localhost:5000/api/config/export

# Verify JSON is valid
jq . test-backup.json

# Check printers array exists
jq '.printers | length' test-backup.json
```

**Periodic restoration test:**
- Restore backup to test instance
- Verify all printers load
- Check no data loss

### 4. Version Control

**Store in Git (without secrets):**
```bash
# Create template (remove sensitive data)
jq '.printers[] | {
  id: .id,
  name: .name,
  ip: "192.168.1.XXX",
  access_code: "XXXXXXXX",
  serial_number: .serial_number
}' bambu-config.json > config-template.json

# Commit template
git add config-template.json
git commit -m "Update printer configuration template"
```

**Why:**
- Track configuration changes over time
- Rollback to previous configurations
- Document printer additions/removals
- Share configuration structure (not secrets)

### 5. Secure Storage

**Encrypt backups:**
```bash
# Encrypt backup
gpg --symmetric --cipher-algo AES256 \
  bambu-config-2025-01-11.json

# Decrypt when needed
gpg --decrypt bambu-config-2025-01-11.json.gpg > \
  bambu-config-2025-01-11.json
```

**Protect access codes:**
- Don't commit to public repositories
- Don't share in screenshots
- Encrypt before cloud upload
- Secure file permissions: `chmod 600`

## Disaster Recovery

### Complete Container Loss

**Scenario:** Container deleted, volume lost

**Recovery:**
```bash
# 1. Reinstall container
docker pull neospektra/bambu-farm-monitor:latest
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest

# 2. Wait for startup
sleep 10

# 3. Restore from backup
curl -X POST http://localhost:5000/api/config/import \
  -H "Content-Type: application/json" \
  -d @./backups/bambu-backup-latest.json

# 4. Verify
curl http://localhost:5000/api/config/printers
```

### Server Hardware Failure

**Scenario:** Server died, need new hardware

**Recovery:**
1. Install Docker on new server
2. Deploy Bambu Farm Monitor container
3. Import configuration from backup
4. Update printer IPs if on different network
5. Verify connectivity

**Time to recovery:** 15-30 minutes with backup

### Configuration Corruption

**Scenario:** Invalid JSON, container won't start

**Recovery:**
```bash
# 1. Stop container
docker stop bambu-farm-monitor

# 2. Backup corrupted file
docker cp bambu-farm-monitor:/app/config/printers.json \
  ./corrupted-config.json

# 3. Restore from backup
docker cp ./backups/bambu-backup-latest.json \
  bambu-farm-monitor:/app/config/printers.json

# 4. Start container
docker start bambu-farm-monitor

# 5. Check logs
docker logs -f bambu-farm-monitor
```

## Troubleshooting

### Export Fails

**Symptoms:**
- Export button does nothing
- API returns error
- Empty file downloaded

**Solutions:**
```bash
# Check config file exists
docker exec bambu-farm-monitor ls -la /app/config/

# Check file permissions
docker exec bambu-farm-monitor cat /app/config/printers.json

# Manual copy as fallback
docker cp bambu-farm-monitor:/app/config/printers.json ./manual-backup.json
```

### Import Fails

**Symptoms:**
- "Invalid JSON" error
- Import does nothing
- Printers don't appear

**Solutions:**
```bash
# Validate JSON syntax
jq . backup-file.json

# Check required fields
jq '.printers[] | {name, ip, access_code, serial_number}' backup-file.json

# Verify structure
jq '.printers | type' backup-file.json  # Should be "array"
```

**Common Issues:**
- Missing closing brace
- Extra comma in JSON
- Wrong field names
- Missing required fields

### Restore Doesn't Persist

**Symptoms:**
- Configuration restored
- Disappears after restart

**Cause:** Volume not mounted properly

**Solutions:**
```bash
# Check volume mount
docker inspect bambu-farm-monitor | grep -A 10 Mounts

# Should see:
# "Destination": "/app/config"

# Recreate with proper volume
docker stop bambu-farm-monitor
docker rm bambu-farm-monitor
# Run with -v bambu-config:/app/config
```

## Next Steps

- **[Printer Configuration](Printer-Configuration.md)** - Managing printers
- **[Environment Variables](Environment-Variables.md)** - Pre-configure at startup
- **[Common Issues](Common-Issues.md)** - Troubleshooting
- **[API Documentation](API-Documentation.md)** - Automate backups via API
