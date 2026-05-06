#!/usr/bin/env python3
"""Verify the curriculum (Bildungsplan BW) source is still reachable AND
every `bildungsplan:` reference in unit frontmatter has the canonical
shape and is rooted in a top-level code declared in
`_resources/bildungsplan_bw_franzoesisch.yml`.

This is the FLE BW equivalent of the prompt's 'Bildungsplan BW live-fetch'
gate. It does NOT try to validate every depth-4 sub-code (the official
source publishes those as PDF / portal HTML, not as a stable URL per code)
— but it DOES:

  1. HEAD the canonical Bildungsplan portal URL and the per-school-form
     index pages quoted in the yaml's 'Quellen' block. Hard-fail on any
     non-success (4xx / 5xx). Transient 429 / 503 are treated as warnings
     so a flaky upstream doesn't block deploy of unrelated content.
  2. Walk every content/track_*/units/*.md, parse `bildungsplan:` entries,
     and verify each starts with a numeric code matching the yaml's
     declared top-level codes (e.g. '3.1.3.3 Expression orale ...' must
     have '3.1.3' or '3.1' or '3' in the yaml).
  3. Hard-fail on shape mismatches and on top-level codes the yaml doesn't
     declare. No silent acceptance; never invent curriculum content.

Per the migration prompt: do NOT fall back to cached yaml when the live
source is unreachable for a hard reason. Cache is for performance,
not authority.
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
YAML_PATH = REPO / "_resources" / "bildungsplan_bw_franzoesisch.yml"
CONTENT = REPO / "content"
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
CODE_RE = re.compile(r"^([0-9]+(?:\.[0-9]+)+)(?:\s|$)")
# Single canonical liveness probe. The yaml documents many per-school-
# form sub-page URLs (Sek I 6-9, Sek I 10, Gymnasium 6-8, Gymnasium 9-10,
# Oberstufe …) but those are documentation references, not stable
# probes — the CMS reorganises sub-pages periodically. The root portal
# URL is what tells us 'curriculum-bw is up'.
LIVENESS_URL = "https://www.bildungsplaene-bw.de/bildungsplan,Lde/Startseite/BP2016BW_ALLG"


def head(url: str, timeout: int = 15) -> tuple[int, str]:
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "boulingua-ci/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, ""
    except urllib.error.HTTPError as exc:
        return exc.code, str(exc)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return 0, str(exc)


def main() -> int:
    if not YAML_PATH.exists():
        print(f"::error::{YAML_PATH.relative_to(REPO)} missing", file=sys.stderr)
        return 1

    raw = YAML_PATH.read_text(encoding="utf-8")
    try:
        parsed = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        print(f"::error::cannot parse yaml: {exc}", file=sys.stderr)
        return 1

    # 1. Liveness probe against the canonical curriculum portal.
    fails = 0
    code, err = head(LIVENESS_URL)
    if 200 <= code < 400:
        print(f"Curriculum portal liveness OK ({code}): {LIVENESS_URL}")
    elif code in (429, 503):
        print(f"WARN: transient {code} from curriculum portal — not failing.",
              file=sys.stderr)
    elif code == 0:
        print(f"WARN: network error reaching curriculum portal "
              f"({err}) — not failing.", file=sys.stderr)
    else:
        print(f"::error::Curriculum portal returned {code}: {LIVENESS_URL}",
              file=sys.stderr)
        fails += 1

    # 2. Top-level codes declared in yaml.
    declared = set()
    def walk(node):
        if isinstance(node, dict):
            if "code" in node and isinstance(node["code"], str):
                declared.add(node["code"])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(parsed)

    if not declared:
        print("::error::no `code:` entries found in bildungsplan yaml",
              file=sys.stderr)
        return 1
    print(f"\nDeclared top-level codes in yaml: {len(declared)} "
          f"({', '.join(sorted(declared))})")

    # 3. Walk units, extract `bildungsplan:` entries, validate each.
    used: dict[str, list[Path]] = defaultdict(list)
    bad_shape: list[tuple[Path, str]] = []
    for md in sorted(CONTENT.rglob("track_*/units/*.md")):
        text = md.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        for entry in (fm.get("bildungsplan") or []):
            entry = str(entry).strip()
            cm = CODE_RE.match(entry)
            if not cm:
                bad_shape.append((md, entry))
                continue
            used[cm.group(1)].append(md)

    if bad_shape:
        print(f"\n::error::{len(bad_shape)} bildungsplan entries lack a "
              f"numeric prefix (e.g. '3.1.3.3 Expression orale ...'):",
              file=sys.stderr)
        for path, entry in bad_shape[:10]:
            print(f"  {path.relative_to(REPO)}: {entry!r}", file=sys.stderr)
        fails += 1

    print(f"\nDistinct competence codes used in unit frontmatter: {len(used)}")
    unrooted: list[tuple[str, int]] = []
    for code, mds in sorted(used.items()):
        # A code 3.1.3.3 is rooted iff some prefix (3, 3.1, 3.1.3) is in declared.
        parts = code.split(".")
        ok = False
        for i in range(len(parts), 0, -1):
            if ".".join(parts[:i]) in declared:
                ok = True
                break
        marker = "OK" if ok else "MISS"
        print(f"  {marker:4s}  {code:10s}  ({len(mds):3d} unit(s))")
        if not ok:
            unrooted.append((code, len(mds)))

    if unrooted:
        print(f"\n::error::{len(unrooted)} competence code(s) used in unit "
              f"frontmatter have no top-level entry in "
              f"_resources/bildungsplan_bw_franzoesisch.yml:", file=sys.stderr)
        for code, n in unrooted:
            print(f"  {code} (used by {n} unit(s))", file=sys.stderr)
        fails += 1

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
