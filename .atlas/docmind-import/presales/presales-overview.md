---
unique-name: presales-overview
display-name: Presales - Panoramica Opportunità (mappa dei filoni)
category: OVERVIEW_DRAFT
description: Mappa di tutte le opportunità/filoni presenti nel canale Teams presales, con stato sintetico, file disponibili e rimando ai documenti di dettaglio. Generata e mantenuta dall'agente teams-channel-agent tramite scan automatico delle cartelle sincronizzate.
---

# Presales — Panoramica Opportunità (canale Teams "Delivery Factory A - PreSales and Opptys - PreSales")

> Fonte: file locale (cartella canale Teams sincronizzata via OneDrive, letta da WSL). Rilevamento e mappatura a cura dell'agente `teams-channel-agent`, tramite scan automatico delle cartelle (`scan-opportunities`).
> Data rilevamento: 2026-10-05, ultimo scan con modifiche rilevate 2026-10-06 (business case Milano Ristorazione aggiornato).

## Come viene mantenuta aggiornata questa panoramica

L'agente esegue uno scan delle sottocartelle del canale (una per opportunità/commessa) e confronta lo stato attuale con l'ultimo snapshot salvato (`output/opportunities_snapshot.json`). Ad ogni esecuzione rileva: nuove opportunità comparse, opportunità non più presenti, file nuovi, file modificati, file rimossi. Questo documento e i documenti di dettaglio per singola opportunità vengono aggiornati di conseguenza. Fonte di ogni informazione sempre dichiarata (file locale / OneDrive sync, oppure idea proposta dall'agente).

## Mappa dei filoni

| Opportunità | Macro-ambito | Cliente / interlocutore | Stato sintetico | File disponibili | Documento di dettaglio |
|---|---|---|---|---|---|
| ARPAV - Integrazione Google Calendar | Integrazione calendari esterni (Prisma/SINAP → Google Calendar) | ARPAV | Analisi/review in corso, nessun pilot avviato; punti P0 da chiudere | 3 (md review, pdf, eml) | presales-arpav |
| MILANO RISTORAZIONE | Portale ticketing MVP (famiglie/scuole/operatori) + integrazione Dynamics CRM | Milano Ristorazione (tramite partner Adesso.it) | Meeting tecnico 06/10; business case formalizzato con prezzo indicativo e review a 10 rilievi (5 Alta priorità, incl. ADR architetturale mancante); go-live target giugno 2027 | 4 (md, business case xlsx, 2 pdf) | presales-miri |
| STAR HOTELS | PoC flow INLAY + Assessment enterprise Tech & Business | Star Hotels | Fase iniziale, needs raccolti da presentazione INLAY, perimetro assessment da definire col cliente, deadline fine 2026 | 1 (summary.txt) | presales-star-hotels |
| RCS - Rizzoli Corriere Della Sera | Non ancora definito | RCS | Nessuna informazione disponibile localmente (cartella vuota) | 0 | presales-rcs |

## Sintesi per filone

### ARPAV — Integrazione Google Calendar
Necessità potenziale: pubblicare su Google Calendar gli eventi gestiti in Prisma (ex SINAP), riducendo doppio inserimento. Perimetro assunto: unidirezionale Prisma → Google, nessuna sincronizzazione inversa né integrazione Outlook/Microsoft in questa fase. Raccomandazione della review esistente: non avviare produzione finché non sono chiariti identità/autorizzazioni, dati trasferiti, modello di calendario (personale vs condiviso) e relazione Prisma/SINAP.

### MILANO RISTORAZIONE
MVP di portale ticketing per famiglie, scuole e operatori, con propagazione profilo a Dynamics CRM. Collaborazione a tre: Milano Ristorazione (cliente), Adesso.it (relazione/coordinamento), ENG (architettura, integrazioni, delivery tecnico). WBS con 13 work package; stima ROM 506-911 gg-persona a seconda dello scenario (basso/base/alto), picco ricalcolato ~5,9 FTE a marzo 2027. Il business case ricevuto il 06/10 (stesso giorno del meeting tecnico) formalizza per la prima volta anche costo (~364k€ scenario base) e prezzo indicativo (~485k€), e include una review strutturata che segnala 5 rilievi ad alta priorità — il più critico: nessuna decisione architetturale (ADR) tra alternativa SAP-centrica e Best of Breed, da cui dipendono master data e sizing delle integrazioni.

### STAR HOTELS
A seguito di una presentazione INLAY, il cliente ha espresso due esigenze: (1) verificare un flow INLAY su una componente a sua scelta; (2) ricevere una proposta/stima di un assessment enterprise (tecnico + business) su un perimetro ancora da definire dal cliente, usando l'Assessment Estimator, con obiettivo di illustrare il journey, stimare l'assessment, farselo commissionare e produrre entro fine 2026 una timeline e un budget di programma.

### RCS — Rizzoli Corriere Della Sera
Nessun file presente nella cartella del canale al momento del rilevamento. Il filone esiste come sottocartella ma non contiene ancora materiale. Da monitorare nei prossimi scan.

## Prossimi passi proposti (agente)
- Approfondire RCS non appena compariranno file nel canale (lo scan li segnalerà automaticamente come "nuovi").
- Per ARPAV: supportare la preparazione dei workshop P0 (allineamento funzionale, fattibilità tecnica/identità, privacy/costi) già delineati nella review esistente.
- Per MILANO RISTORAZIONE: supportare la preparazione del meeting tecnico con Adesso.it (checklist, agenda, stima) e, se utile, raffinare la stima con i planner ENGenius (ANALYSIS, FP_SIZING, WBS).
- Per STAR HOTELS: preparare sia il PoC del flow INLAY sia l'impostazione dell'assessment enterprise (vedi documento di dettaglio per le idee proposte, con supporto delle skill `ui-ux-pro-max`, `proposal-writing` e `impact`).
