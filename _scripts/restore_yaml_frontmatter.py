"""
The earlier translate_and_clean.py pass collapsed runs of 2+ spaces, which
unintentionally damaged YAML indentation in `.qmd` frontmatters. This script
restores each file's YAML frontmatter from git HEAD, applies the same
*translation* substitutions to the value strings only (so the displayed
metadata still reads in French), and re-attaches the file body.
"""
from __future__ import annotations
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "docs", "_resources", "_scripts", "node_modules"}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

# Same display substitutions as translate_and_clean (only those that affect
# user-visible values — keep YAML *keys* like klassenstufe untouched, and skip
# the bibliography page).
VALUE_SUBS: list[tuple[str, str]] = [
    (r"Parcours E \(Gymnasium\)", "Parcours E (lycée)"),
    (r"\(Gymnasium\)", "(lycée)"),
    (r"\bGymnasium\b", "lycée"),
    (r"\bRealschule\b", "collège"),
    (r"\bGesamtschule\b", "établissement secondaire"),
    (r"\bKlasse (\d+)\b", r"classe \1"),
    (r"\bKlassen (\d+)–(\d+)\b", r"classes \1–\2"),
    (r"\bSprechen — an Gesprächen teilnehmen\b",
     "Expression orale — interaction"),
    (r"\bSprechen — zusammenhängendes monologisches Sprechen\b",
     "Expression orale — production en continu"),
    (r"Hör-/Hörsehverstehen", "Compréhension orale et audiovisuelle"),
    (r"Leseverstehen", "Compréhension écrite"),
    (r"\bSchreiben\b", "Expression écrite"),
    (r"\bSprechen\b", "Expression orale"),
    (r"\bHören\b", "Compréhension orale"),
    (r"\bLesen\b", "Compréhension écrite"),
    (r"Sprachmittlung", "Médiation linguistique"),
    (r"Verfügen über sprachliche Mittel — Wortschatz",
     "Moyens linguistiques — lexique"),
    (r"Verfügen über sprachliche Mittel — Grammatik",
     "Moyens linguistiques — grammaire"),
    (r"Verfügen über sprachliche Mittel — Aussprache",
     "Moyens linguistiques — prononciation"),
    (r"Soziokulturelles Orientierungswissen / Themen",
     "Connaissances socio-culturelles / thèmes"),
    (r"Interkulturelle kommunikative Kompetenz",
     "Compétence interculturelle communicative"),
    (r"Funktionale kommunikative Kompetenz",
     "Compétence communicative fonctionnelle"),
    (r"Text- und Medienkompetenz",
     "Compétence textuelle et médiatique"),
    (r"\bKlassenarbeit\b", "devoir surveillé"),
    (r"\bKlausur\b", "épreuve"),
    (r"Mittlere Reife", "diplôme intermédiaire"),
    (r"Mittlerer Bildungsabschluss", "diplôme intermédiaire"),
    (r"Hauptschulabschluss", "diplôme de fin de scolarité obligatoire"),
    (r"Allgemeine Hochschulreife", "baccalauréat équivalent"),
    (r"Kommunikationsprüfung", "épreuve communicative"),
    (r"\bAbitur\b", "épreuve finale"),
    (r"\bKursstufe\b", "cycle terminal"),
    (r"\bBORS\b", "stage d'orientation"),
    (r"\bBOGY\b", "stage d'orientation au lycée"),
    (r"Basisfach", "option de base"),
    (r"Leistungsfach", "option d'approfondissement"),
    (r"Sek I", "secondaire I"),
    (r"Sek II", "secondaire II"),
    (r" BW(?=[\s.,;:\"])", ""),
]


def translate_values(fm_text: str) -> str:
    """Apply value-only translations to YAML frontmatter, preserving keys
    and indentation. Strategy: do textual subs on the whole block — the
    keys themselves don't contain any of the German source phrases, so
    this is safe."""
    for pattern, repl in VALUE_SUBS:
        fm_text = re.sub(pattern, repl, fm_text)
    return fm_text


def git_show(path: Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    try:
        return subprocess.check_output(
            ["git", "show", f"HEAD:{rel}"], cwd=ROOT, encoding="utf-8"
        )
    except subprocess.CalledProcessError:
        return None


def fix(path: Path) -> bool:
    current = path.read_text(encoding="utf-8")
    original = git_show(path)
    if original is None:
        return False
    om = FRONTMATTER_RE.match(original)
    cm = FRONTMATTER_RE.match(current)
    if not om or not cm:
        return False
    new_fm = translate_values(om.group(1))
    new_text = f"---\n{new_fm}\n---\n" + current[cm.end():]
    if new_text != current:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    fixed = 0
    for p in ROOT.rglob("*.qmd"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if fix(p):
            fixed += 1
    print(f"restored frontmatters: {fixed}")


if __name__ == "__main__":
    main()
