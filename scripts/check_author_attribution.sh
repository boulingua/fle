#!/usr/bin/env bash
# Hard-fail if any rendered article page (= a unit page or a top-level
# editorial page) is missing the canonical author string.
#
# The Coder theme + our custom footer emit `<meta name=author content=
# "S. Le Boulanger">` (head) and a footer attribution block on every
# page when params.author is set. This gate is defense-in-depth: catch
# any future regression in the head/footer partials, and any content-only
# page Hugo renders without going through them.
set -eu

PUBLIC="${1:-public}"
SCAN=(
  "$PUBLIC"/track_*/units/*/index.html
  "$PUBLIC/index.html"
  "$PUBLIC/a_propos/index.html"
  "$PUBLIC/programme/index.html"
  "$PUBLIC/bildungsplan/index.html"
  "$PUBLIC/references/index.html"
  "$PUBLIC/bibliographie/index.html"
  "$PUBLIC/remerciements/index.html"
)

# We allow either form (Hugo's minifier may strip quotes).
REQUIRED='S\. Le Boulanger'

fail=0
checked=0
for f in "${SCAN[@]}"; do
  [[ -f "$f" ]] || continue
  checked=$((checked + 1))
  if ! grep -q "$REQUIRED" "$f"; then
    echo "::error::missing author attribution: $f"
    fail=$((fail + 1))
  fi
done

if [[ "$checked" -eq 0 ]]; then
  echo "::error::no rendered pages matched scan globs — public/ empty?"
  exit 1
fi
if [[ "$fail" -gt 0 ]]; then
  exit 1
fi
echo "Author attribution OK: $checked pages, all reference 'S. Le Boulanger'."
