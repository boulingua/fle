"""Reusable PDF attribution helper.

Every PDF shipped from the DaF site — placeholder worksheets today,
real worksheets later — must carry S. Le Boulanger as /Author in
its metadata AND as a visible footer/watermark on every page.

This module exposes `apply_attribution(canvas, context)` so that
both the placeholder generator and any future real-worksheet
generator can share one implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen.canvas import Canvas
except ImportError:  # pragma: no cover
    A4 = (595.27, 841.89)
    mm = 2.834645669
    Canvas = None  # type: ignore


AUTHOR = "S. Le Boulanger"
SITE = "DaF"
LICENCE = "CC-BY-SA 4.0"


@dataclass
class UnitContext:
    """Per-Unit information the helper uses to decorate each page."""

    cefr_level: str                    # "a1" .. "c1"
    unit_nr: int
    slug: str
    unit_title: str


def set_metadata(canvas: "Canvas", context: UnitContext, kind: str) -> None:
    """Set PDF-level metadata. `kind` is e.g. "Worksheet" or "Exam".

    CI reads /Author via pypdf and asserts it contains 'Le Boulanger'.
    """

    canvas.setAuthor(AUTHOR)
    canvas.setTitle(f"{kind} — Einheit {context.unit_nr}: {context.unit_title}")
    canvas.setSubject(f"{SITE} — {kind} (GER {context.cefr_level.upper()})")
    canvas.setKeywords(
        f"DaF, Deutsch als Fremdsprache, Goethe-Zertifikat, CEFR "
        f"{context.cefr_level.upper()}, {kind}"
    )
    canvas.setCreator(f"{SITE} — {AUTHOR}")


def header_line(canvas: "Canvas", width: float, height: float) -> None:
    """Top-left mono header on every page."""

    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawString(20 * mm, height - 15 * mm, f"{AUTHOR} · {SITE}")
    canvas.restoreState()


def footer_line(canvas: "Canvas", width: float, context: UnitContext) -> None:
    """Centred copyright/licence/unit line on every page."""

    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    footer = (
        f"© {AUTHOR} · {LICENCE} · "
        f"GER {context.cefr_level.upper()} · Einheit {context.unit_nr}"
    )
    canvas.drawCentredString(width / 2, 12 * mm, footer)
    canvas.restoreState()


def watermark(canvas: "Canvas", width: float, height: float) -> None:
    """Diagonal 55° grey watermark across the page."""

    canvas.saveState()
    canvas.setFillGray(0.92)
    canvas.setFont("Helvetica-Bold", 48)
    canvas.translate(width / 2, height / 2)
    canvas.rotate(55)
    canvas.drawCentredString(0, 0, AUTHOR)
    canvas.restoreState()


def apply_attribution(canvas: "Canvas", context: UnitContext) -> None:
    """Decorate the current page with header + footer + watermark.

    Call this once per page, AFTER drawing content — the watermark is
    drawn on top of a saved state at the end so it never obscures text
    in a way that hurts readability (it is 92% grey, effectively a
    tint). Header and footer are safe to call anywhere.
    """

    width, height = A4
    header_line(canvas, width, height)
    footer_line(canvas, width, context)
    watermark(canvas, width, height)
