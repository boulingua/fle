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
