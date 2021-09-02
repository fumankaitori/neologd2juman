# -*- coding: utf-8 -*-

"""
neologdのエントリをjuman形式に変換する
(名詞 (普通名詞 ((見出し語 日本語) (読み にほんご))))

usage: python neologd2juman.py < mecab-user-dict-seed.20160509.csv
"""

import sys
import argparse
# if sys.version_info < (3, 0, 0) or sys.version_info > (3, 6):
#     print(sys.version_info)
#     raise Exception('This system requires 3.0 <= python <= 3.6')

# csv変換用（統計情報などがほしいわけでもないので、pandasではなくcsvで）
import csv
import jaconvV2
import re
import logging
logger = logging.getLogger(__file__)

RE_WHITE_SPACE = re.compile(r'\s+')
RE_HALF_BRACKETS = re.compile(r'\(|\)')


def return_subpos(raw):
    if raw[4] == "記号":
        return "記号"
    else:
        # 一般名詞
        if raw[5] == "一般":
            return "普通名詞"
        elif raw[5] == "サ変接続":
            return "サ変名詞"
        # 固有名詞
        elif raw[6] == "一般":
            return "固有名詞"
        elif raw[6] == "人名":
            return "人名"
        elif raw[6] == "地域":
            return "地名"
        elif raw[6] == "組織":
            return "組織名"
    return raw[5]


def my_csv_reader(csv_reader):
    """
    NULL回避のためのcsvジェネレータ
    :return:
    """
    while True:
        try:
            yield next(csv_reader)
        except csv.Error:
            pass
        except StopIteration:
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='%(prog)s [options] < INPUT')
    args = parser.parse_args()

    reader = csv.reader(sys.stdin)
    for i, raw in enumerate(my_csv_reader(reader)):
        # スペースを含んでいる単語は除外。jumanの辞書はスペース区切りのため誤動作につながる。
        if RE_WHITE_SPACE.findall(raw[0]):
            continue
        # 半角カッコを含む単語も誤動作につながる
        if RE_HALF_BRACKETS.findall(raw[0]):
            continue
        # 顔文字、絵文字はエラーの原因になっている可能性があるため、とりあえずはじく
        if raw[4] == "記号":
            continue

        pos = raw[4]
        subpos = return_subpos(raw)
        midasi = jaconvV2.h2z(raw[0])
        if any(jaconvV2.is_han(_) for _ in midasi):
            continue
        yomi = jaconvV2.kata2hira(jaconvV2.h2z(raw[11]))

        # 読みが長すぎると辞書のコンパイルに失敗するので、長すぎるものは除外
        if len(midasi) > 40 or len(yomi) > 40:
            logger.debug(f"[Warning] Following line was ignored because word"
                         f" entry length is >40. Entry={raw[0]}")
            continue

        print(f'({pos} ({subpos} ((見出し語 {midasi}) (読み {yomi}) )))')

        # System Message
        if i != 0 and i % 100000 == 0:
            sys.stderr.write("{}M lines done\n".format(i / 1000000))
        elif i != 0 and i % 10000 == 0:
            sys.stderr.write(".")
            sys.stderr.flush()

    sys.stderr.write("{} lines done\n".format(i))
