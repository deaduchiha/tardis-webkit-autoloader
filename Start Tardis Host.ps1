$ErrorActionPreference = 'Stop'

$hostScript = Join-Path $PSScriptRoot 'webkit-autoloader-host.py'
if (-not (Test-Path -LiteralPath $hostScript -PathType Leaf)) {
    Write-Host 'The generated Tardis setup host was not found:' -ForegroundColor Red
    Write-Host "  $hostScript"
    Write-Host 'Build it first with: make host HOST_PAYLOAD=<installer.elf>'
    Read-Host 'Press Enter to close'
    exit 1
}

$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
$isAdministrator = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdministrator) {
    Write-Host 'Requesting administrator permission for DNS and HTTPS ports 53 and 443...'
    $quotedScript = '"' + $PSCommandPath + '"'
    $elevated = Start-Process -FilePath 'powershell.exe' -Verb RunAs -Wait -PassThru `
        -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File $quotedScript"
    exit $elevated.ExitCode
}

$pythonLauncher = Get-Command 'py.exe' -ErrorAction SilentlyContinue
$python = Get-Command 'python.exe' -ErrorAction SilentlyContinue

Write-Host 'Starting the Tardis PS5 setup host.' -ForegroundColor Cyan
Write-Host 'Use the IP printed below as the PS5 Primary DNS address.'
Write-Host 'Keep this window open while setting up the PS5; press Ctrl-C to stop.'
Write-Host ''

if ($pythonLauncher) {
    & $pythonLauncher.Source -3 $hostScript --verbose
} elseif ($python) {
    & $python.Source $hostScript --verbose
} else {
    Write-Host 'Python 3 was not found. Install Python 3, then run this launcher again.' -ForegroundColor Red
    Read-Host 'Press Enter to close'
    exit 1
}

exit $LASTEXITCODE
