#!/usr/bin/env python3
"""Genera site/index.html a partire da site/data/content.json.

Uso:
    python3 build_content.py   # rigenera data/content.json dai file raw (se servono aggiornamenti)
    python3 generate_site.py   # rigenera index.html dal content.json

Il contenuto in data/content.json riflette uno snapshot dei documenti
DocMind del progetto "PreSales" (panoramica + 4 dettagli opportunità).
Quando quei documenti DocMind cambiano, bisogna aggiornare i file in
/tmp/raw (o la relativa fonte) e rilanciare build_content.py, poi questo
script, per tenere la pagina allineata.
"""
import json
import re
from pathlib import Path
from datetime import datetime

import markdown as md

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "content.json"
OUT_FILE = HERE / "index.html"

STATUS_META = {
    "iniziale": {"label": "Fase iniziale", "color": "#F5A524"},
    "avanzata": {"label": "In preparazione", "color": "#4ADE80"},
    "analisi":  {"label": "Analisi in corso", "color": "#39A7FF"},
    "vuota":    {"label": "Nessuna info", "color": "#5F7290"},
}

MD_EXT = ["tables", "fenced_code", "sane_lists"]


def render_md(text: str) -> str:
    html = md.markdown(text, extensions=MD_EXT)
    # evidenzia i blockquote "fonte/attenzione" con una classe dedicata
    html = html.replace("<blockquote>", '<blockquote class="src-note">')
    return html


def fmt_date(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
        return f"{dt.day} {mesi[dt.month-1]} {dt.year} · {dt.hour:02d}:{dt.minute:02d} UTC"
    except Exception:
        return iso


def build_opportunity_card(idx: int, opp: dict) -> str:
    meta = STATUS_META.get(opp["status"], {"label": opp.get("statusLabel", ""), "color": "#5F7290"})
    body_html = render_md(opp["content"])
    n = f"{idx:02d}"
    return f"""
    <article class="opp-card reveal" style="--accent:{meta['color']}" data-opp="{opp['uniqueName']}">
      <button class="opp-head" type="button" aria-expanded="false">
        <span class="opp-num">{n}</span>
        <span class="opp-head-main">
          <span class="opp-title">{opp['displayName']}</span>
          <span class="opp-client">{opp['client']}</span>
        </span>
        <span class="opp-status" style="--accent:{meta['color']}">{meta['label']}</span>
        <span class="opp-chevron" aria-hidden="true"></span>
      </button>
      <div class="opp-sub">
        <span>{opp['macroAmbito']}</span>
        <span class="dot">&middot;</span>
        <span>{opp['fileCount']} file sorgente</span>
        <span class="dot">&middot;</span>
        <span>agg. {fmt_date(opp['updatedAt'])}</span>
      </div>
      <div class="opp-body">
        <div class="opp-body-inner prose">
          {body_html}
        </div>
      </div>
    </article>"""


def build_overview_block(ov: dict) -> str:
    body_html = render_md(ov["content"])
    return f"""
    <article class="overview-card reveal">
      <div class="overview-head">
        <span class="overview-kicker">01 &middot; Panoramica generale</span>
        <h3>{ov['displayName']}</h3>
        <span class="overview-updated">Aggiornato {fmt_date(ov['updatedAt'])}</span>
      </div>
      <div class="opp-body opp-body--open">
        <div class="opp-body-inner prose">
          {body_html}
        </div>
      </div>
    </article>"""


def main():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    overview = data["overview"]
    opportunities = data["opportunities"]

    overview_html = build_overview_block(overview)
    cards_html = "\n".join(
        build_opportunity_card(i + 1, opp) for i, opp in enumerate(opportunities)
    )

    n_opps = len(opportunities)
    n_files = sum(o["fileCount"] for o in opportunities)
    generated_at = fmt_date(data["generatedAt"])

    template = (HERE / "template.html").read_text(encoding="utf-8")
    html = template
    html = html.replace("__OVERVIEW_BLOCK__", overview_html)
    html = html.replace("__OPP_CARDS__", cards_html)
    html = html.replace("__N_OPPS__", str(n_opps))
    html = html.replace("__N_FILES__", str(n_files))
    html = html.replace("__GENERATED_AT__", generated_at)

    OUT_FILE.write_text(html, encoding="utf-8")
    print(f"Scritto {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
