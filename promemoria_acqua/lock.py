"""Lock a istanza singola multipiattaforma (Mutex Win32 su Windows, flock su Linux/macOS)."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

_LOCK_HANDLE = None


def acquire_single_instance(name: str = "PromemoriaAcqua") -> bool:
    """Ritorna True se questa è l'unica istanza attiva, False se ne gira già un'altra."""
    global _LOCK_HANDLE
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        _LOCK_HANDLE = kernel32.CreateMutexW(None, False, f"{name}_Mutex")
        return kernel32.GetLastError() != 183  # ERROR_ALREADY_EXISTS

    import fcntl
    lock_path = Path(tempfile.gettempdir()) / f"{name}.lock"
    fh = open(lock_path, "w", encoding="utf-8")
    try:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        fh.close()
        return False
    fh.write(str(os.getpid()))
    fh.flush()
    _LOCK_HANDLE = fh  # mantiene aperto il file finché il processo vive
    return True
