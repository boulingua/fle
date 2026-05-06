"""
Add Hugo `aliases:` frontmatter to every migrated content/*.md so the old
Quarto .html URLs continue to resolve (308 redirect via Hugo alias HTML).

Idempotent: only inserts an alias if absent. Aliases follow Quarto's URL
shape (filename stem with .html, e.g. /a_propos.html). For section _index.md
files the alias is the directory's old index.html (e.g. /track_e_kl06/index.html).
"""
from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
CONTENT = REPO / "content"

YAML_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def legacy_url(md: pathlib.Path) -> str | None:
    rel = md.relative_to(CONTENT).as_posix()
    if rel == "_index.md":
        return "/index.html"
    if rel.endswith("/_index.md"):
        return "/" + rel[: -len("/_index.md")] + "/index.html"
    if rel == "materiel/_index.md" or rel.startswith("materiel/"):
        return None  # new pages, no legacy URL
    return "/" + rel[:-3] + ".html"  # .md -> .html


def upsert_alias(md: pathlib.Path) -> bool:
    legacy = legacy_url(md)
    if not legacy:
        return False
    text = md.read_text(encoding="utf-8")
    m = YAML_RE.match(text)
    if not m:
        return False
    fm, body = m.group(1), text[m.end():]
    # If aliases: already lists this URL, skip.
    if re.search(rf"^aliases:.*\n((?:\s+-\s+.*\n)*)\s*-\s*['\"]?{re.escape(legacy)}['\"]?",
                 fm, re.MULTILINE):
        return False
    if re.search(rf"^\s*-\s*['\"]?{re.escape(legacy)}['\"]?\s*$", fm, re.MULTILINE):
        return False
    # Append an aliases block (or extend existing).
    if re.search(r"^aliases:\s*\n", fm, re.MULTILINE):
        fm = re.sub(
            r"^(aliases:\s*\n(?:\s+-\s+.*\n)*)",
            lambda mm: mm.group(1) + f'  - "{legacy}"\n',
            fm, count=1, flags=re.MULTILINE,
        )
    elif re.search(r"^aliases:\s*\[.*\]\s*$", fm, re.MULTILINE):
        # Inline list — leave as-is and append a block list line below
        fm += f'\naliases_legacy:\n  - "{legacy}"\n'  # safe noop key
    else:
        fm += f'\naliases:\n  - "{legacy}"\n'
    md.write_text("---\n" + fm.rstrip("\n") + "\n---\n" + body, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for md in CONTENT.rglob("*.md"):
        if upsert_alias(md):
            changed += 1
    print(f"Added aliases to {changed} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
