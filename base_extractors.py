

# X : list of lists of instances, each instance is a list of feature reprs
# y : list of lists of labels

def word2features(sent, i):
    word = sent[i]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
    ]
    if i > 0:
        word1 = sent[i-1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
        ])
    else:
        features.append('EOS')
                
    return features

# takes a list of token/label pairs; returns a list of [feature]/label pairs
def featurise(sentence, brown_cluster = {}):

	sentence_repr = []

	for i in range(len(sentence)):
		features = []

		word = sentence[i]
		if word in brown_cluster:
			for j in range(1,len(brown_cluster[word])+1):
				features.append('p' + str(j) + 'b' + brown_cluster[word][0:j])

		features += word2features(sentence, i)

		sentence_repr.append(features)

	return(sentence_repr)