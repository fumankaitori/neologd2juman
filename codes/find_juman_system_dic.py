# -*- coding: utf-8 -*-
"""
.jumanrcファイルを探し出して、標準出力で表示

usage:
"""

import os
import re
import sys

if len(sys.argv) == 2:
    parent_dir = sys.argv[1]
else:
    parent_dir = '/usr/'

def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


path_juman_dic = ''
for file in fild_all_files(parent_dir):
    if re.findall(r'juman/dic/', file) != []:
        path_juman_dic = file.split('/dic')[0]
        break

print(os.path.join(parent_dir, path_juman_dic))