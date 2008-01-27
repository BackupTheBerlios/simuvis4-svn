#!/bin/sh
if [ -d .devel ]; then
  . .devel/clear.sh
  TS=$(date +%y%m%d%H%M)
  TBZ=SV4_$TS.tar.bz2
  tar -cjf ../$TBZ ../SimuVis4/
  echo ">>> $TBZ"
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
