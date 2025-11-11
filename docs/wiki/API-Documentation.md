# API Documentation

Bambu Farm Monitor provides two REST APIs for programmatic access to printer configuration and status data.

## API Overview

| API | Port | Purpose | Base URL |
|-----|------|---------|----------|
| Config API | 5000 | Manage printer configurations | `http://localhost:5000` |
| Status API | 5001 | Retrieve real-time printer status | `http://localhost:5001` |

**Note:** Both APIs are accessible via the main web UI port (8080) through nginx proxy:
- Config API: `http://localhost:8080/api/config/`
- Status API: `http://localhost:8080/api/status/`

## Authentication

Currently, the APIs do not require authentication. If you expose your installation to the internet, use a reverse proxy with authentication (see [Reverse Proxy Setup](Reverse-Proxy-Setup.md)).

## Configuration API (Port 5000)

Manage printer configurations programmatically.

### Get All Printers

**Endpoint:** `GET /api/config/printers`

**Description:** Retrieve all configured printers

**Response:**
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
      "name": "Farm P1S #2",
      "ip": "192.168.1.101",
      "access_code": "87654321",
      "serial_number": "01P00A411800002"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/config/printers
```

### Get Single Printer

**Endpoint:** `GET /api/config/printers/<id>`

**Description:** Retrieve a specific printer by ID

**Parameters:**
- `id` (integer) - Printer ID

**Response:**
```json
{
  "id": 1,
  "name": "Farm P1S #1",
  "ip": "192.168.1.100",
  "access_code": "12345678",
  "serial_number": "01P00A411800001"
}
```

**Example:**
```bash
curl http://localhost:5000/api/config/printers/1
```

### Add Printer

**Endpoint:** `POST /api/config/printers`

**Description:** Add a new printer

**Request Body:**
```json
{
  "name": "Farm P1S #3",
  "ip": "192.168.1.102",
  "access_code": "11111111",
  "serial_number": "01P00A411800003"
}
```

**Response:**
```json
{
  "id": 3,
  "name": "Farm P1S #3",
  "ip": "192.168.1.102",
  "access_code": "11111111",
  "serial_number": "01P00A411800003"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/config/printers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Farm P1S #3",
    "ip": "192.168.1.102",
    "access_code": "11111111",
    "serial_number": "01P00A411800003"
  }'
```

### Update Printer

**Endpoint:** `PUT /api/config/printers/<id>`

**Description:** Update an existing printer

**Parameters:**
- `id` (integer) - Printer ID

**Request Body:**
```json
{
  "name": "Updated Name",
  "ip": "192.168.1.200",
  "access_code": "99999999",
  "serial_number": "01P00A411800001"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Updated Name",
  "ip": "192.168.1.200",
  "access_code": "99999999",
  "serial_number": "01P00A411800001"
}
```

**Example:**
```bash
curl -X PUT http://localhost:5000/api/config/printers/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "ip": "192.168.1.200",
    "access_code": "99999999",
    "serial_number": "01P00A411800001"
  }'
```

### Delete Printer

**Endpoint:** `DELETE /api/config/printers/<id>`

**Description:** Remove a printer from configuration

**Parameters:**
- `id` (integer) - Printer ID

**Response:**
```json
{
  "message": "Printer deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/config/printers/3
```

### Bulk Create/Update Printers

**Endpoint:** `POST /api/config/printers/bulk`

**Description:** Create or update multiple printers at once

**Request Body:**
```json
{
  "printers": [
    {
      "name": "Farm P1S #1",
      "ip": "192.168.1.100",
      "access_code": "12345678",
      "serial_number": "01P00A411800001"
    },
    {
      "name": "Farm P1S #2",
      "ip": "192.168.1.101",
      "access_code": "87654321",
      "serial_number": "01P00A411800002"
    }
  ]
}
```

**Response:**
```json
{
  "message": "Printers saved successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/config/printers/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "printers": [
      {
        "name": "Farm P1S #1",
        "ip": "192.168.1.100",
        "access_code": "12345678",
        "serial_number": "01P00A411800001"
      }
    ]
  }'
```

### Check Setup Required

**Endpoint:** `GET /api/config/setup-required`

**Description:** Check if initial setup wizard is needed

**Response:**
```json
{
  "setup_required": false
}
```

**Example:**
```bash
curl http://localhost:5000/api/config/setup-required
```

### Export Configuration

**Endpoint:** `GET /api/config/export`

**Description:** Export all printers as JSON file

**Response:** JSON file download with timestamp

**Example:**
```bash
curl -O -J http://localhost:5000/api/config/export
# Downloads: bambu-config-YYYY-MM-DD-HH-MM-SS.json
```

### Import Configuration

**Endpoint:** `POST /api/config/import`

**Description:** Import printers from JSON file

**Request:** multipart/form-data with file upload

**Example:**
```bash
curl -X POST http://localhost:5000/api/config/import \
  -F "file=@bambu-config-2025-01-11-12-00-00.json"
```

## Status API (Port 5001)

Retrieve real-time printer status from MQTT data.

### Get All Printer Statuses

**Endpoint:** `GET /api/status/printers`

**Description:** Retrieve status for all printers

**Response:**
```json
{
  "1": {
    "connected": true,
    "printing": true,
    "print_progress": 45,
    "print_file": "test_print.gcode",
    "print_layer": 120,
    "print_total_layers": 267,
    "print_time_remaining": 145,
    "nozzle_temp": 220.5,
    "bed_temp": 60.2,
    "nozzle_target": 220,
    "bed_target": 60,
    "ams": {
      "has_ams": true,
      "active_tray": "0",
      "humidity": "4",
      "trays": [
        {
          "id": "0",
          "color": "0D6284",
          "type": "PLA",
          "name": "PLA Basic",
          "empty": false
        },
        {
          "id": "1",
          "color": "F330F9",
          "type": "PLA",
          "name": "",
          "empty": false
        }
      ]
    }
  },
  "2": {
    "connected": true,
    "printing": false,
    "print_progress": 0,
    "nozzle_temp": 25.3,
    "bed_temp": 24.8,
    "ams": {
      "has_ams": false
    }
  }
}
```

**Example:**
```bash
curl http://localhost:5001/api/status/printers
```

### Get Single Printer Status

**Endpoint:** `GET /api/status/printers/<id>`

**Description:** Retrieve status for a specific printer

**Parameters:**
- `id` (integer) - Printer ID

**Response:**
```json
{
  "connected": true,
  "printing": true,
  "print_progress": 45,
  "print_file": "test_print.gcode",
  "print_layer": 120,
  "print_total_layers": 267,
  "print_time_remaining": 145,
  "nozzle_temp": 220.5,
  "bed_temp": 60.2,
  "nozzle_target": 220,
  "bed_target": 60,
  "ams": {
    "has_ams": true,
    "active_tray": "0",
    "humidity": "4",
    "trays": [
      {
        "id": "0",
        "color": "0D6284",
        "type": "PLA",
        "name": "PLA Basic",
        "empty": false
      }
    ]
  }
}
```

**Example:**
```bash
curl http://localhost:5001/api/status/printers/1
```

### Reconnect MQTT

**Endpoint:** `POST /api/status/reconnect`

**Description:** Force reconnection of all MQTT clients

**Response:**
```json
{
  "message": "Reconnecting all MQTT clients"
}
```

**Example:**
```bash
curl -X POST http://localhost:5001/api/status/reconnect
```

### Test MQTT Connection

**Endpoint:** `POST /api/status/mqtt-test/<id>`

**Description:** Test MQTT connection for a specific printer

**Parameters:**
- `id` (integer) - Printer ID

**Response (Success):**
```json
{
  "success": true,
  "message": "MQTT connection successful"
}
```

**Response (Failure):**
```json
{
  "success": false,
  "error": "Connection refused"
}
```

**Example:**
```bash
curl -X POST http://localhost:5001/api/status/mqtt-test/1
```

### Get Raw MQTT Data

**Endpoint:** `GET /api/status/raw/<id>`

**Description:** Get raw MQTT message for debugging

**Parameters:**
- `id` (integer) - Printer ID

**Response:**
```json
{
  "print": {
    "ams": {
      "ams": [{
        "humidity": "4",
        "tray": [...]
      }],
      "tray_now": "0"
    },
    "gcode_file": "test_print.gcode",
    "mc_percent": 45,
    "layer_num": 120,
    "total_layer_num": 267,
    "mc_remaining_time": 145
  }
}
```

**Example:**
```bash
curl http://localhost:5001/api/status/raw/1
```

### Health Check

**Endpoint:** `GET /api/health`

**Description:** Check if Status API is running

**Response:**
```json
{
  "status": "healthy"
}
```

**Example:**
```bash
curl http://localhost:5001/api/health
```

## Data Models

### Printer Configuration Object

```typescript
{
  id: number;              // Auto-generated unique ID
  name: string;            // User-friendly name
  ip: string;              // IP address (e.g., "192.168.1.100")
  access_code: string;     // 8-digit MQTT password
  serial_number: string;   // Printer serial number
}
```

### Printer Status Object

```typescript
{
  connected: boolean;           // MQTT connection status
  printing: boolean;            // Currently printing
  print_progress: number;       // 0-100 percentage
  print_file: string;           // Filename of current print
  print_layer: number;          // Current layer number
  print_total_layers: number;   // Total layers in print
  print_time_remaining: number; // Minutes remaining
  nozzle_temp: number;          // Current nozzle temperature (°C)
  bed_temp: number;             // Current bed temperature (°C)
  nozzle_target: number;        // Target nozzle temperature (°C)
  bed_target: number;           // Target bed temperature (°C)
  ams: AMSData;                 // AMS information (if equipped)
}
```

### AMS Data Object

```typescript
{
  has_ams: boolean;      // Printer has AMS
  active_tray: string;   // Currently active tray ID
  humidity: string;      // Humidity percentage
  trays: Array<{
    id: string;          // Tray ID ("0"-"3")
    color: string;       // Hex color (6 chars, no #)
    type: string;        // Filament type (PLA, PETG, etc.)
    name: string;        // Brand/name
    empty: boolean;      // Tray is empty
  }>;
}
```

## Error Responses

All endpoints may return error responses:

```json
{
  "error": "Error message description"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found (printer ID doesn't exist)
- `500` - Internal Server Error

## Rate Limiting

Currently, there are no rate limits on the APIs. For production use, consider implementing rate limiting at the reverse proxy level.

## Example Automation Scripts

### Python: Monitor All Printers

```python
import requests
import time

API_URL = "http://localhost:5001/api/status/printers"

while True:
    response = requests.get(API_URL)
    statuses = response.json()

    for printer_id, status in statuses.items():
        if status['printing']:
            print(f"Printer {printer_id}: {status['print_progress']}% "
                  f"({status['print_layer']}/{status['print_total_layers']} layers)")

    time.sleep(10)  # Update every 10 seconds
```

### Bash: Add Multiple Printers

```bash
#!/bin/bash

API_URL="http://localhost:5000/api/config/printers"

# Array of printers to add
printers=(
  '{"name":"Farm P1S #1","ip":"192.168.1.100","access_code":"12345678","serial_number":"01P00A411800001"}'
  '{"name":"Farm P1S #2","ip":"192.168.1.101","access_code":"87654321","serial_number":"01P00A411800002"}'
  '{"name":"Farm P1S #3","ip":"192.168.1.102","access_code":"11111111","serial_number":"01P00A411800003"}'
)

for printer in "${printers[@]}"; do
  curl -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "$printer"
  echo ""
done
```

### Node.js: Get Print Status

```javascript
const axios = require('axios');

async function getPrinterStatus(printerId) {
  try {
    const response = await axios.get(
      `http://localhost:5001/api/status/printers/${printerId}`
    );

    const status = response.data;

    if (status.printing) {
      console.log(`Printer ${printerId}:`);
      console.log(`  File: ${status.print_file}`);
      console.log(`  Progress: ${status.print_progress}%`);
      console.log(`  Time Remaining: ${status.print_time_remaining} min`);
    } else {
      console.log(`Printer ${printerId}: Idle`);
    }
  } catch (error) {
    console.error(`Error fetching status: ${error.message}`);
  }
}

// Check printer 1 every 30 seconds
setInterval(() => getPrinterStatus(1), 30000);
```

## Next Steps

- **[Environment Variables](Environment-Variables.md)** - Pre-configure printers
- **[Reverse Proxy Setup](Reverse-Proxy-Setup.md)** - Secure your APIs
- **[Contributing](Contributing.md)** - Extend the API
