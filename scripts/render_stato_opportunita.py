#!/usr/bin/env python3
"""Genera .atlas/stato_opportunita.md (snapshot leggibile in Markdown) a
partire da data/presales_milestones.json, che e' JSON e quindi non
indicizzabile direttamente da Atlas (indicizza solo .md). Questo file e'
SOLO una fotografia di lettura per la Chat RAG dentro Inlay Studio: la
fonte di verita' resta data/presales_milestones.json, aggiornato e
letto/scritto solo con Terminale attivo (repo completo), mai editando
questo snapshot a mano.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "presales_milestones.json"
OUT = ROOT / ".atlas" / "stato_opportunita.md"


def render(data: dict) -> str:
    lines = [
        "# Stato opportunità presales — snapshot di sola lettura",
        "",
        "> Generato automaticamente da `data/presales_milestones.json` via",
        "> `scripts/render_stato_opportunita.py` (chiamato da `scripts/sync_atlas.sh`).",
        "> Non editare questo file a mano: viene sovrascritto. Per aggiornare lo",
        "> stato reale serve il Terminale (repo completo), non la sola Chat RAG.",
        "",
    ]
    for slug, opp in data.items():
        lines.append(f"## {opp.get('nome', slug)} (`{slug}`)")
        lines.append("")
        lines.append(f"- **Stato**: {opp.get('stato')}")
        lines.append(f"- **Esito**: {opp.get('esito') or 'in corso (nessun esito registrato)'}")
        deadline = opp.get("deadline")
        if deadline:
            lines.append(f"- **Deadline**: {deadline} — {opp.get('deadline_descrizione') or ''}")
        if opp.get("in_attesa_di"):
            lines.append(f"- **In attesa di**: {opp['in_attesa_di']}")
        if opp.get("note"):
            lines.append(f"- **Note**: {opp['note']}")
        lines.append(f"- **Ultimo aggiornamento**: {opp.get('ultimo_aggiornamento')}")

        impegni = opp.get("impegni") or []
        if impegni:
            lines.append("")
            lines.append("**Impegni/calendario:**")
            for imp in impegni:
                lines.append(f"- {imp.get('data')} — {imp.get('titolo')} ({imp.get('tipo')})")

        storico = opp.get("storico") or []
        if storico:
            lines.append("")
            lines.append("**Storico passaggi di stato:**")
            for h in storico:
                econ = h.get("economics")
                econ_txt = f" — economics: {econ}" if econ else ""
                lines.append(f"- {h.get('data')} → {h.get('stato')}: {h.get('nota', '')}{econ_txt}")

        invest = opp.get("investimento") or {}
        if any(invest.get(k) for k in ("ore_persona", "costo_eur", "token_totali")):
            lines.append("")
            lines.append(
                f"**Investimento presales**: {invest.get('ore_persona')} ore, "
                f"{invest.get('costo_eur')} EUR, {invest.get('token_totali')} token totali"
            )

        lines.append("")
    return "\n".join(lines)


def main() -> int:
    if not SRC.exists():
        print(f"ERRORE: {SRC} non trovato", file=sys.stderr)
        return 1
    data = json.loads(SRC.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(data), encoding="utf-8")
    print(f"Scritto {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
