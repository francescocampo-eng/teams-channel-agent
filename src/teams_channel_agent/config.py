"""Configurazione centrale dell'agente.

Legge i parametri da variabili d'ambiente (file .env in sviluppo).
Non contiene segreti hardcoded: client_id/tenant_id vanno forniti
tramite .env (vedi .env.example) una volta completata la checklist
Microsoft Entra ID (Milestone 2).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# Client ID pubblico multi-tenant ufficiale Microsoft ("Microsoft Graph
# Command Line Tools"). Usato come fallback quando non è possibile
# registrare una app dedicata su Entra ID (tenant con policy
# "Users can register applications" = No). Vedi Milestone 2/3 nel
# documento di concept (DocMind, progetto AgenteTeams) per i dettagli
# del blocco riscontrato e la decisione presa.
MS_GRAPH_CLI_TOOLS_CLIENT_ID = "14d82eec-204b-4c2f-b7e8-296a70dab67e"


@dataclass(frozen=True)
class GraphSettings:
    tenant_id: str = os.getenv("MS_TENANT_ID", "organizations")
    client_id: str = os.getenv("MS_CLIENT_ID", MS_GRAPH_CLI_TOOLS_CLIENT_ID)
    # Device code flow: nessun client secret necessario per l'app pubblica.
    # Scope minimo per il primo test di autenticazione (Milestone 3).
    # Gli scope Teams verranno aggiunti quando il consenso admin sarà
    # disponibile (vedi Milestone 2).
    scopes: tuple[str, ...] = tuple(
        s.strip()
        for s in os.getenv("MS_GRAPH_SCOPES", "User.Read").split(",")
        if s.strip()
    )
    graph_base_url: str = "https://graph.microsoft.com/v1.0"
    authority: str = field(init=False, default="")

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "authority", f"https://login.microsoftonline.com/{self.tenant_id}"
        )


# Cartella canale Teams sincronizzata via OneDrive (Windows) e letta da WSL.
# Bypassa Microsoft Graph per l'accesso ai FILE del canale, a causa del
# blocco Conditional Access riscontrato in Milestone 3 (vedi documento di
# concept, DocMind progetto AgenteTeams). Non copre i messaggi di chat:
# quelli restano bloccati finché Graph/Teams non sarà sbloccato dall'IT.
TEAMS_CHANNEL_FILES_PATH = Path(
    os.getenv(
        "TEAMS_CHANNEL_FILES_PATH",
        "/mnt/c/Users/fcampo/OneDrive - Engineering Ingegneria Informatica S.p.A/"
        "Delivery Factory A - PreSales and Opptys - PreSales",
    )
)


@dataclass(frozen=True)
class LocalFilesSettings:
    # Cartelle autorizzate per la Modalità B (file locali).
    allowed_roots: tuple[Path, ...] = (PROJECT_ROOT, TEAMS_CHANNEL_FILES_PATH)
    # Sotto TEAMS_CHANNEL_FILES_PATH ogni sottocartella di primo livello
    # rappresenta una opportunità/commessa (es. "RCS - Rizzoli Corriere
    # Della Sera", "STAR HOTELS", ...).
    opportunities_root: Path = TEAMS_CHANNEL_FILES_PATH


graph_settings = GraphSettings()
local_files_settings = LocalFilesSettings()
