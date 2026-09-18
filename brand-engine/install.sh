#!/usr/bin/env bash
# DFC brand engine - installeur autonome (a lancer une fois sur le VPS).
# Cree un venv local, installe les dependances Python et le navigateur Chromium.
# Aucune dependance systeme requise au-dela de python3 (pas de poppler, pas de node).
set -e
cd "$(dirname "$0")"

PYBIN="${PYBIN:-python3}"
echo "[DFC] venv ..."
$PYBIN -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip -q
echo "[DFC] dependances Python ..."
pip install -q playwright pikepdf pyyaml pillow numpy matplotlib
echo "[DFC] navigateur Chromium (Playwright) ..."
# --with-deps tente d'installer les libs systeme du navigateur (necessite root/sudo).
python -m playwright install --with-deps chromium || python -m playwright install chromium
echo "[DFC] test de rendu ..."
python render_doc.py example_pack.yaml _selftest.pdf
echo "[DFC] OK. Moteur pret. Rendu de reference: _selftest.pdf"
