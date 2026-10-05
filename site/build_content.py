#!/usr/bin/env python3
"""Costruisce site/data/content.json a partire dagli snapshot markdown
estratti da DocMind (progetto PreSales). Da rilanciare ogni volta che i
documenti DocMind vengono aggiornati, prima di rigenerare index.html.
"""
import json
from pathlib import Path
from datetime import datetime, timezone

RAW = Path("/tmp/raw")
OUT = Path(__file__).parent / "data" / "content.json"

def read(name):
    return (RAW / name).read_text(encoding="utf-8")

data = {
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "overview": {
        "uniqueName": "presales-overview",
        "displayName": "Presales - Panoramica Opportunità (mappa dei filoni)",
        "updatedAt": "2026-10-05T13:45:34.952546Z",
        "content": read("overview.md"),
    },
    "opportunities": [
        {
            "uniqueName": "presales-star-hotels",
            "displayName": "STAR HOTELS",
            "client": "Star Hotels",
            "macroAmbito": "PoC flow INLAY + Assessment enterprise Tech & Business",
            "status": "iniziale",
            "statusLabel": "Fase iniziale",
            "updatedAt": "2026-10-05T14:45:33.310932Z",
            "fileCount": 1,
            "content": read("star-hotels.md"),
        },
        {
            "uniqueName": "presales-miri",
            "displayName": "MILANO RISTORAZIONE",
            "client": "Milano Ristorazione (via Adesso.it)",
            "macroAmbito": "Portale ticketing MVP + integrazione Dynamics CRM",
            "status": "avanzata",
            "statusLabel": "Preparazione meeting tecnico",
            "updatedAt": "2026-10-05T13:46:51.75758Z",
            "fileCount": 4,
            "content": read("milano-ristorazione.md"),
        },
        {
            "uniqueName": "presales-arpav",
            "displayName": "ARPAV - Integrazione Google Calendar",
            "client": "ARPAV",
            "macroAmbito": "Integrazione calendari esterni (Prisma/SINAP → Google Calendar)",
            "status": "analisi",
            "statusLabel": "Analisi/review in corso",
            "updatedAt": "2026-10-05T13:46:11.049622Z",
            "fileCount": 3,
            "content": read("arpav.md"),
        },
        {
            "uniqueName": "presales-rcs",
            "displayName": "RCS - Rizzoli Corriere Della Sera",
            "client": "RCS",
            "macroAmbito": "Non ancora definito",
            "status": "vuota",
            "statusLabel": "Nessuna informazione disponibile",
            "updatedAt": "2026-10-05T13:47:32.001631Z",
            "fileCount": 0,
            "content": read("rcs.md"),
        },
    ],
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Scritto {OUT} ({OUT.stat().st_size} bytes)")
