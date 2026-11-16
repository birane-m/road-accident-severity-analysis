# Organisation du projet

Le classement suit le parcours de l'étude : comprendre les sources, préparer
les données, analyser, modéliser puis évaluer. Les notebooks sont numérotés dans
cet ordre et leurs résultats sont regroupés par étape.

## Données

- `data/raw/<année>/` contient les quatre fichiers BAAC sources de chaque année,
  de 2019 à 2024. Ces fichiers sont conservés sans modification.
- `data/processed/` contient les tables préparées par le notebook 03, ainsi que
  le schéma, le manifeste des sources et les bilans de préparation.

Les fichiers `.csv.gz` sont des CSV compressés. Ils peuvent être lus directement
avec pandas, sans décompression manuelle.

## Figures, tableaux et métadonnées

| Étape | Figures | Tableaux et métadonnées |
| --- | --- | --- |
| 04 - Exploration | `reports/figures/04_exploration/` | `reports/tables/04_exploration/` |
| 05 - Statistique | `reports/figures/05_statistics/` | `reports/tables/05_statistics/` |
| 06 - Modélisation et validation | `reports/figures/06_modeling/` | `reports/tables/06_modeling/` |
| 07 - Test final | `reports/figures/07_evaluation/` | `reports/tables/07_evaluation/` |
| 08 - Comparaison | `reports/figures/08_comparaison/` | `reports/tables/08_comparaison/` |

Les préfixes des fichiers indiquent le notebook qui les produit. Chaque notebook
écrit ses exports dans les sous-dossiers de son étape.

Les notebooks 07 et 08 lisent la configuration retenue par le notebook 06 dans
`reports/tables/06_modeling/06_configuration_retenue.json`, puis écrivent leurs propres
résultats dans les dossiers de leur étape. Ils vérifient la provenance des entrées
et reconstruisent les scores de validation avant de calculer ceux du test 2024.

Le notebook 08 enregistre en plus son propre protocole dans
`reports/tables/08_comparaison/08_protocole_arbres.json`, écrit avant le premier
entraînement du modèle d'arbres.

## Code et documentation

Les notebooks contiennent les explications, le code, les contrôles et les
conclusions de chaque étape. Le module `src/baac_ml.py` regroupe les fonctions
et les règles de représentation des variables utilisées dans les notebooks 06
à 08. Ce partage permet d'appliquer les mêmes transformations à la validation,
au test et à la comparaison de modèles.

Le dossier `scripts/` contient les utilitaires, dont `rename_files.py` pour
harmoniser les noms des fichiers téléchargés si nécessaire.

Le README à la racine présente le sujet, les résultats et la procédure
d'installation et d'exécution. Le cahier des charges se trouve dans
`docs/BAAC_cahier_des_charges.md`. La documentation ONISR est conservée dans
`docs/references/`.

## Environnement Python

Un seul fichier, `requirements.txt`, liste les bibliothèques directement
utilisées avec leurs versions. Lors de l'installation, `pip` installe également
leurs dépendances en respectant les contraintes déclarées par ces bibliothèques.

Le `Makefile`, situé à la racine, propose deux commandes :

| Commande | Effet |
| --- | --- |
| `make install` | Crée `.venv` et installe les bibliothèques de `requirements.txt` avec leurs dépendances |
| `make clean` | Supprime uniquement le dossier `.venv` |

Ces commandes se lancent depuis la racine du projet. Le Makefile prépare
l'environnement ; il ne télécharge pas les données et n'exécute pas les notebooks.
Les données, notebooks et résultats sont conservés lors du nettoyage du venv.

Le dossier `.venv`, les caches Python et les fichiers temporaires sont exclus
des nouveaux ajouts Git par `.gitignore`, ainsi que les données brutes et les
grandes tables préparées. La récupération des sources est décrite dans le README.

## Rapport et images de présentation

Les graphiques calculés restent dans `reports/figures/`. Lors de l'intégration du
rapport, ses sources LaTeX et ses images de présentation pourront être regroupées
dans `reports/latex/`, avec le PDF final dans `reports/`.

La photographie de couverture sera conservée avec les sources du rapport et
accompagnée de son crédit. Les sources LaTeX pourront référencer les graphiques
existants pour éviter de les dupliquer dans le dépôt.
