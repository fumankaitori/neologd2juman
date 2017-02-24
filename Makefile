install:
	wget --no-check-certificate https://github.com/neologd/mecab-ipadic-neologd/tarball/master -O mecab-ipadic-neologd.tar
	tar -xvf mecab-ipadic-neologd.tar
	xz -dc ./neologd-mecab-ipadic-neologd-*/seed/mecab-user-dict-seed.*.csv.xz > ./mecab-user-dict-seed.csv
	bash neologd2juman.sh mecab-user-dict-seed.csv
	bash install-dictionary.sh
	mv mecab-user-dict-seed.csv.dic neologd-user-dict.dic

clean:
	rm mecab-ipadic-neologd.tar
	rm -r neologd-mecab-ipadic-neologd-*
	rm -r mecab-user-dict-seed.csv*
