#!/bin/sh
if [ -z "$MODULEPATH" ] ; then
   . /etc/profile.d/z00_lmod.sh
   . /etc/profile.d/z01_StdEnv.sh
fi

module add BWA/0.7.17-foss-2018b SAMtools/1.9-foss-2018b

