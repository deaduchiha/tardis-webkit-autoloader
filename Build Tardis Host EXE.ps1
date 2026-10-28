$ErrorActionPreference = 'Stop'

$projectDir = $PSScriptRoot
$hostScript = Join-Path $projectDir 'webkit-autoloader-host.py'
$icon = Join-Path $projectDir 'assets\icon.ico'

if (-not (Test-Path -LiteralPath $hostScript -PathType Leaf)) {
    throw "Generated host script not found: $hostScript"
}
if (-not (Test-Path -LiteralPath $icon -PathType Leaf)) {
    throw "Tardis Windows icon not found: $icon"
}

$python = Get-Command 'py.exe' -ErrorAction SilentlyContinue
$pythonPrefix = @('-3')
if (-not $python) {
    $python = Get-Command 'python.exe' -ErrorAction SilentlyContinue
    $pythonPrefix = @()
}
if (-not $python) {
    throw 'Python 3 was not found. Install Python 3, then run this script again.'
}

$hostSource = Get-Content -LiteralPath $hostScript -Raw
$versionMatch = [regex]::Match($hostSource, '(?m)^VERSION\s*=\s*"([^"]+)"')
$version = if ($versionMatch.Success) { $versionMatch.Groups[1].Value } else { 'custom' }
$exeName = "webkit-autoloader-host_v$version"

Push-Location $projectDir
try {
    & $python.Source @pythonPrefix -m PyInstaller --version *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Installing PyInstaller for the current Windows Python...' -ForegroundColor Cyan
        & $python.Source @pythonPrefix -m pip install --user pyinstaller
        if ($LASTEXITCODE -ne 0) { throw 'Could not install PyInstaller.' }
    }

    & $python.Source @pythonPrefix -m PyInstaller `
        --onefile `
        --noconfirm `
        --clean `
        --uac-admin `
        --icon $icon `
        --name $exeName `
        $hostScript

    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller failed to build the Windows executable.' }

    $exePath = Join-Path $projectDir "dist\$exeName.exe"
    Write-Host ''
    Write-Host 'Windows executable created:' -ForegroundColor Green
    Write-Host "  $exePath"
    Write-Host 'Copy this EXE and run it on the Windows PC that shares a network with the PS5.'
}
finally {
    Pop-Location
}
