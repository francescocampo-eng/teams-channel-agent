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
3. se ci sono novità, invoca `copilot -p "..." --allow-all-tools --silent` passando il diff, con istruzioni di aggiornare **solo** il progetto DocMind `PreSales` (overview + documenti di dettaglio delle opportunità interessate, o crearne uno nuovo se è comparsa una nuova opportunità). Analisi e stesura documentazione usano le skill `impact`, `engenius` e `proposal-writing`; l'aggiornamento del sito statico (`site/`) usa la skill `ui-ux-pro-max`.

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

## Identità dell'agente: Ciro

L'agente ha un'identità definita in `docs/ciro_persona.md`: consulente
analitico e puntuale, attento a scadenze e follow-up aperti, nessun
riempitivo. Entrambi gli script di automazione (`presales_autoupdate.sh` e
`presales_checkin.sh`) la referenziano nel prompt passato a Copilot CLI.

## Tracking milestone e check-in (`scripts/presales_checkin.sh`)

Lo stato di avanzamento di ogni opportunità è mantenuto in
`data/presales_milestones.json` — **unica fonte di verità** (vedi
`docs/ciro_persona.md`, sezione "Memoria canonica"): stato corrente,
deadline, a cosa si è in attesa, log immutabile dei passaggi di stato
(`storico`, con economics associate) e calendario impegni/scadenze
(`impegni`). Lo script `presales_autoupdate.sh` lo aggiorna ad ogni scan
con novità; `presales_checkin.sh` lo legge ogni giorno e segnala (via
digest in `logs/presales_checkin_weekly.md`, generato solo quando serve)
due casi:
- una deadline è imminente (≤ 2 giorni) o superata;
- è lunedì e un'iniziativa senza deadline è ferma da ≥ 7 giorni.

Nessun riepilogo periodico generico: il digest viene scritto solo se c'è
davvero qualcosa da segnalare. Log di ogni esecuzione:
`logs/presales_checkin.log`.

Schedulazione installata (ogni giorno alle 8:30):
```
30 8 * * * PATH=/usr/bin:/usr/local/bin:/bin /usr/bin/bash /home/fcampo/copilot-projects/teams-channel-agent/scripts/presales_checkin.sh
```

## Calendario e dashboard di stato sul sito

`site/generate_site.py` legge `data/presales_milestones.json` e produce:
- **`site/calendario.html`**: tutti gli impegni (meeting/scadenze/milestone)
  di tutte le opportunità, ordinati cronologicamente, con link diretto
  alla pagina di dettaglio.
- **Dashboard stato** in cima a ogni `site/opportunita/<slug>.html`: stato
  corrente, prossima scadenza, "in attesa di", e la timeline completa dei
  passaggi di stato con gli economics registrati (stime, FP sizing,
  valore commessa, ecc.).

Si rigenerano insieme alle pagine normali con
`python3 site/build_content.py && python3 site/generate_site.py`.

## Benchmark presales (idea per evoluzione futura)

Quando un'opportunità passa a stato `VINTA`/`PERSA` in
`data/presales_milestones.json`, l'informazione è già strutturata per
poter calcolare in futuro un tasso di conversione (opportunità vinte /
totale lavorate) semplicemente aggregando il file nel tempo (es. con uno
storico a parte o un export periodico).

## Principi di progetto

- DocMind è una capability già esistente: non va reinstallato né duplicato.
- Nessun nuovo MCP è richiesto in questa fase; valutazione esplicita solo a
  fine POC (Milestone 14).
- Principio di minima complessità: preferire CLI nativa, DocMind, file di
  progetto, script Python prima di introdurre nuovi componenti.

Vedi il documento di concept su DocMind per dettagli completi su
architettura, milestone e stato di avanzamento.
