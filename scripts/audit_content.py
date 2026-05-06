#!/usr/bin/env python3
"""Audit every content/**/*.md for front-matter completeness, deferred
Quarto-era carryover, and asset references that don't resolve.

Run locally and in CI. Exits non-zero if any HARD failure is found.

Hard failures:
  - file has no YAML front matter
  - file has no `title` field
  - unit page (under content/track_*/units/) is missing any of:
      niveau, klassenstufe, track, unit_nr, bildungsplan, skills_focus,
      presentation.file, worksheet.file, vgwort_pixel
  - any image / static asset link in the body resolves to a file that
    does not exist under static/ or assets/
  - leftover Quarto-only constructs in body:
      ::: {.foo} fenced divs (other than the migrated .vgwort-pixel /
      .callout-* / known classes — but the migrator should have stripped
      all of them)
      `@sec-...`, `@fig-...`, `@tbl-...` Pandoc cross-refs
      `#| echo: false` etc. Quarto execution YAML in fenced code

Soft warnings (non-blocking):
  - non-unit page missing tags
  - non-unit page > 1800 chars without vgwort_pixel
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "content"
STATIC = REPO / "static"
ASSETS = REPO / "assets"

UNIT_RE = re.compile(r"track_[a-z]+_kl\d+/units/.+\.md$")
FM_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)", re.DOTALL)
QUARTO_DIV_RE = re.compile(r"^:::\s*\{\.([A-Za-z0-9_-]+)", re.MULTILINE)
QUARTO_XREF_RE = re.compile(r"\B@(sec|fig|tbl|eq)-[A-Za-z0-9_-]+")
QUARTO_EXEC_RE = re.compile(r"^#\|\s*[a-zA-Z]+\s*:", re.MULTILINE)
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
HREF_LOCAL_RE = re.compile(r"\]\(/[^)]+\)")

UNIT_REQUIRED = (
    "title", "niveau", "klassenstufe", "track", "unit_nr",
    "bildungsplan", "skills_focus",
)


def asset_resolves(rel_url: str) -> bool:
    """Return True if a leading-slash URL maps to a file under static/ or
    inside a page bundle. URL is rendered against the site root, not /fle/
    — that prefix is added by Hugo's relURL at template time."""
    rel_url = rel_url.split("#", 1)[0].split("?", 1)[0]
    if not rel_url.startswith("/"):
        return True   # external or relative — out of scope here
    parts = rel_url.lstrip("/").split("/")
    candidates = [STATIC.joinpath(*parts), ASSETS.joinpath(*parts)]
    return any(p.exists() for p in candidates)


def audit_file(md: Path) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warns: list[str] = []
    text = md.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        fails.append("no YAML front matter")
        return fails, warns
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        fails.append(f"YAML parse error: {exc}")
        return fails, warns
    body = m.group(2)
    rel = md.relative_to(REPO).as_posix()

    # Frontmatter checks
    if not fm.get("title"):
        fails.append("missing required field: title")
    if UNIT_RE.search(rel):
        for k in UNIT_REQUIRED:
            if k not in fm or fm[k] in (None, ""):
                fails.append(f"unit missing required field: {k}")
        pres = fm.get("presentation") or {}
        if not isinstance(pres, dict) or not pres.get("file"):
            fails.append("unit missing presentation.file")
        ws = fm.get("worksheet") or {}
        if not isinstance(ws, dict) or not ws.get("file"):
            fails.append("unit missing worksheet.file")
        if not fm.get("vgwort_pixel"):
            fails.append("unit missing vgwort_pixel")

    # Quarto-era carryover in body
    for divmatch in QUARTO_DIV_RE.finditer(body):
        cls = divmatch.group(1)
        if not cls.startswith("callout-") and cls not in {
            "vgwort-pixel", "hero-kicker", "lead", "card-grid", "card",
            "cefr-badge", "notes",
        }:
            fails.append(f"unmigrated Quarto fenced div: ::: {{.{cls}}}")
    if QUARTO_XREF_RE.search(body):
        fails.append("unmigrated Quarto cross-ref (@sec/@fig/@tbl/@eq)")
    if QUARTO_EXEC_RE.search(body):
        fails.append("Quarto execution YAML chunk (#| key: value) still in body")

    # Asset paths
    for img in IMG_RE.findall(body):
        if img.startswith("/") and not asset_resolves(img):
            fails.append(f"unresolved image path: {img}")

    # Soft warnings on non-unit pages
    if not UNIT_RE.search(rel):
        if "tags" not in fm:
            warns.append("no tags")
        body_chars = len(re.sub(r"\s+", " ", body))
        if body_chars >= 1800 and not fm.get("vgwort_pixel"):
            warns.append(f">=1800 chars ({body_chars}) without vgwort_pixel")

    return fails, warns


def main() -> int:
    files = sorted(CONTENT.rglob("*.md"))
    n_files = len(files)
    n_units = 0
    total_fails: dict[str, list[str]] = {}
    total_warns: dict[str, list[str]] = {}
    for md in files:
        rel = md.relative_to(REPO).as_posix()
        if UNIT_RE.search(rel):
            n_units += 1
        fails, warns = audit_file(md)
        if fails:
            total_fails[rel] = fails
        if warns:
            total_warns[rel] = warns

    print(f"Audited {n_files} content/.md files ({n_units} unit pages).")
    if total_warns:
        print(f"\nWarnings ({sum(len(v) for v in total_warns.values())}):")
        for path in sorted(total_warns)[:25]:
            for w in total_warns[path]:
                print(f"  {path}: {w}")
        rest = max(0, len(total_warns) - 25)
        if rest:
            print(f"  ... and {rest} more warning files.")
    if total_fails:
        print(f"\n::error::Hard failures ({sum(len(v) for v in total_fails.values())}):", file=sys.stderr)
        for path in sorted(total_fails):
            for f in total_fails[path]:
                print(f"  {path}: {f}", file=sys.stderr)
        return 1
    print("\nAll content/.md files pass mandatory checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
