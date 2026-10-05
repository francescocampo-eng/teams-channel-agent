#!/usr/bin/env python3
"""Genera site/index.html e site/opportunita/<slug>.html a partire da
site/data/content.json.

Uso:
    python3 build_content.py   # rigenera data/content.json dai file raw (se servono aggiornamenti)
    python3 generate_site.py   # rigenera index.html + pagine di dettaglio dal content.json

Il contenuto in data/content.json riflette uno snapshot dei documenti
DocMind del progetto "PreSales" (panoramica + dettagli opportunità).
Quando quei documenti DocMind cambiano, bisogna aggiornare i file in
site/data/raw/ e rilanciare build_content.py, poi questo script, per
tenere la pagina allineata.

Ogni sezione "## ..." (e sottosezione "### ...") del markdown sorgente di
un'opportunità diventa automaticamente una voce della mini-TOC nella
pagina di dettaglio: aggiungere nuove sottosezioni in futuro non richiede
modifiche a questo script.
"""
import json
import re
from pathlib import Path
from datetime import datetime

import markdown as md

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "content.json"
OUT_FILE = HERE / "index.html"
DETAIL_DIR = HERE / "opportunita"
DETAIL_TEMPLATE_FILE = HERE / "template_detail.html"

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


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)  # rimuove eventuale markup inline (es. <strong>)
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9àèéìòù\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s.strip("-") or "sezione"


def inject_toc(html: str):
    """Aggiunge id=".." a ogni <h2>/<h3> e costruisce la mini-TOC della
    pagina di dettaglio. Qualunque nuova sezione/sottosezione futura nel
    markdown sorgente apparirà qui automaticamente."""
    toc = []
    seen = set()

    def repl(m):
        level, inner = m.group(1), m.group(2)
        base = slugify(inner)
        slug, i = base, 2
        while slug in seen:
            slug = f"{base}-{i}"
            i += 1
        seen.add(slug)
        toc.append({"level": level, "title": re.sub(r"<[^>]+>", "", inner), "id": slug})
        return f'<h{level} id="{slug}">{inner}</h{level}>'

    html = re.sub(r"<h([23])>(.*?)</h\1>", repl, html, flags=re.S)
    return html, toc


def build_toc_html(toc) -> str:
    # salta l'eventuale h1 (già nascosto via CSS) e il primo h2 se coincide col titolo pagina
    items = [t for t in toc if t["level"] in ("2", "3")]
    links = []
    for t in items:
        cls = "toc-h3" if t["level"] == "3" else ""
        links.append(f'<a href="#{t["id"]}" class="{cls}">{t["title"]}</a>')
    return "\n".join(links) if links else '<span style="color:var(--ink3);font-size:13px">Nessuna sottosezione</span>'


def extract_excerpt(markdown_text: str, heading: str, max_len: int = 190) -> str:
    """Estrae il primo paragrafo sotto una sezione '## <heading>' del markdown grezzo."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", markdown_text, flags=re.M)
    if not m:
        return ""
    rest = markdown_text[m.end():]
    rest = re.split(r"^##\s", rest, maxsplit=1, flags=re.M)[0]
    paras = [p.strip() for p in rest.split("\n\n") if p.strip() and not p.strip().startswith(">")]
    if not paras:
        return ""
    text = re.sub(r"[*_`#]", "", paras[0])
    text = re.sub(r"\s+", " ", text).strip()
    return (text[:max_len].rsplit(" ", 1)[0] + "…") if len(text) > max_len else text


def fmt_date(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
        return f"{dt.day} {mesi[dt.month-1]} {dt.year} · {dt.hour:02d}:{dt.minute:02d} UTC"
    except Exception:
        return iso


def build_flip_card(idx: int, opp: dict) -> str:
    meta = STATUS_META.get(opp["status"], {"label": opp.get("statusLabel", ""), "color": "#5F7290"})
    n = f"{idx:02d}"
    excerpt = extract_excerpt(opp["content"], "Richiesta cliente") or opp["macroAmbito"]
    return f"""
    <div class="flip-card reveal" style="--accent:{meta['color']}" data-opp="{opp['uniqueName']}">
      <div class="flip-card-inner">
        <div class="flip-face flip-face-front">
          <span class="opp-num">{n} / OPPORTUNITÀ</span>
          <span class="opp-status" style="--accent:{meta['color']}">{meta['label']}</span>
          <div class="opp-title">{opp['displayName']}</div>
          <div class="opp-client">{opp['client']}</div>
          <p class="opp-summary">{opp['summary']}</p>
          <div class="flip-hint"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 7h16M4 12h16M4 17h10"/></svg> Clicca per girare la card</div>
        </div>
        <div class="flip-face flip-face-back">
          <span class="opp-back-label">Richiesta cliente</span>
          <p class="opp-back-text">{excerpt}</p>
          <div class="opp-meta-row">
            <span><b>Macro ambito:</b> {opp['macroAmbito']}</span>
            <span><b>File sorgente:</b> {opp['fileCount']}</span>
            <span><b>Aggiornato:</b> {fmt_date(opp['updatedAt'])}</span>
          </div>
          <a class="opp-detail-link" href="opportunita/{opp['slug']}.html">Apri dettaglio completo
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M7 17 17 7M9 7h8v8"/></svg>
          </a>
        </div>
      </div>
    </div>"""


def build_overview_block(ov: dict) -> str:
    body_html = render_md(ov["content"])
    body_html, _ = inject_toc(body_html)
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


def build_detail_page(opp: dict, generated_at: str, detail_template: str):
    meta = STATUS_META.get(opp["status"], {"label": opp.get("statusLabel", ""), "color": "#5F7290"})
    body_html = render_md(opp["content"])
    body_html, toc = inject_toc(body_html)
    toc_html = build_toc_html(toc)

    html = detail_template
    html = html.replace("__OPP_TITLE__", opp["displayName"])
    html = html.replace("__OPP_COLOR__", meta["color"])
    html = html.replace("__OPP_STATUS_LABEL__", meta["label"])
    html = html.replace("__OPP_CLIENT__", opp["client"])
    html = html.replace("__OPP_MACRO__", opp["macroAmbito"])
    html = html.replace("__OPP_FILES__", str(opp["fileCount"]))
    html = html.replace("__OPP_UPDATED__", fmt_date(opp["updatedAt"]))
    html = html.replace("__TOC__", toc_html)
    html = html.replace("__OPP_CONTENT__", body_html)
    html = html.replace("__GENERATED_AT__", generated_at)

    DETAIL_DIR.mkdir(parents=True, exist_ok=True)
    out = DETAIL_DIR / f"{opp['slug']}.html"
    out.write_text(html, encoding="utf-8")
    print(f"Scritto {out} ({out.stat().st_size} bytes)")


def main():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    overview = data["overview"]
    opportunities = data["opportunities"]

    overview_html = build_overview_block(overview)
    cards_html = "\n".join(
        build_flip_card(i + 1, opp) for i, opp in enumerate(opportunities)
    )

    n_opps = len(opportunities)
    n_files = sum(o["fileCount"] for o in opportunities)
    generated_at = fmt_date(data["generatedAt"])
    data_updated_at = fmt_date(data["dataUpdatedAt"])

    template = (HERE / "template.html").read_text(encoding="utf-8")
    html = template
    html = html.replace("__OVERVIEW_BLOCK__", overview_html)
    html = html.replace("__OPP_CARDS__", cards_html)
    html = html.replace("__N_OPPS__", str(n_opps))
    html = html.replace("__N_FILES__", str(n_files))
    html = html.replace("__GENERATED_AT__", generated_at)
    html = html.replace("__DATA_UPDATED_AT__", data_updated_at)

    OUT_FILE.write_text(html, encoding="utf-8")
    print(f"Scritto {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")

    detail_template = DETAIL_TEMPLATE_FILE.read_text(encoding="utf-8")
    for opp in opportunities:
        build_detail_page(opp, generated_at, detail_template)


if __name__ == "__main__":
    main()
