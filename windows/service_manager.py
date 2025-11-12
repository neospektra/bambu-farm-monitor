"""
Bambu Farm Monitor - Windows Service Manager
This manages all the components of the application as a unified service.
"""

import os
import sys
import json
import time
import subprocess
import signal
import threading
import logging
from pathlib import Path
from typing import Dict, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bambu-monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('BambuMonitor')


class ProcessManager:
    """Manages multiple subprocesses for the Bambu Farm Monitor."""

    def __init__(self, install_dir: str):
        self.install_dir = Path(install_dir)
        self.processes: Dict[str, subprocess.Popen] = {}
        self.running = False
        self.config_dir = Path.home() / "AppData" / "Local" / "BambuFarmMonitor"

        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Paths to components
        self.go2rtc_path = self.install_dir / "bin" / "go2rtc.exe"
        self.python_path = self.install_dir / "python" / "python.exe"
        self.api_dir = self.install_dir / "api"
        self.www_dir = self.install_dir / "www"

    def start(self):
        """Start all services."""
        logger.info("Starting Bambu Farm Monitor services...")
        self.running = True

        try:
            # Start go2rtc streaming server
            self._start_go2rtc()

            # Start web server
            self._start_web_server()

            # Start config API
            self._start_config_api()

            # Start status API
            self._start_status_api()

            logger.info("All services started successfully!")
            return True

        except Exception as e:
            logger.error(f"Failed to start services: {e}")
            self.stop()
            return False

    def _start_go2rtc(self):
        """Start the go2rtc video streaming server."""
        if not self.go2rtc_path.exists():
            logger.warning(f"go2rtc not found at {self.go2rtc_path}")
            return

        config_path = self.config_dir / "go2rtc.yaml"

        # Create default config if it doesn't exist
        if not config_path.exists():
            self._create_go2rtc_config(config_path)

        logger.info("Starting go2rtc...")
        process = subprocess.Popen(
            [str(self.go2rtc_path), "-config", str(config_path)],
            cwd=str(self.install_dir),
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        self.processes['go2rtc'] = process
        logger.info(f"go2rtc started (PID: {process.pid})")

    def _start_web_server(self):
        """Start the Python web server."""
        logger.info("Starting web server...")
        process = subprocess.Popen(
            [
                str(self.python_path),
                str(self.install_dir / "windows" / "web_server.py"),
                str(self.www_dir),
                "8080"
            ],
            cwd=str(self.install_dir),
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        self.processes['web_server'] = process
        logger.info(f"Web server started (PID: {process.pid})")

    def _start_config_api(self):
        """Start the configuration API."""
        logger.info("Starting config API...")
        process = subprocess.Popen(
            [str(self.python_path), str(self.api_dir / "config_api.py")],
            cwd=str(self.api_dir),
            env={**os.environ, "CONFIG_DIR": str(self.config_dir)},
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        self.processes['config_api'] = process
        logger.info(f"Config API started (PID: {process.pid})")

    def _start_status_api(self):
        """Start the status monitoring API."""
        logger.info("Starting status API...")
        process = subprocess.Popen(
            [str(self.python_path), str(self.api_dir / "status_api.py")],
            cwd=str(self.api_dir),
            env={**os.environ, "CONFIG_DIR": str(self.config_dir)},
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        self.processes['status_api'] = process
        logger.info(f"Status API started (PID: {process.pid})")

    def _create_go2rtc_config(self, config_path: Path):
        """Create default go2rtc configuration."""
        config = """
api:
  listen: ":1984"

log:
  level: info

streams: {}
"""
        config_path.write_text(config)
        logger.info(f"Created default go2rtc config at {config_path}")

    def stop(self):
        """Stop all services."""
        logger.info("Stopping Bambu Farm Monitor services...")
        self.running = False

        for name, process in self.processes.items():
            try:
                logger.info(f"Stopping {name} (PID: {process.pid})...")
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {name}...")
                process.kill()
            except Exception as e:
                logger.error(f"Error stopping {name}: {e}")

        self.processes.clear()
        logger.info("All services stopped")

    def restart(self):
        """Restart all services."""
        logger.info("Restarting services...")
        self.stop()
        time.sleep(2)
        return self.start()

    def is_running(self) -> bool:
        """Check if services are running."""
        if not self.processes:
            return False

        # Check if all processes are still alive
        for name, process in self.processes.items():
            if process.poll() is not None:
                logger.warning(f"Process {name} has died")
                return False

        return True

    def monitor(self):
        """Monitor processes and restart if they die."""
        while self.running:
            time.sleep(5)

            if not self.is_running() and self.running:
                logger.warning("Service died, attempting restart...")
                self.restart()


class WindowsService:
    """Windows service wrapper for the Process Manager."""

    def __init__(self):
        self.install_dir = self._get_install_dir()
        self.manager = ProcessManager(self.install_dir)
        self.monitor_thread: Optional[threading.Thread] = None

    def _get_install_dir(self) -> str:
        """Get the installation directory."""
        # If running as executable, use its directory
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        # If running as script, use parent directory
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def start(self):
        """Start the service."""
        logger.info("Bambu Farm Monitor Service starting...")

        if self.manager.start():
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self.manager.monitor, daemon=True)
            self.monitor_thread.start()

            logger.info("Service started successfully")
            return True

        return False

    def stop(self):
        """Stop the service."""
        logger.info("Bambu Farm Monitor Service stopping...")
        self.manager.stop()

        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

        logger.info("Service stopped")

    def restart(self):
        """Restart the service."""
        self.stop()
        time.sleep(2)
        return self.start()


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    if 'service' in globals():
        service.stop()
    sys.exit(0)


def main():
    """Main entry point."""
    global service

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    service = WindowsService()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "start":
            if service.start():
                # Keep running
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    service.stop()

        elif command == "stop":
            service.stop()

        elif command == "restart":
            service.restart()

        elif command == "status":
            if service.manager.is_running():
                print("Bambu Farm Monitor is running")
                sys.exit(0)
            else:
                print("Bambu Farm Monitor is not running")
                sys.exit(1)

        else:
            print("Usage: service_manager.py [start|stop|restart|status]")
            sys.exit(1)

    else:
        # Default: start service
        if service.start():
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                service.stop()


if __name__ == "__main__":
    main()
