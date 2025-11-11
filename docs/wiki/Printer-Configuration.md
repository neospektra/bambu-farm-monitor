# Printer Configuration

How to add, edit, and manage printers after initial setup.

## Overview

The Settings page allows you to manage your printer fleet dynamically without restarting the container. Changes take effect immediately.

## Accessing Settings

Click the **Settings** icon (⚙️) in the top-right corner of the dashboard.

## Managing Printers

### Adding a New Printer

**Steps:**
1. Click **"➕ Add Printer"** button
2. Fill in printer details (see below)
3. Click **"💾 Save All Changes"**
4. MQTT automatically reconnects
5. New printer appears on dashboard

**Printer Details:**

**Name:**
- Friendly identifier
- Displayed on dashboard
- Examples: "Farm P1S #3", "Office X1C"

**IP Address:**
- Format: `192.168.1.100`
- Must be reachable from container
- Recommend static IP or DHCP reservation

**Access Code:**
- 8-digit MQTT password
- Found in: Printer → Settings → Network → MQTT
- Case sensitive (numbers only)

**Serial Number:**
- Format: `01P00A411800001`
- Found in: Printer → Settings → Device
- Recommended for reliable status

### Editing an Existing Printer

**Steps:**
1. Find the printer in the list
2. Modify any field (name, IP, code, serial)
3. Click **"💾 Save All Changes"**
4. Connection automatically updates

**Common Edits:**
- **IP changed:** Update after router DHCP reassignment
- **Access code changed:** Update after regenerating on printer
- **Name change:** Better organization
- **Serial number:** Add if initially omitted

### Removing a Printer

**Steps:**
1. Find the printer in the list
2. Click **"🗑️ Remove"** button next to it
3. Printer is removed from list
4. Click **"💾 Save All Changes"**
5. Printer disappears from dashboard

**Note:** This only removes from Bambu Farm Monitor, doesn't affect the physical printer.

### Reordering Printers

**Current behavior:**
- Printers display in ID order (order added)

**To reorder:**
1. Export configuration
2. Edit JSON file to rearrange array
3. Import configuration

(Future versions may add drag-and-drop reordering)

## Testing Connections

### Test MQTT Connection

**For individual printers:**
1. Find printer in Settings
2. Click **"🔌 Test MQTT Connection"**
3. Wait for result (5-10 seconds)

**Possible Results:**

**✅ Success:**
```
MQTT connection successful
```
- Printer is reachable
- Access code is correct
- MQTT is enabled

**❌ Failure:**
```
Connection refused
```
- Wrong IP or access code
- MQTT disabled on printer
- Network/firewall issue

**Troubleshooting:**
- Verify IP is correct (ping it)
- Check access code (8 digits exactly)
- Ensure MQTT enabled on printer
- Check firewall rules

### Manual Reconnect

**If status seems stuck:**
1. Make any small change (e.g., add space to name)
2. Click **"💾 Save All Changes"**
3. System automatically reconnects all MQTT clients

**Or via API:**
```bash
curl -X POST http://localhost:5001/api/status/reconnect
```

## Configuration File

### Location

Inside container:
```
/app/config/printers.json
```

On host (with volume mount):
```
./config/printers.json  # Docker Compose
bambu-config volume     # Docker run
```

### Format

```json
{
  "printers": [
    {
      "id": 1,
      "name": "Farm P1S #1",
      "ip": "192.168.1.100",
      "access_code": "12345678",
      "serial_number": "01P00A411800001"
    },
    {
      "id": 2,
      "name": "Farm X1C #1",
      "ip": "192.168.1.101",
      "access_code": "87654321",
      "serial_number": "01X00C411800001"
    }
  ]
}
```

### Manual Editing

**Not recommended, but possible:**

1. **Export configuration:**
   ```bash
   docker exec bambu-farm-monitor cat /app/config/printers.json > backup.json
   ```

2. **Edit file:**
   - Use text editor
   - Maintain JSON format
   - Don't break structure

3. **Import back:**
   ```bash
   docker cp backup.json bambu-farm-monitor:/app/config/printers.json
   docker restart bambu-farm-monitor
   ```

**Better approach:** Use Settings UI or API

## Bulk Operations

### Adding Multiple Printers

**Via UI:**
1. Click "➕ Add Printer" for each
2. Fill in details
3. Click "💾 Save All Changes" once at the end

**Via API:**
```bash
curl -X POST http://localhost:5000/api/config/printers/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "printers": [
      {
        "name": "Printer 1",
        "ip": "192.168.1.100",
        "access_code": "12345678",
        "serial_number": "01P00A411800001"
      },
      {
        "name": "Printer 2",
        "ip": "192.168.1.101",
        "access_code": "87654321",
        "serial_number": "01P00A411800002"
      }
    ]
  }'
```

**Via Environment Variables:**

See [Environment Variables](Environment-Variables.md) for pre-configuration at container startup.

### Updating Multiple Printers

**Scenario:** All printers on new subnet

**Via Export/Import:**
1. Export configuration
2. Find and replace in text editor:
   - Find: `192.168.1.`
   - Replace: `192.168.2.`
3. Import updated configuration

**Via API:**
- Use bulk update endpoint
- See [API Documentation](API-Documentation.md)

## Configuration Limits

**Number of Printers:**
- No hard limit
- Tested with 10+ printers
- Performance depends on server hardware

**Recommendations:**
- **1-4 printers:** Any hardware
- **5-8 printers:** 2+ CPU cores, 2 GB+ RAM
- **9-12 printers:** 4+ CPU cores, 4 GB+ RAM
- **13+ printers:** Consider multiple instances

## Best Practices

### 1. Use Static IPs

**Why:**
- Printers won't lose connection if DHCP lease expires
- No need to update configuration after router reboot

**How:**
- Router DHCP reservation (recommended)
- Or static IP on printer network settings

### 2. Descriptive Names

**Good names:**
- "Production P1S AMS-1" (location + model + feature)
- "Shop Floor X1C #2" (location + model + number)
- "R&D A1 Mini" (department + model)

**Poor names:**
- "Printer 1" (not descriptive)
- "asdfg" (meaningless)
- "" (empty - will show as "Printer {id}")

### 3. Document Serial Numbers

**Create a spreadsheet:**
| Printer Name | IP | Serial Number | Access Code | Location |
|--------------|-------------|---------------|-------------|----------|
| Farm P1S #1 | 192.168.1.100 | 01P00... | 12345678 | Lab A |
| Farm X1C #1 | 192.168.1.101 | 01X00... | 87654321 | Lab B |

**Why:**
- Easy reference during troubleshooting
- Quick recovery if configuration lost
- Helpful for firmware updates

### 4. Regular Backups

**Schedule:**
- After adding/removing printers
- Before major changes
- Monthly for active setups

**Method:**
```bash
# Manual
curl -O -J http://localhost:5000/api/config/export

# Automated (cron)
0 0 * * * curl -o /backups/bambu-$(date +\%F).json http://localhost:5000/api/config/export
```

See [Backup and Restore](Backup-and-Restore.md) for details.

### 5. Test After Changes

**After modifying configuration:**
1. ✅ Video streams load
2. ✅ Status updates appear
3. ✅ AMS colors display (if equipped)
4. ✅ Temperatures update

### 6. Keep Access Codes Secure

**Security tips:**
- Don't share screenshots with access codes visible
- Store backups in secure location
- Consider encrypting backup files
- Don't commit to public repositories

## Troubleshooting

### Printer Won't Save

**Symptoms:**
- "Save All Changes" button doesn't work
- Error message appears
- Configuration reverts

**Solutions:**
1. Check all required fields filled
2. Verify access code is 8 digits
3. Check JSON syntax if manually editing
4. Verify volume permissions:
   ```bash
   docker exec bambu-farm-monitor ls -la /app/config
   ```

### Printer Shows After Deletion

**Symptoms:**
- Deleted printer reappears after refresh
- Can't permanently remove

**Solutions:**
1. Clear browser cache
2. Hard refresh (Ctrl+Shift+R)
3. Check configuration file directly
4. Restart container

### Configuration Not Persisting

**Symptoms:**
- Printers disappear after container restart
- Always shows setup wizard

**Solutions:**
1. Verify volume is mounted:
   ```bash
   docker inspect bambu-farm-monitor | grep Mounts -A 10
   ```

2. Check volume exists:
   ```bash
   docker volume ls
   ```

3. Use bind mount instead:
   ```bash
   -v $(pwd)/config:/app/config
   ```

See [Common Issues](Common-Issues.md) for more.

## Advanced Configuration

### Using the API

**Get all printers:**
```bash
curl http://localhost:5000/api/config/printers
```

**Add printer:**
```bash
curl -X POST http://localhost:5000/api/config/printers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Printer",
    "ip": "192.168.1.102",
    "access_code": "11111111",
    "serial_number": "01P00A411800003"
  }'
```

**Update printer:**
```bash
curl -X PUT http://localhost:5000/api/config/printers/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "ip": "192.168.1.100",
    "access_code": "12345678",
    "serial_number": "01P00A411800001"
  }'
```

**Delete printer:**
```bash
curl -X DELETE http://localhost:5000/api/config/printers/1
```

See [API Documentation](API-Documentation.md) for complete reference.

### Environment Variables

**Pre-configure printers at startup:**

```yaml
environment:
  - PRINTER1_IP=192.168.1.100
  - PRINTER1_CODE=12345678
  - PRINTER1_NAME=Farm P1S #1
  - PRINTER1_SERIAL=01P00A411800001
  - PRINTER2_IP=192.168.1.101
  - PRINTER2_CODE=87654321
  - PRINTER2_NAME=Farm P1S #2
  - PRINTER2_SERIAL=01P00A411800002
```

See [Environment Variables](Environment-Variables.md) for details.

## Next Steps

- **[Backup and Restore](Backup-and-Restore.md)** - Protect your configuration
- **[Layout Customization](Layout-Customization.md)** - Arrange your dashboard
- **[MQTT Connection Problems](MQTT-Connection-Problems.md)** - Fix connectivity issues
- **[API Documentation](API-Documentation.md)** - Automate management
