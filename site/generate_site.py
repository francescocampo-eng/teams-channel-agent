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
from datetime import datetime, timedelta

import markdown as md

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "content.json"
MILESTONES_FILE = HERE.parent / "data" / "presales_milestones.json"
OUT_FILE = HERE / "index.html"
CALENDAR_OUT_FILE = HERE / "calendario.html"
SUMMARY_OUT_FILE = HERE / "riepilogo.html"
DETAIL_DIR = HERE / "opportunita"
DETAIL_TEMPLATE_FILE = HERE / "template_detail.html"
CALENDAR_TEMPLATE_FILE = HERE / "template_calendar.html"
SUMMARY_TEMPLATE_FILE = HERE / "template_summary.html"

ESITO_META = {
    "VINTA": {"label": "Vinta", "color": "#15803D"},
    "PERSA": {"label": "Persa", "color": "#B91C1C"},
}

STATUS_META = {
    "iniziale": {"label": "Fase iniziale", "color": "#B45309"},
    "avanzata": {"label": "In preparazione", "color": "#15803D"},
    "analisi":  {"label": "Analisi in corso", "color": "#1D4ED8"},
    "vuota":    {"label": "Nessuna info", "color": "#475569"},
}

MILESTONE_STATO_META = {
    "ANALISI":                  {"label": "Analisi", "color": "#1D4ED8"},
    "PROPOSTA_IN_PREPARAZIONE": {"label": "Proposta in preparazione", "color": "#B45309"},
    "PROPOSTA_INVIATA":         {"label": "Proposta inviata", "color": "#6D28D9"},
    "ATTESA_FEEDBACK_CLIENTE":  {"label": "Attesa feedback cliente", "color": "#6D28D9"},
    "ATTESA_FEEDBACK_BU":       {"label": "Attesa feedback BU", "color": "#6D28D9"},
    "VINTA":                    {"label": "Vinta", "color": "#15803D"},
    "PERSA":                    {"label": "Persa", "color": "#B91C1C"},
    "STAND_BY":                  {"label": "Stand-by", "color": "#475569"},
}

IMPEGNO_TIPO_META = {
    "meeting":  {"label": "Meeting", "color": "#1D4ED8"},
    "deadline": {"label": "Scadenza", "color": "#B91C1C"},
    "milestone": {"label": "Milestone", "color": "#6D28D9"},
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


def fmt_date_short(iso: str) -> str:
    try:
        d = datetime.fromisoformat(iso)
        mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
        return f"{d.day} {mesi[d.month-1]} {d.year}"
    except Exception:
        return iso


def build_economics_html(economics: dict) -> str:
    if not economics:
        return ""
    labels = {
        "stima_rom_gg_persona_min": "Stima ROM min (gg-persona)",
        "stima_rom_gg_persona_max": "Stima ROM max (gg-persona)",
        "picco_fte": "Picco FTE",
        "fp_sizing_gg_persona": "FP sizing (gg-persona)",
        "valore_commessa_eur": "Valore commessa (€)",
    }
    chips = "".join(
        f'<span class="economics-chip"><b>{labels.get(k, k)}:</b> {v}</span>'
        for k, v in economics.items()
    )
    return f'<div class="economics-row">{chips}</div>'


def build_dashboard_html(slug: str, milestones: dict) -> str:
    opp = milestones.get(slug)
    if not opp:
        return ""
    stato_meta = MILESTONE_STATO_META.get(opp["stato"], {"label": opp["stato"], "color": "#5F7290"})
    deadline_html = ""
    if opp.get("deadline"):
        deadline_html = f'<span class="dash-deadline"><b>Prossima scadenza:</b> {fmt_date_short(opp["deadline"])} — {opp.get("deadline_descrizione") or ""}</span>'
    attesa_html = f'<span class="dash-waiting"><b>In attesa di:</b> {opp["in_attesa_di"]}</span>' if opp.get("in_attesa_di") else ""

    merged = []
    for ev in opp.get("storico", []):
        meta = MILESTONE_STATO_META.get(ev["stato"], {"label": ev["stato"], "color": "#5F7290"})
        merged.append({
            "data": ev["data"], "kind": "stato",
            "label": meta["label"], "color": meta["color"],
            "nota": ev.get("nota", ""), "economics": ev.get("economics"),
        })
    for imp in opp.get("impegni", []):
        tipo_meta = IMPEGNO_TIPO_META.get(imp["tipo"], {"label": imp["tipo"], "color": "#5F7290"})
        merged.append({
            "data": imp["data"], "kind": "impegno",
            "label": tipo_meta["label"], "color": tipo_meta["color"],
            "nota": imp["titolo"], "economics": None,
        })
    merged.sort(key=lambda e: e["data"])

    timeline_items = []
    for ev in merged:
        economics_html = build_economics_html(ev.get("economics"))
        kind_icon = "&#9679;" if ev["kind"] == "stato" else "&#9650;"
        timeline_items.append(f"""
        <li class="htimeline-item htimeline-{ev['kind']}" style="--accent:{ev['color']}">
          <span class="htimeline-date">{fmt_date_short(ev['data'])}</span>
          <span class="htimeline-dot">{kind_icon}</span>
          <span class="htimeline-stato" style="--accent:{ev['color']}">{ev['label']}</span>
          <div class="htimeline-body">
            <p class="htimeline-nota">{ev['nota']}</p>
            {economics_html}
          </div>
        </li>""")
    timeline_html = "\n".join(timeline_items) or '<li class="htimeline-empty">Nessun evento registrato.</li>'

    return f"""
    <div class="dashboard-card reveal">
      <div class="dashboard-head">
        <span class="section-label">Dashboard stato — a cura di Ciro</span>
        <span class="dash-stato-badge" style="--accent:{stato_meta['color']}">{stato_meta['label']}</span>
      </div>
      <div class="dashboard-meta">
        {deadline_html}
        {attesa_html}
      </div>
      <ol class="htimeline">
        {timeline_html}
      </ol>
    </div>"""


def build_detail_page(opp: dict, generated_at: str, detail_template: str, milestones: dict):
    meta = STATUS_META.get(opp["status"], {"label": opp.get("statusLabel", ""), "color": "#5F7290"})
    body_html = render_md(opp["content"])
    body_html, toc = inject_toc(body_html)
    toc_html = build_toc_html(toc)
    dashboard_html = build_dashboard_html(opp["slug"], milestones)

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
    html = html.replace("__DASHBOARD_BLOCK__", dashboard_html)
    html = html.replace("__GENERATED_AT__", generated_at)

    DETAIL_DIR.mkdir(parents=True, exist_ok=True)
    out = DETAIL_DIR / f"{opp['slug']}.html"
    out.write_text(html, encoding="utf-8")
    print(f"Scritto {out} ({out.stat().st_size} bytes)")


def build_calendar_page(opportunities: list, milestones: dict, generated_at: str, calendar_template: str):
    slug_to_opp = {o["slug"]: o for o in opportunities}
    events = []
    for slug, m in milestones.items():
        opp = slug_to_opp.get(slug)
        nome = opp["displayName"] if opp else m.get("nome", slug)
        link = f"opportunita/{slug}.html"
        for imp in m.get("impegni", []):
            events.append({**imp, "slug": slug, "nome": nome, "link": link})
    events.sort(key=lambda e: e["data"])

    today = datetime.now().date().isoformat()
    rows = []
    for ev in events:
        tipo_meta = IMPEGNO_TIPO_META.get(ev["tipo"], {"label": ev["tipo"], "color": "#5F7290"})
        is_past = ev["data"] < today
        cls = "cal-row is-past" if is_past else "cal-row"
        rows.append(f"""
        <li class="{cls}" style="--accent:{tipo_meta['color']}">
          <span class="cal-date">{fmt_date_short(ev['data'])}</span>
          <span class="cal-tipo" style="--accent:{tipo_meta['color']}">{tipo_meta['label']}</span>
          <span class="cal-titolo">{ev['titolo']}</span>
          <a class="cal-link" href="{ev['link']}">{ev['nome']} &rarr;</a>
        </li>""")
    rows_html = "\n".join(rows) or '<li class="cal-empty">Nessun impegno registrato al momento.</li>'

    html = calendar_template
    html = html.replace("__CALENDAR_ROWS__", rows_html)
    html = html.replace("__GENERATED_AT__", generated_at)
    CALENDAR_OUT_FILE.write_text(html, encoding="utf-8")
    print(f"Scritto {CALENDAR_OUT_FILE} ({CALENDAR_OUT_FILE.stat().st_size} bytes)")


def build_kpi_row_html(opportunities: list, milestones: dict) -> str:
    slugs = list(milestones.keys())
    n_tot = len(slugs)
    n_vinte = sum(1 for s in slugs if milestones[s].get("esito") == "VINTA")
    n_perse = sum(1 for s in slugs if milestones[s].get("esito") == "PERSA")
    n_corso = n_tot - n_vinte - n_perse

    investiti = [milestones[s]["investimento"]["costo_eur"] for s in slugs
                 if milestones[s].get("investimento", {}).get("costo_eur") is not None]
    costo_tot = sum(investiti) if investiti else None

    ritorni = [milestones[s].get("economics_vinta_eur") for s in slugs]  # placeholder, non usato oggi
    kpis = [
        ("Iniziative totali", str(n_tot), "#1D4ED8"),
        ("Vinte", str(n_vinte), "#15803D"),
        ("Perse", str(n_perse), "#B91C1C"),
        ("In corso", str(n_corso), "#B45309"),
        ("Investimento consuntivato", f"{costo_tot:,.0f} €".replace(",", ".") if costo_tot is not None else "n/d", "#6D28D9"),
    ]
    cards = "".join(
        f'<div class="kpi-card" style="--accent:{color}"><span class="kpi-num">{val}</span><span class="kpi-label">{label}</span></div>'
        for label, val, color in kpis
    )
    return f'<div class="kpi-row reveal">{cards}</div>'


def build_gantt_html(opportunities: list, milestones: dict) -> str:
    """Asse temporale ancorato all'avanzamento reale (storico + oggi):
    gli impegni/deadline lontani nel tempo (es. un go-live a 9 mesi) non
    devono schiacciare tutto il resto dell'asse — vengono mostrati come
    marker "fuori scala" ancorati al bordo destro, con la data vera nel
    tooltip. Il marker/linea "oggi" viene disegnato DENTRO ogni singola
    `.gantt-track` (non come overlay sull'intera riga, che include anche
    la colonna 200px dell'etichetta) per restare correttamente allineato
    alla scala della barra, anche su mobile dove la colonna sparisce."""
    slug_to_opp = {o["slug"]: o for o in opportunities}
    today_iso = datetime.now().date().isoformat()

    core_dates = [today_iso]
    for m in milestones.values():
        core_dates += [ev["data"] for ev in m.get("storico", [])]

    horizon = datetime.fromisoformat(today_iso) + timedelta(days=120)
    for m in milestones.values():
        for imp in m.get("impegni", []):
            if datetime.fromisoformat(imp["data"]) <= horizon:
                core_dates.append(imp["data"])
        if m.get("deadline") and datetime.fromisoformat(m["deadline"]) <= horizon:
            core_dates.append(m["deadline"])

    if not core_dates:
        return '<p class="dash-waiting">Nessun dato di avanzamento ancora registrato.</p>'

    d0 = datetime.fromisoformat(min(core_dates)) - timedelta(days=3)
    d1 = datetime.fromisoformat(max(core_dates)) + timedelta(days=10)
    span = max((d1 - d0).days, 1)

    def pct(iso: str) -> float:
        dt = datetime.fromisoformat(iso)
        return max(0.0, min(100.0, (dt - d0).days / span * 100))

    today_pct = pct(today_iso)
    rows = []
    for slug, m in milestones.items():
        opp = slug_to_opp.get(slug)
        name = opp["displayName"] if opp else m.get("nome", slug)
        link = f'opportunita/{slug}.html' if opp else "#"
        events = sorted(m.get("storico", []), key=lambda e: e["data"])
        segs = []
        for i, ev in enumerate(events):
            start = pct(ev["data"])
            end = pct(events[i + 1]["data"]) if i + 1 < len(events) else pct(today_iso)
            meta = MILESTONE_STATO_META.get(ev["stato"], {"label": ev["stato"], "color": "#5F7290"})
            width = max(end - start, 0.6)
            segs.append(
                f'<span class="gantt-seg" style="left:{start:.2f}%;width:{width:.2f}%;--accent:{meta["color"]}" '
                f'title="{meta["label"]} — dal {fmt_date_short(ev["data"])}"></span>'
            )
        markers = []
        for imp in m.get("impegni", []):
            p = pct(imp["data"])
            is_future_offscale = datetime.fromisoformat(imp["data"]) > d1
            tipo_meta = IMPEGNO_TIPO_META.get(imp["tipo"], {"label": imp["tipo"], "color": "#5F7290"})
            cls = "gantt-marker gantt-marker--offscale" if is_future_offscale else "gantt-marker"
            label = imp["titolo"] + (" (oltre l'orizzonte dei prossimi 120gg)" if is_future_offscale else "")
            markers.append(
                f'<span class="{cls}" style="left:{p:.2f}%;--accent:{tipo_meta["color"]}" '
                f'title="{label} — {fmt_date_short(imp["data"])}">{"&#9650;"}</span>'
            )
        esito = m.get("esito")
        esito_html = ""
        if esito in ESITO_META:
            meta = ESITO_META[esito]
            esito_html = f'<span class="gantt-esito" style="--accent:{meta["color"]}">{meta["label"]}</span>'
        today_tick = f'<span class="gantt-today-tick" style="left:{today_pct:.2f}%" title="Oggi"></span>'
        rows.append(f"""
        <div class="gantt-row">
          <a class="gantt-label" href="{link}">{name}{esito_html}</a>
          <div class="gantt-track">{today_tick}{''.join(segs)}{''.join(markers)}</div>
        </div>""")

    legend_items = "".join(
        f'<span class="gantt-legend-item"><i style="--accent:{meta["color"]}"></i>{meta["label"]}</span>'
        for meta in {v["label"]: v for v in MILESTONE_STATO_META.values()}.values()
    )
    return f"""
    <div class="gantt-wrap reveal">
      <div class="gantt">
        {''.join(rows)}
      </div>
      <div class="gantt-legend">
        {legend_items}
        <span class="gantt-legend-item"><i style="--accent:#6D28D9;width:2px;height:14px;border-radius:0"></i>Oggi</span>
        <span class="gantt-legend-item">&#9650; scadenza/meeting/milestone (tratteggiata = oltre 120gg, fuori scala)</span>
      </div>
    </div>"""


def build_roi_html(opportunities: list, milestones: dict) -> str:
    slug_to_opp = {o["slug"]: o for o in opportunities}
    rows = []
    any_data = False
    for slug, m in milestones.items():
        opp = slug_to_opp.get(slug)
        name = opp["displayName"] if opp else m.get("nome", slug)
        inv = m.get("investimento") or {}
        costo = inv.get("costo_eur")
        ore = inv.get("ore_persona")
        token = inv.get("token_totali")
        econ_list = m.get("storico", [])
        valore = None
        for ev in econ_list:
            e = ev.get("economics") or {}
            if e.get("valore_commessa_eur") is not None:
                valore = e["valore_commessa_eur"]
        esito = m.get("esito")

        if costo is None and valore is None:
            rows.append(f"""
            <div class="roi-row roi-row--empty">
              <span class="roi-label">{name}</span>
              <span class="roi-empty-note">Investimento non ancora consuntivato — da inserire alla chiusura della presales.</span>
            </div>""")
            continue

        any_data = True
        max_val = max(v for v in [costo, valore] if v is not None) or 1
        costo_w = (costo / max_val * 100) if costo is not None else 0
        valore_w = (valore / max_val * 100) if valore is not None else 0
        roi_note = ""
        if costo is not None and valore is not None:
            roi = valore - costo
            sign = "positivo" if roi >= 0 else "negativo"
            roi_color = "#15803D" if roi >= 0 else "#B91C1C"
            roi_note = f'<span class="roi-net" style="--accent:{roi_color}">Ritorno {sign}: {roi:,.0f} €</span>'.replace(",", ".")

        detail = f"{ore} gg-persona · " if ore else ""
        detail += f"{token:,} token".replace(",", ".") if token else ""

        rows.append(f"""
        <div class="roi-row">
          <span class="roi-label">{name} {f'<i class="roi-esito" style="--accent:{ESITO_META[esito]["color"]}">{ESITO_META[esito]["label"]}</i>' if esito in ESITO_META else ''}</span>
          <div class="roi-bars">
            <div class="roi-bar roi-bar--cost" style="width:{costo_w:.1f}%" title="Investimento: {costo or 0:,.0f} €">
              <span>Investimento{f': {costo:,.0f} €'.replace(',', '.') if costo is not None else ': n/d'}</span>
            </div>
            <div class="roi-bar roi-bar--value" style="width:{valore_w:.1f}%" title="Valore commessa: {valore or 0:,.0f} €">
              <span>Ritorno{f': {valore:,.0f} €'.replace(',', '.') if valore is not None else ': n/d'}</span>
            </div>
          </div>
          <div class="roi-foot">{detail}{roi_note}</div>
        </div>""")

    if not any_data:
        note = '<p class="dash-waiting">Nessuna iniziativa ha ancora un investimento/ritorno consuntivato. Il grafico si popola automaticamente alla chiusura di ciascuna presales (vinta o persa).</p>'
        return note + "".join(rows)
    return f'<div class="roi-block reveal">{"".join(rows)}</div>'


def build_summary_page(opportunities: list, milestones: dict, generated_at: str, summary_template: str):
    kpi_html = build_kpi_row_html(opportunities, milestones)
    gantt_html = build_gantt_html(opportunities, milestones)
    roi_html = build_roi_html(opportunities, milestones)

    html = summary_template
    html = html.replace("__KPI_ROW__", kpi_html)
    html = html.replace("__GANTT_BLOCK__", gantt_html)
    html = html.replace("__ROI_BLOCK__", roi_html)
    html = html.replace("__GENERATED_AT__", generated_at)
    SUMMARY_OUT_FILE.write_text(html, encoding="utf-8")
    print(f"Scritto {SUMMARY_OUT_FILE} ({SUMMARY_OUT_FILE.stat().st_size} bytes)")


def main():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    milestones = json.loads(MILESTONES_FILE.read_text(encoding="utf-8")) if MILESTONES_FILE.exists() else {}
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
        build_detail_page(opp, generated_at, detail_template, milestones)

    if CALENDAR_TEMPLATE_FILE.exists():
        calendar_template = CALENDAR_TEMPLATE_FILE.read_text(encoding="utf-8")
        build_calendar_page(opportunities, milestones, generated_at, calendar_template)

    if SUMMARY_TEMPLATE_FILE.exists():
        summary_template = SUMMARY_TEMPLATE_FILE.read_text(encoding="utf-8")
        build_summary_page(opportunities, milestones, generated_at, summary_template)


if __name__ == "__main__":
    main()
