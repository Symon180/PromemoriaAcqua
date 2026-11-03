#!/usr/bin/env bash
# Registra Promemoria Acqua nell'avvio automatico utente su Linux (XDG autostart) e lo avvia subito in background.
set -e
CARTELLA="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOSTART_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/autostart"
mkdir -p "$AUTOSTART_DIR"

cat > "$AUTOSTART_DIR/promemoria-acqua.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Promemoria Acqua
Comment=Notifica periodica per ricordarti di bere acqua
Exec=/usr/bin/env python3 -m promemoria_acqua
Path=$CARTELLA
Terminal=false
X-GNOME-Autostart-enabled=true
EOF

nohup python3 -m promemoria_acqua >/dev/null 2>&1 &
echo "Installato in $AUTOSTART_DIR/promemoria-acqua.desktop e avviato in background!"
