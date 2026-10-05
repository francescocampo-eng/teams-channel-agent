# Teams Channel Agent

Agente locale (Ubuntu/WSL) per lettura/contesto Microsoft Teams, con
integrazione DocMind (documentazione indicizzata, MCP già configurato)
e accesso controllato ai file locali. Interazione principale tramite
GitHub Copilot CLI.

Documento di concept e stato avanzamento: DocMind, progetto **AgenteTeams**
→ "Teams Channel Agent - Esigenza, Architettura e Milestone".

## Setup locale

```bash
cd ~/copilot-projects/teams-channel-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # poi compilare MS_TENANT_ID / MS_CLIENT_ID (Milestone 2)
```

## Struttura

```
src/teams_channel_agent/
  config.py        # impostazioni da .env (nessun segreto hardcoded)
  main.py           # entry point opzionale (check-env, chat)
  graph/            # Microsoft Graph connector (auth, messages, replies)
  docmind/          # utilizzo del DocMind MCP già configurato
  local_files/       # accesso controllato alle cartelle locali
  artifacts/        # costruzione anteprime/artefatti
tests/
docs/
output/             # artefatti generati (ignorato da git, salvo .gitkeep)
```

## Check rapido ambiente

```bash
python -m teams_channel_agent.main check-env
```

## Automazione: aggiornamento autonomo dei documenti DocMind "PreSales"

Lo script `scripts/presales_autoupdate.sh`:
1. esegue `scan-opportunities --json` (diff su cartelle/file nuovi, modificati, rimossi, nuove opportunità);
2. se non ci sono novità esce subito (nessuna chiamata esterna, nessun upload);
3. se ci sono novità, invoca `copilot -p "..." --allow-all-tools --silent` passando il diff, con istruzioni di aggiornare **solo** il progetto DocMind `PreSales` (overview + documenti di dettaglio delle opportunità interessate, o crearne uno nuovo se è comparsa una nuova opportunità).

Log di ogni esecuzione: `logs/presales_autoupdate.log` (non versionato).

Schedulazione installata (cron utente, ogni ora dalle 9 alle 18):
```
0 9-18 * * * PATH=/usr/bin:/usr/local/bin:/bin /usr/bin/bash /home/fcampo/copilot-projects/teams-channel-agent/scripts/presales_autoupdate.sh
```
Modificabile con `crontab -e`.

**Limite importante**: il job gira solo mentre questa istanza WSL è avviata
(cron non sopravvive allo spegnimento di WSL/Windows). Se la macchina è
spenta durante l'orario previsto, quella esecuzione viene semplicemente
saltata: alla riaccensione lo scan successivo rileverà comunque tutte le
novità accumulate nel frattempo.

## Principi di progetto

- DocMind è una capability già esistente: non va reinstallato né duplicato.
- Nessun nuovo MCP è richiesto in questa fase; valutazione esplicita solo a
  fine POC (Milestone 14).
- Principio di minima complessità: preferire CLI nativa, DocMind, file di
  progetto, script Python prima di introdurre nuovi componenti.

Vedi il documento di concept su DocMind per dettagli completi su
architettura, milestone e stato di avanzamento.
