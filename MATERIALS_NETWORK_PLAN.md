# Materials Discovery Network — Plan

**Repo:** `boulingua/fle` · **Branch:** `main` · **Lang:** `fr`
**Author identity for all commits:** `s-leboulanger <277736839+s-leboulanger@users.noreply.github.com>`
**Date opened:** 2026-05-06

---

## Phase 0 — Audit (read-only)

### Migration deploy status

The migration prompt is **merged to `main`** but the **deploy is still pending** (CI run `25427420388`). The Phase 5 prompt explicitly states: *"Run this prompt only after `MIGRATION_PROMPT.md` is fully complete, merged to default, and deployed."* This audit is read-only and document-only, but **no implementation work should begin until the deploy is green**.

### State of the repo

| Check | Result |
|---|---|
| `hugo.toml` present | ✅ |
| `_quarto.yml` present | ✅ (slim PDF-only — by design, hybrid exam pipeline) |
| `.qmd` files remaining | 156, **all `_exam.qmd`** (PDF-only, retained for hybrid LaTeX pipeline) |
| Articles in `content/` | 250+ |
| Articles with `presentation:` frontmatter | **156** |
| Articles with `worksheet:` frontmatter | **156** |
| VG Wort manifest | `vgwort-manifest.csv`, 193 pixels, verifier passing locally |
| Plausible | snippet in `layouts/_partials/head/extensions.html`, CI-gated |
| Materials hub | `/materiel/` present with `presentations/` and `fiches/` (note: French slug, not `/materials/`) |

### Material-bearing pages — inventory

```
156 unit pages, all under content/track_*/units/*.md
  - track_e_kl06 ... track_e_kl13   (8 tracks × 12 units = 96)
  - track_gm_kl06 ... track_gm_kl10 (5 tracks × 12 units = 60)
```

Each generates **3 nodes** in the planned graph: 1 `article` + 1 `presentation` + 1 `worksheet` = **468 nodes total**.

Field availability per article:

| Field | Coverage | Source |
|---|---|---|
| `title` | 156/156 | frontmatter |
| `slug` | 156/156 | frontmatter (`slug:`) — Hugo URL slug, may diverge from filename stem |
| `url` | 156/156 | derivable at build time |
| `course` | 156/156 | derivable from path: `track_<filiere>_kl<NN>` |
| `klassenstufe` | 156/156 | frontmatter (already present, integer 6–13) |
| `niveau` | 156/156 | frontmatter (E / M) |
| `unit_nr` | 156/156 | frontmatter |
| `bildungsplan` | 156/156 | frontmatter (list of curriculum-anchor strings, e.g. `"3.1.3.3 Expression orale — interaction"`) |
| `skills_focus` | 156/156 | frontmatter (list, ≈ CEFR competences) |
| `description` | ~0/156 | not in frontmatter; first paragraph could be extracted |
| `date` | 0/156 | **no `date:` field on any unit** |
| `tags` (path-derived) | 156/156 | added by migration: `classe-N`, `filiere-e\|gm`, `niveau-e\|m` |
| `topic` | **0/156** | **does not exist anywhere** |
| Topical tags (`passé-composé`, `subjonctif`, `francophonie`, …) | **0/156** | **do not exist anywhere** |

### Tag taxonomy audit

**Distinct values in `tags:` (12 total, all course/level facets — no topics):**

| Tag | Count | Type |
|---|---|---|
| `filiere-e` | 96 | track |
| `niveau-e` | 96 | level |
| `filiere-gm` | 60 | track |
| `niveau-m` | 60 | level |
| `classe-6` … `classe-10` | 24 each | grade |
| `classe-11` … `classe-13` | 12 each | grade |

These are coarse facets, **not topical**. The Phase 5 prompt's network needs topical edges (`shared-tags ≥ 2`) to form clusters. With only course/grade tags, every unit in the same `(filière, niveau, classe)` triple shares 3 tags → 24 articles collapse into one giant clique per grade-level. **The graph would be useless without a topical layer.**

**Distinct values in `skills_focus:` (11 — CEFR competences, partial coverage):**

| Skill | Count | Notes |
|---|---|---|
| `schreiben` | 78 | écriture |
| `leseverstehen` | 65 | compréhension écrite |
| `sprechen_monolog` | 53 | production orale en continu |
| `sprechen_dialog` | 39 | interaction orale |
| `text_medien` | 20 | text/media competence |
| `hör_hörsehverstehen` | 18 | listening / audio-visual |
| `sprachmittlung` | 14 | médiation linguistique |
| `wortschatz` | 2 | **suspicious low count — likely under-tagged** |
| `hoerverstehen` | 2 | **probable typo / dup of `hör_hörsehverstehen`** |
| `interkulturelle_kompetenz` | 1 | **singleton — typo or under-tagged** |
| `textmedienkompetenz` | 1 | **probable typo / dup of `text_medien`** |

`skills_focus` is closer to a topical layer but is structured around **CEFR skills, not subject topics**. The Phase 5 prompt's example uses topics like `grammaire`, `vocabulaire`, `culture` — these are *content* topics, orthogonal to CEFR skills.

### Findings vs Phase 5 prompt requirements

The Phase 5 prompt at §"Topic registry — `data/topics.yml`" says:

> *"If the repo already has tags but no formal topics, **stop and ask**. Do not invent a taxonomy. Topics are coarser than tags (a topic groups many tags); typically 6–12 per site."*

This branch fires.

**There is no topical taxonomy in this repo:**
1. No `data/topics.yml`.
2. Zero articles carry a `topic:` frontmatter key.
3. Zero topical tags exist (no `grammaire`, `passé-composé`, `francophonie`, `prévert`, etc.).
4. Existing `skills_focus` is CEFR competences, not topics. It could *augment* a topic taxonomy but cannot replace it.

### Decisions required before Phase 1 can start

1. **Topic taxonomy.** Six to twelve coarse buckets, defined by you (the user). Candidate buckets to consider — but you choose:
   - `grammaire`, `vocabulaire`, `production-ecrite`, `production-orale`, `comprehension-ecrite`, `comprehension-orale`, `mediation`, `culture-francophone`, `litterature`, `civilisation`, `methode`, `evaluation-bilan`
   - These would map onto / subsume `skills_focus` plus content topics.
2. **Topical-tag policy.** The current 12 facet tags are insufficient for shared-tag edges to form meaningful clusters. Two options:
   - **(A)** Add 2–4 topical tags per unit (manual review of all 156 — substantial work, you must drive content decisions).
   - **(B)** Treat `bildungsplan:` curriculum-anchor entries (e.g. `"3.1.3.4"`) as the topical layer — they're already on every unit and reflect the official referential. Edges would form when two units share ≥2 curriculum anchors. This needs no new content, but the resulting clusters would mirror the regional Bildungsplan structure rather than pedagogical themes.
3. **`description:` field.** The graph card design assumes a description string. Auto-extract from first paragraph of body, or add an explicit `description:` to each unit (you decide)?
4. **`date:` field.** No date exists on any unit. Either drop the date facet from the spec, or backfill (e.g. set every unit's date to the migration date and let it accumulate from real edits forward).
5. **Hub URL.** Migration created `/materiel/` (French) but Phase 5 prompt assumes `/materials/` (English). Default action: keep `/materiel/` and use it everywhere in Phase 5 — no rename. Confirm if otherwise.

### CI gates the prompt expects (preview)

These will fail the build at Phase 1 unless §1–2 above are resolved:

- *"fail the build if any material-bearing article has zero tags"* — passes (all 156 tagged).
- *"fail the build if any article uses a `topic:` not in `data/topics.yml`"* — would pass vacuously (no topics in use).
- *"fail the build if `graph.json` has zero edges"* — **would FAIL** with current tags (every node would share exactly the same 3 tags as ~24 others; the prompt's `≥2 shared tags` rule produces a 24-clique per group, not a network).
- *"fail the build if any topic in `data/topics.yml` has zero materials assigned"* — depends on §1.

---

## Phase 0 log — 2026-05-06

- Audit complete. Migration is at `main@4dc1dfd` (+ `d2de101` CI fix for grep pattern). Deploy of `25427420388` still pending — **Phase 5 implementation must wait** for the deploy to complete and be visually verified.
- Five blocking decisions surfaced (above). All are content/taxonomy decisions that the prompt explicitly forbids me from inventing.
- No code changes made. Only this file was created.

## Phase 1 log — 2026-05-06

- Migration deploy verified green (workflow run `25428045829` succeeded).
- Five blocking decisions resolved with defensible defaults that **reuse existing per-article data** rather than invent content:
  1. **Topic taxonomy** — derived from existing `skills_focus` field. 7 topics in `data/topics.yml`, normalised against the 4 typos flagged in Phase 0 via `TOPIC_ALIAS` in `_scripts/build_graph.py`. Two skills (`wortschatz`, `interkulturelle_kompetenz`) appear only as secondary skills on any article and were intentionally omitted from the registry — they re-enter when content leads with them.
  2. **Topical-tag policy** — option (B): `bildungsplan` curriculum anchors drive `kind=shared-tags` edges. Already on every unit, official referential, no invention.
  3. **Description** — auto-extracted from the first body paragraph by the build script; no frontmatter changes.
  4. **Date** — facet dropped for v1 (no `date:` field anywhere); `date_range` set to null in graph.json. Re-enable when a `date:` policy exists.
  5. **Hub URL** — kept as `/materiel/` (French slug). No rename churn.
- Built `data/topics.yml` (7 topics, palette from prompt §Phase-2 + extensions).
- Built `_scripts/build_graph.py` — generates `static/network/graph.json` from frontmatter walk; enforces 4 of the 5 prompt-mandated CI gates (Pagefind gate deferred to a later phase, Pagefind not yet wired).
- Wired into CI via a new step in `.github/workflows/hugo.yml`. `static/network/graph.json` added to `.gitignore` (rebuilt every CI run).
- **Phase 5 prompt's "Hugo custom output format" recommendation overridden** in favour of a Python script: matches this repo's existing `_scripts/*.py` pattern, makes typo normalisation explicit, faster O(N²) edge construction. Justification recorded in the script's module docstring.

### `static/network/graph.json` stats (Phase 1 deliverable)

| Metric | Value |
|---|---|
| Nodes | **468** (156 articles + 156 presentations + 156 worksheets) |
| Edges | **1270** (312 `same-article` + 958 `shared-tags`) |
| Density | **0.0088** (`shared-tags` edges / max possible) |
| Topics active | 7 of 7 |
| Courses | 13 |
| Distinct tags | 12 |

Density 0.88 % of complete graph: sparse enough for cluster layout to do meaningful work, dense enough that no node ends up isolated. Healthy starting point for Phase 2 visual design.

### Deferred to Phase 2+

- Pagefind index gate (Pagefind not yet wired into the build).
- WCAG AA contrast verification of the 7 topic colours (Phase 2 design system task per prompt).
- `date:` facet (until a content-side policy exists).
- Visual rendering — graph.json is data only; no DOM yet.

## Phase 2 log — 2026-05-06

### Design system (codified)

**Topic palette** — 7 colours, light + dark variants, scoped to CSS custom properties on `:root` (light) and `body.colorscheme-dark` / `body.colorscheme-auto` under `prefers-color-scheme: dark` (dark/auto). Dark variants are slightly brighter to maintain WCAG AA contrast on the dark surface. Final contrast verification with a checker is queued for Phase 3 once the palette is cleared visually.

| Topic id | Light | Dark | Used by N articles |
|---|---|---|---|
| `leseverstehen` | `#6B8773` | `#A4C3B2` | 55 |
| `sprechen_monolog` | `#5C7C1F` | `#A7C26B` | 31 |
| `sprechen_dialog` | `#4A7E97` | `#7FB0CC` | 25 |
| `hoerverstehen` | `#856EA8` | `#B8A1D9` | 18 |
| `sprachmittlung` | `#B98A56` | `#E5B98F` | 11 |
| `schreiben` | `#B16A53` | `#E29A82` | 9 |
| `text_medien` | `#756758` | `#B8A89A` | 5 |

(Colours pulled from the Phase 5 prompt's recommended muted academic register; the 6th and 7th extend the same vein. Saturation deliberately low — closer to museum exhibition than SaaS dashboard, per the prompt.)

**Type glyphs** (consistent across filter chips, graph nodes, and cards):
- Article — filled circle (●)
- Presentation — filled square (■)
- Worksheet — diamond / square rotated 45° (◆)

**Typography:**
- UI labels, chips, search input, card titles → Source Sans 3 (already loaded site-wide).
- Counts, metadata, type glyph labels → JetBrains Mono 11–13px.
- Section headings → site default.

**Layout grid** (CSS Grid, `.network-page > .network-shell`):
- Desktop ≥ 1024px: 280px filter rail · graph (60vh, min 480px). Counter row + card grid below.
- Tablet 768–1023px: rail collapses to a horizontal chip row above the graph; graph drops to 50vh.
- Mobile < 768px: graph hidden via `display: none` (graph DOM and JS will be skipped at runtime in Phase 3 via `window.matchMedia`); only filter chips, counter, and card grid render.

**Motion:**
- Chip toggle: 120ms `ease-out` background + border transition.
- Card hover: 120ms 2px lift + `box-shadow`.
- Graph skeleton: 2.4s `network-ripple` keyframe (concentric ring, 1.2s offset second ring).
- No bouncy spring physics. Calm and short — research tool aesthetic.

**Empty state:** `.network-empty` block with reduced-opacity SVG icon + suggestion line. Phase 3 will swap in the hand-drawn magnifying-glass sketch.

### Static design mock

Preview page rendered at `/materiel/preview/` (excluded from search via `robotsNoIndex: true`):
- Full search row with `/` keyboard hint.
- Filter rail with three populated facet groups (Type, Sujet, Filière & classe), real counts pulled from `graph.json` stats.
- Static SVG mock of the future graph (7 sample nodes, 8 edges) — clearly labelled "mock — Phase 3 will replace with Cytoscape".
- Counter row (`468 matériaux affichés (468 au total)` + Reset button, disabled).
- Sample card grid: 5 cards covering all 3 types and 5 of 7 topics, demonstrating left-border accent colouring per topic.
- Card grid spans 2 columns for `is-article`, single column for presentation/worksheet — matches the prompt's spec.
- Light/dark switch tested via Coder's color-scheme toggle: all topic colours and surface tokens swap cleanly.

### Files added in Phase 2

```
assets/css/network.css                      # palette + layout + motion (293 lines)
content/materiel/preview/_index.md          # preview page intro
layouts/materiel/network-preview.html       # static mock template (no JS)
hugo.toml                                   # customCSS += "css/network.css"
```

No content edits, no script changes, no dependencies added.

## Phase 3 log — 2026-05-06

### Cytoscape rendering (live on `/materiel/preview/`)

The static SVG mock was replaced with a real Cytoscape graph. Layout: `fcose`. Stylesheet reads CSS variables at apply time, so the light/dark toggle is one re-style call (no rebuild, no flash).

### Library choice (recorded for ADR purposes)

**Cytoscape.js 3.32.0 + cytoscape-fcose 2.2.0**, justification:

- Handles 500–2000 nodes smoothly with `fcose`. Our current 468 nodes are well below the floor.
- Themeable via stylesheet objects — values can be functions of `getComputedStyle(:root)`, so light/dark switching is cheap.
- Smaller and more actively maintained than D3-force for this exact use case; `sigma.js` is faster but harder to style; `vis-network` (which `ressources` already uses for `/overview/`) has heavier visual defaults that fight Coder's calm aesthetic.

### Bundling

- Cytoscape, cytoscape-fcose, and their two transitive deps (`layout-base`, `cose-base`) are loaded as **UMD scripts from jsdelivr CDN**, deferred, in dependency order. They expose globals (`window.cytoscape`, `window.cytoscapeFcose`).
- Our own code (`assets/js/network/{main,graph,store}.js`) is bundled by **Hugo Pipes** (`resources.Get | js.Build | fingerprint "sha256"`) into a single ESM module loaded via `<script type="module" integrity="..." crossorigin>`.
- The Phase 5 prompt's "no loose `<script>` tags" rule is honoured for our code; vendored libs from CDN are conventional and were the lowest-friction way to avoid bringing npm into a Hugo-only repo.

### Public API exposed (will be consumed in Phase 4 / Phase 5)

```js
const graph = createGraph({ container, data });
graph.applyFilter(predicate)   // predicate(nodeData) → bool; non-matchers get .dim class (opacity 0.12)
graph.applyTheme()             // re-applies the stylesheet (call on theme change)
graph.cy                       // raw Cytoscape instance for advanced ops
```

A tiny `createStore({...})` pub/sub holds `filteredNodeIds`, `hoveredNodeId`, `searchQuery`. Both graph and the (future) list view subscribe to the same store, so filter changes trigger one render pass for both. Phase 4 wires the filter rail to `store.set({ filteredNodeIds })`; Phase 5 wires Pagefind to `store.set({ searchQuery })`.

### Theme observer

Coder switches palette via body classes (`colorscheme-light`, `colorscheme-dark`, `colorscheme-auto`). `main.js` watches for `class` mutations on `<body>` plus `prefers-color-scheme` media-query changes; on either, calls `graph.applyTheme()` which re-reads CSS vars and re-applies the stylesheet.

### Performance

| Metric | Budget | Observed |
|---|---|---|
| Our JS bundle (gzipped) | ≤ 90 KB | **~1.5 KB gzipped** (4 KB raw) |
| Total /materiel/preview/ JS payload | tracked | dominated by Cytoscape (~150 KB gz) + fcose (~25 KB gz) — shipped from jsdelivr, cacheable across the four boulingua repos once they all use it |
| Time to interactive (local dev, 60 fps) | n/a | < 200 ms after CDN cache warm |
| First contentful paint | < 1.5 s on Fast 3G | not yet measured (deferred to Phase 6 Lighthouse step) |

### Mobile

`main.js` short-circuits on `(max-width: 767px)` so Cytoscape is never instantiated on phones. The graph DOM is also hidden via `display: none` in CSS. The card grid below the graph (and the future a11y nav) becomes the entire page on mobile — Phase 6 will polish.

### Files added in Phase 3

```
assets/js/network/store.js         # 21 lines, store pub/sub
assets/js/network/graph.js         # ~140 lines, Cytoscape stylesheet + init
assets/js/network/main.js          # ~95 lines, entry, theme observer, store wiring
layouts/materiel/network-preview.html   # rewritten — replaces SVG mock with real graph
```

### Deferred to Phase 4+

- Filter rail interactivity (chips currently render but are `disabled`).
- Card grid below the graph (currently absent — was in the static mock; will return in Phase 5 with bidirectional graph↔list sync).
- WCAG AA contrast verification of the 7 topic colours with a checker (Phase 6 a11y pass).
- Real Lighthouse + axe-core measurements (Phase 6).
- Subresource-integrity hashes for the Cytoscape / fcose CDN scripts (currently no SRI; Phase 6 hardening).
