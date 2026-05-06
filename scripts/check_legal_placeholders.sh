#!/usr/bin/env bash
# Hard-fail if any legal page (Impressum / Datenschutz / Haftungsausschluss)
# in the rendered site contains a placeholder string the migration would
# have left behind. Restores the qmd-era 'Impressum / Datenschutz TODO gate'
# from the deleted publish.yml (commit 49ce54c).
set -eu

PUBLIC="${1:-public}"
PAGES=(
  "$PUBLIC/impressum/index.html"
  "$PUBLIC/datenschutz/index.html"
  "$PUBLIC/haftungsausschluss/index.html"
)

# Patterns that must never appear in legal copy. Includes:
#   - the qmd-era <TODO> marker (prior workflow)
#   - common scaffold residue ([NAME], [ADDRESS], [STUB])
#   - generic TODO / XXX / Lorem ipsum
PATTERNS=(
  '<TODO'
  '\[NAME\]'
  '\[ADDRESS\]'
  '\[STUB\]'
  '\[TODO\]'
  '\bTODO\b'
  '\bXXX\b'
  'Lorem ipsum'
)

fail=0
for page in "${PAGES[@]}"; do
  if [[ ! -f "$page" ]]; then
    echo "::error::missing rendered legal page: $page"
    fail=$((fail + 1))
    continue
  fi
  for pat in "${PATTERNS[@]}"; do
    if grep -qE "$pat" "$page"; then
      echo "::error::placeholder match in $page: $pat"
      grep -nE "$pat" "$page" | head -3
      fail=$((fail + 1))
    fi
  done
done

if [[ "$fail" -eq 0 ]]; then
  echo "Legal pages clean: ${#PAGES[@]} files, ${#PATTERNS[@]} patterns checked."
fi
exit $fail
