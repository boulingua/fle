# Current candidate evidence — 2 November 2026

This review branch is not a full-course release. The dated sections below retain
earlier observations; this section supersedes their material-production and local
validation status. No production deployment or release tag is claimed.

All 156 unit bundles now have 468 independently checked PDFs (4,504 pages)
and 468 matching thumbnails. The deck, learner worksheet and teacher worksheet
preserve source content, symbols, links and answer separation. Publication was
guarded by source/artifact hashes and retains original backups. The repository
receipt is [docs/material-build-2026-10-31.json](docs/material-build-2026-10-31.json),
with actual completion dated 2 November. All 312 active unit/exam review
records now match their current source bytes; exact superseded sources and ledger
revisions are archived. Review states and proposed mappings remain pending.

All 156 standalone assessments have source-specific reconciliation records: 77 retain grade scales and 79 explicitly use points-only scoring. The original papers, changed outcomes and retired scales remain archived. Arithmetic passes; native-language, teaching and grading-policy approval remain pending.

The strict Hugo build and all configured engineering checks pass except the
blocking D6 historical-audio gate (1,342 findings). The final browser run
exercised five representative pages and course-specific journeys, including
light/dark accessibility, downloads, search and no-JavaScript access, with zero
accessibility findings, script errors or failed requests. Existing educational
budget and counting-mark warnings remain visible; they have not been waived.

There are 506 separately staged, source-bound candidate voice clips for this
course. Full decode and input/provenance checks pass, but every clip still awaits
real listening review. Production recordings and their truthful failing D6 result
remain unchanged. The suite's `remediation/audio-candidates/index.html` supplies
transcripts, downloads and the pending review queue.

Use the exact prerequisites and commands in [README.md](README.md) with matching
candidate foundations. Release still requires substantive teaching/assessment
repairs, actual native and pedagogical review, timing/grade decisions, accepted
audio, compatible published foundation pins and successful release checks.

## Historical refinement record

# Refinement record — 30 October 2026

This is a local engineering candidate on `refine/2026-10-30`. No hosted CI,
published release or production deployment of these changes has been observed.
The suite strategy and integration order live in the organisation repository,
`docs/refinement-2026-10-30.md` and `docs/release-candidate-2026-10-30.md`.

## Purpose and improvements

The course contains 156 teaching units and 312 committed PDFs. French interface translations and shared labels are checked against actual use. Discovery works on a fresh mobile load, facets use the generated data shape, and the graph loads only on request. Download labels now describe the actual PDF files.

Shared kit repairs provide accessible navigation, real search indexing, corrected contrast/text sizing, local asset/link checks and representative browser tests. Local templates are selected by explicit layout independently of frozen URLs. Material templates have been synchronised; existing course PDFs and recordings were preserved.

## Actual validation

Strict Hugo build passed. Desktop/mobile browser journeys, automated WCAG 2.1 AA checks, search, downloads, no-JavaScript content and required local engineering checks passed. A21 now passes after the template migration. D6 remains a **release failure**: historical recordings lack sufficient model/speaker provenance and dated voice approval. A passing website build must not conceal that result. English also retains the recorded C1 mark-registry warning; no mark or published address was changed to silence it.

The strengthened curriculum resolver accepts the in-progress manifest structure, not its proposed educational assertions. Two framework source omissions and native/educational review remain blockers. One representative deck and worksheet were rebuilt and visually reviewed in a disposable copy; the full PDF corpus was not regenerated or pedagogically reapproved.

## Roadmap and acceptance

1. Review the local software candidate with the matching kit, curriculum and organisation checkouts using README.md.
2. Audition the prepared candidate voice or provide human recordings. Record actual reviewer/date/model or recording provenance; regenerate synthetic recordings only after approval, or document verifiable historical provenance. Do not invent approval for existing files.
3. Repair the framework source omissions, independently review the course mappings and assessments, and review regenerated materials before replacing committed PDFs.
4. Publish compatible dependencies and pins, run the hosted gate battery, and deploy only after every blocking gate is green and publication is authorised.

Local engineering improvements are usable for review. This course has not met all educational/audio release criteria.


## 31 October 2026 — keyed unit structure and source preservation

All units now declare the five canonical EQS steps and preserve prior heading
anchors from the rendered site. Original source and before/after hashes are in
`docs/eqs-archive/2026-10-31/`. Course mappings remain proposed; the source-hashed
review ledger is `docs/curriculum-review-2026-10-31.json`. It records actual tasks,
current descriptor statements and remaining coverage cells without fabricated
review decisions. Body/exam length and pedagogical approval remain separate.

Solutions in all 156 units now use the canonical details control. The first
12 Parcours-E/classe-6 assessments were reconciled as standalone editorial
drafts; `docs/assessment-repair-2026-10-31/` records decisions and originals.
The other 144 differing unit/sibling assessments were subsequently reconciled; see the completed source review below.


## Analytics notice consistency — 31 October 2026

Plausible remains disabled. The privacy notice explicitly says so; copied claims of active Plausible collection were removed. This does not remove or make claims about separately documented hosting or other services.

Privacy pages declare their analytics policy, language and built URL. New kit gate C9 checks actual HTML scripts and visible notices against configuration; it rejects missing, duplicate or mismatched scripts and contradictory notices. Six gate regressions and three scaffold tests passed. Representative strict builds/C9 passed for website, nsf, nvt, gfl, Scriptlibrary and all three resource-hub notice languages; the suite integration run verifies the remaining sites. This is configuration/content evidence, not certification of the remote server or legal compliance.


## Explicit release dependencies — 31 October 2026

The shared workflow caller now names the same immutable org commit in `uses` and
`org_ref`; `release-pins.json` records the actual historical kit/framework pins.
These historical pins are explicitly not the remediated release. The new org
workflow rejects absent/malformed versions, mismatched source commits and schema
bytes, and nonconforming course manifests; hubs pin dependencies without claiming
course conformance. The coordinated updater prepares exact published foundation
sets, updates consumers/checksums together and retains rollback inputs. Separate
read-only candidate CI can validate immutable pre-release commits without release
tags or deployment rights. Hosted execution and new foundation publication remain
unobserved. See the org `docs/release-pins.md`.

2026-10-31 GM06 assessment reconciliation:12 standalone assessments now contain
actual required sources and explicit item/rubric allocations. Corrected clock,
market, weather, club, preference and mediation keys; preserved live oral tasks
and teacher-only listening sources. All24 originals and before/after hashes are
archived in docs/assessment-reconciliation/2026-10-31. Five teaching steps and
audio extraction are unchanged. Strict Hugo build passes; all12 totals are30.
Native/pedagogical review and timing remain pending. Existing teaching word-budget
shortfalls remain recorded rather than padded or represented as fulfilled.


## 31 October 2026 — complete assessment source reconciliation

All 156 unit assessment pointers now identify standalone, source-complete editorial papers. The 144 remaining divergent pairs have immutable full originals, explicit decisions, hashes and revision histories in `docs/assessment-reconciliation/2026-10-31/`. Nineteen papers regained their graded oral outcomes; learner answers and listening scripts stay behind teacher-key controls. Thirty-nine teaching bodies in this tranche received coherent factual/grammar/source corrections, with original text preserved. The declaration/point checker passes all 156 papers: 77 retain proposed grade scales; 79 explicitly use criterion points without an unvalidated grade conversion. This does not approve the pedagogy or scoring policy.

The final source receipt and refreshed curriculum-review ledger bind the current tasks and mappings. All mapping assertions remain proposed and reviewer decisions pending. Native/pedagogical review, actual timing, voice auditions and substantive teaching-word-band deficits remain open. Source checks found 94 units outside the required word bands and 126 pointers without reviewed timings. Rendered exam-length and final material results must come from a rebuild of the frozen revision, not earlier public HTML. Full policy, verification boundaries and next actions are in the reconciliation README.
