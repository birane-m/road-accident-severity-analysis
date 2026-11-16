"""Générer les tableaux LaTeX à partir des seuls résultats agrégés livrés.

Exécuter : python scripts/generer_tableaux.py
Aucune donnée individuelle et aucune dépendance Python externe ne sont nécessaires.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tableaux'
OUT.mkdir(exist_ok=True)

def read(relative):
    with (ROOT / relative).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))

def esc(value):
    text = str(value)
    return ''.join({'&': r'\&', '%': r'\%', '_': r'\_', '#': r'\#', '$': r'\$'}.get(c, c) for c in text)

def integer(value):
    return f'{int(float(value)):,}'.replace(',', r'\,')

def number(value, digits=2):
    return f'{float(value):.{digits}f}'.replace('.', ',')

def table(name, caption, label, headers, rows, columns, source):
    numeric = columns == 'numeric_contrasts'
    begin = (r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrr@{}}' if numeric else
             r'\begin{tabularx}{\textwidth}{@{}' + columns + '@{}}')
    end = r'\end{tabular*}' if numeric else r'\end{tabularx}'
    lines = [r'\begin{table}[htbp]', r'\centering\small', r'\renewcommand{\arraystretch}{1.18}',
             r'\caption{' + caption + r'}\label{' + label + '}',
             begin, r'\toprule',
             ' & '.join(headers) + r' \\', r'\midrule']
    lines.extend(' & '.join(row) + r' \\' for row in rows)
    lines.extend([r'\bottomrule', end, r'\sourcecalcul{' + source + '}', r'\end{table}', ''])
    (OUT / name).write_text('\n'.join(lines), encoding='utf-8')

p = read('resultats/preparation/baac_bilan_effectifs.csv')
rows = [[r['année'], integer(r['usagers_source_complète']), integer(r['usagers_métropole']),
         integer(r['accidents_métropole']), integer(r['cible_inconnue'])] for r in p]
rows.append([r'\textbf{Total}', integer(sum(int(r['usagers_source_complète']) for r in p)),
             integer(sum(int(r['usagers_métropole']) for r in p)),
             integer(sum(int(r['accidents_métropole']) for r in p)),
             integer(sum(int(r['cible_inconnue']) for r in p))])
table('population_preparee.tex', 'Passage des sources complètes à la table métropolitaine.', 'tab:population-preparee',
      ['Année', 'Usagers sources', 'Usagers retenus', 'Accidents retenus', 'Gravités inconnues retenues'],
      rows, 'lRRRR'.replace('R', '>{\\raggedleft\\arraybackslash}X'), 'notebook 03, bilan des effectifs')

rows = [[r['année'], integer(r['âges_suspects']), integer(r['âges_manquants_après_traitement']),
         integer(r['véhicules_sans_usager_métropole'])] for r in p]
table('qualite_preparee.tex', 'Quelques indicateurs de qualité dans le périmètre métropolitain.', 'tab:qualite-preparee',
      ['Année', 'Âges suspects', 'Âges manquants après traitement', 'Véhicules sans usager'],
      rows, 'lLLL', 'notebook 03 ; les trois colonnes ne portent pas toutes sur la même unité')

a = read('resultats/tables/04_population_annuelle.csv')
table('population_apprentissage.tex', 'Population et proportion de décès ou hospitalisations, 2019-2022.', 'tab:population-train',
      ['Année', 'Usagers', 'Accidents', 'Gravités connues', 'Cas positifs', 'Proportion (\\%)'],
      [[r['annee_source'], integer(r['usagers']), integer(r['accidents']), integer(r['cibles_connues']),
        integer(r['positifs']), number(r['proportion_positive_pct'])] for r in a],
      'lLLLLL', 'notebook 04 ; dénominateur : gravités connues de chaque année')

for suffix, first in [('age', 'tranche_age'), ('categorie', 'categorie_usager'), ('lumiere', 'lumiere'), ('agglomeration', 'agglomeration')]:
    data = read('resultats/tables/04_gravite_selon_' + suffix + '.csv')
    table('gravite_' + suffix + '.tex', 'Gravité selon ' + {'age': "l'âge", 'categorie': "la catégorie d'usager", 'lumiere': 'la lumière', 'agglomeration': "l'agglomération"}[suffix] + ', 2019-2022.',
          'tab:gravite-' + suffix, ['Groupe', 'Gravités connues', 'Cas positifs', 'Proportion (\\%)'],
          [[esc(r[first]), integer(r['cible_connue']), integer(r['deces_ou_hospitalisation']), number(r['proportion_positive_pct'])] for r in data],
          '>{\\hsize=1.65\\hsize\\linewidth=\\hsize}L>{\\hsize=.8\\hsize\\linewidth=\\hsize}L>{\\hsize=.75\\hsize\\linewidth=\\hsize}L>{\\hsize=.8\\hsize\\linewidth=\\hsize}L',
          'notebook 04 ; les gravités inconnues sont exclues du dénominateur')

c = read('resultats/tables/05_contrastes.csv')
labels = {'age': '75+ / 35-44 ans', 'usager': 'Piétons / conducteurs', 'lumiere': 'Nuit sans éclairage / jour', 'agglomeration': 'Hors / en agglomération'}
for event, name, caption in [('deces_hospitalisation', 'contrastes_principaux.tex', 'Écarts et rapports : décès ou hospitalisation, 2019-2022.'),
                             ('deces_seul', 'contrastes_deces.tex', 'Écarts et rapports : décès seuls, 2019-2022.')]:
    data = [r for r in c if r['événement'] == event]
    rows = []
    for r in data:
        interval_d = '[' + number(r['écart_ic_bas']) + ' ; ' + number(r['écart_ic_haut']) + ']'
        interval_r = '[' + number(r['rapport_ic_bas']) + ' ; ' + number(r['rapport_ic_haut']) + ']'
        rows.append([esc(labels[r['comparaison']]), number(r['écart_points']), interval_d, number(r['rapport']), interval_r])
    table(name, caption, 'tab:' + event, ['Comparaison A / R', 'Écart (points)', 'IC à 95\\%', 'Rapport', 'IC à 95\\%'],
          rows, 'numeric_contrasts',
          "notebook 05 ; intervalles percentiles marginaux, 2 000 réplications d'accidents stratifiées par année")

s = read('resultats/tables/05_stabilite_bootstrap.csv')
table('stabilite_bootstrap.tex', 'Variation maximale d\'une borne d\'écart entre 1 000 et 2 000 réplications.', 'tab:stabilite',
      ['Comparaison', 'Cible principale (points)', 'Décès seuls (points)'],
      [[esc(labels[k]), number(next(r['variation_max_borne_points'] for r in s if r['comparaison']==k and r['événement']=='deces_hospitalisation'), 4),
        number(next(r['variation_max_borne_points'] for r in s if r['comparaison']==k and r['événement']=='deces_seul'), 4)] for k in labels],
      'LLL', 'notebook 05 ; contrôle numérique sur une graine fixée')


# Seconde partie : résultats fournis des notebooks 06 et 07.
import json

ml06 = 'resultats/tables/06_modeling/'
ml07 = 'resultats/tables/07_evaluation/'
configuration = json.loads((ROOT / ml06 / '06_configuration_retenue.json').read_text())
population = read(ml07 + '07_population_evaluation.csv')
groups = [('2019-2022', [2019,2020,2021,2022]), ('2023', [2023]), ('2024', [2024])]
rows=[]
for label, years in groups:
    selection=[r for r in population if int(r['annee_source']) in years]
    known=sum(int(r['cibles_connues']) for r in selection)
    missing=sum(int(r['cibles_inconnues']) for r in selection)
    positive=sum(int(r['cas_positifs']) for r in selection)
    rows.append([label,integer(known),integer(missing),integer(positive),number(100*positive/known)])
table('ml_population.tex', 'Populations utilisées pour la modélisation, après exclusion des gravités inconnues.',
      'tab:ml-population', ['Période','Cibles connues','Exclues','Cas positifs','Part (\\%)'],
      rows, 'numeric_contrasts', 'notebooks 06 et 07 ; les exclusions portent uniquement sur la cible inconnue')

scores=['log_loss','brier','average_precision','roc_auc']
selection=sorted(read(ml06+'06_selection_regularisation.csv'), key=lambda r:float(r['C']))
rows=[]
for row in selection:
    values=[number(row['C'], 2).rstrip('0').rstrip(',')]+[number(row[k],6) for k in scores]
    if float(row['C'])==configuration['C_retenu_logistique']:
        values=[r'\textbf{'+v+'}' for v in values]
    rows.append(values)
table('ml_selection.tex','Comparaison des quatre régularisations sur 2023 ; ligne retenue en gras.',
      'tab:ml-selection',['C','Log-loss','Brier','AP','ROC-AUC'],rows,'numeric_contrasts',
      'notebook 06 ; même représentation et même apprentissage pour les quatre valeurs de C')

validation=read(ml06+'06_comparaison_validation.csv')
table('ml_validation.tex','Scores de validation de la référence et du modèle retenu, 2023.',
      'tab:ml-validation',['Modèle','Log-loss','Brier','AP','ROC-AUC'],
      [[esc(r['modele'])]+[number(r[k],4) for k in scores] for r in validation],
      'numeric_contrasts','notebook 06 ; comparaison après sélection sur cette même année')

contrasts=read(ml06+'06_contrastes_logistique.csv')
table('ml_contrastes.tex','Contrastes de coefficients de la logistique retenue.',
      'tab:ml-contrastes',['Comparaison A / R','Écart de log-cotes','Rapport de cotes'],
      [[esc(r['comparaison']),number(r['difference_log_cotes'],3),number(r['rapport_de_cotes_penalise'],3)] for r in contrasts],
      'Lrr','notebook 06 ; rapports pénalisés, conditionnels au modèle, sans intervalle ni interprétation causale')

test=read(ml07+'07_scores_validation_test.csv')
table('ml_test.tex','Scores de validation et de test, configuration inchangée.',
      'tab:ml-test',['Année','Modèle','Log-loss','Brier','AP','ROC-AUC'],
      [[r['annee'],esc(r['modele'])]+[number(r[k],4) for k in scores] for r in test],
      'lLrrrr','notebook 07 ; apprentissage conservé sur 2019-2022')

cm=next(r for r in read(ml07+'07_erreurs_seuil_050.csv') if r['annee']=='2024' and r['modele']=='Régression logistique')
tn,fp,fn,tp=[int(cm[k]) for k in ['vrais_negatifs','fausses_alertes','cas_manques','vrais_positifs']]
assert tn+fp+fn+tp==117278 and tp+fn==21024
table('ml_confusion.tex','Matrice de confusion sur 2024, seuil illustratif de 0,5.',
      'tab:ml-confusion',['Issue observée','Prédiction 0','Prédiction 1'],
      [['Indemne ou blessé léger',integer(tn),integer(fp)],
       ['Décès ou hospitalisation',integer(fn),integer(tp)],
       [r'\textbf{Total}',integer(tn+fn),integer(fp+tp)]],
      'Lrr','notebook 07 ; classes observées en lignes, classes prédites en colonnes')

diagnostics=[r for r in read(ml07+'07_diagnostics_sous_populations.csv') if r['annee']=='2024' and r['dimension']=='catégorie']
table('ml_groupes_test.tex',"Diagnostics du test selon la catégorie d'usager.",'tab:ml-groupes',
      ['Catégorie','Usagers','Cas positifs','Observé (\\%)','Prédit (\\%)','ROC-AUC'],
      [[esc(r['groupe']),integer(r['usagers']),integer(r['cas_positifs']),number(100*float(r['proportion_observee'])),
        number(100*float(r['probabilite_moyenne'])),number(r['roc_auc'],4)] for r in diagnostics],
      'Lrrrrr','notebook 07 ; les deux pourcentages sont une proportion observée et une probabilité moyenne')


# Troisieme partie : resultats du notebook 08, comparaison de modeles.
ml08 = 'resultats/tables/08_comparaison/'

comparaison = read(ml08 + '08_comparaison_modeles.csv')
rows = []
for row in comparaison:
    values = [row['annee'], esc(row['modele'])] + [number(row[k], 4) for k in scores]
    if row['modele'] == 'Arbres boostés':
        values = [r'\textbf{' + v + '}' for v in values]
    rows.append(values)
table('ml_comparaison_modeles.tex',
      'Référence, régression logistique et arbres boostés sur 2023 et 2024.',
      'tab:ml-comparaison', ['Année', 'Modèle', 'Log-loss', 'Brier', 'AP', 'ROC-AUC'],
      rows, 'lLrrrr',
      "notebook 08 ; même apprentissage 2019-2022 et même représentation pour les deux modèles")

grille = read(ml08 + '08_selection_arbres.csv')
protocole08 = json.loads((ROOT / ml08 / '08_protocole_arbres.json').read_text())
configuration08 = json.loads((ROOT / ml08 / '08_configuration_arbres.json').read_text()) \
    if (ROOT / ml08 / '08_configuration_arbres.json').exists() else None
meilleur = min(grille, key=lambda r: float(r['log_loss']))
rows = []
for row in sorted(grille, key=lambda r: (float(r['learning_rate']), int(float(r['max_leaf_nodes'])), int(float(r['max_iter'])))):
    values = [number(row['learning_rate'], 2), integer(row['max_leaf_nodes']), integer(row['max_iter'])] \
             + [number(row[k], 6) for k in ['log_loss', 'brier', 'average_precision', 'roc_auc']]
    if row is meilleur or (row['learning_rate'], row['max_leaf_nodes'], row['max_iter']) == \
            (meilleur['learning_rate'], meilleur['max_leaf_nodes'], meilleur['max_iter']):
        values = [r'\textbf{' + v + '}' for v in values]
    rows.append(values)
table('ml_selection_arbres.tex',
      'Les huit configurations d\'arbres évaluées sur 2023 ; ligne retenue en gras.',
      'tab:ml-selection-arbres',
      ['Pas', 'Feuilles', 'Itérations', 'Log-loss', 'Brier', 'AP', 'ROC-AUC'],
      rows, 'rrrrrrr',
      'notebook 08 ; grille écrite avant le premier entraînement, sélection par log-loss de 2023')

seuils = [r for r in read(ml08 + '08_seuils_rappel_cible.csv') if r['rappel_vise_sur_2023']]
rows = []
for row in seuils:
    court = {'Régression logistique': 'Logistique', 'Arbres boostés': 'Arbres'}
    rows.append([esc(court.get(row['modele'], row['modele'])), number(100 * float(row['rappel_vise_sur_2023']), 0),
                 number(row['seuil'], 3), number(100 * float(row['rappel'])),
                 number(100 * float(row['precision'])), integer(row['fausses_alertes']),
                 integer(row['cas_manques']), number(row['part_population_alertee_pct'])])
table('ml_seuils.tex',
      'Seuils fixés sur 2023 pour un rappel visé, puis appliqués sans retouche à 2024.',
      'tab:ml-seuils',
      ['Modèle', 'Visé (\\%)', 'Seuil', 'Rappel (\\%)', 'Précision (\\%)',
       'Fausses alertes', 'Cas manqués', 'Alertés (\\%)'],
      rows, 'Lrrrrrrr',
      "notebook 08 ; « Logistique » et « Arbres » désignent les deux modèles du tableau~\\ref{tab:ml-comparaison} ; toutes les colonnes de résultat portent sur 2024")

profils = read(ml08 + '08_profils_croises_test.csv')
profils = sorted(profils, key=lambda r: -float(r['observe_pct']))[:8]
table('ml_profils_croises.tex',
      "Profils les plus exposés en 2024 : proportions observées et probabilités moyennes.",
      'tab:ml-profils',
      ['Catégorie', 'Tranche d\'âge', 'Usagers', 'Observé (\\%)', 'Logistique (\\%)', 'Arbres (\\%)'],
      [[esc(r['categorie']), esc(r['tranche_age']), integer(r['usagers']),
        number(r['observe_pct']), number(r['logistique_pct']), number(r['arbres_pct'])]
       for r in profils],
      'LLrrrr',
      "notebook 08 ; groupes d'au moins 300 usagers, triés par proportion observée")

ages = read(ml08 + '08_ages_manquants_par_annee.csv')
rows = []
for r in ages:
    taux = number(r['taux_si_age_absent_pct']) if r['taux_si_age_absent_pct'] else '--'
    rows.append([r['annee'], integer(r['usagers']), integer(r['age_absent']),
                 number(r['part_age_absent_pct']), integer(r['dont_age_juge_invraisemblable']),
                 integer(r['positifs_si_age_absent']), taux,
                 number(r['taux_si_age_present_pct'])])
table('ages_manquants_annuel.tex',
      "Usagers sans âge et gravité associée, par année, sur les gravités connues.",
      'tab:ages-manquants',
      ['Année', 'Usagers', 'Sans âge', 'Part (\\%)', 'Dont nettoyage', 'Positifs',
       'Taux sans âge (\\%)', 'Taux avec âge (\\%)'],
      rows, 'lrrrrrrr',
      "notebook 08 ; la colonne « dont nettoyage » compte les âges rendus manquants par le notebook 03")

impact = read(ml08 + '08_ages_manquants_impact_scores.csv')
table('ages_manquants_impact.tex',
      "Scores de 2024 avec et sans les usagers dont l'âge est absent.",
      'tab:ages-impact',
      ['Modèle', 'Population', 'Usagers', 'Log-loss', 'Brier', 'AP', 'ROC-AUC'],
      [[esc(r['modele']), esc(r['population']), integer(r['usagers'])]
       + [number(r[k], 4) if r.get(k) else '--' for k in scores] for r in impact],
      'LLrrrrr',
      "notebook 08 ; mêmes prédictions dans les deux populations, sans réentraînement")

assert abs(float(meilleur['log_loss']) - 0.3846) < 1e-3
assert len(grille) == 8
assert sum(int(r['age_absent']) for r in ages) == 10319
assert configuration['C_retenu_logistique']==1.0
assert configuration['usagers_apprentissage']==467079
assert configuration['usagers_validation']==118101
assert configuration['colonnes_apres_encodage']==117
assert all(abs(float(r['score_06'])-float(r['score_reconstruit'])) <= 1e-4 for r in read(ml07+'07_controle_reconstruction.csv'))
print('23 tableaux générés depuis les résultats agrégés, contrôles numériques validés.')
