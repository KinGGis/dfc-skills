# DFC brand engine - moteur de production documentaire

Moteur autonome qui transforme un pack de contenu (format DFC-CONTENT-PACK v1,
spec DFC-PACK-001) en PDF a la charte DualForce Capital. Logos embarques en
base64 (aucun fichier binaire a fournir, aucune URL externe). Fusion PDF en
Python (pikepdf), pas de poppler ni de node.

## Contenu

- `render_doc.py`   moteur (CLI)
- `assets_b64.py`   logos DFC embarques (blanc + noir), source unique
- `dfc_charts.py`   graphiques a la palette (optionnel, barres / courbe / donut)
- `example_pack.yaml` pack de demonstration (note d'arrete de NAV)
- `install.sh`      installeur (venv + dependances + Chromium)

## Installation (une seule fois, sur le VPS)

Deposer ce dossier a un chemin fixe, par exemple `/opt/dfc/brand-engine`, puis:

    cd /opt/dfc/brand-engine
    bash install.sh

L'installeur cree `.venv`, installe playwright/pikepdf/pyyaml/pillow/numpy/matplotlib
et telecharge Chromium. Il termine par un rendu de test (`_selftest.pdf`).

Dependances systeme: seulement `python3`. `install.sh` tente `playwright install
--with-deps` pour les librairies du navigateur (peut demander root); a defaut il
installe Chromium seul.

## Utilisation (par l'agent, a chaque document)

    /opt/dfc/brand-engine/.venv/bin/python \
        /opt/dfc/brand-engine/render_doc.py  chemin/vers/pack.yaml  chemin/vers/sortie.pdf

Le pack peut etre un fichier `.yaml` ou `.json`, avec ou sans les marqueurs
`=== DFC-CONTENT-PACK v1 ===` / `=== FIN PACK ===`.

## Conventions de contenu (rappel DFC-PACK-001)

- Cellules de tableau: suffixe `(pos)` = vert, `(neg)` = rouge; mot-cle `total`
  en fin de ligne = ligne de total (fond creme, gras).
- `align` par colonne: `left` ou `num` (aligne a droite, tabulaire).
- Corps de section: `**gras**` pour les chiffres cles; paragraphes separes par
  une ligne vide.
- KPI: exactement trois, soit au niveau du pack, soit dans une section.
- Devise explicite, virgule decimale, pas de tiret cadratin.

## Mise a jour des logos

Les logos vivent dans `assets_b64.py` (base64). Pour les changer, remplacer les
deux chaines `LOGO_WHITE_B64` (blanc, fonds sombres) et `LOGO_DARK_B64` (noir,
fonds clairs). L'emblème monogramme des en-tetes est redecoupe automatiquement.
