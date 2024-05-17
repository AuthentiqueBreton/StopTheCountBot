#!/bin/bash

set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
PROJECT_DIR=${SELF%/*/*}
VENV_DIR=$PROJECT_DIR/venv

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install --upgrade pylint

if [[ -e $PROJECT_DIR/requirements.txt ]]
then
  pip install --upgrade --requirement "$PROJECT_DIR/requirements.txt"
fi
