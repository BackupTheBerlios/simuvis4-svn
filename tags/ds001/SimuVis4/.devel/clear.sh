#!/bin/sh
if [ -d .devel ]; then
  rm -Rfv build
  rm -Rfv dist
  find . -type f \( -name "*~" -o -iname "*.pyo" -o -iname "*.pyc" \) -exec rm -v {} \;
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
