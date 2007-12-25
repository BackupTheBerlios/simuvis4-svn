#!/bin/sh
if [ -d .devel ]; then
  for PI in ./*; do
    if [ -f $PI/PLUGIN.INI ]; then
      BASE="$PI/Doc"
      for LANG in $(ls $BASE); do
        P=$BASE/$LANG
        OPT="--language=$LANG --prune=$P/.svn"
        rst-buildhtml $OPT $P
      done
    fi
  done
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
