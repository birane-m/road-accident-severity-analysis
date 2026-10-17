# À lancer depuis la racine du projet, sous Linux ou macOS.
PYTHON ?= python3
REQUIREMENTS ?= requirements.txt

.DEFAULT_GOAL := help
.PHONY: help install clean
# Évite que « make -j clean install » supprime le venv pendant l'installation.
.NOTPARALLEL:

help:
	@printf '%s\n' \
	  'make install  : crée .venv et installe les dépendances du projet' \
	  'make clean    : supprime uniquement .venv' \
	  'Python choisi : make install PYTHON=python3.12'

install:
	@test -f "$(REQUIREMENTS)" || { printf '%s\n' 'Fichier de dépendances introuvable.' >&2; exit 1; }
	"$(PYTHON)" -m venv .venv
	.venv/bin/python -m pip install -r "$(REQUIREMENTS)"
	@printf '%s\n' \
	  'Environnement prêt.' \
	  'Pour l’activer dans votre terminal : source .venv/bin/activate' \
	  'Pour ouvrir les notebooks : .venv/bin/python -m jupyter lab'

clean:
	rm -rf -- .venv
	@printf '%s\n' 'Le dossier .venv a été supprimé.'
