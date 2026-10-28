@echo off
setlocal
set "SCRIPT=%~dp0Start Tardis Host.ps1"

if not exist "%SCRIPT%" (
  echo Could not find the Tardis host launcher:
  echo   %SCRIPT%
  echo.
  pause
  exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%"
exit /b %ERRORLEVEL%
