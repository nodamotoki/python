#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 

import os
import sys
import subprocess
import re
import traceback

if __name__ == "__main__":
    try:
        with open('saved-drop-file-name.txt', 'w') as f:
            for v in sys.argv:
                f.write(v)
                f.write('\n')

    except:
        ei = sys.exc_info()
        print("Exception detected.")
        # スタックトレースの取得
        traceback.print_tb(ei[2])
        # throw された例外とその説明を表示
        print(f'\n  {ei[0]} {ei[1]}')

    # ファイルをドロップしたときにコンソール画面がすぐに消えないようにしておく
    # コマンドラインから実行されたときは必要ないけど、どう判定すればいい？
    input("\nHit any key to finish. ")
