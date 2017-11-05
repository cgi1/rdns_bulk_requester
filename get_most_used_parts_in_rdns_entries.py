#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Purpose:     Read a file and show most occurring substrings
#
# Author:      Christoph Giese <github: cgi1>
#
# Created:     05.11.2017
# Copyright:   (c) Christoph Giese 2017
# Licence:     MIT
# -------------------------------------------------------------------------------


import argparse
import operator
from collections import Counter
import os
import glob
import json
import re
import pprint


def read_arguments_from_cli():
    parser = argparse.ArgumentParser(description='Read a file and show most occurring substrings')
    parser.add_argument('-if', '--file-input', dest="file_input",
                        help='File to read (only line separated files are supported)',
                        required=False)
    parser.add_argument('-all', '--all', dest="all",
                        help='Read all files and create occurring lists)',
                        required=False)
    args = vars(parser.parse_args())

    return args

def count(filepath):

    if not os.path.exists(filepath):
        print('Path (%s) does not exist!' % filepath)
        return



    with open(filepath, 'r') as myfile:
        raw_data_str = myfile.read()

    delimiters = ".", "-", "\n"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    splitted_data = re.split(regex_pattern, str(raw_data_str))

    filtered_data = []

    for entry in splitted_data:

        #if len(entry) <= 1:
        #    continue

        try:
            int_entry = int(entry)
            if 0 <= int_entry <= 255:
                continue
            else:
                filtered_data.append(int_entry)
        except:
            filtered_data.append(entry)

    counted_dict = dict(Counter(filtered_data))
    x_most_common_strings = dict(Counter(filtered_data).most_common(20))
    to_pprint = sorted(x_most_common_strings.items(), key=operator.itemgetter(1), reverse=True)
    pprint.pprint(to_pprint)

    with open(os.getcwd() + '/logs/most_used_parts/' + os.path.basename(filepath) + '.json', 'w') as fout:

        #pprint.pprint(to_pprint, fout)
        fout.write(json.dumps(x_most_common_strings, indent=3))

    """
    list_of_ten_most_common_strings = list(ten_most_common_strings.keys())
    with open(filepath, 'r') as myfile:
        raw_data=myfile.readlines()

    for line in raw_data:

        line = line.rstrip()

        if list_of_ten_most_common_strings[0] in line and list_of_ten_most_common_strings[1] in line and list_of_ten_most_common_strings[2] in line:
            print (line)
    """



def main(args):

    basedir = os.getcwd() + '/logs/'
    all = False

    if 'file_input' in args and args['file_input'] is not None:
        filepath = basedir + args['file_input']

    elif 'all' in args and args['all'] is not None:
        all = True

    else:
        # Use latest log file as defailt
        list_of_files = glob.glob(basedir + '*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        filepath = latest_file

    if all:
        for filename in os.listdir(basedir):
            if filename.endswith('.log'):
                count(filepath=basedir + filename)
    else:
        count(filepath=filepath)


if __name__ == '__main__':
    # Only
    args = read_arguments_from_cli()
    main(args=args)
