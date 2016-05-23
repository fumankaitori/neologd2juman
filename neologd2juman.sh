#!/bin/bash
# usage: bash ./neologd2juman.sh INPUT_neologd
# 今いるディレクトリ内に、dicファイル、intファイル、jumandic.dat、jumandic.patを生成する
# optionで出力ディレクトリを指定しようと思ったが、makepatは、実行した場所にjumandic.datがないとこけるので断念

binary_path=`dirname $0`
input_base=`basename $1`

echo 'Start...'

# neologdのmecab形式から、juman形式の辞書に変換
# また、文字数の多すぎるエントリや、絵文字、顔文字等の記号を排除
python ${binary_path}/codes/neologd2juman.py < $1 > ./${input_base}.dic

echo 'End Converting mecab-neologd-ipadic into juman format.'

# jumanで利用できる辞書（jumandic.dat、jumandic.pat）にコンパイル
/usr/local/opt/juman/libexec/juman/makeint ./${input_base}.dic

# メモリが溢れないようにintファイルを分割
split -l 500000 ./${input_base}.int ./${input_base}.int-

rm jumandic.dat
for int_file in ./${input_base}.int-*
do
  /usr/local/opt/juman/libexec/juman/dicsort ${int_file} >> jumandic.dat
done

/usr/local/opt/juman/libexec/juman/makepat ./${input_base}.int

echo 'End Compiling.'
