#!/usr/bin/env bash
# organise_downloads.sh — déplace les PDFs d'épreuve produits par
# `quarto render` depuis les dossiers `units/` des cours vers le
# chemin canonique `docs/downloads/<track>/kl<NN>/unit<NN>_<slug>_exam.pdf`.

set -euo pipefail

ROOT="${1:-docs}"

if [ ! -d "$ROOT" ]; then
  echo "organise_downloads: $ROOT does not exist — nothing to do."
  exit 0
fi

moved=0

while IFS= read -r src; do
  filename="$(basename "$src")"
  parent="$(dirname "$src")"           # .../track_gm_kl08/units
  grandparent="$(dirname "$parent")"   # .../track_gm_kl08
  trackdir="$(basename "$grandparent")"  # track_gm_kl08

  # Extract track + klassenstufe: track_gm_kl08 → track=gm, kl=08
  track="${trackdir#track_}"
  track="${track%%_*}"               # gm or e
  kl="${trackdir##*_kl}"             # 08

  dest_dir="$ROOT/downloads/$track/kl$kl"
  mkdir -p "$dest_dir"
  dest="$dest_dir/$filename"

  mv "$src" "$dest"
  echo "  moved  $src -> $dest"
  moved=$((moved + 1))
done < <(find "$ROOT" -type f -name "unit*_exam.pdf" -not -path "$ROOT/downloads/*" 2>/dev/null)

echo "organise_downloads: $moved exam PDF(s) moved."
