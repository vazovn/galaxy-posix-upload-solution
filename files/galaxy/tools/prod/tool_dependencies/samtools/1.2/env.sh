#!/bin/sh
if [ -z "$MODULEPATH" ] ; then
   . /etc/profile.d/z00_lmod.sh
   . /etc/profile.d/z01_StdEnv.sh
fi

module load SAMtools/1.12-GCC-10.3.0 
