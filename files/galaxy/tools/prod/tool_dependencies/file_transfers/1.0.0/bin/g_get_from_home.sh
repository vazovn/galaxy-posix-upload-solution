#!/bin/bash
date > out.txt
SOURCE_LOC="/cluster/home/"$SLURM_JOB_USER"/move-to-galaxy"
if [ -d $SOURCE_LOC ]
then
   mv $SOURCE_LOC/* .
else
  echo "Dir $SOURCE_LOC found "> out.txt
fi

#echo "UID" ${UID}
#echo "USER" ${USER}
