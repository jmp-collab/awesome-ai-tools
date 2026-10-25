#!/usr/bin/env python3
"""Baut die KI-Werkstatt-Seite (docs/) aus README.de.md.

Keine Abhängigkeiten, nur Python 3.8+. Aufruf aus dem Repo-Root:
    python3 scripts/build_de_page.py

Quellen:  README.de.md (Tool-Liste), brand/ki-werkstatt.json (Marke),
          data/stacks.json (Werkzeugkisten + Stack-Finder), scripts/template/icons.svg
Ausgabe:  docs/index.html, docs/danke.html, docs/impressum.html, docs/datenschutz.html,
          docs/img/*.svg, docs/tools.json, docs/tools.csv, docs/sitemap.xml, docs/robots.txt
README.de.md bleibt die einzige Quelle für die Liste; docs/ nie von Hand bearbeiten.
"""
import csv
import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "README.de.md"
DOCS = ROOT / "docs"
IMG = DOCS / "img"
BRAND = json.loads((ROOT / "brand" / "ki-werkstatt.json").read_text(encoding="utf-8"))
STACKS = json.loads((ROOT / "data" / "stacks.json").read_text(encoding="utf-8"))
ICONS = (ROOT / "scripts" / "template" / "icons.svg").read_text(encoding="utf-8")

SITE_URL = "https://jmp-collab.github.io/awesome-ai-tools/"
REPO_URL = "https://github.com/jmp-collab/awesome-ai-tools"
TITLE = "KI-Werkstatt: KI-Tools auf Deutsch, geprüft und sortiert"
DESCRIPTION = (
    "Über 400 geprüfte KI-Tools auf Deutsch, jedes in einem Satz erklärt. Chatbots, Schreiben, "
    "Übersetzung, Bilder, Video, Automatisierung, SEO. EU-Anbieter markiert, Stack-Finder, "
    "Werkzeugkisten und PROMPTGOTT-Deep-Dives."
)
SUBSTACK = "https://promptgott.substack.com/"
UTM = "utm_source=github-pages&utm_medium=referral&utm_campaign=awesome-ki-tools-de"
LEAD_TO = BRAND["lead_offer"]["recipient"]
TODAY = date.today().strftime("%d.%m.%Y")  # Build-Datum (Sitemap, Export)
_LC = json.loads((ROOT / "data" / "linkcheck.json").read_text(encoding="utf-8"))
LINK_CHECK = date.fromisoformat(_LC["date"]).strftime("%d.%m.%Y")  # setzt nur scripts/check_links.py
LINK_CHECK_N = _LC["checked"]
if _LC.get("dead"):
    raise SystemExit(f"Abbruch: data/linkcheck.json meldet {len(_LC['dead'])} tote Links. Erst README.de.md bereinigen und scripts/check_links.py erneut laufen lassen.")
sys.path.insert(0, str(ROOT / "scripts"))
from check_links import extract_urls, url_hash  # noqa: E402  (gleiche Linkliste wie der Checker)
if _LC.get("urls_sha256") != url_hash(extract_urls(SRC.read_text(encoding="utf-8"))):
    raise SystemExit("Abbruch: Die Links in README.de.md haben sich seit dem letzten Link-Check geändert. Erst scripts/check_links.py laufen lassen.")
N_STACKS = len(STACKS["stacks"])
STACK_SIZES = sorted({len(s["tools"]) for s in STACKS["stacks"]})
STACK_SIZE_TXT = str(STACK_SIZES[0]) if len(STACK_SIZES) == 1 else f"{STACK_SIZES[0]} bis {STACK_SIZES[-1]}"

# Icon je Kategorie (Slug der H2-Überschrift)
CAT_ICON = {
    "empfehlungen-der-redaktion": "star", "promptgott-deep-dives": "flame", "text-und-sprache": "text",
    "automatisierung-und-ki-agenten": "bot", "entwickler-tools-und-llmops": "cpu", "programmieren-mit-ki": "code",
    "bilder": "image", "video": "video", "audio": "music", "marketing-und-seo": "megaphone",
    "ki-telefonagenten": "phone", "weitere-ki-tools": "box", "lernen-prompting-und-ki-grundlagen": "book",
    "verwandte-listen": "link", "mitmachen": "plus",
}
SUB_ICON = {  # H3-Icons, wo sie etwas aussagen
    "sprachmodelle-und-apis": "cpu", "chatbots-und-assistenten": "chat", "ki-suchmaschinen": "search",
    "lokal-und-privat-mit-dokumenten-chatten": "lock", "schreibassistenten": "pen",
    "übersetzung-und-lokalisierung": "globe", "browser-erweiterungen-und-add-ons": "puzzle",
    "produktivität": "zap", "meeting-assistenten": "calendar", "wissenschaft-und-recherche": "flask",
    "kundenservice": "headset",
}
# Link-Ziel mit bis zu einer Ebene balancierter Klammern, z. B. Wikipedia-Titel
DEST = r"((?:[^()\s]|\([^()\s]*\))+)"
ITEM_RE = re.compile(r"^- \[([^\]]+)\]\(" + DEST + r"\)\s*[-–—]\s*(.*)$")


def slug(text):
    text = re.sub(r"[^\w\- ]", "", text.strip().lower())
    return text.replace(" ", "-")


def retag(href):
    if href.startswith(SUBSTACK):
        href = re.sub(r"utm_source=[^&]+&utm_medium=[^&]+&utm_campaign=[^&#]+", UTM, href)
    return href


def plain(text):
    text = re.sub(r"\[([^\]]+)\]\(" + DEST + r"\)", r"\1", text)
    return re.sub(r"\s+", " ", text.replace("`", "").replace("*", "")).strip()


def inline(text):
    out = html.escape(text, quote=False)
    # Code-Spans erst am Ende einsetzen, damit `[Name](https://url)` wörtlich bleibt
    codes = []
    out = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\x00{len(codes) - 1}\x00", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", out)

    def link(m):
        label, href = m.group(1), html.unescape(m.group(2))
        if href.startswith("#"):
            pass
        elif not href.startswith("http"):
            href = REPO_URL + "/blob/main/" + href
        href = retag(href)
        attrs = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        return f'<a href="{html.escape(href)}"{attrs}>{label}</a>'

    out = re.sub(r"\[([^\]]+)\]\(" + DEST + r"\)", link, out)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", out)


def icon(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def host(url):
    return urlparse(url).hostname or ""


def favicon(url):
    return (f'<img loading="lazy" alt="" width="30" height="30" src="https://icons.duckduckgo.com/ip3/{html.escape(host(url))}.ico" '
            'onerror="this.style.visibility=\'hidden\'">')


# --------------------------------------------------------------------------- Parser
def parse(md):
    """README -> Liste von Sektionen: {title, id, blocks:[...], subs:[{title,id,blocks}]}"""
    lines = md.splitlines()
    sections, cur, sub = [], None, None
    head_md = []
    i = 0

    def target():
        return sub if sub else cur

    while i < len(lines):
        line = lines[i]
        if line.startswith("# "):
            i += 1
            continue
        if line.startswith("## "):
            title = line[3:].strip()
            cur = {"title": title, "id": slug(title), "blocks": [], "subs": []}
            sub = None
            if title != "Inhalt":
                sections.append(cur)
            i += 1
            continue
        if cur is None:
            head_md.append(line)
            i += 1
            continue
        if cur["title"] == "Inhalt":
            i += 1
            continue
        if line.startswith("### "):
            title = line[4:].strip()
            sub = {"title": title, "id": slug(title), "blocks": []}
            cur["subs"].append(sub)
            i += 1
            continue
        blocks = target()["blocks"]
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows))
            continue
        if line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ").rstrip())
                i += 1
            blocks.append(("quote", " ".join(q for q in quote if q)))
            continue
        if ITEM_RE.match(line):
            items = []
            while i < len(lines) and ITEM_RE.match(lines[i]):
                name, url, desc = ITEM_RE.match(lines[i]).groups()
                items.append({"name": name, "url": retag(url), "desc": desc})
                i += 1
            blocks.append(("items", items))
            continue
        if re.match(r"^\d+\. ", line) or line.startswith("- "):
            buf, ordered = [], line[0].isdigit()
            while i < len(lines) and (re.match(r"^\d+\. ", lines[i]) or lines[i].startswith("- ")) and not ITEM_RE.match(lines[i]):
                buf.append(re.sub(r"^(\d+\.|-) ", "", lines[i]))
                i += 1
            blocks.append(("list", (ordered, buf)))
            continue
        if line.strip() and line.strip() != "---":
            para = [line.strip()]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|\||>|- |\d+\. |---)", lines[i + 1]):
                i += 1
                para.append(lines[i].strip())
            blocks.append(("p", " ".join(para)))
        i += 1
    return sections, head_md


def all_items(sections):
    for s in sections:
        for kind, val in s["blocks"]:
            if kind == "items":
                for it in val:
                    yield s, None, it
        for sub in s["subs"]:
            for kind, val in sub["blocks"]:
                if kind == "items":
                    for it in val:
                        yield s, sub, it


def item_meta(it):
    desc = it["desc"]
    eu = "🇪🇺" in desc
    oss = "OSS`" in desc or "`OSS" in desc
    clean = plain(re.sub(r"🇪🇺|\[`OSS`\]\([^)]*\)|`OSS`", " ", desc))
    return eu, oss, clean


# --------------------------------------------------------------------------- Grafiken
def icon_body(name):
    m = re.search(r'<symbol id="i-' + name + r'"[^>]*>(.*?)</symbol>', ICONS, re.S)
    return m.group(1) if m else ""


def cat_art(idx, name, icon_name, dark_first):
    """Abstrakte Kategorie-Grafik: Verlauf, Raster, große Werkzeug-Silhouette, Schubladen-Nummer."""
    a, b = ("#0E1116", "#1C2430") if dark_first else ("#D7FF3C", "#9ED400")
    ink = "#D7FF3C" if dark_first else "#0E1116"
    g = icon_body(icon_name)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" role="img" aria-label="{html.escape(name)}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>
<pattern id="p" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{ink}" stroke-opacity=".14"/></pattern></defs>
<rect width="800" height="300" fill="url(#g)"/><rect width="800" height="300" fill="url(#p)"/>
<circle cx="640" cy="150" r="120" fill="none" stroke="{ink}" stroke-opacity=".25" stroke-width="2"/>
<circle cx="640" cy="150" r="80" fill="none" stroke="{ink}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 8"/>
<g transform="translate(560 70) scale(6.7)" fill="none" stroke="{ink}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">{g}</g>
<g transform="translate(40 40) scale(2.2)" fill="none" stroke="{ink}" stroke-opacity=".5" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{g}</g>
<text x="40" y="250" font-family="IBM Plex Mono, ui-monospace, monospace" font-size="18" font-weight="500" fill="{ink}" fill-opacity=".85" letter-spacing="3">SCHUBLADE {idx:02d}</text>
<text x="40" y="200" font-family="Space Grotesk, system-ui, sans-serif" font-size="44" font-weight="700" fill="{ink}">{html.escape(name.upper())}</text>
<path d="M40 268h220" stroke="{ink}" stroke-width="3"/>
</svg>"""


def hero_floats():
    shapes = [("wrench", "f1", 0.35), ("spark", "f2", 0.6), ("cpu", "f3", 0.25), ("ruler", "f4", 0.5), ("code", "f5", 0.15)]
    out = []
    for name, cls, depth in shapes:
        out.append(f'<div class="float {cls}" data-depth="{depth}"><svg viewBox="0 0 24 24">{icon_body(name)}</svg></div>')
    return "".join(out)


# --------------------------------------------------------------------------- Renderer
def render_blocks(blocks, sec_id, sub_id, tools_map):
    out = []
    for kind, val in blocks:
        if kind == "items":
            out.append('<ul class="tools">')
            for it in val:
                eu, oss, clean = item_meta(it)
                badges = (f'<span class="badge eu" title="Anbieter mit Sitz in der EU">EU</span>' if eu else "") + (
                    '<span class="badge oss" title="Open Source">OSS</span>' if oss else "")
                search = plain(" ".join([it["name"], clean, sec_id.replace("-", " "), (sub_id or "").replace("-", " ")])).lower()
                desc_html = inline(re.sub(r"\s*🇪🇺\s*", " ", re.sub(r"\[`OSS`\]\([^)]*\)|`OSS`", "", it["desc"])).strip())
                out.append(
                    f'<li data-eu="{int(eu)}" data-oss="{int(oss)}" data-search="{html.escape(search)}">{favicon(it["url"])}'
                    f'<div><a class="name" href="{html.escape(it["url"])}" target="_blank" rel="noopener">{html.escape(it["name"])}</a>'
                    f'<span class="badges">{badges}</span><span class="desc">{desc_html}</span></div></li>')
                tools_map.setdefault(it["name"], {"u": it["url"], "d": clean, "eu": eu})
            out.append("</ul>")
        elif kind == "quote":
            cls = "tip" if "💡" in val else "lead"
            out.append(f'<aside class="{cls}">{inline(val)}</aside>')
        elif kind == "table":
            head, *rest = val
            t = ['<div class="table"><table><thead><tr>'] + [f"<th>{inline(c)}</th>" for c in head] + ["</tr></thead><tbody>"]
            for r in rest:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
        elif kind == "list":
            ordered, buf = val
            tag = "ol" if ordered else "ul"
            out.append(f'<{tag} class="plain">' + "".join(f"<li>{inline(x)}</li>" for x in buf) + f"</{tag}>")
        elif kind == "p":
            out.append(f"<p>{inline(val)}</p>")
    return "\n".join(out)


def render_section(sec, idx, tools_map):
    ico = CAT_ICON.get(sec["id"], "box")
    n = sum(1 for s, _, _ in all_items([sec]))
    art = f'<div class="cat-art reveal"><img src="img/cat-{sec["id"]}.svg" alt="" loading="lazy" width="800" height="300"></div>' if n else ""
    body = [render_blocks(sec["blocks"], sec["id"], None, tools_map)]
    for sub in sec["subs"]:
        sico = SUB_ICON.get(sub["id"])
        body.append(f'<h3 id="{sub["id"]}">{icon(sico) if sico else ""}{inline(sub["title"])}</h3>')
        body.append(render_blocks(sub["blocks"], sec["id"], sub["id"], tools_map))
    count = f'<span class="count">{n} TOOLS</span>' if n else ""
    return (f'<section class="cat" id="{sec["id"]}"><div class="cat-head">{icon(ico)}<h2>{inline(sec["title"])}</h2>{count}</div>'
            f'{art}{"".join(body)}</section>')


def render_featured(sec, tools_map):
    cards = []
    for kind, val in sec["blocks"]:
        if kind != "items":
            continue
        for it in val:
            eu, oss, clean = item_meta(it)
            tools_map.setdefault(it["name"], {"u": it["url"], "d": clean, "eu": eu})
            eu_badge = '<span class="badge eu">EU</span>' if eu else ""
            cards.append(
                f'<li data-eu="{int(eu)}" data-oss="{int(oss)}" data-search="{html.escape((it["name"] + " " + clean + " favoriten").lower())}">'
                f'{favicon(it["url"])}<div><a class="name" href="{html.escape(it["url"])}" target="_blank" rel="noopener">{html.escape(it["name"])}</a>'
                f'<span class="badges">{eu_badge}</span><span class="desc">{html.escape(clean)}</span></div></li>')
    return "".join(cards)


def render_pg(sec):
    cards = []
    for kind, val in sec["blocks"]:
        if kind != "table":
            continue
        for row in val[1:]:
            m = re.match(r"\[([^\]]+)\]\(" + DEST + r"\)", row[0])
            if not m:
                continue
            title, url = m.group(1), retag(m.group(2))
            cards.append(f'<a class="pg-card reveal" href="{html.escape(url)}" target="_blank" rel="noopener"><b>{html.escape(title)}</b>'
                         f'<span>{html.escape(plain(row[1]))}</span><small>Passt zu: {html.escape(plain(row[2]))}</small></a>')
    intro = next((v for k, v in sec["blocks"] if k == "p"), "")
    return intro, "".join(cards)


def render_stacks(tools_map):
    out = []
    for st in STACKS["stacks"]:
        lis = []
        for name, why in st["tools"]:
            t = tools_map.get(name)
            if not t:
                raise SystemExit(f"Stack {st['id']}: Tool '{name}' nicht in README.de.md gefunden")
            lis.append(f'<li>{favicon(t["u"])}<div><a href="{html.escape(t["u"])}" target="_blank" rel="noopener">{html.escape(name)}</a> '
                       f'<span>{html.escape(why)}</span></div></li>')
        pg = ""
        if st.get("promptgott"):
            pg = f'<p class="pgline">💡 PROMPTGOTT dazu: <a href="{html.escape(retag(st["promptgott"][1] + "?" + UTM))}" target="_blank" rel="noopener">{html.escape(st["promptgott"][0])}</a></p>'
        if st.get("note"):
            pg = f'<p class="pgline">{html.escape(st["note"])}</p>'
        out.append(f'<article class="stack reveal"><div class="head">{icon(st["icon"])}<div><h3>{html.escape(st["title"])}</h3>'
                   f'<p class="for">{html.escape(st["for"])}</p></div></div><ol>{"".join(lis)}</ol>{pg}</article>')
    return "".join(out)


def lead_form(source, subject, compact=False):
    nxt = SITE_URL + "danke.html"
    return f"""<form class="form" action="https://formsubmit.co/{LEAD_TO}" method="POST">
<input type="hidden" name="_subject" value="{html.escape(subject)}"><input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="{nxt}">
<input type="hidden" name="quelle" value="{source}">
<input type="text" name="_honey" class="honey" tabindex="-1" autocomplete="off">
<div class="row"><div><label for="l-name">Name</label><input id="l-name" name="name" required autocomplete="name"></div>
<div><label for="l-mail">E-Mail</label><input id="l-mail" type="email" name="email" required autocomplete="email"></div></div>
<div class="row"><div><label for="l-web">Website oder Shop (optional)</label><input id="l-web" name="website" placeholder="https://" autocomplete="url"></div>
<div><label for="l-rolle">Du bist</label><select id="l-rolle" name="rolle"><option>Selbstständig / Freelancer</option><option>Marketing / SEO</option><option>Shop-Betreiber</option><option>Entwickler / Maker</option><option>Agentur</option><option>Anderes</option></select></div></div>
<label for="l-proj">Was baust du gerade, und wo hakt es?</label><textarea id="l-proj" name="projekt" rows="4" required placeholder="Beispiel: Shop mit 2.000 Artikeln, Produkttexte in DE/EN/NL, ein Mensch für alles."></textarea>
<label class="consent"><input type="checkbox" name="einwilligung" value="ja" required><span>Ich bin einverstanden, dass meine Angaben per E-Mail an Jean Maurice Port übermittelt werden, um meine Anfrage zu beantworten. Details in der <a href="datenschutz.html">Datenschutzerklärung</a>.</span></label>
<button class="btn" type="submit">{icon("mail")}Stack-Check anfragen</button>
<p class="hint">Antwort kommt per Mail, meist innerhalb weniger Tage. Oder direkt an <a href="mailto:{LEAD_TO}?subject=Stack-Check">{LEAD_TO}</a>.</p>
</form>"""


def page_shell(title, body, desc=DESCRIPTION, canonical=SITE_URL, extra_head=""):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:locale" content="de_DE">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE_URL}og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="assets/fonts.css"><link rel="stylesheet" href="assets/style.css">
{extra_head}
</head>
<body>
{ICONS}
{body}
<script src="assets/app.js" defer></script>
</body>
</html>
"""


def topbar(with_search=True):
    search = ('<form id="searchform" role="search"><label class="sr" for="q">Tools durchsuchen</label>'
              '<input type="search" id="q" placeholder="Suchen: übersetzen, Podcast, SEO, Shop …" autocomplete="off"></form>') if with_search else ""
    return f"""<header class="topbar"><div class="wrap in">
<a class="logo" href="{SITE_URL}"><span class="mark">{icon("wrench")}</span><span>KI-WERKSTATT</span></a>
{search}
<div class="tools">{'<span id="count" class="badge hide-m" aria-live="polite"></span>' if with_search else ''}
<button class="iconbtn" id="theme" type="button" title="Hell/Dunkel umschalten">{icon("sun")}</button>
<a class="btn btn-lime btn-sm hide-m" href="{'' if with_search else SITE_URL}#stack-check">{icon("mail")}Stack-Check</a></div>
</div><div id="progress"></div></header>"""


def footer():
    return f"""<footer><div class="wrap">
<div class="cols">
<div><h4>KI-Werkstatt</h4><p style="margin:0">{html.escape(BRAND["claim"])} Geprüft. Sortiert. Auf Deutsch.</p></div>
<div><h4>Projekt</h4><ul><li><a href="{REPO_URL}">GitHub-Repository</a></li><li><a href="{REPO_URL}/blob/main/README.de.md">Liste als Markdown</a></li><li><a href="{REPO_URL}/blob/main/README.md">English version</a></li><li><a href="tools.csv">Liste als CSV</a> · <a href="tools.json">JSON</a></li></ul></div>
<div><h4>Praxis</h4><ul><li><a href="{SUBSTACK}?{UTM}" target="_blank" rel="noopener">PROMPTGOTT auf Substack</a></li><li><a href="{SUBSTACK}subscribe?{UTM}" target="_blank" rel="noopener">Newsletter abonnieren</a></li></ul></div>
<div><h4>Rechtliches</h4><ul><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li><li><a href="{REPO_URL}/blob/main/LICENSE">MIT-Lizenz</a></li></ul></div>
</div>
<p>Letzter Link-Check: {LINK_CHECK} ({LINK_CHECK_N} Links). Seite gebaut am {TODAY}. Basiert auf <a href="https://github.com/mahseema/awesome-ai-tools">Awesome AI Tools</a> von Mahsima Dastan (MIT). Tool-Logos werden als Favicons der jeweiligen Anbieter geladen; die Rechte liegen bei den Anbietern.</p>
</div></footer>
<button id="totop" type="button" title="Nach oben">{icon("up")}</button>
<a class="btn btn-lime fab" href="#stack-check">{icon("mail")}Stack-Check</a>
<div class="stickybar" id="stickybar"><div class="wrap in">
<div><b>Die Liste als CSV per Mail</b><small>Eine Mail mit dem Download und dem Überblick über die {N_STACKS} Werkzeugkisten. Kein Newsletter-Dauerfeuer.</small></div>
<form action="https://formsubmit.co/{LEAD_TO}" method="POST"><input type="hidden" name="_subject" value="CSV-Anfrage – KI-Werkstatt"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_template" value="table"><input type="hidden" name="_next" value="{SITE_URL}danke.html"><input type="hidden" name="quelle" value="Sticky-Leiste"><input type="text" name="_honey" class="honey" tabindex="-1" autocomplete="off">
<label class="sr" for="sb-mail">E-Mail</label><input id="sb-mail" type="email" name="email" placeholder="deine@mail.de" required><button class="btn btn-lime btn-sm" type="submit">Schicken</button><label class="sb-consent"><input type="checkbox" name="einwilligung" value="ja" required> Einverstanden, dass meine E-Mail über FormSubmit an Jean Maurice Port geht. <a href="datenschutz.html">Datenschutz</a></label></form>
<button class="close" type="button" title="Schließen">{icon("x")}</button>
</div></div>"""


def build_index(sections, head_md):
    tools_map = {}
    by_id = {s["id"]: s for s in sections}
    featured = by_id.pop("empfehlungen-der-redaktion", None)
    pg_sec = by_id.pop("promptgott-deep-dives", None)
    tail_ids = ["lernen-prompting-und-ki-grundlagen", "verwandte-listen", "mitmachen"]
    list_secs = [s for s in sections if s["id"] in by_id and s["id"] not in tail_ids]
    tail_secs = [by_id[i] for i in tail_ids if i in by_id]

    # Liste rendern (füllt tools_map)
    list_html = "".join(render_section(s, i + 1, tools_map) for i, s in enumerate(list_secs))
    tail_html = "".join(render_section(s, i + 1 + len(list_secs), tools_map) for i, s in enumerate(tail_secs))
    featured_html = render_featured(featured, tools_map) if featured else ""
    pg_intro, pg_cards = render_pg(pg_sec) if pg_sec else ("", "")
    stacks_html = render_stacks(tools_map)

    # Statistik (eindeutige URLs)
    uniq = {}
    for s, sub, it in all_items(sections):
        uniq.setdefault(it["url"], it)
    n_tools = len(uniq)
    n_eu = sum(1 for it in uniq.values() if item_meta(it)[0])
    n_oss = sum(1 for it in uniq.values() if item_meta(it)[1])
    n_cats = len(list_secs)
    n_subs = sum(len(s["subs"]) for s in list_secs)

    # Kategorie-Grafiken
    IMG.mkdir(parents=True, exist_ok=True)
    tiles = []
    for i, s in enumerate(list_secs + tail_secs):
        (IMG / f"cat-{s['id']}.svg").write_text(cat_art(i + 1, s["title"], CAT_ICON.get(s["id"], "box"), i % 2 == 0), encoding="utf-8")
    for i, s in enumerate(list_secs):
        n = sum(1 for _ in all_items([s]))
        tiles.append(f'<a class="cat-tile reveal" href="#{s["id"]}"><img src="img/cat-{s["id"]}.svg" alt="" loading="lazy"><span class="t">{html.escape(s["title"])}<small>{n} Tools · {len(s["subs"]) or 1} Bereiche</small></span></a>')

    rail = "".join(f'<a href="#{s["id"]}">{icon(CAT_ICON.get(s["id"], "box"))}{html.escape(s["title"])}</a>' for s in list_secs + tail_secs)
    finder = dict(STACKS["finder"], to=LEAD_TO, next=SITE_URL + "danke.html")
    tools_js = json.dumps(tools_map, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    finder_js = json.dumps(finder, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": SITE_URL, "url": SITE_URL, "name": TITLE, "description": DESCRIPTION, "inLanguage": "de-DE",
         "isBasedOn": "https://github.com/mahseema/awesome-ai-tools",
         "publisher": {"@type": "Organization", "name": "KI-Werkstatt", "url": SITE_URL},
         "citation": {"@type": "CreativeWork", "name": "PROMPTGOTT", "url": SUBSTACK}},
        {"@type": "ItemList", "name": "KI-Tools auf Deutsch", "numberOfItems": n_tools,
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": it["name"], "url": it["url"], "description": item_meta(it)[2]}
                             for i, it in enumerate(uniq.values())]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": "Was bedeutet das EU-Zeichen bei einem Tool?", "acceptedAnswer": {"@type": "Answer", "text": "Der Anbieter hat seinen Firmensitz in der EU. Das ist ein Hinweis, keine Datenschutz-Prüfung. Für die DSGVO zählen Auftragsverarbeitungsvertrag, Serverstandort und Einstellungen."}},
            {"@type": "Question", "name": "Wie werden die Tools geprüft?", "acceptedAnswer": {"@type": "Answer", "text": f"Jeder Link wird per HTTP-Abfrage geprüft (letzter Link-Check: {LINK_CHECK}). Tote Links, Serverfehler und verschwundene Domains fliegen raus. Bot-Schutz (403) gilt als erreichbar."}},
            {"@type": "Question", "name": "Was ist der Stack-Check?", "acceptedAnswer": {"@type": "Answer", "text": BRAND["lead_offer"]["promise"]}},
        ]},
    ]}

    body = f"""{topbar()}
<section class="hero"><div class="hero-art">{hero_floats()}</div><div class="wrap">
<p class="kicker">{icon("wrench")} <b>KI-Werkstatt</b> · Link-Check {LINK_CHECK}: {LINK_CHECK_N} Links geprüft</p>
<h1><em>{n_tools} KI-Tools.</em><br>Geprüft. Sortiert.<br>Auf Deutsch.</h1>
<p class="sub">Jedes Tool in einem Satz erklärt. Tote Links raus. Anbieter aus der EU markiert. Dazu Werkzeugkisten für typische Fälle und ein Stack-Finder, der dir in drei Fragen sagt, womit du anfängst.</p>
<div class="ctas"><a class="btn btn-lime" href="#finder-band">{icon("compass")}Stack-Finder starten</a><a class="btn" href="#liste">{icon("layers")}Zur Liste</a><a class="btn" href="#stack-check">{icon("mail")}Kostenloser Stack-Check</a></div>
<div class="stats">
<div class="stat reveal"><b data-count="{n_tools}">0</b><span>geprüfte Tools</span></div>
<div class="stat reveal"><b data-count="{n_cats}">0</b><span>Kategorien, {n_subs} Unterbereiche</span></div>
<div class="stat reveal"><b data-count="{n_eu}">0</b><span>Anbieter mit Sitz in der EU</span></div>
<div class="stat reveal"><b data-count="{n_oss}">0</b><span>Open-Source-Tools</span></div>
<div class="stat reveal"><b data-count="{N_STACKS}">0</b><span>Werkzeugkisten</span></div>
</div></div></section>

<section class="band" id="favoriten"><div class="wrap">
<p class="eyebrow">Werkbank-Favoriten</p><h2>Ein Tool pro Aufgabe. Mehr brauchst du am Anfang nicht.</h2>
<p class="intro">Der schnelle Einstieg, bewusst mit Alternativen aus der EU. Wenn du nur zehn Minuten hast: hier anfangen.</p>
<ul class="tools">{featured_html}</ul>
</div></section>

<section class="band" id="so-arbeiten-wir"><div class="wrap">
<p class="eyebrow">So arbeitet die Werkstatt</p><h2>Sammeln. Prüfen. Sortieren.</h2>
<p class="intro">Kein Tool kommt auf die Werkbank, ohne dass jemand draufgeschaut hat. Tote Links sind keine Tools.</p>
<div class="steps">
<div class="step reveal"><span class="n">1</span>{icon("search")}<h3>Sammeln</h3><p>Grundlage ist die englische Awesome-Liste plus eigene Funde aus dem DACH-Raum. Jeder Eintrag bekommt einen deutschen Satz, der sagt, wofür das Tool taugt.</p></div>
<div class="step reveal"><span class="n">2</span>{icon("check")}<h3>Prüfen</h3><p>Jeder Link wird per HTTP abgefragt. 404, Serverfehler oder Domain weg: raus. Affiliate- und Referral-Parameter bei Tool-Links: raus. Nur Links zu PROMPTGOTT tragen UTM-Parameter, damit erkennbar ist, dass der Besuch von hier kam. Umbenannte Produkte: korrigiert.</p></div>
<div class="step reveal"><span class="n">3</span>{icon("layers")}<h3>Sortieren</h3><p>{n_cats} Kategorien nach Aufgabe, nicht nach Hype. EU-Sitz und Open Source als Badge. Werkzeugkisten für typische Fälle, damit du nicht {n_tools} Tools lesen musst.</p></div>
</div></div></section>

<section class="band" id="finder-band"><div class="wrap">
<p class="eyebrow">Stack-Finder</p><h2>Drei Fragen. Dann weißt du, womit du anfängst.</h2>
<p class="intro">Welches Werkzeug? Kommt drauf an, was du baust. Der Finder stellt dir ein Setup aus sechs bis acht Tools zusammen. Wenn du willst, schaut Jean danach noch mal drüber.</p>
<div class="finder reveal" id="finder"><p class="finder-q"></p><div class="opts"></div><div class="finder-result hidden"></div>
<div class="finder-bar"><button type="button" class="btn btn-sm back hidden">{icon("arrow")}Zurück</button><div class="dots"></div><span class="steplbl"></span></div></div>
</div></section>

<section class="band" id="werkzeugkisten"><div class="wrap">
<p class="eyebrow">Werkzeugkisten</p><h2>Fertige Stacks für typische Fälle</h2>
<p class="intro">{N_STACKS} Kisten mit je {STACK_SIZE_TXT} Tools, die zusammenpassen, mit einem Satz, warum jedes drin ist. Nimm die Kiste als Startpunkt, nicht als Vorschrift.</p>
<div class="stacks">{stacks_html}</div>
</div></section>

<section class="band" id="kategorien"><div class="wrap">
<p class="eyebrow">Die Schubladen</p><h2>{n_cats} Kategorien, {n_tools} Tools</h2>
<p class="intro">Jede Schublade hat eine Nummer. Klick rein oder nutz die Suche oben.</p>
<div class="catgrid">{"".join(tiles)}</div>
</div></section>

<div class="wrap layout" id="liste">
<aside class="rail"><div class="in"><h4>Kategorien</h4>{rail}
<div style="margin-top:14px;display:grid;gap:6px"><label style="display:flex;gap:8px;align-items:center;font-size:13px"><input type="checkbox" class="f-eu"> nur Anbieter aus der EU</label><label style="display:flex;gap:8px;align-items:center;font-size:13px"><input type="checkbox" class="f-oss"> nur Open Source</label></div>
<div class="lead-mini"><b>Stack-Check</b><p>Sag, was du baust. Du bekommst ein Setup aus 4 bis 6 Tools per Mail. Kostenlos.</p><a class="btn btn-sm" href="#stack-check">{icon("mail")}Anfragen</a></div></div></aside>
<main class="content"><div class="filters"><label><input type="checkbox" class="f-eu"> nur EU-Anbieter</label><label><input type="checkbox" class="f-oss"> nur Open Source</label></div>{list_html}</main>
</div>

<section class="band pg" id="promptgott"><div class="wrap">
<p class="eyebrow">PROMPTGOTT Deep Dives</p><h2>Werkzeug ist das eine. Systeme bauen das andere.</h2>
<p class="intro">{inline(pg_intro)}</p>
<div class="pg-grid">{pg_cards}</div>
<p style="margin-top:24px"><a class="btn btn-pg" href="{SUBSTACK}subscribe?{UTM}" target="_blank" rel="noopener">{icon("flame")}PROMPTGOTT abonnieren</a></p>
</div></section>

<section class="band lead" id="stack-check"><div class="wrap">
<div class="lead-grid"><div>
<p class="eyebrow">Stack-Check</p><h2>Sag, was du baust. Du bekommst ein Setup.</h2>
<p class="intro">{html.escape(BRAND["lead_offer"]["promise"])}</p>
<ul>
<li>{icon("check")}<span><b>Was du bekommst:</b> 4 bis 6 Tools, die zu deinem Fall passen, mit je einem Satz, warum.</span></li>
<li>{icon("check")}<span><b>Was es kostet:</b> nichts. Keine Beratungsstunde, kein Vertrag, kein Pitch.</span></li>
<li>{icon("check")}<span><b>Was wir nicht versprechen:</b> Preise oder DSGVO-Freigaben. Das prüfst du beim Anbieter.</span></li>
<li>{icon("shield")}<span><b>Deine Daten:</b> gehen über den Formulardienst FormSubmit (speichert Einsendungen 30 Tage) per Mail an Jean. Kein CRM, keine Liste. <a href="datenschutz.html">Details</a>.</span></li>
</ul></div>
<div>{lead_form("Hauptformular", "Stack-Check – KI-Werkstatt")}</div></div>
</div></section>

<div class="wrap" style="padding-top:48px">{tail_html}</div>
{footer()}
<script>window.KW_TOOLS={tools_js};window.KW_FINDER={finder_js};</script>
"""
    ld_js = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    extra = f'<script type="application/ld+json">{ld_js}</script>'
    (DOCS / "index.html").write_text(page_shell(TITLE, body, extra_head=extra), encoding="utf-8")
    return uniq, n_tools, n_cats


def build_subpages():
    danke = f"""{topbar(False)}
<div class="page"><p class="eyebrow">Angekommen</p><h1>Danke. Jean schaut drauf.</h1>
<p>Deine Anfrage ist raus. Du bekommst eine Antwort per Mail, meist innerhalb weniger Tage. Wenn du nichts hörst: Spam-Ordner prüfen oder direkt an <a href="mailto:{LEAD_TO}">{LEAD_TO}</a> schreiben.</p>
<p><a class="btn btn-lime" href="tools.csv" download>{icon("download")}Die Liste als CSV laden</a> <a class="btn" href="tools.json" download>{icon("download")}JSON</a></p>
<p>Bis dahin: <a href="{SUBSTACK}?{UTM}" target="_blank" rel="noopener">PROMPTGOTT</a> zeigt, wie man aus Tools Systeme baut. Und die <a href="{SITE_URL}#werkzeugkisten">Werkzeugkisten</a> sind ein guter Startpunkt.</p>
<p><a href="{SITE_URL}">Zurück zur Werkstatt</a></p></div>
<footer><div class="wrap"><p><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></p></div></footer>"""
    (DOCS / "danke.html").write_text(page_shell("Danke – KI-Werkstatt", danke, "Anfrage angekommen.", SITE_URL + "danke.html", '<meta name="robots" content="noindex">'), encoding="utf-8")

    needs = '<p class="needs"><b>[NEEDS_REVIEW]</b> Platzhalter. Vor dem Veröffentlichen eintragen und rechtlich prüfen lassen. Eine Seite mit Kontaktformular und geschäftlichem Zweck braucht in Deutschland ein vollständiges Impressum (§ 5 DDG) und eine Datenschutzerklärung (Art. 13 DSGVO).</p>'
    impressum = f"""{topbar(False)}
<div class="page"><p class="eyebrow">Rechtliches</p><h1>Impressum</h1>{needs}
<p><b>Angaben gemäß § 5 DDG</b><br>[NAME, VORNAME]<br>[STRASSE, HAUSNUMMER]<br>[PLZ, ORT]<br>Deutschland</p>
<p><b>Kontakt</b><br>E-Mail: {LEAD_TO}<br>[TELEFON, optional]</p>
<p><b>Verantwortlich für den Inhalt</b> nach § 18 Abs. 2 MStV: [NAME, ANSCHRIFT wie oben]</p>
<p><b>Umsatzsteuer</b>: [USt-IdNr., falls vorhanden, sonst Zeile löschen]</p>
<p><b>Haftung für Links:</b> Die Liste enthält Links zu externen Websites, auf deren Inhalte wir keinen Einfluss haben. Für diese Inhalte ist der jeweilige Anbieter verantwortlich. Links werden regelmäßig auf Erreichbarkeit geprüft, nicht auf Inhalt.</p>
<p><b>Quelle:</b> Die Liste basiert auf <a href="https://github.com/mahseema/awesome-ai-tools">Awesome AI Tools</a> (MIT-Lizenz). Tool-Logos werden als Favicons vom jeweiligen Anbieter geladen; Marken und Logos gehören den jeweiligen Inhabern.</p>
<p><a href="{SITE_URL}">Zurück zur Werkstatt</a></p></div>
<footer><div class="wrap"><p><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></p></div></footer>"""
    (DOCS / "impressum.html").write_text(page_shell("Impressum – KI-Werkstatt", impressum, "Impressum der KI-Werkstatt.", SITE_URL + "impressum.html", '<meta name="robots" content="noindex">'), encoding="utf-8")

    ds = f"""{topbar(False)}
<div class="page"><p class="eyebrow">Rechtliches</p><h1>Datenschutz</h1>{needs}
<p><b>Verantwortlicher:</b> [NAME, ANSCHRIFT wie im Impressum], E-Mail: {LEAD_TO}</p>
<h3>Hosting</h3><p>Die Seite wird über GitHub Pages ausgeliefert (GitHub, Inc., USA). Beim Aufruf verarbeitet GitHub technisch notwendige Daten wie IP-Adresse und Zeitpunkt des Zugriffs. Details: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">GitHub-Datenschutzerklärung</a>. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer sicheren Auslieferung). [NEEDS_REVIEW: Hinweis auf Drittlandübermittlung und Data Privacy Framework ergänzen]</p>
<h3>Kontaktformulare (Stack-Check, CSV-Anfrage)</h3><p>Wenn du ein Formular absendest, werden deine Angaben (Name, E-Mail, optional Website, Rolle, Projektbeschreibung) über den Dienst FormSubmit (formsubmit.co) per E-Mail an {LEAD_TO} übermittelt. FormSubmit leitet die Daten per E-Mail weiter und speichert Einsendungen nach eigenen Angaben 30 Tage in einem Archiv (<a href="https://formsubmit.co/documentation" target="_blank" rel="noopener">Dokumentation</a>). [NEEDS_REVIEW: Anbieter, Sitz und Datenschutzerklärung von FormSubmit verlinken; prüfen, ob ein AVV nötig ist] Rechtsgrundlage: deine Einwilligung (Art. 6 Abs. 1 lit. a DSGVO), die du mit dem Absenden erteilst und jederzeit per Mail widerrufen kannst. Die Daten werden nur zur Beantwortung deiner Anfrage genutzt, nicht in ein CRM oder einen Newsletter übernommen.</p>
<h3>Favicons der Tool-Anbieter</h3><p>Neben jedem Tool wird dessen Favicon über den Dienst icons.duckduckgo.com geladen. Dabei erfährt DuckDuckGo (USA) deine IP-Adresse und den Domainnamen des Tools. Die Icons werden erst geladen, wenn sie in den sichtbaren Bereich scrollen. [NEEDS_REVIEW: alternativ Icons lokal speichern oder nach Einwilligung laden]</p>
<h3>Schriften, Skripte, Speicher</h3><p>Schriften und Skripte liegen auf dieser Seite selbst; es werden keine Google Fonts von Google-Servern geladen. Im Browser-Speicher (localStorage) werden nur zwei Einstellungen abgelegt: dein Farbschema und ob du die untere Hinweisleiste geschlossen hast. Keine Cookies, kein Tracking, keine Analyse-Tools.</p>
<h3>Externe Links</h3><p>Links zu Tools, zu PROMPTGOTT (Substack) und zu GitHub führen auf fremde Seiten mit eigenen Datenschutzregeln. Links zu PROMPTGOTT enthalten UTM-Parameter, damit erkennbar ist, dass der Besuch von dieser Seite kam; persönliche Daten werden dabei nicht übertragen.</p>
<h3>Deine Rechte</h3><p>Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit, Widerspruch und Beschwerde bei einer Aufsichtsbehörde (Art. 15 bis 21, 77 DSGVO). Schreib dafür an {LEAD_TO}.</p>
<p><a href="{SITE_URL}">Zurück zur Werkstatt</a></p></div>
<footer><div class="wrap"><p><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></p></div></footer>"""
    (DOCS / "datenschutz.html").write_text(page_shell("Datenschutz – KI-Werkstatt", ds, "Datenschutzerklärung der KI-Werkstatt.", SITE_URL + "datenschutz.html", '<meta name="robots" content="noindex">'), encoding="utf-8")


def build_data(uniq, sections):
    rows = []
    for s, sub, it in all_items(sections):
        if uniq.get(it["url"]) is not it:
            continue
        eu, oss, clean = item_meta(it)
        rows.append({"name": it["name"], "url": it["url"], "beschreibung": clean, "kategorie": s["title"], "bereich": sub["title"] if sub else "", "eu": eu, "open_source": oss})
    (DOCS / "tools.json").write_text(json.dumps({"gebaut": TODAY, "link_check": LINK_CHECK, "quelle": REPO_URL, "tools": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    with (DOCS / "tools.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("ja" if v is True else "nein" if v is False else v) for k, v in r.items()})
    (DOCS / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                      f'<url><loc>{SITE_URL}</loc><lastmod>{date.today().isoformat()}</lastmod></url></urlset>\n', encoding="utf-8")
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    (DOCS / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#D7FF3C"/>'
                                      '<g transform="translate(10 10) scale(1.83)" fill="none" stroke="#0E1116" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                                      + icon_body("wrench") + "</g></svg>", encoding="utf-8")


def build_og(n_tools, n_cats):
    og = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><link rel="stylesheet" href="assets/fonts.css"><style>
body{{margin:0;width:1200px;height:630px;background:#0E1116;color:#ECEAE3;font-family:'IBM Plex Sans',sans-serif;position:relative;overflow:hidden;
background-image:linear-gradient(rgba(215,255,60,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(215,255,60,.08) 1px,transparent 1px);background-size:40px 40px}}
.m{{position:absolute;left:72px;top:64px;display:flex;align-items:center;gap:16px;font:700 26px 'Space Grotesk';letter-spacing:.06em}}
.m i{{width:52px;height:52px;border-radius:14px;background:#D7FF3C;display:grid;place-items:center}}
h1{{position:absolute;left:72px;top:170px;margin:0;font:700 96px/1.02 'Space Grotesk';letter-spacing:-.03em;width:900px}}
h1 em{{font-style:normal;color:#D7FF3C}}
p{{position:absolute;left:72px;top:470px;margin:0;font:400 28px 'IBM Plex Sans';color:#B8BDC6;width:900px}}
.s{{position:absolute;right:72px;top:64px;font:500 18px 'IBM Plex Mono';color:#D7FF3C;letter-spacing:.1em}}
svg.w{{position:absolute;right:-60px;bottom:-80px;width:520px;height:520px;fill:none;stroke:#D7FF3C;stroke-width:.6;opacity:.35;stroke-linecap:round;stroke-linejoin:round}}
</style></head><body>{ICONS}
<div class="m"><i><svg width="30" height="30" fill="none" stroke="#0E1116" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><use href="#i-wrench"/></svg></i>KI-WERKSTATT</div>
<div class="s">LINK-CHECK {LINK_CHECK}</div>
<h1><em>{n_tools} KI-Tools.</em><br>Geprüft. Sortiert.<br>Auf Deutsch.</h1>
<p>Jedes Tool in einem Satz. Tote Links raus. EU-Anbieter markiert. {n_cats} Kategorien, Werkzeugkisten, Stack-Finder.</p>
<svg class="w" viewBox="0 0 24 24">{icon_body("wrench")}</svg>
</body></html>"""
    (DOCS / "og.html").write_text(og, encoding="utf-8")
    # og.png aus og.html rendern, damit Social-Vorschau und Seite dieselben Zahlen zeigen
    if shutil.which("node"):
        env = dict(os.environ, NODE_PATH=os.environ.get("NODE_PATH") or subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
        r = subprocess.run(["node", str(ROOT / "scripts" / "render_og.js")], env=env, capture_output=True, text=True)
        if r.returncode:
            print("WARNUNG: og.png nicht aktualisiert (" + r.stderr.strip().splitlines()[-1] + "). Manuell: node scripts/render_og.js")
    else:
        print("WARNUNG: node fehlt, og.png nicht aktualisiert. Manuell: node scripts/render_og.js")


def main():
    sections, head_md = parse(SRC.read_text(encoding="utf-8"))
    uniq, n_tools, n_cats = build_index(sections, head_md)
    build_subpages()
    build_data(uniq, sections)
    build_og(n_tools, n_cats)
    print(f"docs/index.html: {n_tools} Tools, {n_cats} Kategorien, {len(list(IMG.glob('cat-*.svg')))} Grafiken")


if __name__ == "__main__":
    main()
