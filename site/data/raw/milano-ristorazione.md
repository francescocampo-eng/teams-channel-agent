# Presales — Dettaglio Opportunità: MILANO RISTORAZIONE

> Fonte dati: file locale canale Teams (OneDrive sync). Documento sorgente principale: `TODO_Meeting_Tecnico_Adesso_MiRi.md` (checklist preparazione meeting tecnico con Adesso.it), più `Business_Case_MVP_Ticketing_MiRi.xlsx` e 2 PDF (analisi As-Is/To-Be, ticketing). Sezione "Idee proposte dall'agente" in fondo: contenuto generato, non proveniente dal cliente.

## Perimetro e scopo

**MVP Ticketing** per Milano Ristorazione, in collaborazione con il partner Adesso.it:
- login/registrazione utenti;
- lista e dettaglio ticket;
- apertura e risposta ticket;
- stato ticket;
- propagazione del profilo utente a **Dynamics CRM**.

**Esplicitamente escluso dal perimetro MVP:** rette, iscrizioni, presenze, diete, pagamenti, CMS completo; migrazione/decommissioning non ancora definiti.

## Richiesta cliente

Milano Ristorazione necessita di un portale di ticketing rivolto a famiglie, scuole e operatori, con integrazione dei profili utente nel CRM Dynamics esistente. Il progetto è condotto in un modello a tre attori: **Milano Ristorazione** (cliente, sponsor/owner di business e IT), **Adesso.it** (presidio relazione e coordinamento con il cliente), **ENG** (architettura, integrazioni, delivery tecnico). È in preparazione un **meeting tecnico con Adesso.it** per allineare perimetro MVP, domande tecniche, stima preliminare di effort e modello organizzativo.

## Stato

**Fase:** preparazione meeting tecnico (checklist non ancora completata). WBS e stima ROM già elaborate come baseline di lavoro, **non ancora una stima contrattuale**.

**WBS e stima (13 work package MVP):** baseline avvio ottobre 2026, go-live target **giugno 2027**.

| Scenario | Effort pre-riserva | Effort con riserva 15% | FTE medi su 9 mesi |
|---|---:|---:|---:|
| Basso | ~506 gg-persona | ~582 gg-persona | ~3,2 |
| Base | 633 gg-persona | ~728 gg-persona | ~4,0 |
| Alto | ~792 gg-persona | ~911 gg-persona | ~5,1 |

Picco stimato: **~6,5 FTE a febbraio 2027** (riserva inclusa). Composizione principale: Portale/ticketing (115 gg), API Gateway/bus/listener CRM (96 gg), Identity/onboarding (58 gg), Governance/PMO (55 gg), Configurazione Dynamics (32 gg), Test integrati (64 gg), UAT/formazione (24 gg), Cutover/hypercare (21 gg), tra gli altri.

**Assunzioni della stima:** disponibilità tempestiva di ambienti/API/referenti cliente, nessuna migrazione dati, perimetro Dynamics limitato al flusso MVP. Ritardi su identity-to-CRM o dipendenze esterne possono spostare effort e calendario.

**Dati ancora mancanti (da richiedere al cliente prima di una stima vincolante):** utenti potenziali per categoria, volumi ticket attuali e stagionalità, picchi di accesso concorrenti, percentuale ticket con allegati, SLA attesi, sistemi sorgente/API/limiti (CRM, SPID/CIE, identità B2C, API Gateway), regole di identity matching, vincoli privacy/DPIA/accessibilità, data di scadenza licenze attuali.

**Modello organizzativo proposto (da formalizzare in RACI):** governance tripartita su 6 livelli (sponsor/priorità, steering, coordinamento quotidiano, architettura/integrazioni, prodotto/processi, esercizio), con ruoli e accountable distinti per Milano Ristorazione, Adesso.it, ENG.

**Gate consigliato (da fonte originale):** non impegnare prezzo e data di go-live come baseline vincolante finché non sono verificati volumi, requisiti operativi, identity-to-CRM, disponibilità integrazioni e opzione di proroga licenze.

## Preparazione meeting con Adesso.it (06/10/2026)

> Contenuto preparato come primo task assegnato sull'iniziativa, in vista del meeting tecnico con Adesso.it del 06/10/2026. Base: checklist `TODO_Meeting_Tecnico_Adesso_MiRi.md`, business case WBS e i due PDF di analisi As-Is/To-Be e ticketing. Da validare/integrare durante e dopo il meeting.

### Domande per Adesso.it

1. Chi è l'account lead congiunto lato Adesso.it e chi ha mandato a decidere in sessione (per evitare di tornare a chiedere mandato dopo il meeting)?
2. Come vedete la narrativa verso Milano Ristorazione: Adesso.it presidio relazione/coordinamento, ENG guida architettura/integrazioni/delivery — confermate questo split o lo intendete diversamente?
3. Prime contractor: chi fattura al cliente e come si regola la subfornitura ENG (perimetro economico, non solo tecnico)?
4. Come gestiamo insieme le change request dopo la baseline — c'è già un processo Adesso.it-cliente in cui ENG si deve inserire, o lo definiamo da zero?
5. Chi è owner degli artefatti (WBS, documentazione architetturale, codice) e con quale licenza/proprietà verso il cliente?
6. È previsto supporto post go-live (hypercare, L2/L3)? Con quale perimetro e per quanto tempo, e chi lo presidia?
7. Quali materiali (deck, WBS, stima) possiamo condividere direttamente con Milano Ristorazione, e con quale branding (ENG, Adesso.it, congiunto)?
8. Sul CRM Dynamics: chi ha accesso/ownership dell'ambiente e dei dati, Adesso.it o il cliente? ENG avrà un ambiente di test dedicato?
9. Sulla scadenza licenze (menzionata come vincolo nella checklist): qual è la data esatta e quali sono i margini di proroga già negoziati o negoziabili?
10. È disponibile o pianificabile una vertical slice identity-to-CRM come prova di fattibilità separata, prima di una stima vincolante?

### Punti aperti da validare (per area)

**Funzionale**
- Conferma perimetro MVP (login/registrazione, lista/dettaglio ticket, apertura/risposta, stato ticket, propagazione profilo a Dynamics) ed esclusioni esplicite (rette, iscrizioni, presenze, diete, pagamenti, CMS, migrazione/decommissioning).
- Service blueprint minimo: journey famiglie, scuole, operatori CRM — non ancora validato con il cliente.

**Tecnica / Integrazioni**
- Identity-to-CRM: regole di matching, consenso, account linking, gestione duplicati, riconciliazione manuale — nessuna risposta ancora.
- Sistemi sorgente, API, limiti di chiamata, ambienti/dati di test per CRM, SPID/CIE, identità B2C, API Gateway/event bus.
- NFR da validare: sicurezza, privacy/DPIA, accessibilità, performance, disponibilità, audit, retention, notifiche, SLA, allegati, reporting, supporto.

**Organizzativa / Governance**
- RACI formale (proposta a 6 livelli già abbozzata, da far firmare, non solo discutere).
- Composizione nucleo di delivery per fase (seniority, mix interno/partner, backup) — non definibile finché dipendenze e requisiti non sono chiusi.
- Modello di escalation e gestione change request post-baseline.

**Dati / Volumi**
- Nessuna baseline affidabile di utenti, ticket, concorrenza, allegati: servono 3 profili (normale/picco/stress) da costruire nel workshop, non numeri "a sensazione".

**Commerciale**
- Prime contractor e perimetro economico ENG vs Adesso.it.
- Gate esplicito: non impegnare prezzo/data di go-live finché volumi, NFR, identity-to-CRM, disponibilità integrazioni e proroga licenze non sono verificati.

### Ambiti di responsabilità da chiarire

| Area | Milano Ristorazione | Adesso.it | ENG |
|---|---|---|---|
| Sponsorship / priorità | Accountable obiettivi, priorità, accettazione | Supporto relazione/coordinamento | Consulenza impatti tecnici e stime |
| Relazione col cliente | — | Presidio primario | Partecipazione su invito/temi tecnici |
| Architettura e integrazioni | Approva target, accessi, vincoli | Coordina interlocutori/dipendenze | Lead architettura, API/eventi, sicurezza tecnica |
| Prodotto e processi | Owner requisiti, journey, UAT | Facilita raccolta requisiti/decisioni | Analisi impatti, UX, implementazione nel perimetro concordato |
| Delivery tecnico | — | PM/PMO, gestione dipendenze concordate | Project manager, responsabili work package |
| Esercizio post go-live | Service owner, supporto L1 (da modello cliente) | Coordinamento servizio da contratto | Supporto L2/L3, osservabilità (se incluso nel contratto) |

Nodo critico da chiarire in meeting: dove finisce il "coordinamento" di Adesso.it e dove inizia la "guida tecnica" di ENG su architettura/integrazioni — è l'area con più rischio di sovrapposizione operativa.

### Ipotesi di nostro scope (ENG)

- **Dentro perimetro**: solution architecture, integrazioni (API Gateway/event bus, listener CRM), identity-to-CRM, configurazione Dynamics lato integrazione, sviluppo portale/ticketing, test integrati, cloud/DevOps, sicurezza tecnica, supporto a UAT/cutover.
- **Da negoziare/chiarire**: presenza ENG nei tavoli diretti col cliente (oggi presidiati da Adesso.it), responsabilità su UX/UI e accessibilità, perimetro esatto del supporto post go-live (L2/L3 sì, L1 no — da confermare).
- **Fuori perimetro (presunto)**: relazione commerciale/contrattuale con Milano Ristorazione (in capo ad Adesso.it), funzionalità evolutive oltre l'MVP (rette, pagamenti, CMS — da stimare separatamente se richieste in futuro).

### Bozza stima effort / elapsed / FTE

Baseline ROM esistente (WBS a 13 work package, da validare non da ripetere in meeting):

| Scenario | Effort pre-riserva | Effort con riserva 15% | FTE medi su 9 mesi |
|---|---:|---:|---:|
| Basso | ~506 gg-persona | ~582 gg-persona | ~3,2 |
| Base | 633 gg-persona | ~728 gg-persona | ~4,0 |
| Alto | ~792 gg-persona | ~911 gg-persona | ~5,1 |

- **Elapsed**: baseline ottobre 2026 → go-live giugno 2027 (9 mesi), picco ~6,5 FTE a febbraio 2027.
- **Profili/competenze richieste** (non tutti full-time, da attivare per fase): PM/Delivery Lead, Product Owner/Business Analyst, Solution Architect/Integration Lead, UX/UI con competenza accessibilità, team full-stack portale/ticketing, Identity Engineer (SPID/CIE, B2C), Dynamics Engineer, Cloud/DevOps Engineer, QA/Test Lead, Security/Privacy specialist, Service/Operations lead per hypercare.
- **Dipendenze/assunzioni da validare prima che la stima diventi vincolante**: disponibilità tempestiva di ambienti/API/referenti cliente, nessuna migrazione dati, perimetro Dynamics limitato al flusso MVP, dati di volume reali (oggi assenti), esito vertical slice identity-to-CRM.

### Rischi e assunzioni

- **Rischio di sovrapposizione operativa**: confine sfumato tra "coordinamento" (Adesso.it) e "guida tecnica" (ENG) su architettura/integrazioni — senza RACI firmata prima del meeting, rischio di decisioni prese due volte o di nessuno.
- **Rischio stima**: la baseline ROM non ha ancora volumi reali (utenti, ticket, picchi, allegati) — presentarla come "preliminare" esplicitamente, non come impegno.
- **Rischio identity-to-CRM**: è il nodo tecnico più critico e meno definito (matching, consenso, duplicati) — può spostare effort e calendario più di ogni altra dipendenza.
- **Rischio commerciale**: prime contractor e perimetro economico non ancora chiariti — da risolvere prima di condividere stime con il cliente finale.
- **Assunzione da verificare**: scadenza licenze attuali e margine di proroga — condiziona la rigidità della data di go-live.
- **Assunzione da verificare**: disponibilità di ambienti/dati di test per CRM, SPID/CIE, identità B2C, API Gateway in tempi compatibili con la pianificazione.

## Idee proposte dall'agente

> Contenuto generato da questo agente (non dal cliente/partner), da validare prima di presentarlo ad Adesso.it/Milano Ristorazione. Approccio ispirato ai planner ENGenius (ANALYSIS, FP_SIZING, WBS, ACTIVITY).

1. **Raffinare la stima ROM con Function Point / SNAP sizing**: la WBS attuale è per work package; affiancarla con un sizing a Function Point (planner ENGenius `FP_SIZING`, eventualmente supportato dal tool `mcp-fp-snap-server`) darebbe una seconda misura indipendente da confrontare con la stima a gg-persona.
2. **Vertical slice identity-to-CRM come prova di fattibilità anticipata**: proporla come primo "sprint 0" a pagamento separato per validare il collegamento più critico (identità → Dynamics) prima di impegnarsi sulla stima completa.
3. **RACI formalizzata prima del meeting, non durante**: portare in meeting una bozza di RACI già compilata invece di limitarsi a discuterne il modello.
4. **Tre profili di volume (normale/picco/stress) come allegato tecnico separato**: template già strutturato da far compilare a Milano Ristorazione nel workshop.
5. **Dependency matrix con data di scadenza esplicita per ciascuna dipendenza**: collegata visibilmente al gate "non impegnare prezzo/data".
6. **Piano di escalation change request già abbozzato in fase di proposta**: anticipare come verranno gestite le change request post-baseline, per evitare conflitti a metà progetto.
