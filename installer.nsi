; ===============================================
; YTMDOWN NSIS Installer
; ===============================================

!include "MUI2.nsh"

; ----------- 定義 -----------
!ifndef APP_VERSION
  !define APP_VERSION "0.0.0"
!endif

!define APP_NAME "YTMDOWN"
!define COMPANY   "samenoko-112"
!define INSTALL_DIR "$PROGRAMFILES64\\${APP_NAME}"
!define UNINST_KEY "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}"

OutFile "build\\${APP_NAME}-${APP_VERSION}-setup.exe"
InstallDir ${INSTALL_DIR}

; ----------- ページ構成 -----------
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Japanese"

; ----------- インストール処理 -----------
Section "Install"
  SetOutPath $INSTDIR
  ; dist/YTMDOWN の中身をコピー
  File /r "dist\\YTMDOWN\\*.*"

  ; アンインストーラー作成
  WriteUninstaller "$INSTDIR\\Uninstall.exe"

  ; スタートメニューにショートカット
  CreateDirectory "$SMPROGRAMS\\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\YTMDOWN.exe"
  CreateShortcut "$SMPROGRAMS\\${APP_NAME}\\Uninstall ${APP_NAME}.lnk" "$INSTDIR\\Uninstall.exe"

  ; ソフトウェア一覧（コントロールパネル）に追加
  WriteRegStr HKLM "${UNINST_KEY}" "DisplayName" "${APP_NAME} ${APP_VERSION}"
  WriteRegStr HKLM "${UNINST_KEY}" "UninstallString" "$INSTDIR\\Uninstall.exe"
  WriteRegStr HKLM "${UNINST_KEY}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "${UNINST_KEY}" "Publisher" "${COMPANY}"
  WriteRegDWORD HKLM "${UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKLM "${UNINST_KEY}" "NoRepair" 1
SectionEnd

; ----------- アンインストール処理 -----------
Section "Uninstall"
  ; ファイル削除
  Delete "$INSTDIR\\*.*"
  RMDir /r "$INSTDIR"

  ; スタートメニュー削除
  RMDir /r "$SMPROGRAMS\\${APP_NAME}"

  ; レジストリ削除
  DeleteRegKey HKLM "${UNINST_KEY}"
SectionEnd
