# 💧 Promemoria Acqua (HydraPing)

[![CI](https://github.com/Symon180/PromemoriaAcqua/actions/workflows/ci.yml/badge.svg)](https://github.com/Symon180/PromemoriaAcqua/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dipendenze%20runtime-0-brightgreen)
![Platform](https://img.shields.io/badge/Linux%20%7C%20Windows-tested%20in%20CI-lightgrey)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

Notifica **multipiattaforma (Linux & Windows)** in Python puro (zero dipendenze esterne) che invia una notifica di sistema periodica per ricordarti di bere acqua durante il lavoro al PC.

*English: Zero-dependency cross-platform desktop reminder daemon (Linux `notify-send` & Windows 10/11 WinRT Toast Notifications via PowerShell) with single-instance OS mutex/flock protection and one-click autostart installers.*

---

## ✨ Caratteristiche Tecniche

- **🔔 Notifiche Native del Sistema Operativo:**
  - **Windows 10/11:** Toast Notification WinRT nativa (`Windows.UI.Notifications`) generata via PowerShell con pulsante di conferma *"Ho bevuto"* e registrazione automatica dell'`AppUserModelID` nel registro utente (`HKCU`), senza finestre di console grazie a `CREATE_NO_WINDOW`.
  - **Linux:** Notifiche desktop standard FreeDesktop tramite `notify-send` (`libnotify`) o fallback `zenity`.
- **🔒 Protezione Istanza Singola (Single-Instance Lock):**
  - Su **Windows** utilizza un Mutex del kernel Win32 (`CreateMutexW` via `ctypes`).
  - Su **Linux** utilizza un lock esclusivo non bloccante sul file system (`fcntl.flock`).
  - Impedisce avvii multipli accidentali e notifiche duplicate.
- **🚀 Installazione Autostart in 1 Clic (senza privilegi di amministratore):**
  - `INSTALLA.bat` (ibrido Batch + PowerShell per Windows): verifica/installa Python in user-scope, copia i file e registra il task nello **Scheduler di Windows** (`Register-ScheduledTask` all'accesso utente senza scadenza di 72 ore).
  - `installa_linux.sh` (Linux): crea la voce standard XDG Autostart in `~/.config/autostart/` e avvia subito il demone in background.

---

## 🚀 Uso Rapido

### Provare subito una notifica
```bash
git clone https://github.com/Symon180/PromemoriaAcqua.git
cd PromemoriaAcqua

# Invia una singola notifica di prova ed esce:
./avvia.sh --once          # Linux
python -m promemoria_acqua --once   # Windows / Multipiattaforma
```

### Avviare il ciclo periodico (default: ogni 30 minuti)
```bash
./avvia.sh                 # Linux (oppure ./avvia.sh -m 20 per ogni 20 minuti)
avvia.bat                  # Windows (in background senza console)
```

### Installare l'avvio automatico all'accensione del PC
- **Su Linux:** `./installa_linux.sh`
- **Su Windows:** doppio clic su `INSTALLA.bat`

---

## ⚙️ Opzioni da Riga di Comando

| Opzione | Descrizione |
|---|---|
| `-m, --minutes N` | Intervallo in minuti tra una notifica e l'altra (default: `30`) |
| `--title TESTO` | Personalizza il titolo della notifica |
| `--message TESTO` | Personalizza il messaggio della notifica |
| `--once` | Invia una sola notifica immediata e termina |
| `--dry-run` | Stampa la notifica nel terminale senza invocare il sistema operativo |

---

## 🧪 Test

```bash
pytest
```

## 📄 Licenza
Rilasciato sotto licenza [MIT](LICENSE) — Autore: [Simone Mariotti](https://github.com/Symon180).
