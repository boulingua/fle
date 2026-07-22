# FLE — Handover: conformance audit & roadmap

**Repo:** `boulingua/fle` (Français Langue Étrangère, Bildungsplan-BW, Kl. 6–13)
**Audited against:** `pagegen` (structural/benchmark template) + `curriculum` (CEFR descriptor-ID + conformance standard)
**Audit date:** 2026-07-22 · **Auditor scope:** config, content model, layouts, shortcodes, scripts/CI, materials, VG Wort, legal, curriculum conformance

---

## 1. Executive summary

FLE is a **Hugo/hugo-coder site mid-migration off Quarto**. The Hugo shell is real and builds: `hugo.toml` pins the theme, 156 unit pages render, materials are committed, legal pages are filled, and a working VG Wort resolver is in place. But it is **structurally behind `pagegen` on the two load-bearing dimensions** and has **not begun** curriculum-ID conformance.

**The 5 biggest gaps, in priority order:**

1. **156 exams publish ZERO pages.** Every exam is a stranded Quarto `track_*/units/*_exam.qmd` at the repo root, rendered to PDF non-blocking in CI, never migrated into `content/`. EFL publishes 181 exam pages; FLE publishes 0. This is the single largest content and VG Wort gap. (L)
2. **Content is single files, not page bundles.** Units are `content/track_*/units/unitNN_slug.md`; `pagegen` mandates leaf bundles `content/<course>/units/<unitNN-slug>/index.md` with a sibling `…-exam/` bundle. Slug convention (`_` vs `-`), a forbidden front-matter `slug:`, and `.html` aliases are all Quarto carryover. (L)
3. **Front-matter schema is the pre-standard fork.** Flat `niveau`/`klassenstufe`/`track`/`bildungsplan` + a non-standard `skills_focus` enum, no `page_type` discriminator, no polymorphic `curriculum:` block. (M)
4. **Zero curriculum-ID conformance.** No `{LEVEL}.{DOMAIN}.{SCALE}.{SEQ}` references anywhere, no `conformance.yml`, no machine-readable scope/coverage manifest. FLE cannot currently declare any conformance level. (L)
5. **Raw HTML in content instead of shortcodes.** 14 content files embed `<div class="card-grid">` / `<div class="hero-kicker">`; `pagegen` provides `card-grid`/`card`/`hero`/`kicker`/`lead`/`details` shortcodes and forbids raw HTML section markup. FLE ships only `callout` + `downloads`. (M)

**What is already conformant:** the VG Wort resolver (`_partials/vgwort/url.html`, near-identical to `pagegen`), `head`/`body` extension wiring, committed materials (156 decks + 156 worksheets + audio), filled legal pages, `data/accents.yaml` already carries `code: fle` (`#4B8D19`/`#ACE77E`).

**Effort estimate:** ~**3–4 focused weeks**. Config alignment is days; the exam migration + bundle conversion + front-matter rewrite is the bulk (scriptable but touches 300+ files); curriculum-ID mapping is a genuine authoring task (1170 descriptors to map against). Phase 1 quick wins land in ~2 days.

---

## 2. Audit — template (`pagegen`) conformance

| Dimension | CURRENT (fle) | TARGET (pagegen) | GAP |
|---|---|---|---|
| **Config** | `hugo.toml` sets baseURL/title/fr; `navbarTitle`, `params.info`, `params.repoURL`; no `[taxonomies]`; no `params.code`; no `params.license`; no `enableRobotsTXT`; Plausible hardcoded in `head/extensions.html` (`analytics.hellebo.de`), not a `[params.plausible]` block | Declared `[taxonomies]` (tag/skill/level/topic); `params.code` selects accent; `params.navTitle`; `params.license`; `enableRobotsTXT=true`; `[params.plausible]` sub-table kept **last** | Add `[taxonomies]`, `params.code="fle"`, `params.license="CC BY-SA 4.0"` (note: README currently says **CC BY 4.0** — reconcile), `enableRobotsTXT`; rename `navbarTitle`→`navTitle`; decide whether to keep the custom Plausible/self-hosted analytics or move to the standard block |
| **go.mod** | `go 1.26.1`, pins hugo-coder pseudo-version, `// indirect` | pins hugo-coder, no mounts | OK; drop the stray `// indirect` on a direct require |
| **Content model** | 156 single files `content/track_*/units/unitNN_slug.md`; front-matter `slug:` set; `.html` aliases; section keys `track_gm_kl06` | leaf bundles `content/<course>/units/<unitNN-slug>/index.md`; **no** `slug:`; flat section key `gm-kl06` | Convert 156 units to bundles; rename `unitNN_slug`→`unitNN-slug`; drop `slug:`; retire `.html` aliases or move to redirects |
| **Exams** | 156 stranded `track_*/units/*_exam.qmd`; PDF-only, non-blocking Quarto render in CI; **no HTML pages** | first-class sibling bundles `…-exam/index.md`, `page_type: exam` | Migrate all 156 to exam bundles (see Phase 3). Biggest single gap |
| **Front-matter** | `niveau`,`klassenstufe`,`track`,`bildungsplan[]`,`subtitle`; `skills_focus:[sprechen_dialog,…]`; `presentation`/`worksheet`; no `page_type` | `page_type` discriminator; polymorphic `curriculum:{framework:bildungsplan-bw, niveau,klassenstufe,track,codes[]}`; standard `skills_focus` enum (`listening…intercultural`) | Add `page_type`; fold `bildungsplan[]`→`curriculum.codes`; remap `skills_focus` to the 8-value standard enum |
| **Layouts/design** | `_default/filiere.html`, `materiel/`, `audio-block`, `material-links`, `vgwort.html` (legacy) **and** `vgwort/url.html` (new) | `home.html`, `materials/list.html`, shared partials, `_shortcodes/*` | Extra layouts are fine; remove the legacy `vgwort.html` single-partial once `body/extensions.html` calls the resolver directly; confirm accent driven by `params.code` not hand-edited CSS |
| **Shortcodes** | only `callout`, `downloads` | `card-grid`,`card`,`hero`,`kicker`,`lead`,`details`,`callout`,`downloads` | Port the 6 missing shortcodes from `pagegen`; convert the 14 raw-HTML content files to use them |
| **Scripts/CI** | large `hugo.yml` (Quarto exam PDF render, network graph, pagefind, lighthouse, lychee, bundle budget, manifest-based `verify-vgwort.sh`); `regen-materials.yml` | lean `build-deploy.yml` with discrete gate battery incl. `verify_vgwort_coverage.py`, `verify_rendered_pixels.py`, `verify_all_pixels.py` | FLE's pipeline is richer (keep it), but it is **coupled to Quarto exam rendering** and a Quarto-era manifest. Add the coverage + rendered-pixel gates; remove the Quarto step once exams are HTML; add a curriculum `id-audit` gate |
| **Materials/audio** | committed: 156 presentation PDFs + 156 worksheet PDFs + `static/materials/audio/*` | committed under `static/materials`, CI verifies only | Conformant. Confirm every PDF carries `/Author` (gate exists: `check_pdf_attribution.py`) |
| **VG Wort** | resolver present (uses `site.Data`; pagegen uses `hugo.Data` — functionally equal); `head`+`body` wired; `data/vgwort.yaml` (2 filière entries); 193 unit/editorial marks in front matter; `vgwort-manifest.csv` (193 rows) | resolver + preload + eager img; empty `data/vgwort.yaml` seeded per work; usage registry kept **outside** repo | Resolver conformant. **156 exam Zählmarken are drawn but fire nowhere** (see §5) |
| **Legal** | `impressum`, `datenschutz`, `haftungsausschluss` present and **filled** (real § 5 DDG address); `check_legal_placeholders.sh` gate | three pages with ⟨…⟩ placeholders to fill; no mark on legal pages | Conformant. Verify Datenschutz discloses VG Wort METIS on the statutory-remuneration basis |
| **README** | **stale** — describes Quarto (`quarto render`, "rend deux fois", Reveal.js), CC BY 4.0 | Hugo instantiation instructions | Rewrite for the Hugo pipeline; reconcile the licence statement |

---

## 3. Audit — curriculum conformance

**Does fle reference curriculum descriptor IDs (`{LEVEL}.{DOMAIN}.{SCALE}.{SEQ}`)?**
**No — zero.** A repo-wide scan for the ID pattern returns 0 matches in `content/`. FLE grounds its units in **Bildungsplan-BW codes** (e.g. `3.1.3.2`, verified against `_resources/bildungsplan_bw_franzoesisch.yml`) — a *different, orthogonal* framework. The two are complementary: Bildungsplan says what the state syllabus requires; the boulingua curriculum says which CEFR CV descriptor a can-do implements. FLE currently satisfies neither the ID scheme nor the conformance-declaration requirement.

**Which conformance level can fle credibly declare?**
The consumer levels are `core` (A1–B1), `full` (A1–C1), `complete` (Pre-A1–C2). FLE spans Kl. 6–13, so its content plausibly reaches **B2/C1** on the E-track Oberstufe (Abitur units) and sits at **A1–A2** for Kl. 6–7. A credible near-term declaration is **`core` (A1–B1), `declared_conformance: partial`** — matching the `examples/de-a1/conformance.yml` pattern — with the Oberstufe extension toward `full` documented as an explicit, honest gap (the framework's `docs/conformance.md` §"Honest note" blesses declared gaps; do **not** overclaim `complete`).

**What machine-readable scope/coverage manifest must fle publish?**
Per `curriculum/docs/conformance.md`, a conforming repo MUST publish, in machine-readable form, the set of in-scope scales it implements and, per scale, the levels covered vs. `no-official-descriptor`. Concretely, FLE must add a **`conformance.yml`** at repo root modelled on `examples/de-a1/conformance.yml`:

```yaml
framework: boulingua-curriculum
framework_version: 1.0.0        # pin the curriculum release
language: fr
declared_conformance: core       # or: partial
levels: [A1, A2, B1]             # what fle claims to cover
realizations:
  - implements_id: A1.INT.conversation.01
    fr: "Je peux saluer, me présenter et demander son prénom à quelqu'un."
    unit: track_gm_kl06/units/unit01-salutations-et-prenoms
  # … one row per (unit can-do → curriculum descriptor ID)
```

**Does fle pass `curriculum/scripts/id-audit.sh`?**
`id-audit.sh` validates statements **inside the curriculum repo's own `levels/*.md`**; it is not a consumer gate. The consumer obligation (from `examples/de-a1/README.md` + `docs/verification.md`) is that **every `implements_id` in fle's `conformance.yml` must resolve to a real statement in `curriculum/levels/`**. FLE has no such file, so there is nothing to resolve today. The task is to (a) produce the mapping, and (b) add a CI gate that checks each `implements_id` against a pinned checkout of `curriculum/levels/`.

**Mapping task (the real work):** for each of the ~156 units, express its objectives ("Je peux …" bullets — already present in the unit prose) as can-do realizations and bind each to the correct descriptor ID. The curriculum ships **1170** grounded statements across the 7 levels (A2=238, B1=289 dominate — a good fit for FLE's Kl. 7–10 mass). This is authoring, not scripting: it requires reading each unit's objectives and selecting the matching (DOMAIN, SCALE, LEVEL) from `schema/scale-registry.yml`. Bildungsplan codes stay; the CEFR IDs are added alongside.

---

## 4. Task roadmap

Effort tags: **S** ≤½ day · **M** ~1–2 days · **L** ~3+ days. Ordered by dependency and value.

### Phase 1 — Structural quick wins (config + design parity)
1. **`hugo.toml` alignment (M).** Add `[taxonomies]` (tag/skill/level/topic), `params.code="fle"`, `params.license`, `enableRobotsTXT=true`; rename `navbarTitle`→`navTitle`; move analytics into `[params.plausible]` **last** (or document the deliberate self-hosted deviation). *Accept:* `hugo --gc` clean; accent still `#4B8D19`; taxonomy pages build.
2. **Port missing shortcodes (M).** Copy `card-grid`,`card`,`hero`,`kicker`,`lead`,`details` from `pagegen/layouts/_shortcodes/`. *Accept:* shortcodes render; no theme regressions.
3. **De-raw-HTML the 14 content files (M).** Replace `<div class="card-grid">`/`<div class="hero-kicker">`/`<div class="lead">` with shortcodes. *Accept:* `grep -rl '<div class="card' content/` returns 0.
4. **README rewrite (S).** Replace Quarto description with the Hugo pipeline; reconcile CC BY-SA 4.0 vs CC BY 4.0. *Accept:* no `quarto render` references remain.
5. **Retire legacy `vgwort.html` partial (S).** Have `body/extensions.html` emit the pixel directly via the resolver (as `pagegen` does). *Accept:* one img per marked page; render-verify green.

### Phase 2 — Front-matter schema migration
6. **Add `page_type` + polymorphic `curriculum:` block to all 156 units (M, scriptable).** Fold `bildungsplan[]`→`curriculum.codes`, keep `niveau/klassenstufe/track` under `curriculum`, set `framework: bildungsplan-bw`. *Accept:* `audit_content.py` extended to require `page_type` + `curriculum.framework`.
7. **Remap `skills_focus` enum (S, scriptable).** `sprechen_dialog`→`speaking_interaction`, etc., to the 8-value standard. *Accept:* no value outside the enum; network graph still builds.

### Phase 3 — Bundle conversion + exam migration (the core)
8. **Convert 156 units to leaf bundles (L, scriptable).** `content/track_*/units/unitNN_slug.md` → `…/unitNN-slug/index.md`; drop front-matter `slug:`; move `.html` aliases to a redirect map or retire. *Accept:* URLs stable or 301-mapped; lychee internal gate green.
9. **Migrate 156 exams from `.qmd` to exam bundles (L).** For each stranded `track_*/units/*_exam.qmd`, create sibling `content/<course>/units/<unitNN-slug>-exam/index.md`, `page_type: exam`, same `unit_nr`, `curriculum` block, and the exam body converted from Quarto markdown to Hugo markdown (tables/callouts → shortcodes; strip the embedded VG Wort `<img>` — it moves to front matter, see §5). Link the PDF via `exam:{file:…}`. *Accept:* 156 exam HTML pages build; each links its PDF; `audit_content.py` finds no `.qmd` carryover.
10. **Remove Quarto from CI (M).** Once exams are HTML, delete the non-blocking `quarto render` step and TinyTeX bootstrap; keep PDF exams as committed downloads under `static/downloads/` with the attribution gate. *Accept:* build-deploy has no Quarto/TeX in the deploy path.

### Phase 4 — Curriculum-ID conformance
11. **Author unit→descriptor mapping (L).** Map each unit's "Je peux …" objectives to `{LEVEL}.{DOMAIN}.{SCALE}.{SEQ}` IDs from `curriculum/levels/`. *Accept:* every mapped ID resolves against a pinned `curriculum` checkout.
12. **Publish `conformance.yml` + scope manifest (M).** Declare `framework_version`, `declared_conformance: core` (partial), covered levels, and per-scale coverage vs `no-official-descriptor`. *Accept:* consumer id-resolution gate passes.
13. **Add curriculum CI gate (S).** New step resolving every `implements_id` against a pinned `curriculum/levels/`. *Accept:* gate fails on an unresolvable ID.

### Phase 5 — VG Wort completion (see §5 — non-skippable, runs alongside Phase 3)
14. **Assign/attach a Zählmarke to all 156 new exam pages** and re-verify coverage + render across the whole site.

---

## 5. VG Wort — pixel assignment for ALL new content pages (REQUIRED)

**This is a first-class, non-skippable roadmap item.** Every new content page the roadmap introduces that is an original editorial Sprachwerk ≥ 1800 rendered characters MUST carry exactly one VG Wort Zählmarke, on exactly one URL, following `pagegen/docs/vgwort-standard.md`.

**How many new pages does the roadmap create?**
- **156 exam pages** (Phase 3, task 9) — the primary new surface. Each exam is original creative text (tasks, texts, solutions) well over the 1800-char *Mindestumfang*.
- **156 unit bundles** are *conversions* of existing pages, not new works — their marks travel in front matter (`vgwort_pixel:`) and are unaffected by the file→bundle move, **but** any `data/vgwort.yaml` entry keyed by `url:` must be re-keyed to the new bundle URL, and `.html`→bundle alias changes must not orphan a mark.
- **Curriculum artifacts** (`conformance.yml`, scope manifest) are **data, not editorial prose → no mark.** A published human-readable "coverage/can-do" annex page, if authored as ≥1800-char editorial content, **would** need a fresh mark.

**Critical finding — 156 already-drawn exam codes are currently dead.** Each of the 156 stranded `*_exam.qmd` embeds a **unique** public code (verified: 156 distinct 32-hex tokens, none overlapping the 193 unit/editorial codes, none in `vgwort-manifest.csv`). Because no exam HTML page is published, **these 156 Zählmarken fire on zero URLs** — the codes were drawn from T.O.M. but the author's statutory count is not being served. Migrating the exams (task 9) is what finally makes these marks live.

**Procedure per new exam page (task 14):**
1. **Reuse the code already drawn** — extract each exam's embedded 32-hex token from its `.qmd` (do **not** draw a fresh T.O.M. code; one already exists per exam). Draw *fresh* public codes from the author's T.O.M. account **only** for any exam found without a code, or for any genuinely new editorial page (e.g. a can-do annex).
2. **Register** each token in `data/vgwort.yaml`, keyed by the exam bundle's base-stripped `url:` (or `path: content/<File.Path>`), with `public_id`, `pixel_url`, `min_chars: 1800`, `author`, `registered_at`. (Alternatively set `vgwort_pixel:` in the exam's front matter — cleanest, since it survives future moves.)
3. **Render via the shared resolver** — no new logic: `_partials/vgwort/url.html` already resolves front-matter or `data/vgwort.yaml`, and `head/extensions.html` (preload) + `body/extensions.html` (eager `<img>`) emit it on every page. Strip the hand-rolled `<img>` from the old `.qmd` — the resolver owns emission now.
4. **Record** each mark in the private usage registry (§8 of the standard) — `Used`, `Projekt: fle`, `Sprache: fr`, `Niveau (GER)`, `Kurstitel`, `URL`, `Pixel_URL` — kept **outside** the repo. Add the 156 exam rows (and reconcile the 193 unit rows) so free vs assigned codes are authoritative.
5. **Update `vgwort-manifest.csv`** (currently 193 rows, exam rows = 0) to include the 156 exam URL↔code pairs, or migrate the gate off the Quarto-era manifest onto `pagegen`'s `verify_rendered_pixels.py` + `verify_vgwort_coverage.py`.
6. **Verify by the gates:** the **coverage audit** (warning) must show 0 unregistered editorial pages ≥1800 chars (legal excepted); the **render verify** (blocking) must find every registered `pixel_url` on exactly one page; the **hub guard** must confirm `met.vgwort.de` is absent from `/materiel/`. Keep `vgwort.de` excluded in `lychee.toml`.

**Acceptance for §5:** after Phase 3, the coverage audit reports **0** unregistered exam pages, render-verify is green for 156 exam + 193 unit/editorial marks, and the usage registry lists every assigned code with its live URL.

**Open sub-decision:** the 13 track `_index.md` section landings each currently carry a `vgwort_pixel`. The standard says **do not** mark navigation/section landings — but these pages carry substantial editorial prose ("Cap visé", cast, unit summaries). Decide per page: if a landing is genuinely a shortcode/nav surface, drop its mark; if it is a real ≥1800-char Sprachwerk, keep it and record it as such.

---

## 6. Risks & open decisions

- **Exam migrate vs delete (decide first).** The 156 exams are the largest gap *and* hold 156 already-drawn VG Wort codes. **Recommendation: migrate, not delete** — deleting strands the author's statutory marks and drops FLE far below EFL (181 exam pages). Migration is scriptable (front matter + body transform) but body conversion needs QA per exam.
- **URL stability on bundle conversion.** File→bundle renames (`unitNN_slug.md`→`unitNN-slug/`) change URLs and can orphan VG Wort `url:` keys, inbound links, and search index entries. Mitigate with a redirect/alias map and re-key `data/vgwort.yaml`; run the lychee internal gate before deploy.
- **Analytics deviation.** FLE uses a **self-hosted Plausible** (`analytics.hellebo.de`) hardcoded in `head/extensions.html`, not the template's `[params.plausible]` (`plausible.io`). Decide: adopt the standard block, or document this as an intentional, sanctioned deviation (a CI grep gate already asserts the snippet's presence).
- **Licence mismatch.** README says **CC BY 4.0**; `pagegen` standard is **CC BY-SA 4.0**. Reconcile before publishing `params.license` and the legal/attribution surfaces.
- **Conformance level — declare honestly.** Do not claim `full`/`complete`. Kl. 6–13 realistically supports **`core` (A1–B1) partial** now, with a documented path to `full` as the E-track Oberstufe units are mapped. The framework explicitly rewards declared gaps over hidden ones.
- **Curriculum version pinning.** `conformance.yml` must pin `framework_version` and the CI gate must resolve against that pinned `curriculum` tag — an unpinned check will break whenever the curriculum repo renumbers (it never renumbers IDs, but scale/level files evolve).
- **Bildungsplan vs CEFR coexistence.** Keep both: Bildungsplan codes satisfy the state-syllabus gate (`check_bildungsplan_refs.py`); curriculum IDs satisfy conformance. They are additive, not either/or — avoid dropping Bildungsplan codes during the front-matter migration.
- **Materials CI-vs-committed.** Materials are committed (156+156 PDFs + audio), matching the standard; the `regen-materials.yml` manual workflow can push binary churn — keep it manual-dispatch only and rely on the deterministic `build_materials_latex.py` to avoid history bloat.
