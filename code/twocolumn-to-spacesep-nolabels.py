#!/usr/bin/python

import re
import sys

"""
script to map two-column conll-style pos tagging datasets into space-separated plain tokens, e.g.

the DT
IG NNP
Metall NNP
is VBZ
demanding VBG
a DT

to

An avocet is a small , cute bird .

"""

import sys

infile_name = sys.argv[1]
infile = open(infile_name, 'r')

out_line = ''

for line in infile:
    if not line.strip():
        if out_line:
            print out_line
        out_line = ''
        continue

    try:    
        (token, tag) = re.split('\s+', line.strip())
    except Exception, e:
        print >> sys.stderr, 'Failed on:', line
        print >> sys.stderr, re.split('\S+', line.strip())
        print >> sys.stderr, e
        sys.exit()
    out_line += '%s ' % (token)
