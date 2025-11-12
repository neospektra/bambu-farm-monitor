# Bambu Farm Monitor - Windows Native Build

This directory contains everything needed to build a native Windows application that runs **without Docker**.

## Features

✅ **No Docker required** - Runs natively on Windows
✅ **Professional installer** - MSI-style installation with Inno Setup
✅ **System tray application** - Easy access and control
✅ **Windows service** - Can run in the background
✅ **Auto-start with Windows** - Optional startup configuration
✅ **Proper uninstaller** - Clean removal via Windows Add/Remove Programs
✅ **Low resource usage** - No container overhead

## Architecture

The Windows native version consists of:

1. **Service Manager** (`service_manager.py`) - Orchestrates all components
2. **System Tray App** (`tray_app.py`) - User interface and control
3. **Web Server** (`web_server.py`) - Replaces nginx, serves static files and proxies APIs
4. **Config API** (`../api/config_api.py`) - Printer configuration management
5. **Status API** (`../api/status_api.py`) - MQTT status monitoring
6. **go2rtc** - Video streaming server (downloaded automatically)

## Prerequisites

### For Building

- **Windows 10/11** (64-bit)
- **Python 3.11+** (for building)
- **Inno Setup 6** (for creating installer)
  - Download from: https://jrsoftware.org/isdl.php
- **Visual C++ Redistributable** (usually pre-installed)

### For Running (End Users)

- **Windows 10/11** (64-bit)
- **4GB RAM minimum**
- **Network access** to Bambu Lab printers

## Build Process

### Step 1: Install Build Dependencies

```powershell
# Navigate to the windows directory
cd windows

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Run the Build Script

The build script handles everything automatically:

```powershell
python build.py
```

This will:
1. ✅ Clean previous builds
2. ✅ Download go2rtc Windows binary automatically
3. ✅ Build executables with PyInstaller
4. ✅ Prepare distribution folder with all files
5. ✅ Create installer with Inno Setup (if installed)

### Step 3: Locate the Installer

The installer will be created at:
```
windows/Output/BambuFarmMonitorSetup.exe
```

## Manual Build Steps

If you prefer to build manually or the automated script fails:

### 1. Download go2rtc

```powershell
# Create bin directory
New-Item -ItemType Directory -Path build\bin -Force

# Download go2rtc for Windows
$url = "https://github.com/AlexxIT/go2rtc/releases/download/v1.9.4/go2rtc_win64.zip"
Invoke-WebRequest -Uri $url -OutFile build\bin\go2rtc.zip

# Extract
Expand-Archive -Path build\bin\go2rtc.zip -DestinationPath build\bin
Remove-Item build\bin\go2rtc.zip
```

### 2. Build Each Executable

```powershell
# Build service manager
pyinstaller --name service_manager --onefile --console service_manager.py

# Build tray application
pyinstaller --name bambu-monitor --onefile --windowed tray_app.py

# Build web server
pyinstaller --name web_server --onefile --console web_server.py
```

### 3. Prepare Distribution

Create the following structure:
```
output/
├── windows/
│   ├── service_manager.exe
│   ├── bambu-monitor.exe
│   └── web_server.exe
├── bin/
│   └── go2rtc.exe
├── api/
│   ├── config_api.py
│   └── status_api.py
├── www/
│   └── (all web files)
└── README.txt
```

### 4. Compile Installer

```powershell
# Compile with Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

## File Descriptions

### Python Scripts

- **`service_manager.py`** - Main service that manages all subprocesses
  - Starts/stops go2rtc, web server, and APIs
  - Monitors processes and restarts if they crash
  - Handles configuration directory creation

- **`tray_app.py`** - System tray application
  - Provides icon in Windows system tray
  - Menu for start/stop/restart service
  - Quick access to dashboard and config folder
  - Shows service status

- **`web_server.py`** - Python-based web server
  - Serves static files (HTML, CSS, JS)
  - Proxies requests to go2rtc API
  - Proxies requests to config and status APIs
  - Replaces nginx for Windows

- **`build.py`** - Automated build script
  - Downloads go2rtc automatically
  - Builds all executables with PyInstaller
  - Prepares distribution folder
  - Compiles installer with Inno Setup

### Configuration Files

- **`requirements.txt`** - Python dependencies for Windows build
- **`installer.iss`** - Inno Setup script for creating installer
  - Defines installation wizard
  - Sets up file associations
  - Creates shortcuts
  - Registers uninstaller

## Installation Locations

### Application Files
```
C:\Program Files\Bambu Farm Monitor\
├── windows\       - Executables
├── bin\          - go2rtc binary
├── api\          - Python API scripts
└── www\          - Web interface files
```

### Configuration & Data
```
%LOCALAPPDATA%\BambuFarmMonitor\
├── printers.json  - Printer configurations
├── go2rtc.yaml   - Video streaming config
└── *.log         - Log files
```

### Registry
```
HKEY_CURRENT_USER\Software\BambuFarmMonitor
├── InstallPath    - Installation directory
└── Version        - Installed version
```

## Usage

### End User Installation

1. Download `BambuFarmMonitorSetup.exe`
2. Run the installer (requires Administrator)
3. Follow the installation wizard
4. Application starts automatically
5. System tray icon appears
6. Right-click icon → "Open Dashboard"

### Command Line

The service can be controlled via command line:

```powershell
# Start service
service_manager.exe start

# Stop service
service_manager.exe stop

# Restart service
service_manager.exe restart

# Check status
service_manager.exe status
```

### System Tray

The tray application provides:
- **Open Dashboard** - Opens http://localhost:8080 in browser
- **Start Service** - Starts all components
- **Stop Service** - Stops all components
- **Restart Service** - Restarts all components
- **Open Config Folder** - Opens configuration directory
- **Quit** - Exits tray app and stops service

## Ports Used

| Port | Service | Purpose |
|------|---------|---------|
| 8080 | Web Server | Main dashboard interface |
| 1984 | go2rtc | WebRTC video streaming |
| 5000 | Config API | Printer configuration |
| 5001 | Status API | MQTT status updates |

## Troubleshooting

### Build Issues

**PyInstaller not found:**
```powershell
pip install pyinstaller
```

**Inno Setup not found:**
- Download from https://jrsoftware.org/isdl.php
- Install to default location
- Or manually compile with ISCC.exe

**go2rtc download fails:**
- Download manually from: https://github.com/AlexxIT/go2rtc/releases
- Place `go2rtc.exe` in `build/bin/` directory

### Runtime Issues

**Port conflicts:**
- Check if ports 8080, 1984, 5000, 5001 are in use
- Use `netstat -ano | findstr "8080"` to check
- Stop conflicting applications

**Service won't start:**
- Check logs in `%LOCALAPPDATA%\BambuFarmMonitor\`
- Ensure all executables are present
- Run `service_manager.exe` manually to see errors

**Tray icon doesn't appear:**
- Check Windows notification settings
- Ensure system tray is not hidden
- Run `bambu-monitor.exe` manually to see errors

## Development

### Testing Without Building

You can run the components directly with Python:

```powershell
# Start service manager
python service_manager.py start

# Start tray app (in separate window)
python tray_app.py
```

### Cleaning Build Artifacts

```powershell
python build.py clean
```

## Advantages over Docker

✅ **No Docker Desktop needed** - Avoid licensing concerns
✅ **Faster startup** - No container initialization
✅ **Lower memory usage** - No container overhead
✅ **Native Windows integration** - System tray, services, etc.
✅ **Easier for non-technical users** - Simple installer
✅ **Better performance** - Direct hardware access
✅ **Familiar installation** - Standard Windows application

## Future Enhancements

Potential improvements:

- [ ] Windows Service installation (run as background service)
- [ ] Auto-update functionality
- [ ] Custom icon file
- [ ] Digital signature for installer
- [ ] Localization support
- [ ] GUI configuration tool (beyond web interface)
- [ ] Bandwidth monitoring
- [ ] Notification system for print completion

## Contributing

To contribute to the Windows native build:

1. Test on different Windows versions (10, 11)
2. Report build issues
3. Improve documentation
4. Suggest features
5. Submit pull requests

## Support

- GitHub Issues: https://github.com/neospektra/bambu-farm-monitor/issues
- Documentation: https://github.com/neospektra/bambu-farm-monitor/wiki

## License

Same as main project (MIT License)
