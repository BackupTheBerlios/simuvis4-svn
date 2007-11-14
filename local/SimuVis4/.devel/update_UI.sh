#!/bin/sh
if [ -d devel ]; then
  for UI in $(find . -type f -iname "*.ui"); do
    PY=${UI%.ui}.py
    if [ $UI -nt $PY ]; then
      echo "converting $UI to $PY"
      pyuic4 -x $UI | sed -e "s/self.tr/_/g" > $PY
    fi
  done
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
