#!/bin/sh
if [ -z "$MODULEPATH" ] ; then
   . /etc/profile.d/z00_lmod.sh
   . /etc/profile.d/z01_StdEnv.sh
fi

module add FastQC/0.11.9-Java-11
