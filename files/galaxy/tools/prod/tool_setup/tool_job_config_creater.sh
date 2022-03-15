#09-02-2021
#Sabryr
#for balst

 grep "id=" /cluster/galaxy/data/tools/prod/tool_wrappers/blast/*xml | awk -F "id=\"" '{print $NF}' | awk -F "\"" '{print "<tool id=\""$1"\" destination=\"slurm_bigmem\"/>"}'
