"""Accesso controllato alle cartelle locali (Modalità B del progetto).

Fonti coperte:
- cartelle di progetto (PROJECT_ROOT);
- cartella del canale Teams sincronizzata via OneDrive
  (TEAMS_CHANNEL_FILES_PATH), organizzata per opportunità: ogni
  sottocartella di primo livello = una opportunità/commessa.

Ogni funzione valida che il percorso richiesto sia contenuto in una delle
`allowed_roots` configurate, per evitare letture fuori dal perimetro
autorizzato (path traversal).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..config import local_files_settings


class PathNotAllowedError(Exception):
    """Sollevata quando un percorso richiesto non è in una allowed_root."""


def _ensure_allowed(path: Path) -> Path:
    resolved = path.resolve()
    for root in local_files_settings.allowed_roots:
        root_resolved = root.resolve()
        if resolved == root_resolved or root_resolved in resolved.parents:
            return resolved
    raise PathNotAllowedError(f"Percorso non autorizzato: {resolved}")


@dataclass(frozen=True)
class Opportunity:
    name: str
    path: Path


def list_opportunities() -> list[Opportunity]:
    """Elenca le opportunità (sottocartelle di primo livello) presenti
    nella cartella del canale Teams sincronizzata."""
    root = _ensure_allowed(local_files_settings.opportunities_root)
    if not root.exists():
        return []
    return sorted(
        (
            Opportunity(name=p.name, path=p)
            for p in root.iterdir()
            if p.is_dir() and not p.name.startswith(".")
        ),
        key=lambda o: o.name.lower(),
    )


def list_files(opportunity_name: str, pattern: str = "**/*") -> list[Path]:
    """Elenca i file (ricorsivamente) dentro la cartella di una opportunità."""
    root = _ensure_allowed(local_files_settings.opportunities_root)
    target = _ensure_allowed(root / opportunity_name)
    if not target.exists():
        raise FileNotFoundError(f"Opportunità non trovata: {opportunity_name}")
    return sorted(p for p in target.glob(pattern) if p.is_file())


def read_text_file(path: Path, max_bytes: int = 2_000_000) -> str:
    """Legge un file di testo, con limite dimensionale di sicurezza."""
    resolved = _ensure_allowed(Path(path))
    if not resolved.is_file():
        raise FileNotFoundError(f"File non trovato: {resolved}")
    if resolved.stat().st_size > max_bytes:
        raise ValueError(
            f"File troppo grande ({resolved.stat().st_size} byte > {max_bytes})"
        )
    return resolved.read_text(encoding="utf-8", errors="replace")
