# Projet BAAC : cadrage et cahier des charges

**Version 0.9 · 17 octobre 2026 · Installation simplifiée avec un fichier de dépendances unique**  
**Porteur : Papa Birane Mbengue, dernière année du cycle ingénieur informatique, Sup Galilée**  
**Projet : analyse statistique et modélisation de la gravité des blessures, BAAC France 2019–2024**

Ce document rassemble le cadrage du projet et les décisions prises jusqu'au 17 octobre 2026. Les notebooks 01 à 05 sont réalisés et leur première partie de rapport est rédigée. L'étude prédictive limitée à une référence constante et une régression logistique est maintenant évaluée sur 2024, après sélection sur 2023. Les résultats de modélisation seront présentés dans les notebooks et le rapport ; le cahier des charges conserve les objectifs, les règles et les critères de réussite.

## 1. Finalité du projet

Construire une étude reproductible sur des données publiques réelles, comprendre les choix effectués et disposer d'un projet personnel présentable pour un stage de fin d'études en data science ou ML appliqué.

Le résultat attendu comporte trois dimensions : une table d'analyse fiable, des réponses statistiques argumentées et une évaluation honnête de modèles prédictifs. Birane doit pouvoir expliquer le problème, les données, les choix, les résultats et leurs limites en entretien.

Un résultat négatif ou un modèle complexe qui n'améliore pas une référence simple reste un résultat recevable s'il est correctement analysé. Aucun score minimal arbitraire n'est fixé avant l'étude.

## 2. Problématique et population étudiée

> Quels facteurs sont associés au décès ou à l’hospitalisation des usagers impliqués dans les accidents corporels enregistrés en France métropolitaine entre 2019 et 2024, et dans quelle mesure peut-on estimer la probabilité de cette issue sur une année ultérieure ?

**Unité principale conservée depuis le notebook 01 : l'usager.** Une ligne représente une observation de personne impliquée dans un accident, sans prétendre suivre cette personne entre plusieurs accidents.

BAAC décrit les accidents corporels enregistrés par les forces de l'ordre. Les personnes indemnes du fichier sont impliquées dans ces accidents ; elles ne constituent pas un groupe de trajets sans accident. Les résultats portent donc sur la gravité conditionnellement à l'implication dans un accident enregistré. Estimer le risque d'accident par trajet ou kilomètre demanderait des données d'exposition supplémentaires.

Le modèle envisagé est une étude rétrospective à partir des informations décrivant l'accident. L'instant de disponibilité des variables devra être précisé. Aucune capacité de prédiction avant un trajet ou de décision de secours en temps réel n'est revendiquée.

## 3. Choix établis, propositions et limites de périmètre

| Élément | Position de départ | Statut |
|---|---|---|
| Source | Quatre tables BAAC annuelles : caractéristiques, lieux, véhicules, usagers | Choix utilisateur |
| Période | 2019 à 2024 inclus | Choix utilisateur |
| Unité | Une ligne par usager source | Déjà retenue dans les notebooks |
| Démarche | Comprendre les décisions, progresser par étapes, vérifier chaque résultat | Demande utilisateur |
| Analyse | Exploration et comparaisons de proportions avec bootstrap par accident, stratifié par année | Réalisé dans les notebooks 04 et 05 |
| ML | Comparer la fréquence constante à une régression logistique régularisée | Périmètre réduit convenu les 16 et 17 octobre 2026 ; arbres facultatifs |
| Géographie | France métropolitaine, Corse comprise ; outre-mer exclu du périmètre d’analyse | D1 validée par Birane le 16 octobre 2026 |
| Gravité à modéliser | Quatre catégories pour la description ; cible binaire décès ou hospitalisation pour le premier modèle | D2 validée par Birane le 16 octobre 2026 |
| RO, base SQL, application web, API | Extensions possibles, sans dépendance du socle envers ces éléments | Hors première version |

Les fichiers CSV locaux suffisent pour la première version. Python, pandas, SciPy, scikit-learn et les bibliothèques de visualisation usuelles constituent une base technique adaptée. Les versions réellement utilisées seront enregistrées lors de la mise en place de l'environnement.

## 4. Questions auxquelles répondre

Les questions suivantes forment une liste initiale. Nous retiendrons un petit nombre de comparaisons motivées, plutôt qu'une recherche automatique de toutes les relations possibles.

| Question | Résultat attendu | Précaution |
|---|---|---|
| Q1. Comment les catégories de gravité se répartissent-elles selon l'année, l'âge et la catégorie d'usager ? | Effectifs, dénominateurs, proportions et graphiques commentés | Des effectifs élevés ne signifient pas un risque par trajet élevé |
| Q2. Les proportions de décès ou d'hospitalisations diffèrent-elles selon la lumière, l'agglomération ou le type de véhicule ? | Comparaisons de proportions et taille des écarts | Séparer les piétons des occupants ; examiner les facteurs associés |
| Q3. Comment les comparaisons se traduisent-elles dans un modèle combinant plusieurs caractéristiques ? | Contrastes exploratoires de la régression pénalisée, sans intervalles ni revendication d'inférence causale | Les rapports de cotes ne sont pas les rapports de proportions du notebook 05 |
| Q4. Un modèle entraîné sur les années antérieures conserve-t-il des performances utiles sur 2024 ? | Comparaison à une référence, analyse des erreurs et des probabilités | Validation temporelle ; aucune sélection sur les scores du test final |

**Extension probabiliste facultative :** modéliser des nombres d'accidents par département et période avec une régression de Poisson, puis une alternative si la dispersion le justifie. Cela demande une table agrégée distincte, y compris les périodes sans accident. Cette extension ne doit pas retarder la livraison du projet principal sur la gravité.

## 5. Cible de gravité retenue

La variable `grav` est catégorielle : `1` indemne, `2` tué, `3` blessé hospitalisé, `4` blessé léger. Les codes ne sont pas ordonnés numériquement par gravité ; leur moyenne n'a pas de sens.

**D2 validée par Birane le 16 octobre 2026 :** estimer la probabilité de décès ou d’hospitalisation parmi les usagers impliqués dans un accident corporel enregistré. Coder `y = 1` pour `grav` dans `{2, 3}` et `y = 0` pour `grav` dans `{1, 4}`. Le libellé « décès ou hospitalisation » décrit exactement ce regroupement ; il ne constitue pas une définition médicale des blessures graves.

**Justification du choix :** une issue explicite correspondant à notre question, davantage de cas positifs que les décès seuls pour examiner les sous-populations, et un premier modèle binaire interprétable. Cela ne garantit ni une meilleure performance ni une réduction des biais de collecte. Les quatre catégories restent décrites séparément.

La qualité de cette cible sera examinée par année et sous-population. Le PDF signale une modification de saisie depuis 2018 et l’absence de labellisation de l’indicateur hospitalisé depuis 2019. Une analyse complémentaire « décès uniquement » vérifiera si les principales conclusions changent. Toute révision ultérieure de la cible principale devra être justifiée et consignée avant de comparer les scores correspondants.

Les gravités inconnues sont traitées séparément : ni 0 ni 1 ne leur est attribué par défaut. Sans cible connue, ces observations sont exclues de l’apprentissage et de l’évaluation supervisés ; leur nombre et leur répartition restent décrits par année et population. Elles restent présentes dans la traçabilité des données.

## 6. Préparation des données : exigences

| Exigence | Règle de travail | Preuve attendue |
|---|---|---|
| Traçabilité | Conserver les CSV bruts, la source, la date de récupération disponible et une empreinte des fichiers | Inventaire des 24 CSV et manifeste de données |
| Harmonisation | Renommer `Accident_Id` en 2022 ; lire les identifiants en texte ; traiter les espaces insécables | Journal des transformations et contrôle des collisions |
| Identifiant d'observation | Conserver le numéro de ligne source avant toute transformation ; créer une clé technique pour toutes les années | Clé d'observation unique, y compris sans `id_usager` en 2019–2020 |
| Codes spéciaux | Distinguer non renseigné, sans objet, aucun et modalités non documentées | Dictionnaire de règles par variable ; aucun remplacement global des zéros |
| Jointures | Contrôler les clés accident et véhicule, les correspondances et les cardinalités | Comptages avant/après, contrôle des lignes non appariées et absence de multiplication d'usagers |
| Lieux multiples | Examiner les attributs variables et la multiplicité par année | Règle justifiée avant jointure ; aucun choix arbitraire de première ligne |
| Plausibilité | Examiner dates, âge approximatif et coordonnées | Tableau des alertes et décisions, sans suppression automatique par seuil |
| Exclusions | Rendre chaque filtre explicite et chiffré | Tableau de passage des observations brutes aux observations analysées |

Les piétons sont rattachés au véhicule qui les a heurtés : le type de véhicule ne sera pas interprété comme leur propre moyen de transport. Les informations de sécurité doivent être examinées sur les trois champs `secu1`, `secu2`, `secu3` et selon la catégorie d'usager.

Les doublons exacts d'usagers sans identifiant ne prouvent pas qu'une personne est dupliquée. Les véhicules sans usager ne justifient pas la création d'une gravité fictive. L'écart de 24 véhicules en 2024 est explicitement expliqué dans la documentation ; les autres écarts restent à examiner.

## 7. Analyse statistique et probabiliste

Le volet probabiliste se traduira d'abord par des probabilités conditionnelles de gravité et une régression logistique, qui modélise une probabilité d'événement binaire. Nous introduirons les concepts utiles au moment de les utiliser, avec un exemple issu du projet.

Les tableaux donneront les effectifs et leurs dénominateurs. Les comparaisons rapporteront la taille des écarts, et leur incertitude lorsqu'une interprétation au-delà du fichier observé est recherchée. BAAC n'est pas un échantillon aléatoire simple de tous les déplacements : un intervalle de confiance ne corrige pas les biais d'enregistrement.

**Oui, les corrélations et les associations font partie du travail.** La méthode dépendra du type des variables : Pearson ou Spearman pour des mesures numériques lorsque cela a du sens ; tableaux de contingence et mesure d'association comme le V de Cramér pour des catégories ; comparaison de distributions et de proportions pour les situations mixtes. Aucun calcul de Pearson sur les codes bruts de `grav`, `catv` ou `lum` ne sera présenté comme une relation quantitative interprétable.

Les tests statistiques ne seront utilisés que pour une question précise avec des hypothèses examinées. Si de nombreuses comparaisons sont nécessaires, leur multiplicité sera prise en compte. Les usagers d'un même accident sont dépendants ; un rééchantillonnage destiné à estimer l'incertitude se fera par accident, et ses limites seront expliquées.

Les années seront examinées séparément, notamment 2020–2021. Une évolution de proportions ne sera pas automatiquement attribuée au Covid, à la météo, à une limitation de vitesse ou à toute autre cause.

## 8. Machine learning et protocole d'évaluation

La question retenue est la suivante : les caractéristiques disponibles permettent-elles d'estimer la probabilité de décès ou d'hospitalisation parmi les usagers d'accidents corporels enregistrés, et ces estimations restent-elles valables sur une année ultérieure ? L'intérêt est méthodologique et rétrospectif. Aucun besoin opérationnel suffisamment précis n'est établi pour revendiquer une aide au secours, une prévention individuelle ou une décision d'aménagement.

**D3 :** apprentissage sur 2019-2022, validation sur 2023, test final sur 2024. L'année 2024 a déjà été examinée dans les audits de structure. Ses scores ne servent à sélectionner ni les variables, ni le modèle, ni ses réglages. Un accident reste dans une seule partition. Les gravités inconnues sont comptées puis exclues de l'apprentissage et de l'évaluation.

### 8.1. Variables et représentation

**D6, choix fixés le 17 octobre 2026 avant les comparaisons :** onze variables sources : `age_approx`, `sexe`, `catu`, `catv`, `lum`, `agg`, `int`, `atm`, `mois_accident`, `jour_semaine`, `heure_accident`.

L'âge est représenté par les tranches du notebook 04 : 0-17, 18-24, 25-34, 35-44, 45-54, 55-64, 65-74 et 75 ans ou plus. Les bornes sont fixes, sans optimisation sur 2023. Les autres variables sont catégorielles, y compris mois, jour et heure. Une absence devient la modalité « Non renseigné ». Un encodage one-hot, ajusté sur l'apprentissage dans une pipeline, transforme les modalités en colonnes 0/1. Une modalité de validation jamais vue est comptée et encodée en zéros pour le champ concerné ; elle ne modifie pas l'encodeur.

Sont exclus : gravité et dérivés, identifiants, provenance, année, variantes brutes déjà représentées et indicateurs de qualité. Les champs de lieux sont écartés de ce premier modèle en raison des difficultés de représentation apparues en 2023. Équipements, manœuvres et détails du choc restent hors périmètre ; cette exclusion ne les qualifie pas tous de fuites de cible.

`catv` décrit le véhicule associé à l'usager ; pour un piéton, il s'agit du véhicule qui l'a heurté. L'âge regroupé perd la précision à l'intérieur des tranches. La modalité absente peut capturer des pratiques de renseignement : ces limites seront discutées dans les résultats.

### 8.2. Comparaison et sélection

| Élément | Règle fixée avant les scores |
|---|---|
| Référence | Fréquence de la cible 1 dans les seules données d'apprentissage, identique pour tous les usagers évalués |
| Modèle | Régression logistique avec pénalisation L2 ; pas de pondération ou rééchantillonnage des classes |
| Réglage | Quatre valeurs de C : 0.01, 0.1, 1 et 10 ; autres réglages identiques |
| Critère de sélection | Log-loss minimale sur 2023 ; égalité exacte départagée par le plus petit C |
| Comparaison finale sur validation | Conserver la logistique si sa log-loss est strictement inférieure à celle de la référence ; sinon conserver la référence |
| Compléments | Brier, average precision, ROC-AUC, effectifs et courbe de calibration descriptive |
| Seuil | 0,5 pour illustrer les erreurs ; fixé à l'avance et sans revendication opérationnelle |
| Test final | Configuration arrêtée, même apprentissage 2019-2022, aucun réentraînement sur 2023 avant test |

La log-loss et le score de Brier évaluent les probabilités ; plus petit est meilleur. L'average precision résume la courbe précision-rappel avec sa définition propre, sans être renommée aire trapézoïdale. La ROC-AUC renseigne le classement. Aucun de ces scores n'établit à lui seul une utilité opérationnelle ou une bonne calibration partout. Une non-convergence doit interrompre la comparaison, pas être cachée.

### 8.3. Diagnostics et limites

Les résultats de validation servent au choix de C : ils ne sont pas présentés comme une évaluation finale indépendante. Les diagnostics portent sur les catégories d'usagers, la calibration et les valeurs manquantes. Une analyse de sensibilité réutilise les mêmes prédictions sur les usagers dont l'âge et le sexe sont renseignés, sans réentraînement ni nouvelle sélection. Elle change la population évaluée et ne corrige pas les biais d'absence.

Quatre contrastes de coefficients sont lus avec les mêmes orientations que le notebook 05. Ils donnent des rapports de cotes pénalisés à caractéristiques du modèle maintenues identiques, sans intervalle ni conclusion causale. Les différences de scores sont d'abord descriptives. Aucun intervalle fondé sur l'indépendance des usagers d'un même accident n'est utilisé.

La configuration exportée conserve variables, règles, C retenu, référence, seuil, empreintes des entrées et versions réellement utilisées. Le test 2024 a réutilisé ces choix dans le notebook 07. Les performances et leurs limites sont rapportées sans réoptimisation sur cette année. Un modèle d'arbres, SHAP ou un déploiement ne sont pas nécessaires à la première version.

## 9. Architecture et livrables

| Élément | Responsabilité | État au 17 octobre 2026 |
|---|---|---|
| `data/raw/2019` à `2024` | Conserver les 24 CSV d'origine | Sources utilisées, sans modification |
| Notebook 01 | Découverte des quatre tables de 2024 | Réalisé et revu |
| Notebook 02 | Audit et harmonisation des six années | Réalisé et revu |
| Notebook 03 | Préparation et jointures contrôlées | Réalisé et revu |
| Notebook 04 | Exploration sur l'apprentissage 2019-2022 | Réalisé et revu |
| Notebook 05 | Comparaisons probabilistes et bootstrap par accident | Réalisé et revu |
| Notebook 06 | Référence, logistique et sélection sur 2023 | Réalisé et vérifié sur la validation 2023 |
| Notebook 07 | Test sur 2024, erreurs et limites | Réalisé et vérifié avec la configuration du 06 inchangée |
| `src/baac_ml.py` | Représentation déterministe des onze variables | Ajouté avec le notebook 06 |
| `reports/tables`, `reports/figures` | Résultats agrégés, graphiques et métadonnées classés par étape 04 à 07 | Exports des étapes réalisées, chemins adaptés |
| `docs/` et `docs/references/` | Cahier des charges, organisation et documentation ONISR | Version de cadrage actualisée ; références séparées |
| Rapport LaTeX/PDF | Explications, résultats, références et annexes | Première partie rédigée ; seconde à compléter |
| README et dépendances | Présentation, ordre des notebooks et bibliothèques directement utilisées avec leurs versions dans `requirements.txt` | Documentation actualisée ; installation complète dans l’environnement local à vérifier |
| `Makefile` | Créer `.venv` et installer les dépendances avec `make install` ; supprimer uniquement `.venv` avec `make clean` | Cycle de création, suppression et recréation vérifié avec un fichier de dépendances vide ; installation complète des paquets à vérifier |

Les notebooks présentent les objectifs, le code et ses conclusions. Le petit module ML isole une règle réellement réutilisée, sans imposer une refonte des notebooks 01 à 05. Aucun orchestrateur, base SQL ou déploiement n'est requis pour cette version. Les tests ciblés protègent les règles et séparations importantes ; les versions exécutées sont enregistrées.

## 10. Étapes et critères de passage

| Étape | Travail | Critère de passage |
|---|---|---|
| 0. Cadrer | Problème, unité, questions, cible proposée, périmètre | D1, D2 et D3 validées ; choix consignés avant les étapes dépendantes |
| 1. Comprendre l'audit | Relire les notebooks 01–02 et expliquer les points importants | Birane sait décrire les quatre tables et les risques de jointure |
| 2. Préparer | Nettoyer, traiter les lieux, créer les variables de base | Clé usager unique ; aucune multiplication inexpliquée ; exclusions tracées |
| 3. Analyser | Répondre aux questions descriptives et statistiques | Chaque question retenue a un résultat, une interprétation et une limite |
| 4. Modéliser | Référence et logistique ; validation temporelle | Comparaison équitable ; prétraitements ajustés sans test ; limites exposées |
| 5. Évaluer et expliquer | Erreurs, calibration, segments, interprétation utile | Résultats finaux séparés des réglages ; aucune conclusion causale abusive |
| 6. Livrer | Nettoyage du dépôt, tests, README, synthèse | Reproduction possible depuis un environnement documenté et les CSV |

**Rituel pour chaque étape :** expliquer son objectif, regarder un exemple, comparer les options pertinentes, justifier le choix, implémenter une petite partie, vérifier le résultat et rédiger la conclusion. Nous traitons une étape à la fois, sans générer tous les notebooks restants d'un bloc.

La durée est pilotée par ces résultats vérifiables. La possibilité évoquée hier d'un prototype en une journée n'est pas un engagement de terminer le projet complet aujourd'hui. Une première version peut réduire le nombre de variables et de modèles, mais elle doit conserver les contrôles de données et une évaluation honnête.

## 11. Conditions de réussite et restitution

La version complète est considérée comme livrable lorsque les points suivants sont vérifiés :

- Les sources, la population, la cible et les exclusions sont documentées.
- La table finale possède une clé d'observation unique et des jointures contrôlées.
- Les questions statistiques retenues ont des réponses compréhensibles avec les bons dénominateurs.
- La comparaison ML comporte une référence et un protocole temporel déclaré, même si le gain est faible.
- Les résultats incluent les erreurs, la calibration et les limites liées à la collecte et aux variables.
- Les notebooks s'exécutent dans l'ordre depuis un noyau neuf ; la procédure de reproduction est décrite.
- Le dépôt comprend les scripts/modules utiles, les dépendances, les contrôles ciblés et un README.
- Les données volumineuses et `.venv` ne sont pas ajoutées au dépôt ; leur récupération est expliquée.
- Une synthèse courte présente le problème, la méthode, les principaux résultats et les limites.
- Birane peut expliquer les décisions essentielles sans s'appuyer uniquement sur le code généré.

Le CV présentera un projet « en cours » tant que les livrables annoncés ne sont pas terminés. La formulation finale privilégiera le problème étudié, le travail réalisé et les résultats effectivement obtenus, sans chiffres inventés ni accumulation de termes techniques.

## 12. État du projet et registre des décisions

Les 80 cellules de code des notebooks 01 à 05 ont été réexécutées dans des espaces de variables neufs lors de la revue du 16 octobre. Ce contrôle porte sur l'exécution Python des cellules ; il ne prétend pas avoir utilisé un même environnement logiciel ni un noyau Jupyter pour toutes les exécutions.

La table préparée comprend 702 823 usagers métropolitains et 309 756 accidents distincts, avec 365 gravités inconnues conservées. Les analyses des notebooks 04 et 05 portent sur 2019-2022, soit 467 348 usagers, dont 467 079 à gravité connue. Les comparaisons sont descriptives et leur bootstrap conserve les usagers d'un même accident ensemble.

| ID | Décision | Mise en œuvre et justification |
|---|---|---|
| D1 | Métropole, Corse comprise | Filtre fondé sur le département ; exclusions chiffrées et sources complètes conservées |
| D2 | Décès ou hospitalisation | Cible 1 pour gravité 2 ou 3, cible 0 pour 1 ou 4 ; gravité inconnue conservée puis exclue des tâches supervisées |
| D3 | Apprentissage 2019-2022, validation 2023, test 2024 | Partitions temporelles ; exploration passée de 2024 déclarée ; aucun réglage sur ses scores |
| D4 | Résumé des lieux par accident et par variable | Une seule valeur connue conservée ; plusieurs valeurs connues donnent une absence et un indicateur de désaccord ; information partielle signalée. Règles mises en œuvre dans le notebook 03 et revues le 16 octobre |
| D5 | Nettoyage explicite et traçable | Codes inconnus traités champ par champ, âges hors de 0-110 rendus manquants avec trace, cible inconnue jamais transformée en 0, contrôles de relecture et de jointure dans le notebook 03 |
| D6 | Onze variables, âge en tranches, one-hot et absence explicite | Choix de représentation convenu le 17 octobre avant entraînement ; liste et limites détaillées en section 8 |
| D7 | Référence et logistique, sélection par log-loss 2023 | Règles de mise en œuvre fixées avant comparaison le 17 octobre ; quatre C, seuil illustratif 0,5, configuration enregistrée avant test 2024 |

La sensibilité « décès seuls » est réalisée dans le volet statistique ; elle n'implique pas d'entraîner un second modèle ML dans cette version. Les extensions de Poisson, d'arbres, de SHAP et de RO restent facultatives. Elles ne retardent pas la livraison du socle.

Les notebooks 06 et 07 sont exécutés et vérifiés sur 2023 puis 2024. La reconstruction retrouve les scores de validation avant le test ; les empreintes et les règles restent inchangées. Le README et l’organisation des résultats sont maintenant rédigés. Le prochain jalon est la rédaction de la partie ML du rapport et de sa conclusion générale. Les résultats chiffrés seront ajoutés au rapport, sans modifier rétrospectivement les critères du présent protocole.

## Références de travail

- Échanges utilisateur des 12 et 15 octobre 2026 : objectif de stage, période, démarche pédagogique et souhait d'étudier les corrélations.
- `01_data_discovery.ipynb`, version de travail relue et réexécutée le 16 octobre 2026.
- `02_schema_consistency_2019_2024.ipynb`, version de travail relue et réexécutée le 16 octobre 2026.
- ONISR, *Description des bases de données annuelles des accidents corporels de la circulation routière, années 2005–2024*, 21 octobre 2025, document fourni et déjà examiné avec le projet.
- [Page source BAAC sur data.gouv.fr](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024).

- Notebooks 03 à 05 et leurs exports vérifiés le 16 octobre 2026.
- Échanges des 16 et 17 octobre 2026 : limitation du périmètre ML et choix du prétraitement.

- Notebooks 06 et 07 : sélection sur 2023 et test rétrospectif sur 2024, vérifiés le 17 octobre 2026.

## Organisation des résultats mise en place le 17 octobre 2026

Les figures et tableaux sont rangés dans des sous-dossiers correspondant aux notebooks :
`04_exploration`, `05_statistics`, `06_modeling`, `07_evaluation`. Les noms de fichiers conservent
leurs préfixes 04 à 07. Le notebook 07 lit la configuration du 06 dans
`reports/tables/06_modeling/06_configuration_retenue.json` ; ses propres résultats vont dans
`reports/tables/07_evaluation/`. Les données brutes et préparées ne changent pas de place.

Le module ML et les fichiers de données, configurations et résultats sont conservés à l'identique.
Cette réorganisation ne crée pas une nouvelle sélection de modèles ni un nouveau test de 2024.
Les bibliothèques directement utilisées et leurs versions sont indiquées dans un seul fichier,
`requirements.txt`. Leurs dépendances sont installées par `pip`, qui choisit des versions
compatibles avec les contraintes déclarées. Le Makefile crée l’environnement `.venv`
et lance cette installation avec `make install`. La commande `make clean` supprime
uniquement `.venv`, sans toucher aux données, notebooks ou résultats.
La documentation ONISR se trouve dans `docs/references/`.
