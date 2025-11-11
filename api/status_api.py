#!/usr/bin/env python3
"""
Status API for Bambu Farm Monitor
Connects to Bambu printers via MQTT to retrieve real-time status
"""

from flask import Flask, jsonify
from flask_cors import CORS
import json
import ssl
import paho.mqtt.client as mqtt
import threading
import time

app = Flask(__name__)
CORS(app)

# Store printer status in memory
printer_status = {}
mqtt_clients = {}

CONFIG_FILE = '/app/config/printers.json'

def load_config():
    """Load printer configuration"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"printers": []}

def parse_bambu_status(payload):
    """Parse Bambu printer MQTT status message"""
    try:
        data = json.loads(payload)
        print_data = data.get('print', {})

        status = {
            'connected': True,
            'printing': False,
            'bed_temp': 0,
            'bed_target': 0,
            'nozzle_temp': 0,
            'nozzle_target': 0,
            'chamber_temp': 0,
            'fan_speed': 0,
            'print_progress': 0,
            'print_layer': 0,
            'print_total_layers': 0,
            'print_time_remaining': 0,
            'print_time_elapsed': 0,
            'print_file': '',
            'print_status': 'idle',
            'ams': {
                'has_ams': False,
                'trays': [],
                'active_tray': None
            }
        }

        # Extract temperature data
        if 'bed_temper' in print_data:
            status['bed_temp'] = print_data['bed_temper']
        if 'bed_target_temper' in print_data:
            status['bed_target'] = print_data['bed_target_temper']
        if 'nozzle_temper' in print_data:
            status['nozzle_temp'] = print_data['nozzle_temper']
        if 'nozzle_target_temper' in print_data:
            status['nozzle_target'] = print_data['nozzle_target_temper']
        if 'chamber_temper' in print_data:
            status['chamber_temp'] = print_data['chamber_temper']

        # Extract print job data
        if 'mc_percent' in print_data:
            status['print_progress'] = print_data['mc_percent']
        if 'layer_num' in print_data:
            status['print_layer'] = print_data['layer_num']
        if 'total_layer_num' in print_data:
            status['print_total_layers'] = print_data['total_layer_num']
        if 'mc_remaining_time' in print_data:
            status['print_time_remaining'] = print_data['mc_remaining_time']
        if 'gcode_file' in print_data:
            status['print_file'] = print_data['gcode_file']
        if 'gcode_state' in print_data:
            state = print_data['gcode_state']
            status['print_status'] = state
            status['printing'] = state in ['RUNNING', 'PAUSE']

        # Fan speed
        if 'big_fan1_speed' in print_data:
            status['fan_speed'] = print_data['big_fan1_speed']

        # Parse AMS (Automatic Material System) data
        if 'ams' in data:
            ams_data = data['ams']
            if 'ams' in ams_data and len(ams_data['ams']) > 0:
                status['ams']['has_ams'] = True
                # Get first AMS unit (most printers have only one)
                ams_unit = ams_data['ams'][0]

                # Get active tray info
                if 'tray_now' in ams_unit:
                    status['ams']['active_tray'] = ams_unit['tray_now']

                # Parse tray information
                if 'tray' in ams_unit:
                    trays = []
                    for tray in ams_unit['tray']:
                        tray_info = {
                            'id': tray.get('id', ''),
                            'color': tray.get('tray_color', 'CCCCCC'),  # Default gray if no color
                            'type': tray.get('tray_type', ''),
                            'name': tray.get('tray_sub_brands', ''),
                            'empty': tray.get('tray_type', '') == ''  # Empty if no type
                        }
                        trays.append(tray_info)
                    status['ams']['trays'] = trays

        return status
    except Exception as e:
        print(f"Error parsing status: {e}")
        return None

def on_connect(client, userdata, flags, rc):
    """MQTT connection callback"""
    printer_id = userdata['printer_id']
    serial = userdata.get('serial', '')
    print(f"Printer {printer_id} MQTT connected with code: {rc}")

    if rc == 0:
        # Subscribe to device report topic
        # If we have a serial number, use it specifically, otherwise use wildcard
        if serial:
            topic = f"device/{serial}/report"
            print(f"Printer {printer_id} subscribing to specific topic: {topic}")
        else:
            topic = "device/+/report"
            print(f"Printer {printer_id} subscribing to wildcard topic: {topic}")

        client.subscribe(topic)
        printer_status[printer_id]['connected'] = True
        printer_status[printer_id]['mqtt_topic'] = topic
    else:
        print(f"Printer {printer_id} MQTT connection failed: {rc}")
        printer_status[printer_id]['connected'] = False

def on_message(client, userdata, msg):
    """MQTT message callback"""
    printer_id = userdata['printer_id']
    print(f"Printer {printer_id} received message on topic: {msg.topic}")
    status = parse_bambu_status(msg.payload)

    if status:
        # Always update temperature data as it changes frequently
        printer_status[printer_id]['nozzle_temp'] = status['nozzle_temp']
        printer_status[printer_id]['bed_temp'] = status['bed_temp']
        printer_status[printer_id]['chamber_temp'] = status['chamber_temp']
        printer_status[printer_id]['connected'] = status['connected']

        # Always update AMS data when present
        if status['ams']['has_ams']:
            printer_status[printer_id]['ams'] = status['ams']

        # Only update print job data if the new status has valid print info
        current_printing = printer_status[printer_id].get('printing', False)
        current_file = printer_status[printer_id].get('print_file', '')

        new_has_print_data = status['print_file'] != '' and status['print_progress'] > 0
        new_is_clearly_idle = status['print_file'] == '' and status['print_progress'] == 0 and status['print_status'] == 'idle'

        if new_has_print_data:
            # New message has complete print data, update everything
            printer_status[printer_id]['printing'] = status['printing']
            printer_status[printer_id]['print_progress'] = status['print_progress']
            printer_status[printer_id]['print_file'] = status['print_file']
            printer_status[printer_id]['print_layer'] = status['print_layer']
            printer_status[printer_id]['print_total_layers'] = status['print_total_layers']
            printer_status[printer_id]['print_time_remaining'] = status['print_time_remaining']
            printer_status[printer_id]['print_status'] = status['print_status']
            printer_status[printer_id]['nozzle_target'] = status['nozzle_target']
            printer_status[printer_id]['bed_target'] = status['bed_target']
            printer_status[printer_id]['fan_speed'] = status['fan_speed']
        elif new_is_clearly_idle and not current_printing:
            # Was idle, still idle, update to confirm
            printer_status[printer_id]['printing'] = False
            printer_status[printer_id]['print_progress'] = 0
            printer_status[printer_id]['print_file'] = ''
            printer_status[printer_id]['print_layer'] = 0
            printer_status[printer_id]['print_total_layers'] = 0
            printer_status[printer_id]['print_time_remaining'] = 0
            printer_status[printer_id]['print_status'] = 'idle'
        # else: keep cached print data if new message doesn't have complete info

def on_disconnect(client, userdata, rc):
    """MQTT disconnect callback"""
    printer_id = userdata['printer_id']
    if rc != 0:
        print(f"Printer {printer_id} MQTT disconnected unexpectedly with code: {rc}")
        # Try to reconnect
        try:
            client.reconnect()
        except:
            pass
    printer_status[printer_id]['connected'] = False

def connect_printer_mqtt(printer):
    """Connect to a printer's MQTT broker"""
    printer_id = printer['id']
    ip = printer['ip']
    access_code = printer['access_code']
    serial = printer.get('serial', '')

    # Initialize status
    printer_status[printer_id] = {
        'connected': False,
        'printing': False,
        'bed_temp': 0,
        'bed_target': 0,
        'nozzle_temp': 0,
        'nozzle_target': 0,
        'chamber_temp': 0,
        'fan_speed': 0,
        'print_progress': 0,
        'print_layer': 0,
        'print_total_layers': 0,
        'print_time_remaining': 0,
        'print_file': '',
        'print_status': 'unknown',
        'serial': serial,
        'ip': ip,
        'ams': {
            'has_ams': False,
            'trays': [],
            'active_tray': None
        }
    }

    try:
        # Create MQTT client
        client = mqtt.Client(userdata={'printer_id': printer_id, 'serial': serial})

        # Set username/password (access code is used as password)
        client.username_pw_set(username="bblp", password=access_code)

        # Set TLS (Bambu uses self-signed certs, so we need to disable verification)
        client.tls_set(cert_reqs=ssl.CERT_NONE)
        client.tls_insecure_set(True)

        # Set callbacks
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        # Connect to printer
        client.connect(ip, 8883, 60)

        # Start loop in background
        client.loop_start()

        mqtt_clients[printer_id] = client
        print(f"Started MQTT client for printer {printer_id}")

    except Exception as e:
        print(f"Error connecting to printer {printer_id}: {e}")

def initialize_mqtt_connections():
    """Initialize MQTT connections to all printers"""
    config = load_config()

    for printer in config.get('printers', []):
        connect_printer_mqtt(printer)

@app.route('/api/status/printers', methods=['GET'])
def get_all_status():
    """Get status for all printers"""
    return jsonify(printer_status)

@app.route('/api/status/printers/<int:printer_id>', methods=['GET'])
def get_printer_status(printer_id):
    """Get status for a specific printer"""
    if printer_id in printer_status:
        return jsonify(printer_status[printer_id])
    else:
        return jsonify({"error": "Printer not found"}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "mqtt_clients": len(mqtt_clients)})

@app.route('/api/status/reconnect', methods=['POST'])
def reconnect_mqtt():
    """Reconnect all MQTT clients"""
    global mqtt_clients, printer_status

    # Disconnect all existing clients
    for client in mqtt_clients.values():
        try:
            client.loop_stop()
            client.disconnect()
        except:
            pass

    mqtt_clients.clear()
    printer_status.clear()

    # Reinitialize connections
    initialize_mqtt_connections()

    return jsonify({"status": "ok", "mqtt_clients": len(mqtt_clients)})

@app.route('/api/status/test', methods=['GET'])
def test_status():
    """Test endpoint with fake data to verify overlays"""
    return jsonify({
        "1": {
            "connected": True,
            "printing": True,
            "bed_temp": 60,
            "bed_target": 60,
            "nozzle_temp": 210,
            "nozzle_target": 210,
            "chamber_temp": 35,
            "fan_speed": 50,
            "print_progress": 65,
            "print_layer": 120,
            "print_total_layers": 185,
            "print_time_remaining": 135,
            "print_file": "/data/test_model_benchy.gcode",
            "print_status": "RUNNING"
        },
        "2": {
            "connected": True,
            "printing": False,
            "bed_temp": 25,
            "bed_target": 0,
            "nozzle_temp": 28,
            "nozzle_target": 0,
            "chamber_temp": 25,
            "fan_speed": 0,
            "print_progress": 0,
            "print_layer": 0,
            "print_total_layers": 0,
            "print_time_remaining": 0,
            "print_file": "",
            "print_status": "IDLE"
        },
        "3": {
            "connected": True,
            "printing": True,
            "bed_temp": 65,
            "bed_target": 65,
            "nozzle_temp": 220,
            "nozzle_target": 220,
            "chamber_temp": 40,
            "fan_speed": 75,
            "print_progress": 92,
            "print_layer": 275,
            "print_total_layers": 300,
            "print_time_remaining": 45,
            "print_file": "/sdcard/models/gear_assembly_v2.gcode",
            "print_status": "RUNNING"
        },
        "4": {
            "connected": True,
            "printing": False,
            "bed_temp": 24,
            "bed_target": 0,
            "nozzle_temp": 26,
            "nozzle_target": 0,
            "chamber_temp": 24,
            "fan_speed": 0,
            "print_progress": 0,
            "print_layer": 0,
            "print_total_layers": 0,
            "print_file": "",
            "print_status": "IDLE"
        }
    })

@app.route('/api/status/mqtt-test/<int:printer_id>', methods=['POST'])
def test_mqtt_connection(printer_id):
    """Test MQTT connection to a specific printer"""
    config = load_config()

    # Find printer config
    printer = None
    for p in config.get('printers', []):
        if p['id'] == printer_id:
            printer = p
            break

    if not printer:
        return jsonify({"success": False, "error": "Printer not found"}), 404

    ip = printer['ip']
    access_code = printer['access_code']
    serial = printer.get('serial', '')

    test_result = {
        "printer_id": printer_id,
        "ip": ip,
        "serial": serial,
        "success": False,
        "connected": False,
        "subscribed": False,
        "error": None,
        "connection_code": None
    }

    connection_event = threading.Event()
    connection_result = {'rc': None, 'subscribed': False}

    def test_on_connect(client, userdata, flags, rc):
        """Test connection callback"""
        connection_result['rc'] = rc
        if rc == 0:
            # Try to subscribe
            if serial:
                topic = f"device/{serial}/report"
            else:
                topic = "device/+/report"
            client.subscribe(topic)
            connection_result['subscribed'] = True
            connection_result['topic'] = topic
        connection_event.set()

    def test_on_disconnect(client, userdata, rc):
        """Test disconnect callback"""
        if not connection_event.is_set():
            connection_result['rc'] = rc
            connection_event.set()

    try:
        # Create test MQTT client
        test_client = mqtt.Client(userdata={'printer_id': printer_id, 'serial': serial})
        test_client.username_pw_set(username="bblp", password=access_code)
        test_client.tls_set(cert_reqs=ssl.CERT_NONE)
        test_client.tls_insecure_set(True)
        test_client.on_connect = test_on_connect
        test_client.on_disconnect = test_on_disconnect

        # Try to connect
        test_client.connect(ip, 8883, 10)
        test_client.loop_start()

        # Wait for connection result (timeout 5 seconds)
        connection_event.wait(timeout=5)

        test_client.loop_stop()
        test_client.disconnect()

        # Analyze results
        rc = connection_result.get('rc')
        test_result['connection_code'] = rc

        if rc == 0:
            test_result['success'] = True
            test_result['connected'] = True
            test_result['subscribed'] = connection_result.get('subscribed', False)
            test_result['topic'] = connection_result.get('topic', '')
            test_result['message'] = f"Successfully connected and subscribed to {test_result['topic']}"
        elif rc is None:
            test_result['error'] = "Connection timeout - unable to reach printer"
        elif rc == 1:
            test_result['error'] = "Connection refused - incorrect protocol version"
        elif rc == 2:
            test_result['error'] = "Connection refused - invalid client identifier"
        elif rc == 3:
            test_result['error'] = "Connection refused - server unavailable"
        elif rc == 4:
            test_result['error'] = "Connection refused - bad username or password (check access code)"
        elif rc == 5:
            test_result['error'] = "Connection refused - not authorized"
        elif rc == 7:
            test_result['error'] = "Connection established but disconnected immediately (code 7) - likely missing/incorrect serial number"
        else:
            test_result['error'] = f"Connection failed with code {rc}"

    except Exception as e:
        test_result['error'] = str(e)

    return jsonify(test_result)

if __name__ == '__main__':
    # Initialize MQTT connections
    initialize_mqtt_connections()

    app.run(host='0.0.0.0', port=5001, debug=False)
