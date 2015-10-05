#!/bin/bash
# extract features, build model, evaluate model
# params:
#  paths trainfile evalfile [depths]

CRFSUITE=../tools/crfsuite
CONLLEVAL=../wnut_ner_evaluation/connlleval.pl
POSTAG_LIB=../tools/stanford-postagger.jar
POSTAG_MODEL=../tools/gate-EN-twitter.model

if [ $# -eq 0 ]; then
    echo "Usage: ./experiment.sh <evalfile> <paths> <trainfile> [comma,separated,brown,bitdepths]"
    exit 1
fi

# $1paths $2train $3eval $4depths
# extract features


# cleanup:
rm eval.temp.merged.conll eval.temp.conll eval.results eval.conll train.temp.merged.conll train.temp.conll temp.model

echo "== Feature extraction"

echo "=== evaluation set"
if [ ! -f $1.nolabels ]; then 
	echo "  generating plain text"
	./twocolumn-to-spacesep-nolabels.py $1 > $1.nolabels
fi	

if [ ! -f $1.postags ]; then
	echo "  generating pos tags"
	java -cp $POSTAG_LIB edu.stanford.nlp.tagger.maxent.MaxentTagger -model $POSTAG_MODEL -textFile $1.nolabels -outputFormat tsv -tokenize False  | awk '{print $NF}' > $1.postags
fi	

if [ ! -f $1.shapes ]; then
	echo "  generating word shapes"
	./shapes-and-lengths.py $1 > $1.shapes
fi	

if [ ! -f $1.neighbours ]; then
	echo "  generating neighbour window"
	./neighbours.py $1 > $1.neighbours
fi	

if [ ! -f $1.subgrams ]; then
	echo "  generating subgrams"
	./subgrams.py $1 > $1.subgrams
fi	

if [ ! -f $1.gaz ]; then
	echo "  generating gaz hits"
	./gaz.py $1 > $1.gaz
fi	

if [ ! -f $1.lm ]; then
	echo "  generating lang model weight"
	./lm-tuning.py langmodel.50000 $1 > $1.lm
fi	

./extract-features.py $1 $2 $4 > ./eval.temp.conll



echo "=== training set"
if [ ! -f $3.nolabels ]; then 
	echo "  generating plain text"
	./twocolumn-to-spacesep-nolabels.py $3 > $3.nolabels
fi	

if [ ! -f $3.postags ]; then
	echo "  generating pos tags"
	java -cp $POSTAG_LIB edu.stanford.nlp.tagger.maxent.MaxentTagger -model $POSTAG_MODEL -textFile $3.nolabels -outputFormat tsv -tokenize False  | awk '{print $NF}' > $3.postags
fi	

if [ ! -f $3.shapes ]; then
	echo "  generating word shapes"
	./shapes-and-lengths.py $3 > $3.shapes
fi	

if [ ! -f $3.neighbours ]; then
	echo "  generating neighbour window"
	./neighbours.py $3 > $3.neighbours
fi	

if [ ! -f $3.subgrams ]; then
	echo "  generating subgrams"
	./subgrams.py $3 > $3.subgrams
fi	

if [ ! -f $3.gaz ]; then
	echo "  generating gaz hits"
	./gaz.py $3 > $3.gaz
fi	

if [ ! -f $3.lm ]; then
	echo "  generating lang model weight"
	./lm-tuning.py langmodel.50000 $3 > $3.lm
fi	

./extract-features.py $1 $3 $4 > ./train.temp.conll

# merge required features
# join with tabs (crfsuite file format)
# this weird sed is to stop paste making lines of just \n\t\n , which get interpreted as characters by crfsuite, instead of sentence breaks

paste eval.temp.conll $1.postags $1.shapes $1.neighbours $1.subgrams $1.gaz $1.lm | sed $'s/^\t*$//g' > eval.temp.merged.conll
paste train.temp.conll $3.postags $3.shapes $3.neighbours $3.subgrams $3.gaz $3.lm | sed $'s/^\t*$//g' > train.temp.merged.conll


echo "== Training"
#$CRFSUITE learn -m temp.model ./train.temp.merged.conll > /dev/null
$CRFSUITE learn -m temp.model -p feature.minfreq=2  ./train.temp.merged.conll
echo "== Evaluating"
$CRFSUITE tag -m temp.model ./eval.temp.merged.conll > eval.results
paste -d " " $1 eval.results | sed $'s/^\t$//g' | tr '\t' ' ' > eval.conll
$CONLLEVAL < eval.conll