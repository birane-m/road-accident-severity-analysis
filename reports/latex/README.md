# Rapport BAAC - Sources LaTeX

Le rapport comprend une couverture, un résumé, un sommaire automatique, une
introduction générale et deux grandes parties :

1. Compréhension, préparation et analyse des données BAAC, en cinq chapitres.
2. Modélisation probabiliste et évaluation prédictive, en trois chapitres.

Il se termine par une conclusion générale, un glossaire, les références et deux
annexes. Il intègre 18 graphiques des notebooks 04 à 07, un schéma relationnel
dessiné en LaTeX et 17 tableaux générés depuis les résultats agrégés.

## Organisation

- `main.tex` : ordre des pages et des chapitres.
- `preambule.tex` : packages, couleurs, titres et informations de couverture.
- `page_de_garde.tex` : mise en page de la couverture.
- `chapitres/00_resume.tex` et `01_introduction.tex` : résumé et introduction.
- `chapitres/02_cadrage.tex` à `06_statistiques.tex` : première partie.
- `chapitres/07_protocole_ml.tex` à `09_evaluation_ml.tex` : seconde partie.
- `chapitres/10_conclusion.tex` : conclusion générale.
- `glossaire.tex` : définitions des principaux termes.
- `references.tex` : sources documentaires et méthodologiques.
- `annexes/` : reproduction et repères de variables.
- `tableaux/` : tableaux LaTeX générés, déjà disponibles pour compiler.
- `scripts/generer_tableaux.py` : génération des 17 tableaux avec la bibliothèque standard Python.
- `resultats/` : résultats agrégés, configurations et provenance des chiffres.
- `figures/` : graphiques et photographie de couverture créditée au journal DNA.
- `documents/description_baac_2005_2024.pdf` : documentation ONISR.

## Compilation

Prérequis : Python 3 pour régénérer les tableaux, et une distribution LaTeX avec
pdfLaTeX, les fontes Latin Modern, le français de Babel et les packages courants
utilisés dans `preambule.tex`, dont TikZ, titlesec, booktabs, tabularx et hyperref.

Depuis le dossier contenant `main.tex` :

```bash
python3 scripts/generer_tableaux.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

On peut aussi utiliser `latexmk -pdf main.tex` si latexmk est installé.
Le glossaire est rédigé directement en LaTeX : il n'exige pas de commande
`makeglossaries`. Les tableaux étant livrés, Python n'est pas nécessaire pour
une simple modification du texte suivie d'une compilation.

Dans Overleaf, importer l'archive, sélectionner `main.tex` comme document principal
et choisir pdfLaTeX. Les sources peuvent être placées dans `reports/latex/` du projet,
en conservant leurs sous-dossiers. Le PDF final peut être rangé dans `reports/`.

## Chiffres et reproduction

Les chiffres et graphiques sont ceux des résultats fournis et vérifiés le
17 octobre 2026. Les scores ML publiés proviennent des exports du projet sous
Python 3.12.3. La revue d'exécution sous Python 3.12.14 et les faibles variations
numériques sont documentées dans `resultats/environnement_revue.json` et l'annexe A.

Le script de tableaux ne réexécute pas les analyses. Les données individuelles
volumineuses ne sont pas incluses dans cette archive de rédaction. Pour reconstruire
l'étude complète, utiliser les sept notebooks du projet et les 24 CSV sources.
