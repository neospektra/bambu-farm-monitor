"""
Bambu Farm Monitor - System Tray Application
Provides easy control and monitoring from the Windows system tray.
"""

import sys
import os
import webbrowser
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
import threading
import time


class BambuTrayApp:
    """System tray application for Bambu Farm Monitor."""

    def __init__(self):
        self.install_dir = self._get_install_dir()
        self.service_script = self.install_dir / "windows" / "service_manager.py"
        self.python_exe = self.install_dir / "python" / "python.exe"
        self.icon = None
        self.running = False
        self.service_process = None

    def _get_install_dir(self) -> Path:
        """Get the installation directory."""
        if getattr(sys, 'frozen', False):
            return Path(os.path.dirname(sys.executable))
        return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def create_icon(self) -> Image.Image:
        """Create a simple tray icon."""
        # Create a 64x64 icon with a printer symbol
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='#2196F3')
        dc = ImageDraw.Draw(image)

        # Draw a simple printer icon
        # Box for printer body
        dc.rectangle([16, 24, 48, 48], fill='white', outline='white')
        # Paper coming out
        dc.rectangle([20, 12, 44, 24], fill='white', outline='white')
        # Lines on paper
        dc.line([24, 16, 40, 16], fill='#2196F3', width=1)
        dc.line([24, 20, 40, 20], fill='#2196F3', width=1)

        return image

    def is_service_running(self) -> bool:
        """Check if the service is currently running."""
        try:
            result = subprocess.run(
                [str(self.python_exe), str(self.service_script), "status"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def start_service(self, icon=None, item=None):
        """Start the Bambu Farm Monitor service."""
        if self.is_service_running():
            self._show_notification("Already Running", "Bambu Farm Monitor is already running")
            return

        try:
            # Start service in background
            self.service_process = subprocess.Popen(
                [str(self.python_exe), str(self.service_script), "start"],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.running = True
            self._show_notification("Started", "Bambu Farm Monitor has started")

            # Update icon
            if self.icon:
                self.icon.title = "Bambu Farm Monitor (Running)"

        except Exception as e:
            self._show_notification("Error", f"Failed to start service: {e}")

    def stop_service(self, icon=None, item=None):
        """Stop the Bambu Farm Monitor service."""
        if not self.is_service_running():
            self._show_notification("Not Running", "Bambu Farm Monitor is not running")
            return

        try:
            subprocess.run(
                [str(self.python_exe), str(self.service_script), "stop"],
                timeout=10
            )
            self.running = False
            self._show_notification("Stopped", "Bambu Farm Monitor has stopped")

            # Update icon
            if self.icon:
                self.icon.title = "Bambu Farm Monitor (Stopped)"

        except Exception as e:
            self._show_notification("Error", f"Failed to stop service: {e}")

    def restart_service(self, icon=None, item=None):
        """Restart the Bambu Farm Monitor service."""
        self._show_notification("Restarting", "Restarting Bambu Farm Monitor...")

        try:
            subprocess.run(
                [str(self.python_exe), str(self.service_script), "restart"],
                timeout=30
            )
            self._show_notification("Restarted", "Bambu Farm Monitor has restarted")
        except Exception as e:
            self._show_notification("Error", f"Failed to restart service: {e}")

    def open_dashboard(self, icon=None, item=None):
        """Open the web dashboard in default browser."""
        webbrowser.open('http://localhost:8080')

    def open_config_folder(self, icon=None, item=None):
        """Open the configuration folder in Explorer."""
        config_dir = Path.home() / "AppData" / "Local" / "BambuFarmMonitor"
        os.startfile(str(config_dir))

    def _show_notification(self, title: str, message: str):
        """Show a system notification."""
        if self.icon:
            self.icon.notify(message, title)

    def quit_app(self, icon=None, item=None):
        """Quit the tray application."""
        # Stop service if running
        if self.is_service_running():
            self.stop_service()

        # Stop icon
        if self.icon:
            self.icon.stop()

    def setup_menu(self):
        """Setup the system tray menu."""
        return pystray.Menu(
            item('Open Dashboard', self.open_dashboard, default=True),
            item('Start Service', self.start_service, visible=lambda item: not self.is_service_running()),
            item('Stop Service', self.stop_service, visible=lambda item: self.is_service_running()),
            item('Restart Service', self.restart_service, visible=lambda item: self.is_service_running()),
            pystray.Menu.SEPARATOR,
            item('Open Config Folder', self.open_config_folder),
            pystray.Menu.SEPARATOR,
            item('Quit', self.quit_app)
        )

    def update_status(self):
        """Periodically update the service status."""
        while True:
            time.sleep(5)
            running = self.is_service_running()

            if running != self.running:
                self.running = running
                if self.icon:
                    status = "Running" if running else "Stopped"
                    self.icon.title = f"Bambu Farm Monitor ({status})"

    def run(self):
        """Run the tray application."""
        image = self.create_icon()
        menu = self.setup_menu()

        # Start service on startup if not already running
        if not self.is_service_running():
            self.start_service()

        # Create icon
        self.icon = pystray.Icon(
            "bambu-monitor",
            image,
            "Bambu Farm Monitor",
            menu
        )

        # Start status update thread
        status_thread = threading.Thread(target=self.update_status, daemon=True)
        status_thread.start()

        # Run the icon
        self.icon.run()


def main():
    """Main entry point."""
    app = BambuTrayApp()
    app.run()


if __name__ == "__main__":
    main()
