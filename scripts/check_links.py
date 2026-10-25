#!/usr/bin/env python3
"""Prüft alle Links in README.de.md und schreibt das Ergebnis nach data/linkcheck.json.

Nur dieses Skript darf das Link-Check-Datum setzen; der Seiten-Generator liest es nur.
Aufruf aus dem Repo-Root:
    python3 scripts/check_links.py

Erreichbar = HTTP 2xx/3xx oder Bot-Schutz (401/403/429). Ein 405 auf HEAD löst den GET-Versuch aus;
ein 405 auf GET gilt als nicht erreichbar. Alles andere wird gelistet.
"""
import hashlib
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "README.de.md"
OUT = ROOT / "data" / "linkcheck.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
OK_CODES = {401, 403, 429}  # Bot-Schutz: Seite existiert, mag nur keine Skripte; 405 ist absichtlich nicht dabei
DEST = r"((?:[^()\s]|\([^()\s]*\))+)"


def status(url):
    ctx = ssl.create_default_context()
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"}, method=method)
        try:
            with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and not (200 <= e.code < 400 or e.code in OK_CODES):
                continue  # manche Server beantworten HEAD anders als GET (405 eingeschlossen)
            return e.code
        except Exception:
            if method == "HEAD":
                continue
            return 0
    return 0


def extract_urls(md):
    """Alle geprüften Links der README; "https://url" ist das Format-Beispiel unter Mitmachen."""
    return sorted({u for u in re.findall(r"\]\(" + DEST + r"\)", md) if u.startswith("http") and u != "https://url"})


def url_hash(urls):
    """Fingerabdruck der Linkliste; der Generator vergleicht ihn mit dem Report."""
    return hashlib.sha256("\n".join(urls).encode("utf-8")).hexdigest()


def main():
    md = SRC.read_text(encoding="utf-8")
    urls = extract_urls(md)
    with ThreadPoolExecutor(max_workers=24) as ex:
        results = dict(zip(urls, ex.map(status, urls)))
    dead = {u: c for u, c in results.items() if not (200 <= c < 400 or c in OK_CODES)}
    report = {
        "date": date.today().isoformat(),
        "urls_sha256": url_hash(urls),
        "checked": len(urls),
        "ok": len(urls) - len(dead),
        "bot_protected": sum(1 for c in results.values() if c in OK_CODES),
        "dead": dead,
        "method": "HTTP HEAD, bei Nicht-OK (auch 405) GET; 2xx/3xx und Bot-Schutz (401/403/429) gelten als erreichbar",
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{report['checked']} Links geprüft, {len(dead)} tot -> {OUT.relative_to(ROOT)}")
    for u, c in sorted(dead.items()):
        print(f"  {c:>3} {u}")
    sys.exit(1 if dead else 0)


if __name__ == "__main__":
    main()
