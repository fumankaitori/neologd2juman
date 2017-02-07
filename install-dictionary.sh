#!/usr/bin/env bash
binary_path=`dirname $0`

## juman辞書の場所を検索
path_juman_dir_path=`python3 ${binary_path}/codes/find_juman_system_dic.py "/usr/"`
res_find_juman=$?

if [ $res_find_juman -eq 1 ]; then
    echo "Failed to find juman from your system. End."
    exit 1
elif [ $res_find_juman -eq 2 ]; then
    echo "Failed to find juman from your system. End."
    exit 1
else
    :
fi

echo "Your juman dictionary at "${res_find_juman}

## コンパイル済みの辞書を移動
path_generated_juman_dic=$path_juman_dir_path/juman-neologd-dic
if [ -d $path_generated_juman_dic ]; then
    # 古い辞書は削除
    rm -rf $path_generated_juman_dic
    echo "Deleted old dictionary files"
else
    :
fi

echo "Now installing dictionary files..."
mkdir $path_generated_juman_dic
mv jumandic.dat $path_generated_juman_dic
mv jumandic.pat $path_generated_juman_dic


echo "Now editing jumanrc file..."
## jumanrcファイルの検索
path_juman_rc_file=`python3 ${binary_path}/codes/find_jumanrc_file.py`
## jumanrcファイルの加工, または新規作成
path_generated_juman_rc=`python3 ${binary_path}/codes/make_jumanrc_file.py --path-jumanrc ${path_juman_rc_file} --path-juman-dict ${path_juman_dir_path} --path-new-juman-dic ${path_generated_juman_dic}`
res_make_jumanrc=$?

if [ $res_make_jumanrc -eq 1 ]; then
    echo "Failed to find juman from your system. End."
    exit 1
elif [ $res_make_jumanrc -eq 2 ]; then
    echo "Failed to find juman from your system. End."
    exit 1
else
    :
fi

echo "New juman dictionary is at ${path_generated_juman_dic}
New jumanrc file is at ${path_generated_juman_rc}"