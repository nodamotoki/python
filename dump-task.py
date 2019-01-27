#!/usr/bin/python3
#
# Emacs で org-mode の agenda "t" を実行して task agenda を csv で出力し
# その出力を加工するサンプル
# 参考) https://takaxp.github.io/org-ja.html
#
import os
import sys
import re
import subprocess
import traceback

DOT_EMACS="~/.emacs.d/init.el"
CMD = "emacs -batch -l {} -eval '(org-batch-agenda-csv \"t\")' 2> /dev/null".format(DOT_EMACS)
#print(CMD)

def main():
    try:
        output = subprocess.check_output(CMD, shell=True)
        strout = output.decode()
        print(strout)
        for line in strout.split("\n"):
            # print(line)
            line = line.strip()
            if len(line) == 0:
                continue
            category, head, typ, todo, tags, date, time, extra, prio_l, prio_n, *remain = line.split(",")
            print("[{todo}] {head}".format(head=head, todo=todo))
    except subprocess.CalledProcessError as e:
        print("error: retcode:", e.returncode,
              "\ncmd:", e.cmd,
              "\nstdout:\n", e.stdout,
              "\nstderr:\n", e.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


