#!/bin/sh
if [ -d .devel ]; then
    for pi in *; do
        if [ -f $pi/PLUGIN.INI ]; then
            PY=$(find $pi -type f -iname "*.py")
            LANGUAGES="de"
            for L in $LANGUAGES; do
                TS=$pi/$L.ts
                QM=$pi/$L.qm
                pylupdate4 -verbose $PY -ts "$TS"
                if [ "$TS" -nt "$QM" ]; then
                    linguist-qt4 "$TS"
                    lrelease-qt4 "$TS" -qm "$QM"
                fi
            done
        fi
    done
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
