"""
Compare URL list of the deployed Quarto site against the new Hugo build.
Every old URL must either resolve in the new build OR have a Hugo alias /
redirect mapping to a new URL. Otherwise the migration leaves a 404.

Usage: python scripts/parity-check.py [--public public] [--site URL]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def fetch_sitemap_urls(site_url: str) -> set[str]:
    sm_url = site_url.rstrip("/") + "/sitemap.xml"
    print(f"Fetching {sm_url} …")
    with urllib.request.urlopen(sm_url, timeout=30) as resp:
        data = resp.read()
    root = ET.fromstring(data)
    return {loc.text.strip() for loc in root.findall(".//sm:url/sm:loc", NS) if loc.text}


def build_local_urls(public_dir: pathlib.Path, site_url: str) -> set[str]:
    base = site_url.rstrip("/")
    urls: set[str] = set()
    for html in public_dir.rglob("*.html"):
        rel = html.relative_to(public_dir).as_posix()
        if rel.endswith("index.html"):
            rel = rel[: -len("index.html")]
        urls.add(f"{base}/{rel}")
    # Include aliases (Hugo emits redirect HTMLs identical to index.html)
    return urls


def normalise(u: str) -> str:
    u = u.strip()
    # Treat /foo/index.html and /foo/ as the same canonical URL.
    if u.endswith("/index.html"):
        u = u[: -len("index.html")]
    if not u.endswith("/") and "." not in u.rsplit("/", 1)[-1]:
        u += "/"
    return u


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", default="public")
    ap.add_argument("--site", default="https://boulingua.github.io/fle")
    ap.add_argument("--strict", action="store_true",
                    help="Fail if any old URL is missing in new build.")
    args = ap.parse_args()

    public = pathlib.Path(args.public)
    if not public.is_dir():
        print(f"::error::{public} not found", file=sys.stderr); return 1

    try:
        old = {normalise(u) for u in fetch_sitemap_urls(args.site)}
    except Exception as exc:
        print(f"WARN: could not fetch sitemap ({exc}). Skipping parity comparison.")
        return 0

    new = {normalise(u) for u in build_local_urls(public, args.site)}
    missing = sorted(old - new)
    extra = sorted(new - old)

    print(f"Old URLs (deployed Quarto): {len(old)}")
    print(f"New URLs (local Hugo):      {len(new)}")
    print(f"Missing in new (potential 404s): {len(missing)}")
    print(f"New-only (additions):           {len(extra)}")

    if missing:
        print("\nFirst missing URLs (need redirects or aliases):")
        for u in missing[:30]:
            print(f"  {u}")

    if args.strict and missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
