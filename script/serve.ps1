# Local wiki preview: build flattened docs, then serve via mkdocs-material.
# All artifacts (.venv/docs/site) live under build/preview/ (gitignored).
# No uv required; auto-creates venv and installs mkdocs-material on first run.
$ErrorActionPreference = "Stop"

$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path }
$ROOT = Split-Path -Parent $scriptDir   # repo root (parent of script/)

$env:NO_MKDOCS_2_WARNING = "1"

# Host python for creating venv / running build.py
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { Write-Host "ERROR: python not found. Install Python 3.11+ and add to PATH."; exit 1 }

$venvDir = Join-Path $ROOT "build\preview\.venv"
$venvPy  = Join-Path $venvDir "Scripts\python.exe"
$venvMk  = Join-Path $venvDir "Scripts\mkdocs.exe"

if (-not (Test-Path $venvPy)) {
    Write-Host "==> First run: creating venv at $venvDir"
    & $py -m venv $venvDir
}

# Ensure mkdocs-material is installed (first run is slow)
& $venvPy -c "import mkdocs" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "==> First run: installing mkdocs-material ..."
    & $venvPy -m pip install -q "mkdocs-material>=9.7"
}

# Build flattened docs
$buildPy = Join-Path $ROOT "script\build.py"
& $venvPy $buildPy
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: build.py failed"; exit 1 }

$cfg = Join-Path $ROOT "script\mkdocs.yml"
Write-Host "==> Preview: http://127.0.0.1:8001/"
& $venvMk serve -f $cfg -a 127.0.0.1:8001
