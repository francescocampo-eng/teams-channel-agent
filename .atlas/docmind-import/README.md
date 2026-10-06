# Documenti migrati da DocMind — guida per Inlay Studio

Questa cartella raccoglie i documenti esportati dai progetti **DocMind** usati
finora per il lavoro presales/teams-channel-agent, migrati qui secondo la
convenzione di Inlay Studio: Atlas indicizza solo i file `.md` dentro `.atlas/`
(vedi [Importa un progetto da DocMind](https://jubilant-couscous-o8ypm21.pages.github.io/docs/inlay-studio/user-manual/import-docmind)).

## Origine

| Cartella qui | Progetto DocMind originale | Documenti | Note |
|---|---|---|---|
| `agenteteams/` | **AgenteTeams** (id 35) | `teams-channel-agent-concept.md`, `presales-site-render-guide.md` | Concept/architettura dell'agente Ciro e guida al rendering del sito statico. |
| `presales/` | **PreSales** | `presales-overview.md`, `presales-miri.md`, `presales-star-hotels.md`, `presales-arpav.md`, `presales-rcs.md` | Dettaglio delle singole opportunità presales (una per cliente) + panoramica generale. |

Export generati il 2026-10-06 (manifest originali con `uniqueName`, categoria,
embeddings e timestamp disponibili nei file `manifest.json` dell'export, non
copiati qui perché Atlas ricalcola i propri embeddings all'import).

## Come usarli in Inlay Studio

1. Apri il progetto `teams-channel-agent` già importato in Inlay Studio.
2. Vai in **Fonti → GitHub → Sincronizza/Pull** (o ripeti l'import se il
   progetto non supporta ancora il pull incrementale) per scaricare questi
   nuovi file da `.atlas/docmind-import/`.
3. Lascia **Calcola embeddings** attivo per renderli subito interrogabili
   dalla Chat.
4. In Chat puoi riferirti a questi documenti per nome (es. *"leggi
   docmind-import/presales/presales-miri.md e riassumi lo stato
   dell'opportunità"*).

## Nota su "Ciro"

Il file `../ciro_persona.md` (nella root di `.atlas/`) descrive l'identità e
il tono dell'agente Ciro: va usato come **Istruzioni di progetto** (system
prompt) nella Chat, non è un workflow/comando. I documenti di questa cartella
sono invece il **contenuto** su cui Ciro lavora (opportunità presales,
concept/architettura del sito).
