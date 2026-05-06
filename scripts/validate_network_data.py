#!/usr/bin/env python3
"""Validate static/network/graph.json against the Materials Network schema.

Defense-in-depth on top of `_scripts/build_graph.py` — that script is the
producer; this script is the consumer-side gate. If someone edits the JSON
by hand or a future builder regresses, this catches it.

Hard fails (exit 1):
  1. Any node missing `id` | `type` | `title` | `url`
  2. Duplicate node `id`
  3. Duplicate node `url` (separate offence: two distinct ids pointing at
     the same page would split the graph in confusing ways)
  4. Any edge referencing a `source` or `target` that isn't a known node
     (= dangling edge)
  5. Any node carrying a `topic` that isn't declared in `data/topics.yml`
  6. Article node count != count of unit pages on disk (content/track_*/
     units/*.md)

Soft warnings (printed, not blocking):
  - Article nodes whose `url` doesn't 404-locally — there's no page on disk
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
GRAPH = REPO / "static" / "network" / "graph.json"
TOPICS = REPO / "data" / "topics.yml"
CONTENT_UNITS_GLOB = "content/track_*/units/*.md"


def fail(msg: str) -> None:
    print(f"::error::{msg}", file=sys.stderr)


def main() -> int:
    if not GRAPH.exists():
        fail(f"missing {GRAPH.relative_to(REPO)} — run _scripts/build_graph.py first")
        return 1
    with GRAPH.open(encoding="utf-8") as fh:
        data = json.load(fh)

    nodes = data.get("nodes") or []
    edges = data.get("edges") or []
    if not nodes:
        fail("graph.json has zero nodes")
        return 1

    fails = 0

    # 1. Required fields per node
    for n in nodes:
        for k in ("id", "type", "title", "url"):
            if k not in n or n[k] in (None, ""):
                fail(f"node missing required field {k!r}: {n.get('id', '<no id>')}")
                fails += 1

    # 2/3. Duplicate id and duplicate url
    id_counts = Counter(n.get("id") for n in nodes if n.get("id"))
    for nid, c in id_counts.items():
        if c > 1:
            fail(f"duplicate node id ({c}×): {nid}")
            fails += 1
    url_counts = Counter(
        n.get("url") for n in nodes
        if n.get("url") and n.get("type") == "article"
    )
    for url, c in url_counts.items():
        if c > 1:
            fail(f"duplicate article url ({c}×): {url}")
            fails += 1

    # 4. Dangling edges
    known = {n["id"] for n in nodes if n.get("id")}
    for i, e in enumerate(edges):
        s, t = e.get("source"), e.get("target")
        if s not in known:
            fail(f"edge[{i}] dangling source: {s!r}")
            fails += 1
        if t not in known:
            fail(f"edge[{i}] dangling target: {t!r}")
            fails += 1

    # 5. Topic registry coherence
    if TOPICS.exists():
        with TOPICS.open(encoding="utf-8") as fh:
            topics = yaml.safe_load(fh) or []
        topic_ids = {t.get("id") for t in topics if t.get("id")}
        for n in nodes:
            tid = n.get("topic")
            if tid and tid not in topic_ids:
                fail(f"node {n.get('id')} carries unregistered topic {tid!r}")
                fails += 1

    # 6. Article count parity vs disk
    article_nodes = [n for n in nodes if n.get("type") == "article"]
    on_disk = list(REPO.glob(CONTENT_UNITS_GLOB))
    if len(article_nodes) != len(on_disk):
        fail(f"article-node count ({len(article_nodes)}) != "
             f"unit-page count on disk ({len(on_disk)})")
        fails += 1

    # Soft warnings: article node points at an article URL with no
    # corresponding rendered HTML in public/. Only meaningful after a
    # Hugo build, so we just check whether `content/<...>/<slug>.md`
    # exists — Hugo's slug override may differ but the source must be
    # there.
    warns = 0
    for n in article_nodes:
        url = (n.get("url") or "").strip("/")
        if not url:
            continue
        # url shape: /track_e_kl06/units/<slug>/  -> source under content/
        source_glob = REPO / "content" / url
        if not source_glob.exists() and not (source_glob.parent.parent / "units").is_dir():
            print(f"  warn: article node {n.get('id')} -> {url} has no source dir",
                  file=sys.stderr)
            warns += 1

    print(f"Validated {len(nodes)} nodes, {len(edges)} edges, "
          f"{len(article_nodes)} articles ({fails} hard / {warns} soft).")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
