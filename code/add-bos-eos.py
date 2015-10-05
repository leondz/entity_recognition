#!/usr/bin/env python

# add eos, bos lines to conll-formatted tweets, as per wnut15 convention

import sys

out_of_seq = True
for line in open(sys.argv[1], 'r'):
	line = line.strip()

	if not line:
		if not out_of_seq:
			print "EOS O"
		out_of_seq = True
		print

	else:
		line = line.replace("\t", " ")
		if out_of_seq:
			print "BOS O"
			out_of_seq = False
		print line

if not out_of_seq:
	print "EOS O"