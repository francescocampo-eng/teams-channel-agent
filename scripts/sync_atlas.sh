#!/usr/bin/env bash
# Risincronizza le fonti canoniche verso .atlas/, che è l'unica cartella
# indicizzata da Atlas/Inlay Studio. Non editare mai i file dentro .atlas/
# a mano: vengono sovrascritti dal prossimo run di questo script.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

cp docs/ciro_persona.md .atlas/ciro_persona.md

mkdir -p .atlas/opportunita
cp site/data/raw/*.md .atlas/opportunita/

python3 scripts/render_stato_opportunita.py

echo "Sincronizzati in .atlas/:"
echo "  - ciro_persona.md"
echo "  - opportunita/*.md ($(ls site/data/raw/*.md | wc -l) file)"
echo "  - stato_opportunita.md (snapshot sola lettura da data/presales_milestones.json)"
