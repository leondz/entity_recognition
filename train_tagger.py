#!/usr/bin/env python3
# params:
# 1. <conll training data path>
# 2. <brown clusters path>

print('init')

import er
import nltk
import pycrfsuite
import sys
import time

# import feature extraction
from base_extractors import word2features, featurise

infile = sys.argv[1]
clusterfile = sys.argv[2]

print('reading in brown clusters')
brown_cluster = er.load_brown_clusters(clusterfile)

print('reading source data')
y_train, X_train = er.load_conll_file(infile)

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
    'max_iterations': 50,  # stop earlier
    'feature.possible_transitions': True,	# include transitions that are possible, but not observed
    'feature.possible_states': True			# include states that are possible, but not observed
})


print(trainer.get_params())

outfile = infile.split('/')[-1] + time.strftime('.%Y%m%d-%H%M%S') + '.crfsuite.model'
trainer.train(outfile)

print('model written to', outfile)