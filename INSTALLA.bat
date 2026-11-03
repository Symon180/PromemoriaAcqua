@echo off
REM Installer automatico di Promemoria Acqua per Windows 10/11.
REM Registra l'avvio automatico all'accesso utente (Task Scheduler) senza richiedere diritti di amministratore.

setlocal
title Promemoria Acqua - Installazione Windows
set "PROMEMORIA_SRC=%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$testo = Get-Content -LiteralPath '%~f0' -Raw; Invoke-Expression $testo.Substring($testo.IndexOf('#PS' + 'START'))"
exit /b %errorlevel%

#PSSTART
$ErrorActionPreference = "Stop"
$TaskName  = "Promemoria Acqua"
$TargetDir = Join-Path $env:USERPROFILE "Documents\Promemoria_Acqua"
$SourceDir = $env:PROMEMORIA_SRC.TrimEnd("\")

$pythonw = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $pythonw) {
    Write-Host "Installazione Python tramite winget..." -ForegroundColor Cyan
    winget install --id Python.Python.3.12 --exact --scope user --silent --accept-package-agreements --accept-source-agreements | Out-Null
    $pythonw = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
}

if (-not $pythonw) {
    Write-Host "Errore: pythonw.exe non trovato. Installa Python 3.10+ da python.org." -ForegroundColor Red
    Read-Host "Premi INVIO per chiudere"
    exit 1
}

New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
Copy-Item -Path (Join-Path $SourceDir "promemoria_acqua") -Destination $TargetDir -Recurse -Force

$azione = New-ScheduledTaskAction -Execute $pythonw -Argument "-m promemoria_acqua" -WorkingDirectory $TargetDir
$innesco = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$impostazioni = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit ([TimeSpan]::Zero) -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName -Action $azione -Trigger $innesco -Settings $impostazioni -Description "Promemoria per bere acqua ogni 30 minuti" -Force | Out-Null
Start-ScheduledTask -TaskName $TaskName

Write-Host ""
Write-Host "  INSTALLAZIONE COMPLETATA!" -ForegroundColor Green
Write-Host "  Dovresti aver appena visto la prima notifica." -ForegroundColor White
Read-Host "  Premi INVIO per chiudere"
