param(
  [ValidateSet("setup","test","cov","run","format","lint","all")]
  [string]$Task = "all"
)

$ErrorActionPreference = "Stop"

function Ensure-Venv {
  if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    python -m venv .venv
  }
  . .\.venv\Scripts\Activate.ps1
}

function Install-Deps {
  python -m pip install -U pip
  pip install -r .\requirements-dev.txt
}

switch ($Task) {
  "setup" {
    Ensure-Venv
    Install-Deps
    Write-Host "Setup complete."
  }
  "test" {
    Ensure-Venv
    pytest -q
  }
  "cov" {
    Ensure-Venv
    pytest --cov=. --cov-report=term-missing
  }
  "run" {
    Ensure-Venv
    python .\src\main.py
    if (Test-Path .\events.json) { Get-Item .\events.json | Out-String | Write-Host }
  }
  "format" {
    Ensure-Venv
    black .\src .\tests
  }
  "lint" {
    Ensure-Venv
    ruff check .\src .\tests
  }
  "all" {
    Ensure-Venv
    Install-Deps
    ruff check .\src .\tests
    black .\src .\tests
    pytest -q
    pytest --cov=. --cov-report=term-missing
    python .\src\main.py
    if (Test-Path .\events.json) { Get-Item .\events.json | Out-String | Write-Host }
  }
}

# --- Auto-refresh submission copy (no git commit)
if (Test-Path .\events.json) {
  New-Item -ItemType Directory -Force -Path .\submission | Out-Null
  Copy-Item .\events.json .\submission\events.json -Force
}

