# ==============================================================================
#                  ⚡ ESHKERI // AUTOMATED BUILD & PACKAGING ⚡
#             PowerShell Script to build Eshkeri.exe & Eshkeri_Setup.exe
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "ESHKERI BUILD SYSTEM // COMPILER & PACKAGER"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

function Write-CyberHeader {
    Write-Host ""
    Write-Host " ==============================================================================" -ForegroundColor Cyan
    Write-Host "                ⚡ ESHKERI // FULL AUTOMATED BUILD SYSTEM ⚡                  " -ForegroundColor Yellow
    Write-Host "         Compiling Application (Eshkeri.exe) & Installer (Eshkeri_Setup.exe)   " -ForegroundColor DarkCyan
    Write-Host " ==============================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Num, [string]$Title)
    Write-Host " [STEP $Num] " -NoNewline -ForegroundColor Yellow
    Write-Host "$Title..." -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host " [+] $Text" -ForegroundColor Green
}

function Write-Failure {
    param([string]$Text)
    Write-Host " [!] $Text" -ForegroundColor Red
}

Write-CyberHeader

# ------------------------------------------------------------------------------
# 0. CLOSE RUNNING INSTANCES TO PREVENT FILE LOCKS
# ------------------------------------------------------------------------------
Write-Step "0" "Closing running instances of Eshkeri or Setup"
Get-Process -Name "Eshkeri", "Eshkeri_Setup", "dummy_stub" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 500
Write-Success "Process lock check completed"

# ------------------------------------------------------------------------------
# 1. DETECT PYTHON & CSC COMPILER
# ------------------------------------------------------------------------------
Write-Step "1" "Detecting Compilers (Python & C# Roslyn/CSC)"

$PythonExe = "python"
if (-not (Get-Command $PythonExe -ErrorAction SilentlyContinue)) {
    $PythonCandidates = @(
        "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe"
    )
    foreach ($cand in $PythonCandidates) {
        if (Test-Path $cand) {
            $PythonExe = $cand
            break
        }
    }
}
Write-Success "Using Python: $PythonExe"

$CscCandidates = @(
    "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
    "C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
)
$CscExe = $CscCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $CscExe) {
    Write-Failure "csc.exe not found in Microsoft.NET Framework directories!"
} else {
    Write-Success "Using C# Compiler: $CscExe"
}

# ------------------------------------------------------------------------------
# 2. COMPILE DUMMY_STUB.EXE
# ------------------------------------------------------------------------------
if ($CscExe -and (Test-Path "$ScriptDir\dummy_stub.cs")) {
    Write-Step "2" "Compiling dummy_stub.exe (Background Simulation Engine)"
    & $CscExe /target:winexe /optimize+ /out:"$ScriptDir\dummy_stub.exe" "$ScriptDir\dummy_stub.cs" | Out-Null
    if ($LASTEXITCODE -eq 0 -and (Test-Path "$ScriptDir\dummy_stub.exe")) {
        $stubSize = (Get-Item "$ScriptDir\dummy_stub.exe").Length / 1KB
        Write-Success "Compiled dummy_stub.exe ($([math]::Round($stubSize, 2)) KB)"
    } else {
        Write-Failure "Failed to compile dummy_stub.exe"
    }
}

# ------------------------------------------------------------------------------
# 3. BUILD ESHKERI.EXE (STANDALONE APPLICATION)
# ------------------------------------------------------------------------------
Write-Step "3" "Building Eshkeri.exe with PyInstaller"

$BuildAppCmd = @(
    "-m", "PyInstaller",
    "--noconsole",
    "--onefile",
    "--name=Eshkeri",
    "--icon=app_icon.ico",
    "--add-data=icons;icons",
    "--add-data=dummy_stub.exe;.",
    "--add-data=games_db.json;.",
    "--add-data=discord_detectable.json;.",
    "--add-data=app_icon.png;.",
    "--add-data=app_icon.ico;.",
    "--hidden-import=PyQt5.QtMultimedia",
    "--hidden-import=PyQt5.QtMultimediaWidgets",
    "--hidden-import=game_icons",
    "--hidden-import=pypresence",
    "--clean",
    "main.py"
)

& $PythonExe $BuildAppCmd
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Building Eshkeri.exe failed!"
    exit 1
}

$DistApp = Join-Path $ScriptDir "dist\Eshkeri.exe"
$TargetApp = Join-Path $ScriptDir "Eshkeri.exe"
if (Test-Path $DistApp) {
    Copy-Item $DistApp $TargetApp -Force
    $appSize = (Get-Item $TargetApp).Length / 1MB
    Write-Success "Eshkeri.exe compiled successfully ($([math]::Round($appSize, 2)) MB)"
}

# ------------------------------------------------------------------------------
# 4. REPACK PAYLOAD.ZIP FOR INSTALLER
# ------------------------------------------------------------------------------
Write-Step "4" "Packaging payload.zip (Application + Complete Source Code + Assets)"

$PackScript = @"
import os, zipfile

base = r'$ScriptDir'
zip_path = os.path.join(base, 'payload.zip')

files_to_pack = [
    'Eshkeri.exe',
    'main.py',
    'main_window.py',
    'spoofer.py',
    'game_icons.py',
    'games_db.json',
    'discord_detectable.json',
    'dummy_stub.cs',
    'dummy_stub.exe',
    'app_icon.ico',
    'app_icon.png',
    'fonpril.mp4',
    'README.txt',
    'build.py',
    'build.ps1',
    'installer.py',
    'Eshkeri.spec'
]

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files_to_pack:
        fp = os.path.join(base, f)
        if os.path.exists(fp):
            z.write(fp, arcname=f)
    icons_dir = os.path.join(base, 'icons')
    if os.path.exists(icons_dir):
        for root, dirs, files in os.walk(icons_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base)
                z.write(full_path, arcname=rel_path)

print(f'PAYLOAD_SIZE:{os.path.getsize(zip_path) / (1024*1024):.2f}')
"@

$PackOut = & $PythonExe -c $PackScript
$PayloadMb = ($PackOut | Select-String "PAYLOAD_SIZE:([0-9.]+)").Matches.Groups[1].Value
Write-Success "payload.zip created successfully ($PayloadMb MB)"

# ------------------------------------------------------------------------------
# 5. BUILD ESHKERI_SETUP.EXE (GRAPHICAL INSTALLER)
# ------------------------------------------------------------------------------
Write-Step "5" "Building Eshkeri_Setup.exe with PyInstaller"

$BuildSetupCmd = @(
    "-m", "PyInstaller",
    "--noconsole",
    "--onefile",
    "--name=Eshkeri_Setup",
    "--icon=app_icon.ico",
    "--add-data=payload.zip;.",
    "--add-data=app_icon.ico;.",
    "--clean",
    "installer.py"
)

& $PythonExe $BuildSetupCmd
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Building Eshkeri_Setup.exe failed!"
    exit 1
}

$DistSetup = Join-Path $ScriptDir "dist\Eshkeri_Setup.exe"
$TargetSetup = Join-Path $ScriptDir "Eshkeri_Setup.exe"
if (Test-Path $DistSetup) {
    Copy-Item $DistSetup $TargetSetup -Force
    $setupSize = (Get-Item $TargetSetup).Length / 1MB
    Write-Success "Eshkeri_Setup.exe compiled successfully ($([math]::Round($setupSize, 2)) MB)"
}

# ------------------------------------------------------------------------------
# 6. FINAL SUMMARY
# ------------------------------------------------------------------------------
Write-Host ""
Write-Host " ==============================================================================" -ForegroundColor Green
Write-Host "                       ★ ALL BUILDS COMPLETED SUCCESSFULLY ★                    " -ForegroundColor Yellow
Write-Host " ==============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  1. Main Executable:  " -NoNewline -ForegroundColor Cyan
Write-Host "$TargetApp ($([math]::Round((Get-Item $TargetApp).Length / 1MB, 2)) MB)" -ForegroundColor Yellow
Write-Host "  2. Setup Installer:  " -NoNewline -ForegroundColor Cyan
Write-Host "$TargetSetup ($([math]::Round((Get-Item $TargetSetup).Length / 1MB, 2)) MB)" -ForegroundColor Yellow
Write-Host "  3. Packed Payload:   " -NoNewline -ForegroundColor Cyan
Write-Host "$ScriptDir\payload.zip ($PayloadMb MB)" -ForegroundColor Yellow
Write-Host ""
Write-Host " [Cyberpunk HUD]: Ready for deployment." -ForegroundColor DarkCyan
Write-Host ""
