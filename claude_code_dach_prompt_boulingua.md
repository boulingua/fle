# ROLLE UND KONTEXT

Du bist Claude Code und arbeitest an einem **vierteiligen
Schwesternsite-Projekt** unter einer GitHub-Dachorganisation
namens **`boulingua`** (Boulanger + lingua), deren Repos
Fremdsprachen-Curricula und eine zugehörige Ressourcen-
Sammlung umfassen. Autorin aller Inhalte ist
**S. Le Boulanger**.

Dieser Prompt ist der **Dach-Prompt**. Er definiert alles, was
über die vier Repos hinweg identisch oder abgestimmt sein muss.
Die inhaltlichen Details je Repo stehen in vier **eigenständigen
Repo-Prompts**, die als separate Markdown-Dateien im
`.github`-Meta-Repo vorliegen und beim Start jedes Repo-
Arbeitsabschnitts geladen werden:

- `efl-bw.prompt.md` — 180 Units EFL, Gesamtschule BW Kl. 5–13.
- `fle-bw.prompt.md` — 156 Units FLE, Gesamtschule BW Kl. 6–13.
- `daf-goethe.prompt.md` — 60 Units DaF, CEFR A1–C1 mit
  Goethe-Formaten.
- `lingua-resources.prompt.md` — kuratierter Ressourcen-Hub.

Zusätzlich gilt das **Turn-Protokoll** aus
`meta-turn-protokoll.prompt.md` für jeden einzelnen Arbeits-
Turn in jedem Repo — insbesondere: kein Turn über 3 Minuten,
ein Deliverable pro Turn, Commit am Ende jedes Turns,
`_resources/generation_log.yml` als Rückgrat.

Dieser Dach-Prompt **ersetzt die vier Repo-Prompts nicht** — er
ordnet sie ein und legt die gemeinsamen Standards fest. Kein
Repo-Inhalt wird hier ein zweites Mal dupliziert.

# ORGANISATIONSSTRUKTUR AUF GITHUB

```
github.com/boulingua/
├── .github/                  Org-Meta-Repo: gemeinsame READMEs,
│                             Issue-Templates, die vier Repo-
│                             Prompts, dieses Dach-Prompt,
│                             CONTRIBUTING.md, globale Lizenz-
│                             informationen.
├── efl                       EFL BW (1 Site, Quarto, GitHub Pages).
├── fle                       FLE BW (1 Site, Quarto, GitHub Pages).
├── daf                       DaF Goethe (1 Site, Quarto, GitHub Pages).
└── hub                       Ressourcen-Hub (1 Site, Quarto, GitHub Pages).
```

Die Repo-Namen sind bewusst kurz (`efl`, `fle`, `daf`, `hub`).
Der curriculare Kontext (BW-Schulform, Klassenstufen, CEFR-
Niveau) steht in der jeweiligen `README.md` und im Site-
Impressum.

Jedes der vier Content-Repos wird auf GitHub Pages deployt
unter `https://boulingua.github.io/<repo>/`:

- EFL: `https://boulingua.github.io/efl/`
- FLE: `https://boulingua.github.io/fle/`
- DaF: `https://boulingua.github.io/daf/`
- Hub: `https://boulingua.github.io/hub/`

Falls später eine Custom Domain gewünscht ist (z. B.
`boulingua.de` oder `leboulanger.edu`), ist das über die Pages-
Einstellungen nachträglich möglich — der Dach-Prompt trifft
dazu keine Annahme.

# AUTORIN UND URHEBERRECHT

Alle Inhalte — Curricula, Prüfungsbeispiele, Arbeitsblatt-
Platzhalter, Ressourcen-Kuratierungen, Redaktionstexte — stammen
von **S. Le Boulanger**. Auf jeder Site, jedem PDF, jedem
Foliensatz wird sie einheitlich so geführt:

- Fließtext und Metadaten: `S. Le Boulanger`.
- PDF-Metadaten-Autorfeld: `S. Le Boulanger`.
- Sichtbarer Copyright-Vermerk auf jedem PDF und Site-Footer:
  `© S. Le Boulanger · <MIT für Code / CC-BY-SA 4.0 für Inhalt>`.
- Setzung pro Repo einmalig via `_metadata.yml` im `units/`-
  bzw. Content-Ordner. Nie Autor-Felder in einzelnen `.qmd`-
  Dateien.

**Lizenzsplit** ist für alle vier Repos identisch:

- **MIT-Lizenz** für den Website-Code (Quarto-Konfig, Lua-
  Shortcodes, Python-/Shell-Skripte, YAML-Schema).
- **CC-BY-SA 4.0** für die didaktischen und kuratorischen
  Inhalte (Units, Prüfungsbeispiele, Ressourcen-Beschreibungen,
  Annotationen).

In jedem Repo liegt:
- `LICENSE` — MIT-Text.
- `LICENSE-content` — CC-BY-SA 4.0-Text.
- `README.md` — kurze Erklärung des Lizenzsplits mit Verweis
  auf beide Dateien.

# DESIGN-SYSTEM (für alle vier Repos verbatim identisch)

Die vier Sites müssen **visuell ununterscheidbar** sein, bis auf
die Navbar-Inhalte und den Site-Titel. Das ist eine bewusste
Designentscheidung: Lehrende und Lernende, die zwischen den
Sites wechseln (z. B. vom FLE-Unit zur Ressourcen-Hub-Suche),
sollen nicht das Gefühl bekommen, eine andere Plattform zu
betreten.

## Palette, Typografie, CSS

Identisch in allen vier Repos — siehe `efl-bw.prompt.md`
Abschnitt „DESIGN-SYSTEM" als kanonische Definition. Die
anderen drei Repo-Prompts verweisen explizit auf diese
Definition. Bei Änderungen am Design-System wird die
kanonische Quelle (EFL-Prompt) aktualisiert und die drei
Schwestern-Prompts müssen ihren Verweis darauf bestätigen.

Konkret identisch:
- `--bg`, `--fg`, `--accent`, `--rule` usw. (siehe
  EFL-Prompt „Palette").
- Source Sans 3 + JetBrains Mono.
- `_quarto.yml`-Theme-Block (`flatly` hell, `darkly` dunkel,
  `custom.scss` drüber).
- Hell/Dunkel-Toggle, `data-bs-theme`-Kaskade.

## Repo-Abweichungen im Design

Jede Site darf sich **nur** an folgenden Stellen unterscheiden:

1. **Navbar-Title** (`EFL BW`, `FLE BW`, `DaF`, `Ressourcen`).
2. **Navbar-Menüstruktur** (Klassenstufen, CEFR-Stufen,
   Filter — repospezifisch).
3. **Site-Titel und -Beschreibung** in `_quarto.yml`.
4. **Akzentbadges** wie CEFR-Stufenfarben (A1 grün, A2 blau-
   grün, B1 blau, B2 violett, C1 dunkelrot) im DaF-Repo oder
   Niveau-Badges (G/M/E farblich verschieden) in EFL/FLE.
5. **Repo-spezifische Ressourcen-Typ-Badges** im Hub (OE/CC/PD-
   Lizenztypen).

Alles andere — Schriftarten, Hauptfarben, Hero-Blöcke, Karten-
Raster, Footer — ist identisch.

# GEMEINSAME SEITEN: IMPRESSUM UND DATENSCHUTZ

Alle vier Sites führen **eigene** Impressums- und Datenschutz-
Seiten. Sie sind inhaltlich fast identisch, aber nicht verlinkt
auf eine Master-Version, weil das rechtlich fragwürdig wäre
(jede Site muss ihr eigenes vollständiges Impressum haben).

Pro Repo:
- `impressum.qmd`
- `datenschutz.qmd`
- Beide in deutscher Sprache (deutsches Recht gilt).
- Beide mit `<TODO>`-Platzhaltern für Adresse + Kontakt-E-Mail,
  umhüllt in `callout-warning`-Blöcken, die vor dem Livegang
  ausgefüllt werden müssen.
- CI-Gate in jedem Repo: `grep -R "<TODO>" impressum.qmd
  datenschutz.qmd` muss null Treffer liefern, bevor deployt
  wird.

**Pro Repo ein site-spezifischer Zusatz im Impressum:**

- **EFL-Repo und FLE-Repo:** Hinweis „Diese Materialien sind
  eine persönliche didaktische Sammlung der Autorin und
  stehen in keinem offiziellen Zusammenhang mit einer Schule,
  dem Land Baden-Württemberg oder dem Kultusministerium. Der
  Bezug zum Bildungsplan BW ist inhaltlich-fachlich, keine
  offizielle Freigabe."
- **DaF-Repo:** Hinweis „Die bereitgestellten Prüfungsbeispiele
  orientieren sich formal an den öffentlich dokumentierten
  Prüfungsformaten der Goethe-Zertifikate A1–C1. Sie sind
  eigene didaktische Adaptionen der Autorin und stehen in
  keinem offiziellen Zusammenhang mit dem Goethe-Institut
  e. V."
- **Hub-Repo:** Passus zur Haftung für Links (siehe
  `lingua-resources.prompt.md`) und klare Unterscheidung
  zwischen verlinkten und inhaltlich nutzbaren Quellen.

Datenschutzerklärung in allen vier Repos identisch, mit
GitHub-Pages-US-Hosting offengelegt, keine Cookies, keine
Tracker.

# LIZENZTYPOLOGIE (nur relevant für Hub, aber hier festgelegt)

Aus Konsistenzgründen wird die vierstufige Lizenztypologie
**zentral im Dach-Prompt** definiert, obwohl nur der Hub sie
aktiv verwendet. Die drei Curriculum-Repos nennen sie in ihren
„Weiterführende Ressourcen"-Abschnitten als Orientierung:

- **Typ OE** — öffentliche Institution, Vollurheberrecht,
  verlinkbar, nicht kopierbar.
- **Typ CC** — Creative-Commons-lizenziert, Wiederverwendung
  unter Lizenzbedingungen.
- **Typ PD** — gemeinfrei / Public Domain.
- **Typ K** — kommerziell, aus allen vier Repos
  **ausgeschlossen**.

Detail siehe `lingua-resources.prompt.md`.

# CI-MUSTER (einheitlich, mit repo-spezifischen Gates)

Alle vier Repos nutzen:

- GitHub Actions mit **offiziellen Pages-Actions**
  (`actions/deploy-pages@v4`), nicht `peaceiris/actions-gh-pages`.
- `actions/checkout@v4`, `quarto-dev/quarto-actions/setup@v2`,
  `actions/setup-python@v5`.
- Python 3.11 mit `pyyaml pandas jupyter` als Basis.
- Cache von `_freeze/` zwischen Läufen.
- Pages-Quelle im Repo-Setting auf „GitHub Actions".

**Repo-spezifische Zusatzabhängigkeiten und -Gates:**

| Repo | Zusätzlich in pip | CI-Gates |
|------|-------------------|----------|
| efl  | `reportlab pypdf` + tinytex | 180 Exam-PDFs + 180 Worksheet-PDFs vorhanden; Autor-Metadata in allen PDFs; Impressum-TODO-Check |
| fle  | `reportlab pypdf` + tinytex | 156 Exam-PDFs + 156 Worksheet-PDFs vorhanden; Autor-Metadata; Impressum-TODO-Check |
| daf  | `reportlab pypdf` + tinytex | 60 Exam-PDFs + 60 Worksheet-PDFs vorhanden; Autor-Metadata; Impressum-TODO-Check |
| hub  | `jsonschema requests` | Kommerziell-Quellen-Blocker; Copyright-Vollständigkeitscheck; Impressum-TODO-Check; wöchentlicher Link-Check-Cron |

Jedes Repo hat seinen eigenen `publish.yml`. Der Hub hat
zusätzlich einen `link-check.yml` (Cron Montag 06:00 UTC).

# META-TURN-PROTOKOLL (verbindlich für alle vier Repos)

Für jede Arbeit an jedem der vier Repos gilt das Meta-Turn-
Protokoll aus `meta-turn-protokoll.prompt.md`, insbesondere:

- **Ein Deliverable pro Turn.** Nie zwei Dateien oder zwei
  Units in einem Turn schreiben.
- **Commit am Ende jedes Turns.** Unclean zu enden gilt als
  Turn-Fehlschlag.
- **`_resources/generation_log.yml`** pro Repo als Rückgrat der
  Wiederaufnahmefähigkeit. Am Anfang jedes Turns lesen, am Ende
  aktualisieren.
- **Drei-Zeilen-Statusantwort** pro Turn: „✓ Fertig: <X> ·
  Commit: <sha> · Nächster Turn: <Y>".
- **Kein `quarto render` in Content-Turns** — rendern ist ein
  eigener dedizierter Turn.
- **Turn-Größenlimits**: Unit ≤ 350 Zeilen, bei Überschreitung
  Split in Turn A und Turn B mit `<!-- TURN B: -->`-Marker.

Die Phasengliederung pro Repo steht in der jeweiligen
Repo-Prompt-Datei. Der Dach-Prompt legt nur die Orchestrierung
über Repos hinweg fest.

# ORCHESTRIERUNG ÜBER REPOS HINWEG

Die vier Repos werden **nicht parallel** von Anfang bis Ende
gebaut, sondern in einer sinnvollen Reihenfolge, in der jedes
Repo entweder vom Vorgänger profitiert oder als Referenz für
das nächste dient.

## Empfohlene globale Reihenfolge

**Block 1 — Org-Setup (eine Session)**

- `boulingua`-Organisation auf GitHub anlegen (manuell durch
  Nutzer:in).
- `.github`-Meta-Repo mit README, CONTRIBUTING.md, den fünf
  Prompt-Dateien und einem einheitlichen Issue-Template.
- Der User bestätigt die Org-URL und GitHub-Pages-Setting.

**Block 2 — DaF-Repo als Kleinstes und Prototypisches (~80 Turns)**

Startet zuerst, weil:
- 60 Units ist die kleinste Menge — reale Proofs entstehen
  schneller.
- CEFR A1–C1 ist didaktisch gut abgegrenzt, keine
  Bildungsplan-Fetch-Risiken.
- Das Design-System wird hier zum ersten Mal komplett geprüft
  und falls nötig im Dach-Prompt nachgeschärft.
- B1 als Prototyp (aus `daf-goethe.prompt.md` Phase 3) liefert
  die Referenz für alle weiteren Units der drei
  Curriculum-Repos.

Am Ende von Block 2: alle vier Phasen durchlaufen, Site live,
Handover-Dokument vorhanden.

**Block 3 — FLE-Repo (~187 Turns)**

Startet nach DaF, weil:
- FLE erbt das Design-System vollständig.
- Die Arbeit am französischsprachigen immersiven Tonfall
  profitiert vom deutschsprachigen DaF als Kontrast.
- Die Bildungsplan-BW-Fetch-Risiken entstehen erst hier und
  können in Phase 0 abgefangen werden.
- Ein FLE-Prototyp auf Kl. 8 G+M wird geschrieben, bevor die
  restlichen 12 Kurse fan-out gemacht werden.

**Block 4 — EFL-Repo (~215 Turns)**

Größtes Curriculum. Profitiert maximal von FLE:
- Dieselbe Zweitrack-Struktur (G+M vs. E).
- Dieselben Bildungsplan-Strukturen.
- Derselbe Prototyp-Ansatz (Kl. 7 G+M).

EFL als Letztes der drei Curricula, weil der akkumulierte
Lernprozess die größte und riskanteste Einheit am besten
absichert.

**Block 5 — Hub-Repo (~23 Turns)**

Startet erst **nachdem die drei Curriculum-Repos live sind**,
weil:
- Der Hub pro Ressource eine Unit-Zuordnung braucht, und die
  Units müssen existieren, damit Links stabil sind.
- Die Lizenz-Audit-Phase (Phase 0 des Hub-Prompts) kann dann
  konkret für die kuratierten Quellen live geprüft werden.
- Die Hub-Coverage-Matrix (Phase 3) kann gegen die tatsächliche
  Unit-Menge aller drei Curriculum-Sites validiert werden
  (180 + 156 + 60 = 396 Units, jede soll ≥ 1 Ressource haben).

## Alternative Orchestrierung: paralleler DaF + Hub

Falls zeitliche Bandbreite vorhanden ist und zwei Strömen
gleichzeitig gearbeitet werden kann (z. B. verschiedene
Wochentage), ist parallel zulässig: **DaF und Hub-Scaffold
gleichzeitig**. Der Hub beginnt Phase 0 und 1 während der
DaF-Phasen 3–5. Der Hub geht dann erst in Phase 2 (Kern-
Ressourcen einpflegen), wenn DaF Block 2 abgeschlossen ist.

FLE und EFL bleiben strikt sequenziell nach DaF, weil sie
dieselben Bildungsplan-Ressourcen nutzen und parallele Fetches
zu Ratenlimits auf `bildungsplaene-bw.de` führen könnten.

# CROSS-REPO-VERWEISE

Jede Site verweist im Footer auf die Schwesternsites:

```
[EFL BW](https://boulingua.github.io/efl/) ·
[FLE BW](https://boulingua.github.io/fle/) ·
[DaF](https://boulingua.github.io/daf/) ·
[Ressourcen](https://boulingua.github.io/hub/)
```

Zusätzlich auf jeder Startseite ein kurzer Schwesternsite-
Abschnitt (3–4 Sätze), der die anderen drei Sites erklärt.

Der Hub hat **zusätzlich** pro Ressource Deep-Links in die
Unit-Seiten der drei Curriculum-Sites. Damit die Deep-Links
nicht brechen, gilt in allen drei Curriculum-Repos die
**Unit-URL-Garantie**:

- Pfad pro Unit: `<repo>/<kurs>/units/unit<NN>_<slug>.html`.
- `unit_nr` und `slug` aus dem Front Matter. Einmal
  festgelegt, nie geändert.
- Falls eine Unit umbenannt wird, gilt **301-Redirect-Pflicht**:
  Entweder via GitHub Pages `_redirects`-Datei (wenn Netlify-
  kompatibel) oder via Meta-Refresh-Stub-Seiten unter der
  alten URL, die auf die neue weiterleiten. Redirects werden in
  `_redirects.yml` pro Repo dokumentiert.

# GEMEINSAME QUALITÄTSSTANDARDS

Diese Standards gelten über alle vier Repos hinweg und werden
in jedem Repo-Prompt referenziert, nicht dupliziert:

1. **Keine urheberrechtlich geschützte Imagery.** Lucide-Icons
   (ISC), selbst gezeichnete SVG-Meme-Templates, Wikimedia
   Commons mit korrekter Attribution. Keine Stock-Fotos mit
   unklarer Lizenz.
2. **Keine Institutionenlogos.** Kein Goethe-, British-Council-,
   Institut-Français-Logo. Auch nicht bei Prüfungsbeispielen,
   die sich formal an deren Formaten orientieren. Markenrecht.
3. **Keine Paraphrase von Lehrwerken.** Keine Inhalte von Klett,
   Cornelsen, Hueber, Oxford UP, Cambridge UP, Hachette FLE,
   CLE International, Didier, Schubert, Pons — auch nicht
   „inspired by". Originaltexte der Autorin.
4. **Keine Reproduktion offizieller Prüfungstexte.** Goethe-
   Modellsätze, BW-Abitur-Originaltexte, offizielle
   Bildungsstandard-Testaufgaben werden nicht kopiert. Formal
   orientieren, inhaltlich original.
5. **Keine R-Umgebung.** Kein R-Code, kein `renv.lock`, kein
   `setup_check.R`, keine R-Pakete in CI. Python nur für
   Hilfsskripte (YAML-Rendering, Placeholder-PDFs, Schema-
   Validierung).
6. **Keine Emojis im Content.** Ausnahmen: die kleinen
   Download-Icons in den `{{< downloads >}}`-Shortcodes
   (📄 🎞 📋 📝), die Teil der Karten-UX sind. Sonst keine.
7. **Kein Berlin-/München-Monopol im DaF-Content** (Österreich,
   Schweiz, Südtirol, Diaspora berücksichtigen).
   **Kein Paris-Monopol im FLE-Content** (Belgien, Schweiz,
   Québec, Maghreb, Afrika berücksichtigen). **Ausgewogene
   britische/US-amerikanische/weitere anglophone
   Perspektiven im EFL-Content** (Irland, Kanada, Australien,
   Neuseeland, anglophone Karibik, anglophone Afrika).

# INITIALER SETUP-TURN

Wenn Claude Code zum ersten Mal für das `boulingua`-Projekt
startet — bevor irgendein Repo angefasst wird — ist der erste
Turn ausschließlich für Org-Setup:

1. **Fragen an den User** (nur einmal, dann nie wieder):
   - Ist die Org `boulingua` auf GitHub angelegt? (Nutzer:in
     muss das manuell tun; falls Name belegt, Alternative
     festlegen.)
   - Sind die vier Repos `efl`, `fle`, `daf`, `hub` und das
     `.github`-Meta-Repo angelegt und leer?
   - Ist GitHub Pages pro Content-Repo auf „GitHub Actions"
     als Source gesetzt?
   - Welcher Account ist als Admin der Org festgelegt (für
     Secrets, Pages-Konfig)?
2. **Warten auf Bestätigung.**
3. **Scaffold des `.github`-Repos** mit:
   - `README.md` der Org (Kurzbeschreibung aller vier Repos).
   - `CONTRIBUTING.md` (wie externe Beiträge gehandhabt werden —
     voreingestellt auf „nicht aktiv, persönliches Projekt").
   - `ISSUE_TEMPLATE/` mit Vorlagen für Bug, Ressourcenvorschlag
     (hub-spezifisch), Unit-Vorschlag (curriculum-spezifisch).
   - Kopien der fünf Prompt-Dateien (dieser Dach-Prompt, das
     Meta-Turn-Protokoll, die vier Repo-Prompts) unter
     `prompts/`.
   - `LICENSE` (MIT) und `LICENSE-content` (CC-BY-SA 4.0).
4. **Generation-Log für das `.github`-Repo** anlegen:
   `_resources/generation_log.yml` mit `site: "boulingua-meta"`.
5. **Commit + Status-Meldung**:
   ```
   ✓ Fertig: .github-Meta-Repo scaffoldet (8 Dateien)
   Commit: <sha>
   Nächster Turn: DaF-Repo Phase 0 beginnen (Goethe-Format-Fetch A1)
   ```

# TURN-WEITERGABE ZWISCHEN REPOS

Wenn Claude Code zwischen Repos wechselt (z. B. von DaF nach
FLE), ist der letzte DaF-Turn immer ein **Handover-Turn**:

1. DaF-Generation-Log als „phase_complete" markieren.
2. Kurze Zusammenfassung in `docs/HANDOVER_DAF.md` schreiben:
   Was ist fertig, welche Kompromisse gab es, welche offenen
   Punkte stehen für spätere Pflege an.
3. Commit unter dem Branch `main` mit Tag `v1.0.0`.
4. Status-Meldung an User:
   ```
   ✓ Fertig: DaF-Repo Block 2 abgeschlossen, Site live unter
     https://boulingua.github.io/daf/
   Commit: <sha>
   Nächster Turn: FLE-Repo Phase 0 (BW-Bildungsplan-Fetch Kl. 6 E)
   ```

Danach beginnt FLE-Repo mit einem eigenen, neuen
`generation_log.yml`. Kein Durchmischen der Logs.

# AKZEPTANZKRITERIUM DIESES DACH-PROMPTS

Das Dach-Prompt ist erfolgreich, wenn:

- Alle vier Repos unter `boulingua` existieren und live
  deploybar sind.
- Jede Site ist visuell ununterscheidbar von den anderen (bis
  auf die erlaubten Abweichungen).
- Jede Site hat korrektes Impressum und Datenschutz in deutscher
  Sprache mit ausgefüllten Kontaktdaten.
- Die Footer-Verlinkung zwischen den vier Sites funktioniert in
  beide Richtungen (jede Site hat die drei anderen im Footer).
- Der Hub hat für jede der 396 Curriculum-Units mindestens
  eine empfohlene Ressource.
- Kein Repo enthält kommerziellen Content oder Lehrwerks-
  Paraphrasen.
- Das `.github`-Meta-Repo enthält alle fünf Prompt-Dateien und
  dient als nachvollziehbare Projektdokumentation.
- Die vier `_resources/generation_log.yml`-Dateien
  dokumentieren den Verlauf nachvollziehbar.

# WAS DIESES PROMPT NICHT LEISTET

Es ist explizit **kein** Ersatz für die vier Repo-Prompts. Die
stehen weiterhin als eigenständige Spezifikationen (1300–1500
Zeilen jeweils) zur Verfügung. Dieses Dach-Prompt regelt nur
das Dazwischen: Orchestrierung, Gemeinsamkeiten, Org-
Management, Querverweise.

Es ist auch **kein** Ersatz für das Meta-Turn-Protokoll. Das
regelt die Turn-Kadenz pro Repo und gilt separat.

# HARTER STOPP

Kein Turn dieses Dach-Prompts beginnt, bevor die
`boulingua`-Org auf GitHub existiert und die fünf Repos
(`efl`, `fle`, `daf`, `hub`, `.github`) manuell angelegt sind.
Kein Content-Repo wird gebaut, bevor das `.github`-Meta-Repo
steht und die fünf Prompt-Dateien dort liegen. Die Reihenfolge
der Blöcke (DaF → FLE → EFL → Hub) wird nicht umgestellt ohne
expliziten User-Auftrag. Kein kommerzieller Anbieter taucht in
einem der vier Repos auf. Kein Repo wird ohne lokalen
`quarto render`-Erfolg gepusht.
