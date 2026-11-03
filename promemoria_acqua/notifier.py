"""Invio notifiche desktop native su Windows (Toast WinRT via PowerShell) e Linux (notify-send / zenity)."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_PS1 = Path(__file__).resolve().parent / "Notifica_Desktop_Acqua.ps1"


def send_notification(title: str, message: str, dry_run: bool = False) -> bool:
    """Invia una notifica desktop nativa. Ritorna True se il comando è stato avviato con successo."""
    if dry_run:
        print(f"[NOTIFICA] {title}: {message}")
        return True

    if sys.platform == "win32":
        if not SCRIPT_PS1.exists():
            return False
        try:
            subprocess.Popen(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(SCRIPT_PS1),
                    "-Title",
                    title,
                    "-Message",
                    message,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            return True
        except OSError:
            return False

    # Linux / FreeDesktop (libnotify)
    notify_send = shutil.which("notify-send")
    if notify_send:
        try:
            subprocess.run(
                [notify_send, "--app-name=Promemoria Acqua", "-i", "dialog-information", title, message],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=5,
            )
            return True
        except Exception:
            return False

    # Fallback grafico minimale se notify-send non è presente
    zenity = shutil.which("zenity")
    if zenity:
        try:
            subprocess.Popen(
                [zenity, "--notification", f"--text={title}: {message}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except OSError:
            return False

    # Ultimo fallback su terminale
    print(f"[NOTIFICA] {title}: {message}")
    return True
