#!/usr/bin/env python3
"""Layer A: unsichtbare Unicode-Zeichen und Metadaten-Chunks in geänderten Dateien finden.

Aufruf aus dem Repo-Root:
    python3 scripts/layer_a.py          # prüft geänderte und neue Dateien (git)
    python3 scripts/layer_a.py --fix    # entfernt unsichtbare Zeichen aus Textdateien

Erlaubt ist nur das BOM am Anfang von CSV-Dateien (Excel braucht es für Umlaute).
PNG-Dateien dürfen nur IHDR, IDAT, IEND und PLTE/tRNS enthalten, keine tEXt/iTXt/eXIf/caBX-Chunks.
"""
import re
import struct
import subprocess
import sys

BAD = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\u00ad\u180e\u2066-\u2069]")
PNG_OK = {"IHDR", "IDAT", "IEND", "PLTE", "tRNS", "gAMA", "sRGB"}


def changed_files():
    out = subprocess.check_output(["git", "ls-files", "-m", "-o", "--exclude-standard"]).decode().split()
    staged = subprocess.check_output(["git", "diff", "--cached", "--name-only"]).decode().split()
    return sorted(set(out + staged))


def png_chunks(path):
    d = open(path, "rb").read()
    i, chunks = 8, set()
    while i < len(d):
        n = struct.unpack(">I", d[i:i + 4])[0]
        chunks.add(d[i + 4:i + 8].decode("latin-1"))
        i += 12 + n
    return chunks


def main():
    fix = "--fix" in sys.argv
    problems = []
    for f in changed_files():
        try:
            if f.endswith(".png"):
                extra = png_chunks(f) - PNG_OK
                if extra:
                    problems.append(f"{f}: PNG-Metadaten {sorted(extra)}")
                continue
            if f.endswith((".jpg", ".jpeg", ".webp", ".gif", ".ico", ".woff", ".woff2", ".pdf")):
                continue
            s = open(f, encoding="utf-8").read()
        except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError):
            continue
        body = s[1:] if f.endswith(".csv") and s.startswith("\ufeff") else s
        hits = BAD.findall(body)
        if hits:
            if fix:
                clean = BAD.sub("", body)
                open(f, "w", encoding="utf-8").write(("\ufeff" if body is not s else "") + clean)
                print(f"bereinigt: {f} ({len(hits)} Zeichen)")
            else:
                problems.append(f"{f}: {len(hits)} unsichtbare Zeichen")
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("Layer A: sauber")


if __name__ == "__main__":
    main()
