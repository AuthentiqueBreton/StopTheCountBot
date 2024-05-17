#!/bin/bash

_SELF=$(readlink -f "${BASH_SOURCE[0]}")
_PROJECT_DIR=${_SELF%/*}
_VENV_DIR=$_PROJECT_DIR/venv
_SRC_DIR=$_PROJECT_DIR/src

source "$_PROJECT_DIR/venv/bin/activate"

if [[ -e $_SRC_DIR ]]
then
  if [[ -z ${PYTHONPATH:-} ]]
  then
    export PYTHONPATH=$_SRC_DIR
  elif [[ ":$PYTHONPATH:" != *":$_SRC_DIR:"* ]]
  then
    export PYTHONPATH=$_SRC_DIR:$PYTHONPATH
  fi
fi

unset _SELF _PROJECT_DIR _VENV_DIR _SRC_DIR
