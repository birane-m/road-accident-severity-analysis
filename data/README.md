# Données BAAC

`raw/<année>/` contient les quatre CSV annuels d'origine, de 2019 à 2024.
Ils sont conservés sans modification. Le fichier source, le périmètre et les
empreintes sont documentés dans le cahier des charges et le manifeste du notebook 03.

`processed/` contient deux tables principales :

- `baac_usagers_metropole_2019_2024.csv.gz` : une ligne par usager source métropolitain ;
- `baac_lieux_sources_metropole_2019_2024.csv.gz` : les lieux sources conservés pour la traçabilité.

Le schéma `baac_regles_et_schema.json` indique les types et le marqueur de données
manquantes. Les six bilans décrivent les effectifs, la géographie, les identifiants,
les jointures, les lieux et le nettoyage. Les notebooks reprennent ce schéma lors
de la lecture ; ouvrir le CSV seul dans un tableur ne restitue pas tous ces types.

Les analyses lisent directement les fichiers gzip. Une gravité inconnue est
conservée dans la table puis exclue des tâches supervisées. Les fichiers volumineux
ne sont pas destinés à être ajoutés au dépôt Git ; leurs noms et leur reconstruction
restent documentés. Les petits bilans, le schéma et le manifeste sont versionnables.
