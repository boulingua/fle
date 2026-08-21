# Licence history

## 2026-08-21 — content moves from CC BY 4.0 to CC BY-SA 4.0

Until this date the content of this repository was licensed **CC BY 4.0**, and
the file named `LICENSE` held that content licence while the MIT code licence
sat in `LICENSE-CODE.md`. From this date:

- `LICENSE` is the **MIT** code licence, as it is in every other boulingua
  repository. The file named `LICENSE` now means the same thing org-wide.
- `LICENSE-CONTENT.md` is the **CC BY-SA 4.0** content licence.
- `LICENSE-CODE.md` is removed; its text is now `LICENSE`.

**Last commit under CC BY 4.0:** `a64ac01510fc9709a2f369dfdf2e6e3fab67ec36`
**Last release under CC BY 4.0:** `v0.1.0`

### This is prospective only

The CC BY 4.0 grant on every version published before this commit is
**irrevocable**. Anyone who obtained this content under CC BY 4.0 keeps that
licence for that material, permanently, and may continue to use it on those
terms. Nothing here withdraws a grant already made, and nothing here should be
read as an attempt to.

### Why

The organisation had five different licence arrangements across its
repositories and stated its terms six different ways, including two public
statements — the organisation profile and the site footer — that already
promised MIT code and CC BY-SA content. This aligns the files with what was
already being said.

ShareAlike is also the point rather than a detail: the resource hub runs a CI
gate named "Block commercial sources", and licensing the corpus CC BY — which
permits proprietary enclosure of derivatives — would contradict the gate the
author wrote.

VG Wort remuneration under §§ 54 ff. UrhG is licence-neutral, so the change
costs nothing on that side.

Recorded as ADR-0004 in <https://github.com/boulingua/.github>.
