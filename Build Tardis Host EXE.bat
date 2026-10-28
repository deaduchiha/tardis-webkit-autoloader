@echo off
setlocal
set "SCRIPT=%~dp0Build Tardis Host EXE.ps1"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%"
if errorlevel 1 (
  echo.
  echo Windows executable build failed.
  pause
  exit /b 1
)

echo.
pause
