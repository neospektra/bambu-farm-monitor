# Finding Printer Information

To configure Bambu Farm Monitor, you need three pieces of information for each printer:

1. **IP Address** - The local network address of the printer
2. **Access Code** - 8-digit MQTT password
3. **Serial Number** - Unique printer identifier (recommended)

This guide shows you how to find each of these.

## Finding the IP Address

There are several methods to find your printer's IP address.

### Method 1: Printer Display (Easiest)

1. On your printer's touchscreen, tap **Settings** (gear icon)
2. Navigate to **Network** → **Connection Info** or **LAN Settings**
3. The IP address is displayed (e.g., `192.168.1.100`)

**Note:** The exact menu location varies by printer model:
- **P1S/P1P**: Settings → Network → Wi-Fi → Details
- **X1 Carbon**: Settings → LAN Settings → IP Address
- **A1**: Settings → Device → Network Info

### Method 2: Bambu Studio

1. Open **Bambu Studio**
2. Go to **Devices** tab
3. Find your printer in the list
4. Right-click → **View Device Info** or hover over the printer name
5. The IP address is shown in the device details

### Method 3: Bambu Handy App

1. Open the **Bambu Handy** mobile app
2. Select your printer
3. Tap the **Settings** icon (⚙️)
4. Navigate to **Network Settings** or **Device Info**
5. The IP address is displayed

### Method 4: Router DHCP List

1. Log into your router's admin panel (typically `192.168.1.1` or `192.168.0.1`)
2. Find **DHCP Client List**, **Connected Devices**, or **LAN Status**
3. Look for devices named "Bambu" or with manufacturer "Bambu Lab"
4. Note the IP address

**Tip:** Device names usually include the printer model (e.g., "BambuLab-P1S-1234")

### Method 5: Network Scanner

Use a network scanning tool:

**Windows:**
```powershell
arp -a
```
Look for devices in your subnet

**Linux/Mac:**
```bash
nmap -sn 192.168.1.0/24
# Or use arp
arp -a
```

**Mobile Apps:**
- iOS: Fing, Network Analyzer
- Android: Fing, Network Scanner

### Assign Static IP (Recommended)

To prevent the IP from changing:

1. Log into your router
2. Find **DHCP Reservation** or **Static IP Assignment**
3. Reserve the current IP for your printer's MAC address
4. Save settings and reboot printer (optional)

This ensures the printer always gets the same IP address.

## Finding the Access Code

The access code is an 8-digit number used for MQTT authentication.

### Method 1: Printer Display (Primary Method)

1. Tap **Settings** on the printer touchscreen
2. Navigate to **Network** → **MQTT** or **LAN Access**
3. You'll see **Access Code** or **MQTT Password**
4. Note the 8-digit code (e.g., `12345678`)

**If MQTT is disabled:**
1. Toggle **MQTT** or **LAN Access** to **ON**
2. The access code will be displayed
3. Write it down - you won't see it again without resetting

**Important Notes:**
- The access code is generated when MQTT is first enabled
- If you lose it, you must disable and re-enable MQTT to generate a new one
- Each printer has its own unique access code

### Method 2: Bambu Studio

1. Open **Bambu Studio**
2. Go to **Devices**
3. Right-click your printer → **Edit Device**
4. The access code may be shown in the authentication section

**Note:** This only works if you previously saved the code in Bambu Studio

### Method 3: Reset Access Code

If you've lost the access code:

1. On the printer, go to **Settings** → **Network** → **MQTT**
2. Toggle MQTT **OFF**
3. Toggle MQTT **ON** again
4. A new access code will be generated
5. **Write it down immediately**

**Warning:** Changing the access code will break any existing MQTT connections (including Bambu Studio if configured for LAN mode).

## Finding the Serial Number

The serial number uniquely identifies your printer and is used for MQTT topic routing.

### Method 1: Printer Display

1. Tap **Settings** on the touchscreen
2. Navigate to **Device** or **About**
3. Look for **Serial Number** or **SN**
4. Format: Usually starts with `01` (e.g., `01P00A411800001`)

### Method 2: Physical Label

1. Check the bottom or back of the printer
2. Look for a label with a QR code
3. The serial number is printed below or next to the QR code

### Method 3: Bambu Studio

1. Open **Bambu Studio**
2. Go to **Devices** tab
3. Right-click your printer → **View Device Info**
4. Serial number is displayed

### Method 4: Bambu Handy App

1. Open the **Bambu Handy** app
2. Select your printer
3. Tap **Settings** (⚙️)
4. Navigate to **Device Info** or **About**
5. Serial number is listed

### Serial Number Format

Bambu Lab serial numbers follow this format:
```
01P00A411800001
││├───┤├─────┤
││  │    └─ Unit number
││  └────── Production batch
│└───────── Model code
└────────── Manufacturer code (01 = Bambu Lab)
```

**Common Model Codes:**
- `P1S` = P1S printer
- `X1C` = X1 Carbon
- `A1` = A1 Mini

## Configuration Example

Once you have all three pieces of information:

```yaml
Printer Name: Farm P1S #1
IP Address: 192.168.1.100
Access Code: 12345678
Serial Number: 01P00A411800001
```

Enter these into the Bambu Farm Monitor setup wizard.

## Troubleshooting

### Can't Find IP Address

**Problem:** Printer not showing in router DHCP list

**Solutions:**
1. Ensure printer is connected to Wi-Fi (check touchscreen status)
2. Restart the printer
3. Verify you're checking the correct network (2.4GHz vs 5GHz)
4. Check if printer is on a guest network

### MQTT Option Not Available

**Problem:** No MQTT or LAN Access option in printer settings

**Solutions:**
1. Update printer firmware to latest version
2. Ensure you're in **Settings** → **Network** (not other settings)
3. Some early firmware versions may not support MQTT

### Access Code Not Working

**Problem:** Authentication fails with correct access code

**Solutions:**
1. Verify you're using the IP address, not hostname
2. Double-check the code (easy to confuse 0/O and 1/I)
3. Ensure MQTT is enabled on the printer
4. Try regenerating the access code

### Serial Number Not Found

**Problem:** Can't locate serial number

**Solutions:**
1. Check original packaging - often printed on box
2. Contact Bambu Lab support with purchase receipt
3. Serial numbers are optional - the system works without them, but status updates may be less reliable

## Next Steps

Once you have your printer information:
- **[First Time Setup](First-Time-Setup.md)** - Complete the setup wizard
- **[Printer Configuration](Printer-Configuration.md)** - Add your printers
- **[MQTT Connection Problems](MQTT-Connection-Problems.md)** - Troubleshoot connection issues
