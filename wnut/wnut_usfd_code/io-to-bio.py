#!/usr/bin/env python
# assign bio tags to non-bio text in a conll-format file
# input example:  fish   location
# output example: fish   B-location


import sys

prev_label = 'O'
out_label = 'O'

for line in open(sys.argv[1], 'r'):
	line = line.strip()

	#skip blanks
	if not line:
		print
		continue

	token,label = line.split()
	if label == out_label:
		prev_label = label
		print token + " " + label
		continue

	label = label.lower()
	if label[0] != out_label:
		if prev_label == 'O':
			print token + "B-" + label
			prev_label = 'B'
		else:
			print token + "I-" + label
