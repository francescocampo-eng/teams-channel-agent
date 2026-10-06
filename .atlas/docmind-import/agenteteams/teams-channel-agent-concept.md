---
unique-name: teams-channel-agent-concept
display-name: Teams Channel Agent - Esigenza, Architettura e Milestone
category: CONCEPT_DRAFT
description: Sostituita la nota INLAY/Atlas non verificata con info confermate dalla documentazione ufficiale: Atlas (porta 8010/mcp, 22 tool) non ancora installato in questo ambiente; chiarito perché la migrazione .docmind→.atlas non si applica ai progetti DocMind di questo agente.
---

# Teams Channel Agent — Esigenza, Architettura e Milestone

> Documento di avvio progetto. Stato: DRAFT. Progetto DocMind di riferimento: **AgenteTeams**.
> Working directory di sviluppo: `~/copilot-projects/teams-channel-agent`

## 1. Esigenza

Realizzare un agente interattivo, eseguito localmente su Ubuntu/WSL, in grado di:
- comunicare con l'utente in linguaggio naturale tramite GitHub Copilot CLI;
- leggere messaggi/reply e file da Microsoft Teams;
- utilizzare DocMind (MCP già configurato) come fonte di contesto documentale indicizzato;
- leggere file locali di progetto quando esplicitamente richiesto;
- integrare le fonti (Teams, DocMind, file locali, istruzioni utente) in un contesto unificato;
- produrre anteprime di artefatti, sottoposte a revisione utente prima della scrittura su disco.

Vincolo di fase: **nessuna distribuzione remota** (no server, no Azure Functions, no container, no VM, no cloud). Il browser Windows è usato solo per il login Microsoft (device code); l'esecuzione resta in WSL.

## 2. Principi guida

### 2.1 DocMind come capability esistente
DocMind è già installato, configurato e rilevato dalla Copilot CLI. Non va reinstallato, duplicato o sostituito. Nessun nuovo indice vettoriale, nessun nuovo DB documentale, nessuna duplicazione locale dei documenti già gestiti da DocMind, nessuna modifica alla configurazione MCP esistente.

### 2.2 Doppia modalità documentale
- **Modalità A — DocMind**: documentazione consolidata, ricerche semantiche, dominio di progetto.
- **Modalità B — File locali**: sorgenti, configurazioni, file appena creati, artefatti di lavoro, directory locali autorizzate — incluso l'accesso ai file del canale Teams tramite sincronizzazione OneDrive (vedi §6).

L'agente deve sempre dichiarare la provenienza di un'informazione: Microsoft Teams, DocMind, file locale, istruzione utente, o contenuto generato.

### 2.3 Principio di minima complessità
Ordine di preferenza: 1) funzionalità native Copilot CLI; 2) DocMind già configurato; 3) file e istruzioni di progetto; 4) script Python locale; 5) comando CLI strutturato; 6) skill locale; 7) nuovo MCP server, solo se necessario.

### 2.4 MCP non obbligatorio
Nessun nuovo MCP è un requisito iniziale. Valutazione esplicita solo a fine POC (Milestone 14): `MCP_NON_NECESSARIO` / `MCP_UTILE_MA_OPZIONALE` / `MCP_NECESSARIO`.

## 3. Architettura iniziale (aggiornata dopo il blocco Conditional Access)

```
Utente
  → GitHub Copilot CLI (Ubuntu/WSL)
    → agente interattivo
      → Microsoft Graph Connector (Python, device code, client pubblico)
          → Microsoft Graph /me  [OK — scope User.Read]
          → Messaggi/reply canale Teams  [BLOCCATO da Conditional Access, vedi §5]
      → File canale Teams via OneDrive sync (Windows) → letti da WSL (/mnt/c/...)
          → organizzati per opportunità/commessa (una sottocartella ciascuna)
          → scanner di differenze (nuove opportunità, file nuovi/modificati/rimossi)
      → DocMind MCP (già configurato) → documentazione indicizzata
          → progetto "AgenteTeams": documentazione del progetto agente stesso
          → progetto "PreSales": panoramica + dettaglio per singola opportunità, generati dall'agente
      → working directory / cartelle locali autorizzate → file locali di progetto
      → Skill locali (Copilot CLI) → impact, engenius, ui-ux-pro-max, proposal-writing
          → usate per arricchire i documenti di dettaglio opportunità con idee/proposte
      → Artifact Builder → anteprima → revisione utente → directory di output
```

Nessun livello MCP aggiuntivo tra agente e Graph Connector in questa fase.

## 4. Milestone

0. Verifica ambiente Ubuntu/WSL — **completata**
0b. Verifica GitHub Copilot CLI — **completata**
0c. Verifica DocMind esistente — **completata**
1. Scaffolding progetto Python — **completata**
2. Checklist Microsoft Entra ID (app registration) — **bloccata**: policy tenant "Users can register applications = No". Pivot deciso: uso client pubblico multi-tenant Microsoft ("Microsoft Graph Command Line Tools", client_id `14d82eec-204b-4c2f-b7e8-296a70dab67e`), nessuna registrazione app necessaria.
3. Autenticazione Microsoft tramite device code flow — **parzialmente completata**: login OK con scope `User.Read`; tentativo con scope Teams bloccato da **Conditional Access** del tenant ("L'accesso è stato completato ma non rispetta i criteri per l'accesso a questa risorsa"). Non risolvibile cambiando client ID: è un blocco a livello di policy tenant (device/località/app non gestita).
4. Prima chiamata Microsoft Graph (`/me`) — comando `whoami` implementato, da validare con token ottenuto in Milestone 3.
5-7. Configurazione team/canale, lettura messaggi/reply Teams via Graph — **in pausa**, in attesa di decisione su come gestire il blocco Conditional Access (vedi §5).
8. Lettura sicura delle cartelle locali — **completata**: pivot architetturale, vedi §6.
8b. Rilevamento differenze (nuove opportunità, file nuovi/modificati/rimossi) — **completata**, vedi §7.
9. Utilizzo coordinato di DocMind — **completata (prima iterazione)**: creati/aggiornati documenti su progetto "PreSales" (panoramica + 4 dettagli opportunità), vedi §8.
10. Costruzione del contesto unificato (Teams/OneDrive + DocMind + skill) — **avviata**: applicata nella generazione dei documenti di dettaglio opportunità (idee proposte con supporto skill `impact`, `engenius`, `ui-ux-pro-max`, `proposal-writing`).
11. Produzione anteprima di un artefatto — **prima istanza completata**: i documenti Presales sono stati generati e caricati (non ancora un ciclo formale di anteprima/correzione utente prima dell'upload).
12. Interazione tramite Copilot CLI — in uso corrente, nessuna chat custom creata finora.
13. Test end-to-end — da avviare.
14. Valutazione necessità nuovo MCP — da avviare a fine POC.

## 5. Blocco Conditional Access — decisione presa

Tentata autenticazione device code con client pubblico Microsoft e scope Graph per Teams: risposta "L'accesso è stato completato ma non rispetta i criteri per l'accesso a questa risorsa" (Conditional Access del tenant aziendale: blocco per app/dispositivo/località non gestiti).

Opzioni valutate con l'utente: (A) client pubblico Microsoft — provato, bloccato da CA, non dal permesso di registrazione; (B) Microsoft 365 Developer Tenant separato; (C) pausa su Teams via Graph, focus su altri moduli.

**Decisione presa**: pivotare sull'accesso ai **file** del canale Teams tramite sincronizzazione OneDrive (Windows) + lettura da WSL, bypassando interamente Graph per questo caso d'uso (vedi §6). La lettura di **messaggi/reply di chat** via Graph resta bloccata e sospesa: da riconsiderare con Opzione B o coinvolgimento IT se/quando necessario.

## 6. Accesso file canale Teams via OneDrive sync (pivot architetturale)

Il canale Teams ha una tab "File" supportata da una libreria SharePoint; agganciandola a OneDrive (Windows: Teams → canale → File → "Aggiungi collegamento a OneDrive" / Sincronizza), diventa una cartella locale Windows raggiungibile da WSL via `/mnt/c/...`.

Percorso verificato e funzionante:
```
/mnt/c/Users/fcampo/OneDrive - Engineering Ingegneria Informatica S.p.A/Delivery Factory A - PreSales and Opptys - PreSales
```

Struttura: ogni sottocartella di primo livello = una **opportunità/commessa** (es. "ARPAV - Integrazione Google Calendar", "MILANO RISTORAZIONE", "RCS - Rizzoli Corriere Della Sera", "STAR HOTELS").

Implementazione (`src/teams_channel_agent/local_files/browser.py`):
- `list_opportunities()` — elenca le sottocartelle/opportunità;
- `list_files(opportunity_name, pattern)` — elenca i file di una opportunità;
- `read_text_file(path)` — legge un file di testo con limite dimensionale;
- tutte le funzioni validano il percorso contro `allowed_roots` (protezione path traversal).

Config (`config.py`): `TEAMS_CHANNEL_FILES_PATH` (override via env `TEAMS_CHANNEL_FILES_PATH`), aggiunta a `LocalFilesSettings.allowed_roots` insieme a `PROJECT_ROOT`.

CLI: comandi `list-opportunities` e `list-files <nome opportunità>`, testati con successo (4 opportunità rilevate: ARPAV, MILANO RISTORAZIONE, RCS, STAR HOTELS).

Provenienza dichiarata nell'output CLI: "fonte: file locale / OneDrive sync" — coerente con il principio di dichiarare sempre la fonte dell'informazione (§2.2).

## 7. Rilevamento differenze (diff scanner)

Implementazione (`src/teams_channel_agent/local_files/diff.py`): snapshot delle opportunità e dei file (percorso relativo, dimensione, data modifica) persistito in `output/opportunities_snapshot.json` (locale, non versionato). Ad ogni esecuzione del comando CLI `scan-opportunities` viene confrontato lo stato attuale con l'ultimo snapshot e segnalato:
- opportunità nuove / rimosse;
- file nuovi / modificati / rimossi per ciascuna opportunità.

Primo scan (baseline): 4 opportunità, 8 file totali, tutti segnalati come "nuovi" (nessuno snapshot precedente). Scan successivo: "Nessuna novità" (comportamento corretto). Meccanismo pensato per alimentare in futuro l'aggiornamento automatico dei documenti Presales su DocMind quando compare nuovo materiale (es. la cartella RCS, oggi vuota).

## 8. Progetto DocMind "PreSales" — prima generazione documenti

Su richiesta esplicita, l'agente ha generato e caricato su DocMind (progetto **PreSales**, già esistente con 0 documenti) i seguenti documenti, con contenuto interamente derivato dai file locali delle opportunità (sezione "fonte" sempre dichiarata) più una sezione esplicita "Idee proposte dall'agente" per ciascun dettaglio (contenuto generato, non proveniente dal cliente):

| Documento (uniqueName) | Contenuto |
|---|---|
| `presales-overview` | Panoramica/mappa di tutti i filoni: tabella riepilogativa (opportunità, macro-ambito, cliente, stato, file disponibili, doc di dettaglio), sintesi per filone, prossimi passi proposti |
| `presales-arpav` | ARPAV - Integrazione Google Calendar: perimetro (Prisma→Google unidirezionale), richiesta cliente, stato (analisi, attività P0 aperte, raccomandazione di non andare in produzione), idee proposte (FP sizing, ADR Prisma/SINAP, contratto d'integrazione versionato, criteri di uscita pilot) |
| `presales-miri` | MILANO RISTORAZIONE: perimetro MVP ticketing + CRM Dynamics, richiesta cliente (collaborazione con Adesso.it), stato (WBS 13 work package, stima ROM 506-911 gg-persona, governance tripartita), idee proposte (sizing FP/SNAP, vertical slice identity-to-CRM come sprint 0, RACI anticipata) |
| `presales-star-hotels` | STAR HOTELS: perimetro (PoC flow INLAY + assessment enterprise), richiesta cliente, stato (fase iniziale, perimetro da definire dal cliente, deadline fine 2026), idee proposte con supporto esplicito delle skill `ui-ux-pro-max` (mockup INLAY) e `proposal-writing` (profilo hospitality) |
| `presales-rcs` | RCS - Rizzoli Corriere Della Sera: placeholder, cartella canale vuota, nessun contenuto disponibile, da aggiornare al primo scan utile |

Skill locali installate/adattate per supportare la generazione di queste idee proposte (vedi anche §10):
- `ui-ux-pro-max` (adattata da `nextlevelbuilder/ui-ux-pro-max-skill`, MIT) — prototipazione UI/UX rapida, usata per STAR HOTELS;
- `proposal-writing` (adattata da `peterbamuhigire/proposal-skills`, MIT) — struttura proposte commerciali, inclusi profili settoriali (es. hospitality), usata per STAR HOTELS;
- `impact` (già disponibile) — rigore di assessment tecnico, richiamata nelle idee proposte per ARPAV e STAR HOTELS;
- `engenius` (già disponibile) — planner ANALYSIS/FP_SIZING/WBS, richiamati nelle idee proposte per ARPAV e MILANO RISTORAZIONE.

## 9. Stato di avanzamento

| Data | Attività | Esito |
|---|---|---|
| 2026-10-05 | Collegamento progetto locale a DocMind "AgenteTeams" | Fatto |
| 2026-10-05 | Raccolta requisiti e vincoli architetturali | Fatto |
| 2026-10-05 | Diagnostica Milestone 0 | Fatto |
| 2026-10-05 | Milestone 1 — Scaffolding progetto Python | Fatto |
| 2026-10-05 | Milestone 2 — Checklist Entra ID | Bloccata (policy tenant), pivot su client pubblico |
| 2026-10-05 | Milestone 3 — Device code auth | Parziale: OK scope User.Read, bloccato scope Teams (Conditional Access) |
| 2026-10-05 | Pivot — Accesso file canale Teams via OneDrive sync | Fatto, testato con successo |
| 2026-10-05 | Milestone 8 — Lettura sicura cartelle locali (incl. file Teams) | Fatto |
| 2026-10-05 | Diff scanner (nuove opportunità, file nuovi/modificati/rimossi) | Fatto |
| 2026-10-05 | Import/adattamento skill `ui-ux-pro-max` e `proposal-writing` | Fatto |
| 2026-10-05 | Generazione documenti DocMind progetto "PreSales" (1 overview + 4 dettaglio) | Fatto |

## 10. Dettaglio Milestone 1 — Scaffolding progetto Python

Percorso: `~/copilot-projects/teams-channel-agent`. Struttura: `src/teams_channel_agent/{config.py, main.py, graph/, docmind/, local_files/, artifacts/}`, `tests/`, `docs/`, `output/`, `pyproject.toml` (layout src/, editable install), `requirements.txt`, `.env.example`, `.gitignore`, `README.md`. Gestione dipendenze: venv + pip. Blocco riscontrato e risolto: pacchetto di sistema `python3.12-venv` mancante (ambiente "externally-managed"), richiesta sudo eseguita dall'utente. Repo git locale inizializzato (commit: scaffolding, auth+local files, diff scanner).
## 11. Contesto: INLAY e migrazione DocMind → Atlas (verificato)

> Fonte: repository `DevExpPlatform/project-am-inlay-docs-portal` (documentazione ufficiale INLAY Studio), letto direttamente dal repo scaricato in locale dall'utente (`~/project-am-inlay-docs-portal`) dopo che l'accesso diretto alla Pages GitHub e il tool MCP GitHub `get_file_contents` sono risultati non utilizzabili (pagina privata dietro login; poi bug del tool indipendente dal login, non risolto). Aggiorna e sostituisce la nota precedente basata solo su quanto riferito a voce.

**INLAY Studio** è la suite applicativa locale dell'azienda, eseguita tramite container **podman**. Include **Atlas**, il motore di knowledge base che **sostituisce DocMind**: espone un MCP server HTTP (porta default **8010**, endpoint `http://localhost:8010/mcp`, nessuna autenticazione richiesta, 22 tool). La configurazione di Atlas su GitHub Copilot CLI è **separata** da quella usata da Inlay Studio stesso e va fatta a mano una tantum:
- automatica: `gh api repos/DevExpPlatform/project-am-inlay-docs-portal/contents/static/scripts/configure-inlay-atlas-mcp.sh -H "Accept: application/vnd.github.raw" | bash`
- manuale: `copilot mcp add --transport http atlas http://localhost:8010/mcp`

**Stato verificato in questo ambiente**: Inlay Studio/Atlas **non è installato** (`podman` assente, porta 8010 non raggiungibile). Nessuna azione di installazione è stata effettuata: resta una possibile attività futura, da avviare solo su istruzione esplicita dell'utente.

**Migrazione progetti DocMind → Atlas**: si applica a progetti la cui documentazione-as-code vive in un **repository git** con cartella `.docmind/` (rinominata poi in `.atlas/`, push, import del repo in Inlay Studio). I progetti DocMind di questo agente (`AgenteTeams`, `PreSales`) vivono invece nel database di DocMind, gestiti solo via MCP (`stageDraft`/`uploadDocument`/`updateDocument`) — **non** sono organizzati come cartella `.docmind/` in un repo git, quindi questa procedura di migrazione non si applica direttamente a loro. Un'eventuale migrazione richiederebbe un passaggio ad-hoc (es. esportare i documenti e reimportarli come fonti in Inlay Studio), non ancora valutato né richiesto.

**Collegamento con l'opportunità STAR HOTELS**: dettaglio completo e implicazioni nel documento DocMind `presales-star-hotels` (progetto PreSales) — il PoC "flow INLAY" richiesto dal cliente presuppone come prerequisito tecnico l'installazione dello stack Inlay Studio, oggi assente.

## 12. Automazione: aggiornamento autonomo documenti DocMind "PreSales"

A valle della prima generazione manuale dei documenti (§8), è stata implementata l'automazione richiesta dall'utente.

**Meccanismo** (`scripts/presales_autoupdate.sh`):
1. esegue `python -m teams_channel_agent.main scan-opportunities --json` per ottenere il diff (nuove opportunità, file nuovi/modificati/rimossi) rispetto all'ultimo snapshot;
2. se non ci sono novità, termina senza alcuna azione (nessuna chiamata Copilot CLI, nessun upload DocMind) — loggato in `logs/presales_autoupdate.log`;
3. se ci sono novità, invoca **GitHub Copilot CLI in modalità non interattiva** (`copilot -p "<prompt con diff>" --allow-all-tools --silent`), istruendola ad aggiornare **esclusivamente** il progetto DocMind `PreSales`: rigenerare `presales-overview` e i documenti di dettaglio delle opportunità coinvolte nel diff (o crearne uno nuovo se è comparsa una nuova opportunità), rileggendo i file aggiornati dalle cartelle locali.

**Perché questo approccio (e non uno script puramente meccanico)**: la generazione dei contenuti (in particolare la sezione "idee proposte") richiede ragionamento, non solo dati grezzi; riusare Copilot CLI in modalità headless (`-p`/`--allow-all-tools`) permette di mantenere la stessa qualità di analisi della generazione manuale, senza introdurre un nuovo motore AI/indice separato — coerente col principio di minima complessità (§2.3).

**Schedulazione**: cron utente, ogni ora dalle 9:00 alle 18:00:
```
0 9-18 * * * PATH=/usr/bin:/usr/local/bin:/bin /usr/bin/bash /home/fcampo/copilot-projects/teams-channel-agent/scripts/presales_autoupdate.sh
```

**Limiti noti e dichiarati esplicitamente all'utente:**
- Il job gira solo mentre l'istanza WSL è avviata: se la macchina è spenta nell'orario previsto, quell'esecuzione viene saltata (le novità accumulate verranno comunque rilevate al primo scan successivo).
- `--allow-all-tools` è necessario per l'esecuzione non interattiva; il rischio è mitigato restringendo esplicitamente nel prompt l'ambito al solo progetto DocMind "PreSales" e vietando scritture sulle cartelle sorgente (accesso di sola lettura).
- Non è un demone persistente né un nuovo MCP: resta uno script + cron, in linea con l'architettura "senza server" richiesta.

**Stato:** implementato e testato manualmente (scan senza novità → skip corretto, nessuna chiamata Copilot CLI); cron installato e cron.service verificato attivo. Non ancora osservato un ciclo completo con novità reali (in attesa del prossimo cambiamento nelle cartelle del canale).

## 13. Note
Documento aggiornato progressivamente; ogni versione sostituisce integralmente la precedente su DocMind (l'update sovrascrive il contenuto, non lo accoda — vedi nota tecnica interna).



