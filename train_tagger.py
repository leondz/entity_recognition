#!/usr/bin/env python
# params:
# 1. <conll training data path>
# 1. <brown clusters path>

from itertools import chain
import nltk
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
import sys

brown_cluster = {}
for line in open(sys.argv[2], 'r'):
	line = line.strip()
	if not line:
		continue
	path,token = line.split()[0:2]
	brown_cluster[token] = path