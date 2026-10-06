#!/usr/bin/env bash
# Check-in "Ciro" sulle opportunità presales.
#
# Eseguito ogni mattina via cron. Non chiama Copilot CLI tutti i giorni:
# usa un piccolo controllo Python su data/presales_milestones.json per
# capire se c'è davvero qualcosa da segnalare, e invoca l'AI (con
# l'identità Ciro, docs/ciro_persona.md) SOLO in questi casi:
#   - una deadline è imminente (entro 2 giorni) o già superata;
#   - è lunedì: riepilogo delle iniziative SENZA deadline ferme da più di
#     7 giorni (ultimo_aggiornamento), per chiedere un aggiornamento.
# L'output va in logs/presales_checkin.log e, quando c'è qualcosa da dire,
# anche in logs/presales_checkin_weekly.md (ultimo digest leggibile).
#
# Schedulazione consigliata: una volta al giorno, es. alle 8:30.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/presales_checkin.log"
DIGEST_FILE="$LOG_DIR/presales_checkin_weekly.md"
MILESTONES_FILE="$PROJECT_DIR/data/presales_milestones.json"
mkdir -p "$LOG_DIR"

cd "$PROJECT_DIR"
TS="$(date '+%Y-%m-%d %H:%M:%S')"

NEEDS_ATTENTION="$(python3 - "$MILESTONES_FILE" <<'PYEOF'
import json, sys, datetime

path = sys.argv[1]
today = datetime.date.today()
is_monday = today.weekday() == 0

with open(path) as f:
    data = json.load(f)

flags = []
for slug, opp in data.items():
    deadline = opp.get("deadline")
    if deadline:
        d = datetime.date.fromisoformat(deadline)
        delta = (d - today).days
        if delta <= 2:
            stato = "SCADUTA" if delta < 0 else ("OGGI/DOMANI" if delta <= 1 else "entro 2 giorni")
            flags.append(f"- [{slug}] {opp.get('nome')}: deadline {deadline} ({stato}) — {opp.get('deadline_descrizione') or ''}")
    elif is_monday and opp.get("stato") not in ("VINTA", "PERSA", "STAND_BY"):
        ultimo = opp.get("ultimo_aggiornamento")
        ferma_da = None
        if ultimo:
            ferma_da = (today - datetime.date.fromisoformat(ultimo)).days
        if ferma_da is None or ferma_da >= 7:
            attesa = f" (in attesa di: {opp['in_attesa_di']})" if opp.get("in_attesa_di") else ""
            flags.append(f"- [{slug}] {opp.get('nome')}: nessuna deadline, ferma da {ferma_da if ferma_da is not None else 'N/D'} giorni{attesa}")

    # follow-up automatico su impegni passati (es. meeting avvenuto ieri):
    # chiedi l'esito/feedback se non risulta un aggiornamento di stato dopo l'impegno.
    ultimo = opp.get("ultimo_aggiornamento")
    ultimo_d = datetime.date.fromisoformat(ultimo) if ultimo else None
    for imp in opp.get("impegni", []):
        imp_d = datetime.date.fromisoformat(imp["data"])
        if imp_d < today and (ultimo_d is None or ultimo_d <= imp_d):
            flags.append(f"- [{slug}] {opp.get('nome')}: follow-up dovuto su '{imp['titolo']}' ({imp['data']}, {imp.get('tipo')}) — nessun esito/feedback ancora registrato, chiedi all'utente com'è andata.")

if flags:
    print("SI")
    for line in flags:
        print(line)
else:
    print("NO")
PYEOF
)"

FIRST_LINE="$(echo "$NEEDS_ATTENTION" | head -1)"

if [ "$FIRST_LINE" != "SI" ]; then
    echo "[$TS] Nessuna segnalazione (nessuna deadline imminente, nessun riepilogo lunedì dovuto)." >> "$LOG_FILE"
    exit 0
fi

FLAGS="$(echo "$NEEDS_ATTENTION" | tail -n +2)"
echo "[$TS] Segnalazioni rilevate:" >> "$LOG_FILE"
echo "$FLAGS" >> "$LOG_FILE"

source .venv/bin/activate 2>/dev/null || true

PROMPT="Agisci con l'identità descritta in docs/ciro_persona.md (agente 'Ciro': consulente analitico e puntuale, attento a scadenze e follow-up aperti).

Queste sono le segnalazioni rilevate oggi su data/presales_milestones.json:
$FLAGS

Istruzioni:
- Scrivi un digest breve (poche righe per voce, niente riempitivi) in italiano, in stile Ciro: per ogni voce spiega perché richiede attenzione ORA (scadenza vicina/superata, oppure iniziativa ferma senza deadline) e cosa serve per sbloccarla.
- Sovrascrivi interamente il file logs/presales_checkin_weekly.md con questo digest (titolo con la data di oggi).
- Non toccare DocMind, non toccare il sito, non modificare data/presales_milestones.json in questa fase: è solo un digest da far leggere all'utente alla prossima apertura di sessione."

if copilot -p "$PROMPT" --allow-all-tools --silent >> "$LOG_FILE" 2>&1; then
    echo "[$TS] Digest aggiornato in $DIGEST_FILE." >> "$LOG_FILE"
else
    echo "[$TS] ERRORE durante la generazione del digest (vedi log sopra)." >> "$LOG_FILE"
fi
