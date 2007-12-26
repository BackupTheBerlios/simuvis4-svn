#!/bin/sh
if [ -d .devel ]; then
  GOPT="--input-encoding=UTF-8 --output-encoding=ascii --output-encoding-error-handler=xmlcharrefreplace"
  # main doc
  BASE="data/Doc"
  for LANG in $(ls $BASE); do
    P=$BASE/$LANG
    OPT="$GOPT --language=$LANG --prune=$P/.svn"
    rst-buildhtml $OPT $P
  done
  # plugin doc
  for PI in data/PlugIns/*; do
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
