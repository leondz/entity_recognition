#!/usr/bin/env python3
# params:
# 1. <conll training data path>
# 2. <brown clusters path>
# 3. <model file path>

print('init')

from collections import Counter
import nltk
from optparse import OptionParser
import pycrfsuite
import sys

# local imports
import er

# import feature extraction
from base_extractors import word2features, featurise

parser = OptionParser()
parser.add_option("-f", "--file", dest="infile",
                  help="read conll data from this file")
parser.add_option("-c", "--clusters", dest="clusterfile",
                  help="path to brown clusters file")
parser.add_option("-m", "--model", dest="modelfile",
                  help="path to CRFsuite model to use")
parser.add_option("-p", "--performance", dest="performance", action="store_true",
                  help="give performance summary", default=False)
parser.add_option("-o", "--output", dest="outfile",
                  help="file to write predicted labels to", default="")
parser.add_option("-O", "--full-output", dest="full_output", action="store_true",
                  help="write conll input rows to output file as well", default=False)


(options, args) = parser.parse_args()
if not options.infile:
	parser.error('please specify at least an input file')

if options.clusterfile:
	print('reading in brown clusters')
	brown_cluster = er.load_brown_clusters(options.clusterfile)
else:
	brown_cluster = {}

y, X = er.load_conll_file(options.infile)

tagger = pycrfsuite.Tagger()
tagger.open(options.modelfile)

print('building feature representations')

#for xseq,yseq in zip(X, y):
#	xrepr = featurise(xseq, brown_cluster)
#	print("Predicted:", ' '.join(tagger.tag(featurise(xseq))))
#	print("Correct:  ", ' '.join(yseq))

y_hat = [tagger.tag(featurise(xseq, brown_cluster)) for xseq in X]

if options.outfile:
	f = open(options.outfile, 'w')
	for seq in y_hat:
		for item in seq:
			f.write(item + "\n")
		f.write("\n")

if options.performance:
	info = tagger.info()

	print("\nTop likely transitions:")
	er.print_transitions(Counter(info.transitions).most_common(10))

	print("\nTop unlikely transitions:")
	er.print_transitions(Counter(info.transitions).most_common()[-10:])

	print("\nTop positive:")
	er.print_state_features(Counter(info.state_features).most_common(10))

	print("\nTop negative:")
	er.print_state_features(Counter(info.state_features).most_common()[-10:])	

	print("\n", er.bio_classification_report(y, y_hat))
