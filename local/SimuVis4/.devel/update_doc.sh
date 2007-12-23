#!/bin/sh
if [ -d .devel ]; then
  BASE="data/Doc"
  for LANG in $(ls $BASE); do
    P=$BASE/$LANG
    OPT="--language=$LANG --prune=$P/.svn"
    rst-buildhtml $OPT $P
  done
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
