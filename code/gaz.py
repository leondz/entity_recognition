#!/usr/bin/env python
import os
import sys

# summon gazetteers
gaz_root = '../../gazetteers/'

gaz = {}

DEBUG = False
LOWER_EVERYTHING = True
MAX_WINDOW_SIZE = 6
PHRASE_MIN_LEN = 3

# load as dict, with key = phrase, value = list of dicts

if True:
	for gaz_dir in os.listdir(gaz_root):
		if gaz_dir[0] == '.':
			continue
		if os.path.isfile(gaz_root + gaz_dir):
			continue

		for gaz_file in os.listdir(gaz_root + gaz_dir):
			if os.path.isdir(gaz_dir):
				continue
			if gaz_file[0] in ('.', '_'):
				continue
			if gaz_file[-3:] == '.db':
				continue

			print >> sys.stderr, 'Loading', gaz_dir, ':', gaz_file
			for line in open(gaz_root + gaz_dir + '/' + gaz_file):
				line = line.strip()
				if not line:
					continue
				if LOWER_EVERYTHING:
					line = line.lower()
				if line not in gaz:
					gaz[line] = []
				gaz[line].append(gaz_dir+'_'+gaz_file)
else:
	gaz = {"the green party":["organization"], "green":['colour']}



#sent = "I'm voting for The Green Party this time"
words = []
for line in open(sys.argv[1], 'r'):
	line = line.strip()

	if line:
		token,label = line.split()
#		token = token.replace('#', '')
		if LOWER_EVERYTHING:
			token = token.lower()
		words.append(token)

	if not line:
		if len(words):
			# things to mark future tokens
			feature_stack = {}

			for i in range(len(words) ):
				features = []
				if i not in feature_stack:
					feature_stack[i] = []
				for window in range(1, MAX_WINDOW_SIZE+1):
					start = i
					end = start + window

					if end > len(words):
						continue

					phrase = ' '.join(words[start:end])

					if DEBUG:
						print >> sys.stderr, start, end, phrase

					if gaz.has_key(phrase) and len(phrase) >= PHRASE_MIN_LEN:
						if DEBUG:
							print >> sys.stderr, 'MATCH!', gaz[phrase]

						for j in gaz[phrase]:
							features.append('in_gaz=' + j)
#							if window > 1:
#								features.append('gaz_len=' + j + "=" + str(window) )

						phrase_len = len(phrase.split())
						if phrase_len > 1:
							for k in range(i, i + phrase_len ):
								if k not in feature_stack:
									feature_stack[k] = []
								feature_stack[k] += list(features)

#							features.append('in_gaz_first=' + j)

				if DEBUG:
					print >> sys.stderr, 'FEATURES:', i, words[i], "\t" + "\t".join(set(features).union(set(feature_stack[i])))

				print "\t".join(set(features).union(set(feature_stack[i])))

		print
		words = []
		continue



