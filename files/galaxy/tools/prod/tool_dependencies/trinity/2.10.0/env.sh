#!/bin/sh
if [ -z "$MODULEPATH" ] ; then
   . /etc/profile.d/z00_lmod.sh
   . /etc/profile.d/z01_StdEnv.sh
fi

module load Trinity/2.10.0-foss-2020a-Python-3.8.2
