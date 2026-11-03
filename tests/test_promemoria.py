from pathlib import Path
from promemoria_acqua.cli import main
from promemoria_acqua.lock import acquire_single_instance
from promemoria_acqua.notifier import SCRIPT_PS1, send_notification


def test_notifica_dry_run(capsys):
    assert send_notification("Titolo", "Messaggio", dry_run=True) is True
    assert "[NOTIFICA] Titolo: Messaggio" in capsys.readouterr().out


def test_cli_once_dry_run(capsys):
    code = main(["--once", "--dry-run", "--title", "Acqua", "--message", "Bevi!"])
    assert code == 0
    assert "[NOTIFICA] Acqua: Bevi!" in capsys.readouterr().out


def test_cli_intervallo_non_valido(capsys):
    assert main(["-m", "0", "--once"]) == 2
    assert main(["-m", "-5", "--once"]) == 2
    assert "maggiore di zero" in capsys.readouterr().err


def test_lock_istanza_singola():
    assert acquire_single_instance("PromemoriaAcqua_TestUnit") is True


def test_script_powershell_esiste_ed_e_anonimizzato():
    assert SCRIPT_PS1.exists()
    content = SCRIPT_PS1.read_text(encoding="utf-8")
    assert "Symon.PromemoriaAcqua" in content
    assert "FreeEnergia" not in content
