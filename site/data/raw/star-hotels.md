# Presales — Dettaglio Opportunità: STAR HOTELS

> Fonte dati: file locale canale Teams (OneDrive sync). Documento sorgente: [summary.txt](https://engit.sharepoint.com/:t:/r/sites/DeliveryFactoryA-PreSalesandOpptys/Documenti%20condivisi/PreSales/STAR%20HOTELS/summary.txt?d=we208c200da614d7c9973afdcffe1358a&csf=1&web=1&e=d5nFEd) (nota sintetica, 6 righe). Sezione "Idee proposte dall'agente" in fondo: contenuto generato, non proveniente dal cliente.

## Contesto: cos'è INLAY (verificato dalla documentazione ufficiale)

> Fonte: repository `DevExpPlatform/project-am-inlay-docs-portal` (documentazione INLAY Studio, letta direttamente dal repo scaricato dall'utente in locale). Aggiorna e sostituisce la nota precedente, basata solo su quanto riferito a voce.

**INLAY Studio** è la suite applicativa locale dell'azienda (container podman) che include **Atlas**: il motore di knowledge base che **sostituisce DocMind**. Atlas espone un MCP server HTTP (default porta **8010**, endpoint `http://localhost:8010/mcp`, nessuna autenticazione richiesta) con **22 tool**, da registrare a parte su GitHub Copilot CLI (config separata da quella usata da Inlay Studio stesso).

**Stato in questo ambiente: INLAY Studio/Atlas NON è installato** (verificato: `podman` non presente, porta 8010 non raggiungibile). Il PoC "flow INLAY" per Star Hotels richiede quindi, come prerequisito tecnico, prima l'installazione dello stack Inlay Studio.

**Migrazione progetti DocMind → Atlas** (per riferimento futuro): si applica solo a progetti la cui documentazione vive in un **repository git** con cartella `.docmind/` — si rinomina in `.atlas/`, si fa push, poi si importa il repo in Inlay Studio ("Importa da GitHub"). I progetti DocMind di questo agente (`AgenteTeams`, `PreSales`) **non** seguono questo schema, quindi questa procedura non si applica direttamente a loro.

> ⚠️ **Vincolo non negoziabile sul modello di delivery INLAY**: INLAY gira **esclusivamente in casa nostra** (infrastruttura ENG). Non va **mai installato, distribuito o consegnato al cliente**, in nessuna forma. Il PoC per il cliente consiste nel **prendere un asset del cliente** e **lavorarlo internamente con INLAY**, per poi mostrare al cliente solo il **risultato prodotto** e le **capability dimostrate**. Il messaggio di vendita non è "vi diamo l'AI" (ce l'hanno già tutti), ma "abbiamo sviluppato una suite proprietaria che ci dà vantaggi di velocità/qualità e vi dà garanzie — di sicurezza, tracciabilità, controllo — che un tool generico non offre". Questo vincolo si applica a ogni opportunità in cui si proponga INLAY.

## Perimetro e scopo

Due filoni distinti, entrambi in fase iniziale:
1. **PoC di un flow INLAY** su una componente scelta dal cliente (perimetro tecnico ancora da definire).
2. **Assessment enterprise Tech & Business**: valutazione combinata tecnica e di business su un perimetro che deve ancora essere definito dal cliente, da realizzare con il supporto dell'**Assessment Estimator**.

Perimetro non ancora delimitato in dettaglio: non è noto quale componente verrà scelta per il PoC INLAY, né quale sarà l'ampiezza esatta dell'assessment enterprise.

## Richiesta cliente

A seguito di una presentazione della metodologia/piattaforma **INLAY**, Star Hotels ha chiesto:
- una **proof of concept** del flow INLAY applicato a una componente a propria scelta;
- una **proposta con stima** per un assessment enterprise che copra sia l'ambito tecnico sia quello di business, utilizzando l'Assessment Estimator come strumento di stima.

Obiettivo dichiarato dal cliente: ottenere entro **fine 2026** una timeline e un budget di programma, a valle di un journey che illustri l'approccio e porti alla commissione formale dell'assessment.

## Stato

**Fase:** molto iniziale. Nessun documento di scoping ricevuto dal cliente oltre alla nota sintetica; il perimetro dell'assessment è esplicitamente "da definire dal cliente". Non risultano ancora fissati workshop, date o referenti. **Inlay Studio/Atlas non è ancora installato in questo ambiente**: è un prerequisito da chiudere prima del PoC.

**Rischio principale:** procedere a stimare/proporre senza un perimetro condiviso rischia di produrre una proposta generica poco vincolante per il cliente.

## Idee proposte dall'agente

> Contenuto generato da questo agente (non dal cliente), da validare prima di presentarlo a Star Hotels.

1. **Chiedere al cliente un asset reale su cui lavorare** da usare come caso concreto per il PoC: l'asset viene acquisito e lavorato **internamente** con INLAY, senza mai installare o esporre INLAY al cliente.
2. **Presentare il PoC come demo dell'output, non del tool**: mostrare solo il "prima/dopo" sull'asset del cliente e i vantaggi misurabili, senza accesso diretto del cliente a INLAY.
3. **Usare la skill `impact`** sul sistema enterprise esistente del cliente, se accessibile, per produrre internamente un'anteprima dell'approccio di assessment tecnico — dà credibilità all'Assessment Estimator.
4. **Costruire la proposta con la skill `proposal-writing`**, profilo settoriale hospitality.
5. **Proporre un workshop di scoping preliminare (1 incontro, 2h)** dedicato a delimitare il perimetro dell'assessment enterprise e a raccogliere l'asset per il PoC.
6. **Collegare esplicitamente PoC INLAY e Assessment enterprise** in un'unica narrativa ("capitolo 0").
7. **Definire già ora 2-3 opzioni di pacchetto** per l'assessment (ambito ridotto/medio/ampio).
8. **Installare Inlay Studio/Atlas come primo passo tecnico abilitante** (solo in ambiente ENG, mai lato cliente).
