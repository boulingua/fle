"""Final translation polish — remaining German tokens in body text only.
Excludes German legal pages (datenschutz, impressum, haftungsausschluss) and
the bibliography page (verbatim referential names retained there)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "docs", "_resources", "_scripts"}
EXCLUDE_FILES = {
    "bibliographie.qmd",
    "datenschutz.qmd",
    "impressum.qmd",
    "haftungsausschluss.qmd",
}

SUBS: list[tuple[str, str]] = [
    (r"\bInhalt\b", "Contenu"),
    (r"\bSprache\b", "Langue"),
    (r"sehr gut", "très bien"),
    (r"\bSchriftliche\b", "Écrit"),
    (r"\bMündliche\b", "Oral"),
    (r"Erwartungshorizont", "horizon d'attente"),
    (r"\bGenügend\b", "Suffisant"),
]


def main() -> None:
    changed = 0
    for p in ROOT.rglob("*.qmd"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.name in EXCLUDE_FILES:
            continue
        text = p.read_text(encoding="utf-8")
        new = text
        for pattern, repl in SUBS:
            new = re.sub(pattern, repl, new)
        if new != text:
            p.write_text(new, encoding="utf-8")
            changed += 1
    print(f"polished {changed} files")


if __name__ == "__main__":
    main()
