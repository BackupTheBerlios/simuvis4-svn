#!/bin/sh
if [ -d .devel ]; then
    for pi in *; do
        if [ -f $pi/PLUGIN.INI ]; then
            piz=$pi.zip
            echo "Making $piz:"
            if [ -f $piz ]; then
                rm $piz
            fi
            cd $pi
            zip -r ../$piz .
            cd ..
        fi
    done
else
  echo "Start this tool in the base folder of development"
  exit 1
fi
