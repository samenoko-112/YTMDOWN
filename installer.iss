[Setup]

AppName=YTMDOWN
AppVersion={#AppVersion}
DefaultDirName={autopf}\YTMDOWN
DefaultGroupName=YTMDOWN
OutputDir=installer_output
OutputBaseFilename=YTMDOWN-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\YTMDOWN\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\\YTMDOWN"; Filename: "{app}\\YTMDOWN.exe"
Name: "{autodesktop}\\YTMDOWN"; Filename: "{app}\\YTMDOWN.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked