# Recovery — Phase 1 Discovery

**Repo:** `boulingua/fle` (FLE BW — French, Gesamtschule BW, Klassen 6–13)
**Date:** 2026-05-06

## TL;DR — no recovery needed

Both **Track G+M** and **Track E** are fully present in `content/`, fully
deployed, and serving HTTP 200 on the live site. The premise of the recovery
prompt — "content appears to have been lost or only partially carried over"
— does not match this repo's state. The migration is complete.

## Inventory

### Track E (Gymnasium / Niveau E, Klassen 6–13) — 96 unit pages

| Section | Units |
|---|---|
| `content/track_e_kl06/units/` | 12 |
| `content/track_e_kl07/units/` | 12 |
| `content/track_e_kl08/units/` | 12 |
| `content/track_e_kl09/units/` | 12 |
| `content/track_e_kl10/units/` | 12 |
| `content/track_e_kl11/units/` | 12 |
| `content/track_e_kl12/units/` | 12 |
| `content/track_e_kl13/units/` | 12 |
| **Total** | **96** |

### Track G+M (Gemeinschaftsschule / Niveau G+M, Klassen 6–10) — 60 unit pages

| Section | Units |
|---|---|
| `content/track_gm_kl06/units/` | 12 |
| `content/track_gm_kl07/units/` | 12 |
| `content/track_gm_kl08/units/` | 12 |
| `content/track_gm_kl09/units/` | 12 |
| `content/track_gm_kl10/units/` | 12 |
| **Total** | **60** |

### Per-track meta pages — 26

13 × `_index.md` (track landing) + 13 × `uebersicht.md` (weekly plan).

### Grand total

**156 unit pages + 26 meta pages + 10 top-level + 5 annexes + 3 materiel hub = 200 `content/**/*.md`** — confirmed by `scripts/audit_content.py`.

## Liveness sample

| URL | Status |
|---|---|
| `https://boulingua.github.io/fle/track_e_kl06/units/salutations-et-prenoms-e/` | 200 |
| `https://boulingua.github.io/fle/track_gm_kl08/units/sport-et-equipe/` | 200 |
| `https://boulingua.github.io/fle/track_e_kl13/units/synthese-themes-litteraires/` | 200 |

## Completeness signals

| Check | Result |
|---|---|
| Drafts (would indicate stalled migration) | 0 |
| Stub bodies (< 1 KB) | 0 |
| Hard fails in `scripts/audit_content.py` (frontmatter sanity) | 0 of 200 |
| Hard fails in `scripts/validate_network_data.py` | 0 |
| VG Wort pixel coverage | 193/193 (verifier passes) |
| Bildungsplan refs rooted in `_resources/bildungsplan_bw_franzoesisch.yml` | 12 distinct codes / 318 cites — 100% rooted |
| Materials hub graph | 156 article nodes, 1270 edges, 7 topics |
| Lighthouse a11y on `/materiel/` | 95/100 (gate ≥ 95) |
| Lychee internal-link audit | 1791 URLs / 0 errors |

## What I did NOT do

- Did NOT run `git log --diff-filter=D --summary` for deleted track files: there are no deletions to recover; both track trees are fully present in HEAD.
- Did NOT search backup branches / stash / reflog: not needed.
- Did NOT extract anything to `recovery/02_sources/`: nothing to extract.

The migration record (`MIGRATION_PLAN.md` + `MIGRATION_NOTES.md`) documents the qmd → Hugo conversion, including 197 `.qmd` migrated to `.md` and 156 `_exam.qmd` retained for the hybrid PDF pipeline. Track-level deletions in git history are limited to the original `.qmd` source files removed in commit `7f05bca` (Phase 4 of the migration), all of which were already converted to `.md` in commit `80461ff`.

## Recommendation

**Stop.** The recovery prompt was likely meant for a different repo (efl, daf, ressourcen) where the qmd → Hugo migration is incomplete. In `boulingua/fle`, no Phase 2 work is needed.

If you have a specific unit you believe is missing, name it and I'll trace it. Otherwise this phase is closed.
