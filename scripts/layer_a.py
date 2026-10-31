#!/usr/bin/env python3
"""Layer A: unsichtbare Unicode-Zeichen und Metadaten-Chunks in geänderten Dateien finden.

Aufruf aus dem Repo-Root:
    python3 scripts/layer_a.py          # prüft geänderte und neue Dateien (git)
    python3 scripts/layer_a.py --fix    # entfernt unsichtbare Zeichen aus Textdateien

Erlaubt ist nur das BOM am Anfang von CSV-Dateien (Excel braucht es für Umlaute).
PNG-Dateien dürfen nur IHDR, IDAT, IEND und PLTE/tRNS enthalten, keine tEXt/iTXt/eXIf/caBX-Chunks.
"""
import os
import re
import struct
import subprocess
import sys

BAD = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\u00ad\u180e\u2066-\u2069]")
BOM = "\ufeff"  # erlaubt nur am Anfang von CSV-Dateien
PNG_OK = {"IHDR", "IDAT", "IEND", "PLTE", "tRNS", "gAMA", "sRGB"}


def git_paths(*args):
    # NUL-getrennt: Pfade mit Leerzeichen oder Umlauten bleiben unverändert
    out = subprocess.check_output(["git", *args, "-z"]).decode("utf-8", "surrogateescape")
    return [x for x in out.split("\0") if x]


def changed_files():
    work = git_paths("ls-files", "-m", "-o", "--exclude-standard")
    staged = git_paths("diff", "--cached", "--name-only", "--diff-filter=d")
    return sorted(set(work + staged)), set(staged)


def versions(f, staged):
    """Arbeitskopie und, falls gestaged, die Fassung im Index (die wird committet)."""
    out = []
    if os.path.islink(f):
        # Symlinks nie auflösen: nur den Linktext prüfen, --fix schreibt hier nichts
        out.append(("Symlink", os.fsencode(os.readlink(f))))
    else:
        try:
            out.append(("Arbeitskopie", open(f, "rb").read()))
        except (FileNotFoundError, IsADirectoryError):
            pass
    if f in staged:
        try:
            out.append(("Index", subprocess.check_output(["git", "show", ":" + f])))
        except subprocess.CalledProcessError:
            pass
    return out


def png_chunks(d):
    i, chunks = 8, set()
    while i < len(d):
        n = struct.unpack(">I", d[i:i + 4])[0]
        chunks.add(d[i + 4:i + 8].decode("latin-1"))
        i += 12 + n
    return chunks


def main():
    fix = "--fix" in sys.argv
    files, staged = changed_files()
    problems = []
    for f in files:
        low = f.lower()  # .PNG und .png gleich behandeln
        link = os.path.islink(f)  # Linktext ist immer Text, egal welche Endung
        if not link and low.endswith((".jpg", ".jpeg", ".webp", ".gif", ".ico", ".woff", ".woff2", ".pdf")):
            continue
        for where, data in versions(f, staged):
            if not link and low.endswith(".png"):
                try:
                    extra = png_chunks(data) - PNG_OK
                except (struct.error, UnicodeDecodeError):
                    problems.append(f"{f} ({where}): PNG nicht lesbar")
                    continue
                if extra:
                    problems.append(f"{f} ({where}): PNG-Metadaten {sorted(extra)}")
                continue
            try:
                s = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            body = s[1:] if low.endswith(".csv") and s.startswith(BOM) else s
            hits = BAD.findall(body)
            if not hits:
                continue
            if fix and where == "Arbeitskopie":
                clean = BAD.sub("", body)
                open(f, "w", encoding="utf-8").write((BOM if body is not s else "") + clean)
                print(f"bereinigt: {f} ({len(hits)} Zeichen)" + (", bitte neu stagen" if f in staged else ""))
            else:
                problems.append(f"{f} ({where}): {len(hits)} unsichtbare Zeichen")
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("Layer A: sauber")


if __name__ == "__main__":
    main()
