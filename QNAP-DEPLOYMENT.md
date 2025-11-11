# QNAP Container Station Deployment Guide
## Bambu Labs P1S Farm Monitor

This guide will walk you through deploying the Bambu Farm Monitor on your QNAP NAS using Container Station.

## What You Need

Before starting, gather this information for each printer:

1. **IP Address** - Find in printer settings or router DHCP table
2. **Access Code** - Printer Settings > Network > LAN Mode MQTT
3. **Serial Number** - Printer Settings > Device > Device Info

## Step-by-Step Deployment

### Step 1: Get the Container Image

**Option A: Pull from Docker Hub (Recommended - Easiest!)**

No file transfer needed! Container Station will download directly from Docker Hub:

1. Open **Container Station** from QTS menu
2. Click **Create** button (top of page)
3. Select **Create Container**
4. In the **Image** field, type: `neospektra/bambu-farm-monitor:latest`
5. Container Station will automatically pull the image
6. Skip to Step 2 below

**Option B: Import from Tar File**

If you have the tar file or prefer offline installation:

1. Open **File Station** on your QNAP
2. Create a temporary folder (e.g., `docker-images`)
3. Upload `bambu-farm-monitor.tar` to this folder
   - Via web interface (drag and drop)
   - Via SMB/CIFS network share
   - Via SFTP/FTP
4. Open **Container Station** from QTS menu
5. Click **Images** tab (left sidebar)
6. Click **Import** button (top right)
7. Click **Browse** and navigate to your uploaded tar file
8. Select `bambu-farm-monitor.tar`
9. Click **OK** to start import
10. Wait for import to complete (progress bar shows status)

### Step 2: Create Storage Location

1. Open **File Station**
2. Navigate to `/Container` (or create it if it doesn't exist)
3. Create a new folder: `bambu-config`
4. This folder will store your printer configuration

Full path should be: `/share/Container/bambu-config`

### Step 3: Create the Container

**If you used Option A (Docker Hub):**
- Continue from the Create Container dialog that opened in Step 1

**If you used Option B (Tar File):**
1. In Container Station, go to **Images** tab
2. Find `bambu-farm-monitor` or `neospektra/bambu-farm-monitor` in the image list
3. Click the **Create** button next to it

#### Container Configuration Wizard:

**Page 1 - Basic Settings:**
- **Name**: `bambu-farm-monitor`
- **CPU Limit**: `2` (or leave default)
- **Memory Limit**: `2048 MB` (minimum 1024 MB)
- Click **Advanced Settings**

**Page 2 - Network:**
- Select **Bridge** mode
- Add port mappings (click + for each):
  ```
  Host Port 8080  → Container Port 8080
  Host Port 1984  → Container Port 1984
  Host Port 5000  → Container Port 5000
  Host Port 5001  → Container Port 5001
  ```

**Page 3 - Shared Folders:**
- Click **Add** or **Volume**
- **Mount local folder**:
  - **Host Path**: Browse and select `/Container/bambu-config`
  - **Mount Path**: Type exactly: `/app/config`
  - **Permission**: Read/Write
- Click **OK**

**Page 4 - Environment (Optional):**
You can skip this - we'll configure via the web UI instead.
But if you want to pre-configure, add these variables:
```
PRINTER1_NAME = Farm P1S AMS-1
PRINTER1_IP = 192.168.1.100
PRINTER1_CODE = 12345678
PRINTER1_SERIAL = 01P09A440200543
```
(Repeat for PRINTER2_, PRINTER3_, PRINTER4_)

**Final Page:**
- Review settings
- Click **Create** to start the container

### Step 4: Verify Container is Running

1. Go to **Containers** tab in Container Station
2. Look for `bambu-farm-monitor` - status should be **Running**
3. If status is **Error** or **Stopped**:
   - Click on the container name
   - Check **Logs** tab for error messages
   - Common issues: Port conflicts, volume permissions

### Step 5: Access the Web Interface

1. Open a web browser on any device on your network
2. Navigate to: `http://YOUR-QNAP-IP:8080`
   - Replace `YOUR-QNAP-IP` with your NAS IP address
   - Example: `http://192.168.1.50:8080`

You should see the main dashboard with 4 printer camera feeds.

### Step 6: Configure Your Printers

1. Click the **⚙️ Settings** button (top right of web page)
2. The settings page will show 4 printer configuration forms

For each printer:
1. **Printer Name**: Give it a friendly name (e.g., "Front Left Printer")
2. **IP Address**: Enter the printer's IP address
3. **Access Code**: Enter the 8-digit MQTT access code
4. **Serial Number**: Enter the printer serial number (starts with 01P)
5. Click **Test Connection** - should show "Successfully connected"
6. If test fails, verify the information is correct

After configuring all printers:
1. Click **Save Changes**
2. Wait 30 seconds for streams to restart
3. Click **Back to Dashboard**

### Step 7: Verify Everything Works

1. You should see video feeds from all 4 printers
2. Below each video, you should see either:
   - **PRINTING** status with progress bar, layer info, temperatures
   - **IDLE** status with current temperatures
3. Test fullscreen by clicking the **⛶** button on any camera

## Updating to a New Version

### Method 1: Pull Latest from Docker Hub (Easiest)

If you originally deployed from Docker Hub:

1. **Stop the Container**:
   - Container Station > Containers
   - Select `bambu-farm-monitor`
   - Click **Stop**

2. **Note Your Settings**:
   - Click on the container name
   - Go to **Overview** tab
   - Write down the volume mount path (should be `/share/Container/bambu-config`)

3. **Remove Old Container**:
   - Click **Remove** button
   - Confirm removal (your config is safe in the mounted folder!)

4. **Pull Latest Image**:
   - Container Station > Images
   - Find `neospektra/bambu-farm-monitor:latest`
   - Click the **⟳** (refresh/pull) icon to get the latest version

5. **Recreate Container**:
   - Follow Step 3 above
   - **Critical**: Use the SAME volume mount path
   - All your printer settings will be preserved!

### Method 2: Import New Tar File

If you have a new tar file:

1. **Stop and Note Settings** (steps 1-2 from Method 1)
2. **Remove Old Container and Image** (step 3 from Method 1)
3. **Import New Image**: Follow Step 1 Option B above
4. **Recreate Container**: Follow Step 3 above with same volume mount

## Troubleshooting

### "Port is already in use" Error

One of the required ports is in use by another container:

1. Container Station > Containers
2. Check what's using ports 8080, 1984, 5000, 5001
3. Either:
   - Stop/remove the conflicting container, OR
   - Use different host ports (e.g., 8081 instead of 8080)

### Camera Feeds Show Black Screen

1. Check printer IPs are correct in Settings
2. Verify access codes are correct
3. Ensure printers are powered on and connected to network
4. Check Container logs:
   - Container Station > Containers > bambu-farm-monitor
   - Click **Logs** tab
   - Look for "BambuP1SCam" errors

### Status Information Not Appearing

1. Verify you entered the serial numbers correctly
2. Use the **Test Connection** button for each printer
3. Common test results:
   - ✅ **Success**: Everything configured correctly
   - ❌ **Code 4**: Wrong access code
   - ❌ **Code 7**: Wrong or missing serial number
   - ❌ **Timeout**: Can't reach printer (wrong IP or network issue)

### Configuration Not Saving

1. Check volume mount permissions:
   - File Station > Navigate to `/Container/bambu-config`
   - Right-click folder > Properties
   - Ensure you have Read/Write permissions

2. Check if `printers.json` file was created:
   - Should appear in `/Container/bambu-config/printers.json`
   - If missing, check container logs for API errors

### Web UI Not Loading

1. Verify container is running:
   - Container Station > Containers
   - Status should be **Running**

2. Check correct port:
   - Web UI is on port **8080**
   - Example: `http://192.168.1.50:8080`

3. Check firewall:
   - QTS Control Panel > Security > Firewall
   - Ensure port 8080 is allowed

## Container Station Tips

### Viewing Logs

Real-time logs help diagnose issues:
1. Container Station > Containers
2. Click on `bambu-farm-monitor`
3. Go to **Logs** tab
4. Use the search box to filter for specific errors

### Auto-Start on Boot

To make the container start automatically when QNAP boots:
1. Container Station > Containers
2. Select `bambu-farm-monitor`
3. Click **Settings**
4. Enable **Auto-start**
5. Click **OK**

### Resource Monitoring

To check how much CPU/RAM the container uses:
1. Container Station > Containers
2. Click on `bambu-farm-monitor`
3. Go to **Overview** tab
4. View real-time CPU and memory usage graphs

## Getting Help

If you encounter issues not covered here:

1. **Check Container Logs**:
   - Most issues are logged with clear error messages

2. **Check README.md**:
   - More detailed troubleshooting information
   - API documentation
   - Architecture details

3. **Verify Printer Connectivity**:
   - Can you ping the printer from the QNAP?
   - Is the printer in LAN Mode (not Cloud Mode)?

4. **Test Individual Components**:
   - go2rtc API: `http://your-qnap-ip:1984/api/streams`
   - Config API: `http://your-qnap-ip:5000/api/config/printers`
   - Status API: `http://your-qnap-ip:5001/api/status/printers`

## What's Available

You can deploy using either:

- **Docker Hub**: `neospektra/bambu-farm-monitor:latest` (Recommended - no file transfer needed!)
- **Tar File**: `bambu-farm-monitor.tar` (548 MB) - For offline installation

Documentation included:
- `README.md` - Comprehensive technical documentation
- `QNAP-DEPLOYMENT.md` - This step-by-step guide

## Next Steps

Once everything is working:

1. **Bookmark the Dashboard**: `http://your-qnap-ip:8080`
2. **Set up Auto-Start**: So it starts with your QNAP
3. **Test Fullscreen**: Click ⛶ on any camera feed
4. **Configure DHCP Reservations**: Assign static IPs to printers in your router to prevent IP changes

---

Happy Printing! 🖨️
