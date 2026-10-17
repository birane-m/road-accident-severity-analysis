"""Représentation des 11 variables retenues pour l'étude prédictive BAAC.

Ces règles sont déterministes : elles ne calculent aucune statistique sur les
années de validation ou de test. L'encodeur reste ajusté dans la pipeline.
"""

import pandas as pd

SOURCE_FEATURES = [
    "age_approx", "sexe", "catu", "catv", "lum", "agg", "int", "atm",
    "mois_accident", "jour_semaine", "heure_accident",
]
MODEL_FEATURES = ["tranche_age", *SOURCE_FEATURES[1:]]
AGE_EDGES = [0, 18, 25, 35, 45, 55, 65, 75, 111]
AGE_LABELS = [
    "0-17 ans", "18-24 ans", "25-34 ans", "35-44 ans", "45-54 ans",
    "55-64 ans", "65-74 ans", "75 ans ou plus",
]
MISSING = "Non renseigné"


def make_features(data):
    """Créer les seules colonnes autorisées, sans modifier la table d'entrée.

    L'âge est déjà contrôlé dans le notebook 03. Une valeur connue hors du
    domaine ou non entière signale ici une entrée différente de celle attendue.
    Les autres codes restent des étiquettes, y compris heure, mois et semaine.
    """
    absent = set(SOURCE_FEATURES) - set(data.columns)
    if absent:
        raise ValueError(f"Variables absentes de la table préparée : {sorted(absent)}")
    age = pd.to_numeric(data["age_approx"], errors="raise")
    known = age.dropna()
    if not (known.between(0, 110) & known.mod(1).eq(0)).all():
        raise ValueError("Âge préparé hors du domaine entier 0-110 : revoir le notebook 03.")
    result = data.loc[:, SOURCE_FEATURES[1:]].astype("string").copy()
    result.insert(0, "tranche_age", pd.cut(
        age, bins=AGE_EDGES, right=False, labels=AGE_LABELS
    ).astype("string"))
    result = result.fillna(MISSING).astype(object)
    if not result.index.equals(data.index) or result.isna().any().any():
        raise AssertionError("La représentation doit conserver l'ordre des usagers sans NA.")
    return result.loc[:, MODEL_FEATURES]
