#!/usr/bin/env python
import sys

lm = {}
max_freq = 0
for line in open(sys.argv[1], 'r'):
	line = line.strip()
	if not line:
		continue
	try:
		freq,tok = line.split()
	except:
		continue
	freq = int(freq)
	if freq > max_freq:
		max_freq = freq
	lm[tok] = freq


for line in open(sys.argv[2], 'r'):
	line = line.strip()
	if not line:
		print
		continue

	token,label = line.split()

	if token in lm:
		print "lm:" + str( lm[token] * 100 / float(max_freq) )
	else:
		print