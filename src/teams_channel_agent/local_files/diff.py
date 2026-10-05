"""Rilevamento differenze nelle cartelle opportunità (canale Teams via
OneDrive sync).

Mantiene uno snapshot JSON (`output/opportunities_snapshot.json`, non
versionato) con {opportunità: {percorso_relativo: {size, mtime}}}.
Ogni scan confronta lo stato attuale con l'ultimo snapshot salvato e
restituisce cosa è cambiato, senza mai scrivere nelle cartelle sorgente
(sola lettura).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from ..config import PROJECT_ROOT
from .browser import list_files, list_opportunities

SNAPSHOT_PATH = PROJECT_ROOT / "output" / "opportunities_snapshot.json"


@dataclass
class OpportunityDiff:
    new_opportunities: list[str] = field(default_factory=list)
    removed_opportunities: list[str] = field(default_factory=list)
    new_files: dict[str, list[str]] = field(default_factory=dict)
    modified_files: dict[str, list[str]] = field(default_factory=dict)
    removed_files: dict[str, list[str]] = field(default_factory=dict)

    @property
    def has_changes(self) -> bool:
        return any(
            [
                self.new_opportunities,
                self.removed_opportunities,
                self.new_files,
                self.modified_files,
                self.removed_files,
            ]
        )


def _current_snapshot() -> dict:
    snapshot: dict = {}
    for opp in list_opportunities():
        files = {}
        for f in list_files(opp.name):
            try:
                stat = f.stat()
            except OSError:
                continue
            rel = str(f.relative_to(opp.path))
            files[rel] = {"size": stat.st_size, "mtime": int(stat.st_mtime)}
        snapshot[opp.name] = files
    return snapshot


def _load_previous_snapshot() -> dict:
    if not SNAPSHOT_PATH.exists():
        return {}
    return json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))


def _save_snapshot(snapshot: dict) -> None:
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def scan(persist: bool = True) -> OpportunityDiff:
    """Esegue lo scan, calcola il diff rispetto all'ultimo snapshot salvato
    e (se persist=True) aggiorna lo snapshot su disco."""
    previous = _load_previous_snapshot()
    current = _current_snapshot()

    diff = OpportunityDiff()
    diff.new_opportunities = sorted(set(current) - set(previous))
    diff.removed_opportunities = sorted(set(previous) - set(current))

    for opp_name, files in current.items():
        prev_files = previous.get(opp_name, {})
        new = sorted(set(files) - set(prev_files))
        removed = sorted(set(prev_files) - set(files))
        modified = sorted(
            rel
            for rel in set(files) & set(prev_files)
            if files[rel] != prev_files[rel]
        )
        if new:
            diff.new_files[opp_name] = new
        if removed:
            diff.removed_files[opp_name] = removed
        if modified:
            diff.modified_files[opp_name] = modified

    if persist:
        _save_snapshot(current)

    return diff
