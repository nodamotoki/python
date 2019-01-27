#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# TASKDIR フォルダに指定したタスク専用のフォルダを掘り、
# TASKLOGDIR フォルダにそのタスク専用のログファイルを作成する。
# その後、ログファイルのショートカットを作成したフォルダに作る。
#

import os
import sys
import re
from datetime import datetime
import traceback
import subprocess
from pathlib import Path
import glob
import win32com.client

# \\ を / に置換した HOME
# HOME = re.sub(r'\\', '/', os.environ['HOME'])
HOME = "C:/cygwin64/home/somebody"

# ★フォルダ名をここで指定する
TASKDIR = f"{HOME}/タスク"

# ★共通ログ置き場をここで指定する
TASKLOGDIR = f"{HOME}/タスクログ"


def get_task_dir_and_logfile_path(title):
    # TASKDIR フォルダがなければ何もしない
    if not os.path.exists(TASKDIR):
        return

    # YYYYMM_xxx で始まるフォルダをリストアップ
    today = datetime.today()
    dir_header = f"{TASKDIR}/{today.year:04d}{today.month:02d}_"
    taskdirs = sorted([d for d in glob.iglob(
        dir_header + "*") if os.path.isdir(d)])
    # YYYYMM_xxx の数が一番大きいものを取り出す
    length = len(taskdirs)
    if length != 0:
        latest_dir = taskdirs[length-1]
        name = os.path.basename(latest_dir)
        # YYYYMM_xxx_yyy の xxx (番号)を取り出す
        number = int(name[7:10], base=10)
        # 次の番号は + 10 する
        number += 10
        numstr = f"{number:03d}"
    else:
        # 初期値は 010
        numstr = "010"

    dir_path = dir_header + f"{numstr}_{title}"

    logfile_path = f"{TASKLOGDIR}/{os.path.basename(dir_path)}.txt"

    return dir_path, logfile_path


def win32_create_shortcut(target_path, shortcut_path):
    shell = win32com.client.Dispatch("WScript.shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.WindowStyle = 1
    shortcut.Save()


def win32_start(path):
    shell = win32com.client.Dispatch("WScript.shell")
    shell.Run(path)


def create_task(title):
    # タスクフォルダとログファイルのパスを取得
    dir_path, logfile_path = get_task_dir_and_logfile_path(title)
    # タスクフォルダがなければ新規作成
    os.makedirs(dir_path, exist_ok=True)
    # ログファイルがなければ新規作成
    if not os.path.exists(logfile_path):
        with open(logfile_path, "w") as f:
            # ちょっとした記述を追加しておく
            f.write("\n\n\n\n\n")
            f.write("-" * 72 + "\n")
            today = datetime.today()
            f.write(
                f"{today.year:04d}{today.month:02d}{today.day:02d}\n\n\n")

    # ショートカットの作成
    shortcut_path = f"{dir_path}/{os.path.basename(logfile_path)}.lnk"
    win32_create_shortcut(logfile_path, shortcut_path)

    return dir_path, logfile_path, shortcut_path


if __name__ == "__main__":
    title = input("Input new task title (q:quit): ")
    if title != "q":
        dir, logfile, shortcut = create_task(title)
        print("Task Created:")
        print("task dir:", dir)
        print("task log:", logfile)
        print("shortcut:", shortcut)
        win32_start(dir)
        win32_start(logfile)

    # input('\nHit any key to finish. ')
