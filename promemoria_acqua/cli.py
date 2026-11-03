"""Entry point a riga di comando e ciclo periodico di Promemoria Acqua."""
from __future__ import annotations

import argparse
import sys
import time

from .lock import acquire_single_instance
from .notifier import send_notification

DEFAULT_MINUTES = 30
DEFAULT_TITLE = "Promemoria Acqua"
DEFAULT_MESSAGE = "Vai a riempire la borraccia! 💧"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="promemoria_acqua",
        description="Invia una notifica desktop periodica per ricordarti di bere acqua (Linux & Windows).",
    )
    p.add_argument(
        "-m", "--minutes",
        type=float,
        default=DEFAULT_MINUTES,
        help=f"intervallo in minuti tra una notifica e l'altra (default: {DEFAULT_MINUTES})",
    )
    p.add_argument("--title", default=DEFAULT_TITLE, help="titolo della notifica")
    p.add_argument("--message", default=DEFAULT_MESSAGE, help="testo della notifica")
    p.add_argument("--once", action="store_true", help="invia una sola notifica di prova ed esce subito")
    p.add_argument("--dry-run", action="store_true", help="stampa la notifica a terminale invece di usare il sistema")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.minutes <= 0:
        print("Errore: l'intervallo in minuti deve essere maggiore di zero.", file=sys.stderr)
        return 2

    if not args.once and not acquire_single_instance():
        print("Promemoria Acqua è già in esecuzione in background.", file=sys.stderr)
        return 0

    send_notification(args.title, args.message, dry_run=args.dry_run)
    if args.once:
        return 0

    interval_seconds = args.minutes * 60.0
    try:
        while True:
            time.sleep(interval_seconds)
            send_notification(args.title, args.message, dry_run=args.dry_run)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
