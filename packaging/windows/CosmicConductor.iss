#define MyAppName "Cosmic Conductor Engine"
#define MyAppVersion "0.2.0"
#define MyAppPublisher "NavisWORLD"
#define MyAppExeName "CosmicConductor.exe"

[Setup]
AppId={{6F1D7E1E-9F6E-4F35-A8D9-CC667C0C0E20}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Cosmic Conductor Engine
DefaultGroupName=Cosmic Conductor Engine
OutputDir={#SourcePath}\..\..\release\windows
OutputBaseFilename=Cosmic-Conductor-Engine-Setup-v0.2.0
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "{#SourcePath}\..\..\dist\CosmicConductor.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Cosmic Conductor Engine"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Cosmic Conductor Engine"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Cosmic Conductor Engine"; Flags: nowait postinstall skipifsilent
