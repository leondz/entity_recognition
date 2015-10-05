#!/usr/bin/env python

import sys

sentence = []

contexts = [[-2], [-1], [0], [1], [2], [-1, 0], [0, 1], [-2, -1], [1, 2]]

for line in open(sys.argv[1]):
	line = line.strip()

	if line:
		token = line.split()[0]
		sentence.append(token)

	else:
		# the magic
		for i in range(len(sentence)):
			features = []
			for context in contexts:
				if i+max(context) < len(sentence) and i+min(context) >= 0:
					context_tokens = []
					for offset in context:
						context_tokens.append(sentence[i+offset])
					feature= 'w[' + ','.join(map(str, context)) + ']=' + '|'.join(context_tokens)
					features.append(feature)

			print "\t".join(features)




#			this = sentence[i]

#			print "\t".join(["w[-1]="+prev, "w[0]="+this, "w[+1]="+next, 'w[-1,0]='+prev+'|'+this, 'w[0,1]='+this+'|'+next])
#			print "\t".join(["w[-1]="+prev, "w[0]="+this, "w[+1]="+next])

		sentence = []
		print
