#!/usr/bin/env bash
# Automazione Milestone "Presales autoupdate".
#
# Eseguito periodicamente via cron (vedi README.md "Automazione"). Passi:
#   1. Esegue lo scan delle cartelle opportunità (OneDrive sync) in modalità
#      --json per ottenere un diff machine-readable.
#   2. Se non ci sono novità, esce senza fare nulla (nessuna chiamata a
#      Copilot CLI, nessun upload DocMind).
#   3. Se ci sono novità, invoca GitHub Copilot CLI in modalità non
#      interattiva (-p / --allow-all-tools) passando il diff, con istruzioni
#      di aggiornare SOLO il progetto DocMind "PreSales": il documento
#      presales-overview e i documenti di dettaglio delle opportunità
#      interessate dal diff, rileggendo i file aggiornati dalle rispettive
#      cartelle locali.
#
# Logga ogni esecuzione in logs/presales_autoupdate.log (creata se assente).

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/presales_autoupdate.log"
mkdir -p "$LOG_DIR"

cd "$PROJECT_DIR"
source .venv/bin/activate

TS="$(date '+%Y-%m-%d %H:%M:%S')"
DIFF_JSON="$(python -m teams_channel_agent.main scan-opportunities --json)"
HAS_CHANGES="$(python -c "import json,sys; print(json.loads(sys.argv[1])['has_changes'])" "$DIFF_JSON")"

if [ "$HAS_CHANGES" != "True" ]; then
    echo "[$TS] Nessuna novità, skip." >> "$LOG_FILE"
    exit 0
fi

echo "[$TS] Novità rilevate, avvio aggiornamento DocMind PreSales. Diff: $DIFF_JSON" >> "$LOG_FILE"

PROMPT="Scan automatico (cron) del canale Teams presales. Diff rilevato (JSON): $DIFF_JSON

Istruzioni:
- Progetto DocMind di riferimento per l'aggiornamento: PreSales (NON toccare altri progetti DocMind).
- Per le opportunità con file nuovi/modificati, rileggi i file dalla cartella locale corrispondente (usa list-files/read_text_file del progetto teams_channel_agent, path configurato in TEAMS_CHANNEL_FILES_PATH) e aggiorna il relativo documento di dettaglio esistente (uniqueName presales-<slug-opportunità>, es. presales-arpav, presales-miri, presales-star-hotels, presales-rcs) con docmind-stageDraft + docmind-updateDocument (contenuto completo, non parziale).
- Per ogni nuova opportunità comparsa, crea un nuovo documento di dettaglio (stesso schema: perimetro/scopo, richiesta cliente, stato, idee proposte dall'agente) con docmind-stageDraft + docmind-uploadDocument nel progetto PreSales.
- Aggiorna sempre anche presales-overview (tabella/mappa) per riflettere lo stato corrente di tutte le opportunità.
- Non modificare file locali nelle cartelle del canale (sola lettura).
- Se il diff riguarda solo file non rilevanti per nessuna opportunità esistente o nuova, non fare nulla oltre a un log.
- Dopo aver aggiornato DocMind, allinea anche la pagina HTML di presentazione: sovrascrivi i file markdown corrispondenti in site/data/raw/ (overview.md, star-hotels.md, milano-ristorazione.md, arpav.md, rcs.md; per una nuova opportunità crea il nuovo file .md corrispondente e aggiungine i metadati in site/build_content.py, sezioni OPPS_META/FILES/SLUGS) con lo stesso contenuto appena scritto su DocMind, poi esegui 'python3 site/build_content.py && python3 site/generate_site.py' per rigenerare site/index.html (flip-card nella home) e site/opportunita/<slug>.html (pagina di dettaglio completa, con TOC auto-generata dalle sezioni "## ..."/"### ..." del documento).
- Alla fine stampa un breve riepilogo testuale di cosa è stato aggiornato (DocMind + pagina HTML)."

if copilot -p "$PROMPT" --allow-all-tools --silent >> "$LOG_FILE" 2>&1; then
    echo "[$TS] Aggiornamento completato." >> "$LOG_FILE"
else
    echo "[$TS] ERRORE durante l'aggiornamento (vedi log sopra)." >> "$LOG_FILE"
fi
