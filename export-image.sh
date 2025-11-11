#!/bin/bash
set -e

echo "Exporting Bambu Labs Farm Monitor Image for QNAP"
echo "================================================="

# Determine which container runtime to use
if command -v docker &> /dev/null; then
    RUNTIME="docker"
elif command -v podman &> /dev/null; then
    RUNTIME="podman"
else
    echo "Error: Neither docker nor podman found!"
    exit 1
fi

OUTPUT_FILE="bambu-farm-monitor-$(date +%Y%m%d).tar.gz"

echo "Exporting image to: $OUTPUT_FILE"
$RUNTIME save bambu-farm-monitor:latest | gzip > "$OUTPUT_FILE"

echo ""
echo "Export completed successfully!"
echo ""
echo "File: $OUTPUT_FILE"
echo "Size: $(du -h "$OUTPUT_FILE" | cut -f1)"
echo ""
echo "To import on QNAP Container Station:"
echo "1. Transfer $OUTPUT_FILE to your QNAP"
echo "2. Open Container Station"
echo "3. Go to 'Image' tab"
echo "4. Click 'Import' and select the file"
echo "5. Create a container from the imported image"
