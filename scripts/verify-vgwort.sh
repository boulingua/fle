#!/usr/bin/env bash
# Verify every VG Wort pixel from vgwort-manifest.csv appears in exactly one
# rendered HTML file under public/. Fails if any token is missing or duplicated.
# (We intentionally do not assume a deterministic URL slug because some pages
# carry a `slug:` override in frontmatter that diverges from the filename.)
set -euo pipefail

MANIFEST="${1:-vgwort-manifest.csv}"
PUBLIC="${2:-public}"

if [[ ! -f "$MANIFEST" ]]; then echo "::error::$MANIFEST not found"; exit 1; fi
if [[ ! -d "$PUBLIC" ]]; then echo "::error::$PUBLIC dir not found"; exit 1; fi

fail=0
total=0
while IFS=',' read -r qmd_path md_path url; do
  url="${url%$'\r'}"  # strip CRLF tail on Windows-authored manifests
  [[ "$qmd_path" == "qmd_path" ]] && continue
  [[ -z "${url:-}" ]] && continue
  total=$((total+1))
  count=$(grep -rl --include="*.html" -- "$url" "$PUBLIC" 2>/dev/null | wc -l)
  if [[ "$count" -ne 1 ]]; then
    echo "::error::pixel for $md_path appears in $count pages (want 1): $url"
    fail=$((fail+1))
  fi
done < "$MANIFEST"

echo "Verified $total VG Wort pixels; $fail failures."
[[ "$fail" -eq 0 ]]
