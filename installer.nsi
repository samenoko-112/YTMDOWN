!include "MUI2.nsh"

RequestExecutionLevel user

!ifndef APP_VERSION
  !define APP_VERSION "0.0.0"
!endif

!define APP_NAME "YTMDOWN"
!define COMPANY   "samenoko-112"
!define INSTALL_DIR "$LOCALAPPDATA\${APP_NAME}"
!define UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

OutFile "build\${APP_NAME}-${APP_VERSION}-setup.exe"
InstallDir ${INSTALL_DIR}

Var StartMenuFolder
Var AddDesktopShortcut

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY

Page custom SelectShortcutsPage SelectShortcutsPageLeave

!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Japanese"

Function SelectShortcutsPage
  nsDialogs::Create 1018
  Pop $0
  ${If} $0 == error
    Abort
  ${EndIf}

  ${NSD_CreateCheckbox} 0 0 100% 12u "デスクトップにショートカットを作成する"
  Pop $1
  ${NSD_Check} $1

  nsDialogs::Show
FunctionEnd

Function SelectShortcutsPageLeave
  ${NSD_GetState} $1 $AddDesktopShortcut
FunctionEnd

Section "Install"
  SetOutPath $INSTDIR
  File /r "dist\YTMDOWN\*.*"

  WriteUninstaller "$INSTDIR\Uninstall.exe"

  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\YTMDOWN.exe"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\Uninstall ${APP_NAME}.lnk" "$INSTDIR\Uninstall.exe"

  ${If} $AddDesktopShortcut == ${BST_CHECKED}
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\YTMDOWN.exe"
  ${EndIf}

  WriteRegStr HKCU "${UNINST_KEY}" "DisplayName" "${APP_NAME} ${APP_VERSION}"
  WriteRegStr HKCU "${UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKCU "${UNINST_KEY}" "Publisher" "${COMPANY}"
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoRepair" 1
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\*.*"
  RMDir /r "$INSTDIR"
  RMDir /r "$SMPROGRAMS\${APP_NAME}"
  Delete "$DESKTOP\${APP_NAME}.lnk"
  DeleteRegKey HKCU "${UNINST_KEY}"
SectionEnd
