#!/bin/sh
if [ -d devel ]; then
  . devel/clear.sh
  export SVN_EDITOR=ne
  svn commit .
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
