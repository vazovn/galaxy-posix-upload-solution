#!/bin/sh
if [ -z "$MODULEPATH" ] ; then
   . /etc/profile.d/z00_lmod.sh
   . /etc/profile.d/z01_StdEnv.sh
fi

module add BLAST+/2.10.1-gompi-2020a

