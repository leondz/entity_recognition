#!/usr/bin/env python3

from itertools import chain
import json
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer


def load_brown_clusters(cluster_file_path):
	brown_cluster = {}
	for line in open(cluster_file_path, 'r'):
		line = line.strip()
		if not line:
			continue
		path,token = line.split()[0:2]
		brown_cluster[token] = path
	return brown_cluster

def load_conll_file(conll_file_path):
	y_seq = []
	X_seq = []
	for line in open(conll_file_path,'r'):
		line = line.strip().split()
		if not len(line):
			yield(y_seq, X_seq, None)
			y_seq = []
			X_seq = []
			continue

		y_seq.append(line[-1])
		X_seq.append(line[0])
	
	if y_seq and X_seq:
		yield(y_seq, X_seq)

def load_json_file(json_file_path, text_field='text'):
	for line in open(json_file_path, 'r'):
		if line.strip():
			try:
				entry = json.loads(line)
				if 'tokens' not in entry:
					X_seq = nltk.word_tokenize(entry[text_field])
				else:
					X_seq = entry['tokens']
				yield([None]*len(X_seq), X_seq, entry)
			except ValueError:
				continue

def bio_classification_report(y_true, y_pred):
    """
    Classification report for a list of BIO-encoded sequences.
    It computes token-level metrics and discards "O" labels.
    
    Note that it requires scikit-learn 0.15+ (or a version from github master)
    to calculate averages properly!
    """
    lb = LabelBinarizer()
    y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
    y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))
        
    tagset = set(lb.classes_) - {'O'}
    tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
    class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}
    
    return classification_report(
        y_true_combined,
        y_pred_combined,
        labels = [class_indices[cls] for cls in tagset],
        target_names = tagset,
        digits=4,
    )

def print_transitions(trans_features):
    for (label_from, label_to), weight in trans_features:
        print("%-6s \t-> \t%-7s \t%0.6f" % (label_from, label_to, weight))

def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%-6s \t%s \t%0.6f" % (label, attr, weight)) 	

# extract entities prefixed in BIO scheme
def chunk_tokens(tokens, labels):
	if len(tokens) != len(labels):
		raise Exception('different counts of tokens and labels')

	entities = []
	entity_tokens = []
	prev_state = ''
	for i in range(len(tokens)):
		token = tokens[i]
		state = labels[i][0]

		if state == 'I':
			entity_tokens.append(token)

		if state == 'B': 
			if entity_tokens:
				entities.append(' '.join(entity_tokens))
			entity_tokens = [token]

		if state == 'O'	and len(entity_tokens):
			entities.append(' '.join(entity_tokens))
			entity_tokens = []

	if len(entity_tokens):
		entities.append(' '.join(entity_tokens))

	return entities

