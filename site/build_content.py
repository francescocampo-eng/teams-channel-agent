#!/usr/bin/env python3
"""Costruisce site/data/content.json a partire dagli snapshot markdown
in site/data/raw/*.md (riflettono il contenuto dei documenti DocMind del
progetto PreSales). Da rilanciare ogni volta che quei file .md vengono
aggiornati, prima di rigenerare index.html con generate_site.py.

La data di "ultimo aggiornamento dati" di ogni opportunità è derivata
automaticamente dal mtime del relativo file .md: non serve mantenerla a
mano, basta sovrascrivere il file quando il documento DocMind cambia.
"""
import json
from pathlib import Path
from datetime import datetime, timezone

RAW = Path(__file__).parent / "data" / "raw"
OUT = Path(__file__).parent / "data" / "content.json"


def read(name: str) -> str:
    return (RAW / name).read_text(encoding="utf-8")


def mtime_iso(name: str) -> str:
    ts = (RAW / name).stat().st_mtime
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


FILES = {
    "overview": "overview.md",
    "presales-star-hotels": "star-hotels.md",
    "presales-miri": "milano-ristorazione.md",
    "presales-arpav": "arpav.md",
    "presales-rcs": "rcs.md",
}

OPPS_META = [
    {
        "uniqueName": "presales-star-hotels",
        "displayName": "STAR HOTELS",
        "client": "Star Hotels",
        "macroAmbito": "PoC flow INLAY + Assessment enterprise Tech & Business",
        "status": "iniziale",
        "statusLabel": "Fase iniziale",
        "fileCount": 1,
    },
    {
        "uniqueName": "presales-miri",
        "displayName": "MILANO RISTORAZIONE",
        "client": "Milano Ristorazione (via Adesso.it)",
        "macroAmbito": "Portale ticketing MVP + integrazione Dynamics CRM",
        "status": "avanzata",
        "statusLabel": "Preparazione meeting tecnico",
        "fileCount": 4,
    },
    {
        "uniqueName": "presales-arpav",
        "displayName": "ARPAV - Integrazione Google Calendar",
        "client": "ARPAV",
        "macroAmbito": "Integrazione calendari esterni (Prisma/SINAP → Google Calendar)",
        "status": "analisi",
        "statusLabel": "Analisi/review in corso",
        "fileCount": 3,
    },
    {
        "uniqueName": "presales-rcs",
        "displayName": "RCS - Rizzoli Corriere Della Sera",
        "client": "RCS",
        "macroAmbito": "Non ancora definito",
        "status": "vuota",
        "statusLabel": "Nessuna informazione disponibile",
        "fileCount": 0,
    },
]

opportunities = []
all_updated = []
for meta in OPPS_META:
    fname = FILES[meta["uniqueName"]]
    updated = mtime_iso(fname)
    all_updated.append(updated)
    opportunities.append({**meta, "updatedAt": updated, "content": read(fname)})

overview_updated = mtime_iso(FILES["overview"])
all_updated.append(overview_updated)

data = {
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "dataUpdatedAt": max(all_updated),
    "overview": {
        "uniqueName": "presales-overview",
        "displayName": "Presales - Panoramica Opportunità (mappa dei filoni)",
        "updatedAt": overview_updated,
        "content": read(FILES["overview"]),
    },
    "opportunities": opportunities,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Scritto {OUT} ({OUT.stat().st_size} bytes)")
