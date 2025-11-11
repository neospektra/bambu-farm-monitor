#!/bin/bash
set -e

# Default values for printer IPs and access codes
# These can be overridden by environment variables

# Printer 1
export PRINTER1_IP=${PRINTER1_IP:-""}
export PRINTER1_CODE=${PRINTER1_CODE:-""}
export PRINTER1_NAME=${PRINTER1_NAME:-"Printer 1"}
export PRINTER1_SERIAL=${PRINTER1_SERIAL:-""}

# Printer 2
export PRINTER2_IP=${PRINTER2_IP:-""}
export PRINTER2_CODE=${PRINTER2_CODE:-""}
export PRINTER2_NAME=${PRINTER2_NAME:-"Printer 2"}
export PRINTER2_SERIAL=${PRINTER2_SERIAL:-""}

# Printer 3
export PRINTER3_IP=${PRINTER3_IP:-""}
export PRINTER3_CODE=${PRINTER3_CODE:-""}
export PRINTER3_NAME=${PRINTER3_NAME:-"Printer 3"}
export PRINTER3_SERIAL=${PRINTER3_SERIAL:-""}

# Printer 4
export PRINTER4_IP=${PRINTER4_IP:-""}
export PRINTER4_CODE=${PRINTER4_CODE:-""}
export PRINTER4_NAME=${PRINTER4_NAME:-"Printer 4"}
export PRINTER4_SERIAL=${PRINTER4_SERIAL:-""}

# Create log directory
mkdir -p /var/log/supervisor

echo "Starting Bambu Labs Farm Monitor"
echo "========================================"
echo "Web UI: http://localhost:8080"
echo "go2rtc API: http://localhost:1984"
echo "Config API: http://localhost:5000"
echo "Status API: http://localhost:5001"
echo "========================================"
echo "First time setup: Navigate to the Web UI to configure your printers"
echo "========================================"

# Create a dummy BambuNetworkEngine.conf to bypass config check
echo "Creating dummy BambuNetworkEngine.conf..."
cat > /app/BambuNetworkEngine.conf <<CONF
{
  "country_code": "us",
  "last_monitor_machine": "dummy",
  "user": {
    "user_id": "0",
    "token": "dummy_token"
  }
}
CONF

# Create wrapper scripts for each printer stream
echo "Creating stream wrapper scripts..."
for i in 1 2 3 4; do
  ip_var="PRINTER${i}_IP"
  code_var="PRINTER${i}_CODE"
  cat > /app/stream${i}.sh <<WRAPPER
#!/bin/bash
export LD_LIBRARY_PATH=/app:\$LD_LIBRARY_PATH
cd /app
exec ./BambuP1SCam start_stream_local -s ${!ip_var} -a ${!code_var}
WRAPPER
  chmod +x /app/stream${i}.sh
done

# Generate go2rtc.yaml with actual environment variable values
echo "Generating go2rtc configuration..."
cat > /app/go2rtc.yaml <<EOF
streams:
  # Printer 1: $PRINTER1_NAME
  printer1: "exec:/app/stream1.sh#video=h264#hardware"

  # Printer 2: $PRINTER2_NAME
  printer2: "exec:/app/stream2.sh#video=h264#hardware"

  # Printer 3: $PRINTER3_NAME
  printer3: "exec:/app/stream3.sh#video=h264#hardware"

  # Printer 4: $PRINTER4_NAME
  printer4: "exec:/app/stream4.sh#video=h264#hardware"

# API settings
api:
  listen: ":1984"
  origin: "*"

# WebRTC settings
webrtc:
  listen: ":8555"

# Log settings
log:
  level: info
  format: text
EOF

echo "Configuration generated successfully!"

# Create initial printer configuration JSON if it doesn't exist
if [ ! -f /app/config/printers.json ]; then
  echo "Creating initial printer configuration..."
  mkdir -p /app/config

  # Check if environment variables are set for at least one printer
  if [ -n "$PRINTER1_IP" ] && [ -n "$PRINTER1_CODE" ]; then
    echo "Using environment variables to configure printers..."
    cat > /app/config/printers.json <<JSON
{
  "printers": [
    {
      "id": 1,
      "name": "$PRINTER1_NAME",
      "ip": "$PRINTER1_IP",
      "access_code": "$PRINTER1_CODE",
      "serial": "$PRINTER1_SERIAL"
    },
    {
      "id": 2,
      "name": "$PRINTER2_NAME",
      "ip": "$PRINTER2_IP",
      "access_code": "$PRINTER2_CODE",
      "serial": "$PRINTER2_SERIAL"
    },
    {
      "id": 3,
      "name": "$PRINTER3_NAME",
      "ip": "$PRINTER3_IP",
      "access_code": "$PRINTER3_CODE",
      "serial": "$PRINTER3_SERIAL"
    },
    {
      "id": 4,
      "name": "$PRINTER4_NAME",
      "ip": "$PRINTER4_IP",
      "access_code": "$PRINTER4_CODE",
      "serial": "$PRINTER4_SERIAL"
    }
  ]
}
JSON
  else
    echo "No configuration found. Creating empty config - use Web UI to setup printers..."
    cat > /app/config/printers.json <<JSON
{
  "printers": []
}
JSON
  fi
  echo "Initial configuration created at /app/config/printers.json"
else
  echo "Using existing configuration at /app/config/printers.json"
fi

# Execute the command passed to the entrypoint
exec "$@"
