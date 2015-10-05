#!/usr/bin/env python

import sys

for line in open(sys.argv[1], 'r'):
	line = line.strip()
	if not line:
		print
		continue

	subgrams = []

	line = line.split()[0].lower()

#	subgrams.append('all-lower:'+line)

	if len(line) > 1:
		subgrams.append('suff='+line[-1])
		subgrams.append('pref='+line[:1])

	if len(line) > 2:
		subgrams.append('suff='+line[-2:])
		subgrams.append('pref='+line[:2])

	if len(line) > 3:
		subgrams.append('suff='+line[-3:])
		subgrams.append('pref='+line[:3])

	print "\t".join(subgrams)