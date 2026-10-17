# Résultats de l'étude

Les tableaux, graphiques et métadonnées sont regroupés par étape :

| Sous-dossier | Contenu |
| --- | --- |
| `04_exploration` | Population, gravité et comparaisons descriptives sur 2019-2022 |
| `05_statistics` | Contrastes, intervalles bootstrap, stabilité et sensibilité aux décès seuls |
| `06_modeling` | Comparaison sur 2023, choix de C et configuration arrêtée |
| `07_evaluation` | Évaluation sur 2024 et diagnostics du modèle conservé |

Chaque sous-dossier existe à la fois sous `figures/` et sous `tables/`.
Les fichiers JSON décrivent les choix, les empreintes et l'environnement utilisé.

La configuration à lire pour reconstruire le modèle est
`tables/06_modeling/06_configuration_retenue.json`. Le fichier
`tables/07_evaluation/07_configuration_evaluee.json` est la copie de traçabilité
de la configuration évaluée, pas un nouveau réglage effectué sur le test.

Une ligne de `05_replicats_contrastes.csv.gz` représente un résultat de
rééchantillonnage, pas un usager. Les autres tableaux précisent leurs effectifs
et leur unité dans les notebooks associés.

Les résultats reçus et leurs métadonnées ont été conservés lors de la réorganisation.
La rédaction de la seconde partie du rapport reste un travail de restitution.
