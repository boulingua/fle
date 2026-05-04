"""Generate placeholder worksheet PDFs for every Unit in the FLE
curriculum outline.

Usage:
    python _scripts/make_placeholder_worksheets.py

Reads `_resources/curriculum_outline.yml` and writes 156 placeholder
PDFs to `docs/downloads/<track>/kl<NN>/unit<NN>_<slug>_worksheet.pdf`.
Safe no-op when the outline does not yet exist (scaffold phase).
"""

from __future__ import annotations

import pathlib
import sys

try:
    import yaml
except ImportError:
    print("pyyaml not installed.", file=sys.stderr)
    sys.exit(1)

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as _canvas
except ImportError:
    print("reportlab not installed.", file=sys.stderr)
    sys.exit(1)

from pdf_attribution import UnitContext, apply_attribution, set_metadata


REPO = pathlib.Path(__file__).resolve().parent.parent
OUTLINE = REPO / "_resources" / "curriculum_outline.yml"
OUTPUT_ROOT = REPO / "docs" / "downloads"


def render_placeholder(out_path: pathlib.Path, ctx: UnitContext, klassenstufe: int, track: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = _canvas.Canvas(str(out_path), pagesize=A4)
    width, height = A4

    set_metadata(c, ctx, kind="Fiche d'exercices")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, height - 35 * mm, f"Fiche d'exercices — Unité {ctx.unit_nr} : {ctx.unit_title}")

    c.setFont("Helvetica", 11)
    c.drawString(
        20 * mm,
        height - 45 * mm,
        f"Niveau {ctx.cefr_level.upper()} · Klasse {klassenstufe} · Parcours {track}",
    )

    c.setFont("Helvetica-Oblique", 11)
    c.drawString(20 * mm, height - 65 * mm, "Placeholder — contenu de la fiche à venir.")

    apply_attribution(c, ctx)
    c.showPage()
    c.save()


def main() -> int:
    if not OUTLINE.exists():
        print(f"{OUTLINE.relative_to(REPO)} not found — scaffold phase. Nothing to do.")
        return 0

    plan = yaml.safe_load(OUTLINE.read_text(encoding="utf-8"))
    total = 0

    for course in plan.get("courses", []):
        track = course.get("track", "")
        klassenstufe = int(course.get("klassenstufe", 0))
        niveau = str(course.get("niveau", "")).lower()
        for unit in course.get("units", []):
            ctx = UnitContext(
                cefr_level=niveau,
                unit_nr=int(unit["unit_nr"]),
                slug=str(unit["slug"]),
                unit_title=str(unit["title"]),
            )
            out = (
                OUTPUT_ROOT
                / track
                / f"kl{klassenstufe:02d}"
                / f"unit{ctx.unit_nr:02d}_{ctx.slug}_worksheet.pdf"
            )
            render_placeholder(out, ctx, klassenstufe, track)
            total += 1

    print(f"Generated {total} placeholder worksheet PDFs under {OUTPUT_ROOT}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
