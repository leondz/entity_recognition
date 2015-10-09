#!/usr/bin/env python3
import nltk
import sys

for line in open(sys.argv[1], 'r'):
	line = line.strip()
	print("\tO\n".join(nltk.word_tokenize(line)) + "\tO\n")
