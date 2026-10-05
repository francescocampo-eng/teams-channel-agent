"""Configurazione centrale dell'agente.

Legge i parametri da variabili d'ambiente (file .env in sviluppo).
Non contiene segreti hardcoded: client_id/tenant_id vanno forniti
tramite .env (vedi .env.example) una volta completata la checklist
Microsoft Entra ID (Milestone 2).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class GraphSettings:
    tenant_id: str | None = os.getenv("MS_TENANT_ID")
    client_id: str | None = os.getenv("MS_CLIENT_ID")
    # Device code flow: nessun client secret necessario per l'app pubblica.
    scopes: tuple[str, ...] = (
        "User.Read",
        "Team.ReadBasic.All",
        "Channel.ReadBasic.All",
        "ChannelMessage.Read.All",
    )
    graph_base_url: str = "https://graph.microsoft.com/v1.0"


@dataclass(frozen=True)
class LocalFilesSettings:
    # Cartelle autorizzate per la Modalità B (file locali).
    allowed_roots: tuple[Path, ...] = (PROJECT_ROOT,)


graph_settings = GraphSettings()
local_files_settings = LocalFilesSettings()
