"""Append the original German domain term in « » after the first occurrence
of its French translation in each .qmd file (and the SCSS file for hero
labels). Skips legal pages, bibliography (already references the originals),
and YAML frontmatter."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "docs", "_resources", "_scripts"}
EXCLUDE_FILES = {
    "bibliographie.qmd",
    "datenschutz.qmd",
    "impressum.qmd",
    "haftungsausschluss.qmd",
}

# (translated form, German original)
PAIRS: list[tuple[str, str]] = [
    ("Expression orale — interaction", "Sprechen — an Gesprächen teilnehmen"),
    ("Expression orale — production en continu",
     "Sprechen — zusammenhängendes monologisches Sprechen"),
    ("Compréhension orale et audiovisuelle", "Hör-/Hörsehverstehen"),
    ("Compréhension écrite", "Leseverstehen"),
    ("Expression écrite", "Schreiben"),
    ("Expression orale", "Sprechen"),
    ("Compréhension orale", "Hören"),
    ("Médiation linguistique", "Sprachmittlung"),
    ("médiation linguistique", "Sprachmittlung"),
    ("Compétence interculturelle communicative",
     "Interkulturelle kommunikative Kompetenz"),
    ("Compétence communicative fonctionnelle",
     "Funktionale kommunikative Kompetenz"),
    ("Compétence textuelle et médiatique", "Text- und Medienkompetenz"),
    ("Connaissances socio-culturelles / thèmes",
     "Soziokulturelles Orientierungswissen / Themen"),
    ("Moyens linguistiques — lexique",
     "Verfügen über sprachliche Mittel — Wortschatz"),
    ("Moyens linguistiques — grammaire",
     "Verfügen über sprachliche Mittel — Grammatik"),
    ("Moyens linguistiques — prononciation",
     "Verfügen über sprachliche Mittel — Aussprache"),
    ("référentiel régional", "Bildungsplan"),
    ("référentiel", "Bildungsplan"),
    ("devoir surveillé", "Klassenarbeit"),
    ("épreuve communicative", "Kommunikationsprüfung"),
    ("épreuve finale (option d'approfondissement)", "Abitur Leistungsfach"),
    ("épreuve finale (option de base)", "Abitur Basisfach"),
    ("épreuve finale", "Abitur"),
    ("option de base", "Basisfach"),
    ("option d'approfondissement", "Leistungsfach"),
    ("diplôme intermédiaire", "Mittlerer Bildungsabschluss"),
    ("diplôme de fin de scolarité obligatoire", "Hauptschulabschluss"),
    ("baccalauréat équivalent", "Allgemeine Hochschulreife"),
    ("cycle terminal", "Kursstufe"),
    ("stage d'orientation au lycée", "BOGY"),
    ("stage d'orientation", "BORS"),
    ("barème de notes", "Notenschlüssel"),
    ("horizon d'attente", "Erwartungshorizont"),
    ("lycée", "Gymnasium"),
    ("collège", "Realschule"),
    ("établissement secondaire", "Gesamtschule"),
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def split_frontmatter(text: str) -> tuple[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return text[: m.end()], text[m.end():]


def annotate_first(body: str, fr: str, de: str) -> str:
    """Append « de » after the first occurrence of `fr` that is not already
    immediately followed by an opening guillemet."""
    # Avoid annotating if the literal "fr (« de »)" or "fr (\"de\")" already exists
    already = re.compile(re.escape(fr) + r"\s*\(?[«\"]")
    if already.search(body):
        return body
    pattern = re.compile(re.escape(fr))
    m = pattern.search(body)
    if not m:
        return body
    end = m.end()
    insertion = f" (« {de} »)"
    return body[:end] + insertion + body[end:]


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    new_body = body
    for fr, de in PAIRS:
        new_body = annotate_first(new_body, fr, de)
    if new_body != body:
        path.write_text(fm + new_body, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    for p in ROOT.rglob("*.qmd"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.name in EXCLUDE_FILES:
            continue
        if process(p):
            n += 1
    print(f"annotated {n} files")


if __name__ == "__main__":
    main()
