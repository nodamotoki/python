#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# このスクリプトは Windows のファイルをドラッグ&ドロップするだけで
# cygwin 向けに書かれたスクリプトを実行できるようにするために書かれた。
#
# 具体的には、このスクリプトは、渡された引数をすべて検査し、Windows の
# 絶対パスらしき箇所を cygwin 形式の絶対パスに変換し、cygwin 上のスク
# リプトに引き渡す。
#
# cygwin 上のスクリプトは、このスクリプトの第一引数に指定する。このス
# クリプトの第二引数以降は、第一引数に指定したスクリプトの引数となる。
#
# コマンドラインからの実行例
# python execute-on-cygwin.py echo "Hello World!"
#
# ファイルを引数にとるスクリプトの実行例
# python execute-on-cygwin.py script-name.py C:\path\to\file1 C:\path\to\file2
#
# ショートカットを作り、ファイル名の指定だけを省いてショートカットのリ
# ンク欄に書いておくと、そのショートカットにファイルをドロップすること
# で cygwin 上のスクリプトを実行できる。
#
# 但し、フォルダ名、ファイル名に日本語を含むとうまく動かない。

import os
import sys
import subprocess
import re
import traceback


def conv_path_win2unix(path):
    if re.search(r'^\w:\.*', path):
        path = path[0].lower() + path[1:]
        path = re.sub(r'^(\w):', r'/cygdrive/\1', path)
        path = re.sub(r'\\', r'/', path)

    return path


if __name__ == '__main__':
    try:
        # 先頭はarg[0]はこのスクリプトのファイル名なので省く
        argv = sys.argv[1:]

        # commandline はあとで bash -c に渡すので全体を "" で囲んでおく
        # commandline = '"'
        for arg in argv:
            # print(f'arg={arg}')
            tmp = conv_path_win2unix(arg)
            #tmp = arg

            # 空白を含む場合はダブルクオーテーションでクォートする。
            # commandline 全体がダブルクォートで囲まれるのでエスケーブ
            # しておく。
            if re.search('\s', tmp):
                tmp = r'\"' + tmp + r'\"'

            commandline += tmp
            commandline += ' '

        commandline = commandline[:-1]  # 最後の空白は消しておく
        # commandline += '"'
        # print(f'commandline={commandline}')

        os.chdir(r'C:/cygwin64/bin')
        subprocess.run(f'bash --login -i -c {commandline}')

    except:
        ei = sys.exc_info()
        print('Exception detected.')
        # スタックトレースの取得
        traceback.print_tb(ei[2])
        # throw された例外とその説明を表示
        print(f'\n  {ei[0]} {ei[1]}')

    # ファイルをドロップしたときにコンソール画面がすぐに消えないように
    # しておく。コマンドラインから実行されたときは必要ないけど、どう判
    # 定すればいい？
    input('\nHit any key to finish. ')
