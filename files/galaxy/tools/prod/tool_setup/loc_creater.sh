#1/bin/bash
#Sabryr 09-09-2021
#To generate loc files
#argument 1 : Loations of genomes
#argument 2 : outputfile

LOC_PATH=$1
DATESTRING="04-02-2021"
ls $LOC_PATH |grep -v md5  | awk -v LOC_PATH="$LOC_PATH" -v CDATE="$DATESTRING" -F "." '{print $1"_"CDATE"\t"$1"_"CDATE"\t"LOC_PATH"/"$1 }' | sort | uniq > $2

