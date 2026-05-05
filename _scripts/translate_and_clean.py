"""
One-shot maintenance script:
  - translate German structural terms to French in all .qmd files
  - remove direct citations of "Baden-Württemberg" / "Bade-Wurtemberg" / "BW" in prose
    (bibliography page is excluded)
  - remove duplicated explicit H1 that follows the YAML `title:` (Quarto already
    renders the YAML title as the page H1)

Idempotent textual substitutions only — does not touch _resources/, .git/, docs/,
LICENSE files, or the bibliography (which is the only place where the regional
referential is named).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "docs", "_resources", "_scripts", "node_modules"}
EXCLUDE_FILES = {"bibliographie.qmd"}  # keeps the verbatim referential names

# ---------------------------------------------------------------------------
# Textual substitutions — order matters (longer phrases first)
# ---------------------------------------------------------------------------
SUBS: list[tuple[str, str]] = [
    # Hero kicker / branding
    (r"\bFLE BW ·", "FLE ·"),
    (r"\bFLE BW —", "FLE —"),
    (r"\bFLE-BW\b", "FLE"),
    (r"\bEFL BW\b", "EFL"),
    (r"\bBW-(conforme|aligné|alignée|alignés|alignées)\b",
     r"conforme au référentiel régional"),
    # KLASSE in caps (hero kicker)
    (r"\bKLASSE (\d+)", r"CLASSE \1"),
    (r"\bKL\. (\d+)", r"CL. \1"),
    # Sprechen / Schreiben standalone (e.g. in tables, prose)
    (r"\bSprechen \(Dialog\)", "Expression orale (interaction)"),
    (r"\bSprechen \(Monolog\)", "Expression orale (production en continu)"),
    (r"^\| 3\.1\.3\.5 \| Schreiben \|", "| 3.1.3.5 | Expression écrite |"),
    (r"\+ Schreiben", "+ Expression écrite"),
    (r"\+ Sprechen", "+ Expression orale"),
    (r"\bSchreiben\b", "Expression écrite"),
    (r"\bSprechen\b", "Expression orale"),
    (r"\bHören\b", "Compréhension orale"),
    (r"\bLesen\b", "Compréhension écrite"),
    (r"\bModul\b", "Module"),
    # Diploma terminology with BW/Lf
    (r"Abitur Lf BW", "épreuve finale (option d'approfondissement)"),
    (r"Abitur Bf BW", "épreuve finale (option de base)"),
    (r"Abitur Lf", "épreuve finale (option d'approfondissement)"),
    (r"Abitur Bf", "épreuve finale (option de base)"),
    (r"\bAbitur\b", "épreuve finale"),
    (r"Kommunikations-\s*\n\s*prüfung", "épreuve communicative"),
    (r"Kommunikationsprüfung", "épreuve communicative"),
    (r"\bBORS\b", "stage d'orientation"),
    (r"\bBOGY\b", "stage d'orientation au lycée"),
    (r"\bKursstufe\b", "cycle terminal"),
    (r"\(voie générale\)", "(lycée)"),
    (r"au voie générale", "au lycée"),
    (r"du voie générale", "du lycée"),
    (r"de voie générale", "de lycée"),
    (r"\bvoie générale\b", "lycée"),
    # BW standalone token (after stripping branding)
    (r"\bau format BW\b", "au format officiel"),
    (r"15/15 BW", "15/15"),
    (r"15 points BW", "15 points (barème officiel)"),
    (r"15 points BW", "15 points"),
    (r"contexte scolaire BW", "contexte scolaire local"),
    (r"format épreuve finale écrit Lf BW", "format de l'épreuve finale écrite (option d'approfondissement)"),
    (r"5 critères d'évaluation \(KMK / BW\)", "5 critères d'évaluation (officiels)"),
    (r"5 critères KMK \(Lf BW\)", "5 critères officiels (option d'approfondissement)"),
    (r"Conditions du mock final \(Lf BW\)", "Conditions du mock final (option d'approfondissement)"),
    (r"\(note allemande sur 15 points BW\)", "(note sur 15 points)"),
    (r"BW Niveau M", "Niveau M"),
    (r"barème de notes typique BW", "barème de notes typique"),
    (r"Indications de notation \(M, indicatives BW\)", "Indications de notation (M, indicatives)"),
    (r" BW(?=[\s.,;:])", ""),
    (r"\(BW\)", ""),
    # Phrases citing the Land directly — drop or neutralise
    (r"Bildungsplan-BW Französisch", "référentiel officiel de français"),
    (r"\bBildungsplan-BW\b", "référentiel régional"),
    (r"Bildungsplan gymnasiale Oberstufe 2021",
     "référentiel du cycle terminal (2021)"),
    (r"Bildungsplan 2016 Sekundarstufe I — Französisch \(2\.\s*Fremdsprache\)",
     "référentiel du secondaire I (2016) — Français (2ᵉ langue vivante)"),
    (r"Bildungsplan 2016 Baden-Württemberg",
     "référentiel régional 2016"),
    (r"Bildungsplan gymnasiale Oberstufe 2021 Baden-Württemberg",
     "référentiel du cycle terminal (2021)"),
    (r"\bBildungspläne\b", "référentiels"),
    (r"\bBildungsplan\b", "référentiel"),
    (r"Land Bade-Wurtemberg", "ayants droit régionaux"),
    (r"\bBade-Wurtemberg\b", ""),
    (r"\bBaden-Württemberg\b", ""),
    (r"Gesamtschule du Bade-Wurtemberg", "établissement secondaire"),
    (r"Gesamtschule du ", "établissement secondaire "),
    (r"\bGesamtschule\b", "établissement secondaire"),
    # Class labels — preserve initial capital when present
    (r"\bKlassen (\d+) à (\d+)\b", r"classes \1 à \2"),
    (r"\bKlasse (\d+) à (\d+)\b", r"classes \1 à \2"),
    (r"(?<=[\"\n\(>] )Klasse (\d+)\b", r"Classe \1"),
    (r"^Klasse (\d+)\b", r"Classe \1"),
    (r"\"Klasse (\d+)", r"\"Classe \1"),
    (r"\bKlasse (\d+)\b", r"classe \1"),
    (r"\bKl\. (\d+)\b", r"cl. \1"),
    (r"Klassenstufe", "niveau de classe"),
    (r"Klassenarbeit", "devoir surveillé"),
    (r"Klausur", "épreuve"),
    # Modules and skills (German official terms)
    (r"\bModul ?: ?Sprechen\b", "Module : Expression orale"),
    (r"\bModul ?: ?Schreiben\b", "Module : Expression écrite"),
    (r"\bModul ?: ?Hören\b", "Module : Compréhension orale"),
    (r"\bModul ?: ?Lesen\b", "Module : Compréhension écrite"),
    (r"\bModul ?: ?Sprachmittlung\b", "Module : Médiation"),
    (r"\bSprachmittlung\b", "médiation linguistique"),
    (r"Hör-/Hörsehverstehen", "Compréhension orale et audiovisuelle"),
    (r"Leseverstehen", "Compréhension écrite"),
    (r"zusammenhängendes monologisches Sprechen",
     "production orale en continu"),
    (r"Sprechen — an Gesprächen teilnehmen",
     "Expression orale — interaction"),
    (r"Sprechen — zusammenhängendes monologisches Sprechen",
     "Expression orale — production en continu"),
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
    (r"Bezeichnung", "Désignation"),
    # Diplomas
    (r"Mittlerer Bildungsabschluss", "diplôme intermédiaire"),
    (r"Mittlere Reife", "diplôme intermédiaire"),
    (r"Hauptschulabschluss", "diplôme de fin de scolarité obligatoire"),
    (r"Allgemeine Hochschulreife", "baccalauréat équivalent"),
    (r"Kommunikationsprüfung", "épreuve communicative"),
    # Filière labels
    (r"Niveau G\+M \(Kl\. (\d+)–(\d+)\)", r"Filière G+M (cl. \1–\2)"),
    (r"Niveau E \(Kl\. (\d+)–(\d+)\)", r"Filière E (cl. \1–\2)"),
    (r"Niveau G\+M", "Filière G+M"),
    # Misc
    (r"Notenschlüssel", "barème de notes"),
    (r"Erwartungshorizont", "horizon d'attente"),
    (r"Basisfach", "option de base"),
    (r"Leistungsfach", "option d'approfondissement"),
    (r"Sek I", "secondaire I"),
    (r"Sek II", "secondaire II"),
    (r"Prozessbezogene Kompetenzen", "Compétences transversales"),
    (r"kommunikativ, interkulturell, Text/Medien, Sprachbewusstheit, Sprachlern-\s*kompetenz",
     "communicative, interculturelle, textuelle / médiatique, conscience linguistique, compétence d'apprentissage des langues"),
    # capitalisation fixes for common derived forms at sentence/heading starts
    (r'title: "classe ', 'title: "Classe '),
    (r'title: "référentiel', 'title: "Référentiel'),
    (r'title: "devoir surveillé', 'title: "Devoir surveillé'),
    (r"\[référentiel\]", "[Référentiel]"),
    (r"^(#+ )référentiel", r"\1Référentiel", ),
    (r"^(#+ )devoir surveillé", r"\1Devoir surveillé"),
    (r"^(#+ )épreuve", r"\1Épreuve"),
    (r"^(#+ )barème", r"\1Barème"),
    (r"^(#+ )médiation", r"\1Médiation"),
    (r"^(#+ )classe ", r"\1Classe "),
    (r"^(\* +|- +|\d+\. +)référentiel", r"\1Référentiel"),
    (r"^devoir surveillé", "Devoir surveillé"),
    (r"\. devoir surveillé", ". Devoir surveillé"),
    (r"\. classe ", ". Classe "),
    (r"\. barème de notes", ". Barème de notes"),
    (r"\. référentiel", ". Référentiel"),
    (r"\. médiation", ". Médiation"),
    (r"\. épreuve", ". Épreuve"),
    # cleanup of double spaces / orphan punctuation left by removals
    (r"  +", " "),
    (r" \.", "."),
    (r" ,", ","),
    (r" \)", ")"),
    (r"\( ", "("),
]


def transform_text(text: str) -> str:
    for pattern, repl in SUBS:
        text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    return text


# ---------------------------------------------------------------------------
# Duplicate H1 removal
# ---------------------------------------------------------------------------
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
H1_RE = re.compile(r"^# (?!\#)(.+)$", re.MULTILINE)


def strip_duplicate_h1(text: str) -> str:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return text
    fm = m.group(1)
    title_match = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", fm, re.MULTILINE)
    if not title_match:
        return text
    body_start = m.end()
    body = text[body_start:]

    # Find the first H1 in the body
    h1 = H1_RE.search(body)
    if not h1:
        return text
    # Remove that single H1 line (and any single blank line that immediately follows)
    line_start = body.rfind("\n", 0, h1.start()) + 1
    line_end = h1.end()
    if line_end < len(body) and body[line_end] == "\n":
        line_end += 1
    # also consume a single blank line after
    if line_end < len(body) and body[line_end] == "\n":
        line_end += 1
    new_body = body[:line_start] + body[line_end:]
    return text[:body_start] + new_body


def process(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    new = strip_duplicate_h1(transform_text(original))
    if new != original:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    scanned = 0
    for p in ROOT.rglob("*.qmd"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.name in EXCLUDE_FILES:
            continue
        scanned += 1
        if process(p):
            changed += 1
    print(f"scanned {scanned} files, changed {changed}")


if __name__ == "__main__":
    main()
