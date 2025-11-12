"""
Bambu Farm Monitor - Windows Build Script
Builds the Windows native installer using PyInstaller and Inno Setup.
"""

import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

# Build configuration
APP_NAME = "BambuFarmMonitor"
APP_VERSION = "3.3.9"
GO2RTC_VERSION = "1.9.4"
GO2RTC_URL = f"https://github.com/AlexxIT/go2rtc/releases/download/v{GO2RTC_VERSION}/go2rtc_win64.zip"

class WindowsBuilder:
    """Builds the Windows native application."""

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.windows_dir = self.root_dir / "windows"
        self.build_dir = self.windows_dir / "build"
        self.dist_dir = self.windows_dir / "dist"
        self.output_dir = self.windows_dir / "output"

        print(f"Root directory: {self.root_dir}")
        print(f"Windows directory: {self.windows_dir}")
        print(f"Build directory: {self.build_dir}")

    def clean(self):
        """Clean previous build artifacts."""
        print("\n=== Cleaning previous builds ===")

        for dir_path in [self.build_dir, self.dist_dir, self.output_dir]:
            if dir_path.exists():
                print(f"Removing {dir_path}...")
                shutil.rmtree(dir_path)

        print("Clean complete!")

    def download_go2rtc(self):
        """Download go2rtc Windows binary."""
        print("\n=== Downloading go2rtc ===")

        go2rtc_dir = self.build_dir / "bin"
        go2rtc_dir.mkdir(parents=True, exist_ok=True)

        zip_path = go2rtc_dir / "go2rtc.zip"
        exe_path = go2rtc_dir / "go2rtc.exe"

        if exe_path.exists():
            print(f"go2rtc already exists at {exe_path}")
            return

        print(f"Downloading from {GO2RTC_URL}...")
        try:
            urllib.request.urlretrieve(GO2RTC_URL, zip_path)

            print("Extracting...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(go2rtc_dir)

            zip_path.unlink()
            print(f"go2rtc downloaded to {exe_path}")

        except Exception as e:
            print(f"Error downloading go2rtc: {e}")
            print("Please download manually and place at:", exe_path)
            sys.exit(1)

    def build_executables(self):
        """Build executables using PyInstaller."""
        print("\n=== Building executables with PyInstaller ===")

        # Build service manager
        print("\nBuilding service_manager.exe...")
        self._build_pyinstaller(
            script="service_manager.py",
            name="service_manager",
            console=True
        )

        # Build tray application
        print("\nBuilding bambu-monitor.exe...")
        self._build_pyinstaller(
            script="tray_app.py",
            name="bambu-monitor",
            console=False,
            icon=None  # TODO: Add icon file
        )

        # Build web server
        print("\nBuilding web_server.exe...")
        self._build_pyinstaller(
            script="web_server.py",
            name="web_server",
            console=True
        )

    def _build_pyinstaller(self, script: str, name: str, console: bool = True, icon: str = None):
        """Build a single executable with PyInstaller."""
        cmd = [
            "pyinstaller",
            "--name", name,
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir / "pyinstaller_work"),
            "--specpath", str(self.build_dir / "specs"),
            "--onefile",
        ]

        if not console:
            cmd.append("--windowed")

        if icon:
            cmd.extend(["--icon", icon])

        # Add data files for tray app
        if "tray_app" in script:
            cmd.extend([
                "--hidden-import", "pystray._win32",
            ])

        cmd.append(str(self.windows_dir / script))

        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=str(self.root_dir))

        if result.returncode != 0:
            print(f"Error building {name}")
            sys.exit(1)

    def prepare_distribution(self):
        """Prepare the distribution folder with all necessary files."""
        print("\n=== Preparing distribution ===")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create directory structure
        dirs = [
            "bin",
            "api",
            "www",
            "windows",
            "config"
        ]

        for dir_name in dirs:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)

        # Copy executables
        print("Copying executables...")
        for exe in ["service_manager.exe", "bambu-monitor.exe", "web_server.exe"]:
            src = self.dist_dir / exe
            dst = self.output_dir / "windows" / exe
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  Copied {exe}")

        # Copy go2rtc
        print("Copying go2rtc...")
        go2rtc_src = self.build_dir / "bin" / "go2rtc.exe"
        if go2rtc_src.exists():
            shutil.copy2(go2rtc_src, self.output_dir / "bin" / "go2rtc.exe")

        # Copy API files
        print("Copying API files...")
        api_dir = self.root_dir / "api"
        for py_file in api_dir.glob("*.py"):
            shutil.copy2(py_file, self.output_dir / "api" / py_file.name)

        # Copy www files
        print("Copying web files...")
        www_dir = self.root_dir / "www"
        if www_dir.exists():
            shutil.copytree(www_dir, self.output_dir / "www", dirs_exist_ok=True)

        # Copy requirements
        print("Copying requirements...")
        shutil.copy2(
            self.windows_dir / "requirements.txt",
            self.output_dir / "requirements.txt"
        )

        # Create README
        self._create_readme()

        print("\nDistribution prepared at:", self.output_dir)

    def _create_readme(self):
        """Create README for the distribution."""
        readme = """# Bambu Farm Monitor - Windows Native

## Installation

1. Run the installer (BambuFarmMonitorSetup.exe)
2. Follow the installation wizard
3. The application will start automatically after installation

## Usage

The Bambu Farm Monitor tray icon will appear in your system tray.

Right-click the icon to:
- Open Dashboard
- Start/Stop/Restart Service
- Open Configuration Folder
- Quit

## Configuration

Configuration files are stored in:
%LOCALAPPDATA%\\BambuFarmMonitor

## Ports

- 8080: Web UI
- 1984: go2rtc WebRTC streaming
- 5000: Configuration API
- 5001: Status API

## Uninstall

Use Windows Add/Remove Programs to uninstall.

## Support

https://github.com/neospektra/bambu-farm-monitor
"""
        (self.output_dir / "README.txt").write_text(readme)

    def build_installer(self):
        """Build the installer using Inno Setup."""
        print("\n=== Building installer with Inno Setup ===")

        inno_script = self.windows_dir / "installer.iss"

        if not inno_script.exists():
            print("Error: installer.iss not found")
            print("Please create the Inno Setup script first")
            return

        # Check if Inno Setup is installed
        iscc_paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe",
        ]

        iscc = None
        for path in iscc_paths:
            if os.path.exists(path):
                iscc = path
                break

        if not iscc:
            print("Warning: Inno Setup not found. Please install from:")
            print("https://jrsoftware.org/isdl.php")
            print("\nYou can manually compile the installer later using:")
            print(f"ISCC.exe {inno_script}")
            return

        print(f"Running Inno Setup: {iscc}")
        result = subprocess.run([iscc, str(inno_script)])

        if result.returncode == 0:
            print("\nInstaller created successfully!")
        else:
            print("\nError creating installer")

    def build(self):
        """Run the complete build process."""
        print(f"\n{'='*60}")
        print(f"Building Bambu Farm Monitor {APP_VERSION} for Windows")
        print(f"{'='*60}")

        self.clean()
        self.download_go2rtc()
        self.build_executables()
        self.prepare_distribution()
        self.build_installer()

        print(f"\n{'='*60}")
        print("Build complete!")
        print(f"{'='*60}")
        print(f"\nOutput directory: {self.output_dir}")
        print(f"Installer: {self.windows_dir / 'Output' / f'{APP_NAME}Setup.exe'}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        builder = WindowsBuilder()
        builder.clean()
        return

    builder = WindowsBuilder()
    builder.build()


if __name__ == "__main__":
    main()
