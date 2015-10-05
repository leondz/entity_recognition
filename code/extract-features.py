#!/usr/bin/env python
# takes two or three params: wcluster paths, conll file [, path bitdepths]
import sys

if len(sys.argv) > 3:
	depths = map(int, sys.argv[3].split(','))
else:
	depths = [4,6,10,20]

print >> sys.stderr, "With parameters:", 'paths =', sys.argv[1], 'conllfile =', sys.argv[2]

# wcluster format: path token count
class_path = {}
for line in open(sys.argv[1], 'r'):
	try:
		path, word, count = line.strip().split("\t")
	except:
		print >> sys.stderr, line
		die
	class_path[word] = path

prev_tok = ''
# conll format: token tag
for line in open(sys.argv[2], 'r'):
	line = line.strip()
	if not line:
		prev_tok = ''
		print
		continue

	token, tag = line.split()

	if token == '-DOCSTART-':
		continue

	try:
		path = class_path[token]
	except:
		path = None

	this_features = []

	if path:
		for depth in depths:
			this_features.append('p' + str(depth) + 'x' + path[:depth])
	
	features = list(this_features)
	if prev_tok and prev_tok in class_path and False:
		path = class_path[prev_tok]
		for d in depths:
			features.append('prev_p' + str(d) + 'x' + path[:d])

#	for prev_f in prev_features:
#		features.append('prev_' + prev_f)

	print tag + "\t" + "\t".join(features)

	prev_tok = token

