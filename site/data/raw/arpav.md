# Presales — Dettaglio Opportunità: ARPAV - Integrazione Google Calendar

> Fonte dati: file locale canale Teams (OneDrive sync). Documento sorgente originale: [Review-opportunita-calendari-esterni-SINAP.md](https://engit.sharepoint.com/:t:/r/sites/DeliveryFactoryA-PreSalesandOpptys/Documenti%20condivisi/PreSales/ARPAV%20-%20Integrazione%20Google%20Calendar/Review-opportunita-calendari-esterni-SINAP.md?d=w54d6b90e830242febc89a64b93a76cdb&csf=1&web=1&e=rz5eBX) (review del 2 ottobre 2026, basata sul corpo testuale di una email del 1 ottobre 2026; un [PDF Outlook allegato](https://engit.sharepoint.com/:b:/r/sites/DeliveryFactoryA-PreSalesandOpptys/Documenti%20condivisi/PreSales/ARPAV%20-%20Integrazione%20Google%20Calendar/%5BARPAV%5D%5BCheckAP_exSINAP%5D%20-%20analisi%20su%20c...outlook)%20-%20Domenico%20La%20Rocca%20-%20Outlook.pdf?d=w528e1378ab434ad5b23b36b59b8d22e8&csf=1&web=1&e=S3qHBe) (e la relativa [email originale .eml](https://engit.sharepoint.com/:u:/r/sites/DeliveryFactoryA-PreSalesandOpptys/Documenti%20condivisi/PreSales/ARPAV%20-%20Integrazione%20Google%20Calendar/%5BARPAV%5D%5BCheckAP_exSINAP%5D%20-%20analisi%20su%20connessione%20a%20calendari%20esterni%20(google%20calendar%20e_o%20outlook).eml?d=w0a14bdf60a1e490493eb32dcbf31eaf9&csf=1&web=1&e=471zLl)) non è stato estratto). Sezione "Idee proposte dall'agente" in fondo: contenuto generato, non proveniente dal cliente.

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

**Raccomandazione della review esistente:** non avviare la pubblicazione in produzione. Prima completare le attività P0, chiarire il rapporto Prisma/SINAP e fissare modello di calendario e regole di propagazione; poi validare un pilot nel solo verso Prisma → Google.

**Attività P0 aperte (da fonte originale):**
1. Recuperare il DOCX tecnico e i thread Teams citati; raccogliere codice/prototipo e decisioni successive al 2024.
2. Verificare se Prisma è lo stesso sistema SINAP delle fonti 2024; identificare applicazione, owner e ambiente attuali.
3. Confermare il problema utente con 2-3 esempi reali di eventi Prisma da pubblicare su Google Calendar.
4. Definire il target Google del pilot (calendario personale collegato vs calendario condiviso dell'ente) e l'ente/account di test.

**Punti di attenzione principali:** identità e autorizzazioni (OAuth utente vs accesso applicativo), dati e privacy (quali campi evento escono da SINAP), coerenza (sistema autorevole, conflitti, fusi orari), continuità operativa (retry, limiti API, monitoraggio), gestione credenziali, costi/governance Google Workspace, validazione tecnica attuale.

**Incontri già proposti nella review:** (1) Allineamento funzionale e priorità — 45 min; (2) Fattibilità tecnica e identità — 60 min; (3) Privacy, costi e decisione di avvio — 45 min.

## Idee proposte dall'agente

> Contenuto generato da questo agente (non dal cliente), da validare con il team prima di proporlo ad ARPAV. Approccio ispirato ai planner ENGenius (ANALYSIS, DESIGN) e alla disciplina di `impact` per la parte di assessment tecnico.

1. **Formalizzare il discovery come mini-assessment strutturato** prima del workshop 1: usare un formato BR/FR leggero (planner ENGenius `ANALYSIS`).
2. **ADR esplicito su Prisma vs SINAP**: produrre un Architecture Decision Record — è bloccante e a basso costo da chiarire subito.
3. **Pilot "calendario condiviso per ente" come opzione di default**: riduce la superficie di consenso/revoca OAuth individuale.
4. **Contratto di integrazione versionato** (schema esplicito tipo OpenAPI/JSON Schema), così prova tecnica e pilot condividono la stessa definizione.
5. **Criterio di uscita misurabile per il pilot**: 2-3 metriche semplici per decidere il go/no-go.
6. **Non sottovalutare l'alternativa `.ics`**: presentarla come opzione "a costo quasi zero" nel workshop 3.
