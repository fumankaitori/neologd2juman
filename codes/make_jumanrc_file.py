# -*- coding: utf-8 -*-
"""
.jumanrcファイルを探し出して、ファイルの書き換えを実施する

usage:
"""

import os
import re
import shutil
import logging
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

JUMAN_RC_FILE_TEMPLATE = """
(文法ファイル
        {path_default_dict}/dic
)

(品詞コスト
    ((*)                10)
    ((特殊 *)           100)
    ((動詞)             100)
    ((形容詞)           100)
    ((判定詞)           11)
    ((助動詞)           10)
    ((名詞 *)           100)
    ((名詞 数詞)            40)
    ((名詞 形式名詞)        70)
    ((名詞 副詞的名詞)      70)
    ((指示詞 *)         40)
    ((指示詞 副詞形態指示詞)    60)
    ((副詞 *)           100)
    ((助詞 *)           10)
    ((助詞 終助詞)          20)
    ((接続詞)           100)
    ((連体詞)           100)
    ((感動詞)           110)
    ((接頭辞 *)         50)
        ((接尾辞 名詞性述語接尾辞)  14)
    ((接尾辞 名詞性名詞接尾辞)  35)
    ((接尾辞 名詞性名詞助数辞)  35)
    ((接尾辞 名詞性特殊接尾辞)  35)
    ((接尾辞 形容詞性述語接尾辞)    14)
    ((接尾辞 形容詞性名詞接尾辞)    14)
    ((接尾辞 動詞性接尾辞)      14)
    ((未定義語 カタカナ)        1000)
    ((未定義語 アルファベット)  100)
    ((未定義語 その他)      1000)
)

(連接コスト重み 4)
(形態素コスト重み 1)

(コスト幅 0)

(辞書ファイル
        {path_default_dict}/dic
        {path_default_dict}/autodic
        {path_default_dict}/wikipediadic
        {path_new_dict}
)
"""


def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


def generate_new_jumanrc_file(path_juman_dict_dir,
                              path_new_juman_dict_dir):
    """* What you can do
    - It generates new jumanrc file

    * Output
    - Path to new .jumanrc file
    """
    new_jumanrc_path = os.path.join(path_juman_dict_dir, 'jumanrc')

    juman_template_sting = JUMAN_RC_FILE_TEMPLATE.format(
        path_default_dict=path_juman_dict_dir,
        path_new_dict=path_new_juman_dict_dir
    )
    with open(new_jumanrc_path, 'w') as f:
        f.write(juman_template_sting)

    return new_jumanrc_path


def edit_jumanrc_file(path_jumanrc_file,
                      path_new_juman_dict_dir):
    """* What you can do
    - You edit/create jumanrc file
    """
    with open(path_jumanrc_file, 'r') as f:
        jumanrc_content = f.read()

    extracted_pattern = re.match(r'\(辞書ファイル[^)]+\)', jumanrc_content)
    existing_content = jumanrc_content[:extracted_pattern.end()-2]
    existing_content += '\n\t{}'.format(path_new_juman_dict_dir)

    jumanrc_non_dict_nontent = re.sub(r'\(辞書ファイル[^)]+\)', '', jumanrc_content)

    new_jumanrc_content = jumanrc_non_dict_nontent + existing_content
    ## make copy of existing jumanrc
    shutil.copy(path_jumanrc_file, '{}__bk'.format(path_jumanrc_file))

    with open(path_jumanrc_file, 'w') as f:
        f.write(new_jumanrc_content)

    return path_jumanrc_file

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(usage="""python make_jumanrc_file.py --path-jumanrc [existing jumanrc]
    --path-juman-dict [path to existing juman dictionary]
    --path-new-juman-dic [path to new juman dictionary]""")
    parser.add_argument('--path-jumanrc', required=True, help='Path to existing .jumanrc. If there is not, put None instead.')
    parser.add_argument('--path-juman-dict', required=True, help='Path to existing juman dict direcotires.')
    parser.add_argument('--path-new-juman-dic', required=True, help='Path to new juman dict directory.')
    args = parser.parse_args()

    if args.path_jumanrc is None or args.path_jumanrc == 'None':
        if not os.path.exists(args.path_new_juman_dic):
            raise Exception('There is no directory at {}'.format(args.path_new_juman_dic))
        print(generate_new_jumanrc_file(args.path_juman_dict, args.path_new_juman_dic))
    else:
        print(edit_jumanrc_file(path_jumanrc_file=args.path_jumanrc,
                                path_new_juman_dict_dir=args.path_new_juman_dic))