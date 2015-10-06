#!/usr/bin/env python
import re
import sys

for line in open(sys.argv[1], 'r'):

	line = line.strip()

	if not line:
		print
		continue

	token = line.split()[0]

	shape = re.sub('[A-Z]', 'X', token)
	shape = re.sub('[a-z]', 'x', shape)
	shape = re.sub('[0-9]', '0', shape)
	shape = re.sub('#', '#', shape)
	shape = re.sub('[^A-Za-z0-9#]', '.', shape)
	
	shapeshort = re.sub('X+', 'X', shape)
	shapeshort = re.sub('x+', 'x', shapeshort)
	shapeshort = re.sub('0+', '0', shapeshort)
	shapeshort = re.sub('#+', '#', shapeshort)
	shapeshort = re.sub('\.+', '.', shapeshort)
	
	shape = "shape-" + shape
	shapeshort = "shapeshort-" + shapeshort
	length = "length-" + str(len(token))

	print "\t".join([length, shape, shapeshort])