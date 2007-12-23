#!/bin/sh
if [ -d .devel ]; then
  for pi in *; do
    if [ -f $pi/PLUGIN.INI ]; then
      BASE="$pi/Doc"
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
