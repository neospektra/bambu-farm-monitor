# Environment Variables

Complete reference for configuring Bambu Farm Monitor using environment variables.

## Overview

Environment variables allow you to pre-configure printers when starting the container, bypassing the setup wizard. This is useful for automation, deployment scripts, and infrastructure-as-code.

## Configuration Methods

### Method 1: Environment Variables (Pre-configuration)

Configure printers before first run using environment variables.

### Method 2: Setup Wizard (Interactive)

Use the web-based setup wizard on first run.

### Method 3: Configuration File (Manual)

Directly edit `/app/config/printers.json` inside container.

### Method 4: API (Programmatic)

Use REST API to configure printers dynamically.

**This guide focuses on Method 1 (Environment Variables).**

## Printer Configuration Variables

### Variable Format

**Pattern:**
```
PRINTER{N}_{FIELD}=value
```

**Where:**
- `{N}` = Printer number (1, 2, 3, ...)
- `{FIELD}` = Configuration field (IP, CODE, NAME, SERIAL)

### Required Variables Per Printer

**PRINTER{N}_IP**
- Printer IP address
- Format: `192.168.1.100`
- Example: `PRINTER1_IP=192.168.1.100`

**PRINTER{N}_CODE**
- 8-digit MQTT access code
- Format: `12345678`
- Example: `PRINTER1_CODE=12345678`

### Optional Variables Per Printer

**PRINTER{N}_NAME**
- Friendly printer name
- Default: `Printer {N}`
- Example: `PRINTER1_NAME="Farm P1S #1"`

**PRINTER{N}_SERIAL**
- Printer serial number
- Recommended for reliable status
- Format: `01P00A411800001`
- Example: `PRINTER1_SERIAL=01P00A411800001`

## Examples

### Single Printer

**Docker run:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  -e PRINTER1_IP=192.168.1.100 \
  -e PRINTER1_CODE=12345678 \
  -e PRINTER1_NAME="My P1S" \
  -e PRINTER1_SERIAL=01P00A411800001 \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

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
    environment:
      - PRINTER1_IP=192.168.1.100
      - PRINTER1_CODE=12345678
      - PRINTER1_NAME=My P1S
      - PRINTER1_SERIAL=01P00A411800001
    restart: unless-stopped

volumes:
  bambu-config:
```

### Multiple Printers

**Docker run:**
```bash
docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  -e PRINTER1_IP=192.168.1.100 \
  -e PRINTER1_CODE=12345678 \
  -e PRINTER1_NAME="Farm P1S #1" \
  -e PRINTER1_SERIAL=01P00A411800001 \
  -e PRINTER2_IP=192.168.1.101 \
  -e PRINTER2_CODE=87654321 \
  -e PRINTER2_NAME="Farm P1S #2" \
  -e PRINTER2_SERIAL=01P00A411800002 \
  -e PRINTER3_IP=192.168.1.102 \
  -e PRINTER3_CODE=11111111 \
  -e PRINTER3_NAME="Farm X1C #1" \
  -e PRINTER3_SERIAL=01X00C411800001 \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

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
    environment:
      # Printer 1
      - PRINTER1_IP=192.168.1.100
      - PRINTER1_CODE=12345678
      - PRINTER1_NAME=Farm P1S #1
      - PRINTER1_SERIAL=01P00A411800001

      # Printer 2
      - PRINTER2_IP=192.168.1.101
      - PRINTER2_CODE=87654321
      - PRINTER2_NAME=Farm P1S #2
      - PRINTER2_SERIAL=01P00A411800002

      # Printer 3
      - PRINTER3_IP=192.168.1.102
      - PRINTER3_CODE=11111111
      - PRINTER3_NAME=Farm X1C #1
      - PRINTER3_SERIAL=01X00C411800001

      # Printer 4
      - PRINTER4_IP=192.168.1.103
      - PRINTER4_CODE=22222222
      - PRINTER4_NAME=Farm X1C #2
      - PRINTER4_SERIAL=01X00C411800002
    restart: unless-stopped

volumes:
  bambu-config:
```

### Using .env File

**Create `.env` file:**
```bash
# .env
PRINTER1_IP=192.168.1.100
PRINTER1_CODE=12345678
PRINTER1_NAME=Farm P1S #1
PRINTER1_SERIAL=01P00A411800001

PRINTER2_IP=192.168.1.101
PRINTER2_CODE=87654321
PRINTER2_NAME=Farm P1S #2
PRINTER2_SERIAL=01P00A411800002

PRINTER3_IP=192.168.1.102
PRINTER3_CODE=11111111
PRINTER3_NAME=Farm X1C #1
PRINTER3_SERIAL=01X00C411800001
```

**Docker Compose with .env:**
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
    env_file:
      - .env
    restart: unless-stopped

volumes:
  bambu-config:
```

**Run:**
```bash
docker-compose up -d
```

## Platform-Specific Configuration

### QNAP Container Station

**Via GUI:**
1. Container Station → Create Container
2. Advanced Settings → Environment
3. Add each variable:
   - Variable: `PRINTER1_IP`
   - Value: `192.168.1.100`
4. Repeat for all variables

**Via docker-compose.yml:**
Place file in `/share/Container/bambu-monitor/docker-compose.yml`
```bash
cd /share/Container/bambu-monitor
docker-compose up -d
```

### Synology Container Manager

**Via GUI (DSM 7):**
1. Container Manager → Create Container
2. Advanced Settings → Environment
3. Add each variable

**Via docker-compose:**
Place file in `/volume1/docker/bambu-monitor/docker-compose.yml`
```bash
cd /volume1/docker/bambu-monitor
sudo docker-compose up -d
```

### Unraid

**Via Template:**
1. Docker tab → Add Container
2. Add Variable for each:
   - Config Type: Variable
   - Name: PRINTER1_IP
   - Key: PRINTER1_IP
   - Value: 192.168.1.100

**Via docker-compose:**
1. Install "Docker Compose Manager" plugin
2. Create compose file
3. Deploy

## Behavior and Priority

### Configuration Priority

**Order of precedence (highest to lowest):**
1. Existing configuration file (`/app/config/printers.json`)
2. Environment variables
3. Setup wizard

### First Run Behavior

**If config file doesn't exist:**
- Environment variables are processed
- Printers auto-configured
- Config file created
- Setup wizard skipped

**If config file exists:**
- Environment variables ignored
- Existing configuration used
- Can add more via Settings UI

### Updating Configuration

**To change configuration:**
1. Stop container
2. Delete config file:
   ```bash
   docker exec bambu-farm-monitor rm /app/config/printers.json
   ```
3. Update environment variables
4. Start container
5. New configuration applied

**Or use Settings UI:**
- Modify via web interface
- No container restart needed
- Environment variables not consulted

## Validation and Errors

### Variable Validation

**IP Address:**
- Must be valid IPv4 format
- Example: `192.168.1.100`
- Invalid: `192.168.1` or `printer.local`

**Access Code:**
- Must be exactly 8 digits
- Example: `12345678`
- Invalid: `1234` or `abcd1234`

**Serial Number:**
- Typically 15 characters
- Format: `01P00A411800001`
- Optional but recommended

### Error Handling

**Missing required variables:**
```bash
# Will fail - missing CODE
docker run -d \
  -e PRINTER1_IP=192.168.1.100 \
  bambu-farm-monitor:latest

# Error in logs:
# "PRINTER1_CODE not set, skipping printer 1"
```

**Invalid format:**
```bash
# Will fail - invalid IP
docker run -d \
  -e PRINTER1_IP=invalid \
  -e PRINTER1_CODE=12345678 \
  bambu-farm-monitor:latest

# Error in logs:
# "Invalid IP address for printer 1"
```

### Checking Logs

```bash
# Check if configuration loaded
docker logs bambu-farm-monitor 2>&1 | grep "Loaded.*printer"

# Expected output:
# "Loaded 3 printers from environment variables"

# Check for errors
docker logs bambu-farm-monitor 2>&1 | grep -i "error.*printer"
```

## Advanced Scenarios

### Templating with Scripts

**Bash script to generate config:**
```bash
#!/bin/bash

# printers.sh
declare -A PRINTERS=(
  [1]="192.168.1.100:12345678:Farm P1S #1:01P00A411800001"
  [2]="192.168.1.101:87654321:Farm P1S #2:01P00A411800002"
  [3]="192.168.1.102:11111111:Farm X1C #1:01X00C411800001"
)

ENV_VARS=""
for id in "${!PRINTERS[@]}"; do
  IFS=':' read -r ip code name serial <<< "${PRINTERS[$id]}"
  ENV_VARS="$ENV_VARS -e PRINTER${id}_IP=$ip"
  ENV_VARS="$ENV_VARS -e PRINTER${id}_CODE=$code"
  ENV_VARS="$ENV_VARS -e PRINTER${id}_NAME=\"$name\""
  ENV_VARS="$ENV_VARS -e PRINTER${id}_SERIAL=$serial"
done

docker run -d \
  --name bambu-farm-monitor \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v bambu-config:/app/config \
  $ENV_VARS \
  --restart unless-stopped \
  neospektra/bambu-farm-monitor:latest
```

**Run:**
```bash
chmod +x printers.sh
./printers.sh
```

### Secret Management

**Using Docker Secrets:**
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
    environment:
      - PRINTER1_IP=192.168.1.100
      - PRINTER1_CODE_FILE=/run/secrets/printer1_code
      - PRINTER1_NAME=Farm P1S #1
      - PRINTER1_SERIAL=01P00A411800001
    secrets:
      - printer1_code
    restart: unless-stopped

secrets:
  printer1_code:
    file: ./secrets/printer1_code.txt

volumes:
  bambu-config:
```

**Note:** Docker secrets support would require custom implementation in the application.

### Infrastructure as Code

**Terraform example:**
```hcl
# main.tf
resource "docker_container" "bambu_farm_monitor" {
  name  = "bambu-farm-monitor"
  image = "neospektra/bambu-farm-monitor:latest"

  ports {
    internal = 8080
    external = 8080
  }

  ports {
    internal = 1984
    external = 1984
  }

  ports {
    internal = 5000
    external = 5000
  }

  ports {
    internal = 5001
    external = 5001
  }

  volumes {
    volume_name    = docker_volume.bambu_config.name
    container_path = "/app/config"
  }

  env = [
    "PRINTER1_IP=${var.printer1_ip}",
    "PRINTER1_CODE=${var.printer1_code}",
    "PRINTER1_NAME=${var.printer1_name}",
    "PRINTER1_SERIAL=${var.printer1_serial}",
  ]

  restart = "unless-stopped"
}

resource "docker_volume" "bambu_config" {
  name = "bambu-config"
}

# variables.tf
variable "printer1_ip" {
  description = "Printer 1 IP address"
  type        = string
}

variable "printer1_code" {
  description = "Printer 1 access code"
  type        = string
  sensitive   = true
}

variable "printer1_name" {
  description = "Printer 1 name"
  type        = string
  default     = "Printer 1"
}

variable "printer1_serial" {
  description = "Printer 1 serial number"
  type        = string
}
```

**Deploy:**
```bash
terraform init
terraform plan
terraform apply
```

### Ansible Playbook

```yaml
# deploy-bambu.yml
---
- name: Deploy Bambu Farm Monitor
  hosts: docker_hosts
  become: yes

  vars:
    printers:
      - id: 1
        ip: "192.168.1.100"
        code: "12345678"
        name: "Farm P1S #1"
        serial: "01P00A411800001"
      - id: 2
        ip: "192.168.1.101"
        code: "87654321"
        name: "Farm P1S #2"
        serial: "01P00A411800002"

  tasks:
    - name: Create config volume
      docker_volume:
        name: bambu-config
        state: present

    - name: Deploy Bambu Farm Monitor
      docker_container:
        name: bambu-farm-monitor
        image: neospektra/bambu-farm-monitor:latest
        state: started
        restart_policy: unless-stopped
        published_ports:
          - "8080:8080"
          - "1984:1984"
          - "5000:5000"
          - "5001:5001"
        volumes:
          - bambu-config:/app/config
        env: "{{ lookup('template', 'printer_env.j2') }}"

# templates/printer_env.j2
{% for printer in printers %}
PRINTER{{ printer.id }}_IP: "{{ printer.ip }}"
PRINTER{{ printer.id }}_CODE: "{{ printer.code }}"
PRINTER{{ printer.id }}_NAME: "{{ printer.name }}"
PRINTER{{ printer.id }}_SERIAL: "{{ printer.serial }}"
{% endfor %}
```

**Run:**
```bash
ansible-playbook deploy-bambu.yml
```

## Security Considerations

### Protecting Access Codes

**Don't:**
- ❌ Commit .env files to git
- ❌ Share compose files with codes
- ❌ Store in plain text publicly

**Do:**
- ✅ Use `.gitignore` for `.env`
- ✅ Use secret management tools
- ✅ Encrypt sensitive files
- ✅ Limit file permissions: `chmod 600 .env`

**Example .gitignore:**
```
.env
.env.local
.env.*.local
docker-compose.override.yml
secrets/
```

### File Permissions

```bash
# Secure .env file
chmod 600 .env
chown root:root .env

# Verify
ls -la .env
# Should show: -rw------- 1 root root
```

## Troubleshooting

### Variables Not Applied

**Check:**
```bash
# View container environment
docker inspect bambu-farm-monitor | grep -A 20 Env

# Should see PRINTER variables
```

**Common issues:**
- Configuration file already exists (takes precedence)
- Typo in variable name
- Wrong format

**Solution:**
```bash
# Delete config and restart
docker stop bambu-farm-monitor
docker exec bambu-farm-monitor rm /app/config/printers.json
docker start bambu-farm-monitor
```

### Configuration Not Persisting

**Check volume:**
```bash
docker inspect bambu-farm-monitor | grep -A 10 Mounts

# Should show volume mounted to /app/config
```

**Fix:**
```bash
# Ensure volume exists
docker volume ls | grep bambu

# Recreate with proper volume
docker rm bambu-farm-monitor
# Run with -v bambu-config:/app/config
```

### Invalid Configuration

**Check logs:**
```bash
docker logs bambu-farm-monitor 2>&1 | grep -i "invalid\|error"
```

**Validate format:**
```bash
# IP should be IPv4
echo $PRINTER1_IP | grep -E '^([0-9]{1,3}\.){3}[0-9]{1,3}$'

# Code should be 8 digits
echo $PRINTER1_CODE | grep -E '^[0-9]{8}$'
```

## Related Documentation

- **[Installation Guide](Installation-Guide.md)** - Basic installation
- **[Docker Deployment](Docker-Deployment.md)** - Docker deployment details
- **[Backup and Restore](Backup-and-Restore.md)** - Configuration management
- **[Security Best Practices](Security-Best-Practices.md)** - Security hardening
