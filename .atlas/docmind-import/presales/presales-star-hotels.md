---
unique-name: presales-star-hotels
display-name: Presales - Dettaglio Opportunità: STAR HOTELS
category: OPPORTUNITY_DRAFT
description: Corretto il modello di delivery INLAY: mai installato/consegnato al cliente, gira solo in casa ENG. PoC = lavorare internamente un asset del cliente con INLAY e mostrare solo l'output/capability, non il tool. Aggiornate le idee proposte (punti 1-3, 6, 8) di conseguenza.
---

# Presales — Dettaglio Opportunità: STAR HOTELS

> Fonte dati: file locale canale Teams (OneDrive sync). Documento sorgente: `summary.txt` (nota sintetica, 6 righe). Sezione "Idee proposte dall'agente" in fondo: contenuto generato, non proveniente dal cliente.

## Contesto: cos'è INLAY (verificato dalla documentazione ufficiale)

> Fonte: repository `DevExpPlatform/project-am-inlay-docs-portal` (documentazione INLAY Studio, letta direttamente dal repo scaricato dall'utente in locale). Aggiorna e sostituisce la nota precedente, basata solo su quanto riferito a voce.

**INLAY Studio** è la suite applicativa locale dell'azienda (container podman) che include **Atlas**: il motore di knowledge base che **sostituisce DocMind**. Atlas espone un MCP server HTTP (default porta **8010**, endpoint `http://localhost:8010/mcp`, nessuna autenticazione richiesta) con **22 tool**, da registrare a parte su GitHub Copilot CLI (config separata da quella usata da Inlay Studio stesso).

**Stato in questo ambiente: INLAY Studio/Atlas NON è installato** (verificato: `podman` non presente, porta 8010 non raggiungibile). Il PoC "flow INLAY" per Star Hotels richiede quindi, come prerequisito tecnico, prima l'installazione dello stack Inlay Studio.

**Migrazione progetti DocMind → Atlas** (per riferimento futuro, se si deciderà di migrare anche i progetti di questo agente): si applica solo a progetti la cui documentazione vive in un **repository git** con cartella `.docmind/` — si rinomina in `.atlas/`, si fa push, poi si importa il repo in Inlay Studio ("Importa da GitHub", selezionando il branch). I progetti DocMind di questo agente (`AgenteTeams`, `PreSales`) **non** seguono questo schema (vivono nel database di DocMind via MCP, non in una cartella di un repo git), quindi questa procedura di migrazione non si applica direttamente a loro.

**Implicazione per questa opportunità**: il PoC "flow INLAY" richiesto da Star Hotels è una dimostrazione del framework/suite interna INLAY (non un tool di terze parti). Prima di costruirlo serve: (1) installare Inlay Studio localmente, (2) verificare Atlas attivo (`podman ps`, `curl http://localhost:8010/health`), (3) opzionalmente registrare Atlas anche su Copilot CLI (`copilot mcp add --transport http atlas http://localhost:8010/mcp`) per poterlo interrogare da qui.

> ⚠️ **Vincolo non negoziabile sul modello di delivery INLAY**: INLAY gira **esclusivamente in casa nostra** (infrastruttura ENG). Non va **mai installato, distribuito o consegnato al cliente**, in nessuna forma (né come software, né come accesso diretto all'ambiente). Il PoC per il cliente consiste nel **prendere un asset del cliente** (es. un documento, uno screen, un dataset, un processo) **e lavorarlo internamente con INLAY**, per poi mostrare al cliente solo il **risultato prodotto** e le **capability dimostrate**. Il messaggio di vendita non è "vi diamo l'AI" (ce l'hanno già tutti), ma "abbiamo sviluppato una suite proprietaria che ci dà vantaggi di velocità/qualità e vi dà garanzie — di sicurezza, tracciabilità, controllo — che un tool generico non offre, perché resta sotto il nostro controllo diretto". Questo vincolo si applica a ogni opportunità in cui si proponga INLAY, non solo a Star Hotels.

## Perimetro e scopo

Due filoni distinti, entrambi in fase iniziale:
1. **PoC di un flow INLAY** su una componente scelta dal cliente (perimetro tecnico ancora da definire).
2. **Assessment enterprise Tech & Business**: valutazione combinata tecnica e di business su un perimetro che deve ancora essere definito dal cliente, da realizzare con il supporto dell'**Assessment Estimator**.

Perimetro non ancora delimitato in dettaglio: non è noto quale componente verrà scelta per il PoC INLAY, né quale sarà l'ampiezza esatta (quante funzioni/sistemi aziendali) dell'assessment enterprise.

## Richiesta cliente

A seguito di una presentazione della metodologia/piattaforma **INLAY**, Star Hotels ha chiesto:
- una **proof of concept** del flow INLAY applicato a una componente a propria scelta;
- una **proposta con stima** per un assessment enterprise che copra sia l'ambito tecnico sia quello di business, utilizzando l'Assessment Estimator come strumento di stima.

Obiettivo dichiarato dal cliente: ottenere entro **fine 2026** una timeline e un budget di programma, a valle di un journey che illustri l'approccio e porti alla commissione formale dell'assessment.

## Stato

**Fase:** molto iniziale. Nessun documento di scoping ricevuto dal cliente oltre alla nota sintetica; il perimetro dell'assessment è esplicitamente "da definire dal cliente". Non risultano ancora fissati workshop, date o referenti. **Inlay Studio/Atlas non è ancora installato in questo ambiente**: è un prerequisito da chiudere prima del PoC.

**Rischio principale:** procedere a stimare/proporre senza un perimetro condiviso rischia di produrre una proposta generica poco vincolante per il cliente.

## Idee proposte dall'agente

> Contenuto generato da questo agente (non dal cliente), da validare prima di presentarlo a Star Hotels. Approccio basato sulle skill `ui-ux-pro-max` (per lavorare l'asset del cliente durante il PoC INLAY), `proposal-writing` (in particolare il profilo settoriale hospitality) e `impact` (per l'assessment tecnico enterprise). **Corretto rispetto alla versione precedente**: INLAY non viene mai installato, distribuito o lasciato in mano al cliente — resta sempre eseguito internamente da ENG, e al cliente viene mostrato solo l'output prodotto.

1. **Chiedere al cliente un asset reale su cui lavorare** (es. una schermata/flusso del percorso ospite, un documento di processo, un set di dati non sensibili) **da usare come caso concreto per il PoC**: l'asset viene acquisito e lavorato **internamente** con INLAY (es. con la skill `ui-ux-pro-max` per ricostruire/migliorare una componente UI), senza mai installare o esporre INLAY al cliente.
2. **Presentare il PoC come demo dell'output, non del tool**: nel readout mostrare solo il "prima/dopo" sull'asset del cliente (es. mockup migliorato, analisi prodotta, documento arricchito) e i vantaggi misurabili (velocità, qualità, coerenza), senza accesso diretto del cliente a INLAY — la narrativa è "ecco cosa siamo in grado di fare per voi", non "ecco lo strumento che usiamo".
3. **Usare la skill `impact` (modalità "how" o "how-deepdive") sul sistema enterprise esistente del cliente, se accessibile**, per produrre internamente un'anteprima dell'approccio di assessment tecnico (architettura, debito tecnico, entry point): anche qui il cliente riceve solo il **documento di output**, mai accesso diretto agli strumenti usati per produrlo — dà credibilità all'Assessment Estimator.
4. **Costruire la proposta con la skill `proposal-writing`, sezione profili settoriali (hospitality)**: strutturare il documento di proposta seguendo un formato già tarato sul settore alberghiero, per rendere il linguaggio e i casi d'uso immediatamente riconoscibili dal cliente invece di partire da un template generico.
5. **Proporre un workshop di scoping preliminare (1 incontro, 2h) dedicato esclusivamente a delimitare il perimetro dell'assessment enterprise**, prima di qualunque stima: dato che il cliente stesso deve ancora definire l'ambito, offrire un metodo guidato (es. canvas di scoping per dominio/processo aziendale) accelera questa decisione invece di aspettarla passivamente. In questa sede si può anche raccogliere formalmente l'asset da usare per il PoC (punto 1).
6. **Collegare esplicitamente PoC INLAY e Assessment enterprise in un'unica narrativa**: presentare il PoC come "capitolo 0" dell'assessment (dimostra il metodo su piccola scala, sull'asset del cliente lavorato internamente) per aumentare la probabilità che il cliente commissioni l'assessment completo, sfruttando il momentum della demo — mantenendo sempre chiaro che il valore è nel risultato e nel metodo proprietario ENG, non nella cessione di un tool.
7. **Definire già ora 2-3 opzioni di pacchetto per l'assessment** (es. ambito ridotto/medio/ampio con relativa stima a range), da presentare nel journey verso fine 2026, così il cliente può decidere rapidamente il livello di investimento senza dover negoziare da zero il perimetro.
8. **Installare Inlay Studio/Atlas come primo passo tecnico abilitante** (solo in ambiente ENG, mai lato cliente): senza lo stack attivo non è possibile lavorare l'asset del cliente né produrre l'output del PoC; priorità operativa prima di qualunque altro passo su questa opportunità.
