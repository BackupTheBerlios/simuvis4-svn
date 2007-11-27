#!/bin/sh
if [ -d .devel ]; then
  PY=$(find . -type f -iname "*.py")
  LANGUAGES="de"
  LANGPATH="data/Language"
  for L in $LANGUAGES; do
    TS=$LANGPATH/$L.ts
    QM=$LANGPATH/$L.qm
    pylupdate4 -noobsolete -verbose $PY -ts "$TS"
    if [ "$TS" -nt "$QM" ]; then
      linguist-qt4 "$TS"
    fi
  done
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
