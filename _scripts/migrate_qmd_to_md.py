"""
Quarto -> Hugo migrator for boulingua/fle.

Reads a list of source .qmd paths, writes .md equivalents under content/,
extracts VG Wort tokens to frontmatter, converts callouts and pandoc
bracketed spans, rewrites .qmd -> .md links, and emits per-file word-count
diffs into a JSON report.

Pure rewrite — does NOT touch original .qmd files. Safe to re-run.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import sys
from typing import Optional

REPO = pathlib.Path(__file__).resolve().parent.parent
CONTENT = REPO / "content"

VGWORT_BLOCK_RE = re.compile(
    r"^:::\s*\{\.vgwort-pixel\}\s*\n.*?^:::\s*$\n?",
    re.MULTILINE | re.DOTALL,
)
VGWORT_IMG_RE = re.compile(
    r'<img\s+src="(https://vg\d+\.met\.vgwort\.de/na/[a-f0-9]{32})"',
    re.IGNORECASE,
)

# Pandoc bracketed span: [text]{.class .other-class}
SPAN_RE = re.compile(r"\[([^\]]+)\]\{((?:\s*\.[A-Za-z0-9_-]+)+)\}")

# Custom-class fenced div: ::: {.classname}
DIV_OPEN_RE = re.compile(r"^:::\s*\{\.([A-Za-z0-9_-]+(?:\s+\.[A-Za-z0-9_-]+)*)\}\s*$")
DIV_CLOSE_RE = re.compile(r"^:::\s*$")

# Callout: ::: {.callout-note}, optionally with attributes
CALLOUT_OPEN_RE = re.compile(
    r"^:::\s*\{\.callout-(note|tip|warning|important|caution)"
    r"(?:\s+([^}]*))?\}\s*$"
)

# Quarto link target: ](something.qmd) or ](path/to/file.qmd) or with #anchor.
# We rewrite to absolute Hugo URLs without extension, e.g. /a_propos/ or
# /annexes/strategies/ — matching Hugo's clean-URL routing and the menu config.
QMD_LINK_RE = re.compile(r"\]\((?!https?://|/)([^)\s#]+?)\.qmd(#[^)]*)?\)")

YAML_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_yaml_frontmatter(text: str) -> tuple[Optional[str], str]:
    m = YAML_FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def extract_vgwort_token(body: str) -> tuple[str, Optional[str]]:
    """Return (body_without_vgwort_block, token_url_or_None)."""
    token: Optional[str] = None

    def _capture(match: re.Match) -> str:
        nonlocal token
        block = match.group(0)
        m = VGWORT_IMG_RE.search(block)
        if m:
            token = m.group(1)
        return ""  # remove block

    new_body = VGWORT_BLOCK_RE.sub(_capture, body)
    return new_body, token


def convert_spans(body: str) -> str:
    def _sub(m: re.Match) -> str:
        text = m.group(1)
        classes = " ".join(c.lstrip(".") for c in m.group(2).split())
        return f'<span class="{classes}">{text}</span>'

    return SPAN_RE.sub(_sub, body)


def convert_callouts_and_divs(body: str) -> str:
    """Convert ::: blocks to either {{< callout >}} shortcodes or raw <div>."""
    out_lines: list[str] = []
    stack: list[str] = []  # stack of close-tags to emit at matching :::
    for line in body.splitlines():
        co = CALLOUT_OPEN_RE.match(line.strip())
        if co:
            ctype = co.group(1)
            attrs = co.group(2) or ""
            title_match = re.search(r'title="([^"]+)"', attrs)
            shortcode = f'{{{{< callout type="{ctype}"'
            if title_match:
                shortcode += f' title="{title_match.group(1)}"'
            shortcode += " >}}"
            out_lines.append(shortcode)
            stack.append("{{< /callout >}}")
            continue
        do = DIV_OPEN_RE.match(line.strip())
        if do:
            classes = " ".join(c.lstrip(".") for c in do.group(1).split())
            out_lines.append(f'<div class="{classes}">')
            stack.append("</div>")
            continue
        dc = DIV_CLOSE_RE.match(line.strip())
        if dc and stack:
            out_lines.append(stack.pop())
            continue
        out_lines.append(line)
    # any unmatched opens
    while stack:
        out_lines.append(stack.pop())
    return "\n".join(out_lines)


def convert_qmd_links(body: str, src_qmd: pathlib.Path) -> str:
    """Rewrite [Text](page.qmd) -> [Text](/clean/url/) absolute Hugo paths,
    resolving relative-to-source. `index.qmd` -> section root URL."""
    src_dir = src_qmd.parent.relative_to(REPO)

    def _sub(m: re.Match) -> str:
        target = m.group(1)
        anchor = m.group(2) or ""
        # Resolve relative to source file's directory
        if target.startswith("../") or target.startswith("./") or "/" not in target:
            full = (src_dir / target).resolve().relative_to(REPO.resolve())
        else:
            full = pathlib.Path(target)
        parts = list(full.parts)
        if parts and parts[-1] == "index":
            parts = parts[:-1]
        url = "/" + "/".join(parts)
        if not url.endswith("/"):
            url += "/"
        return f"]({url}{anchor})"

    return QMD_LINK_RE.sub(_sub, body)


def word_count(text: str) -> int:
    # strip frontmatter, shortcodes, html tags, fenced code
    text = YAML_FRONTMATTER_RE.sub("", text)
    text = re.sub(r"\{\{<.*?>\}\}", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r":::\s*[^\n]*", "", text)
    return len(re.findall(r"\b[\wÀ-ÿ'’-]+\b", text))


def hugo_target(qmd_path: pathlib.Path) -> pathlib.Path:
    rel = qmd_path.relative_to(REPO)
    parts = list(rel.parts)
    name = parts[-1]
    if name == "index.qmd":
        parts[-1] = "_index.md"
    else:
        parts[-1] = name[:-4] + ".md"
    return CONTENT.joinpath(*parts)


def migrate_one(qmd_path: pathlib.Path) -> dict:
    src = qmd_path.read_text(encoding="utf-8")
    fm_yaml, body = parse_yaml_frontmatter(src)

    body, token_url = extract_vgwort_token(body)
    body = convert_callouts_and_divs(body)
    body = convert_spans(body)
    body = convert_qmd_links(body, qmd_path)
    body = body.lstrip("\n")

    # Build new frontmatter as YAML lines, preserving original keys verbatim.
    fm_lines: list[str] = []
    drop_keys = {"page-layout", "format", "editor", "filters", "lang"}
    skipping_block = False
    if fm_yaml:
        for raw in fm_yaml.splitlines():
            indent = len(raw) - len(raw.lstrip(" "))
            stripped = raw.strip()
            top_key = re.match(r"^([A-Za-z][\w-]*):", raw) if indent == 0 else None
            if skipping_block:
                if indent == 0 and top_key:
                    skipping_block = False
                else:
                    continue  # still inside dropped block
            if top_key and top_key.group(1) in drop_keys:
                # Inline form (`format: html`) — single-line drop.
                # Block form — also drop following indented lines.
                skipping_block = True
                continue
            fm_lines.append(raw)
    if token_url:
        fm_lines.append(f'vgwort_pixel: "{token_url}"')

    new_text = "---\n" + "\n".join(fm_lines).rstrip() + "\n---\n\n" + body
    if not new_text.endswith("\n"):
        new_text += "\n"

    target = hugo_target(qmd_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(new_text, encoding="utf-8")

    src_wc = word_count(src)
    dst_wc = word_count(new_text)
    diff_pct = 0.0 if src_wc == 0 else abs(dst_wc - src_wc) / src_wc * 100

    return {
        "qmd": str(qmd_path.relative_to(REPO)).replace("\\", "/"),
        "md": str(target.relative_to(REPO)).replace("\\", "/"),
        "vgwort_url": token_url,
        "src_wc": src_wc,
        "dst_wc": dst_wc,
        "diff_pct": round(diff_pct, 2),
        "review": diff_pct > 2.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="qmd paths (relative to repo); empty = all non-_exam")
    ap.add_argument("--report", default="_scripts/migration-report.json")
    ap.add_argument("--manifest", default="vgwort-manifest.csv")
    args = ap.parse_args()

    if args.paths:
        qmds = [REPO / p for p in args.paths]
    else:
        qmds = [
            p for p in REPO.rglob("*.qmd")
            if not p.name.endswith("_exam.qmd")
            and ".git" not in p.parts
            and "docs" not in p.parts
        ]

    qmds.sort()
    results = [migrate_one(p) for p in qmds]

    report_path = REPO / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest_path = REPO / args.manifest
    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["qmd_path", "md_path", "vgwort_url"])
        for r in results:
            if r["vgwort_url"]:
                w.writerow([r["qmd"], r["md"], r["vgwort_url"]])

    flagged = [r for r in results if r["review"]]
    print(f"Migrated {len(results)} files")
    print(f"VG Wort pixels captured: {sum(1 for r in results if r['vgwort_url'])}")
    print(f"Files flagged for manual review (>2% wc drift): {len(flagged)}")
    for r in flagged[:25]:
        print(f"  {r['qmd']}: src={r['src_wc']}, dst={r['dst_wc']} ({r['diff_pct']}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
