#!/bin/sh
if [ -d .devel ]; then
  GOPT="--input-encoding=UTF-8 --output-encoding=ascii --output-encoding-error-handler=xmlcharrefreplace --stylesheet-path=../SimuVis4/data/Doc/style.css"
  for PI in ./*; do
    if [ -f $PI/PLUGIN.INI ]; then
      BASE="$PI/Doc"
      for LANG in $(ls $BASE); do
        P=$BASE/$LANG
        OPT="$GOPT --language=$LANG --prune=$P/.svn"
        rst-buildhtml $OPT $P
      done
    fi
  done
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
