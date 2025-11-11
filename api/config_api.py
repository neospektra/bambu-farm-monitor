#!/usr/bin/env python3
"""
Configuration API for Bambu Farm Monitor
Provides REST endpoints for managing printer configuration and retrieving status
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import subprocess
import signal
from datetime import datetime

app = Flask(__name__)
CORS(app)

CONFIG_FILE = '/app/config/printers.json'
GO2RTC_YAML = '/app/go2rtc.yaml'

def load_config():
    """Load printer configuration from JSON file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)

    # Default empty configuration
    return {"printers": []}

def save_config(config):
    """Save printer configuration to JSON file"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def regenerate_go2rtc_config(config):
    """Regenerate go2rtc.yaml from printer configuration"""
    streams_config = "streams:\n"

    for printer in config['printers']:
        printer_id = printer['id']
        name = printer['name']
        ip = printer['ip']
        code = printer['access_code']

        streams_config += f"  # Printer {printer_id}: {name}\n"
        streams_config += f"  printer{printer_id}: \"exec:/app/stream{printer_id}.sh#video=h264#hardware\"\n\n"

    full_config = streams_config + """
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
"""

    with open(GO2RTC_YAML, 'w') as f:
        f.write(full_config)

    # Regenerate stream wrapper scripts
    for printer in config['printers']:
        printer_id = printer['id']
        ip = printer['ip']
        code = printer['access_code']

        script_path = f'/app/stream{printer_id}.sh'
        script_content = f"""#!/bin/bash
export LD_LIBRARY_PATH=/app:$LD_LIBRARY_PATH
cd /app
exec ./BambuP1SCam start_stream_local -s {ip} -a {code}
"""

        with open(script_path, 'w') as f:
            f.write(script_content)

        os.chmod(script_path, 0o755)

def restart_go2rtc():
    """Restart go2rtc to apply new configuration"""
    try:
        # Send SIGHUP to supervisor to reload go2rtc
        subprocess.run(['supervisorctl', 'restart', 'go2rtc'], check=True)
        return True
    except Exception as e:
        print(f"Error restarting go2rtc: {e}")
        return False

@app.route('/api/config/printers', methods=['GET'])
def get_printers():
    """Get all printer configurations"""
    config = load_config()
    return jsonify(config)

@app.route('/api/config/printers/<int:printer_id>', methods=['PUT'])
def update_printer(printer_id):
    """Update a specific printer configuration"""
    config = load_config()
    data = request.json

    # Find and update printer
    for printer in config['printers']:
        if printer['id'] == printer_id:
            if 'name' in data:
                printer['name'] = data['name']
            if 'ip' in data:
                printer['ip'] = data['ip']
            if 'access_code' in data:
                printer['access_code'] = data['access_code']
            if 'serial' in data:
                printer['serial'] = data['serial']

            # Save configuration
            save_config(config)

            # Regenerate go2rtc config
            regenerate_go2rtc_config(config)

            # Restart go2rtc
            restart_go2rtc()

            return jsonify({"success": True, "printer": printer})

    return jsonify({"error": "Printer not found"}), 404

@app.route('/api/config/printers/<int:printer_id>', methods=['DELETE'])
def delete_printer(printer_id):
    """Delete a specific printer configuration"""
    config = load_config()

    # Find and remove printer
    printers = config.get('printers', [])
    original_count = len(printers)
    config['printers'] = [p for p in printers if p['id'] != printer_id]

    if len(config['printers']) == original_count:
        return jsonify({"error": "Printer not found"}), 404

    # Save configuration
    save_config(config)

    # Regenerate go2rtc config
    regenerate_go2rtc_config(config)

    # Restart go2rtc
    restart_go2rtc()

    return jsonify({"success": True, "message": f"Printer {printer_id} deleted"})

@app.route('/api/config/reload', methods=['POST'])
def reload_config():
    """Reload go2rtc configuration"""
    config = load_config()
    regenerate_go2rtc_config(config)

    if restart_go2rtc():
        return jsonify({"success": True, "message": "Configuration reloaded"})
    else:
        return jsonify({"error": "Failed to restart go2rtc"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

@app.route('/api/config/setup-required', methods=['GET'])
def setup_required():
    """Check if initial setup is required"""
    config = load_config()
    printers = config.get('printers', [])

    # Setup is required if no printers are configured or all printers are empty
    needs_setup = len(printers) == 0 or all(
        not p.get('ip') or not p.get('access_code')
        for p in printers
    )

    return jsonify({
        "setup_required": needs_setup,
        "printer_count": len([p for p in printers if p.get('ip') and p.get('access_code')])
    })

@app.route('/api/config/printers', methods=['POST'])
def add_printer():
    """Add a new printer configuration"""
    config = load_config()
    data = request.json

    # Determine next printer ID
    existing_ids = [p['id'] for p in config['printers']]
    next_id = max(existing_ids) + 1 if existing_ids else 1

    # Create new printer
    new_printer = {
        "id": next_id,
        "name": data.get('name', f'Printer {next_id}'),
        "ip": data.get('ip', ''),
        "access_code": data.get('access_code', ''),
        "serial": data.get('serial', '')
    }

    config['printers'].append(new_printer)
    save_config(config)
    regenerate_go2rtc_config(config)
    restart_go2rtc()

    return jsonify({"success": True, "printer": new_printer})

@app.route('/api/config/printers/bulk', methods=['POST'])
def bulk_update_printers():
    """Bulk update/create all printers (for setup wizard)"""
    data = request.json
    printers_data = data.get('printers', [])

    # Create configuration with proper IDs
    config = {"printers": []}
    for i, printer_data in enumerate(printers_data, 1):
        config['printers'].append({
            "id": i,
            "name": printer_data.get('name', f'Printer {i}'),
            "ip": printer_data.get('ip', ''),
            "access_code": printer_data.get('access_code', ''),
            "serial": printer_data.get('serial', '')
        })

    save_config(config)
    regenerate_go2rtc_config(config)
    restart_go2rtc()

    return jsonify({"success": True, "printers": config['printers']})

@app.route('/api/config/export', methods=['GET'])
def export_config():
    """Export printer configuration as JSON file"""
    try:
        config = load_config()

        # Create a backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'bambu_config_{timestamp}.json'

        # Save to temporary file
        temp_path = f'/tmp/{filename}'
        with open(temp_path, 'w') as f:
            json.dump(config, f, indent=2)

        return send_file(
            temp_path,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config/import', methods=['POST'])
def import_config():
    """Import printer configuration from JSON file"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Read and parse JSON
        try:
            config_data = json.load(file)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON file"}), 400

        # Validate config structure
        if 'printers' not in config_data:
            return jsonify({"error": "Invalid configuration format - missing 'printers' key"}), 400

        if not isinstance(config_data['printers'], list):
            return jsonify({"error": "Invalid configuration format - 'printers' must be an array"}), 400

        # Validate each printer has required fields
        for i, printer in enumerate(config_data['printers']):
            required_fields = ['id', 'name', 'ip', 'access_code']
            for field in required_fields:
                if field not in printer:
                    return jsonify({"error": f"Printer {i+1} missing required field: {field}"}), 400

        # Save configuration
        save_config(config_data)

        # Regenerate go2rtc config
        regenerate_go2rtc_config(config_data)

        # Restart go2rtc
        restart_go2rtc()

        return jsonify({
            "success": True,
            "message": f"Successfully imported {len(config_data['printers'])} printers",
            "printers": config_data['printers']
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Initialize config file if it doesn't exist
    if not os.path.exists(CONFIG_FILE):
        save_config(load_config())

    app.run(host='0.0.0.0', port=5000, debug=False)
