# entity-recognition

## Intro
Framework for doing NER and other types of entity recognition in Python.

Baseline feature extraction relies on Brown clusters and typical NER features, similar to Roth & Ratinov 2009. We use CRFsuite and try to keep things modular and simple, so you're not stuck to just NEs - parts of speech, MWEs, temporal expressions and the whole smørrebrød of entity classes are up for grabs with this framework; simply adjust training data accordingly.

## Features
* Pluggable feature generation
* Support for Reddit/Twitter JSON formats
* State-of-the-art Twitter NER performance out-of-the-box

## Running
To get started, run `./train_tagger.py --help`

Toy data in `datasets/` top-level directory.

Should you like to tag data with your code, `./run_tagger.py --help` is your friend. Remember to keep the Brown clusters around!

## Dependencies
At least:

* Python 3
* NLTK
* pycrfsuite
* sklearn
* scipy
* numpy

Check you're using Python 3, with `python -V` (THAT'S A BIG V). Next, try something like:

    $ sudo easy_install3 -U pip
    $ sudo pip3 install numpy scipy sklearn pycrfsuite nltk

Then go for two cups of tea / one brief fika, after troubleshooting errors. If you get super stuck, sometimes it helps to try your distribution's Python 3 packages for numpy and scipy, and then upgrade them with something like:

    $ sudo pip3 install -U numpy
    $ sudo pip3 install -U scipy

## Hints and tips

If you use Brown clusters (and we recommend them!), this system expects cluster paths in binary branch format - à la `wcluster` - as opposed to base 10 paths, like from `JCLUSTER`. If you're not sure how many Brown clusters to use, check out our 3D interactive [guide to tuning Brown clustering](http://www.derczynski.com/sheffield/brown-tuning/).

## Reference
If you use this work, please cite our paper:

> USFD: Twitter NER with Drift Compensation and Linked Data
> L Derczynski, I Augenstein, K Bontcheva
> Proceedings of the ACL Workshop on Noisy User-generated Text (W-NUT)

Tools under active development until at least 2017 as part of the PHEME project: www.pheme.eu
