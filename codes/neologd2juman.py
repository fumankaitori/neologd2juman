# -*- coding: utf-8 -*-

"""
neologdのエントリをjuman形式に変換する
(名詞 (普通名詞 ((見出し語 日本語) (読み にほんご))))

usage: python neologd2juman.py < mecab-user-dict-seed.20160509.csv
"""

import sys
import argparse
if sys.version_info < (3, 0, 0):
    raise Exception('This system requires python >= 3.x')

# csv変換用（統計情報などがほしいわけでもないので、pandasではなくcsvで）
import csv
import mojimoji
import jaconv

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

if __name__ == "__main__":


    parser = argparse.ArgumentParser(usage='%(prog)s [options] < INPUT')
    args = parser.parse_args()

    reader = csv.reader(sys.stdin)
    for i, raw in enumerate(my_csv_reader(reader)):
        # 顔文字、絵文字はエラーの原因になっている可能性があるため、とりあえずはじく
        if raw[4] == "記号":
            continue

        pos = raw[4]
        subpos = return_subpos(raw)
        midasi = mojimoji.han_to_zen(raw[0])
        daihyo = mojimoji.han_to_zen(raw[10])
        yomi = jaconv.kata2hira(raw[11])

        # 読みが長すぎると辞書のコンパイルに失敗するので、長すぎるものは除外
        if len(midasi) > 40 or len(yomi) > 40:
            continue

        info = {'pos': pos,
                'subpos': subpos,
                'midasi': midasi,
                'daihyo': daihyo,
                'yomi': yomi}
        print('({pos} ({subpos} ((見出し語 {midasi}) (読み {yomi}) (意味情報 "代表表記:{daihyo}/{yomi}"))))'.format(**info))

        # System Message
        if i != 0 and i % 100000 == 0:
            sys.stderr.write("{}M lines done\n".format(i / 1000000))
        elif i != 0 and i % 10000 == 0:
            sys.stderr.write(".")
            sys.stderr.flush()

    sys.stderr.write("{} lines done\n".format(i))