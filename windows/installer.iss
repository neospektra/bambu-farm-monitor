; Bambu Farm Monitor - Inno Setup Installer Script
; Creates a professional Windows installer

#define MyAppName "Bambu Farm Monitor"
#define MyAppVersion "3.3.9"
#define MyAppPublisher "Bambu Farm Monitor"
#define MyAppURL "https://github.com/neospektra/bambu-farm-monitor"
#define MyAppExeName "bambu-monitor.exe"
#define MyServiceExe "service_manager.exe"

[Setup]
; Basic information
AppId={{9A7D4E8F-3C5B-4F9A-8D6E-1B2C3A4D5E6F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output configuration
OutputDir=Output
OutputBaseFilename=BambuFarmMonitorSetup
Compression=lzma
SolidCompression=yes

; Windows version requirements
MinVersion=10.0
ArchitecturesInstallIn64BitMode=x64

; Visual appearance
WizardStyle=modern
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\windows\{#MyAppExeName}

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startupicon"; Description: "Start with Windows"; GroupDescription: "Startup Options:"
Name: "openafterinstall"; Description: "Open Bambu Farm Monitor after installation"; GroupDescription: "Launch Options:"; Flags: unchecked

[Files]
; Main executables
Source: "output\windows\{#MyAppExeName}"; DestDir: "{app}\windows"; Flags: ignoreversion
Source: "output\windows\{#MyServiceExe}"; DestDir: "{app}\windows"; Flags: ignoreversion
Source: "output\windows\web_server.exe"; DestDir: "{app}\windows"; Flags: ignoreversion

; go2rtc binary
Source: "output\bin\go2rtc.exe"; DestDir: "{app}\bin"; Flags: ignoreversion

; API files
Source: "output\api\*"; DestDir: "{app}\api"; Flags: ignoreversion recursesubdirs createallsubdirs

; Web files
Source: "output\www\*"; DestDir: "{app}\www"; Flags: ignoreversion recursesubdirs createallsubdirs

; Configuration and documentation
Source: "output\README.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "output\requirements.txt"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
; Create config directory in user's AppData
Name: "{localappdata}\BambuFarmMonitor"; Permissions: users-full

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\windows\{#MyAppExeName}"
Name: "{group}\Open Dashboard"; Filename: "http://localhost:8080"
Name: "{group}\Configuration Folder"; Filename: "{localappdata}\BambuFarmMonitor"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop icon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\windows\{#MyAppExeName}"; Tasks: desktopicon

; Startup icon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\windows\{#MyAppExeName}"; Tasks: startupicon

[Registry]
; Register application path
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\App Paths\{#MyAppExeName}"; ValueType: string; ValueName: ""; ValueData: "{app}\windows\{#MyAppExeName}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\App Paths\{#MyAppExeName}"; ValueType: string; ValueName: "Path"; ValueData: "{app}\windows"; Flags: uninsdeletekey

; Application settings
Root: HKCU; Subkey: "Software\BambuFarmMonitor"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\BambuFarmMonitor"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\BambuFarmMonitor"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"

[Run]
; Open application after install
Filename: "{app}\windows\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent; Tasks: openafterinstall

[UninstallRun]
; Stop service before uninstall
Filename: "{app}\windows\{#MyServiceExe}"; Parameters: "stop"; Flags: runhidden

[UninstallDelete]
; Clean up log files
Type: files; Name: "{app}\*.log"
Type: filesandordirs; Name: "{localappdata}\BambuFarmMonitor\*.log"

[Code]
var
  PortCheckPage: TInputQueryWizardPage;
  ConfigDirPage: TInputDirWizardPage;

function IsPortInUse(Port: Integer): Boolean;
var
  ResultCode: Integer;
  Output: AnsiString;
begin
  Result := False;
  if Exec('cmd.exe', '/c netstat -ano | findstr ":'+ IntToStr(Port) + '"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    Result := (ResultCode = 0);
  end;
end;

procedure InitializeWizard;
begin
  // Create port check page
  PortCheckPage := CreateInputQueryPage(wpSelectDir,
    'Port Configuration', 'Checking required ports',
    'The application requires the following ports to be available:' + #13#10 +
    '- 8080 (Web UI)' + #13#10 +
    '- 1984 (go2rtc)' + #13#10 +
    '- 5000 (Config API)' + #13#10 +
    '- 5001 (Status API)' + #13#10 + #13#10 +
    'If any ports are in use, the application may not work correctly.');
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  PortsInUse: String;
begin
  Result := True;

  if CurPageID = PortCheckPage.ID then
  begin
    PortsInUse := '';

    // Check ports
    if IsPortInUse(8080) then
      PortsInUse := PortsInUse + '8080, ';
    if IsPortInUse(1984) then
      PortsInUse := PortsInUse + '1984, ';
    if IsPortInUse(5000) then
      PortsInUse := PortsInUse + '5000, ';
    if IsPortInUse(5001) then
      PortsInUse := PortsInUse + '5001, ';

    if PortsInUse <> '' then
    begin
      // Remove trailing comma and space
      SetLength(PortsInUse, Length(PortsInUse) - 2);

      if MsgBox('The following ports are currently in use: ' + PortsInUse + #13#10 + #13#10 +
                'The application may not work correctly. Do you want to continue?',
                mbConfirmation, MB_YESNO) = IDNO then
      begin
        Result := False;
      end;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Create default config if it doesn't exist
    if not FileExists(ExpandConstant('{localappdata}\BambuFarmMonitor\printers.json')) then
    begin
      SaveStringToFile(ExpandConstant('{localappdata}\BambuFarmMonitor\printers.json'),
        '[]', False);
    end;

    // Create go2rtc config
    if not FileExists(ExpandConstant('{localappdata}\BambuFarmMonitor\go2rtc.yaml')) then
    begin
      SaveStringToFile(ExpandConstant('{localappdata}\BambuFarmMonitor\go2rtc.yaml'),
        'api:' + #13#10 +
        '  listen: ":1984"' + #13#10 + #13#10 +
        'log:' + #13#10 +
        '  level: info' + #13#10 + #13#10 +
        'streams: {}' + #13#10, False);
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ConfigDir: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    ConfigDir := ExpandConstant('{localappdata}\BambuFarmMonitor');

    if MsgBox('Do you want to remove your configuration files and data?' + #13#10 + #13#10 +
              'Directory: ' + ConfigDir,
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      DelTree(ConfigDir, True, True, True);
    end;
  end;
end;
