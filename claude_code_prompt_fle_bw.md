# RÔLE ET CONTEXTE

Tu es Claude Code, agissant en tant qu'ingénieur de curriculum
reproductible et développeur front-end pour du contenu d'enseignement
des langues. Construis un site web complet et déployable de type
« cours » avec Quarto pour le **FLE (Français Langue Étrangère)** dans
une Gesamtschule du Bade-Wurtemberg, couvrant la Klasse 6 à la
Klasse 13.

Ce projet est le **site jumeau** d'un site EFL déjà défini. Les deux
sites doivent être visuellement et structurellement identiques —
même palette, même navbar, même architecture, même auteure, même
chaîne CI. Seul le contenu linguistique et la grille des
Klassenstufen diffèrent.

Ceci n'est PAS un cours de statistiques ou de programmation. Pas de
code R, pas d'exécution de code, pas de `renv.lock`, pas de
`setup_check.R`, pas de paquets R dans la CI. Chaque Unité est une
unité d'enseignement des langues : compréhension écrite,
compréhension orale, médiation (Sprachmittlung), expression écrite,
expression orale, grammaire, lexique, interculturel. Le contenu se
présente sous forme de prose, de tableaux, de diapositives
illustrées d'icônes, de notes de présentation et d'exemples
d'épreuves corrigés.

L'architecture est adaptée d'un scaffold Quarto à double format :

- Pages d'accueil multi-cours avec blocs hero et grilles de cartes.
- Découpage hebdomadaire par cours (= par Klassenstufe).
- Chaque Unité est rendue DEUX FOIS à partir d'un seul source
  `.qmd` — article HTML ET jeu de diapositives Reveal.js.
- Modèle pédagogique à cinq étapes de type CLIL/EMILE sur chaque
  Unité : **Activer → Découvrir → S'entraîner → Produire → Réfléchir**.
  (Variante préparation-épreuve : **Tâche → Modèle → Stratégie →
  Essai → Feedback**.)
- Palette claire + sombre avec un bouton soleil/lune accessible.
- CI GitHub Pages via les actions officielles `actions/deploy-pages@v4`.

# AUTEURE

Tous les contenus sont de **S. Le Boulanger** (même auteure que le
site EFL jumeau) et doivent apparaître comme telle sur chaque Unité
et chaque jeu de diapositives, défini une seule fois via un
`_metadata.yml` dans le dossier `units/` de chaque cours — jamais en
modifiant les fichiers individuellement.

# STRUCTURE À DEUX PARCOURS (verbatim)

Gesamtschule du Bade-Wurtemberg, français deuxième langue vivante,
deux parcours parallèles :

- **Parcours A — G+M (niveau grundlegend + mittleres Niveau) :**
  Klasse 6 → 10. Cinq Klassenstufen. Objectif : Hauptschulabschluss
  (fin Kl. 9) et Realschulabschluss / Mittlerer Bildungsabschluss
  (fin Kl. 10).
- **Parcours B — E → Abitur (niveau erweitert, gymnasial) :**
  Klasse 6 → 13. Huit Klassenstufen. Objectif : Allgemeine
  Hochschulreife (Abitur), épreuve écrite de français et épreuve
  communicative (Kommunikationsprüfung).

**Note sur le démarrage en Kl. 6.** En BW, le français comme 2e
langue vivante commence typiquement en Klasse 6. Si la Gesamtschule
de l'auteure propose un profil langues démarrant en Kl. 5, ajouter
deux cours supplémentaires (track_gm_kl05 et track_e_kl05) dans la
phase 0 — mais uniquement après confirmation explicite.

Total par défaut : **13 cours**, une grille par Klassenstufe par
parcours (5 pour G+M, 8 pour E).

# PORTÉE

- **12 Unités par Klassenstufe.** Environ alignées sur l'année
  scolaire (semaines 1–40 moins les semaines d'épreuves, donc
  12 Unités de ~3 semaines chacune).
- **156 Unités au total** sur les deux parcours (5×12 + 8×12).
- Chaque Unité comprend : article HTML, jeu de diapositives
  Reveal.js, exemple d'épreuve, fiche d'exercices (placeholder).
- Klasse 6–10 : exemple d'épreuve = **Klassenarbeit** au format BW
  (kompetenzorientiert, adapté au niveau).
- Klasse 11–13 : exemple d'épreuve = **épreuve type Abitur** au
  format BW (écrite ou communicative, selon le focus de l'Unité).

# ALIGNEMENT SUR LE CURRICULUM DU BADE-WURTEMBERG — CONTRAINTE DURE

Le site doit correspondre au **Bildungsplan 2016 Sekundarstufe I**
(pour Kl. 6–10, les deux parcours) ET au **Bildungsplan gymnasiale
Oberstufe 2021** (pour Kl. 11–13, parcours E), spécifiquement pour
**Französisch als zweite Fremdsprache**.

Avant de rédiger toute Unité, tu dois :

1. Récupérer les pages actuelles du Bildungsplan BW pour
   Französisch (2. Fremdsprache) au niveau concerné (G, M, E)
   depuis `https://www.bildungsplaene-bw.de/` — spécifiquement les
   Fachpläne Französisch en Sekundarstufe I et les pages Oberstufe
   pour Französisch (Basisfach et Leistungsfach).
2. Extraire, par Klassenstufe et niveau, les **prozessbezogene
   Kompetenzen** (communicatives, interculturelles, conscience
   langagière, méthodologiques) et **inhaltsbezogene Kompetenzen**
   (thèmes, types de textes, grammaire, lexique, compétences).
3. Stocker le squelette extrait à
   `_resources/bildungsplan_bw_<track>_<klasse>.yml` afin que le
   front matter de chaque Unité puisse citer explicitement son
   Kompetenzbereich.
4. Si une page ne peut pas être récupérée, STOP et signaler. Ne
   pas inventer de références Bildungsplan. Ne pas paraphraser de
   mémoire.

Le front matter de chaque Unité doit comporter un champ
`bildungsplan:` listant les compétences couvertes (p. ex.
`["2.1.1 Hör-/Hörsehverstehen", "3.1.1.3 Umgang mit Texten und Medien"]`).

# CONTRAINTES DURES

- **Aucun code R, aucune exécution de code, aucune simulation de
  données.** Le bloc `execute:` est supprimé de `_quarto.yml`. Pas
  de dossiers `code/`. Pas de chunks.
- **La métalangue est le français tout au long** (immersif / CLIL).
  Notes pour l'enseignante, rubriques, consignes — tout en
  français. Les seules portions en allemand sont : (a) les
  citations verbatim du Bildungsplan, (b) la terminologie des
  épreuves BW (Klassenarbeit, Sprachmittlung/Mediation, Abitur,
  Kommunikationsprüfung), (c) les textes sources allemands dans
  les tâches de Sprachmittlung.
- **Chaque Unité suit le modèle à cinq étapes** (ou la variante
  préparation-épreuve lorsque l'Unité est une unité de préparation
  aux épreuves).
- **Chaque Unité est rendue en article HTML ET en jeu de
  diapositives Reveal.js** à partir d'un seul source. Vérifier deux
  fois le front matter de chaque Unité.
- **Récit adapté à l'âge.** Kl. 6 (première année de français) :
  très concret, ludique, personnages forts, beaucoup d'images
  (icônes), phrases courtes. Kl. 7–9 : arc narratif, personnages
  réalistes, humour léger, culture française et francophone
  quotidienne. Kl. 10–11 : porté par l'argumentation, culturel et
  littéraire, problématisé. Kl. 12–13 : analytique, niveau
  discursif, qualité épreuve.
- **Diapositives visuellement accrocheuses.** Utiliser les icônes
  Lucide (via des SVG `lucide-static` dans `assets/icons/`) et des
  modèles de mèmes génériques dessinés en SVG (p. ex. « Drake »,
  « Distracted Boyfriend », « Expanding Brain » — reconstructions
  géométriques uniquement, jamais de photos des vrais mèmes
  téléchargées). Aucune imagerie pop-culture sous droits d'auteur.
  Aucun logo d'institution.
- **Le commutateur clair/sombre fonctionne dans les deux sens.**
  Corps, cartes, bordures, liens et pied de page doivent tous
  suivre `data-bs-theme`.
- **Le pied de page et les pages d'accueil pointent vers du vrai
  contenu.** Pas de stubs.
- **S. Le Boulanger apparaît comme auteure sur chaque Unité et
  chaque jeu de diapositives** via un `_metadata.yml` dans chaque
  dossier `units/`.
- Pas d'épreuves au-delà de l'exemple-épreuve par Unité. Pas de
  notation. Pas d'emoji.
- Ton : pratique, chaleureux, immersif, pédagogiquement précis.
  Voix d'enseignante, pas voix d'éditeur de manuel.

# SYSTÈME DE DESIGN (verbatim, identique au site EFL)

## Palette

```
Clair :
  --bg #ffffff   --fg #23272b   --fg-alt #555
  --rule #eaeaea --surface #f7f8fa
  --accent #1a73e8 --accent-hover #0b57d0
  --code-bg #f5f5f5

Sombre :
  --bg #1d1f21   --fg #e8e8e8   --fg-alt #a8a8a8
  --rule #2d3035 --surface #26292c
  --accent #79b8ff --accent-hover #b8d4fd
  --code-bg #2a2d31
```

## Typographie

- Corps + titres : **Source Sans 3**
- Mono (brand navbar, kickers, étiquettes de format d'épreuve) :
  **JetBrains Mono**

## `styles.css`

La palette CSS s'appuie sur `data-bs-theme="light"/"dark"` (l'attribut
que le bouton Quarto bascule), avec un repli
`@media (prefers-color-scheme: dark) :root:not([data-bs-theme])`
pour la détection OS à la première visite. Forcer les propres
variables CSS de Bootstrap à suivre la palette :

```css
:root, [data-bs-theme="light"], [data-bs-theme="dark"] {
  --bs-body-bg: var(--bg);
  --bs-body-color: var(--fg);
  --bs-border-color: var(--rule);
  --bs-secondary-bg: var(--surface);
  --bs-tertiary-bg: var(--surface);
  --bs-emphasis-color: var(--fg);
  --bs-link-color: var(--accent);
  --bs-link-hover-color: var(--accent-hover);
  --bs-heading-color: var(--fg);
  --bs-primary: var(--accent);
}
```

Sans ceci, `darkly`/`flatly` se mélangent en cascade et le bouton
ne fonctionne qu'à moitié. Également, donner à `html`, `body`,
navbar et footer un `background: var(--bg) !important` explicite
pour qu'aucun thème par défaut ne transparaisse.

Inclure le CSS pour : bloc hero (avec kicker mono), grille de
cartes (auto-fit minmax 240px, translate-Y au survol), navbar
discrète (fond `var(--bg)`, brand mono, liens `var(--fg-alt)`,
`var(--accent)` au survol/actif), footer aligné sur le corps, une
classe utilitaire `.icon-circle` pour les SVG Lucide inline dans la
prose, `.meme-frame` pour les mèmes génériques SVG sur les
diapositives, et une puce `.niveau-badge` (G / M / E colorée
différemment).

## `custom.scss`

```scss
/*-- scss:defaults --*/
$primary: #1a73e8;
$body-color: #23272b;
$link-color: #1a73e8;
$link-hover-color: #0b57d0;
$font-family-sans-serif: "Source Sans 3", -apple-system, BlinkMacSystemFont, sans-serif;
$font-family-monospace: "JetBrains Mono", "Fira Code", monospace;
$headings-font-weight: 600;
$border-radius: 6px;
```

## `assets/slides.scss` (Reveal.js, palette sombre)

```scss
/*-- scss:defaults --*/
$body-bg: #1d1f21;
$body-color: #e8e8e8;
$link-color: #79b8ff;
$presentation-font-family: "Source Sans 3", sans-serif;
$presentation-heading-color: #e8e8e8;
$code-block-bg: #2a2d31;
```

# ARCHITECTURE DU DÉPÔT

```
<repo>/
├── fle-bw.Rproj
├── _quarto.yml
├── index.qmd                 accueil
├── a_propos.qmd
├── demarrer.qmd
├── calendrier.qmd            index complet avec liens
├── references.qmd
├── remerciements.qmd
├── bildungsplan.qmd          vue d'ensemble de l'alignement curriculaire
├── impressum.qmd             mentions légales (TMG § 5 / DDG § 5)
├── datenschutz.qmd           politique de confidentialité (RGPD)
├── styles.css
├── custom.scss
├── assets/
│   ├── slides.scss
│   ├── icons/                SVG Lucide, récupérés localement
│   └── memes/                modèles de mèmes SVG génériques
├── _includes/
│   └── _exam.tex             en-tête LaTeX partagé pour les PDF d'épreuves
├── _extensions/
│   └── downloads/            shortcode Lua pour {{< downloads >}}
├── _scripts/
│   ├── make_placeholder_worksheets.py  génère 156 PDF placeholder
│   ├── pdf_attribution.py              helper réutilisable en-tête/pied/filigrane
│   └── organise_downloads.sh           déplace les PDF d'épreuves aux chemins canoniques
├── _resources/
│   ├── bildungsplan_bw_gm_kl06.yml  … kl10.yml
│   └── bildungsplan_bw_e_kl06.yml   … kl13.yml
├── downloads/                 (généré ; .gitignored ; peuplé en CI)
├── README.md, LICENSE, .gitignore, .nojekyll
├── .github/workflows/publish.yml
├── appendices/
│   ├── demarche_pedagogique.qmd
│   ├── arbre_competences.qmd
│   ├── glossaire.qmd
│   ├── erreurs_frequentes.qmd
│   └── baremes_evaluation.qmd
├── track_gm_kl06/            … jusqu'à track_gm_kl10/
│   ├── index.qmd
│   ├── calendrier.qmd
│   └── units/
│       ├── _metadata.yml     author: "S. Le Boulanger"
│       ├── unit01_<slug>.qmd      … unit12_<slug>.qmd
│       └── unit01_<slug>_exam.qmd … unit12_<slug>_exam.qmd
└── track_e_kl06/             … jusqu'à track_e_kl13/
    ├── index.qmd
    ├── calendrier.qmd
    └── units/
        ├── _metadata.yml
        ├── unit01_<slug>.qmd      … unit12_<slug>.qmd
        └── unit01_<slug>_exam.qmd … unit12_<slug>_exam.qmd
```

# `_quarto.yml`

```yaml
project:
  type: website
  output-dir: docs

website:
  title: "FLE BW — S. Le Boulanger"
  description: "Un cursus de français langue étrangère à deux parcours pour Gesamtschule Baden-Württemberg, de la Klasse 6 à la Klasse 13, aligné sur le Bildungsplan."
  site-url: "https://<user>.github.io/<repo>/"
  navbar:
    title: "FLE BW"
    left:
      - href: index.qmd
        text: "Accueil"
      - href: a_propos.qmd
        text: "À propos"
      - href: bildungsplan.qmd
        text: "Bildungsplan"
      - href: calendrier.qmd
        text: "Calendrier"
      - text: "Niveau G+M (Kl. 6–10)"
        menu:
          - href: track_gm_kl06/index.qmd
            text: "Klasse 6"
          - href: track_gm_kl07/index.qmd
            text: "Klasse 7"
          - href: track_gm_kl08/index.qmd
            text: "Klasse 8"
          - href: track_gm_kl09/index.qmd
            text: "Klasse 9"
          - href: track_gm_kl10/index.qmd
            text: "Klasse 10"
      - text: "Niveau E (Kl. 6–13)"
        menu:
          - href: track_e_kl06/index.qmd
            text: "Klasse 6"
          - href: track_e_kl07/index.qmd
            text: "Klasse 7"
          - href: track_e_kl08/index.qmd
            text: "Klasse 8"
          - href: track_e_kl09/index.qmd
            text: "Klasse 9"
          - href: track_e_kl10/index.qmd
            text: "Klasse 10"
          - href: track_e_kl11/index.qmd
            text: "Klasse 11"
          - href: track_e_kl12/index.qmd
            text: "Klasse 12"
          - href: track_e_kl13/index.qmd
            text: "Klasse 13"
    right:
      - icon: github
        href: https://github.com/<user>/<repo>
  page-navigation: true
  page-footer:
    left: "FLE BW · © S. Le Boulanger · MIT / CC-BY-SA 4.0"
    center: |
      [Démarrer](/demarrer.qmd) · [Calendrier](/calendrier.qmd) ·
      [Bildungsplan](/bildungsplan.qmd) ·
      [Démarche pédagogique](/appendices/demarche_pedagogique.qmd) ·
      [Arbre des compétences](/appendices/arbre_competences.qmd) ·
      [Glossaire](/appendices/glossaire.qmd) ·
      [Erreurs fréquentes](/appendices/erreurs_frequentes.qmd) ·
      [Barèmes](/appendices/baremes_evaluation.qmd) ·
      [Références](/references.qmd) ·
      [Remerciements](/remerciements.qmd) ·
      **[Impressum](/impressum.qmd)** ·
      **[Datenschutz](/datenschutz.qmd)**
    right: "Construit avec [Quarto](https://quarto.org)"

format:
  html:
    theme:
      light: [flatly, custom.scss]
      dark:  [darkly, custom.scss]
    css: styles.css
    toc: true
    toc-depth: 3
    toc-location: right
    link-external-newwindow: true
    include-in-header:
      - text: |
          <link rel="preconnect" href="https://fonts.googleapis.com">
          <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
          <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

editor: source
```

Tous les liens du pied de page DOIVENT être absolus (slash
initial). L'Impressum et la Datenschutzerklärung restent en
allemand car ce sont des mentions légales au droit allemand.

# AUTEURE PAR MÉTADONNÉES

Dans le dossier `units/` de chaque cours, émettre un
`_metadata.yml` :

```yaml
author: "S. Le Boulanger"
```

Quarto l'hérite automatiquement pour chaque `.qmd` du dossier. Ne
jamais éditer les fichiers d'Unité un par un pour définir l'auteure.

# FRONT MATTER D'UNITÉ (chaque Unité, verbatim)

```yaml
---
title: "Unité N — <Thème>"
subtitle: "<Libellé parcours> · Klasse <K> · Niveau <G|M|E>"
niveau: "<G|M|E>"
klassenstufe: <K>
track: "<gm|e>"
unit_nr: <N>
slug: "<slug-en-kebab>"
bildungsplan:
  - "<code et libellé exact depuis bildungsplaene-bw.de>"
  - "<deuxième code le cas échéant>"
skills_focus:
  - comprehension_orale
  - expression_orale
  - comprehension_ecrite
  - expression_ecrite
  - mediation
  - reflexion_sur_la_langue
format:
  html:
    toc: true
    toc-depth: 3
  revealjs:
    output-file: "unit<NN>_slides.html"
    theme: [default, ../../assets/slides.scss]
    slide-number: c/t
    progress: true
    scrollable: true
    transition: none
    preview-links: auto
---
```

L'article est rendu uniquement en HTML. Le jeu de diapositives
uniquement en HTML. L'épreuve uniquement en PDF, depuis le fichier
wrapper séparé `unit<NN>_<slug>_exam.qmd`.

Exactement un niveau par fichier d'Unité. Les Unités appartiennent
à exactement un dossier de parcours.

# STRUCTURE D'UNITÉ (chaque Unité, verbatim)

1. `::: {.callout-note}` indiquant la variante du modèle (par
   défaut = Activer → Découvrir → S'entraîner → Produire →
   Réfléchir ; préparation-épreuve = Tâche → Modèle → Stratégie →
   Essai → Feedback) ET le niveau.
2. Appel du shortcode `{{< downloads >}}` pour afficher les quatre
   liens de téléchargement en haut de l'Unité.
3. `## Objectifs d'apprentissage` — 3 énoncés « Je peux... » au
   format CECRL (p. ex. « Je peux présenter ma famille en utilisant
   les adjectifs possessifs au singulier. »).
4. `## Alignement Bildungsplan` — liste à puces correspondant au
   front matter, avec le code et le libellé allemand verbatim.
5. `## Amorce narrative` — un court crochet narratif (80–250 mots
   selon la Klassenstufe) présentant les personnages, le lieu ou
   l'ancrage culturel de l'Unité. Voix adaptée à l'âge.
6. `## 1. Activer` (ou Tâche) — mise en train, vérification des
   prérequis, remue-méninges, ou amorce visuelle.
7. `## 2. Découvrir` (ou Modèle) — le texte cible (compréhension
   écrite/orale avec transcription), explication grammaticale ou
   exemple travaillé. Inclure l'intégralité du texte ou de la
   transcription ici, rédigée originalement.
8. `## 3. S'entraîner` (ou Stratégie) — exercices guidés :
   exercices à trous, appariement, transformation, repérage
   d'erreurs, substitution. Fournir exercices ET corrigés dans un
   bloc `::: {.callout-tip collapse="true"}` intitulé
   « Corrigé ».
9. `## 4. Produire` (ou Essai) — production ouverte : consigne
   d'expression orale, tâche d'expression écrite, jeu de rôle,
   mini-médiation. Inclure une production-modèle au niveau cible.
10. `## 5. Réfléchir` (ou Feedback) — bilan métacognitif, grille
    d'auto-évaluation alignée sur les objectifs « Je peux... ».
11. `## Exemple d'épreuve` — tâche d'épreuve complète au niveau
    approprié à la Klassenstufe. Voir la section EXEMPLES
    D'ÉPREUVES ci-dessous. Cette section est AUSSI rendue en PDF
    autonome (voir TÉLÉCHARGEMENTS).
12. `## Téléchargements` — bloc callout listant quatre liens,
    peuplé par le même shortcode `{{< downloads >}}` (article HTML,
    diapositives HTML, fiche d'exercices PDF placeholder, épreuve
    PDF).
13. `::: {.notes} ... :::` — notes de présentation pour le jeu de
    diapositives uniquement, donnant à l'enseignante le minutage,
    les transitions et les indications de différenciation.
14. `## Pièges classiques` — 2 à 4 puces, centrées sur les erreurs
    d'apprenants.
15. `## Pour aller plus loin` — 1 à 3 ressources authentiques
    (liens vers TV5Monde Apprendre, RFI Apprendre le français,
    Les Zexperts FLE, Bonjour de France, France Culture, ressources
    éducatives libres). Aucun contenu payant. Aucune numérisation
    pirate de manuel.

Chaque Unité fait 150 à 350 lignes de prose. Contenu réel,
rédigé originalement. Ne pas paraphraser Klett, Cornelsen, Hachette
FLE, CLE International, Didier, Hueber, ou tout autre manuel
publié.

# JEU DE DIAPOSITIVES — EXIGENCES VISUELLES

Chaque sortie Reveal.js d'Unité doit comporter :

- Une **diapositive titre** avec le nom de l'Unité, la
  Klassenstufe, une puce de niveau et une grande icône Lucide qui
  représente le thème (p. ex. `utensils` pour une Unité « La
  cuisine »).
- Une **diapositive « Amorce »** avec le crochet narratif en
  30–50 mots plus un grand mème SVG générique réagissant au thème.
  Utiliser la classe `.meme-frame`. Le mème doit provenir des
  modèles génériques dans `assets/memes/` (Drake, Distracted
  Boyfriend, Expanding Brain, Success Kid, Is This A Pigeon, Two
  Buttons, Change My Mind) reconstruits en SVG original avec des
  rectangles et formes simples — jamais tracés ni téléchargés
  depuis les vrais mèmes. Légender le mème comme une blague
  pédagogique.
- **Diapositives-compétences riches en icônes.** Pour chacune des
  cinq étapes, une diapositive avec le nom de l'étape, une icône
  Lucide (`brain-circuit` pour Activer, `book-open` pour
  Découvrir, `dumbbell` pour S'entraîner, `mic` pour Produire,
  `compass` pour Réfléchir) et trois puces brèves.
- **Diapositives lexique/grammaire** en disposition à deux
  colonnes avec des icônes encadrant les items cibles.
- Une **diapositive « Zoom »** pour tout texte authentique :
  utiliser la fonctionnalité de zoom de Reveal (classe `r-stretch`
  sur un bloc) pour que le texte remplisse l'écran.
- Une **diapositive « Aperçu épreuve »** montrant la structure de
  la Klassenarbeit ou de la tâche Abitur qui clôt l'Unité.
- **Diapositive de clôture** avec les objectifs « Je peux... »
  réapparaissant en checklist à lire à voix haute.

Notes de présentation sur chaque diapositive, couvrant : estimation
de temps, transition, différenciation pour l'autre niveau présent
dans la salle, micro-question de vérification de compréhension.

# RÉCIT ADAPTÉ À L'ÂGE PAR KLASSENSTUFE

| Klasse | Voix | Longueur de phrase | Humour | Personnages |
|--------|------|--------------------|--------|-------------|
| 6      | Concret, ludique, présent de l'indicatif dominant | 6–10 mots | Silly, visuel | Ensemble animal + enfant (p. ex. **Léa**, **Tom**, **Pépin le lapin**) |
| 7      | Épisodique, aventurier | 8–12 mots | Slapstick | Camarades de classe + famille (collège) |
| 8      | Réaliste, centré sur les pairs | 10–15 mots | Observationnel | Ado protagoniste + groupe (correspondance francophone) |
| 9      | Identité, équité, appartenance | 12–18 mots | Sec, ironique | Ado + correspondant·e francophone international |
| 10     | Choix de société, monde du travail, médias | 15–20 mots | Argumentatif | Ensemble jeunes adultes |
| 11     | Entrée culturelle et littéraire | 18–25 mots | Essayistique | Narrateurs + voix d'auteurs (courts textes) |
| 12     | Analytique, niveau discursif | 20–30 mots | Académique | Textes-comme-personnages (Camus, Sartre, Ernaux, Despentes) |
| 13     | Niveau épreuve, problématisé | Variée, académique | Retenu | Voix publiques, écrivains francophones |

Les personnages récurrents reviennent d'une Unité à l'autre au sein
d'une Klassenstufe (petite distribution nommée : p. ex. Kl. 6 a
**Léa**, **Tom**, **Pépin le lapin**, **M. Moutarde**). Nommer la
distribution dans l'`index.qmd` du cours et la réutiliser.

**Ancrage francophone, pas seulement hexagonal.** Intégrer dès
Kl. 7 des personnages et des contextes venant de Belgique
francophone, Suisse romande, Québec, Maghreb, Afrique francophone
de l'Ouest et Océan Indien — le FLE scolaire allemand a tendance à
ne représenter que Paris, ce que cette ressource corrige
délibérément.

# EXEMPLES D'ÉPREUVES — FORMAT BW

## Klasse 6–10 (les deux parcours) : Klassenarbeit

Chaque Unité se termine par une **Klassenarbeit corrigée** adaptée
au niveau :

- **Niveau G :** courte, fortement structurée, étayage important,
  support visuel, QCM + exercices à trous dominants, courte tâche
  productive à la fin.
- **Niveau M :** items fermés et semi-ouverts mélangés, une tâche
  de médiation (résumé allemand → français), courte tâche
  d'expression écrite.
- **Niveau E :** moins d'étayages, items plus ouverts, médiation +
  tâche d'expression écrite plus longue, une question de
  compréhension inférentielle.

Chaque Klassenarbeit fournit :

- Un en-tête avec niveau, durée (typique BW : 45 ou 90 minutes),
  matériel autorisé.
- 3 à 5 tâches étiquetées au format BW (Tâche 1 : Compréhension
  orale / Tâche 2 : Compréhension écrite / Tâche 3 : Maniement de
  la langue / Tâche 4 : Médiation / Tâche 5 : Expression écrite —
  adapté au focus de compétences de l'Unité).
- Matériel stimulus (courts textes originaux, transcriptions,
  passages allemands pour la médiation).
- Un **corrigé attendu** dans un callout replié, rédigé au niveau
  cible.
- Un **barème** avec les points par tâche typiques BW et une
  Notenschlüssel indicative (1–6).

## Klasse 11–13 (parcours E uniquement) : épreuve type Abitur

Chaque Unité se termine par une **tâche Abitur exemplifiée** au
format BW :

- **Écrit Abitur :** Partie A (compréhension : env. 24 BE), Partie
  B (analyse : env. 18 BE), Partie C (rédaction / prise de
  position : env. 18 BE), plus tâche de médiation ou de traduction
  (env. 30 BE). Total env. 90 BE, ajusté à 60 ou 90 BE selon que
  l'Unité modélise Basisfach ou Leistungsfach.
- **Kommunikationsprüfung :** tâche monologue + dialogue avec
  matériel stimulus.
- Distinguer Unité par Unité entre **Basisfach** et
  **Leistungsfach** — étiqueter dans le front matter sous `niveau`
  comme `E-BF` ou `E-LF` pour Kl. 11–13 uniquement.
- Inclure les réponses attendues au niveau de référence et une
  grille d'évaluation alignée sur les catégories
  Erwartungshorizont + Bewertungsraster du BW (Inhalt / Sprache).

## Contrainte sur les sources des exemples d'épreuves

Tous les textes stimulus dans les exemples d'épreuves doivent être
originaux (rédigés par l'auteure), dans le domaine public, ou
clairement sous licence de réutilisation éducative. Citer la source
sous chaque stimulus. Ne jamais reproduire de matériel d'épreuves
sous droits d'auteur issu de sujets Abitur BW passés ou de tests
blancs commerciaux.

# TÉLÉCHARGEMENTS — QUATRE LIENS PAR UNITÉ

Chaque Unité expose quatre liens, présentés dans une carte callout
bien visible près du haut (sous le `callout-note` qui nomme la
variante du modèle) ET de nouveau en bas de l'Unité dans la section
`## Téléchargements`. Mêmes quatre liens aux deux endroits.

Deux sont des pages web vivantes, deux sont des PDF.

| Lien | Format | Pointe vers |
|------|--------|-------------|
| Article d'Unité | HTML | La page rendue de l'Unité (auto-lien). |
| Jeu de diapositives | HTML | Le compagnon Reveal.js. |
| Fiche d'exercices | PDF | Polycopié élève. **PDF placeholder pour l'instant.** |
| Exemple d'épreuve | PDF | Klassenarbeit ou tâche Abitur autonome. |

## Convention de nommage (stricte)

```
unit<NN>_<slug>.html                                    (article d'Unité)
unit<NN>_slides.html                                    (Reveal.js)
downloads/<track>/kl<NN>/unit<NN>_<slug>_worksheet.pdf  (fiche, placeholder)
downloads/<track>/kl<NN>/unit<NN>_<slug>_exam.pdf       (épreuve)
```

Exemple pour parcours E, Klasse 12, Unité 3 « Dystopies
francophones » :
```
track_e_kl12/units/unit03_dystopies_francophones.html
track_e_kl12/units/unit03_slides.html
downloads/e/kl12/unit03_dystopies_francophones_worksheet.pdf
downloads/e/kl12/unit03_dystopies_francophones_exam.pdf
```

## Production du PDF d'épreuve

Un second source `.qmd` vit à côté de chaque Unité :
`units/unit<NN>_<slug>_exam.qmd`. C'est un wrapper fin qui
`{{< include >}}` uniquement le contenu de l'épreuve (la section
`## Exemple d'épreuve` plus ses callouts corrigé et barème) depuis
l'Unité. Son front matter fixe `format: pdf` uniquement. Cela
préserve une source unique tout en produisant un PDF d'épreuve
autonome propre, construit via Quarto + tinytex pendant
`quarto render`.

## Production du PDF de fiche d'exercices (stratégie placeholder)

Le contenu des fiches d'exercices sera rédigé plus tard. Pour
l'instant, livrer un **PDF placeholder d'une page par Unité** avec
le nom de fichier canonique correct. Ainsi, tous les liens du site
en ligne fonctionnent immédiatement et remplir plus tard les vraies
fiches devient un simple remplacement de fichier, sans modification
du code du site.

Générer les placeholders programmatiquement avec un petit script
Python `_scripts/make_placeholder_worksheets.py` :

```python
# Pseudo-code — à implémenter dans l'étape scaffold.
# Pour chaque Unité du plan du curriculum :
#   - calculer track, klassenstufe, unit_nr, slug
#   - produire un PDF A4 d'une page contenant :
#       en-tête :       "S. Le Boulanger · FLE BW"
#       titre :         "Fiche d'exercices — Unité {N} : {titre}"
#       ligne meta :    "Niveau {G|M|E} · Klasse {K} · Parcours {gm|e}"
#       corps :         "Placeholder — contenu de la fiche à venir."
#       pied :          "© S. Le Boulanger · CC-BY-SA 4.0"
#       filigrane :     "S. Le Boulanger" en diagonale 55°
#   - écrire dans downloads/<track>/kl<NN>/unit<NN>_<slug>_worksheet.pdf
```

Utiliser `reportlab` ou `fpdf2` (installer en CI avec
pyyaml/pandas). Le script lit le même YAML d'outline du curriculum
que la carte thématique, donc les noms de fichiers sont garantis
cohérents avec le reste du site.

## Shortcode `{{< downloads >}}`

Implémenter un shortcode Quarto Lua à `_extensions/downloads/` qui
lit `track`, `klassenstufe`, `unit_nr` et `slug` depuis le front
matter de l'Unité et émet les quatre liens. Chaque Unité appelle
`{{< downloads >}}` deux fois — une fois près du haut, une fois
dans `## Téléchargements`.

Émettre exactement ce markup :

```markdown
::: {.callout-tip icon=false title="Téléchargements"}
- [📄 Article d'Unité](unit<NN>_<slug>.html)
- [🎞 Jeu de diapositives](unit<NN>_slides.html)
- [📋 Fiche d'exercices (PDF)](/downloads/<track>/kl<NN>/unit<NN>_<slug>_worksheet.pdf)
- [📝 Exemple d'épreuve (PDF)](/downloads/<track>/kl<NN>/unit<NN>_<slug>_exam.pdf)
:::
```

Les liens article et diapositives sont relatifs (même dossier).
Les liens fiche et épreuve sont absolus depuis la racine du site.

## Ordre du pipeline de build (CI)

1. `python _scripts/make_placeholder_worksheets.py` → écrit 156
   PDF placeholder directement dans
   `docs/downloads/<track>/kl<NN>/`.
2. `quarto render` → produit le site HTML (articles + jeux de
   diapositives) ET chaque PDF d'épreuve depuis les wrappers
   `_exam.qmd`.
3. `_scripts/organise_downloads.sh` déplace les PDF d'épreuves
   dans `docs/downloads/<track>/kl<NN>/` avec le nom canonique.
4. `docs/` est téléversé comme artéfact Pages.

Pas de decktape. Pas de Chromium. Pas de PDF d'article.

## Gestion des PDF manquants

La CI DOIT échouer si un PDF attendu est absent :

```bash
EXAMS=$(find docs/downloads -name "*_exam.pdf" | wc -l)
WORKS=$(find docs/downloads -name "*_worksheet.pdf" | wc -l)
test "$EXAMS" -eq 156
test "$WORKS" -eq 156
```

# PLAN THÉMATIQUE (proposer-et-confirmer)

Avant de rédiger toute Unité, générer un grand tableau unique
montrant, pour chacun des 13 cours (Parcours × Klassenstufe), les
12 titres d'Unités et leur Kompetenzbereich Bildungsplan principal.
Utiliser des thèmes issus du Bildungsplan BW (famille, école,
maison, loisirs, nourriture, animaux, saisons, France, Belgique,
Suisse romande, Québec, Maghreb, Afrique francophone, francophonie
plurielle, médias, travail, justice sociale, littérature, théâtre,
cinéma français, dystopies et contre-utopies, discours politique,
science et éthique, mondialisation). Attribuer les thèmes
progressivement — concret et personnel en Kl. 6–7, élargi au
culturel et global en Kl. 8–9, critique et analytique en Kl. 10–13.

ATTENDRE mon feu vert sur le plan avant de générer des Unités.

# PAGE D'ACCUEIL (`index.qmd`)

Bloc hero avec kicker (mono, accent : « FLE · BADE-WURTEMBERG »),
H1 « Français pour Gesamtschule, Klasse 6 à 13 », paragraphe
d'intro signé S. Le Boulanger. Ensuite :

- *Ce qu'est ce site* (~120 mots).
- *À qui s'adresse ce site* (~100 mots) — enseignantes des deux
  parcours, tous niveaux.
- *Les deux parcours* — grille de deux cartes (G+M Kl. 6–10 ;
  E Kl. 6–13, bachelière) pointant vers l'index de chaque
  parcours.
- *Les treize cours* — grille secondaire pointant chaque
  Klassenstufe.
- *Le modèle en cinq étapes* (~100 mots) avec icônes Lucide
  inline.
- *Une source, deux formats* (~80 mots).
- *Préparation aux épreuves* (~80 mots) expliquant la couverture
  Klassenarbeit et Abitur.
- *Site jumeau* — court paragraphe signalant l'existence du site
  EFL frère par la même auteure, avec lien.
- *Pour aller plus loin* — liens à puces (Démarrer, Bildungsplan,
  Calendrier, Annexes, Références, Remerciements).

Pas de remerciements inline — pointer vers la page complète.

# PAGE D'ACCUEIL PAR COURS (`track_<x>_kl<NN>/index.qmd`)

- Kicker : « PARCOURS <G+M|E> · KLASSE <NN> » en mono/accent.
- H1 : « Klasse <NN> français — <baseline personnage sur une
  ligne> ».
- Présentation de la distribution récurrente (les personnages
  nommés de cette Klassenstufe) avec une icône Lucide chacun.
- Grille de cartes des 12 Unités du cours, montrant le numéro
  d'Unité, le titre, le focus de compétences et la puce de niveau.
- Un court bloc « Ce que vous saurez faire à la fin de l'année »,
  paraphrasant les Kompetenzerwartungen du Bildungsplan (avec les
  libellés allemands exacts dans un callout replié).
- Lien vers le `calendrier.qmd` de ce cours.

# PAGE BILDUNGSPLAN (`bildungsplan.qmd`)

- Vue d'ensemble du Bildungsplan BW 2016 (Sek I) et du
  Bildungsplan gymnasiale Oberstufe 2021 pour Französisch.
- Tableaux récapitulatifs par Klassenstufe des prozessbezogene et
  inhaltsbezogene Kompetenzen, sourcés depuis
  `_resources/bildungsplan_bw_*.yml`.
- Liens directs profonds vers chaque Unité qui couvre chaque
  Kompetenz.

Cette page est **générée depuis les ressources YAML**, pas
rédigée à la main. Écrire un petit helper `.qmd` qui lit les YAML
et rend un tableau via un filtre Lua inline ou un équivalent
simple en Python (puisqu'il n'y a pas de R dans ce projet,
utiliser un chunk Python avec `yaml` et `pandas` via
`jupyter: python3`). Installer les dépendances en CI.

# ANNEXES (liées depuis le pied de page)

- `demarche_pedagogique.qmd` — organigramme mermaid + prose
  (Alignement curriculum → Plan d'Unité → Activer → Découvrir →
  S'entraîner → Produire → Réfléchir → Évaluation → Feedback →
  Unité suivante).
- `arbre_competences.qmd` — arbre mermaid : départ au besoin de
  compétence (compréhension orale / écrite / expression orale /
  écrite / médiation / réflexion sur la langue / interculturel),
  feuille = liens directs vers les Unités dans les 13 cours.
- `glossaire.qmd` — termes FLE (étayage, CECRL, i+1, réceptif vs
  productif, tâche, approche actionnelle) et termes spécifiques
  BW (Klassenarbeit, Sprachmittlung / médiation,
  Kompetenzerwartung, Bildungsplan, Basisfach, Leistungsfach,
  Kommunikationsprüfung, Erwartungshorizont, Bewertungsraster),
  par ordre alphabétique, première occurrence liée à l'Unité qui
  l'introduit.
- `erreurs_frequentes.qmd` — erreurs d'apprenants par
  Klassenstufe : transferts L1 (allemand) typiques (faux amis
  FR/DE, place de l'adjectif, accord des participes, subjonctif,
  emploi des articles, pronoms COD/COI, passé composé vs
  imparfait), avec stratégies de remédiation par niveau.
- `baremes_evaluation.qmd` — barèmes BW complets : Notenschlüssel
  Klassenarbeit par niveau ; structure de l'Erwartungshorizont
  Abitur ; pondération Inhalt/Sprache pour Basisfach et
  Leistungsfach.

# PAGE REMERCIEMENTS

`remerciements.qmd` dédiée, ordonnée :

1. **Didactique et pédagogie** — sources *former la formatrice*
   (CECRL Volume complémentaire 2020, Christian Puren, Jean-Pierre
   Cuq, Jean-Claude Beacco, Jean-Marc Defays, Évelyne Bérard pour
   l'approche communicative, Robert Galisson).
2. **Profondeur de contenu** — sources de textes authentiques
   (RFI Apprendre le français, TV5Monde Apprendre, France Culture,
   Le Monde, Libération, Médiapart, Le Soir Belgique, Le Devoir
   Québec, Jeune Afrique, Project Gutenberg pour la littérature,
   BNF Gallica pour les œuvres du domaine public).
3. **Outillage** — Quarto, Pandoc, Reveal.js, icônes Lucide,
   Source Sans 3 et JetBrains Mono.
4. **Inspiration structurelle** — à la fin.
5. **Personnel** — collègues et élèves (générique ; pas de noms
   sauf indication contraire).
6. **Licence** — MIT pour le code ; CC-BY-SA 4.0 pour le contenu
   pédagogique.

Chaque entrée pointe vers une URL réelle. Pas de name-drops
génériques.

# PAGE IMPRESSUM (`impressum.qmd`)

La loi allemande (TMG § 5, devenu DDG § 5 depuis 2024) impose un
Impressum légalement conforme sur tout site web qui n'est pas
purement privé. Le site curriculaire d'une enseignante compte
comme « geschäftsmäßig » — donc l'Impressum est **obligatoire**,
pas optionnel. Le RGPD impose en plus une
Datenschutzerklärung séparée.

**L'Impressum et la Datenschutzerklärung sont rédigés en allemand**
(c'est le droit allemand qui s'applique, et c'est la langue dans
laquelle les autorités attendent le texte). Le reste du site est
en français.

## Structure de `impressum.qmd` (squelette verbatim)

Créer la page avec des champs placeholder que l'auteure DOIT
remplir avant la mise en ligne. Chaque placeholder est entouré
d'un bloc `::: {.callout-warning}` visible intitulé
« ACTION ERFORDERLICH » pour que rien ne parte avec un `<TODO>`.

```markdown
---
title: "Impressum"
lang: de
---

## Angaben gemäß § 5 DDG

**S. Le Boulanger**
<TODO: Anschrift — Straße, Hausnummer>
<TODO: PLZ, Ort>
Deutschland

## Kontakt

E-Mail: <TODO: kontakt@domain.tld>

## Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV

S. Le Boulanger
<TODO: gleiche Anschrift wie oben>

## Haftungsausschluss

**Haftung für Inhalte.** Als Diensteanbieterin bin ich gemäß § 7
Abs. 1 DDG für eigene Inhalte auf diesen Seiten nach den allgemeinen
Gesetzen verantwortlich. Nach §§ 8 bis 10 DDG bin ich als
Diensteanbieterin jedoch nicht verpflichtet, übermittelte oder
gespeicherte fremde Informationen zu überwachen oder nach Umständen
zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen.

**Haftung für Links.** Diese Website enthält Links zu externen
Websites Dritter, auf deren Inhalte ich keinen Einfluss habe. Für
die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter
oder Betreiber der Seiten verantwortlich.

## Urheberrecht

Die durch S. Le Boulanger erstellten Inhalte und Werke auf diesen
Seiten unterliegen dem deutschen Urheberrecht. Der Lehrinhalt
(Texte, Aufgaben, Prüfungsbeispiele) steht unter der Lizenz
**CC-BY-SA 4.0**. Der zugrundeliegende Website-Code steht unter der
**MIT-Lizenz**. Zitate Dritter bleiben Eigentum der jeweiligen
Rechteinhaber.

## Schulrechtlicher Hinweis

Diese Materialien sind eine persönliche didaktische Sammlung der
Autorin und stehen in keinem offiziellen Zusammenhang mit einer
Schule, dem Land Baden-Württemberg oder dem Kultusministerium. Der
Bezug zum Bildungsplan 2016 (Sek I) bzw. Bildungsplan gymnasiale
Oberstufe 2021 für Französisch als zweite Fremdsprache ist
inhaltlich-fachlich, keine offizielle Freigabe.
```

## Structure de `datenschutz.qmd` (squelette verbatim)

GitHub Pages est hébergé aux États-Unis par GitHub Inc. ; les IP
des visiteurs y sont traitées. Cela doit être déclaré.

```markdown
---
title: "Datenschutzerklärung"
lang: de
---

## Verantwortliche Stelle

S. Le Boulanger
<TODO: Anschrift>
E-Mail: <TODO>

## Hosting bei GitHub Pages

Diese Website wird auf GitHub Pages gehostet, einem Dienst der
GitHub Inc., 88 Colin P Kelly Jr St, San Francisco, CA 94107, USA.
Beim Aufruf der Seiten überträgt Ihr Browser technisch notwendige
Daten (IP-Adresse, Datum, Zeit, User-Agent, angefragte URL) an
GitHub. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO
(berechtigtes Interesse an zuverlässiger Auslieferung der Inhalte).
GitHubs Datenschutzerklärung:
<https://docs.github.com/site-policy/privacy-policies/github-privacy-statement>.

## Keine Cookies, kein Tracking

Diese Website setzt keine Cookies, verwendet keine Analyse-Tools
und bindet keine Drittanbieter-Schriftarten, -Videos oder
-Social-Media-Widgets ein.

## Ihre Rechte

Sie haben nach DSGVO das Recht auf Auskunft, Berichtigung, Löschung,
Einschränkung der Verarbeitung, Datenübertragbarkeit und
Widerspruch. Ansprechpartnerin: siehe oben.

## Beschwerderecht

Sie haben das Recht, sich bei einer Aufsichtsbehörde zu beschweren.
Zuständig ist die
Landesbeauftragte für den Datenschutz und die Informationsfreiheit
Baden-Württemberg (LfDI BW).
```

**L'auteure doit faire relire les deux fichiers par une
Datenschutz-beauftragte ou un·e juriste avant la mise en ligne.**
Le scaffold émet le squelette ; il ne constitue pas un conseil
juridique.

# ATTRIBUTION PDF — NOM DE L'AUTEURE SUR CHAQUE TÉLÉCHARGEMENT

Chaque PDF produit par le site (156 PDF d'épreuves + 156 PDF de
fiches d'exercices) doit porter « S. Le Boulanger » à la fois en
métadonnées ET en filigrane visible ou pied de page. C'est non
négociable : les PDF voyagent hors du site et doivent attribuer
l'auteure sur leur face.

## PDF d'épreuves (Quarto + LaTeX)

Implémenter l'attribution dans `_includes/_exam.tex` (l'en-tête
LaTeX que chaque `unit<NN>_<slug>_exam.qmd` récupère) :

```latex
% --- Métadonnées du document ---
\usepackage{hyperref}
\hypersetup{
  pdftitle={Exemple d'épreuve},
  pdfauthor={S. Le Boulanger},
  pdfsubject={FLE BW — Épreuve},
  pdfkeywords={FLE, français, Baden-Württemberg, Bildungsplan, Klassenarbeit, Abitur}
}

% --- Pied de page sur chaque page ---
\usepackage{fancyhdr}
\usepackage{lastpage}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[L]{\small © S. Le Boulanger · FLE BW}
\fancyfoot[C]{\small \thepage\ / \pageref{LastPage}}
\fancyfoot[R]{\small CC-BY-SA 4.0}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0.3pt}

% --- Filigrane diagonal sur chaque page ---
\usepackage{draftwatermark}
\SetWatermarkText{S. Le Boulanger}
\SetWatermarkScale{0.6}
\SetWatermarkLightness{0.92}
\SetWatermarkAngle{55}
```

Tinytex peut nécessiter l'installation de `draftwatermark` ; en cas
d'échec CI, repli sur le paquet `background` ou un simple bloc
`\AddToShipoutPictureBG` avec `\rotatebox{55}{...}` — le script doit
essayer trois stratégies dans l'ordre et échouer bruyamment si les
trois échouent.

## PDF de fiches d'exercices (reportlab)

Mettre à jour `_scripts/make_placeholder_worksheets.py` pour rendre,
sur chaque page placeholder :

- **En-tête** (haut gauche, 9 pt) :
  `« S. Le Boulanger · FLE BW »`.
- **Bloc titre** : titre d'Unité + puce niveau/Klasse.
- **Corps** : « Placeholder — contenu de la fiche à venir. »
- **Pied de page** (centré en bas, 8 pt) :
  `« © S. Le Boulanger · CC-BY-SA 4.0 · Klasse {K} · Niveau {G|M|E} · Unité {N} »`.
- **Filigrane diagonal** (centré, rotation 55°, 48 pt, gris 92 %) :
  `« S. Le Boulanger »`.
- Métadonnées PDF via `canvas.setAuthor("S. Le Boulanger")`,
  `setTitle(...)`, `setSubject("FLE BW — Fiche d'exercices")`.

Quand les vraies fiches remplaceront les placeholders, les mêmes
en-tête / pied / filigrane doivent apparaître. Ajouter un helper
reportlab réutilisable `_scripts/pdf_attribution.py` exposant
`apply_attribution(canvas, context)` pour que les générateurs de
vraies fiches branchent le même traitement sans duplication.

## Porte d'audit en CI

Ajouter une étape de vérification dans le workflow, après la
génération des PDF :

```bash
# Chaque PDF doit déclarer S. Le Boulanger comme auteure en métadonnées.
python -c "
import sys, pathlib
from pypdf import PdfReader
bad = []
pdfs = list(pathlib.Path('docs/downloads').rglob('*.pdf'))
for p in pdfs:
    r = PdfReader(str(p))
    author = (r.metadata or {}).get('/Author', '')
    if 'Le Boulanger' not in author:
        bad.append(str(p))
if bad:
    print('ATTRIBUTION MANQUANTE :', *bad, sep='\n')
    sys.exit(1)
print(f'Tous les {len(pdfs)} PDF sont attribués à S. Le Boulanger.')
"
```

Installer `pypdf` aux côtés de `reportlab` dans l'étape pip de la
CI. Si ce contrôle échoue, le déploiement ne se poursuit pas.

# CI (`.github/workflows/publish.yml`)

Utiliser les **actions officielles GitHub Pages**, PAS
`peaceiris/actions-gh-pages`. La Source de Pages doit être réglée
sur « GitHub Actions » dans le dépôt. Pas de R. Python uniquement
pour le petit helper de rendu Bildungsplan et le générateur de
placeholder worksheets.

```yaml
name: Rendu et déploiement
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
        with:
          tinytex: true
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install pyyaml pandas jupyter reportlab pypdf
      - uses: actions/cache@v4
        with:
          path: _freeze
          key: ${{ runner.os }}-quarto-freeze-${{ hashFiles('**/*.qmd') }}
          restore-keys: ${{ runner.os }}-quarto-freeze-
      - name: Génération des PDF de fiches d'exercices placeholder
        run: python _scripts/make_placeholder_worksheets.py
      - name: Rendu du site (Unités HTML + Reveal.js + PDF d'épreuves)
        run: quarto render
      - name: Placement des PDF d'épreuves aux chemins canoniques
        run: bash _scripts/organise_downloads.sh
      - name: Vérification de la présence de tous les PDF
        run: |
          EXAMS=$(find docs/downloads -name "*_exam.pdf" | wc -l)
          WORKS=$(find docs/downloads -name "*_worksheet.pdf" | wc -l)
          echo "PDF d'épreuves : $EXAMS (attendu 156)"
          echo "PDF de fiches : $WORKS (attendu 156)"
          test "$EXAMS" -eq 156
          test "$WORKS" -eq 156
      - name: Vérification que chaque PDF attribue S. Le Boulanger
        run: |
          python -c "
          import sys, pathlib
          from pypdf import PdfReader
          bad = []
          pdfs = list(pathlib.Path('docs/downloads').rglob('*.pdf'))
          for p in pdfs:
              r = PdfReader(str(p))
              author = (r.metadata or {}).get('/Author', '')
              if 'Le Boulanger' not in author:
                  bad.append(str(p))
          if bad:
              print('ATTRIBUTION MANQUANTE :', *bad, sep='\n')
              sys.exit(1)
          print(f'Tous les {len(pdfs)} PDF sont attribués à S. Le Boulanger.')
          "
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

# STRATÉGIE DE GÉNÉRATION DE CONTENU — PAR ÉTAPES, INCRÉMENTALE, REPRENABLE

Ce curriculum fait 156 Unités × 350 lignes ≈ 55 000 lignes de prose
pédagogique originale. Tenter de le générer en une passe échouera :
le contexte débordera, la qualité se dégradera en milieu de cours,
les erreurs s'accumuleront silencieusement et un seul échec de
rendu fera perdre des heures.

Générer le site en **sept phases strictement ordonnées**. Chaque
phase produit un jalon committable. Après chaque phase, s'arrêter,
valider, commiter avant de poursuivre. Une humaine peut reprendre
à n'importe quelle limite de phase sans perdre de travail.

## Phase 0 — Préflight (une session, ~15 min)

**Objectif :** confirmer la portée, récupérer les sources
autoritatives, figer les conventions.

1. Poser les trois questions de contexte (coordonnées GitHub,
   permission pour la distribution de personnages, licence). Si la
   Gesamtschule démarre le français dès Kl. 5 en profil langues,
   demander confirmation. Attendre les réponses.
2. Récupérer chaque page pertinente de `bildungsplaene-bw.de` pour
   Französisch als 2. Fremdsprache : Sek I niveaux G, M, E (Kl.
   6–10) et Oberstufe 2021 (Basisfach + Leistungsfach). Si une
   récupération échoue, STOP et signaler. Ne pas inventer.
3. Parser chaque page récupérée en YAML et écrire dans
   `_resources/bildungsplan_bw_<track>_kl<NN>.yml`. Chaque fichier
   liste les prozessbezogene et inhaltsbezogene Kompetenzen avec
   les codes verbatim et les libellés allemands.
4. Commit : `chore(preflight): BW Bildungsplan Ressourcen erfasst`.

**Critère de sortie :** 13 fichiers YAML existent, chacun non
vide, chacun correspond à une URL live citée en en-tête du fichier.

## Phase 1 — Scaffold (une session, ~30 min)

**Objectif :** un site vide déployable.

1. Émettre le scaffold de haut niveau (configs, styles, CI,
   extensions, scripts).
2. Émettre les 13 dossiers de cours vides avec `index.qmd` stub,
   `calendrier.qmd` et `units/_metadata.yml`.
3. Émettre les 5 annexes comme stubs (titre + un paragraphe
   `TODO`).
4. Émettre les pages de haut niveau (`index.qmd`, `a_propos.qmd`,
   `demarrer.qmd`, `calendrier.qmd`, `references.qmd`,
   `remerciements.qmd`, `bildungsplan.qmd`, `impressum.qmd`,
   `datenschutz.qmd`) avec du contenu réel, car elles ne
   dépendent pas de la sortie des Unités. L'Impressum et la
   Datenschutzerklärung sont livrées avec des placeholders `<TODO>`
   explicites pour l'adresse + l'e-mail de contact, entourés de
   `::: {.callout-warning title="ACTION ERFORDERLICH"}` pour que
   l'auteure ne puisse pas oublier de les remplir avant la mise en
   ligne.
5. Lancer `quarto render` localement. Corriger les erreurs.
   Pousser. Confirmer que le déploiement GitHub Pages réussit avec
   le squelette vide.
6. Commit : `feat(scaffold): déployable squelette vide`.

**Critère de sortie :** URL live résout ; nav fonctionne ; bouton
clair/sombre fonctionne ; aucun 404 dans la nav.

## Phase 2 — Plan thématique (une session, ~45 min)

**Objectif :** la carte complète 13×12 des titres d'Unités et
ancrages Kompetenz.

1. Générer un YAML consolidé à `_resources/curriculum_outline.yml`
   listant, pour chacun des 13 cours, les 12 Unités avec :
   - `unit_nr`, `slug`, `title`
   - `skills_focus` (depuis les catégories Bildungsplan)
   - `bildungsplan` (codes verbatim depuis le YAML de ressource
     du cours)
   - `theme_arc_position` (1 sur 12, utilisé pour l'ajustement à
     l'âge)
   - `exam_type` (`klassenarbeit` ou `abitur_bf` ou `abitur_lf`)
   - `francophone_anchor` (France / Belgique / Suisse / Québec /
     Maghreb / Afrique / Océan Indien) — pour équilibrer la
     représentation de la francophonie plurielle.
2. Rendre ce YAML en un grand tableau unique et le présenter.
   **Attendre mon feu vert.** Itérer selon mes retours.
3. Commit : `feat(outline): carte curriculaire 156-Unités validée`.

**Critère de sortie :** l'outline YAML existe, l'utilisateur l'a
approuvé, chaque Kompetenz du YAML Bildungsplan de chaque cours
apparaît dans le champ `bildungsplan` d'au moins une Unité (contrôle
de couverture), et les ancrages francophones sont répartis (pas plus
de 60 % France métropolitaine par cours).

## Phase 3 — Prototyper un cours de bout en bout (une session, ~2 h)

**Objectif :** dérisquer le modèle d'Unité avant de passer à
l'échelle.

1. Choisir UN cours comme prototype : **Parcours G+M, Klasse 8**.
   C'est la 3e année de français pour les élèves, au milieu de la
   courbe de difficulté — ni bébé-Kl.6-débutants-complets, ni
   Abitur-Kl.13 — et cela fera apparaître la plupart des problèmes
   structurels.
2. Rédiger les 12 Unités ET les 12 fichiers wrapper d'épreuves de
   ce cours unique, en séquence, une Unité par tour de modèle. Ne
   pas paralléliser pour l'instant.
3. Lancer `python _scripts/make_placeholder_worksheets.py` pour ce
   cours uniquement (ajouter un flag `--course track_gm_kl08` au
   script).
4. Rendre localement. Confirmer :
   - Les 12 articles d'Unités rendus en HTML.
   - Les 12 jeux de diapositives Reveal.js rendus.
   - Les 12 PDF d'épreuves rendus, filigrane visible.
   - Les 12 PDF placeholder de fiches existent, attribués.
   - Le shortcode `{{< downloads >}}` produit des liens
     fonctionnels aux deux positions sur chaque Unité.
   - Le champ d'alignement Bildungsplan correspond au YAML du
     cours.
5. Commit : `feat(kl08-gm): cours prototype complet`.

**Critère de sortie :** 48 fichiers déployables ; humaine a
examiné au moins trois Unités et le contenu correspond à
l'intention du prompt.

## Phase 4 — Déploiement parallèle sur les cours (multi-sessions)

**Objectif :** les 12 cours restants, 144 Unités.

Invoquer **un sous-agent par cours**. Chaque sous-agent reçoit :

- L'outline de curriculum approuvé pour son cours.
- Le YAML Bildungsplan du cours.
- Le cours prototype (Kl. 8 G+M) comme exemple canonique.
- Le bloc d'instructions complet (modèle, front matter,
  téléchargements, voix narrative pour sa Klassenstufe, format
  d'épreuve, ancrage francophone).
- Interdictions explicites (pas de paraphrase de manuels, pas de
  codes Bildungsplan inventés, pas de R, pas d'imagerie sous
  droits d'auteur, pas d'imagerie centrée uniquement sur Paris).

**Batching.** Ne pas lancer les 12 d'un coup. Par lots de 3 :

- **Lot A :** Kl. 6 G+M, Kl. 6 E, Kl. 7 G+M.
- **Lot B :** Kl. 7 E, Kl. 9 G+M, Kl. 9 E.
- **Lot C :** Kl. 10 G+M, Kl. 10 E, Kl. 11 E.
- **Lot D :** Kl. 12 E, Kl. 13 E. (Abitur = enjeux maximaux.)

Après chaque lot, commiter, rendre, vérifier les décomptes,
corriger tout problème systémique avant de poursuivre.

**Gestion d'échec.** Si un sous-agent produit moins de 12 Unités,
ou si une Unité échoue à la validation (front matter manquant,
codes Bildungsplan absents, erreurs de rendu), REJOUER ce seul
cours, en passant au sous-agent la liste des Unités manquantes ou
cassées. Ne jamais rejouer un lot entier pour un échec partiel.

**Reprise.** Maintenir un fichier `_resources/generation_log.yml`
mis à jour après la fin de chaque cours, listant `course_id`,
`units_written`, `units_verified`, `commit_sha`. Une relance lit ce
fichier et saute les cours déjà complets.

**Critère de sortie :** 156 fichiers `.qmd` d'Unités, 156 fichiers
wrapper d'épreuves, rendu complet passe en CI avec tous les PDF
présents et attribués (312 PDF au total).

## Phase 5 — Polish transversal (une session, ~1 h)

**Objectif :** ce qu'on ne peut vérifier qu'une fois toutes les
Unités existantes.

1. **Liens de première occurrence du glossaire.** Parcourir chaque
   Unité, repérer la première apparition de chaque terme du
   glossaire, insérer des ancres retour vers `glossaire.qmd`.
2. **Feuilles de l'arbre des compétences.** Peupler l'arbre
   mermaid dans `appendices/arbre_competences.qmd` avec des liens
   directs vers les Unités qui exemplifient le mieux chaque
   cellule compétence-par-niveau.
3. **Page calendrier.** Régénérer `calendrier.qmd` depuis l'outline
   YAML — un seul tableau triable des 156 Unités avec parcours,
   classe, niveau, numéro d'Unité, titre, compétences, type
   d'épreuve, ancrage francophone, et lien profond.
4. **Matrice de couverture Bildungsplan.** Vérifier que chaque
   code de chaque YAML Bildungsplan est référencé par au moins une
   Unité. Signaler les orphelins.
5. **Cohérence de la distribution récurrente.** Par Klassenstufe,
   confirmer que la distribution nommée apparaît dans ≥ 4 Unités.
   Signaler les manques.
6. **Équilibre francophone.** Par cours, confirmer qu'au moins 30
   % des Unités ancrent leur contexte hors de France
   métropolitaine. Signaler les cours trop Paris-centrés.
7. Commit : `feat(polish): liens transversaux + cohérence`.

**Critère de sortie :** matrice de couverture 100 % ; aucun lien
interne cassé ; page calendrier rendue ; équilibre francophone
respecté.

## Phase 6 — Rendu final, déploiement, passation (une session, ~30 min)

1. Lancer la CI complète localement si possible (`act` ou venv
   propre).
2. Pousser. Surveiller Actions. Corriger les échecs CI-uniquement
   (souvent encodage LaTeX sur caractères inhabituels dans textes
   littéraires de l'Oberstufe — accents en contexte UTF-8 exotique,
   apostrophes courbes, guillemets français « »).
3. Visiter 10 URL d'Unités échantillonnées aléatoirement et
   confirmer :
   - Les quatre liens de téléchargement se résolvent tous.
   - Le jeu de diapositives s'ouvre.
   - Le PDF d'épreuve s'ouvre, propre, filigrane visible.
   - Le PDF de fiche s'ouvre (placeholder OK), attribué.
4. Produire un HANDOVER.md récapitulant :
   - décomptes de fichiers par parcours et Klassenstufe
   - matrice de couverture Bildungsplan
   - répartition francophone (pourcentage de chaque zone)
   - liste des fiches d'exercices placeholder à remplacer
   - toute Kompetenz non encore mappée
   - **LÉGAL — remplir l'adresse + contact Impressum, faire
     relire la Datenschutzerklärung par une
     Datenschutz-beauftragte ou un·e juriste AVANT la mise en
     ligne publique**
   - prochaines étapes pour l'auteure (contenu réel des fiches,
     vraie photo d'auteure, passe de relecture par cours)
5. Commit : `docs(handover): génération terminée`.

**Critère de sortie :** site live avec les 156 Unités fonctionnelles,
CI verte, HANDOVER.md existe.

## Principes opérationnels transversaux

- **Un commit par jalon significatif.** Ne jamais mélanger
  changements de scaffold et de contenu. Le log git doit se lire
  comme un plan de cours.
- **Jamais de saut silencieux.** Si une Unité ne peut pas être
  rédigée (données Bildungsplan manquantes, entrée d'outline
  ambiguë), écrire le fichier `.qmd` avec un bloc
  `::: {.callout-important}` TODO visible et l'enregistrer dans
  `generation_log.yml`. Ne pas produire de fichier vide et
  continuer.
- **Préserver le freeze.** Garder le répertoire `_freeze/` de
  Quarto entre les phases — régénérer des Unités inchangées fait
  perdre des heures.
- **Pas d'héroïsme.** Si une seule Unité demande plus d'un tour de
  modèle pour être bien rédigée, s'arrêter et demander. Une
  mauvaise Unité coûte plus cher qu'une session en pause.
- **La voix de l'auteure d'abord.** S. Le Boulanger est l'auteure
  unique — des deux sites jumeaux, EFL et FLE. Chaque Unité doit
  se lire comme écrite par la même enseignante. Pas de dérive
  stylistique entre sous-agents — l'Unité prototype est la
  référence de style.
- **Équilibre francophone permanent.** Chaque sous-agent doit
  vérifier l'ancrage géographique de ses 12 Unités avant rendu.
  Paris-centrisme = refus et réécriture.

# ORDRE D'EXÉCUTION

Suivre les sept phases définies dans **STRATÉGIE DE GÉNÉRATION DE
CONTENU** ci-dessus, dans l'ordre, sans sauter de limite de phase.
Chaque phase se termine par un commit et une porte de validation.
Ne pas commencer la phase N+1 tant que le critère de sortie de la
phase N n'est pas satisfait.

Index rapide :

- **Phase 0 — Préflight :** questions de contexte, récupération
  Bildungsplan.
- **Phase 1 — Scaffold :** squelette vide déployable.
- **Phase 2 — Outline :** carte 13×12 des Unités, validée
  utilisateur.
- **Phase 3 — Prototype :** Kl. 8 G+M de bout en bout comme
  référence de style.
- **Phase 4 — Déploiement :** 12 cours restants en lots de 3.
- **Phase 5 — Polish :** liens glossaire, matrice de couverture,
  calendrier, équilibre francophone.
- **Phase 6 — Passation :** rendu final, déploiement, HANDOVER.md.

# ARRÊT DUR

Ne PAS paraphraser, réécrire ou inventer de contenu Bildungsplan.
Si une page source BW ne peut être récupérée, s'arrêter et
signaler. Ne PAS utiliser de mèmes, photographies ou matériel de
manuel sous droits d'auteur. Ne PAS utiliser
`peaceiris/actions-gh-pages`. Ne PAS commiter sans un
`quarto render` local au préalable si disponible. Ne PAS créer de
pull request sauf demande explicite. Ne PAS ajouter de code R ou
d'outillage adjacent au R ; ce site curriculaire est sans code. Ne
PAS centrer le contenu exclusivement sur Paris : la francophonie
est plurielle et le curriculum BW l'exige.
