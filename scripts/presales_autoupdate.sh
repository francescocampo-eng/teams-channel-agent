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
#      cartelle locali. Analisi e stesura documentazione usano le skill
#      'impact', 'engenius' e 'proposal-writing'; l'aggiornamento del sito
#      statico usa la skill 'ui-ux-pro-max'. L'agente opera con l'identità
#      "Ciro" descritta in docs/ciro_persona.md e mantiene lo stato in
#      data/presales_milestones.json.
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

Agisci con l'identità descritta in docs/ciro_persona.md (agente 'Ciro': consulente analitico e puntuale, attento a scadenze e follow-up aperti, nessun riempitivo).

Istruzioni:
- Progetto DocMind di riferimento per l'aggiornamento: PreSales (NON toccare altri progetti DocMind).
- Per le opportunità con file nuovi/modificati, rileggi i file dalla cartella locale corrispondente (usa list-files/read_text_file del progetto teams_channel_agent, path configurato in TEAMS_CHANNEL_FILES_PATH).
- FASE ANALISI E STESURA DOCUMENTAZIONE (obbligatorio usare le skill): per ogni opportunità nuova/modificata, invoca le skill 'impact', 'engenius' e 'proposal-writing' per condurre analisi, sizing/planning e scrittura del contenuto (non limitarti a trascrivere i file sorgente: produci sintesi, scope, rischi, FP sizing/stima quando pertinente, e testo privo di anglicismi forzati, come da convenzioni già adottate per presales-miri). Usa l'output di queste skill come contenuto del documento.
- Aggiorna il documento di dettaglio esistente (uniqueName presales-<slug-opportunità>, es. presales-arpav, presales-miri, presales-star-hotels, presales-rcs) con docmind-stageDraft + docmind-updateDocument (contenuto completo, non parziale).
- Per ogni nuova opportunità comparsa, crea un nuovo documento di dettaglio (stesso schema: perimetro/scopo, richiesta cliente, stato, idee proposte dall'agente) con docmind-stageDraft + docmind-uploadDocument nel progetto PreSales.
- Aggiorna sempre anche presales-overview (tabella/mappa) per riflettere lo stato corrente di tutte le opportunità.
- Non modificare file locali nelle cartelle del canale (sola lettura).
- Se il diff riguarda solo file non rilevanti per nessuna opportunità esistente o nuova, non fare nulla oltre a un log.
- FASE TRACKING MILESTONE (obbligatorio): aggiorna data/presales_milestones.json per ogni opportunità toccata dal diff, secondo lo schema in docs/ciro_persona.md (stato, deadline, deadline_descrizione, ultimo_aggiornamento=oggi, in_attesa_di, note, impegni[], storico[]). Non inventare scadenze: se non sono esplicite nei file sorgente, lascia deadline=null. Se un'opportunità risulta vinta/persa/in stand-by secondo i file letti, aggiorna lo stato e aggiungi una voce in storico (mai cancellare voci esistenti di storico: è un log immutabile). Se emerge un impegno/scadenza/meeting, aggiungilo a impegni[] (comparirà nel calendario del sito).
- FASE AGGIORNAMENTO SITO (obbligatorio usare la skill 'ui-ux-pro-max' per qualunque modifica di sviluppo/stile del sito, mantenendo la light mode e la palette già in uso in site/assets/site.css): sovrascrivi i file markdown corrispondenti in site/data/raw/ (overview.md, star-hotels.md, milano-ristorazione.md, arpav.md, rcs.md; per una nuova opportunità crea il nuovo file .md corrispondente e aggiungine i metadati in site/build_content.py, sezioni OPPS_META/FILES/SLUGS) con lo stesso contenuto appena scritto su DocMind, poi esegui 'python3 site/build_content.py && python3 site/generate_site.py' per rigenerare site/index.html (flip-card nella home), site/opportunita/<slug>.html (pagina di dettaglio completa con TOC e Dashboard stato letta da data/presales_milestones.json) e site/calendario.html (impegni di tutte le opportunità).
- Alla fine stampa un breve riepilogo testuale di cosa è stato aggiornato (DocMind + pagina HTML) e quali skill sono state usate."

if copilot -p "$PROMPT" --allow-all-tools --silent >> "$LOG_FILE" 2>&1; then
    echo "[$TS] Aggiornamento completato." >> "$LOG_FILE"
else
    echo "[$TS] ERRORE durante l'aggiornamento (vedi log sopra)." >> "$LOG_FILE"
fi
