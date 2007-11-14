#!/bin/sh
if [ -d devel ]; then
  . devel/clear.sh
  TS=$(date +%y%m%d%H%M)
  A7Z=SV4_$TS.7z
  7za a  ../$A7Z ../SimuVis4/
  echo ">>> $A7Z"
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
