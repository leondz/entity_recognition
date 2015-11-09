#!/usr/bin/env python3
# params:
# 1. <conll training data path>
# 2. <brown clusters path>
# 3. <model file path>

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="infile",
                  help="read data to be tagged (e.g. conll, json) from this file")
parser.add_option("-x", "--extractor", dest="extractor_module",
                  help="name of feature extractor python module", default="base_extractors")
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
parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help="dump debugging / progress info on stderr", default=False)


(options, args) = parser.parse_args()

if not options.infile:
	parser.error('please specify at least an input file')

if not options.modelfile:
	parser.error('please specify the model file to load for tagging')	

import sys
if options.verbose:
	print('init', file=sys.stderr)

from collections import Counter
import json
import nltk

# local imports
import er

t = er.Tagger(options.modelfile, options.extractor_module)

if options.clusterfile:
	if options.verbose:
		print('reading in brown clusters', file=sys.stderr)
	t.load_clusters(options.clusterfile)


out = False
if options.outfile:
	f = open(options.outfile, 'w')
	out = True

if options.stdout:
	out = True


if options.verbose:
	print('doing tagging', file=sys.stderr)


if not options.json:
	file_generator = er.load_conll_file(options.infile)
else:
	if options.json_text:
		file_generator = er.load_json_file(options.infile, options.json_text)
	else:
		file_generator = er.load_json_file(options.infile)

ys = []
y_hats=[]
for y, X, entry in file_generator:
	y_hat = t.tag(X)

	if out:
		if not options.json:
			for item in y_hat:
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
			entity_texts = er.chunk_tokens(X, y_hat)
			entry['entity_texts'] = list(set(entity_texts))
			print(json.dumps(entry))

	if options.performance:
		ys.append(y)
		y_hats.append(y_hat)


if options.performance:
	info = t.tagger.info()

	print("\nTop likely transitions:")
	er.print_transitions(Counter(info.transitions).most_common(10))

	print("\nTop unlikely transitions:")
	er.print_transitions(Counter(info.transitions).most_common()[-10:])

	print("\nTop positive:")
	er.print_state_features(Counter(info.state_features).most_common(10))

	print("\nTop negative:")
	er.print_state_features(Counter(info.state_features).most_common()[-10:])	

	print("\n", er.bio_classification_report(y, y_hat))
