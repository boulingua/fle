# FLE assessment reconciliation — 31 October 2026

All 156 teaching units now point to a single sibling assessment. The first 12 Parcours E/class 6 papers were repaired in `docs/assessment-repair-2026-10-31/`; the remaining 144 pairs were individually reconciled here. Full earlier units and siblings are immutable under `originals/`. Per-pair records identify source sections, decisions, point totals and before/after hashes. Later corrections have their own full before copies under `revisions/`; the original archive is never overwritten.

The learner paper supplies the texts its questions require. Listening scripts and teacher keys use `role="key"` and are excluded from learner extraction. Reading a familiar course text is practice, not an independent transfer test. A future summative assessment requires a separately validated source. Nineteen earlier E07–E11 papers regained their originally graded speaking outcomes; written preparation does not replace observation of speaking or interaction. Compatible written tasks remain separate optional activities or are preserved in the original archive with their disposition recorded. GM06, GM07–09, GM10 and E13 retain their observed oral outcomes.

## Scoring policy

Seventy-seven papers retain a printed conversion scale from the earlier standalone paper. The scale is labelled as a proposed training scale, not a school regulation or evidence of CEFR certification. Its presence does not establish classroom validity.

Seventy-nine papers explicitly declare `assessment_scoring: points-only`. Their selected task outcomes, task allocations or recovered total differ from the incompatible prior sibling paper, or their canonical embedded assessment originally had only criterion points. Applying the former grade conversion without validation would imply a policy that has not been established. These papers state the total and additive task/criterion maxima, retain the former conversion in the immutable original archive, and await pedagogical approval. A missing conversion alone never creates an exemption: the explicit declaration and coherent point structure are required.

The independent declaration inventory is copied alongside this note as `points-only-independent-inventory.json`. Actual verification: all 156 papers pass the strict A13 arithmetic/format check (77 scales, 79 declared points-only). This verifies consistency, not difficulty, fairness, timing or approval of the score policy. GM07 unit 7 explicitly redistributes its original 8/8/12/12 allocation to 10/8/12/10, retaining a 40-point total and a graded oral performance; that editorial weighting remains proposed.

## Source corrections and evidence

`docs/factual-source-repairs/2026-10-31/manifest.json` records the first 83 factual/grammar decisions and original bytes. Later source/task/key corrections are in `revisions/coherence-followup/manifest.json`. Corrections include auxiliary and participle rules, narrative person versus focalization, purpose and future constructions, Swiss language status, historical institutional dates, privacy rights, source fidelity, and clear boundaries between fictional learning scenarios and real-world statistics, visitor information or scientific evidence. The current references identify the authoritative sources used; original bibliographies remain available for provenance.

`final-source-receipt.json` binds all 156 unit sources and sibling exams at the source freeze. The review ledger `docs/curriculum-review-2026-10-31.json` was refreshed against the actual final headings and source hashes. Mappings remain proposed, reviewer/date remain unset, and no coverage assertion was promoted. Material-only frontmatter updates after this freeze require their own receipts and ledger hash refresh.

## Verification and remaining acceptance criteria

Verified locally: curriculum resolver accepts 1,560 proposed realizations covering 261 distinct descriptors, with no coverage claim; immutable original/final record hashes for 144 pairs; YAML parsing; canonical five-step order; short in-unit exam pointers; balanced teacher-key controls; learner extraction excluding actual key blocks; point metadata; unchanged curriculum mapping declarations; strict A13 for all 156. Independent source/task reviews cover E13, GM06, GM10 and GM07–09 oral outcomes. Earlier per-track validation files describe their captured intermediate revisions; the final source receipt supersedes those hashes. The final build, rendered page checks and PDF/audio production run from the supplied freeze receipt are recorded separately by the integration/material pipelines.

Native-language and pedagogical approval, actual classroom timings, independent transfer validity and voice auditions remain pending. At freeze, 126 unit pointers have no reviewed duration. Ninety-four teaching units remain outside their required EQS word bands under the canonical learner-only count. These are content acceptance deficits; no minimum was lowered and no padding was introduced to conceal them. The earlier public HTML was stale when the source audit ran, so its exam-character counts must not be reported as a final result. Rebuild this exact revision and rerun EQS before making a rendered-length claim.

## Reproduce the source checks

From the suite checkout, run the shared curriculum resolver, strict Hugo build and kit A13/EQS commands documented in the kit and course README. The source receipt lists every frozen path and SHA-256, permitting an independent byte comparison before material capture. To review a paper, open its sibling page from the unit's assessment pointer, inspect the supplied stimulus against each task and teacher key, observe the required speaking/listening task, then record a dated review with evidence. Approval is not implied by a passing build or arithmetic check.

## Current-revision licence consistency

Current course-owned exam footers and the newly supplied illustration caption now use the existing CC BY-SA 4.0 licence established in August 2026. The stale CC BY notices came from earlier source versions and are preserved in the full original/revision archives. This correction does not withdraw the irrevocable licence on historically published versions or change any third-party source licence; see `LICENSE-HISTORY.md`. The exact exam-only revision is recorded in `revisions/licence-footer/manifest.json`. Frozen teaching-unit sources are unchanged.
