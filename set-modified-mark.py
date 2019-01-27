#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# 引数にファイルを二つ取り、変更箇所の行頭に + マークを付ける
#
import os
import sys
import re
import subprocess
import traceback

if __name__ == '__main__':
	file1 = sys.argv[1]
	file2 = sys.argv[2]
	root, ext = os.path.splitext(file2)
	ofile = root + '_marked' + ext
	cmdline = f"diff -u9999 '{file1}' '{file2}' | grep -v -e '^\(@@\|+++\|---\|-\)' > {ofile}"
	subprocess.run(cmdline, shell=True)


