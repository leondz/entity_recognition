#!/usr/bin/env python3
# params:
# 1. <conll training data path>
# 2. <brown clusters path>

print('init')

import nltk
from optparse import OptionParser
import pycrfsuite
import sys
import time

# local imports
import er

# import feature extraction
from base_extractors import word2features, featurise

parser = OptionParser()
parser.add_option("-f", "--file", dest="infile",
                  help="read conll data from this file")
parser.add_option("-c", "--clusters", dest="clusterfile",
                  help="path to brown clusters file")
parser.add_option("-i", "--max-iter", dest="max_iterations",
                  help="number of training iterations", default=50)
parser.add_option("-m", "--min-freq", dest="min_freq",
                  help="minimum number of feature occurrences for inclusion", default=2)
parser.add_option("-v", "--verbose-training", dest="trainer_verbose", action="store_true",
                  help="output crfsuite progress during model training", default=False)
(options, args) = parser.parse_args()
if not options.infile:
	parser.error('please specify at least an input file')

if options.clusterfile:
	print('reading in brown clusters')
	brown_cluster = er.load_brown_clusters(options.clusterfile)
else:
	brown_cluster = {}

print('reading source data')
y_train, X_train = er.load_conll_file(options.infile)

trainer = pycrfsuite.Trainer(verbose=options.trainer_verbose)

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
    'feature.minfreq': options.min_freq,
    'max_iterations': options.max_iterations,  # stop earlier
    'feature.possible_transitions': True,	# include transitions that are possible, but not observed
    'feature.possible_states': True			# include states that are possible, but not observed
})


print(trainer.get_params())

outfile = options.infile.split('/')[-1] + time.strftime('.%Y%m%d-%H%M%S') + '.crfsuite.model'
trainer.train(outfile)

print('model written to', outfile)