# Fonts shipped by this repository

Seven self-hosted faces, Google Fonts cuts rather than
`kit/design/build_fonts.py` output, because this course uses weights the kit's
tiers do not carry.

Self-hosting rather than linking `fonts.googleapis.com` is deliberate: a
webfont request from a learner's browser to a third party is a data transfer
the Datenschutzerklärung would have to declare.

Not covered by `kit/design/fonts/ATTRIBUTION.md`, which documents the kit's own
subsets. Gate A4 reads both.

| File | Family | Licence | Upstream |
|---|---|---|---|
| `jetbrains-mono-v24-latin_latin-ext-500.woff2` | JetBrains Mono | OFL 1.1 | <https://github.com/JetBrains/JetBrainsMono> |
| `jetbrains-mono-v24-latin_latin-ext-regular.woff2` | JetBrains Mono | OFL 1.1 | <https://github.com/JetBrains/JetBrainsMono> |
| `source-sans-3-v19-latin_latin-ext-300.woff2` | Source Sans 3 | OFL 1.1 | <https://github.com/adobe-fonts/source-sans> |
| `source-sans-3-v19-latin_latin-ext-500.woff2` | Source Sans 3 | OFL 1.1 | <https://github.com/adobe-fonts/source-sans> |
| `source-sans-3-v19-latin_latin-ext-600.woff2` | Source Sans 3 | OFL 1.1 | <https://github.com/adobe-fonts/source-sans> |
| `source-sans-3-v19-latin_latin-ext-700.woff2` | Source Sans 3 | OFL 1.1 | <https://github.com/adobe-fonts/source-sans> |
| `source-sans-3-v19-latin_latin-ext-regular.woff2` | Source Sans 3 | OFL 1.1 | <https://github.com/adobe-fonts/source-sans> |

Licence texts: [`kit/design/fonts/LICENSES/`](https://github.com/boulingua/kit/tree/main/design/fonts/LICENSES).
Both families are the same OFL projects the kit documents; only the cut differs.

The `latin-ext` subset is required: French needs é è ê à ç ù û ô î and the
œ ligature, and the course teaches names well outside basic Latin.
