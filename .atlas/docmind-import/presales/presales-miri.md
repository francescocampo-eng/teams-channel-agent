---
unique-name: presales-miri
display-name: Presales - Dettaglio Opportunità: MILANO RISTORAZIONE
category: OPPORTUNITY_DRAFT
description: Dettaglio opportunità Milano Ristorazione: wording corretto (rimossi anglicismi/gergo forzato), chiarito perimetro ENG-only della stima WBS, aggiunto cross-check FP sizing (IFPUG), e integrate le 6 decisioni dell'utente sulle idee proposte dall'agente (no nuovi documenti, test pilota a investimento non fatturabile, RACI aperta, volume profiles/escalation plan come bozze da discutere al meeting).
---

# Presales — Dettaglio Opportunità: MILANO RISTORAZIONE

> Fonte dati: file locale canale Teams (OneDrive sync). Documento sorgente principale: `TODO_Meeting_Tecnico_Adesso_MiRi.md` (checklist preparazione meeting tecnico con Adesso.it), più `Business_Case_MVP_Ticketing_MiRi.xlsx` (aggiornato il 06/10/2026, lo stesso giorno del meeting) e 2 PDF (analisi As-Is/To-Be, ticketing). Sezione "Idee proposte dall'agente" in fondo: contenuto generato, non proveniente dal cliente.

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

> **Perimetro della stima:** riferita al solo effort di delivery **ENG** (tutti i 13 work package hanno ruolo lead e costo giornaliero del team interno ENG). Non include l'effort di coordinamento/relazione verso il cliente svolto da Adesso.it.

| Scenario | Effort pre-riserva | Effort con riserva 15% | FTE medi su 9 mesi |
|---|---:|---:|---:|
| Basso | ~506 gg-persona | ~582 gg-persona | ~3,2 |
| Base | 633 gg-persona | ~728 gg-persona | ~4,0 |
| Alto | ~792 gg-persona | ~911 gg-persona | ~5,1 |

Picco stimato: **~6,5 FTE a febbraio 2027** (riserva inclusa) nella baseline del 02/10; ricalcolo del 06/10 sul business case aggiornato: **~5,9 FTE a marzo 2027** (vedi sezione "Business case aggiornato" più sotto per il dettaglio del ricalcolo).

Composizione principale: Portale/ticketing (115 gg), API Gateway/bus/listener CRM (96 gg), Identity/onboarding (58 gg), Governance/PMO (55 gg), Configurazione Dynamics (32 gg), Test integrati (64 gg), UAT/formazione (24 gg), Avvio in produzione/assistenza post avvio (21 gg), tra gli altri.

**Cross-check indipendente (Function Point, IFPUG):** sizing rapido delle 5 capability core (profilo utente, ticket, propagazione CRM) → **44 FP**, equivalenti a **~44 gg-persona di solo sviluppo funzionale** a velocità team media (8h/FP). Coerente come ordine di grandezza con la quota di puro coding dei WP 1.6/1.8/1.9 (Portale+API Gateway+Config Dynamics, 243 gg totali, di cui test/integrazione/non-funzionali sono la parte restante). *Conteggio basato su DET/RET assunti, da validare con requisiti definitivi — non sostituisce la WBS.*

**Assunzioni della stima:** disponibilità tempestiva di ambienti/API/referenti cliente, nessuna migrazione dati, perimetro Dynamics limitato al flusso MVP. Ritardi su collegamento identità-Dynamics o dipendenze esterne possono spostare effort e calendario.

**Dati ancora mancanti (da richiedere al cliente prima di una stima vincolante):** utenti potenziali per categoria, volumi ticket attuali e stagionalità, picchi di accesso concorrenti, percentuale ticket con allegati, SLA attesi, sistemi sorgente/API/limiti (CRM, SPID/CIE, identità B2C, API Gateway), regole di identity matching, vincoli privacy/DPIA/accessibilità, data di scadenza licenze attuali.

**Modello organizzativo proposto (da formalizzare in RACI):** governance tripartita su 6 livelli (sponsor/priorità, steering, coordinamento quotidiano, architettura/integrazioni, prodotto/processi, esercizio), con ruoli e accountable distinti per Milano Ristorazione, Adesso.it, ENG.

**Gate consigliato (da fonte originale):** non impegnare prezzo e data di go-live come baseline vincolante finché non sono verificati volumi, requisiti operativi, collegamento identità-Dynamics, disponibilità integrazioni e opzione di proroga licenze.

## Business case aggiornato (06/10/2026) — lettura del file `Business_Case_MVP_Ticketing_MiRi.xlsx`

> Il file, modificato il giorno stesso del meeting tecnico con Adesso.it, non cambia il perimetro né i numeri aggregati della WBS (restano 13 work package, 633 gg-persona base) ma lo **formalizza**: aggiunge un foglio Parametri con le assunzioni esplicite di costo/prezzo, un foglio Review con 10 rilievi critici strutturati e un foglio Copertura che mappa l'MVP contro 12 requisiti dell'assessment AS-IS/TO-BE. È la prima volta che il business case riporta un prezzo indicativo, non solo un effort.

### Indicatori economici (nuovi — prima non calcolati)

Parametri dichiarati nel foglio "Parametri": costo medio team 500 €/gg-persona, margine commerciale 25% sul prezzo, riserva di progetto 15% sull'effort, 20 gg lavorative/mese per FTE, periodo ottobre 2026–giugno 2027 (9 mesi).

| Scenario | Effort base (gg) | Effort con riserva 15% (gg) | FTE medio periodo | Costo team (EUR) | Prezzo indicativo (EUR) |
|---|---:|---:|---:|---:|---:|
| Low (-20%) | ~506 | ~582 | ~3,2 | ~291.000 | ~388.000 |
| Base | 633 | ~728 | ~4,0 | ~364.000 | ~485.000 |
| High (+25%) | ~791 | ~910 | ~5,1 | ~455.000 | ~607.000 |

*Verificato ricalcolando le formule del foglio (i valori cache erano assenti, file non ancora ricalcolato in Excel/LibreOffice): prezzo = costo / (1 − margine), costo = effort con riserva × 500 €/gg. Numeri coerenti con la baseline ROM già nota (506/633/791 gg pre-riserva), quindi nessuna sorpresa sull'effort — la novità è l'esplicitazione di costo e prezzo, finora assenti dal tracking.*

**Picco di carico ricalcolato dalla distribuzione mensile dei 13 WP (foglio "Carico mensile"):** ~5,9 FTE a **marzo 2027** (scenario base, riserva inclusa), non ~6,5 FTE a febbraio come riportato nella baseline del 02/10. Lo scostamento è spiegabile con la sovrapposizione tra Portale/ticketing (1.6, gen-mar), Identity/onboarding (1.7, dic-feb) e API Gateway/CRM (1.8, nov-mar): il mese di picco effettivo dipende da come si distribuisce l'effort di ciascun WP nel suo intervallo, sensibile a assunzioni di dettaglio non esplicitate nel file. Da non trattare come contraddizione ma come raffinamento: la differenza (~0,6 FTE) rientra nel margine di incertezza di una stima ROM.

### Rilievi della review (10, già incorporati nel foglio "Review" del business case)

Priorità **Alta** (5 su 10 — i nodi che vanno chiusi prima di una stima vincolante):

1. **Nessuna decisione architetturale (ADR)** tra alternativa SAP-centrica e Best of Breed: l'assessment descrive entrambe (pp.20-35) ma il deck MVP non sceglie. Rischio di rework su master data, API e sizing delle integrazioni se la decisione arriva dopo l'avvio del build.
2. **Scope gap tra Quick Win e trasformazione ecosistemica**: il deck limita l'MVP a 5 capability di ticketing, l'assessment estende il portale a iscrizioni, pagamenti, diete, presenze e CMS (pp.21, 31). Senza una baseline di scope con incluso/escluso esplicito, il rischio è che budget e aspettative del cliente includano implicitamente l'intera roadmap pluriennale.
3. **Ticketing non ancora definito come servizio operativo**: SLA, notifiche, allegati, categorie/priorità, spam, reporting non sono specificati nel deck. UAT e go-live rischiano di scoprire requisiti di processo non stimati.
4. **Identità-Dynamics come nodo di percorso critico**: matching, consenso, account linking, duplicati non hanno ancora risposta. Confermato come il rischio tecnico più alto, coerente con quanto già tracciato (R3 nella sezione rischi sotto).
5. **Dipendenze esterne senza owner/data/fallback**: federazione SPID/CIE, CRM, SAP/reporting sono citate come dipendenze ma senza dependency matrix formalizzata.

Priorità **Media** (4): piattaforma Gateway/Event Bus proposta senza sizing né modello operativo; governance tripartita e modello economico (RACI, IP, change control) ancora da formalizzare; timeline coerente con la scadenza licenze ma senza buffer/rollback verificati; NFR (accessibilità, privacy, audit) citati ma senza criteri di accettazione misurabili.

Priorità **Bassa** (1): processi strategici (assenze/RID/ISEE, valutazioni commissari) dichiarati manuali o non analizzati — da trattare come discovery futura, non da sottostimare come "già coperti".

### Matrice di copertura (12 requisiti AS-IS/TO-BE vs perimetro MVP)

Nessuno dei 12 requisiti strategici dell'assessment risulta "Completo" nel perimetro MVP: **9 Parziale**, **1 Fuori perimetro** (vista integrata dei servizi attivi — rette/pagamenti/diete/presenze, rimandata a tranche future), **1 Da decidere** (modello dati/master data condiviso, dipende dall'ADR SAP-centrica vs Best of Breed ancora non presa), **1 Parziale** sul rilascio prima della scadenza licenze (percorso critico, buffer e proroga non contrattualizzati). Lettura sintetica: l'MVP è un **passo coerente ma circoscritto** verso la trasformazione descritta nell'assessment, non una sua realizzazione anticipata — va comunicato così ad Adesso.it e al cliente per evitare un disallineamento di aspettative sul perimetro.

### Cross-check indipendente (metodo FP/ENGenius, skill `impact` + `engenius`)

Il cross-check FP già realizzato il 05/10 (44 FP ≈ 44 gg-persona sulle 5 capability core: profilo utente, ticket, propagazione CRM) resta valido e non richiede revisione: il business case aggiornato non cambia le capability MVP, solo la loro presentazione economica. Applicando la stessa logica di scoring a complessità usata nel planner WBS di ENGenius (fattori: complessità funzionale/tecnica/integrazione/dati/rischio, scala XS→XL), il work package più esposto a deriva di stima resta **1.8 "API Gateway, bus e listener CRM"** (96 gg base): alta complessità di integrazione (identity-to-CRM, retry/idempotenza, DLQ) e rischio per requisiti non ancora chiusi — classificabile **XL** con la tabella di conversione ENGenius (10-20 gg per singolo macro-task, qui aggregato su più sotto-attività), a conferma che è il WP con maggior necessità di una vertical slice di prova (vedi R3/D10 sotto) prima di congelare il prezzo.

## Preparazione meeting con Adesso.it (06/10/2026)

> Contenuto preparato come primo task assegnato sull'iniziativa, in vista del meeting tecnico con Adesso.it del 06/10/2026. Base: checklist `TODO_Meeting_Tecnico_Adesso_MiRi.md`, business case WBS e i due PDF di analisi As-Is/To-Be e ticketing. Da validare/integrare durante e dopo il meeting.

> ID stabili per riferimento in sede di meeting e nel verbale che seguirà (convenzione `D`=domanda, `OP`=open point, `R`=rischio): ogni voce sotto può essere citata per ID durante la discussione invece di doverla ridescrivere.

### Domande per Adesso.it

1. **D1** — Chi è il referente unico condiviso lato Adesso.it e chi ha mandato a decidere in sessione (per evitare di tornare a chiedere mandato dopo il meeting)?
2. **D2** — Come vedete l'impostazione da comunicare a Milano Ristorazione: Adesso.it presidio relazione/coordinamento, ENG guida architettura/integrazioni/delivery — confermate questa suddivisione o la intendete diversamente? *(collegata a OP-ORG-1/nodo critico sotto)*
3. **D3** — Capofila contrattuale: chi fattura al cliente e come si regola la subfornitura ENG (perimetro economico, non solo tecnico)?
4. **D4** — Come gestiamo insieme le change request dopo la baseline — c'è già un processo Adesso.it-cliente in cui ENG si deve inserire, o lo definiamo da zero?
5. **D5** — Chi è owner degli artefatti (WBS, documentazione architetturale, codice) e con quale licenza/proprietà verso il cliente?
6. **D6** — È prevista assistenza post avvio (L2/L3)? Con quale perimetro e per quanto tempo, e chi lo presidia?
7. **D7** — Quali materiali (presentazione, WBS, stima) possiamo condividere direttamente con Milano Ristorazione, e con quale branding (ENG, Adesso.it, congiunto)?
8. **D8** — Sul CRM Dynamics: chi ha accesso/ownership dell'ambiente e dei dati, Adesso.it o il cliente? ENG avrà un ambiente di test dedicato?
9. **D9** — Sulla scadenza licenze (vincolo citato nella checklist): qual è la data esatta e quali sono i margini di proroga già negoziati o negoziabili? Se la risposta è vaga, è un segnale che il gate "non impegnare la data di go-live" (vedi R2) va mantenuto esplicitamente in chiusura meeting.
10. **D10** — È disponibile o pianificabile un test pilota sul collegamento identità-Dynamics come prova di fattibilità separata, prima di una stima vincolante?

### Punti aperti da validare (per area)

**Funzionale**
- **OP-FUN-1** — Conferma perimetro MVP (login/registrazione, lista/dettaglio ticket, apertura/risposta, stato ticket, propagazione profilo a Dynamics) ed esclusioni esplicite (rette, iscrizioni, presenze, diete, pagamenti, CMS, migrazione/decommissioning).
- **OP-FUN-2** — Mappa del servizio minima: journey famiglie, scuole, operatori CRM — non ancora validato con il cliente.

**Tecnica / Integrazioni**
- **OP-TEC-1** — Collegamento identità-Dynamics: regole di matching, consenso, account linking, gestione duplicati, riconciliazione manuale — nessuna risposta ancora. *(nodo a effort/calendario più alto, vedi R3)*
- **OP-TEC-2** — Sistemi sorgente, API, limiti di chiamata, ambienti/dati di test per CRM, SPID/CIE, identità B2C, API Gateway/event bus.
- **OP-TEC-3** — NFR da validare: sicurezza, privacy/DPIA, accessibilità, performance, disponibilità, audit, retention, notifiche, SLA, allegati, reporting, supporto.

**Organizzativa / Governance**
- **OP-ORG-1** — RACI formale (proposta a 6 livelli già abbozzata). **Punto tenuto aperto**: non è garantito avere una bozza compilabile e condivisibile in tempo per il meeting del 06/10 — se pronta la si porta come bozza di lavoro, altrimenti si discute il modello a voce e si formalizza come follow-up post-meeting. *(collegata a D2 e al nodo critico di responsabilità sotto)*
- **OP-ORG-2** — Composizione nucleo di delivery per fase (seniority, mix interno/partner, riserve/sostituti) — non definibile finché dipendenze e requisiti non sono chiusi.
- **OP-ORG-3** — Modello di escalation e gestione change request post-baseline.

**Dati / Volumi**
- **OP-DAT-1** — Nessuna baseline affidabile di utenti, ticket, concorrenza, allegati: servono 3 profili (normale/picco/stress) da costruire in un incontro di lavoro dedicato, non numeri "a sensazione".

**Commerciale**
- **OP-COM-1** — Capofila contrattuale e perimetro economico ENG vs Adesso.it.
- **OP-COM-2** — Gate esplicito: non impegnare prezzo/data di go-live finché volumi, NFR, collegamento identità-Dynamics, disponibilità integrazioni e proroga licenze non sono verificati.

### Ambiti di responsabilità da chiarire

| Area | Milano Ristorazione | Adesso.it | ENG |
|---|---|---|---|
| Sponsorship / priorità | Accountable obiettivi, priorità, accettazione | Supporto relazione/coordinamento | Consulenza impatti tecnici e stime |
| Relazione col cliente | — | Presidio primario | Partecipazione su invito/temi tecnici |
| Architettura e integrazioni | Approva target, accessi, vincoli | Coordina interlocutori/dipendenze | Lead architettura, API/eventi, sicurezza tecnica |
| Prodotto e processi | Owner requisiti, journey, UAT | Facilita raccolta requisiti/decisioni | Analisi impatti, UX, implementazione nel perimetro concordato |
| Delivery tecnico | — | PM/PMO, gestione dipendenze concordate | Project manager, responsabili work package |
| Esercizio post go-live | Service owner, supporto L1 (da modello cliente) | Coordinamento servizio da contratto | Supporto L2/L3, osservabilità (se incluso nel contratto) |

Nodo critico da chiarire in meeting (**OP-ORG-1**): dove finisce il "coordinamento" di Adesso.it e dove inizia la "guida tecnica" di ENG su architettura/integrazioni — è l'area con più rischio di sovrapposizione operativa. Controfattuale da verificare: se Adesso.it intende mantenere anche le decisioni architetturali (non solo la relazione), la suddivisione di scope qui sotto va rivista prima, non dopo, la firma della RACI.

### Ipotesi di nostro scope (ENG)

- **Dentro perimetro**: solution architecture, integrazioni (API Gateway/event bus, listener CRM), collegamento identità-Dynamics, configurazione Dynamics lato integrazione, sviluppo portale/ticketing, test integrati, cloud/DevOps, sicurezza tecnica, supporto a UAT/avvio in produzione.
- **Da negoziare/chiarire**: presenza ENG nei tavoli diretti col cliente (oggi presidiati da Adesso.it), responsabilità su UX/UI e accessibilità, perimetro esatto dell'assistenza post avvio (L2/L3 sì, L1 no — da confermare).
- **Fuori perimetro (presunto)**: relazione commerciale/contrattuale con Milano Ristorazione (in capo ad Adesso.it), funzionalità evolutive oltre l'MVP (rette, pagamenti, CMS — da stimare separatamente se richieste in futuro).

### Bozza stima effort / elapsed / FTE

Baseline ROM esistente (WBS a 13 work package, da validare non da ripetere in meeting):

| Scenario | Effort pre-riserva | Effort con riserva 15% | FTE medi su 9 mesi |
|---|---:|---:|---:|
| Basso | ~506 gg-persona | ~582 gg-persona | ~3,2 |
| Base | 633 gg-persona | ~728 gg-persona | ~4,0 |
| Alto | ~792 gg-persona | ~911 gg-persona | ~5,1 |

- **Elapsed**: baseline ottobre 2026 → go-live giugno 2027 (9 mesi), picco ~5,9 FTE a marzo 2027 (ricalcolo 06/10, vedi sopra).
- **Profili/competenze richieste** (non tutti full-time, da attivare per fase): PM/Delivery Lead, Product Owner/Business Analyst, Solution Architect/Integration Lead, UX/UI con competenza accessibilità, team full-stack portale/ticketing, Identity Engineer (SPID/CIE, B2C), Dynamics Engineer, Cloud/DevOps Engineer, QA/Test Lead, Security/Privacy specialist, Service/Operations lead per assistenza post avvio.
- **Dipendenze/assunzioni da validare prima che la stima diventi vincolante**: disponibilità tempestiva di ambienti/API/referenti cliente, nessuna migrazione dati, perimetro Dynamics limitato al flusso MVP, dati di volume reali (oggi assenti), esito test pilota sul collegamento identità-Dynamics.

### Rischi e assunzioni

| ID | Rischio / assunzione | Implicazione se non gestito | Mitigazione proposta |
|---|---|---|---|
| **R1** | Sovrapposizione operativa: confine sfumato tra "coordinamento" (Adesso.it) e "guida tecnica" (ENG) su architettura/integrazioni (OP-ORG-1) | Decisioni prese due volte, o da nessuno, a metà progetto | RACI in bozza se pronta prima del meeting, altrimenti modello discusso a voce e formalizzato come follow-up — vedi D2 |
| **R2** | Stima ROM senza volumi reali (utenti, ticket, picchi, allegati) | Rischio di percepire la stima come impegno vincolante | Presentarla esplicitamente come "preliminare"; mantenere il gate OP-COM-2 (non impegnare prezzo/data) |
| **R3** | Il collegamento identità-Dynamics è il nodo tecnico più critico e meno definito (matching, consenso, duplicati) | Può spostare effort e calendario più di ogni altra dipendenza | Test pilota dedicato (D10) prima di stima vincolante |
| **R4** | Capofila contrattuale e perimetro economico non ancora chiariti (OP-COM-1) | Blocca la condivisione di stime con il cliente finale | Chiudere D3 in meeting, non rimandarlo a un follow-up separato |
| **R5 (assunzione)** | Scadenza licenze attuali e margine di proroga non confermati | Condiziona la rigidità della data di go-live | Verificare con D9; se la risposta resta vaga, mantenere il gate su go-live |
| **R6 (assunzione)** | Disponibilità di ambienti/dati di test (CRM, SPID/CIE, identità B2C, API Gateway) nei tempi del piano | Slittamento a cascata su sviluppo e test integrati | Tabella delle dipendenze con owner e data esplicita (azione da chiudere in meeting, non dopo) |

## Idee proposte dall'agente — decisioni interne ENG (pre-meeting)

> Contenuto generato da questo agente, validato internamente il 05/10/2026 e integrato il 06/10/2026. Nessun documento aggiuntivo: tutte le decisioni restano in questo stesso file.

1. **FP sizing** — Eseguito (vedi cross-check sopra, 44 FP / ~44 gg-persona sulle capability core), integrato nella sezione "Stato" invece di un documento a parte. Nessuna ulteriore produzione documentale prevista.
2. **Test pilota identità-Dynamics** — **Non a pagamento separato**: lo facciamo come **investimento ENG**, per avere confidenza su una stima realistica prima dell'impegno definitivo (non lo offriamo come voce fatturabile a sé).
3. **RACI** — **Punto tenuto aperto**: non abbiamo certezza di riuscire a preparare una bozza condivisibile entro il meeting del 06/10; si valuta avvicinandosi alla data (vedi OP-ORG-1/R1).
4. **Tre profili di volume (normale/picco/stress)** — Prepariamo una bozza di template e la **proponiamo ad Adesso.it durante il meeting** (da far compilare insieme a Milano Ristorazione in un secondo momento).
5. **Tabella delle dipendenze con data di scadenza** — Confermata, procede come proposto.
6. **Piano di escalation change request** — Prepariamo una **bozza di proposta ENG**, da portare e discutere al meeting (non già concordata/definitiva).
7. **ADR architetturale come precondizione commerciale** — Alla luce della review del business case (rilievo Alta priorità su SAP-centrica vs Best of Breed), proponiamo di portare al meeting odierno una richiesta esplicita: **nessun prezzo impegnativo finché l'ADR non è firmato**, anche se questo significa spostare la baseline economica definitiva oltre il 06/10. È coerente con il gate OP-COM-2 già tracciato, ma lo rende più stringente: oggi il rischio di scope/architettura è documentato in un foglio formale (Copertura), non solo in una nota interna.
