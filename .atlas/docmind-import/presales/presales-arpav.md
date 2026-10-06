---
unique-name: presales-arpav
display-name: Presales - Dettaglio Opportunità: ARPAV - Integrazione Google Calendar
category: OPPORTUNITY_DRAFT
description: Perimetro/scopo, richiesta cliente, stato e idee proposte per l'opportunità ARPAV - Integrazione Google Calendar (Prisma/SINAP verso Google Calendar). Basato su review esistente nel canale Teams.
---

# Presales — Dettaglio Opportunità: ARPAV - Integrazione Google Calendar

> Fonte dati: file locale canale Teams (OneDrive sync). Documento sorgente originale: `Review-opportunita-calendari-esterni-SINAP.md` (review del 2 ottobre 2026, basata sul corpo testuale di una email del 1 ottobre 2026; un PDF Outlook allegato non è stato estratto). Sezione "Idee proposte dall'agente" in fondo: contenuto generato, non proveniente dal cliente.

## Perimetro e scopo

Pubblicazione **unidirezionale** degli eventi da **Prisma verso Google Calendar**: le modifiche originate in Prisma possono essere pubblicate su Google; le modifiche fatte direttamente in Google non vengono riportate in Prisma. Fuori perimetro in questa fase: integrazione Outlook/Microsoft, sincronizzazione Google → Prisma o bidirezionale.

Punto aperto esplicito nella review sorgente: verificare se **Prisma coincide con il sistema SINAP** citato nelle fonti storiche (documento tecnico del 13 agosto 2024, prototipo Spring Boot, conversazioni Teams di agosto 2024) — non ancora confermato.

## Richiesta cliente

ARPAV ha richiesto un'analisi sulla connessione a calendari esterni (Google Calendar e/o Outlook) a partire dal sistema SINAP/Prisma (riferimento email: "[ARPAV][CheckAP_exSINAP] - analisi su connessione a calendari esterni"). L'email rimanda a un documento tecnico (`ANNOTAZIONI_SP_SINAP_CALENDAR.docx`, non disponibile localmente) e a conversazioni Teams non recuperate.

**Necessità possibile:** pubblicare su Google Calendar gli eventi gestiti in Prisma, riducendo la duplicazione di inserimento e migliorando la visibilità degli eventi per utenti/enti.

**Valore potenziale:** minori disallineamenti, adozione più semplice se il calendario SINAP è già parte dei flussi di lavoro degli enti.

**Non ancora dimostrato:** utenti coinvolti e frequenza del problema reale; eventi/campi da pubblicare; calendario Google destinatario (personale vs condiviso per ente); account/tenant disponibili; costi e oneri amministrativi Google Workspace; benefici misurabili rispetto a una semplice esportazione `.ics`.

## Stato

**Fase:** analisi/review documentale, nessun pilot tecnico avviato. Nessuna data di workshop ancora fissata.

**Raccomandazione della review esistente:** non avviare la pubblicazione in produzione. Prima completare le attività P0 (vedi sotto), chiarire il rapporto Prisma/SINAP e fissare modello di calendario e regole di propagazione; poi validare un pilot nel solo verso Prisma → Google.

**Attività P0 aperte (da fonte originale):**
1. Recuperare il DOCX tecnico e i thread Teams citati; raccogliere codice/prototipo e decisioni successive al 2024.
2. Verificare se Prisma è lo stesso sistema SINAP delle fonti 2024; identificare applicazione, owner e ambiente attuali.
3. Confermare il problema utente con 2-3 esempi reali di eventi Prisma da pubblicare su Google Calendar.
4. Definire il target Google del pilot (calendario personale collegato vs calendario condiviso dell'ente) e l'ente/account di test.

**Punti di attenzione principali:** identità e autorizzazioni (OAuth utente vs accesso applicativo), dati e privacy (quali campi evento escono da SINAP), coerenza (sistema autorevole, conflitti, fusi orari), continuità operativa (retry, limiti API, monitoraggio), gestione credenziali, costi/governance Google Workspace, validazione tecnica attuale (non riusare per assunto l'ipotesi 2024).

**Incontri già proposti nella review:** (1) Allineamento funzionale e priorità — 45 min; (2) Fattibilità tecnica e identità — 60 min; (3) Privacy, costi e decisione di avvio — 45 min.

## Idee proposte dall'agente

> Contenuto generato da questo agente (non dal cliente), da validare con il team prima di proporlo ad ARPAV. Approccio ispirato ai planner ENGenius (ANALYSIS, DESIGN) e alla disciplina di `impact` per la parte di assessment tecnico.

1. **Formalizzare il discovery come mini-assessment strutturato** prima del workshop 1: usare un formato BR/FR leggero (planner ENGenius `ANALYSIS`) per tradurre le evidenze email in requisiti verificabili, invece di partire direttamente dal workshop con informazioni ancora incerte.
2. **ADR esplicito su Prisma vs SINAP**: produrre un Architecture Decision Record che fissi la risposta alla domanda aperta #1, con impatto su tutto il resto dell'analisi — è bloccante e a basso costo da chiarire subito.
3. **Pilot "calendario condiviso per ente" come opzione di default**: rispetto al collegamento per singolo utente, riduce la superficie di consenso/revoca OAuth individuale e semplifica la governance Google Workspace lato ARPAV; da validare nel workshop 2.
4. **Contratto di integrazione versionato** (non solo "specifica funzionale"): definire fin da subito uno schema esplicito degli eventi/campi pubblicati (tipo contratto OpenAPI/JSON Schema), così la prova tecnica e il pilot condividono la stessa definizione e si riducono le sorprese in produzione.
5. **Criterio di uscita misurabile per il pilot**: proporre 2-3 metriche semplici (eventi pubblicati con successo, errori/retry, tempo di adozione da parte di un ente pilota) per decidere oggettivamente il go/no-go, invece di una valutazione solo qualitativa.
6. **Non sottovalutare l'alternativa `.ics`**: la review la cita già come confronto; vale la pena presentarla esplicitamente come opzione "a costo quasi zero" nel workshop 3, anche solo per giustificare meglio il valore incrementale dell'integrazione Google Calendar piena.
