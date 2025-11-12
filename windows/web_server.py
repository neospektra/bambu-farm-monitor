"""
Bambu Farm Monitor - Python Web Server
Replaces nginx for Windows native installation.
"""

import sys
import os
from pathlib import Path
from waitress import serve
from flask import Flask, send_from_directory, request
import requests

app = Flask(__name__)

# Configuration
WWW_DIR = None
GO2RTC_URL = "http://localhost:1984"
CONFIG_API_URL = "http://localhost:5000"
STATUS_API_URL = "http://localhost:5001"


@app.route('/')
def index():
    """Serve index.html."""
    return send_from_directory(WWW_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files."""
    try:
        return send_from_directory(WWW_DIR, path)
    except:
        # If file not found, return index.html for SPA routing
        return send_from_directory(WWW_DIR, 'index.html')


@app.route('/api/go2rtc/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_go2rtc(path):
    """Proxy requests to go2rtc API."""
    try:
        url = f"{GO2RTC_URL}/{path}"

        if request.method == 'GET':
            resp = requests.get(url, params=request.args, timeout=10)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.json, timeout=10)
        elif request.method == 'PUT':
            resp = requests.put(url, json=request.json, timeout=10)
        elif request.method == 'DELETE':
            resp = requests.delete(url, timeout=10)

        return resp.content, resp.status_code, resp.headers.items()
    except Exception as e:
        return str(e), 502


@app.route('/api/config/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_config_api(path):
    """Proxy requests to config API."""
    try:
        url = f"{CONFIG_API_URL}/api/config/{path}"

        if request.method == 'GET':
            resp = requests.get(url, params=request.args, timeout=10)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.json, timeout=10)
        elif request.method == 'PUT':
            resp = requests.put(url, json=request.json, timeout=10)
        elif request.method == 'DELETE':
            resp = requests.delete(url, timeout=10)

        return resp.content, resp.status_code, resp.headers.items()
    except Exception as e:
        return str(e), 502


@app.route('/api/status/<path:path>', methods=['GET', 'POST'])
def proxy_status_api(path):
    """Proxy requests to status API."""
    try:
        url = f"{STATUS_API_URL}/api/status/{path}"

        if request.method == 'GET':
            resp = requests.get(url, params=request.args, timeout=10)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.json, timeout=10)

        return resp.content, resp.status_code, resp.headers.items()
    except Exception as e:
        return str(e), 502


def main():
    """Start the web server."""
    global WWW_DIR

    if len(sys.argv) < 3:
        print("Usage: web_server.py <www_dir> <port>")
        sys.exit(1)

    WWW_DIR = Path(sys.argv[1])
    port = int(sys.argv[2])

    if not WWW_DIR.exists():
        print(f"Error: WWW directory not found: {WWW_DIR}")
        sys.exit(1)

    print(f"Starting web server on port {port}...")
    print(f"Serving files from: {WWW_DIR}")
    print(f"Proxying go2rtc API from: {GO2RTC_URL}")
    print(f"Proxying config API from: {CONFIG_API_URL}")
    print(f"Proxying status API from: {STATUS_API_URL}")

    # Use waitress for production-grade WSGI server
    serve(app, host='0.0.0.0', port=port, threads=4)


if __name__ == '__main__':
    main()
