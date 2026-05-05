# FLE BW — Français Langue Étrangère, Gesamtschule Bade-Wurtemberg

Curriculum FLE pour la Gesamtschule du Bade-Wurtemberg, **Klasse
6 à 13**, aligné sur le Bildungsplan 2016 (Sek I) et le
Bildungsplan gymnasiale Oberstufe 2021. **156 Unités** sur deux
parcours :

- **G+M** (grundlegend + mittel) — Klasse 6 à 10 (5 cours).
- **E** (erweitert / gymnasial) — Klasse 6 à 13 (8 cours).

Auteure : **S. Le Boulanger**. Site live :
<https://boulingua.github.io/fle/>

## Sites sœurs

- **[EFL BW](https://boulingua.github.io/efl/)** — Anglais, Kl. 5–13.
- **FLE BW** — Français, Kl. 6–13 (ce site).
- **[DaF](https://boulingua.github.io/daf/)** — Allemand langue
  étrangère, GER A1–C1.
- **[Ressources](https://boulingua.github.io/ressources/)** — hub
  de ressources curées.

## Architecture

- Bâti avec **[Quarto](https://quarto.org)**.
- Chaque Unité rend **deux fois** depuis une seule source `.qmd` :
  article HTML + diapositives Reveal.js.
- Exemple d'épreuve par Unité (Klassenarbeit Kl. 6–10, Abitur
  Kl. 11–13) en PDF.
- Fiche d'exercices en PDF (placeholder, contenu réel à venir).
- Bascule clair/sombre. Icônes Lucide.

Déploiement via **GitHub Actions** (`actions/deploy-pages@v4`).

## Modèle pédagogique

Cinq étapes : **Activer → Apporter → S'entraîner → Produire →
Réfléchir** (variante préparation-épreuve : *Tâche → Modèle →
Stratégie → Tentative → Retour*).

## Bildungsplan-BW

Le squelette des compétences est dans
`_resources/bildungsplan_bw_franzoesisch.yml`, extrait verbatim
des pages officielles `bildungsplaene-bw.de`. Aucune compétence
n'est inventée ; chaque Unité cite des codes vérifiables.

## Licence

- **MIT** (`LICENSE`) — code du site.
- **CC-BY-SA 4.0** (`LICENSE-content`) — contenu didactique.

`© S. Le Boulanger · MIT / CC-BY-SA 4.0`.

## Citation

Si vous réutilisez ce curriculum, merci de le citer :

> Le Boulanger, S. (2026). *FLE — Curriculum bilingue pour
> l'enseignement secondaire, classes 6 à 13* [Cours en ligne].
> Boulingua. <https://boulingua.github.io/fle/>

```bibtex
@misc{leboulanger2026fle,
  author       = {Le Boulanger, S.},
  title        = {{FLE} --- Curriculum bilingue pour l'enseignement
                  secondaire, classes 6 {\`a} 13},
  year         = {2026},
  howpublished = {\url{https://boulingua.github.io/fle/}},
  note         = {Boulingua. Code sous licence MIT ; contenu sous
                  licence CC-BY-SA 4.0.}
}
```

Voir la page **[Références](https://boulingua.github.io/fle/references.html)**
pour la bibliographie complète et les remerciements.

## Build local

```
quarto render
```

Le CI reproduit le même build et déploie via les actions Pages
officielles.
