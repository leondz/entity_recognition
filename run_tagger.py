#!/usr/bin/env python3
# params:
# 1. <conll training data path>
# 2. <brown clusters path>
# 3. <model file path>

from optparse import OptionParser

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
parser.add_option("-s", "--stdout", dest="stdout", action="store_true",
                  help="write output to stdout", default=False)
parser.add_option("-O", "--full-output", dest="full_output", action="store_true",
                  help="write conll input rows to output file as well [not implemented]", default=False)
parser.add_option("-j", "--json", dest="json", action="store_true",
                  help="enable JSON mode - look for a top-level 'text' or 'tokens' field and add an 'entity_texts' field", default=False)
parser.add_option("-t", "--json-text", dest="json_text",
                  help="name of body text field in JSON record", default="")


(options, args) = parser.parse_args()

if not options.infile:
	parser.error('please specify at least an input file')


print('init')

from collections import Counter
import json
import nltk
import pycrfsuite
import sys

# local imports
import er

# import feature extraction
from base_extractors import word2features, featurise


if options.clusterfile:
	print('reading in brown clusters')
	brown_cluster = er.load_brown_clusters(options.clusterfile)
else:
	brown_cluster = {}

if not options.json:
	y, X = er.load_conll_file(options.infile)
else:
	if options.json_text:
		y, X = er.load_json_file(options.infile, options.json_text)
	else:
		y, X = er.load_json_file(options.infile)

tagger = pycrfsuite.Tagger()
tagger.open(options.modelfile)

print('building feature representations')

#for xseq,yseq in zip(X, y):
#	xrepr = featurise(xseq, brown_cluster)
#	print("Predicted:", ' '.join(tagger.tag(featurise(xseq))))
#	print("Correct:  ", ' '.join(yseq))

y_hat = [tagger.tag(featurise(xseq, brown_cluster)) for xseq in X]

out = False
if options.outfile:
	f = open(options.outfile, 'w')
	out = True

if options.stdout:
	out = True

if out:
	if not options.json:
		for seq in y_hat:
			for item in seq:
				if options.outfile:
					f.write(item + "\n")
				if options.stdout:
					print(item)
			if options.outfile:
				f.write("\n")
			if options.stdout:
				print()
	else:
		# this may require some work
		i = 0
		for line in open(options.infile, 'r'):
			if line.strip():
				entity_texts = er.chunk_tokens(X[i], y_hat[i])
				entry = json.loads(line.strip())
				entry['entity_texts'] = entity_texts
				print(json.dumps(entry))
			i += 1


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
