#!/usr/bin/env python3
# params:
# 1. <conll training data path>
# 2. <brown clusters path>
# 3. <model file path>

print('init')

from collections import Counter
import er
import nltk
import pycrfsuite
import sys

# import feature extraction
from base_extractors import word2features, featurise

infile = sys.argv[1]
clusterfile = sys.argv[2]
modelfile = sys.argv[3]


print('reading in brown clusters')
brown_cluster = er.load_brown_clusters(clusterfile)

y, X = er.load_conll_file(infile)

tagger = pycrfsuite.Tagger()
tagger.open(modelfile)

print('building feature representations')

#for xseq,yseq in zip(X, y):
#	xrepr = featurise(xseq, brown_cluster)
#	print("Predicted:", ' '.join(tagger.tag(featurise(xseq))))
#	print("Correct:  ", ' '.join(yseq))

y_hat = [tagger.tag(featurise(xseq, brown_cluster)) for xseq in X]

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
