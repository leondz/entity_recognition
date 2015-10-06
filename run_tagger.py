#!/usr/bin/env python3
# params:
# 1. <conll training data path>
# 1. <brown clusters path>

print('init')

from itertools import chain
import nltk
import pycrfsuite
import sklearn
from sklearn.preprocessing import LabelBinarizer
import sys
import time

# import feature extraction
from base_extractors import word2features, featurise

print('reading in brown clusters')
brown_cluster = {}
for line in open(sys.argv[2], 'r'):
	line = line.strip()
	if not line:
		continue
	path,token = line.split()[0:2]
	brown_cluster[token] = path


test_sents = list(nltk.corpus.conll2002.iob_sents('esp.test'))

y_test = [[seq[-1] for seq in sent] for sent in test_sents]
X_test = [[seq[0] for seq in sent] for sent in test_sents]

trainer = pycrfsuite.Trainer(verbose=False)

print('building feature representations')

i = 0
for xseq,yseq in zip(X_train, y_train):
	xrepr = featurise(xseq, brown_cluster)
	trainer.append(xrepr, yseq)

	i += 1
	if not i % 100:
		print('.', end='')
		if not i % 1000:
			print(i, end='')
		sys.stdout.flush()
print(i)

trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'feature.minfreq': 2,

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True,
    # include states that are possible, but not observed
    'feature.possible_states': True
})


print(trainer.get_params())

trainer.train(sys.argv[1] + time.strftime('.%Y%m%d-%H%M%S') + '.crfsuite.model')