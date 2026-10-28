#!/usr/bin/env python3
"""Baut die KI-Werkstatt-Seite (docs/) aus README.de.md.

Keine Abhängigkeiten, nur Python 3.8+. Aufruf aus dem Repo-Root:
    python3 scripts/build_de_page.py

Quellen:  README.de.md (Tool-Liste), brand/ki-werkstatt.json (Marke),
          data/stacks.json (Werkzeugkisten + Stack-Finder), data/rechner.json (Zeitspar-Rechner),
          data/glossar.json (KI-Glossar), data/kategorien.json (eigene Texte je Kategorie-Seite),
          scripts/template/icons.svg
Ausgabe:  docs/index.html, docs/ki-tools-*.html (eine Seite je Kategorie), docs/ki-glossar.html,
          docs/404.html, docs/danke.html, docs/impressum.html, docs/datenschutz.html, docs/img/*.svg,
          docs/tools.json, docs/tools.csv, docs/sitemap.xml, docs/robots.txt
README.de.md bleibt die einzige Quelle für die Liste; docs/ nie von Hand bearbeiten.
Am Ende prüft scripts/check_unique.py, dass kein Satz auf zwei Seiten steht.
"""
import csv
import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "README.de.md"
DOCS = ROOT / "docs"
IMG = DOCS / "img"
BRAND = json.loads((ROOT / "brand" / "ki-werkstatt.json").read_text(encoding="utf-8"))
STACKS = json.loads((ROOT / "data" / "stacks.json").read_text(encoding="utf-8"))
RECHNER = json.loads((ROOT / "data" / "rechner.json").read_text(encoding="utf-8"))
GLOSSAR = json.loads((ROOT / "data" / "glossar.json").read_text(encoding="utf-8"))
KAT = json.loads((ROOT / "data" / "kategorien.json").read_text(encoding="utf-8"))
TRENDS = json.loads((ROOT / "data" / "trends.json").read_text(encoding="utf-8"))
NEU = json.loads((ROOT / "data" / "neu.json").read_text(encoding="utf-8"))
EINSATZ = json.loads((ROOT / "data" / "einsatz.json").read_text(encoding="utf-8"))
RATGEBER = json.loads((ROOT / "data" / "ratgeber.json").read_text(encoding="utf-8"))
RG_DIR = ROOT / "content" / "ratgeber"
ZAHLWORT = {2: "Zwei", 3: "Drei", 4: "Vier", 5: "Fünf", 6: "Sechs", 7: "Sieben", 8: "Acht", 9: "Neun", 10: "Zehn", 11: "Elf", 12: "Zwölf"}
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
from check_links import all_urls, url_hash  # noqa: E402  (gleiche Linkliste wie der Checker)
if _LC.get("urls_sha256") != url_hash(all_urls(SRC.read_text(encoding="utf-8"))):
    raise SystemExit("Abbruch: Die Links in README.de.md, data/rechner.json oder data/trends.json haben sich seit dem letzten Link-Check geändert. Erst scripts/check_links.py laufen lassen.")
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
# H1 der Kategorie-Seiten (sonst "KI-Tools: <Titel>")
CAT_H1 = {
    "text-und-sprache": "KI-Tools für Text und Sprache", "automatisierung-und-ki-agenten": "KI-Tools für Automatisierung und Agenten",
    "entwickler-tools-und-llmops": "KI-Entwickler-Tools und LLMOps", "programmieren-mit-ki": "Programmieren mit KI",
    "bilder": "KI-Tools für Bilder", "video": "KI-Tools für Video", "audio": "KI-Tools für Audio",
    "marketing-und-seo": "KI-Tools für Marketing und SEO", "ki-telefonagenten": "KI-Telefonagenten", "weitere-ki-tools": "Weitere KI-Tools",
}
GLOSSAR_PAGE = "ki-glossar.html"
TRENDS_PAGE = "ki-trends.html"
# NEU-Badge: gilt ab "seit" für genau NEU["tage"] Tage (seit <= heute < seit + tage); vorher und danach kein Badge
NEU_AKTIV = [t for t in NEU["tools"] if date.fromisoformat(t["seit"]) <= date.today() < date.fromisoformat(t["seit"]) + timedelta(days=NEU["tage"])]
NEU_NAMES = {t["name"] for t in NEU_AKTIV}
NEU_BADGE = '<span class="badge neu" title="Neu in der Liste">NEU</span>'


def cat_page(sec_id):
    return f"ki-tools-{sec_id}.html"


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


def inline(text, site=False):
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
        elif not href.startswith("http") and not site:
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
    # Versalien in Space Grotesk sind etwa 0,7 em breit; links bleiben rund 480 px bis zum Kreis
    fs = min(44, int(480 / (0.64 * max(1, len(name)))))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" role="img" aria-label="{html.escape(name)}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>
<pattern id="p" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{ink}" stroke-opacity=".14"/></pattern></defs>
<rect width="800" height="300" fill="url(#g)"/><rect width="800" height="300" fill="url(#p)"/>
<circle cx="640" cy="150" r="120" fill="none" stroke="{ink}" stroke-opacity=".25" stroke-width="2"/>
<circle cx="640" cy="150" r="80" fill="none" stroke="{ink}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 8"/>
<g transform="translate(560 70) scale(6.7)" fill="none" stroke="{ink}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">{g}</g>
<g transform="translate(40 40) scale(2.2)" fill="none" stroke="{ink}" stroke-opacity=".5" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{g}</g>
<text x="40" y="250" font-family="IBM Plex Mono, ui-monospace, monospace" font-size="18" font-weight="500" fill="{ink}" fill-opacity=".85" letter-spacing="3">SCHUBLADE {idx:02d}</text>
<text x="40" y="200" font-family="Space Grotesk, system-ui, sans-serif" font-size="{fs}" font-weight="700" fill="{ink}">{html.escape(name.upper())}</text>
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
                    '<span class="badge oss" title="Open Source">OSS</span>' if oss else "") + (NEU_BADGE if it["name"] in NEU_NAMES else "")
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


def render_section(sec, idx, tools_map, page_link=False):
    ico = CAT_ICON.get(sec["id"], "box")
    n = len(sec_items(sec))  # eindeutige Tools, wie Kategorie-Seite und Kacheln
    art = f'<div class="cat-art reveal"><img src="img/cat-{sec["id"]}.svg" alt="" loading="lazy" width="800" height="300"></div>' if n else ""
    body = [render_blocks(sec["blocks"], sec["id"], None, tools_map)]
    for sub in sec["subs"]:
        sico = SUB_ICON.get(sub["id"])
        body.append(f'<h3 id="{sub["id"]}">{icon(sico) if sico else ""}{inline(sub["title"])}</h3>')
        body.append(render_blocks(sub["blocks"], sec["id"], sub["id"], tools_map))
    count = f'<span class="count">{n} TOOLS</span>' if n else ""
    if page_link:
        count += f'<a class="more" href="{cat_page(sec["id"])}" title="Eigene Seite: {html.escape(sec["title"])}">Seite{icon("arrow")}</a>'
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


def render_stacks(tools_map, stacks=None):
    out = []
    for st in (STACKS["stacks"] if stacks is None else stacks):
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
        out.append(f'<article class="stack reveal" id="kiste-{st["id"]}"><div class="head">{icon(st["icon"])}<div><h3>{html.escape(st["title"])}</h3>'
                   f'<p class="for">{html.escape(st["for"])}</p></div></div><ol>{"".join(lis)}</ol>{pg}</article>')
    return "".join(out)


ROLLEN_FORM = ["Selbstständig / Freelancer", "Marketing / SEO", "Shop-Betreiber", "Entwickler / Maker", "Kundenservice / Vertrieb",
               "Content / Social Media", "Büro / Geschäftsführung", "Agentur", "Anderes"]


def lead_form(source, subject, compact=False, rolle=""):
    nxt = SITE_URL + "danke.html"
    if rolle and rolle not in ROLLEN_FORM:
        raise SystemExit(f"lead_form: unbekannte Rolle {rolle!r}")
    opts = "".join(f"<option{' selected' if r == rolle else ''}>{r}</option>" for r in ROLLEN_FORM)
    return f"""<form class="form" action="https://formsubmit.co/{LEAD_TO}" method="POST">
<input type="hidden" name="_subject" value="{html.escape(subject)}"><input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="{nxt}">
<input type="hidden" name="quelle" value="{html.escape(source)}">
<input type="text" name="_honey" class="honey" tabindex="-1" autocomplete="off">
<input type="hidden" name="merkliste" id="l-merk" value=""><input type="hidden" name="rechner" id="l-rechner" value=""><input type="hidden" name="radar" id="l-radar" value="">
<div class="row"><div><label for="l-name">Name</label><input id="l-name" name="name" required autocomplete="name"></div>
<div><label for="l-mail">E-Mail</label><input id="l-mail" type="email" name="email" required autocomplete="email"></div></div>
<div class="row"><div><label for="l-web">Website oder Shop (optional)</label><input id="l-web" name="website" placeholder="https://" autocomplete="url"></div>
<div><label for="l-rolle">Du bist</label><select id="l-rolle" name="rolle">{opts}</select></div></div>
<label for="l-proj">Was baust du gerade, und wo hakt es?</label><textarea id="l-proj" name="projekt" rows="4" required placeholder="Beispiel: Shop mit 2.000 Artikeln, Produkttexte in DE/EN/NL, ein Mensch für alles."></textarea>
<div class="attach hidden" id="l-attach-merk">{icon("bookmark")}<span></span><button type="button" data-clear="l-merk">entfernen</button></div>
<div class="attach hidden" id="l-attach-rechner">{icon("clock")}<span></span><button type="button" data-clear="l-rechner">entfernen</button></div>
<div class="attach hidden" id="l-attach-radar">{icon("chart")}<span></span><button type="button" data-clear="l-radar">entfernen</button></div>
<label class="consent"><input type="checkbox" name="einwilligung" value="ja" required><span>Ich bin einverstanden, dass meine Angaben per E-Mail an Jean Maurice Port übermittelt werden, um meine Anfrage zu beantworten. Details in der <a href="datenschutz.html">Datenschutzerklärung</a>.</span></label>
<button class="btn" type="submit">{icon("mail")}Stack-Check anfragen</button>
<p class="hint">Antwort kommt per Mail, meist innerhalb weniger Tage. Oder direkt an <a href="mailto:{LEAD_TO}?subject=Stack-Check">{LEAD_TO}</a>.</p>
</form>"""


def absolutize(doc, base):
    """Relative href/src auf den Seitenpfad umschreiben. Ersatz für <base>, das Fragment-Verweise wie
    <use href="#i-wrench"> auf die Startseite umbiegen würde."""
    def fix(m):
        url = m.group(2)
        if re.match(r"(https?:|mailto:|#|/|data:)", url):
            return m.group(0)
        return f'{m.group(1)}="{base}{url[2:] if url.startswith("./") else url}"'
    return re.sub(r'\b(href|src)="([^"]*)"', fix, doc)


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
<link rel="alternate" type="application/atom+xml" title="KI-Werkstatt: Trends und Neuzugänge" href="{SITE_URL}feed.xml">
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


def topbar(with_search=True, here=""):
    home = "" if here == "index" else "./"
    nav_items = [("kategorien", f"{home}#kategorien", "Schubladen"), ("rechner", f"{home}#rechner", "Rechner"), ("trends", TRENDS_PAGE, "Trends"), ("ratgeber", f"{home}#ratgeber", "Ratgeber"), ("glossar", GLOSSAR_PAGE, "Glossar")]
    cur = ' aria-current="page"'
    nav = '<nav class="mainnav" aria-label="Seiten">' + "".join(
        f'<a href="{href}"{cur if key == here else ""}>{label}</a>' for key, href, label in nav_items) + "</nav>"
    search = ('<form id="searchform" role="search"><label class="sr" for="q">Tools durchsuchen</label>'
              '<input type="search" id="q" placeholder="Suchen: übersetzen, Podcast, SEO, Shop …" autocomplete="off"></form>') if with_search else ""
    return f"""<header class="topbar"><div class="wrap in">
<a class="logo" href="./"><span class="mark">{icon("wrench")}</span><span>KI-WERKSTATT</span></a>
{search}{nav}
<div class="tools">{'<span id="count" class="badge hide-m" aria-live="polite"></span>' if with_search else ''}
<button class="iconbtn" id="theme" type="button" title="Hell/Dunkel umschalten">{icon("sun")}</button>
<a class="btn btn-lime btn-sm hide-m" href="{'' if here != 'sub' else './'}#stack-check">{icon("mail")}Stack-Check</a></div>
</div><div id="progress"></div></header>"""


def footer(fab_href="#stack-check"):
    return f"""<footer><div class="wrap">
<div class="cols">
<div><h4>KI-Werkstatt</h4><p style="margin:0">{html.escape(BRAND["claim"])} Geprüft. Sortiert. Auf Deutsch.</p></div>
<div><h4>Projekt</h4><ul><li><a href="{REPO_URL}">GitHub-Repository</a></li><li><a href="{REPO_URL}/blob/main/README.de.md">Liste als Markdown</a></li><li><a href="{REPO_URL}/blob/main/README.md">About (English)</a></li><li><a href="tools.csv">Liste als CSV</a> · <a href="tools.json">JSON</a></li><li><a href="feed.xml">Trends als Feed (Atom)</a></li></ul></div>
<div><h4>Werkstatt</h4><ul><li><a href="./#kategorien">Alle Schubladen</a></li><li><a href="./#rechner">Zeitspar-Rechner</a></li><li><a href="./#einsatz">KI nach Einsatzgebiet</a></li><li><a href="./#ratgeber">Ratgeber</a></li><li><a href="{TRENDS_PAGE}">KI-Trends</a></li><li><a href="{GLOSSAR_PAGE}">KI-Glossar</a></li><li><a href="./#finder-band">Stack-Finder</a></li></ul></div>
<div><h4>Praxis</h4><ul><li><a href="{SUBSTACK}?{UTM}" target="_blank" rel="noopener">PROMPTGOTT auf Substack</a></li><li><a href="{SUBSTACK}subscribe?{UTM}" target="_blank" rel="noopener">Newsletter abonnieren</a></li></ul></div>
<div><h4>Rechtliches</h4><ul><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li><li><a href="{REPO_URL}/blob/main/LICENSE">MIT-Lizenz</a></li></ul></div>
</div>
<p>Letzter Link-Check: {LINK_CHECK} ({LINK_CHECK_N} Links). Seite gebaut am {TODAY}. Tool-Logos werden als Favicons der jeweiligen Anbieter geladen; die Rechte liegen bei den Anbietern.</p>
</div></footer>
<button id="totop" type="button" title="Nach oben">{icon("up")}</button>
<a class="btn btn-lime fab" href="{fab_href}">{icon("mail")}Stack-Check</a>
<div class="stickybar" id="stickybar"><div class="wrap in">
<div><b>Die Liste als CSV per Mail</b><small>Eine Mail mit dem Download und dem Überblick über die {N_STACKS} Werkzeugkisten. Kein Newsletter-Dauerfeuer.</small></div>
<form action="https://formsubmit.co/{LEAD_TO}" method="POST"><input type="hidden" name="_subject" value="CSV-Anfrage – KI-Werkstatt"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_template" value="table"><input type="hidden" name="_next" value="{SITE_URL}danke.html"><input type="hidden" name="quelle" value="Sticky-Leiste"><input type="text" name="_honey" class="honey" tabindex="-1" autocomplete="off">
<label class="sr" for="sb-mail">E-Mail</label><input id="sb-mail" type="email" name="email" placeholder="deine@mail.de" required><button class="btn btn-lime btn-sm" type="submit">Schicken</button><label class="sb-consent"><input type="checkbox" name="einwilligung" value="ja" required> Einverstanden, dass meine E-Mail über FormSubmit an Jean Maurice Port geht. <a href="datenschutz.html">Datenschutz</a></label></form>
<button class="close" type="button" title="Schließen">{icon("x")}</button>
</div></div>
<button id="merk-pill" class="merk-pill hidden" type="button" aria-controls="merk" aria-expanded="false">{icon("bookmark")}Merkliste <b id="merk-n">0</b></button>
<div id="merk" class="merk" role="dialog" aria-labelledby="merk-h" hidden>
<div class="merk-head"><h3 id="merk-h">{icon("bookmark")}Deine Merkliste</h3><button class="close" type="button" title="Schließen">{icon("x")}</button></div>
<p class="merk-empty">Noch leer. Klick bei einem Tool auf das Lesezeichen.</p>
<ol class="merk-list"></ol>
<div class="merk-actions"><button type="button" class="btn btn-lime btn-sm" id="merk-send">{icon("mail")}Jean drüberschauen lassen</button><button type="button" class="btn btn-sm" id="merk-copy">{icon("copy")}Kopieren</button><button type="button" class="btn btn-sm" id="merk-clear">{icon("trash")}Leeren</button></div>
<p class="merk-note">Die Merkliste liegt nur in deinem Browser. An Jean geht sie erst, wenn du das Stack-Check-Formular abschickst.</p>
</div>"""


# --------------------------------------------------------------------------- Kurbel, der Werkstatt-Roboter
def kurbel(cls="", wink=False, label="Kurbel, der Werkstatt-Roboter"):
    eye_r = ('<path d="M68 42h10"/>' if wink else '<circle cx="73" cy="42" r="4.5" fill="currentColor" stroke="none"/>')
    return f"""<svg class="kurbel {cls}" viewBox="0 0 130 124" role="img" aria-label="{html.escape(label)}">
<g class="kb-ant"><path d="M60 22V11" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><circle cx="60" cy="8" r="4.5" class="kb-spark"/>
<path d="M50 5l-4-3M70 5l4-3M60-3v0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></g>
<g class="kb-bob" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
<rect x="30" y="22" width="60" height="44" rx="14" class="kb-head"/>
<circle cx="47" cy="42" r="4.5" fill="currentColor" stroke="none"/>{eye_r}
<path d="M48 54q12 8 24 0"/>
<circle cx="38" cy="53" r="3" class="kb-cheek" stroke="none"/><circle cx="82" cy="53" r="3" class="kb-cheek" stroke="none"/>
<path d="M54 66v6M66 66v6"/>
<rect x="36" y="72" width="48" height="32" rx="10" class="kb-body"/>
<circle cx="60" cy="88" r="5"/><path d="M57 88h6"/>
<path d="M36 80q-12 4-14 16"/><path d="M84 80q10-2 15-12"/>
<g transform="translate(97 52) rotate(35)"><path d="M0 14V4"/><path d="M-5 4a5 5 0 1 1 10 0l-2 2h-6Z"/></g>
<path d="M48 104v10M72 104v10"/>
</g>
<g transform="translate(96 114) rotate(-18)" class="kb-screw"><rect x="0" y="0" width="12" height="4.5" rx="1.5"/><rect x="11" y="-1.5" width="3.5" height="7.5" rx="1"/></g>
</svg>"""


# --------------------------------------------------------------------------- Hans Moritz, der Werkstattmeister
def hans(cls="", wink=False, label="Hans Moritz, der Werkstattmeister"):
    def eye(x, closed=False):
        if closed:
            return f'<path d="M{x-4.5} 61.5q4.5 3 9 0" fill="none" class="hm-ln" stroke-linecap="round"/>'
        return (f'<ellipse cx="{x}" cy="61" rx="4.8" ry="2.9" fill="#fff"/><circle cx="{x+.4}" cy="61.3" r="2.6" class="hm-iris"/>'
                f'<circle cx="{x+.4}" cy="61.3" r="1.15" fill="#1b1f26"/><circle cx="{x+1.2}" cy="60.4" r=".6" fill="#fff"/>'
                f'<path d="M{x-5.2} 59.6q5.2-2.6 10.4 0" fill="none" class="hm-ln" stroke-width="1.4" stroke-linecap="round"/>'
                f'<path d="M{x-5} 64.4q5 2 10 0" fill="none" stroke="#d99b7c" stroke-width="1" stroke-linecap="round"/>')
    def bud(x, d):
        return (f'<ellipse cx="{x}" cy="64.5" rx="3.6" ry="3.2" class="hm-bud"/>'
                f'<rect x="{x-1.5}" y="65.5" width="3" height="9.5" rx="1.5" class="hm-bud"/>')
    return f"""<svg class="hans {cls}" viewBox="0 0 140 160" role="img" aria-label="{html.escape(label)}">
<g class="hm-bob">
<path class="hm-jacket" d="M8 160q2-30 30-40l18-6h28l18 6q28 10 30 40Z"/>
<path d="M44 116q-22 6-28 30M96 116q22 6 28 30" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>
<path class="hm-skin" d="M57 92h26v20H57Z"/>
<path class="hm-collar" d="M52 103q18 7 36 0l3 15q-21 9-42 0Z"/>
<path d="M70 108v52" stroke="#c9ced8" stroke-width="1.6"/><rect x="68" y="109" width="4" height="7" rx="1.5" fill="#c9ced8"/>
<g transform="translate(52 130) rotate(-8)"><rect x="-7" y="-7" width="14" height="14" rx="3.5" fill="#D7FF3C"/><path d="M-3.5 3.5 3.5-3.5M-.5-3.5h4v4" fill="none" stroke="#0E1116" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>
<path d="M106 117 38 160" stroke="#14171c" stroke-width="8"/>
<path d="M44 160q-2-12 10-18l6 7q-8 4-8 11" fill="#efe6cf" stroke="#14171c" stroke-width="1.4"/>
<g class="hm-head">
<ellipse class="hm-skin hm-ln" cx="37.5" cy="66" rx="5.5" ry="8.5"/><ellipse class="hm-skin hm-ln" cx="102.5" cy="66" rx="5.5" ry="8.5"/>
<path class="hm-skin hm-ln" d="M41 62q-1-36 29-37q30 1 29 37q0 14-4 22H45q-4-8-4-22Z"/>
{bud(37.5, -1)}{bud(102.5, 1)}
<path class="hm-buzz" d="M42 52q2-25 28-26q26 1 28 26q-9-16-28-17q-19 1-28 16Z"/>
<path d="M57 40q13-3 26 0M60 45q10-2 20 0" fill="none" stroke="#d99b7c" stroke-width="1" stroke-linecap="round"/>
<path class="hm-beard" d="M41 60q-1 27 12 39q8 7 17 7t17-7q13-12 12-39q-3 12-10 17q-7-4-19-4t-19 4q-7-5-10-17Z"/>
<path class="hm-beard-d" d="M54 81q8-7 16-5q8-2 16 5q-8 3-16 1q-8 2-16-1Z"/>
<path d="M60 86.5q10 5.5 20-1" fill="none" stroke="#7a2f12" stroke-width="1.9" stroke-linecap="round"/>
<path d="M49.5 54q7.5-3.8 14-.6M76.5 53.4q6.5-3.2 14 .6" fill="none" stroke="#c8642a" stroke-width="2.5" stroke-linecap="round"/>
{eye(58)}{eye(82, wink)}
<path d="M51 62.5l-3 1.6M89 62.5l3 1.6" stroke="#d99b7c" stroke-width="1" stroke-linecap="round"/>
<path d="M70 61q-1.5 8-4.5 11q4.5 2.2 9 0" fill="none" stroke="#b9775a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<g fill="#d0865a" opacity=".75"><circle cx="52" cy="69" r=".8"/><circle cx="55.5" cy="71" r=".7"/><circle cx="50" cy="72" r=".6"/><circle cx="86" cy="69" r=".8"/><circle cx="89.5" cy="71.5" r=".7"/><circle cx="84" cy="72" r=".6"/><circle cx="66.5" cy="66" r=".55"/><circle cx="73.5" cy="66.5" r=".55"/></g>
</g>
</g>
</svg>"""


def eu_names(sec, limit=5):
    names = [it["name"] for it in sec_items(sec) if item_meta(it)[0]]
    if not names:
        return ""
    names = names[:limit]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " und " + names[-1]


def kat_text(sec, key):
    """Text aus data/kategorien.json mit Platzhaltern {n}, {subs}, {eu}."""
    raw = KAT[sec["id"]][key]
    eu = eu_names(sec)

    def fill(t):
        if "{eu}" in t and not eu:
            raise SystemExit(f"kategorien.json/{sec['id']}/{key}: {{eu}} benutzt, aber keine EU-Anbieter in dieser Schublade")
        return t.replace("{n}", str(len(sec_items(sec)))).replace("{subs}", str(max(1, len(sec["subs"])))).replace("{eu}", eu)
    if isinstance(raw, list):
        return [[fill(x) for x in r] if isinstance(r, list) else fill(r) for r in raw]
    return fill(raw)


def top_tools(sec, k=3):
    """Bekannte Tools zuerst: was in Favoriten oder Werkzeugkisten steht, dann der Rest."""
    known = {n for st in STACKS["stacks"] for n, _ in st["tools"]}
    its = sec_items(sec)
    return (sorted(its, key=lambda it: 0 if it["name"] in known else 1))[:k]


def faq_html(items):
    return "".join(f'<details class="faq-item reveal"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in items)


def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def build_index(sections, head_md):
    by_id = {s["id"]: s for s in sections}
    featured = by_id.pop("empfehlungen-der-redaktion", None)
    pg_sec = by_id.pop("promptgott-deep-dives", None)
    tail_ids = ["lernen-prompting-und-ki-grundlagen", "verwandte-listen", "mitmachen"]
    list_secs = [s for s in sections if s["id"] in by_id and s["id"] not in tail_ids]
    tail_secs = [by_id[i] for i in tail_ids if i in by_id]
    missing = [s["id"] for s in list_secs if s["id"] not in KAT]
    if missing:
        raise SystemExit(f"data/kategorien.json: Texte fehlen für {missing}")

    # Werkzeug-Verzeichnis für Finder und Kisten: sachliche Beschreibung aus der Kategorie, nicht der Favoriten-Gag
    tools_map = {}
    for s_, sub, it in all_items(list_secs + tail_secs):
        eu, oss, clean = item_meta(it)
        tools_map.setdefault(it["name"], {"u": it["url"], "d": clean, "eu": eu})
    tail_html = "".join(render_section(s, i + 1 + len(list_secs), tools_map) for i, s in enumerate(tail_secs))
    featured_html = render_featured(featured, tools_map) if featured else ""
    pg_intro, pg_cards = render_pg(pg_sec) if pg_sec else ("", "")
    stacks_html = render_stacks(tools_map)

    uniq = {}
    for s_, sub, it in all_items(sections):
        uniq.setdefault(it["url"], it)
    n_tools = len(uniq)
    n_eu = sum(1 for it in uniq.values() if item_meta(it)[0])
    n_oss = sum(1 for it in uniq.values() if item_meta(it)[1])
    n_cats = len(list_secs)
    n_subs = sum(len(s["subs"]) for s in list_secs)

    IMG.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(list_secs + tail_secs):
        (IMG / f"cat-{s['id']}.svg").write_text(cat_art(i + 1, s["title"], CAT_ICON.get(s["id"], "box"), i % 2 == 0), encoding="utf-8")
    drawers = []
    for i, s in enumerate(list_secs):
        its = sec_items(s)
        n_e = sum(1 for it in its if item_meta(it)[0])
        tops = "".join(f'<li>{favicon(it["url"])}<span>{html.escape(it["name"])}</span></li>' for it in top_tools(s))
        eu_txt = f" · {n_e} EU" if n_e else ""
        drawers.append(f"""<a class="drawer reveal" href="{cat_page(s['id'])}">
<span class="drawer-art"><img src="img/cat-{s['id']}.svg" alt="" loading="lazy" width="800" height="300"></span>
<span class="drawer-body"><span class="drawer-no">Schublade {i + 1:02d}</span><b class="drawer-title">{icon(CAT_ICON.get(s["id"], "box"))}{html.escape(s["title"])}</b>
<span class="drawer-teaser">{html.escape(kat_text(s, "teaser"))}</span>
<ul class="drawer-tools">{tops}</ul>
<span class="drawer-meta">{len(its)} Tools · {max(1, len(s["subs"]))} {"Bereiche" if len(s["subs"]) > 1 else "Bereich"}{eu_txt}</span><span class="drawer-cta">Schublade aufziehen{icon("arrow")}</span></span></a>""")

    finder = dict(STACKS["finder"], to=LEAD_TO, next=SITE_URL + "danke.html")
    tools_js = json.dumps(tools_map, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    finder_js = json.dumps(finder, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    faq = [
        ("Was bedeutet das EU-Zeichen bei einem Tool?", "Der Anbieter hat seinen Firmensitz in der EU. Das ist ein Hinweis, keine Datenschutz-Prüfung. Für die DSGVO zählen Auftragsverarbeitungsvertrag, Serverstandort und Einstellungen."),
        ("Wie prüft ihr die Tools?", f"Jeder Link wird per HTTP abgefragt, zuletzt am {LINK_CHECK}. Tote Links, Serverfehler und verschwundene Domains fliegen raus. Bot-Schutz gilt als erreichbar, denn dahinter steckt fast immer eine echte Seite."),
        ("Was kostet der Stack-Check?", "Nichts. Du schreibst, was du baust, und bekommst einen Vorschlag per Mail. Keine Beratungsstunde, kein Vertrag, kein Newsletter-Abo durch die Hintertür."),
        ("Wer ist Hans Moritz?", "Der Werkstattmeister der KI-Werkstatt: Glatze, roter Vollbart, Trainingsjacke, Earbuds im Ohr. Hans Moritz probiert jedes Werkzeug aus, bevor es in eine Schublade darf, und sagt dir in einem Satz, wofür es taugt."),
        ("Wer ist Kurbel?", "Der Werkstatt-Roboter von Hans Moritz. Hilfsbereit, gründlich und leicht schusselig, denn nach jeder Reparatur bleibt eine Schraube übrig. Du triffst Kurbel überall dort, wo es sonst leer wäre."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": SITE_URL, "url": SITE_URL, "name": TITLE, "description": DESCRIPTION, "inLanguage": "de-DE",
         "publisher": {"@type": "Organization", "name": "KI-Werkstatt", "url": SITE_URL},
         "citation": {"@type": "CreativeWork", "name": "PROMPTGOTT", "url": SUBSTACK}},
        {"@type": "ItemList", "name": "Die Schubladen der KI-Werkstatt", "numberOfItems": n_cats,
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["title"], "url": SITE_URL + cat_page(s["id"])}
                             for i, s in enumerate(list_secs)]},
        faq_ld(faq),
    ]}

    body = f"""{topbar(True, "index")}
<div class="searchpanel" id="searchpanel" hidden><div class="wrap">
<div class="sp-head"><b id="sp-count" aria-live="polite"></b><label><input type="checkbox" id="sp-eu"> nur EU</label><label><input type="checkbox" id="sp-oss"> nur Open Source</label><label><input type="checkbox" id="sp-neu"> nur neu</label><button class="close" type="button" title="Suche schließen">{icon("x")}</button></div>
<ol class="sp-list"></ol>
<div class="sp-empty hidden">{kurbel("kb-sm", wink=True)}<p><b>Die Schublade klemmt.</b> Zu diesem Wort hat Kurbel nichts gefunden. Probier ein anderes oder frag direkt beim <a href="#stack-check">Stack-Check</a>.</p></div>
</div></div>
<section class="hero"><div class="hero-art">{hero_floats()}</div><div class="wrap">
<div class="hero-hm" aria-hidden="true">{hans("hm-xl", label="")}<p class="bubble">Moin, ich bin Hans Moritz. Erst testen, dann empfehlen.</p></div>
<p class="kicker">{icon("wrench")} <b>KI-Werkstatt</b> · Link-Check {LINK_CHECK}: {LINK_CHECK_N} Links geprüft</p>
<h1><em>{n_tools} KI-Tools.</em><br>Geprüft. Sortiert.<br>Ohne Zauberstab.</h1>
<p class="sub">Hier gibt es kein Wundermittel, nur gutes Werkzeug: jedes Tool in einem Satz erklärt, tote Links aussortiert, EU-Anbieter markiert. Dazu Werkzeugkisten für typische Jobs und ein Stack-Finder, der schneller zum Punkt kommt als jedes Beratungsgespräch.</p>
<div class="ctas"><a class="btn btn-lime" href="#finder-band">{icon("compass")}Stack-Finder starten</a><a class="btn" href="#kategorien">{icon("layers")}Schubladen öffnen</a><a class="btn" href="#stack-check">{icon("mail")}Kostenloser Stack-Check</a></div>
<div class="stats">
<div class="stat reveal"><b data-count="{n_tools}">{n_tools}</b><span>geprüfte Tools</span></div>
<div class="stat reveal"><b data-count="{n_cats}">{n_cats}</b><span>Schubladen, {n_subs} Fächer</span></div>
<div class="stat reveal"><b data-count="{n_eu}">{n_eu}</b><span>Anbieter mit EU-Sitz</span></div>
<div class="stat reveal"><b data-count="{n_oss}">{n_oss}</b><span>Open-Source-Tools</span></div>
<div class="stat reveal"><b data-count="{N_STACKS}">{N_STACKS}</b><span>Werkzeugkisten</span></div>
</div></div></section>

<section class="band" id="favoriten"><div class="wrap">
<p class="eyebrow">Werkbank-Favoriten</p><h2>Zehn Werkzeuge für den Anfang. Mehr braucht kaum jemand.</h2>
<p class="intro">Wer nur zehn Minuten hat, fängt hier an. Bewusst mit Alternativen aus der EU, weil nicht jeder Schraubenschlüssel aus Kalifornien kommen muss.</p>
<ul class="tools">{featured_html}</ul>
</div></section>

{einsatz_band()}

{neu_band(list_secs)}

{ratgeber_band()}

<section class="band" id="so-arbeiten-wir"><div class="wrap">
<p class="eyebrow">So arbeitet die Werkstatt</p><h2>Sammeln. Prüfen. Sortieren.</h2>
<p class="intro">Kein Tool kommt auf die Werkbank, ohne dass es jemand in die Hand genommen hat. Tote Links sind keine Tools, sondern Staubfänger.</p>
<div class="steps">
<div class="step reveal"><span class="n">1</span>{icon("search")}<h3>Sammeln</h3><p>Gesammelt wird, was in Projekten, Fachartikeln und Herstellerankündigungen auftaucht, mit besonderem Blick auf den DACH-Raum. Jeder Eintrag bekommt einen deutschen Satz, der sagt, wofür das Tool taugt. Ohne Werbeprosa.</p></div>
<div class="step reveal"><span class="n">2</span>{icon("check")}<h3>Prüfen</h3><p>Jeder Link wird per HTTP abgeklopft. 404, Serverfehler oder Domain weg: ab in die Tonne. Affiliate- und Referral-Parameter bei Tool-Links fliegen auch raus. Nur Links zu PROMPTGOTT tragen UTM-Parameter, damit erkennbar ist, dass der Besuch von hier kam.</p></div>
<div class="step reveal"><span class="n">3</span>{icon("layers")}<h3>Sortieren</h3><p>{n_cats} Schubladen nach Aufgabe, nicht nach Hype. EU-Sitz und Open Source als Badge. Dazu Werkzeugkisten für typische Jobs, damit du nicht alle {n_tools} Tools einzeln anfassen musst.</p></div>
</div></div></section>

<section class="band" id="finder-band"><div class="wrap">
<p class="eyebrow">Stack-Finder</p><h2>Drei Fragen. Dann weißt du, womit du anfängst.</h2>
<p class="intro">Welches Werkzeug? Kommt drauf an, was du baust. Der Finder fragt kurz nach und legt dir sechs bis acht Tools auf die Werkbank. Wenn du magst, schaut Jean danach noch einmal drüber.</p>
<div class="finder reveal" id="finder"><p class="finder-q"></p><div class="opts"></div><div class="finder-result hidden"></div>
<div class="finder-bar"><button type="button" class="btn btn-sm back hidden">{icon("arrow")}Zurück</button><div class="dots"></div><span class="steplbl"></span></div></div>
</div></section>

<section class="band" id="werkzeugkisten"><div class="wrap">
<p class="eyebrow">Werkzeugkisten</p><h2>Fertig gepackte Kisten für typische Jobs</h2>
<p class="intro">{N_STACKS} Kisten mit je {STACK_SIZE_TXT} Tools, die zusammenpassen, und einem Satz, warum jedes drin liegt. Nimm die Kiste als Startpunkt, nicht als Bauanleitung.</p>
<div class="stacks">{stacks_html}</div>
</div></section>

{rechner_band()}

<section class="band" id="kategorien"><div class="wrap">
<p class="eyebrow">Die Schubladen</p><h2>{n_cats} Schubladen, {n_tools} Tools, eine Werkstatt</h2>
<p class="intro">Jede Schublade hat eine eigene Seite mit allen Tools, einem Werkstatt-Tipp und Antworten auf die Fragen, die uns am häufigsten gestellt werden. Such dir eine aus oder tipp oben ins Suchfeld, was du vorhast.</p>
<p class="sp-filters"><button type="button" class="btn btn-sm" data-sp="eu">{icon("globe")}Alle {n_eu} EU-Anbieter zeigen</button><button type="button" class="btn btn-sm" data-sp="oss">{icon("code")}Alle {n_oss} Open-Source-Tools zeigen</button>{f'<button type="button" class="btn btn-sm" data-sp="neu">{icon("plus")}Alle {len(NEU_AKTIV)} Neuzugänge zeigen</button>' if NEU_AKTIV else ""}</p>
<div class="drawers">{"".join(drawers)}
<a class="drawer drawer-gl reveal" href="{GLOSSAR_PAGE}"><span class="drawer-art gl-art">{icon("abc")}</span><span class="drawer-body"><span class="drawer-no">Nachschlagen</span><b class="drawer-title">{icon("book")}KI-Glossar</b>
<span class="drawer-teaser">Token, RAG, Halluzination: {len(GLOSSAR["begriffe"])} Begriffe, jeder mit ernster Erklärung und einer Werkstatt-Übersetzung zum Merken.</span>
<span class="drawer-cta">Glossar aufschlagen{icon("arrow")}</span></span></a></div>
</div></section>

<section class="band pg" id="promptgott"><div class="wrap">
<p class="eyebrow">PROMPTGOTT Deep Dives</p><h2>Werkzeug ist das eine. Systeme bauen das andere.</h2>
<p class="intro">{inline(pg_intro)}</p>
<div class="pg-grid">{pg_cards}</div>
<p style="margin-top:24px"><a class="btn btn-pg" href="{SUBSTACK}subscribe?{UTM}" target="_blank" rel="noopener">{icon("flame")}PROMPTGOTT abonnieren</a></p>
</div></section>

<section class="band faq" id="faq"><div class="wrap">
<p class="eyebrow">Fragen an der Werkbank</p><h2>Was Leute uns am Tresen fragen</h2>
<div class="faq-list">{faq_html(faq)}</div>
</div></section>

<section class="band lead" id="stack-check"><div class="wrap">
<div class="lead-grid"><div>
<p class="eyebrow">Stack-Check</p><h2>Sag, was du baust. Jean legt dir das Werkzeug hin.</h2>
<p class="intro">{html.escape(BRAND["lead_offer"]["promise"])}</p>
<ul>
<li>{icon("check")}<span><b>Was du bekommst:</b> 4 bis 6 Tools, die zu deinem Fall passen, mit je einem Satz, warum.</span></li>
<li>{icon("check")}<span><b>Was es kostet:</b> zwei Minuten fürs Formular. Kein Vertrag, kein Pitch.</span></li>
<li>{icon("check")}<span><b>Was wir nicht versprechen:</b> Preise oder DSGVO-Freigaben. Die prüfst du beim Anbieter.</span></li>
<li>{icon("shield")}<span><b>Deine Daten:</b> gehen über den Formulardienst FormSubmit (speichert Einsendungen 30 Tage) per Mail an Jean. Kein CRM, keine Liste. <a href="datenschutz.html">Details</a>.</span></li>
</ul>
<div class="kb-say hm-say">{hans("hm-md")}{kurbel("kb-sm", wink=True)}<p class="bubble">Ich such dir das Werkzeug raus. Kurbel hält solange die Schraube fest.</p></div></div>
<div>{lead_form("Hauptformular", "Stack-Check – KI-Werkstatt")}</div></div>
</div></section>

<div class="wrap" style="padding-top:48px">{tail_html}</div>
{footer()}
<script>window.KW_TOOLS={tools_js};window.KW_FINDER={finder_js};</script>
"""
    ld_js = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    extra = f'<script type="application/ld+json">{ld_js}</script>'
    (DOCS / "index.html").write_text(page_shell(TITLE, body, extra_head=extra), encoding="utf-8")
    return uniq, n_tools, n_cats, list_secs, tools_map


def build_subpages(list_secs=()):
    danke = f"""{topbar(False, "sub")}
<div class="page page-kb"><div class="kb-say kb-hero">{kurbel("kb-lg", wink=True)}<p class="bubble">Ich sortiere solange die Schrauben.</p></div>
<p class="eyebrow">Angekommen</p><h1>Danke. Deine Anfrage liegt auf der Werkbank.</h1>
<p>Jean schaut sie sich an und antwortet per Mail, meist innerhalb weniger Tage. Hörst du nichts, wirf einen Blick in den Spam-Ordner, manchmal versteckt sich die Post dort. Oder schreib direkt an <a href="mailto:{LEAD_TO}">{LEAD_TO}</a>.</p>
<p><a class="btn btn-lime" href="tools.csv" download>{icon("download")}Die Liste als CSV laden</a> <a class="btn" href="tools.json" download>{icon("download")}JSON</a></p>
<p>Zum Überbrücken: <a href="{SUBSTACK}?{UTM}" target="_blank" rel="noopener">PROMPTGOTT</a> zeigt, wie man aus Tools Systeme baut. Und in den <a href="./#werkzeugkisten">Werkzeugkisten</a> liegt schon ein Startpunkt bereit.</p>
<p><a href="./">Zurück in die Werkstatt</a></p></div>
<footer><div class="wrap"><p><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></p></div></footer>"""
    (DOCS / "danke.html").write_text(page_shell("Danke – KI-Werkstatt", danke, "Anfrage angekommen.", SITE_URL + "danke.html", '<meta name="robots" content="noindex">'), encoding="utf-8")

    # 404: GitHub Pages liefert docs/404.html für jede unbekannte Adresse aus, deshalb absolute Pfade
    base = urlparse(SITE_URL).path or "/"
    chips = "".join(f'<a class="chip" href="{cat_page(s["id"])}">{icon(CAT_ICON.get(s["id"], "box"))}{html.escape(s["title"])}</a>' for s in list_secs)
    nf = f"""{topbar(False, "sub")}
<div class="page page-kb"><div class="kb-say kb-hero">{kurbel("kb-lg")}<p class="bubble">Eine Schraube hab ich gefunden. Die Seite nicht.</p></div>
<p class="eyebrow">Fehler 404</p><h1>Diese Schublade gibt es nicht.</h1>
<p>Kurbel hat überall nachgesehen, sogar unter der Werkbank und hinter dem Kaffeeautomaten. Vielleicht hat sich die Adresse verschraubt, vielleicht ist die Seite umgezogen.</p>
<p>Von hier aus kommst du sicher weiter:</p>
<div class="chips nf-chips"><a class="chip cat" href="./">{icon("wrench")}Startseite</a>{chips}<a class="chip" href="{GLOSSAR_PAGE}">{icon("abc")}KI-Glossar</a></div>
<p style="margin-top:22px"><a class="btn btn-lime" href="./#stack-check">{icon("mail")}Jean direkt fragen</a></p></div>
<footer><div class="wrap"><p><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></p></div></footer>"""
    (DOCS / "404.html").write_text(absolutize(page_shell("Schublade nicht gefunden – KI-Werkstatt", nf, "Diese Seite gibt es nicht.", SITE_URL + "404.html",
                                                         '<meta name="robots" content="noindex">'), base), encoding="utf-8")

    needs = '<p class="needs"><b>[NEEDS_REVIEW]</b> Platzhalter: Name und Anschrift fehlen noch. Wer eine Seite mit Kontaktformular und geschäftlichem Zweck betreibt, braucht in Deutschland ein vollständiges Impressum nach § 5 DDG.</p>'
    needs_ds = '<p class="needs"><b>[NEEDS_REVIEW]</b> Entwurf, vor dem Bewerben der Seite rechtlich prüfen lassen. Die Informationspflichten nach Art. 13 DSGVO gelten ab dem ersten Formular, das Daten einsammelt.</p>'
    impressum = f"""{topbar(False, "sub")}
<div class="page"><p class="eyebrow">Rechtliches</p><h1>Impressum</h1>{needs}
<p><b>Angaben gemäß § 5 DDG</b><br>[NAME, VORNAME]<br>[STRASSE, HAUSNUMMER]<br>[PLZ, ORT]<br>Deutschland</p>
<p><b>Kontakt</b><br>E-Mail: {LEAD_TO}<br>[TELEFON, optional]</p>
<p><b>Verantwortlich für den Inhalt</b> nach § 18 Abs. 2 MStV: [NAME, ANSCHRIFT wie oben]</p>
<p><b>Umsatzsteuer</b>: [USt-IdNr., falls vorhanden, sonst Zeile löschen]</p>
<p><b>Haftung für Links:</b> Die Liste enthält Links zu externen Websites, auf deren Inhalte wir keinen Einfluss haben. Für diese Inhalte ist der jeweilige Anbieter verantwortlich. Links werden regelmäßig auf Erreichbarkeit geprüft, nicht auf Inhalt.</p>
<p><b>Schriften und Logos:</b> Die Schriften IBM Plex (IBM Corp.) und Space Grotesk (Florian Karsten) stehen unter der SIL Open Font License 1.1; die Lizenztexte liegen unter <a href="assets/fonts/LICENSE-IBM-Plex.txt">assets/fonts/LICENSE-IBM-Plex.txt</a> und <a href="assets/fonts/LICENSE-Space-Grotesk.txt">assets/fonts/LICENSE-Space-Grotesk.txt</a>. Tool-Logos werden als Favicons vom jeweiligen Anbieter geladen; Marken und Logos gehören den jeweiligen Inhabern.</p>
<p><a href="{SITE_URL}">Zurück zur Werkstatt</a></p></div>
<footer><div class="wrap"><p><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></p></div></footer>"""
    (DOCS / "impressum.html").write_text(page_shell("Impressum – KI-Werkstatt", impressum, "Impressum der KI-Werkstatt.", SITE_URL + "impressum.html", '<meta name="robots" content="noindex">'), encoding="utf-8")

    ds = f"""{topbar(False, "sub")}
<div class="page"><p class="eyebrow">Rechtliches</p><h1>Datenschutz</h1>{needs_ds}
<p><b>Verantwortlicher:</b> [NAME, ANSCHRIFT wie im Impressum], E-Mail: {LEAD_TO}</p>
<h3>Hosting</h3><p>Die Seite wird über GitHub Pages ausgeliefert (GitHub, Inc., USA). Beim Aufruf verarbeitet GitHub technisch notwendige Daten wie IP-Adresse und Zeitpunkt des Zugriffs. Details: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">GitHub-Datenschutzerklärung</a>. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer sicheren Auslieferung). [NEEDS_REVIEW: Hinweis auf Drittlandübermittlung und Data Privacy Framework ergänzen]</p>
<h3>Kontaktformulare (Stack-Check, CSV-Anfrage)</h3><p>Wenn du ein Formular absendest, werden deine Angaben (Name, E-Mail, optional Website, Rolle, Projektbeschreibung) über den Dienst FormSubmit (formsubmit.co) per E-Mail an {LEAD_TO} übermittelt. FormSubmit leitet die Daten per E-Mail weiter und speichert Einsendungen nach eigenen Angaben 30 Tage in einem Archiv (<a href="https://formsubmit.co/documentation" target="_blank" rel="noopener">Dokumentation</a>). [NEEDS_REVIEW: Anbieter, Sitz und Datenschutzerklärung von FormSubmit verlinken; prüfen, ob ein AVV nötig ist] Rechtsgrundlage: deine Einwilligung (Art. 6 Abs. 1 lit. a DSGVO), die du mit dem Absenden erteilst und jederzeit per Mail widerrufen kannst. Die Daten werden nur zur Beantwortung deiner Anfrage genutzt, nicht in ein CRM oder einen Newsletter übernommen. Antwortet FormSubmit nicht oder lehnt die Anfrage ab, bietet das Formular an, sie zusätzlich über dein eigenes E-Mail-Programm zu senden. Deine Angaben sind zu diesem Zeitpunkt bereits an FormSubmit übermittelt worden; mit dem Mail-Weg gehen sie außerdem über deinen Mail-Anbieter.</p>
<h3>Favicons der Tool-Anbieter</h3><p>Neben jedem Tool wird dessen Favicon über den Dienst icons.duckduckgo.com geladen. Dabei erfährt DuckDuckGo (USA) deine IP-Adresse und den Domainnamen des Tools. Die Icons werden erst geladen, wenn sie in den sichtbaren Bereich scrollen. [NEEDS_REVIEW: alternativ Icons lokal speichern oder nach Einwilligung laden]</p>
<h3>Schriften, Skripte, Speicher</h3><p>Schriften und Skripte liegen auf dieser Seite selbst; es werden keine Google Fonts von Google-Servern geladen. Im Browser-Speicher (localStorage) liegen nur drei Dinge: dein Farbschema, ob du die untere Hinweisleiste geschlossen hast, und deine Merkliste (Name und Link der Tools, die du markiert hast). Zeitspar-Rechner und Trend-Radar rechnen nur in deinem Browser und speichern nichts. Merkliste, Rechner-Ergebnis und Radar gehen nur dann an Jean, wenn du sie an das Stack-Check-Formular anhängst und es abschickst. Keine Cookies, kein Tracking, keine Analyse-Tools.</p>
<h3>Externe Links</h3><p>Links zu Tools, zu PROMPTGOTT (Substack) und zu GitHub führen auf fremde Seiten mit eigenen Datenschutzregeln. Links zu PROMPTGOTT enthalten UTM-Parameter, damit erkennbar ist, dass der Besuch von dieser Seite kam; persönliche Daten werden dabei nicht übertragen.</p>
<h3>Deine Rechte</h3><p>Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit, Widerspruch und Beschwerde bei einer Aufsichtsbehörde (Art. 15 bis 21, 77 DSGVO). Schreib dafür an {LEAD_TO}.</p>
<p><a href="{SITE_URL}">Zurück zur Werkstatt</a></p></div>
<footer><div class="wrap"><p><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></p></div></footer>"""
    (DOCS / "datenschutz.html").write_text(page_shell("Datenschutz – KI-Werkstatt", ds, "Datenschutzerklärung der KI-Werkstatt.", SITE_URL + "datenschutz.html", '<meta name="robots" content="noindex">'), encoding="utf-8")


# --------------------------------------------------------------------------- Zeitspar-Rechner
def fmt_pct(v):
    return f"{v} %"


def rechner_band():
    rows = []
    for a in RECHNER["aufgaben"]:
        src = (f' <a href="{html.escape(a["url"])}" target="_blank" rel="noopener">Quelle: {html.escape(a["quelle"])}</a>' if a["url"] else "")
        cat = (f' <a href="{cat_page(a["kategorie"])}">Passende Tools</a>' if a.get("kategorie") else "")
        rows.append(f"""<div class="calc-row reveal" data-id="{a['id']}" data-label="{html.escape(a['label'])}">
<div class="calc-head"><span class="calc-ico">{icon(a["icon"])}</span><b>{html.escape(a["label"])}</b></div>
<div class="calc-in"><div><label for="c-h-{a['id']}">Stunden pro Woche</label><input type="number" id="c-h-{a['id']}" class="c-h" min="0" max="60" step="0.5" value="{a['stunden']}" inputmode="decimal"></div>
<div><label for="c-p-{a['id']}">Ersparnis: <output id="c-po-{a['id']}" for="c-p-{a['id']}">{fmt_pct(a['prozent'])}</output></label><input type="range" id="c-p-{a['id']}" class="c-p" min="0" max="60" step="1" value="{a['prozent']}"></div></div>
<div class="calc-bar" aria-hidden="true"><div class="track"><i></i></div><span></span></div>
<p class="calc-src">{html.escape(a["befund"])}{src}{cat}</p></div>""")
    return f"""<section class="band" id="rechner"><div class="wrap">
<p class="eyebrow">Zeitspar-Rechner</p><h2>Wie viel Feierabend steckt in deiner Woche?</h2>
<p class="intro">Trag ein, wie viele Stunden du pro Woche mit diesen Aufgaben verbringst. Jeder Regler startet bei ungefähr der Hälfte des Werts aus einer Studie, die Quelle steht jeweils darunter. Gerechnet wird nur in deinem Browser, wir gucken nicht mit.</p>
<p class="nojs">Der Rechner braucht JavaScript. Ohne JavaScript siehst du hier die Studienwerte.</p>
<div class="calc" id="calc" data-wochen="{RECHNER['wochen']}">
<div class="calc-rows">{"".join(rows)}</div>
<aside class="calc-out"><div class="in">
<p class="eyebrow">Dein Ergebnis</p>
<div class="calc-ring"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="bg" cx="60" cy="60" r="50"/><circle class="fg" cx="60" cy="60" r="50" pathLength="100" stroke-dasharray="0 100"/></svg><div><b id="c-share">0 %</b><small>deiner Stunden</small></div></div>
<dl><div><dt>pro Woche</dt><dd id="c-week">0 h</dd></div><div><dt>pro Jahr</dt><dd id="c-year">0 h</dd></div><div><dt>Gegenwert</dt><dd id="c-eur">0 €</dd></div></dl>
<label for="c-rate">Dein Stundensatz in Euro</label><input type="number" id="c-rate" min="0" max="1000" step="5" value="{RECHNER['stundensatz']}" inputmode="decimal">
<p class="calc-note">{html.escape(RECHNER["wochen_hinweis"])}</p>
<button type="button" class="btn btn-lime" id="c-send">{icon("mail")}Mit diesen Zahlen zum Stack-Check</button>
</div></aside></div>
<p class="calc-method">{icon("ruler")} {html.escape(RECHNER["methode"])}</p>
</div></section>"""


# --------------------------------------------------------------------------- Kategorie-Seiten
def sec_items(sec):
    seen = {}
    for _, _, it in all_items([sec]):
        seen.setdefault(it["url"], it)
    return list(seen.values())


def breadcrumb_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": url} for i, (name, url) in enumerate(trail)]}


def build_category_pages(list_secs, tools_map):
    pages = []
    terms_by_cat = {}
    for g in GLOSSAR["begriffe"]:
        if g.get("cat"):
            terms_by_cat.setdefault(g["cat"], []).append(g)
    for idx, sec in enumerate(list_secs):
        its = sec_items(sec)
        n = len(its)
        n_eu = sum(1 for it in its if item_meta(it)[0])
        n_oss = sum(1 for it in its if item_meta(it)[1])
        urls = {it["url"] for it in its}
        h1 = CAT_H1.get(sec["id"], "KI-Tools: " + sec["title"])
        page = cat_page(sec["id"])
        desc = kat_text(sec, "meta")
        faq = [tuple(x) for x in kat_text(sec, "faq")]
        # Werkzeugkisten nur als Verweis: die ausführliche Kiste steht einmal, auf der Startseite
        ranked = []
        for st in STACKS["stacks"]:
            hits = [name for name, _ in st["tools"] if tools_map.get(name, {}).get("u") in urls]
            if len(hits) >= 2:
                ranked.append((len(hits), st, hits))
        ranked.sort(key=lambda x: -x[0])
        refs = []
        for cnt, st, hits in ranked[:3]:
            names = ", ".join(hits[:-1]) + " und " + hits[-1]
            refs.append(f'<a class="kiste-ref reveal" href="./#kiste-{st["id"]}">{icon(st["icon"])}<span><b>{html.escape(st["title"])}</b>'
                        f'<small>{cnt} von {len(st["tools"])} Tools liegen in dieser Schublade: {html.escape(names)}.</small></span>{icon("arrow")}</a>')
        stacks_html = (f"""<section class="band" id="werkzeugkisten"><div class="wrap">
<p class="eyebrow">Passende Werkzeugkisten</p><h2>Kisten mit Werkzeug aus „{html.escape(sec["title"])}“</h2>
<div class="kisten-refs">{"".join(refs)}</div></div></section>""") if refs else ""
        terms = terms_by_cat.get(sec["id"], [])
        terms_html = "".join(f'<a class="chip" href="{GLOSSAR_PAGE}#{slug(g["t"])}">{icon(g["icon"])}{html.escape(g["t"])}</a>' for g in terms)
        side = []
        if any(a.get("kategorie") == sec["id"] for a in RECHNER["aufgaben"]):
            side.append(f'<div class="side-card reveal">{icon("clock")}<b>Wie viel Zeit spart das?</b><a class="btn btn-sm" href="./#rechner">{icon("calc")}Zum Zeitspar-Rechner</a></div>')
        if terms:
            side.append(f'<div class="side-card reveal">{icon("abc")}<b>Begriffe zu dieser Schublade</b><div class="chips">{terms_html}</div></div>')
        rail_links = "".join(f'<a href="#{sub["id"]}">{icon(SUB_ICON.get(sub["id"], "layers"))}{html.escape(sub["title"])}</a>' for sub in sec["subs"]) \
            or f'<a href="#{sec["id"]}">{icon(CAT_ICON.get(sec["id"], "box"))}Alle Tools</a>'
        rail_links += f'<a href="#faq">{icon("chat")}Fragen</a>'
        if refs:
            rail_links += f'<a href="#werkzeugkisten">{icon("layers")}Werkzeugkisten</a>'
        rail_links += f'<a href="#stack-check">{icon("mail")}Stack-Check</a>'
        others = []
        for j, o in enumerate(list_secs):
            if o is sec:
                continue
            others.append(f'<a class="cat-tile reveal" href="{cat_page(o["id"])}"><img src="img/cat-{o["id"]}.svg" alt="" loading="lazy">'
                          f'<span class="t">{html.escape(o["title"])}<small>Schublade {j + 1:02d} · {len(sec_items(o))} Tools</small></span></a>')
        section_html = render_section(sec, idx + 1, {})
        intro_html = "".join(f"<p>{html.escape(x)}</p>" for x in kat_text(sec, "intro"))
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "@id": SITE_URL + page, "url": SITE_URL + page, "name": h1, "description": desc, "inLanguage": "de-DE",
             "isPartOf": {"@type": "WebSite", "name": "KI-Werkstatt", "url": SITE_URL}},
            breadcrumb_ld([("KI-Werkstatt", SITE_URL), (sec["title"], SITE_URL + page)]),
            {"@type": "ItemList", "name": h1, "numberOfItems": n,
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": it["name"], "url": it["url"], "description": item_meta(it)[2]}
                                 for i, it in enumerate(its)]},
            faq_ld(faq),
        ]}
        ld_js = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
        first = sec["subs"][0]["id"] if sec["subs"] else sec["id"]
        body = f"""{topbar(True, "kategorie")}
<section class="hero cat-hero"><div class="hero-art">{hero_floats()}</div><div class="wrap">
<nav class="crumbs" aria-label="Brotkrümel"><a href="./">KI-Werkstatt</a>{icon("arrow")}<a href="./#kategorien">Schubladen</a>{icon("arrow")}<span aria-current="page">{html.escape(sec["title"])}</span></nav>
<div class="cat-hero-grid"><div>
<p class="kicker">{icon(CAT_ICON.get(sec["id"], "box"))} <b>Schublade {idx + 1:02d}</b> · Link-Check {LINK_CHECK}</p>
<h1><em>{html.escape(h1)}</em></h1>
<p class="sub">{html.escape(kat_text(sec, "hero"))}</p>
<div class="ctas"><a class="btn btn-lime" href="#{first}">{icon("layers")}Zu den {n} Tools</a><a class="btn" href="#stack-check">{icon("mail")}Kostenloser Stack-Check</a></div>
</div><div class="cat-hero-art reveal"><img src="img/cat-{sec["id"]}.svg" alt="" width="800" height="300"></div></div>
<div class="stats">
<div class="stat reveal"><b data-count="{n}">{n}</b><span>Tools in dieser Schublade</span></div>
<div class="stat reveal"><b data-count="{max(1, len(sec["subs"]))}">{max(1, len(sec["subs"]))}</b><span>{"Fächer" if len(sec["subs"]) > 1 else "Fach"}</span></div>
<div class="stat reveal"><b data-count="{n_eu}">{n_eu}</b><span>mit EU-Sitz</span></div>
<div class="stat reveal"><b data-count="{n_oss}">{n_oss}</b><span>Open Source</span></div>
</div></div></section>

<section class="band cat-intro"><div class="wrap intro-grid">
<div class="intro-text reveal">{intro_html}</div>
<aside class="tipp reveal">{kurbel("kb-sm", wink=True)}<p class="eyebrow">Werkstatt-Tipp</p><p>{html.escape(kat_text(sec, "tipp"))}</p></aside>
</div></section>

<div class="wrap layout" id="liste">
<aside class="rail" data-chrome><div class="in"><h4>Auf dieser Seite</h4>{rail_links}
<div style="margin-top:14px;display:grid;gap:6px"><label style="display:flex;gap:8px;align-items:center;font-size:13px"><input type="checkbox" class="f-eu"> nur Anbieter aus der EU</label><label style="display:flex;gap:8px;align-items:center;font-size:13px"><input type="checkbox" class="f-oss"> nur Open Source</label></div>
<div class="lead-mini"><b>Stack-Check</b><a class="btn btn-sm" href="#stack-check">{icon("mail")}Anfragen</a></div></div></aside>
<main class="content"><div class="filters"><label><input type="checkbox" class="f-eu"> nur EU-Anbieter</label><label><input type="checkbox" class="f-oss"> nur Open Source</label></div>
{section_html}
<div class="side-cards">{"".join(side)}</div>
</main>
</div>

<section class="band faq" id="faq"><div class="wrap">
<p class="eyebrow">Fragen aus der Werkstatt</p><h2>{html.escape(sec["title"])}: kurz beantwortet</h2>
<div class="faq-list">{faq_html(faq)}</div>
</div></section>

{stacks_html}

<section class="band lead" id="stack-check"><div class="wrap">
<div class="lead-grid"><div>
<p class="eyebrow">Stack-Check</p><h2>{html.escape(kat_text(sec, "lead_hook"))}</h2>
<p class="intro">{html.escape(kat_text(sec, "lead_text"))}</p>
<p class="lead-merk" data-chrome>{icon("bookmark")}<span>Markier Tools mit dem Lesezeichen, die Merkliste reist mit deiner Anfrage mit.</span></p>
</div>
<div>{lead_form("Kategorie: " + sec["title"], "Stack-Check (" + sec["title"] + ") – KI-Werkstatt")}</div></div>
</div></section>

<section class="band" id="weitere"><div class="wrap">
<p class="eyebrow">Weitere Schubladen</p><h2>Woanders weiterstöbern</h2>
<div class="catgrid">{"".join(others)}</div>
</div></section>
{footer()}
"""
        title = f"{kat_text(sec, 'seo_title')} – KI-Werkstatt"
        (DOCS / page).write_text(page_shell(title, body, desc, SITE_URL + page, f'<script type="application/ld+json">{ld_js}</script>'), encoding="utf-8")
        pages.append(page)
    return pages


# --------------------------------------------------------------------------- KI-Glossar
def build_glossar(tools_map, list_secs, sections):
    terms = sorted(GLOSSAR["begriffe"], key=lambda g: g["t"].lower())
    names = {g["t"] for g in terms}
    page_ids = {s["id"] for s in list_secs}
    slugs = [slug(g["t"]) for g in terms]
    if len(set(slugs)) != len(slugs):
        raise SystemExit("Glossar: doppelte Anker")
    letters = []
    cards = []
    cur = None
    for g in terms:
        for ref in g["see"]:
            if ref not in names:
                raise SystemExit(f"Glossar '{g['t']}': Verweis '{ref}' fehlt")
        for t in g["tools"]:
            if t not in tools_map:
                raise SystemExit(f"Glossar '{g['t']}': Tool '{t}' nicht in README.de.md gefunden")
        L = g["t"][0].upper()
        if L != cur:
            cur = L
            letters.append(L)
            cards.append(f'<h2 class="az-letter" id="buchstabe-{L.lower()}">{L}</h2>')
        see = " ".join(f'<a href="#{slug(r)}">{html.escape(r)}</a>' for r in g["see"])
        tools = "".join(f'<a class="chip tool" href="{html.escape(tools_map[t]["u"])}" target="_blank" rel="noopener">{favicon(tools_map[t]["u"])}{html.escape(t)}</a>' for t in g["tools"])
        cat = ""
        if g.get("cat"):
            href = cat_page(g["cat"]) if g["cat"] in page_ids else f'./#{g["cat"]}'
            label = next((s["title"] for s in sections if s["id"] == g["cat"]), None)
            if label is None:
                raise SystemExit(f"Glossar '{g['t']}': Kategorie '{g['cat']}' fehlt")
            cat = f'<a class="chip cat" href="{href}">{icon("layers")}Schublade: {html.escape(label)}</a>'
        extra = ""
        if tools or cat:
            extra = f'<div class="chips">{tools}{cat}</div>'
        search = " ".join([g["t"], g["d"]] + g.get("auch", [])).lower()
        cards.append(f"""<article class="term reveal" id="{slug(g['t'])}" data-search="{html.escape(search)}">
<div class="term-head"><span class="term-ico">{icon(g["icon"])}</span><h3><dfn>{html.escape(g["t"])}</dfn></h3><a class="anchor" href="#{slug(g['t'])}" title="Link auf diesen Begriff">#</a></div>
<p>{html.escape(g["d"])}</p>
<p class="spruch">{icon("wrench")}<span><b>Werkstatt-Übersetzung:</b> {html.escape(g["spruch"])}</span></p>
<p class="see"><b>Siehe auch:</b> {see}</p>{extra}</article>""")
    az = "".join(f'<a href="#buchstabe-{L.lower()}">{L}</a>' for L in letters)
    n = len(terms)
    url = SITE_URL + GLOSSAR_PAGE
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "DefinedTermSet", "@id": url, "url": url, "name": "KI-Glossar der KI-Werkstatt", "inLanguage": "de-DE",
         "hasDefinedTerm": [{"@type": "DefinedTerm", "name": g["t"], "description": g["d"], "url": f"{url}#{slug(g['t'])}"} for g in terms]},
        breadcrumb_ld([("KI-Werkstatt", SITE_URL), ("KI-Glossar", url)]),
    ]}
    ld_js = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    body = f"""{topbar(False, "glossar")}
<section class="hero gl-hero"><div class="hero-art">{hero_floats()}</div><div class="wrap">
<nav class="crumbs" aria-label="Brotkrümel"><a href="./">KI-Werkstatt</a>{icon("arrow")}<span aria-current="page">KI-Glossar</span></nav>
<p class="kicker">{icon("abc")} <b>KI-Glossar</b> · {n} Begriffe von A bis Z</p>
<h1><em>{n} KI-Begriffe.</em><br>Ernst erklärt.<br>Mit Augenzwinkern übersetzt.</h1>
<p class="sub">{html.escape(GLOSSAR["intro"])}</p>
<div class="ctas"><a class="btn btn-lime" href="#begriffe">{icon("book")}Zu den Begriffen</a><a class="btn" href="#stack-check">{icon("mail")}Kostenloser Stack-Check</a></div>
</div></section>
<nav class="az" aria-label="Buchstaben"><div class="wrap in"><div class="az-letters">{az}</div>
<label class="sr" for="gq">Begriffe filtern</label><input type="search" id="gq" placeholder="Begriff filtern: Token, RAG, DSGVO …" autocomplete="off"><span id="gcount" aria-live="polite"></span></div></nav>
<div class="wrap gl" id="begriffe">{"".join(cards)}<div class="gl-empty hidden">{kurbel("kb-sm", wink=True)}<p><b>Die Schublade klemmt.</b> Diesen Begriff kennt Kurbel noch nicht. Fehlt einer? Schreib an <a href="mailto:{LEAD_TO}?subject=Glossar">{LEAD_TO}</a>.</p></div></div>

<section class="band lead" id="stack-check"><div class="wrap">
<div class="lead-grid"><div>
<p class="eyebrow">Stack-Check</p><h2>Vokabeln sitzen. Und welches Tool jetzt?</h2>
<p class="intro">Wer weiß, was ein Token ist, stellt die besseren Fragen. Stell eine davon Jean und bekomm ein Setup, das zu deinem Vorhaben passt.</p>
<div class="kb-say">{hans("hm-md")}<p class="bubble">Ich hab das Glossar übrigens auswendig gelernt. Fast.</p></div></div>
<div>{lead_form("Glossar", "Stack-Check (Glossar) – KI-Werkstatt")}</div></div>
</div></section>
{footer()}
"""
    desc = f"{n} KI-Begriffe auf Deutsch erklärt, von Agent bis Zero-Shot: Token, RAG, MCP, Halluzination, DSGVO und EU AI Act. Jeder mit Werkstatt-Übersetzung, Querverweisen und passenden Tools."
    (DOCS / GLOSSAR_PAGE).write_text(page_shell(f"KI-Glossar: {n} Begriffe auf Deutsch erklärt – KI-Werkstatt", body, desc, url,
                                                f'<script type="application/ld+json">{ld_js}</script>'), encoding="utf-8")
    return GLOSSAR_PAGE


# --------------------------------------------------------------------------- Trends und Neuzugänge
def de_date(iso):
    return date.fromisoformat(iso).strftime("%d.%m.%Y") if iso else ""


def tool_home(list_secs):
    """Name -> Kategorie-Seite mit Fach-Anker, wie in tools.json."""
    out = {}
    for s, sub, it in all_items(list_secs):
        out.setdefault(it["name"], cat_page(s["id"]) + (f"#{sub['id']}" if sub else ""))
    return out


def neu_band(list_secs):
    home = tool_home(list_secs)
    trend_ids = {t["id"]: t for t in TRENDS["trends"]}
    for t in NEU["tools"]:
        if t["name"] not in home:
            raise SystemExit(f"data/neu.json: '{t['name']}' steht in keiner Schublade von README.de.md")
        if t["trend"] not in trend_ids:
            raise SystemExit(f"data/neu.json: Trend '{t['trend']}' fehlt in data/trends.json")
    cards = "".join(f"""<a class="trend-card reveal" href="{TRENDS_PAGE}#{t['id']}"><span class="term-ico">{icon(t["icon"])}</span>
<span><span class="trend-no">Trend {i + 1:02d}</span><b>{html.escape(t["label"])}</b><small>{html.escape(t["kurz"])}</small></span></a>""" for i, t in enumerate(TRENDS["trends"]))
    neu = "".join(f"""<li><a class="name" href="{home[t['name']]}">{html.escape(t["name"])}</a>{NEU_BADGE}<span class="desc">{html.escape(t["notiz"])}</span>
<a class="neu-trend" href="{TRENDS_PAGE}#{t['trend']}">{icon("spark")}{html.escape(trend_ids[t["trend"]]["label"])}</a></li>""" for t in NEU_AKTIV)
    neu_html = f"""<div class="neu-box reveal"><h3>{icon("plus")}Frisch in den Schubladen</h3><ul class="neu-list">{neu}</ul></div>""" if neu else ""
    return f"""<section class="band" id="neu-und-trends"><div class="wrap">
<p class="eyebrow">Neu &amp; im Trend · Stand {de_date(TRENDS["stand"])}</p><h2>Was diesen Herbst in der Werkstatt angekommen ist</h2>
<p class="intro">{ZAHLWORT.get(len(TRENDS["trends"]), str(len(TRENDS["trends"])))} Entwicklungen, die wir beim Hersteller nachgelesen haben, und die Tools, die deshalb neu in der Liste stehen. Die ausführliche Einordnung mit Quellen liegt auf der Trend-Seite.</p>
<div class="trend-cards">{cards}</div>
{neu_html}
<p style="margin-top:20px"><a class="btn btn-lime" href="{TRENDS_PAGE}">{icon("chart")}Alle Trends mit Quellen</a></p>
</div></section>"""


def gl_aliases():
    out = []
    for g in GLOSSAR["begriffe"]:
        for a in [g["t"]] + g.get("auch", []):
            out.append((a, g["t"]))
    return sorted(out, key=lambda x: -len(x[0]))


GL_ALIASES = gl_aliases()


def gl_autolink(txt, used):
    """Text escapen und das erste Vorkommen jedes Glossarbegriffs (oder Synonyms) auf der Seite verlinken."""
    out, slots = html.escape(txt), []
    for alias, term in GL_ALIASES:
        if term in used:
            continue
        m = re.search(r"(?<![\w-])" + re.escape(html.escape(alias)) + r"(?![\w-])", out)
        if not m:
            continue
        used.add(term)
        slots.append(f'<a class="gl-link" href="{GLOSSAR_PAGE}#{slug(term)}" title="Im Glossar: {html.escape(term)}">{m.group(0)}</a>')
        out = out[:m.start()] + f"\x00{len(slots) - 1}\x00" + out[m.end():]
    return re.sub("\x00(\\d+)\x00", lambda m: slots[int(m.group(1))], out)


def build_trends(tools_map, list_secs):
    stand = de_date(TRENDS["stand"])
    url = SITE_URL + TRENDS_PAGE
    n = len(TRENDS["trends"])
    ids = [t["id"] for t in TRENDS["trends"]]
    if len(set(ids)) != len(ids):
        raise SystemExit("data/trends.json: doppelte Trend-ID")
    links, arts, used = [f'<a href="#radar" data-js-only hidden>{icon("compass")}Radar</a>'], [], set()
    rollen = {r["id"] for r in TRENDS["rollen"]}
    for i, t in enumerate(TRENDS["trends"]):
        if set(t["radar"]) != rollen or not all(v in (0, 1, 2, 3) for v in t["radar"].values()):
            raise SystemExit(f"Trend '{t['id']}': radar braucht für jede Rolle einen Wert 0 bis 3")
        for name in t["tools"]:
            if name not in tools_map:
                raise SystemExit(f"Trend '{t['id']}': Tool '{name}' nicht in README.de.md gefunden")
        if not t["quellen"]:
            raise SystemExit(f"Trend '{t['id']}': keine Quelle")
        chips = "".join(f'<a class="chip tool" href="{html.escape(tools_map[name]["u"])}" target="_blank" rel="noopener">{favicon(tools_map[name]["u"])}{html.escape(name)}'
                        f'{NEU_BADGE if name in NEU_NAMES else ""}</a>' for name in t["tools"])
        chips_html = f'<div class="chips trend-tools"><span class="chips-lbl">Werkzeug dazu:</span>{chips}</div>' if chips else ""
        quellen = "".join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(lbl)}</a>{f" <small>({de_date(d)})</small>" if d else ""}</li>'
                          for lbl, u, d in t["quellen"])
        text = "".join(f"<p>{gl_autolink(x, used)}</p>" for x in t["text"])
        links.append(f'<a href="#{t["id"]}">{icon(t["icon"])}{html.escape(t["label"])}</a>')
        arts.append(f"""<article class="trend reveal" id="{t['id']}">
<div class="trend-head"><span class="term-ico">{icon(t["icon"])}</span><div><p class="eyebrow">Trend {i + 1:02d} · {html.escape(t["label"])}</p><h2>{html.escape(t["titel"])}</h2></div></div>
<div class="trend-text">{text}</div>
<div class="trend-grid"><div class="fuer-dich"><h3>{icon("user")}Was heißt das für dich?</h3><p>{gl_autolink(t["fuer_dich"], used)}</p></div>
<div class="schritt"><h3>{icon("check")}Erster Schritt</h3><p>{html.escape(t["erster_schritt"])}</p></div>
<div class="urteil"><h3>{icon("wrench")}Werkstatt-Urteil</h3><p>{html.escape(t["urteil"])}</p></div></div>
{chips_html}
{rg_link(t.get("ratgeber"))}
<details class="quellen" data-chrome><summary>{icon("link")}Quellen ({len(t["quellen"])})</summary><ol>{quellen}</ol></details>
</article>""")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url, "url": url, "headline": TRENDS["titel"], "description": TRENDS["intro"], "inLanguage": "de-DE",
         "datePublished": TRENDS["stand"], "dateModified": TRENDS["stand"], "mainEntityOfPage": url,
         "author": {"@type": "Organization", "name": "KI-Werkstatt", "url": SITE_URL},
         "publisher": {"@type": "Organization", "name": "KI-Werkstatt", "url": SITE_URL},
         "citation": [u for t in TRENDS["trends"] for _, u, _ in t["quellen"]]},
        {"@type": "ItemList", "name": TRENDS["titel"], "numberOfItems": n,
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t["titel"], "url": f"{url}#{t['id']}"} for i, t in enumerate(TRENDS["trends"])]},
        breadcrumb_ld([("KI-Werkstatt", SITE_URL), ("KI-Trends", url)]),
    ]}
    ld_js = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    radar_btns = "".join(f'<button type="button" class="opt" data-rolle="{r["id"]}">{icon(r["icon"])}{html.escape(r["label"])}</button>' for r in TRENDS["rollen"])
    pages_by_rolle = {e["rolle"]: {"page": e["page"], "h1": e["h1"], "form": e["form_rolle"]} for e in EINSATZ["seiten"]}
    missing = [r["id"] for r in TRENDS["rollen"] if pages_by_rolle.get(r["id"], {}).get("form") not in ROLLEN_FORM]
    if missing:
        raise SystemExit(f"data/einsatz.json: form_rolle fehlt oder unbekannt für Rollen {missing}")
    radar_js = json.dumps({"rollen": [dict(r, **pages_by_rolle.get(r["id"], {})) for r in TRENDS["rollen"]], "trends": [{"id": t["id"], "label": t["label"], "schritt": t["erster_schritt"], "radar": t["radar"]}
                                                                for t in TRENDS["trends"]]}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    body = f"""{topbar(False, "trends")}
<section class="hero tr-hero"><div class="hero-art">{hero_floats()}</div><div class="wrap">
<nav class="crumbs" aria-label="Brotkrümel"><a href="./">KI-Werkstatt</a>{icon("arrow")}<span aria-current="page">KI-Trends</span></nav>
<p class="kicker">{icon("chart")} <b>{html.escape(TRENDS["titel"])}</b> · Stand {stand}</p>
<h1><em>{n} KI-Trends.</em><br>Beim Hersteller nachgelesen.<br>Für die Werkbank übersetzt.</h1>
<p class="sub">{html.escape(TRENDS["intro"])}</p>
<div class="ctas"><a class="btn btn-lime" href="#radar" data-js-only hidden>{icon("compass")}Trend-Radar starten</a><a class="btn" href="#{ids[0]}">{icon("chart")}Zum ersten Trend</a><a class="btn" href="#stack-check">{icon("mail")}Kostenloser Stack-Check</a></div>
</div></section>
<nav class="az tr-nav" aria-label="Trends"><div class="wrap in"><div class="tr-links">{"".join(links)}</div></div></nav>
<div class="wrap tr-wrap">
<aside class="tipp tr-method reveal">{kurbel("kb-sm", wink=True)}<p class="eyebrow">So haben wir sortiert</p><p>{html.escape(TRENDS["methode"])}</p></aside>
<section class="radar" id="radar" hidden><p class="eyebrow">Trend-Radar</p><h2>Welche dieser Trends treffen deine Arbeit?</h2>
<p class="radar-intro">Wähl, woran du hauptsächlich arbeitest. Das Radar sortiert die Trends nach unserer Einschätzung für diese Rolle und legt dir für die drei wichtigsten einen ersten Handgriff hin.</p>
<div class="radar-roles" role="group" aria-label="Deine Rolle">{radar_btns}</div>
<div class="radar-out" aria-live="polite"></div></section>
{"".join(arts)}
</div>

<section class="band lead" id="stack-check"><div class="wrap">
<div class="lead-grid"><div>
<p class="eyebrow">Stack-Check</p><h2>Trends gelesen. Welcher davon zahlt bei dir ein?</h2>
<p class="intro">Nicht jede Neuheit gehört in deinen Werkzeugkasten. Schreib Jean, woran du gerade arbeitest, und du erfährst, welcher dieser Trends dir tatsächlich Arbeit abnimmt und welchen du getrost vorbeiziehen lässt.</p>
<div class="kb-say">{hans("hm-md")}<p class="bubble">Ich hab alle Quellen gelesen. Zweimal. Eine Schraube ist trotzdem übrig.</p></div></div>
<div>{lead_form("Trends", "Stack-Check (Trends) – KI-Werkstatt")}</div></div>
</div></section>
{footer()}
<script>window.KW_RADAR={radar_js};</script>
"""
    desc = (f"{TRENDS['titel']}: {n} KI-Entwicklungen auf Deutsch eingeordnet, von günstigeren Spitzenmodellen über Agenten-Standards bis zum EU AI Act. "
            "Mit Quellen beim Hersteller und passenden Tools.")
    (DOCS / TRENDS_PAGE).write_text(page_shell(f"{TRENDS['titel']}: {n} Entwicklungen eingeordnet – KI-Werkstatt", body, desc, url,
                                               f'<script type="application/ld+json">{ld_js}</script>'), encoding="utf-8")
    return TRENDS_PAGE


# --------------------------------------------------------------------------- Einsatzgebiete
RADAR_TXT = ["kannst du auslassen", "am Rande", "lohnt einen Blick", "trifft dich direkt"]


def radar_bar(score):
    on = ' class="on"'
    return f'<span class="radar-bar" title="{RADAR_TXT[score]}">' + "".join(f'<i{on if j <= score else ""}></i>' for j in (1, 2, 3)) + "</span>"


def einsatz_band():
    tiles = "".join(f"""<a class="einsatz-tile reveal" href="{e['page']}"><span class="term-ico">{icon(e["icon"])}</span>
<span><b>{html.escape(e["h1"])}</b><small>{html.escape(e["teaser"])}</small><span class="drawer-cta">Ansehen{icon("arrow")}</span></span></a>""" for e in EINSATZ["seiten"])
    return f"""<section class="band" id="einsatz"><div class="wrap">
<p class="eyebrow">{html.escape(EINSATZ["titel"])}</p><h2>Sag, wo du arbeitest. Wir zeigen, wo KI anpackt.</h2>
<p class="intro">Sechs Arbeitsfelder, jedes mit konkreten Aufgaben, passenden Werkzeugen, den Trends, die dort zählen, und den Fragen, die uns dazu am häufigsten erreichen.</p>
<div class="einsatz-grid">{tiles}</div>
</div></section>"""


def build_einsatz(tools_map, list_secs, sections):
    rollen = {r["id"]: r for r in TRENDS["rollen"]}
    kisten = {st["id"]: st for st in STACKS["stacks"]}
    sec_by_id = {x["id"]: x for x in sections}
    page_ids = {x["id"] for x in list_secs}
    terms = {g["t"]: g for g in GLOSSAR["begriffe"]}
    tasks = {a["id"]: a for a in RECHNER["aufgaben"]}
    pages = []
    for e in EINSATZ["seiten"]:
        where = f"data/einsatz.json/{e['id']}"
        if e["rolle"] not in rollen:
            raise SystemExit(f"{where}: Rolle '{e['rolle']}' fehlt in data/trends.json")
        for a in e["aufgaben"]:
            for name in a["tools"]:
                if name not in tools_map:
                    raise SystemExit(f"{where}: Tool '{name}' nicht in README.de.md gefunden")
        for k in e["kisten"]:
            if k not in kisten:
                raise SystemExit(f"{where}: Werkzeugkiste '{k}' fehlt")
        for c in e["kategorien"]:
            if c not in page_ids:
                raise SystemExit(f"{where}: Schublade '{c}' hat keine eigene Seite")
        for t in e["glossar"]:
            if t not in terms:
                raise SystemExit(f"{where}: Glossarbegriff '{t}' fehlt")
        if e["rechner"] and e["rechner"] not in tasks:
            raise SystemExit(f"{where}: Rechner-Aufgabe '{e['rechner']}' fehlt")
        url = SITE_URL + e["page"]
        n_tools = len({n for a in e["aufgaben"] for n in a["tools"]})

        def chip(name):
            t = tools_map[name]
            return (f'<a class="chip tool" href="{html.escape(t["u"])}" target="_blank" rel="noopener">{favicon(t["u"])}{html.escape(name)}'
                    f'{NEU_BADGE if name in NEU_NAMES else ""}</a>')
        auf = "".join(f"""<article class="aufgabe reveal"><span class="n">{i + 1}</span><h3>{html.escape(a["titel"])}</h3><p>{html.escape(a["text"])}</p>
<div class="chips">{"".join(chip(n) for n in a["tools"])}</div></article>""" for i, a in enumerate(e["aufgaben"]))
        ranked = sorted(enumerate(TRENDS["trends"]), key=lambda x: (-x[1]["radar"][e["rolle"]], x[0]))[:3]
        trend_cards = "".join(f"""<a class="trend-card reveal" href="{TRENDS_PAGE}#{t['id']}"><span class="term-ico">{icon(t["icon"])}</span>
<span><span class="trend-no">Trend {i + 1:02d}</span><b>{html.escape(t["label"])}</b>{radar_bar(t["radar"][e["rolle"]])}</span></a>""" for i, t in ranked)
        kiste_html = "".join(f'<a class="kiste-ref reveal" href="./#kiste-{k}">{icon(kisten[k]["icon"])}<span><b>{html.escape(kisten[k]["title"])}</b>'
                             f'<small>{len(kisten[k]["tools"])} Tools, fertig gepackt</small></span>{icon("arrow")}</a>' for k in e["kisten"])
        kat_chips = "".join(f'<a class="chip cat" href="{cat_page(c)}">{icon(CAT_ICON.get(c, "layers"))}{html.escape(sec_by_id[c]["title"])}</a>' for c in e["kategorien"])
        gl_chips = "".join(f'<a class="chip" href="{GLOSSAR_PAGE}#{slug(t)}">{icon(terms[t]["icon"])}{html.escape(t)}</a>' for t in e["glossar"])
        rechner = (f'<a class="btn btn-sm" href="./#rechner">{icon("calc")}Rechner: {html.escape(tasks[e["rechner"]]["label"])}</a>') if e["rechner"] else ""
        others = "".join(f'<a class="einsatz-mini" href="{o["page"]}">{icon(o["icon"])}{html.escape(o["h1"])}</a>' for o in EINSATZ["seiten"] if o is not e)
        faq = [tuple(x) for x in e["faq"]]
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "@id": url, "url": url, "name": e["h1"], "description": e["meta"], "inLanguage": "de-DE",
             "isPartOf": {"@type": "WebSite", "name": "KI-Werkstatt", "url": SITE_URL}},
            breadcrumb_ld([("KI-Werkstatt", SITE_URL), ("Einsatzgebiete", SITE_URL + "#einsatz"), (e["h1"], url)]),
            {"@type": "ItemList", "name": f"Aufgaben: {e['h1']}", "numberOfItems": len(e["aufgaben"]),
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a["titel"]} for i, a in enumerate(e["aufgaben"])]},
            faq_ld(faq),
        ]}
        ld_js = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
        label = rollen[e["rolle"]]["label"]
        body = f"""{topbar(False, "einsatz")}
<section class="hero cat-hero"><div class="hero-art">{hero_floats()}</div><div class="wrap">
<nav class="crumbs" aria-label="Brotkrümel"><a href="./">KI-Werkstatt</a>{icon("arrow")}<a href="./#einsatz">Einsatzgebiete</a>{icon("arrow")}<span aria-current="page">{html.escape(e["h1"])}</span></nav>
<p class="kicker">{icon(e["icon"])} <b>Einsatzgebiet</b> · {len(e["aufgaben"])} Aufgaben · {n_tools} Tools</p>
<h1><em>{html.escape(e["h1"])}</em></h1>
<p class="sub">{html.escape(e["hero"])}</p>
<div class="ctas"><a class="btn btn-lime" href="#aufgaben">{icon("wrench")}Zu den Aufgaben</a><a class="btn" href="#stack-check">{icon("mail")}Kostenloser Stack-Check</a></div>
</div></section>

<section class="band cat-intro"><div class="wrap intro-grid">
<div class="intro-text reveal">{"".join(f"<p>{gl_autolink(x, set())}</p>" for x in e["intro"])}</div>
<aside class="tipp reveal">{kurbel("kb-sm", wink=True)}<p class="eyebrow">Werkstatt-Tipp</p><p>{html.escape(e["tipp"])}</p></aside>
</div></section>

<section class="band" id="aufgaben"><div class="wrap">
<p class="eyebrow">Wo KI mit anpackt</p><h2>{len(e["aufgaben"])} Aufgaben, bei denen es sich lohnt: {html.escape(e["h1"])}</h2>
<div class="aufgaben">{auf}</div>
</div></section>

<section class="band" id="trends"><div class="wrap">
<p class="eyebrow">Trend-Radar · {html.escape(label)}</p><h2>Drei Trends mit dem größten Hebel: {html.escape(e["h1"])}</h2>
<div class="trend-cards">{trend_cards}</div>
<p style="margin-top:18px"><a class="btn" href="{TRENDS_PAGE}?rolle={e['rolle']}#radar">{icon("compass")}Ganzes Trend-Radar ansehen</a></p>
</div></section>

<section class="band" id="werkzeug"><div class="wrap">
<p class="eyebrow">Weiter in der Werkstatt</p><h2>Kisten, Schubladen und Begriffe: {html.escape(e["h1"])}</h2>
<div class="kisten-refs">{kiste_html}</div>
<div class="einsatz-more">
<div><h3>{icon("layers")}Passende Schubladen</h3><div class="chips">{kat_chips}</div></div>
<div><h3>{icon("abc")}Begriffe zum Nachschlagen</h3><div class="chips">{gl_chips}</div></div>
{f'<div><h3>{icon("clock")}Zeit nachrechnen</h3>{rechner}</div>' if rechner else ""}
{rg_more(e["rolle"])}
</div></div></section>

<section class="band faq" id="faq"><div class="wrap">
<p class="eyebrow">Fragen aus der Werkstatt</p><h2>{html.escape(e["h1"])}: kurz beantwortet</h2>
<div class="faq-list">{faq_html(faq)}</div>
</div></section>

<section class="band lead" id="stack-check"><div class="wrap">
<div class="lead-grid"><div>
<p class="eyebrow">Stack-Check</p><h2>{html.escape(e["lead_hook"])}</h2>
<p class="intro">{html.escape(e["lead_text"])}</p>
<div class="kb-say">{hans("hm-md")}<p class="bubble">{html.escape(e["bubble"])}</p></div></div>
<div>{lead_form("Einsatz: " + e["h1"], "Stack-Check (" + e["h1"] + ") – KI-Werkstatt", rolle=e["form_rolle"])}</div></div>
</div></section>

<section class="band" id="weitere"><div class="wrap">
<p class="eyebrow">Andere Einsatzgebiete</p><div class="einsatz-minis">{others}</div>
</div></section>
{footer()}
"""
        (DOCS / e["page"]).write_text(page_shell(f"{e['seo_title']} – KI-Werkstatt", body, e["meta"], url,
                                                f'<script type="application/ld+json">{ld_js}</script>'), encoding="utf-8")
        pages.append(e["page"])
    return pages


# --------------------------------------------------------------------------- Ratgeber (Long-Form)
def rg_by_id():
    return {a["id"]: a for a in RATGEBER["artikel"]}


def rg_link(rid):
    if not rid:
        return ""
    a = rg_by_id().get(rid)
    if not a:
        raise SystemExit(f"data/trends.json: Ratgeber '{rid}' fehlt in data/ratgeber.json")
    return f'<p class="rg-link"><a class="btn btn-sm" href="{a["page"]}">{icon("book")}Ausführlich im Ratgeber: {html.escape(a["label"])}</a></p>'


def rg_more(rolle):
    hits = [a for a in RATGEBER["artikel"] if rolle in a["rollen"]]
    if not hits:
        return ""
    links = "".join(f'<a class="chip cat" href="{a["page"]}">{icon(a["icon"])}{html.escape(a["label"])}</a>' for a in hits)
    return f'<div data-chrome><h3>{icon("book")}Zum Weiterlesen</h3><div class="chips">{links}</div></div>'


def rg_words(md):
    return len(re.findall(r"\w+", md))


def rg_total_words(a):
    """Wörter aus Text und FAQ; Grundlage für Lesezeit auf Karte und Seite."""
    md = (RG_DIR / f"{a['id']}.md").read_text(encoding="utf-8")
    return rg_words(md) + sum(rg_words(q + " " + x) for q, x in a["faq"])


def ratgeber_band():
    cards = "".join(f"""<a class="rg-card reveal" href="{a['page']}"><span class="term-ico">{icon(a["icon"])}</span>
<span><span class="trend-no">Ratgeber · {max(1, round(rg_total_words(a) / 200))} Min. Lesezeit</span><b>{html.escape(a["h1"])}</b><small>{html.escape(a["teaser"])}</small>
<span class="drawer-cta">Lesen{icon("arrow")}</span></span></a>""" for a in RATGEBER["artikel"])
    return f"""<section class="band" id="ratgeber"><div class="wrap">
<p class="eyebrow">{html.escape(RATGEBER["titel"])}</p><h2>Zum Durchlesen statt Durchscrollen</h2>
<p class="intro">Ausführliche Anleitungen zu den Fragen, die uns gerade am häufigsten erreichen, mit Beispielen, Checklisten und allen Quellen zum Nachprüfen.</p>
<div class="rg-cards">{cards}</div>
</div></section>"""


def gl_autolink_html(markup, used):
    """Glossar-Begriffe im fertigen HTML verlinken, nur in Fließtext (nicht in Links, Code, Überschriften, Tabellenköpfen)."""
    parts = re.split(r"(<[^>]+>)", markup)
    skip = 0
    out = []
    for part in parts:
        if part.startswith("<"):
            m = re.match(r"<(/?)(a|code|h2|h3|th|strong)\b", part)
            if m:
                skip += -1 if m.group(1) else 1
            out.append(part)
        elif skip or not part.strip():
            out.append(part)
        else:
            out.append(gl_autolink(html.unescape(part), used))
    return "".join(out)


def render_md(md):
    """Kleines Markdown: ## Kapitel, ### Unterkapitel, > Kasten, - und 1. Listen, | Tabellen, Absätze."""
    blocks, toc = [], []
    lines = md.strip().split("\n")
    i = 0

    def para(buf):
        if buf:
            blocks.append(f"<p>{inline(' '.join(buf), site=True)}</p>")
    buf = []
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            para(buf)
            buf = []
            i += 1
            continue
        if ln.startswith("## "):
            para(buf)
            buf = []
            t = ln[3:].strip()
            toc.append((slug(t), t))
            blocks.append(f'<h2 id="{slug(t)}">{html.escape(t)}</h2>')
        elif ln.startswith("### "):
            para(buf)
            buf = []
            blocks.append(f"<h3>{inline(ln[4:].strip(), site=True)}</h3>")
        elif ln.startswith("> "):
            para(buf)
            buf = []
            box = []
            while i < len(lines) and lines[i].startswith("> "):
                box.append(lines[i][2:])
                i += 1
            blocks.append(f'<aside class="rg-box">{icon("spark")}<p>{inline(" ".join(box), site=True)}</p></aside>')
            continue
        elif ln.startswith("|"):
            para(buf)
            buf = []
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            head, *body = rows
            t = ['<div class="table"><table><thead><tr>'] + [f"<th>{inline(c, site=True)}</th>" for c in head] + ["</tr></thead><tbody>"]
            t += ["<tr>" + "".join(f"<td>{inline(c, site=True)}</td>" for c in r) + "</tr>" for r in body]
            blocks.append("".join(t) + "</tbody></table></div>")
            continue
        elif re.match(r"(- |\d+\. )", ln):
            para(buf)
            buf = []
            ordered = bool(re.match(r"\d+\. ", ln))
            items = []
            while i < len(lines) and re.match(r"(- |\d+\. )", lines[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i]))
                i += 1
            tag = "ol" if ordered else "ul"
            blocks.append(f'<{tag} class="plain">' + "".join(f"<li>{inline(x, site=True)}</li>" for x in items) + f"</{tag}>")
            continue
        else:
            buf.append(ln.strip())
        i += 1
    para(buf)
    return "\n".join(blocks), toc


def build_ratgeber(tools_map):
    terms = {g["t"]: g for g in GLOSSAR["begriffe"]}
    rollen = {r["id"]: r for r in TRENDS["rollen"]}
    trend_ids = {t["id"] for t in TRENDS["trends"]}
    pages = []
    for a in RATGEBER["artikel"]:
        where = f"data/ratgeber.json/{a['id']}"
        for n in a["tools"]:
            if n not in tools_map:
                raise SystemExit(f"{where}: Tool '{n}' nicht in README.de.md gefunden")
        for t in a["glossar"]:
            if t not in terms:
                raise SystemExit(f"{where}: Glossarbegriff '{t}' fehlt")
        for r in a["rollen"]:
            if r not in rollen:
                raise SystemExit(f"{where}: Rolle '{r}' fehlt in data/trends.json")
        if a.get("trend") and a["trend"] not in trend_ids:
            raise SystemExit(f"{where}: Trend '{a['trend']}' fehlt")
        if not a["quellen"]:
            raise SystemExit(f"{where}: keine Quellen")
        md = (RG_DIR / f"{a['id']}.md").read_text(encoding="utf-8")
        body_html, toc = render_md(md)
        body_html = gl_autolink_html(body_html, set())
        words = rg_total_words(a)
        minutes = max(1, round(words / 200))
        url = SITE_URL + a["page"]
        faq = [tuple(x) for x in a["faq"]]
        toc_html = "".join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in toc) + f'<a href="#faq">Fragen</a><a href="#quellen">Quellen</a>'
        tool_chips = "".join(f'<a class="chip tool" href="{html.escape(tools_map[n]["u"])}" target="_blank" rel="noopener">{favicon(tools_map[n]["u"])}{html.escape(n)}'
                             f'{NEU_BADGE if n in NEU_NAMES else ""}</a>' for n in a["tools"])
        gl_chips = "".join(f'<a class="chip" href="{GLOSSAR_PAGE}#{slug(t)}">{icon(terms[t]["icon"])}{html.escape(t)}</a>' for t in a["glossar"])
        einsatz = [e for e in EINSATZ["seiten"] if e["rolle"] in a["rollen"]]
        einsatz_chips = "".join(f'<a class="chip cat" href="{e["page"]}">{icon(e["icon"])}{html.escape(e["h1"])}</a>' for e in einsatz)
        quellen = "".join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(lbl)}</a>{f" <small>({de_date(d)})</small>" if d else ""}</li>'
                          for lbl, u, d in a["quellen"])
        others = "".join(f'<a class="einsatz-mini" href="{o["page"]}">{icon(o["icon"])}{html.escape(o["label"])}</a>' for o in RATGEBER["artikel"] if o is not a)
        trend_btn = ""
        if a.get("trend"):
            t = next(t for t in TRENDS["trends"] if t["id"] == a["trend"])
            trend_btn = f'<a class="btn" href="{TRENDS_PAGE}#{t["id"]}">{icon("chart")}Zum Trend: {html.escape(t["label"])}</a>'
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "@id": url, "url": url, "headline": a["h1"], "description": a["meta"], "inLanguage": "de-DE",
             "datePublished": a["stand"], "dateModified": a["stand"], "wordCount": words, "mainEntityOfPage": url,
             "author": {"@type": "Organization", "name": "KI-Werkstatt", "url": SITE_URL},
             "publisher": {"@type": "Organization", "name": "KI-Werkstatt", "url": SITE_URL},
             "citation": [u for _, u, _ in a["quellen"]]},
            faq_ld(faq),
            breadcrumb_ld([("KI-Werkstatt", SITE_URL), ("Ratgeber", SITE_URL + "#ratgeber"), (a["label"], url)]),
        ]}
        ld_js = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
        body = f"""{topbar(False, "ratgeber")}
<section class="hero rg-hero"><div class="hero-art">{hero_floats()}</div><div class="wrap">
<nav class="crumbs" aria-label="Brotkrümel"><a href="./">KI-Werkstatt</a>{icon("arrow")}<a href="./#ratgeber">Ratgeber</a>{icon("arrow")}<span aria-current="page">{html.escape(a["label"])}</span></nav>
<p class="kicker" data-chrome>{icon(a["icon"])} <b>Ratgeber</b> · Stand {de_date(a["stand"])} · {minutes} Min. Lesezeit</p>
<h1>{html.escape(a["h1"])}</h1>
<p class="sub">{html.escape(a["hero"])}</p>
<div class="ctas"><a class="btn btn-lime" href="#{toc[0][0] if toc else 'faq'}">{icon("book")}Lesen</a><a class="btn" href="#stack-check">{icon("mail")}Kostenloser Stack-Check</a></div>
</div></section>

<div class="wrap layout rg-layout">
<aside class="rail" data-chrome><div class="in"><h4>Inhalt</h4>{toc_html}
<div class="lead-mini"><b>Stack-Check</b><a class="btn btn-sm" href="#stack-check">{icon("mail")}Anfragen</a></div></div></aside>
<article class="content rg-body">
{body_html}
<section class="rg-extras">
<div><h3>{icon("wrench")}Werkzeug zum Thema</h3><div class="chips">{tool_chips}</div></div>
<div><h3>{icon("abc")}Begriffe zum Nachschlagen</h3><div class="chips">{gl_chips}</div></div>
<div><h3>{icon("layers")}Passende Einsatzgebiete</h3><div class="chips">{einsatz_chips}</div></div>
</section>
<p class="rg-trend">{trend_btn}</p>
<section id="faq" class="rg-faq"><h2>Häufige Fragen</h2><div class="faq-list">{faq_html(faq)}</div></section>
<section id="quellen" class="rg-quellen" data-chrome><h2>Quellen</h2><ol>{quellen}</ol></section>
</article>
</div>

<section class="band lead" id="stack-check"><div class="wrap">
<div class="lead-grid"><div>
<p class="eyebrow">Stack-Check</p><h2>{html.escape(a["lead_hook"])}</h2>
<p class="intro">{html.escape(a["lead_text"])}</p>
<div class="kb-say">{hans("hm-md")}<p class="bubble">{html.escape(a["bubble"])}</p></div></div>
<div>{lead_form("Ratgeber: " + a["label"], "Stack-Check (Ratgeber " + a["label"] + ") – KI-Werkstatt")}</div></div>
</div></section>

<section class="band" id="weitere"><div class="wrap">
<p class="eyebrow">Weitere Ratgeber</p><div class="einsatz-minis">{others}</div>
</div></section>
{footer()}
"""
        (DOCS / a["page"]).write_text(page_shell(f"{a['seo_title']} – KI-Werkstatt", body, a["meta"], url,
                                                f'<script type="application/ld+json">{ld_js}</script>'), encoding="utf-8")
        pages.append(a["page"])
    return pages


def build_feed(list_secs):
    home = tool_home(list_secs)
    # Nur bereits gestartete Neuzugänge; abgelaufene bleiben als Historie im Feed
    neu = [t for t in NEU["tools"] if date.fromisoformat(t["seit"]) <= date.today()]
    stamp = max([TRENDS["stand"]] + [t["seit"] for t in neu] + [a["stand"] for a in RATGEBER["artikel"]]) + "T00:00:00Z"
    x = html.escape
    entries = []
    for t in TRENDS["trends"]:
        u = f"{SITE_URL}{TRENDS_PAGE}#{t['id']}"
        entries.append(f'<entry><title>{x(t["titel"])}</title><link href="{x(u)}"/><id>{x(u)}</id><updated>{TRENDS["stand"]}T00:00:00Z</updated><summary>{x(t["kurz"])}</summary></entry>')
    for a in RATGEBER["artikel"]:
        u = SITE_URL + a["page"]
        entries.append(f'<entry><title>{x(a["h1"])}</title><link href="{x(u)}"/><id>{x(u)}</id><updated>{a["stand"]}T00:00:00Z</updated><summary>{x(a["teaser"])}</summary></entry>')
    for t in neu:
        u = SITE_URL + home[t["name"]]
        entries.append(f'<entry><title>Neu in der Liste: {x(t["name"])}</title><link href="{x(u)}"/><id>{x(SITE_URL)}neu/{slug(t["name"])}</id>'
                       f'<updated>{t["seit"]}T00:00:00Z</updated><summary>{x(t["notiz"])}</summary></entry>')
    (DOCS / "feed.xml").write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="de"><title>KI-Werkstatt: Trends und Neuzugänge</title>
<link href="{SITE_URL}feed.xml" rel="self"/><link href="{SITE_URL}{TRENDS_PAGE}"/><id>{SITE_URL}feed.xml</id><updated>{stamp}</updated>
<author><name>KI-Werkstatt</name></author>
{chr(10).join(entries)}
</feed>
""", encoding="utf-8")


def csv_safe(v):
    """Zellen, die wie eine Tabellenformel beginnen, bekommen ein führendes Hochkomma (CSV-Injection)."""
    if isinstance(v, str) and v[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + v
    return v


def build_data(uniq, sections, pages=(), list_secs=()):
    page_ids = {s["id"] for s in list_secs}
    first = {}
    # Zuerst die Fundstelle in einer Kategorie (sachlicher Text, eigene Seite), Favoriten nur als Rückfall
    ordered = [x for x in all_items(sections) if x[0]["id"] != "empfehlungen-der-redaktion"] + \
              [x for x in all_items(sections) if x[0]["id"] == "empfehlungen-der-redaktion"]
    for s, sub, it in ordered:
        first.setdefault(it["url"], (s, sub, it))
    rows = []
    for url in uniq:
        s, sub, it = first[url]
        eu, oss, clean = item_meta(it)
        seite = (cat_page(s["id"]) + (f"#{sub['id']}" if sub else "")) if s["id"] in page_ids else f"./#{s['id']}"
        rows.append({"name": it["name"], "url": it["url"], "beschreibung": clean, "kategorie": s["title"], "bereich": sub["title"] if sub else "",
                     "eu": eu, "open_source": oss, "neu": it["name"] in NEU_NAMES, "seite": seite})
    (DOCS / "tools.json").write_text(json.dumps({"gebaut": TODAY, "link_check": LINK_CHECK, "quelle": REPO_URL, "tools": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    with (DOCS / "tools.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("ja" if v is True else "nein" if v is False else csv_safe(v)) for k, v in r.items()})
    lastmod = date.today().isoformat()
    urls = "".join(f"<url><loc>{SITE_URL}{pg}</loc><lastmod>{lastmod}</lastmod></url>" for pg in ("",) + tuple(pages))
    (DOCS / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                      f"{urls}</urlset>\n", encoding="utf-8")
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
    uniq, n_tools, n_cats, list_secs, tools_map = build_index(sections, head_md)
    pages = build_category_pages(list_secs, tools_map)
    pages.append(build_glossar(tools_map, list_secs, sections))
    pages.append(build_trends(tools_map, list_secs))
    pages += build_einsatz(tools_map, list_secs, sections)
    pages += build_ratgeber(tools_map)
    build_feed(list_secs)
    build_subpages(list_secs)
    build_data(uniq, sections, pages, list_secs)
    build_og(n_tools, n_cats)
    print(f"docs/index.html: {n_tools} Tools, {n_cats} Kategorien, {len(list(IMG.glob('cat-*.svg')))} Grafiken, {len(pages)} Unterseiten")
    from check_unique import find_duplicates
    dups = find_duplicates(DOCS)
    if dups:
        for sent, where in dups[:20]:
            print(f"  doppelt: {sent[:90]!r} in {', '.join(where)}")
        raise SystemExit(f"Abbruch: {len(dups)} Sätze stehen auf mehr als einer Seite (oder doppelt auf einer). Texte umschreiben.")
    print("Uniqueness-Check: kein Satz doppelt")


if __name__ == "__main__":
    main()
