# Rechtliches — Pflege- und Build-Hinweise

Dieses Repository veröffentlicht eine DSGVO-konforme Konfiguration:

- `impressum.qmd` — Anbieter nach § 5 DDG, § 18 Abs. 2 MStV
- `datenschutz.qmd` — Datenschutzerklärung mit allen Drittanbietern
  (Plausible self-hosted, VG Wort, GitHub Pages, Google Fonts)
- `haftungsausschluss.qmd` — Haftung Inhalte, Haftung Links,
  Urheberrecht

Im Header oben rechts erscheinen alle drei unter dem Eintrag
**Rechtliches**, im Footer als eigene Linkgruppe inkl. Kontakt.

## Plausible Analytics

Eingebunden über `_quarto.yml` → `format.html.include-in-header`.
Die Instanz ist selbst gehostet auf `analytics.hellebo.de`
(Server in Deutschland).

## VG Wort Standard-Zählpixel

Per Pandoc-Lua-Filter `_scripts/vgwort.lua` (in `_quarto.yml`
unter `filters:` aktiviert). Pro zählpflichtige Seite in der
YAML-Frontmatter ergänzen:

```yaml
---
title: "Mon unité"
vgwort_pixel: "vg08.met.vgwort.de/na/<32-hex-token>"
---
```

### Workflow

1. Token aus [VG Wort T.O.M.](https://tom.vgwort.de/) ziehen —
   eine Marke pro Werk, nicht wiederverwenden.
2. Mindestens **1.500 Zeichen** Text (METIS-Standardverfahren).
3. Token in die Frontmatter eintragen, neu rendern.
4. Übersichten, Listings, Rechtliches-Seiten und Werke unter
   1.500 Zeichen bleiben pixelfrei.

## CI-Guard

`scripts/check-legal-placeholders.sh` prüft das gerenderte
`docs/`-Verzeichnis auf unausgefüllte Platzhalter und TODO/FIXME
in den Rechtliches-Seiten. Lokal:

```bash
bash scripts/check-legal-placeholders.sh
```
