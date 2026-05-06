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
