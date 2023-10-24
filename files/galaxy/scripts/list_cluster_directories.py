#!/usr/bin/env python3
import os
import subprocess
from subprocess import check_output
import sys
import re

def validate_parameters():
    if len(sys.argv) < 3:
        sys.stderr.write("usage: %s path user_name\n" % sys.argv[0])
        exit(1)
    path = sys.argv[2]
    username = sys.argv[1]
    return path, username


def main():
    path, username = validate_parameters()
    list_command = "runuser -l " + username + " -c 'ls -lc " + path  +  "'"


    try:
            ls_output = subprocess.check_output([list_command], shell=True).decode().split('\n');
            ls_output.pop()
            ls_output.remove(ls_output[0])

            # final file_dirs list
            user_accessible_files_and_dirs = []

            # store every ls line in a list
            elem_list = []

            # ctime
            ctime_index_list = [5,6,7]

            for elem_str in ls_output:
               elem_list = elem_str.split()
               type = elem_list[0]
               size = elem_list[4]
               ctime = (' '.join([elem_list[i] for i in ctime_index_list]))
               name = elem_list[8]
               user_accessible_files_and_dirs.extend((type,size,ctime,name))

            print(user_accessible_files_and_dirs)

    except subprocess.CalledProcessError as e:
                print("Cannot open directory %s  Permission denied " % path)


if __name__ == "__main__":
    main()






