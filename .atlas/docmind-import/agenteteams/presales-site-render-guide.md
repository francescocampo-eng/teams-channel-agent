---
unique-name: presales-site-render-guide
display-name: Guida: pagina HTML "PreSales Opportunity" (rendering DocMind)
category: TECHNICAL_GUIDE
description: Spiega la pagina HTML statica site/index.html che visualizza i documenti DocMind del progetto PreSales (overview + 4 dettagli opportunità): struttura file, design, come rigenerarla quando i documenti cambiano.
---

# Guida: pagina HTML "PreSales Opportunity" (sito statico di rendering DocMind)

> Fonte: file locale del progetto `teams-channel-agent` (`site/`). Documento di guida creato dall'agente per spiegare la pagina HTML di presentazione delle opportunità presales e come rigenerarla.

## Cos'è

Una singola pagina HTML standalone (`site/index.html`) che presenta in forma visuale ("piramide": panoramica in cima, dettaglio opportunità alla base) il contenuto dei 5 documenti DocMind del progetto **PreSales**:
- `presales-overview` (mappa generale dei filoni)
- `presales-star-hotels`, `presales-miri`, `presales-arpav`, `presales-rcs` (dettaglio per singola opportunità)

La pagina è **self-contained**: CSS e JS sono inline, i contenuti sono incorporati staticamente nell'HTML generato (nessuna chiamata a DocMind dal browser). Si apre con un doppio click (`file://`) o servendola con un server statico qualsiasi.

## Design

Palette ispirata al sito istituzionale ENG (Science Blue `#0073CE`, Midnight Blue `#003170`) su sfondo scuro, tipografia Fraunces (titoli) + Inter (testo) + IBM Plex Mono (dettagli tecnici). Stile e pattern di animazione (hero a tutta pagina, scroll-reveal, header che si solidifica allo scroll, progress bar, card ad accordion) ispirati a `mimmoai.com` e `brandmaxstudio.agency`, costruiti con la skill `ui-ux-pro-max` già installata in locale.

## Struttura dei file (`teams-channel-agent/site/`)

| File | Ruolo |
|---|---|
| `template.html` | Template HTML/CSS/JS statico, con placeholder (`__OVERVIEW_BLOCK__`, `__OPP_CARDS__`, `__N_OPPS__`, `__N_FILES__`, `__GENERATED_AT__`) |
| `build_content.py` | Legge gli snapshot markdown (sorgente: contenuto dei documenti DocMind del progetto PreSales) e scrive `data/content.json` |
| `data/content.json` | Snapshot strutturato dei 5 documenti (overview + 4 dettagli), con metadati (cliente, stato, numero file, data aggiornamento) |
| `generate_site.py` | Legge `data/content.json`, converte il markdown di ogni documento in HTML, lo inserisce nel template, scrive `index.html` |
| `index.html` | **Output finale**, pronto da aprire nel browser o pubblicare |

## Come rigenerare la pagina quando i documenti DocMind cambiano

1. Recuperare il contenuto aggiornato dei documenti DocMind del progetto PreSales (`docmind-getFlavorByName` per ciascun `uniqueName`: `presales-overview`, `presales-star-hotels`, `presales-miri`, `presales-arpav`, `presales-rcs`).
2. Aggiornare i file markdown sorgente usati da `build_content.py` (attualmente letti da `/tmp/raw/*.md` in sessione; valutare, se si vuole rendere il processo più stabile, di spostarli dentro `site/data/raw/` nel repo, cosa consigliata come miglioramento futuro).
3. Eseguire `python3 site/build_content.py` per rigenerare `site/data/content.json`.
4. Eseguire `python3 site/generate_site.py` per rigenerare `site/index.html`.
5. Aprire `site/index.html` per verificare il risultato.

**Nota:** questo processo di rigenerazione non è (ancora) collegato automaticamente allo script di automazione `scripts/presales_autoupdate.sh` (quello che aggiorna i documenti DocMind da cron). Oggi sono due passi distinti: (a) l'automazione cron aggiorna DocMind, (b) la rigenerazione della pagina HTML va lanciata manualmente quando si vuole un refresh della vista visuale. Collegare i due passi in un'unica pipeline è un possibile miglioramento futuro, da valutare solo se utile nella pratica (principio di minima complessità).

## Dipendenze

- Python 3 con il pacchetto `markdown` (`pip install markdown`), usato per convertire ogni sezione markdown in HTML.
- Nessuna dipendenza JavaScript esterna: il font è caricato da Google Fonts via CDN (richiede connessione internet per il rendering tipografico ottimale; in assenza di rete la pagina resta leggibile con i font di sistema).

## Principi seguiti

- Nessuna menzione esplicita del percorso di cartella locale nella pagina: si parla genericamente di "cartella collegata al canale PreSales".
- Le idee proposte dall'agente restano sempre etichettate come tali nel contenuto (ereditato dai documenti DocMind sorgente).
- Nessun nuovo MCP, database o servizio introdotto: la pagina è un artefatto statico generato da script Python locali, in linea con il principio di minima complessità del progetto.
