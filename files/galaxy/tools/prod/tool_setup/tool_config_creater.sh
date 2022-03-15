#!/bin/bash
#sabryr 29-02-2021

#BLAST
ls /cluster/galaxy/data/tools/prod/tool_wrappers/blast/*xml  awk -F "/" '{print "<tool file=blast/"$NF" />"}'
