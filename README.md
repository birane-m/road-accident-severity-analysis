# Accidents de la route : comprendre et modéliser leur gravité

Projet personnel de data science consacré aux accidents corporels de la route
en **France métropolitaine, Corse comprise**, à partir des données BAAC de **2019 à 2024**.

L'objectif est de comprendre les différences de gravité entre les usagers,
de quantifier certains écarts et d'évaluer ce qu'une régression logistique
permet d'estimer sur une année ultérieure.

[Consulter le rapport complet](reports/BAAC_rapport.pdf) · [Sources LaTeX](reports/latex/)

## Question étudiée

**Quelles caractéristiques sont associées au décès ou à l'hospitalisation des
usagers impliqués dans un accident, et dans quelle mesure permettent-elles
d'estimer cette issue ?**

Une observation correspond à **un usager dans un accident**. Une même personne
ne peut pas être suivie d'un accident à l'autre dans ces données.

La cible est définie ainsi :

| Valeur | Gravité enregistrée |
| --- | --- |
| 1 | Usager tué ou blessé hospitalisé |
| 0 | Usager indemne ou blessé léger |

Les gravités inconnues sont conservées dans les données préparées, puis exclues
de la modélisation supervisée. L'étude porte sur la gravité parmi les usagers
déjà impliqués dans un accident corporel enregistré. Elle ne mesure pas le
risque d'avoir un accident par trajet.

## Démarche

Le projet suit trois étapes : contrôler et préparer les données, explorer les
différences de gravité, puis évaluer un modèle simple avec un découpage temporel.

| Période | Utilisation |
| --- | --- |
| 2019-2022 | Exploration, analyses statistiques et apprentissage du modèle |
| 2023 | Validation et choix de la régularisation de la régression logistique |
| 2024 | Évaluation finale de la configuration retenue |

La référence de comparaison attribue à chaque usager la fréquence de décès ou
d'hospitalisation observée dans l'apprentissage. La régression logistique utilise
onze variables décrivant l'usager, le véhicule et les circonstances de l'accident.
Après la sélection sur 2023, le modèle reste entraîné sur 2019-2022 pour le test de 2024.

## Parcours des notebooks

Les notebooks se lisent et s'exécutent dans cet ordre. Chacun recharge ses entrées
et peut être lancé depuis un noyau neuf.

| Notebook | Travail réalisé | Principales sorties |
| --- | --- | --- |
| [01 - Découverte](notebooks/01_data_discovery.ipynb) | Comprendre les quatre tables de 2024 et leurs relations | Premiers constats et tableaux de contrôle |
| [02 - Audit](notebooks/02_schema_consistency_2019_2024.ipynb) | Examiner les schémas, identifiants et anomalies de 2019 à 2024 | Règles à appliquer pendant la préparation |
| [03 - Préparation](notebooks/03_data_preparation.ipynb) | Harmoniser, nettoyer et joindre les tables sans multiplier les usagers | Données préparées, schéma, manifeste et six bilans |
| [04 - Exploration](notebooks/04_exploratory_data_analysis.ipynb) | Décrire la population et les différences de gravité sur 2019-2022 | Tableaux descriptifs et huit graphiques |
| [05 - Statistique](notebooks/05_statistical_probability_analysis.ipynb) | Quantifier les écarts et leur variabilité par bootstrap d'accidents | Contrastes, intervalles, diagnostics et quatre graphiques |
| [06 - Modélisation](notebooks/06_logistic_regression.ipynb) | Comparer la référence constante à la régression logistique sur 2023 | Scores de validation, configuration retenue et trois graphiques |
| [07 - Évaluation](notebooks/07_final_evaluation.ipynb) | Évaluer la configuration retenue sur 2024 | Scores de test, analyse des erreurs et trois graphiques |

## Organisation du projet

| Emplacement | Contenu |
| --- | --- |
| `data/raw/<année>/` | Les quatre CSV sources de chaque année |
| `data/processed/` | Données préparées, schéma, manifeste et bilans de préparation |
| `notebooks/` | Les sept notebooks avec leurs explications et conclusions |
| `src/baac_ml.py` | Fonctions et règles de représentation des variables, partagées par les notebooks 06 et 07 |
| `scripts/rename_files.py` | Harmonisation des noms des fichiers téléchargés, si nécessaire |
| `reports/figures/` | Graphiques exportés par les notebooks 04 à 07 |
| `reports/tables/` | Tableaux, scores, configurations et métadonnées |
| `reports/BAAC_rapport.pdf` | Rapport final de l'étude |
| `reports/latex/` | Sources LaTeX du rapport, figures, tableaux et guide de compilation |
| `docs/BAAC_cahier_des_charges.md` | Objectifs, périmètre et décisions méthodologiques |
| `docs/references/` | Documentation des données BAAC |
| `requirements.txt` | Bibliothèques directement utilisées et versions retenues |
| `Makefile` | Installation et suppression de l'environnement virtuel |

Les figures et tableaux sont répartis dans les sous-dossiers `04_exploration`,
`05_statistics`, `06_modeling` et `07_evaluation`.
Voir aussi [l'organisation détaillée](docs/organisation.md)
et [le guide des résultats](reports/README.md).

## Installation

Prérequis : **Python 3.12**, GNU Make et un accès au dépôt de paquets Python.
Les commandes ci-dessous sont prévues pour Linux ou macOS et se lancent depuis
la racine du projet.

```bash
make install
```

Cette commande crée `.venv` et installe les bibliothèques de `requirements.txt`
avec leurs dépendances. Elle utilise directement le Python de cet environnement ;
il n'est pas nécessaire d'activer le venv avant l'installation.

Pour ouvrir JupyterLab :

```bash
.venv/bin/python -m jupyter lab
```

On peut également activer l'environnement dans le terminal :

```bash
source .venv/bin/activate
python -m jupyter lab
```

Pour supprimer l'environnement, puis le recréer :

```bash
make clean
make install
```

Si le venv est activé dans le terminal, lancer `deactivate` avant de le supprimer.
**`make clean` supprime uniquement `.venv`** : les données, notebooks et résultats
sont conservés. Après la réinstallation, réactiver le venv si nécessaire et
redémarrer les noyaux Jupyter qui utilisaient l'ancien environnement.

Pour choisir explicitement l'interpréteur :

```bash
make install PYTHON=python3.12
```

Sans Make, l'installation reste possible :

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Données et exécution

Source : [bases annuelles BAAC sur data.gouv.fr](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024).
La documentation utilisée est conservée dans [docs/references](docs/references/).

Pour chaque année de 2019 à 2024, placer les quatre fichiers suivants dans
`data/raw/<année>/` : `caracteristiques.csv`, `lieux.csv`, `vehicules.csv` et
`usagers.csv`. Si les noms téléchargés diffèrent, le script de renommage peut
être exécuté depuis la racine du projet :

```bash
.venv/bin/python scripts/rename_files.py
```

Le Makefile installe l'environnement. Le téléchargement des données et
l'exécution des notebooks restent des étapes distinctes.

Dans JupyterLab, sélectionner le noyau Python du `.venv`, puis exécuter les
notebooks dans l'ordre, chacun depuis un noyau neuf. Les notebooks 01 à 03
utilisent les fichiers sources. Les notebooks 04 à 07 utilisent les données
préparées par le 03. Le 07 lit également la configuration produite par le 06 :

```text
reports/tables/06_modeling/06_configuration_retenue.json
```

Le notebook 07 vérifie les empreintes des entrées et reconstruit les scores de
validation avant de calculer ceux de 2024. Un écart de provenance doit être
examiné avant de poursuivre.

Les fichiers `.csv.gz` sont lisibles directement avec pandas, sans décompression
manuelle. Les données préparées comprennent **702 823 observations d'usagers
pour 309 756 accidents distincts**. Les bilans permettent de suivre les filtres,
les jointures et les valeurs rendues manquantes.

Les données brutes et les grandes tables préparées sont exclues des nouveaux
ajouts Git par `.gitignore`. Elles doivent donc être récupérées ou reconstruites
sur une autre machine. Les schémas, bilans, tableaux et graphiques restent versionnables.

## Principaux résultats

Sur les usagers dont la cible est connue en 2024 :

| Indicateur | Référence constante | Régression logistique |
| --- | --- | --- |
| Log-loss | 0,4703 | 0,4001 |
| Score de Brier | 0,1471 | 0,1268 |

Une valeur plus faible est préférable pour ces deux indicateurs. La régression
logistique améliore donc l'estimation des probabilités par rapport à la référence.
Sa ROC-AUC est d'environ **0,770**, avec des résultats proches de ceux de 2023.

Au seuil illustratif de 0,5, le rappel est toutefois limité à **18,2 %**.
Les notebooks examinent aussi la calibration des probabilités, les différences
entre catégories d'usagers et le rôle des informations manquantes.

## Limites

- Les associations observées ne permettent pas de conclure à un effet causal.
- L'hospitalisation est un indicateur sensible aux conditions de collecte ;
  elle ne constitue pas une définition médicale uniforme des blessures graves.
- La structure de 2024 a été examinée pendant l'audit initial. L'évaluation est
  une étude rétrospective avec séparation chronologique.
- Les scores de 2024 ont été consultés. Cette année ne doit plus servir à choisir
  de nouvelles variantes en la présentant comme un test encore vierge.
- Les résultats ne démontrent pas l'utilité opérationnelle d'un système d'alerte.
  Les performances varient selon les groupes et les probabilités restent
  imparfaitement calibrées.

## Rapport

Le [rapport final](reports/BAAC_rapport.pdf) compte **49 pages** et présente
le travail en deux grandes parties :

1. Compréhension des sources, audit, préparation, exploration et analyse statistique.
2. Modélisation probabiliste, validation sur 2023 et évaluation sur 2024.

Il comprend également une introduction, une conclusion générale, un glossaire,
les références et les annexes de reproduction. Les **18 graphiques** des notebooks
04 à 07 y sont intégrés et commentés.

Les [sources LaTeX](reports/latex/) permettent de modifier le texte, les tableaux
et la mise en page. Le document principal est `reports/latex/main.tex`.
Le [README des sources](reports/latex/README.md) explique la compilation locale
et l'utilisation dans Overleaf.

## État du projet

L'étude est finalisée dans le périmètre retenu : sept notebooks, préparation
contrôlée des données, analyses statistiques, comparaison à une référence
constante et évaluation de la régression logistique. Le rapport est terminé,
avec ses résultats, ses limites et ses sources modifiables.

## Auteur et contact

**Papa Birane Mbengue**, élève ingénieur en informatique à Sup Galilée.

Contact : [papabirane.mbengue@outlook.com](mailto:papabirane.mbengue@outlook.com).
