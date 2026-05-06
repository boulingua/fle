#!/usr/bin/env python3
"""Build static/network/graph.json — Materials Discovery Network data.

The Phase 5 prompt suggests a Hugo custom output format. We instead
generate the graph from Python because:

  - This repo already uses _scripts/*.py for build-time data shaping
    (see make_materials.py, pdf_attribution.py).
  - Topic-typo normalisation (e.g. `hör_hörsehverstehen` →
    `hoerverstehen`) needs explicit logic. Cleaner in Python than in
    a Hugo template.
  - Edge construction (≥2 shared bildungsplan anchors) is O(N²);
    Python with dict lookups is faster and easier to test than a
    Hugo template doing the same with `intersect`.

What this script does:

  1. Reads data/topics.yml — the topic registry.
  2. Walks every content/track_*/units/*.md and extracts frontmatter.
  3. For each material-bearing article (one with `presentation:`
     and/or `worksheet:`), emits up to three nodes (article,
     presentation, worksheet) into graph.json.
  4. Forms edges:
       - kind=same-article, weight=3, between an article and each
         of its presentation/worksheet nodes (always emitted).
       - kind=shared-tags, weight=N, between any two articles that
         share ≥2 bildungsplan curriculum anchors. Capped at 5
         visually. (Course-only `tags:` like classe-6 / niveau-e
         are ignored — they would collapse the graph into one
         clique per grade level.)
  5. Computes facets (counts per type / course / topic / tag /
     date range).
  6. Enforces Phase 5 CI gates: zero tags / unknown topic / zero
     edges / orphan topic. Loud, specific errors. Exit 1 on any.

Output: static/network/graph.json (≈ 1300 nodes for fle today).
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOPICS_PATH = ROOT / "data" / "topics.yml"
CONTENT_ROOT = ROOT / "content"
OUT_PATH = ROOT / "static" / "network" / "graph.json"

# --- skills_focus → topic id normalisation ---------------------------
# Maps the four typo variants flagged in the Phase 0 audit to the
# canonical topic ids in data/topics.yml. New variants here must also
# be added to topics.yml as `id` or aliased here.
TOPIC_ALIAS = {
    "sprechen_dialog": "sprechen_dialog",
    "sprechen_monolog": "sprechen_monolog",
    "schreiben": "schreiben",
    "leseverstehen": "leseverstehen",
    "hoerverstehen": "hoerverstehen",
    "hör_hörsehverstehen": "hoerverstehen",
    "sprachmittlung": "sprachmittlung",
    "wortschatz": "wortschatz",
    "text_medien": "text_medien",
    "textmedienkompetenz": "text_medien",
    "interkulturelle_kompetenz": "interkulturelle_kompetenz",
}

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def fail(msg: str, *paths: Path) -> None:
    print(f"::error::{msg}", file=sys.stderr)
    for p in paths:
        print(f"  {p.relative_to(ROOT)}", file=sys.stderr)
    sys.exit(1)


def load_topics() -> dict[str, dict]:
    if not TOPICS_PATH.exists():
        fail(f"data/topics.yml is missing")
    with TOPICS_PATH.open(encoding="utf-8") as fh:
        topics = yaml.safe_load(fh) or []
    by_id: dict[str, dict] = {}
    for t in topics:
        tid = t.get("id")
        if not tid:
            fail(f"topic entry without `id`: {t!r}")
        if tid in by_id:
            fail(f"duplicate topic id: {tid}")
        by_id[tid] = t
    return by_id


def parse_frontmatter(md_path: Path) -> dict | None:
    txt = md_path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(txt)
    if not m:
        return None
    fm = yaml.safe_load(m.group(1)) or {}
    return fm


def first_paragraph(md_path: Path) -> str:
    """Return the first prose paragraph after the frontmatter.

    Skips Hugo shortcodes (`{{< ... >}}`), front matter, and headings.
    Used as a description fallback (Phase 5 prompt §1: graph cards
    need a description; we don't add a frontmatter field, we extract
    from body).
    """
    txt = md_path.read_text(encoding="utf-8")
    body = FRONTMATTER_RE.sub("", txt, count=1)
    paragraphs: list[str] = []
    buf: list[str] = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("{{<") or s.startswith("{{%"):
            continue
        if s.startswith("#"):
            if buf:
                paragraphs.append(" ".join(buf).strip())
                buf = []
            continue
        if not s:
            if buf:
                paragraphs.append(" ".join(buf).strip())
                buf = []
            continue
        buf.append(s)
    if buf:
        paragraphs.append(" ".join(buf).strip())
    for p in paragraphs:
        # skip any line of pure shortcode / list of bullets
        cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", p)
        cleaned = re.sub(r"\*([^*]+)\*", r"\1", cleaned)
        cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
        if len(cleaned) >= 40 and not cleaned.startswith("- "):
            return cleaned[:280]
    return ""


def derive_course(rel_path: Path) -> str:
    """`content/track_e_kl06/units/...md` → `track-e-kl06`."""
    parts = rel_path.parts
    for p in parts:
        if p.startswith("track_"):
            return p.replace("_", "-")
    return ""


def url_for(rel_path: Path, slug: str | None) -> str:
    """Hugo URL for a unit. Mirrors the production URL shape.

    `rel_path` is relative to ROOT (e.g. content/track_e_kl06/units/x.md).
    """
    parts = rel_path.parts  # ('content','track_e_kl06','units','x.md')
    # drop leading 'content' and the filename
    section = parts[1:-1]
    base = "/" + "/".join(section) + "/"
    return base + (slug or rel_path.stem) + "/"


def collect_articles(topics: dict[str, dict]) -> list[dict]:
    """Walk all unit .md files; return list of article dicts."""
    articles: list[dict] = []
    no_tag: list[Path] = []
    bad_topic: list[tuple[Path, str]] = []
    for md in sorted(CONTENT_ROOT.rglob("*.md")):
        rel = md.relative_to(ROOT)
        if "/units/" not in str(md.as_posix()):
            continue
        fm = parse_frontmatter(md)
        if not fm:
            continue
        # only material-bearing articles participate in the graph
        if not (fm.get("presentation") or fm.get("worksheet")):
            continue
        tags = list(fm.get("tags") or [])
        if not tags:
            no_tag.append(md)
        # resolve topic from skills_focus[0] (first entry wins; multi-skill
        # units appear under their primary competence). Typos are normalised
        # via TOPIC_ALIAS, but unknown skills_focus values still fail.
        skills = list(fm.get("skills_focus") or [])
        topic = None
        for s in skills:
            if s in TOPIC_ALIAS:
                topic = TOPIC_ALIAS[s]
                break
        # if skills_focus is set but none resolve, fail loudly
        for s in skills:
            if s not in TOPIC_ALIAS:
                bad_topic.append((md, s))
        articles.append({
            "path": rel,
            "fm": fm,
            "tags": tags,
            "topic": topic,
            "bildungsplan": list(fm.get("bildungsplan") or []),
            "url": url_for(rel, fm.get("slug")),
            "course": derive_course(rel),
        })
    if no_tag:
        fail("CI gate: every material-bearing article must have at least "
             "one tag. Articles missing `tags:` frontmatter:", *no_tag)
    if bad_topic:
        msg = ("CI gate: skills_focus entry not in topic alias map "
               "(data/topics.yml or _scripts/build_graph.py:TOPIC_ALIAS):")
        print(f"::error::{msg}", file=sys.stderr)
        for path, val in bad_topic:
            print(f"  {path.relative_to(ROOT)}: {val!r}", file=sys.stderr)
        sys.exit(1)
    return articles


def build_nodes(articles: list[dict], topics: dict[str, dict]) -> list[dict]:
    """For each article, emit article + presentation + worksheet nodes."""
    nodes: list[dict] = []
    for a in articles:
        fm = a["fm"]
        slug = fm.get("slug") or a["path"].stem
        article_id = f"article-{slug}"
        common = {
            "course": a["course"],
            "topic": a["topic"],
            "tags": a["tags"],
            "bildungsplan": a["bildungsplan"],
        }
        # description from first paragraph (no frontmatter field on units)
        desc = first_paragraph(ROOT / a["path"])
        nodes.append({
            "id": article_id,
            "type": "article",
            "title": fm.get("title", slug),
            "url": a["url"],
            "description": desc,
            "thumbnail": None,
            "related": [],  # filled in below
            **common,
        })
        if fm.get("presentation"):
            p = fm["presentation"]
            pres_id = f"pres-{slug}"
            nodes.append({
                "id": pres_id,
                "type": "presentation",
                "title": fm.get("title", slug),
                "url": p.get("file") if isinstance(p, dict) else "",
                "thumbnail": p.get("thumbnail") if isinstance(p, dict) else None,
                "parent_article": article_id,
                **common,
            })
        if fm.get("worksheet"):
            w = fm["worksheet"]
            ws_id = f"ws-{slug}"
            nodes.append({
                "id": ws_id,
                "type": "worksheet",
                "title": fm.get("title", slug),
                "url": w.get("file") if isinstance(w, dict) else "",
                "thumbnail": w.get("thumbnail") if isinstance(w, dict) else None,
                "parent_article": article_id,
                **common,
            })
    # link `related` on the article to its child material nodes
    by_parent: dict[str, list[str]] = defaultdict(list)
    for n in nodes:
        if n.get("parent_article"):
            by_parent[n["parent_article"]].append(n["id"])
    for n in nodes:
        if n["type"] == "article":
            n["related"] = by_parent.get(n["id"], [])
    return nodes


def build_edges(articles: list[dict], nodes: list[dict]) -> list[dict]:
    """Two edge kinds (see module docstring)."""
    edges: list[dict] = []
    # 1. same-article edges, weight=3
    by_id = {n["id"]: n for n in nodes}
    for n in nodes:
        if n.get("parent_article") and n["parent_article"] in by_id:
            edges.append({
                "source": n["parent_article"],
                "target": n["id"],
                "weight": 3,
                "kind": "same-article",
            })
    # 2. shared-tags edges, between articles only, weight = shared
    #    bildungsplan-anchor count, capped at 5. Threshold ≥2.
    by_slug = {a["path"].stem: a for a in articles}
    keys = list(by_slug.keys())
    for i, j in combinations(keys, 2):
        a, b = by_slug[i], by_slug[j]
        shared = set(a["bildungsplan"]) & set(b["bildungsplan"])
        if len(shared) < 2:
            continue
        edges.append({
            "source": f"article-{a['fm'].get('slug') or i}",
            "target": f"article-{b['fm'].get('slug') or j}",
            "weight": min(len(shared), 5),
            "kind": "shared-tags",
        })
    return edges


def build_facets(nodes: list[dict], topics: dict[str, dict]) -> dict:
    """Counts per facet, computed across every node in the graph."""
    type_count = Counter(n["type"] for n in nodes)
    course_count = Counter(n["course"] for n in nodes if n.get("course"))
    topic_count = Counter(n["topic"] for n in nodes if n.get("topic"))
    tag_count: Counter = Counter()
    for n in nodes:
        for t in n.get("tags") or []:
            tag_count[t] += 1
    return {
        "types": [{"id": k, "count": v} for k, v in sorted(type_count.items())],
        "courses": [
            {"id": k, "label": k.replace("track-", "").replace("-", " ").title(),
             "count": v}
            for k, v in sorted(course_count.items())
        ],
        "topics": [
            {
                "id": k,
                "label_fr": topics[k].get("label_fr", k),
                "label_en": topics[k].get("label_en", k),
                "label_de": topics[k].get("label_de", k),
                "color": topics[k].get("color", "#888888"),
                "count": v,
            }
            for k, v in sorted(topic_count.items())
            if k in topics
        ],
        "tags": [{"id": k, "count": v}
                 for k, v in sorted(tag_count.items(), key=lambda x: -x[1])],
        "date_range": {"min": None, "max": None},
    }


def enforce_post_gates(nodes: list[dict], edges: list[dict],
                        topics: dict[str, dict]) -> None:
    if len(edges) == 0:
        fail("CI gate: graph.json has zero edges — the topical layer is "
             "too sparse to form clusters. Check bildungsplan tagging.")
    used_topics = {n["topic"] for n in nodes if n.get("topic")}
    orphans = sorted(set(topics.keys()) - used_topics)
    if orphans:
        fail("CI gate: topic(s) declared in data/topics.yml but assigned "
             f"to zero materials: {', '.join(orphans)}")


def main() -> None:
    topics = load_topics()
    articles = collect_articles(topics)
    if not articles:
        fail("No material-bearing articles found under content/track_*/units/.")
    nodes = build_nodes(articles, topics)
    edges = build_edges(articles, nodes)
    enforce_post_gates(nodes, edges, topics)
    facets = build_facets(nodes, topics)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(
            {"nodes": nodes, "edges": edges, "facets": facets},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    n_articles = sum(1 for n in nodes if n["type"] == "article")
    n_pres = sum(1 for n in nodes if n["type"] == "presentation")
    n_ws = sum(1 for n in nodes if n["type"] == "worksheet")
    n_same = sum(1 for e in edges if e["kind"] == "same-article")
    n_shared = sum(1 for e in edges if e["kind"] == "shared-tags")
    n_total = len(nodes)
    max_edges = n_total * (n_total - 1) // 2
    density = (n_shared / max_edges) if max_edges else 0
    print(f"wrote {OUT_PATH.relative_to(ROOT)}:")
    print(f"  nodes:   {n_total}  ({n_articles} articles + "
          f"{n_pres} presentations + {n_ws} worksheets)")
    print(f"  edges:   {len(edges)}  ({n_same} same-article + "
          f"{n_shared} shared-tags)")
    print(f"  density: {density:.4f}  "
          f"(shared-tags edges / max possible)")
    print(f"  topics:  {len(facets['topics'])} active")
    print(f"  courses: {len(facets['courses'])}")
    print(f"  tags:    {len(facets['tags'])} distinct")


if __name__ == "__main__":
    main()
