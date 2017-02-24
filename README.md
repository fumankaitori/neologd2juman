# neologd2juman

Convert `mecab-ipadic-neologd` to [Juman](http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN) dictionary

You're able to use this dictionary file for [Juman++](http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN++) also.

## Required

- Python (>= 3.x)
- Juman
- mojimoji
  - python package: convert one-byte character to two-byte character
- jaconv
  - python package: convert katakana to hiragana
- mecab-ipadic-neologd
  - See https://github.com/neologd/mecab-ipadic-neologd

## Install


```
make
```

If there is no error, you see following message at end of make

```
New juman dictionary is at /usr/local/share/juman/juman-neologd-dic
New jumanrc file is at /usr/local/share/juman/jumanrc
```


## Manual Installation

### 1. Preparation

You need to install `mecab-ipadic-neologd` and unzip `seed/mecab-user-dict-seed.*.csv.xz`


### 2. Generate juman-neologd dictionary

You can run the shell script packing a series of steps:

```
$ bash neologd2juman.sh INPUT
```

If you run above script, you can obtain 4 or more files in the running directory.

- INPUT.dic
- INPUT.int
  - INPUT.int-* (splitted files of INPUT.int) if INPUT.int is large
- jumandic.dat
- jumandic.pat

INPUT.dic is text file of Juman dictionary format obtained by this script. Other files are made by Juman scripts.

Example of Juman dictionary format:

```
(名詞 (組織名 ((見出し語 エンジャパン（株）) (読み えんじゃぱんかぶしきがいしゃ) (意味情報 "代表表記:エン・ジャパン株式会社/えんじゃぱんかぶしきがいしゃ"))))
(名詞 (地名 ((見出し語 西新宿駅) (読み にししんじゅくえき) (意味情報 "代表表記:西新宿駅/にししんじゅくえき"))))
(名詞 (固有名詞 ((見出し語 新宿アイランドタワー) (読み しんじゅくあいらんどたわー) (意味情報 "代表表記:新宿アイランドタワー/しんじゅくあいらんどたわー"))))
```

### 3. Edit your .jumanrc file

You should add the path of Juman dictionary to `.jumanrc`.
You may create other `jumanrc` instead of default `.jumanrc`.

```
(辞書ファイル
        /usr/local/Cellar/juman/7.01/share/juman/dic
        /usr/local/Cellar/juman/7.01/share/juman/autodic
        /usr/local/Cellar/juman/7.01/share/juman/wikipediadic
        /your/jumandic/dir <- You write generated dictionary here!
)
```

# Use dictionary for Juman++

Use `neologd-user-dict.dic` for Juman++. 
`neologd-user-dict.dic` is generated your make process.

You're supposed to download [Juman++](http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN++) and install it.

When you made download Juman++ and made unzip, you see following directories.

```
% ls 
COPYING			VERSION			configure.ac		missing
INSTALL			aclocal.m4		depcomp			sample
Makefile.am		compile			dict-build		script
Makefile.in		config.guess		install-sh		src
README.md		config.sub		jumanpp-manual.pdf
README_ja.md		configure		jumanpp-resource
```

Go to `./dict-build`, and you see `userdic/` there.
You copy `neologd-user-dict.dic` into `userdic/`

After that, you make dictionary for juman++.
With this command, the script sets new dictioanry for your Juman++.

```
% cd dict-build
% cp [PATH-TO-YOUR neologd-user-dict.dic FILE] userdic/neologd-user-dict.dic
% make
% [sudo] ./install.sh
```


# Comparison of Juman output

## Juman

You can call new dictionary with `-r` flag of Juman

```
echo "[input sentence here]" | juman -r [path to jumanrc file]
```


Before adding:

```
$ echo "エン・ジャパン（株）は、西新宿駅の近くにある新宿アイランドタワー内の会社だ。" | juman
エン エン エン 未定義語 15 カタカナ 2 * 0 * 0 NIL
・ ・ ・ 特殊 1 記号 5 * 0 * 0 NIL
ジャパン じゃぱん ジャパン 名詞 6 地名 4 * 0 * 0 "代表表記:ジャパン/じゃぱん 地名:国:別称:日本"
（ （ （ 特殊 1 括弧始 3 * 0 * 0 NIL
株 かぶ 株 名詞 6 普通名詞 1 * 0 * 0 "代表表記:株/かぶ 漢字読み:訓 カテゴリ:抽象物 ドメイン:ビジネス;無し 多義"
） ） ） 特殊 1 括弧終 4 * 0 * 0 NIL
は は は 助詞 9 副助詞 2 * 0 * 0 NIL
、 、 、 特殊 1 読点 2 * 0 * 0 NIL
西新 にしじん 西新 名詞 6 地名 4 * 0 * 0 "自動獲得:Wikipedia Wikipedia上位語:地名/ちめい"
宿駅 しゅくえき 宿駅 名詞 6 普通名詞 1 * 0 * 0 "代表表記:宿駅/しゅくえき カテゴリ:場所-施設 ドメイン:交通"
の の の 助詞 9 接続助詞 3 * 0 * 0 NIL
近く ちかく 近く 名詞 6 普通名詞 1 * 0 * 0 "代表表記:近く/ちかく カテゴリ:場所-機能;時間 反義:名詞-普通名詞:遠く/とおく 形容詞派生:近い/ちかい"
に に に 助詞 9 格助詞 1 * 0 * 0 NIL
ある ある ある 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:有る/ある 補文ト 反義:形容詞:無い/ない"
新宿 しんじゅく 新宿 名詞 6 地名 4 * 0 * 0 "代表表記:新宿/しんじゅく 地名:日本:東京都:区"
アイランド あいらんど アイランド 名詞 6 普通名詞 1 * 0 * 0 "代表表記:アイランド/あいらんど カテゴリ:場所-自然"
タワー たわー タワー 名詞 6 普通名詞 1 * 0 * 0 "代表表記:タワー/たわー カテゴリ:場所-施設"
内 ない 内 接尾辞 14 名詞性名詞接尾辞 2 * 0 * 0 "代表表記:内/ない"
の の の 助詞 9 接続助詞 3 * 0 * 0 NIL
会社 かいしゃ 会社 名詞 6 普通名詞 1 * 0 * 0 "代表表記:会社/かいしゃ カテゴリ:組織・団体;場所-施設 ドメイン:ビジネス"
だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2 NIL
。 。 。 特殊 1 句点 1 * 0 * 0 NIL
EOS
```

After Adding:

```
$ echo "エン・ジャパン（株）は、西新宿駅の近くにある新宿アイランドタワー内の会社だ。" | juman -r jumanrc
エン・ジャパン（株） えんじゃぱんかぶしきがいしゃ エン・ジャパン（株） 名詞 6 組織名 6 * 0 * 0 "代表表記:エン・ジャパン株式会社/えんじゃぱんかぶしきがいしゃ"
は は は 助詞 9 副助詞 2 * 0 * 0 NIL
、 、 、 特殊 1 読点 2 * 0 * 0 NIL
西新宿駅 にししんじゅくえき 西新宿駅 名詞 6 固有名詞 3 * 0 * 0 "代表表記:西新宿駅/にししんじゅくえき"
@ 西新宿駅 にししんじゅくえき 西新宿駅 名詞 6 地名 4 * 0 * 0 "代表表記:西新宿駅/にししんじゅくえき"
の の の 助詞 9 接続助詞 3 * 0 * 0 NIL
近く ちかく 近く 名詞 6 普通名詞 1 * 0 * 0 "代表表記:近く/ちかく カテゴリ:場所-機能;時間 反義:名詞-普通名詞:遠く/とおく 形容詞派生:近い/ちかい"
に に に 助詞 9 格助詞 1 * 0 * 0 NIL
ある ある ある 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:有る/ある 補文ト 反義:形容詞:無い/ない"
新宿アイランドタワー しんじゅくあいらんどたわー 新宿アイランドタワー 名詞 6 固有名詞 3 * 0 * 0 "代表表記:新宿アイランドタワー/しんじゅくあいらんどたわー"
内 ない 内 接尾辞 14 名詞性名詞接尾辞 2 * 0 * 0 "代表表記:内/ない"
の の の 助詞 9 接続助詞 3 * 0 * 0 NIL
会社 かいしゃ 会社 名詞 6 普通名詞 1 * 0 * 0 "代表表記:会社/かいしゃ カテゴリ:組織・団体;場所-施設 ドメイン:ビジネス"
だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2 NIL
。 。 。 特殊 1 句点 1 * 0 * 0 NIL
EOS
```

"エン・ジャパン（株）", "西新宿駅" and "新宿アイランドタワー" are regardes as one morphemes by neologd.

## Juman++

Before adding:

```
エン エン エン 名詞 6 人名 5 * 0 * 0 "代表表記:エン/エン 自動獲得:Wikipedia Wikipedia人名 Wikipedia名 カタカナ 記英数カ"
・ ・ ・ 特殊 1 記号 5 * 0 * 0 "代表表記:・/・"
ジャパン じゃぱん ジャパン 名詞 6 地名 4 * 0 * 0 "代表表記:ジャパン/じゃぱん 地名:国:別称:日本 カタカナ 記英数カ"
（ （ （ 特殊 1 括弧始 3 * 0 * 0 "代表表記:（/（ 記号 記英数カ"
株 かぶ 株 名詞 6 普通名詞 1 * 0 * 0 "代表表記:株/かぶ 漢字読み:訓 カテゴリ:抽象物 ドメイン:ビジネス;無し 多義 漢字"
） ） ） 特殊 1 括弧終 4 * 0 * 0 "代表表記:）/） 記号 記英数カ"
は は は 助詞 9 副助詞 2 * 0 * 0 NIL
、 、 、 特殊 1 読点 2 * 0 * 0 "代表表記:、/、 記号 記英数カ"
西 にし 西 名詞 6 普通名詞 1 * 0 * 0 "代表表記:西/にし 漢字読み:訓 カテゴリ:場所-機能 漢字"
新宿 しんじゅく 新宿 名詞 6 地名 4 * 0 * 0 "代表表記:新宿/しんじゅく 地名:日本:東京都:区 漢字"
駅 えき 駅 名詞 6 普通名詞 1 * 0 * 0 "代表表記:駅/えき 漢字読み:音 地名末尾 カテゴリ:場所-施設 ドメイン:交通 漢字"
の の の 助詞 9 接続助詞 3 * 0 * 0 NIL
近く ちかく 近く 名詞 6 普通名詞 1 * 0 * 0 "代表表記:近く/ちかく カテゴリ:場所-機能;時間 反義:名詞-普通名詞:遠く/とおく 形容詞派生:近い/ちかい"
に に に 助詞 9 格助詞 1 * 0 * 0 NIL
ある ある ある 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:有る/ある 補文ト 反義:形容詞:無い/ない"
新宿 しんじゅく 新宿 名詞 6 地名 4 * 0 * 0 "代表表記:新宿/しんじゅく 地名:日本:東京都:区 漢字"
アイランドタワー アイランドタワー アイランドタワー 未定義語 15 カタカナ 2 * 0 * 0 "代表表記:アイランドタワー/アイランドタワー 品詞推定:名詞 カタカナ 記英数カ"
内 ない 内 接尾辞 14 名詞性名詞接尾辞 2 * 0 * 0 "代表表記:内/ない 漢字"
の の の 助詞 9 接続助詞 3 * 0 * 0 NIL
会社 かいしゃ 会社 名詞 6 普通名詞 1 * 0 * 0 "代表表記:会社/かいしゃ カテゴリ:組織・団体;場所-施設 ドメイン:ビジネス 漢字"
だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2 NIL
。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。 記号 記英数カ"
EOS
```


After Adding:

```
% echo "エン・ジャパン（株）は、西新宿駅の近くにある新宿アイランドタワー内の会社だ。" | jumanpp
エン・ジャパン（株） えんじゃぱんかぶしきがいしゃ エン・ジャパン（株） 名詞 6 組織名 6 * 0 * 0 "代表表記:エン・ジャパン/えんじゃぱんかぶしきがいしゃ"
は は は 助詞 9 副助詞 2 * 0 * 0 NIL
、 、 、 特殊 1 読点 2 * 0 * 0 NIL
西新宿駅 にししんじゅくえき 西新宿駅 名詞 6 固有名詞 3 * 0 * 0 "代表表記:西新宿駅/にししんじゅくえき"
の の の 助詞 9 接続助詞 3 * 0 * 0 NIL
近く ちかく 近く 名詞 6 普通名詞 1 * 0 * 0 "代表表記:近く/ちかく カテゴリ:場所-機能;時間 反義:名詞-普通名詞:遠く/とおく 形容詞派生:近い/ちかい"
に に に 助詞 9 格助詞 1 * 0 * 0 NIL
ある ある ある 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:有る/ある 補文ト 反義:形容詞:無い/ない"
新宿 しんじゅく 新宿 名詞 6 地名 4 * 0 * 0 "代表表記:新宿/しんじゅく 地名:日本:東京都:区"
アイランドタワー アイランドタワー アイランドタワー 未定義語 15 その他 1 * 0 * 0 "品詞推定:名詞"
内 ない 内 接尾辞 14 名詞性名詞接尾辞 2 * 0 * 0 "代表表記:内/ない"
の の の 助詞 9 接続助詞 3 * 0 * 0 NIL
会社 かいしゃ 会社 名詞 6 普通名詞 1 * 0 * 0 "代表表記:会社/かいしゃ カテゴリ:組織・団体;場所-施設 ドメイン:ビジネス"
だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2 NIL
。 。 。 特殊 1 句点 1 * 0 * 0 NIL
EOS
```

You see following improvement,

- `エン・ジャパン（株）`
- `西新宿駅`
