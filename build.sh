#!/bin/bash
set -e

echo "Building Bambu Labs Farm Monitor Docker Image"
echo "=============================================="

# Determine which container runtime to use
if command -v docker &> /dev/null; then
    RUNTIME="docker"
    echo "Using Docker"
elif command -v podman &> /dev/null; then
    RUNTIME="podman"
    echo "Using Podman"
else
    echo "Error: Neither docker nor podman found!"
    exit 1
fi

# Build the image
echo "Building image..."
$RUNTIME build -t bambu-farm-monitor:latest .

echo ""
echo "Build completed successfully!"
echo ""
echo "To run the container:"
echo "  $RUNTIME-compose up -d"
echo ""
echo "Or manually:"
echo "  $RUNTIME run -d --name bambu-farm-monitor -p 8080:8080 -p 1984:1984 \\"
echo "    -e PRINTER1_IP=192.168.7.192 \\"
echo "    -e PRINTER1_CODE=32086612 \\"
echo "    # ... (add other environment variables) \\"
echo "    bambu-farm-monitor:latest"
echo ""
echo "Access the web UI at: http://localhost:8080"
