# entity-recognition

## Intro
Framework for doing NER and other types of entity recognition in Python.

Baseline feature extraction relies on Brown clusters and typical NER features, similar to Roth & Ratinov 2009. We use CRFsuite and try to keep things modular and simple, so you're not stuck to just NEs - parts of speech, MWEs, temporal expressions and the whole smørrebrød of entity classes are up for grabs with this framework; simply adjust training data and labels to taste.

## Features
* Pluggable feature generation
* Support for Reddit/Twitter JSON formats
* State-of-the-art Twitter NER performance out-of-the-box

## Running
To get started, run `./train_tagger.py --help`

Toy data in `datasets/` top-level directory.

Should you like to tag data with your code, `./run_tagger.py --help` is your friend. Remember to keep the Brown clusters around!

For example, to learn a model from the Ritter NER CoNLL data, and then apply it to some Reddit JSON, try this:

    $ ./train_tagger.py -f datasets/ritter.ner.conll \
      --clusters brown_paths/gha.250M-c2000.paths --output \ 
      ritter.socmed.crfsuite.model
    $ ./run_tagger.py -f datasets/RC_2013-04.1000.json \ 
      -c brown_paths/gha.250M-c2000.paths \ 
      --model ritter.socmed.crfsuite.model \ 
      --json --json-text body --stdout 

An "entity_texts" top-level field is added, containing extracted entities. For example:

    {
    	"archived": true, 
    	"author": "walrusboy", 
    	"author_flair_css_class": null, 
    	"author_flair_text": null, 
    	"body": "Quick, someone photoshop Natalie Portman!",
    	"controversiality": 0, 
    	"created_utc": "1364774484", 
    	"distinguished": null, 
    	"downs": 0,
    	"edited": false, 
    	"entity_texts": ["Natalie Portman"],
    	"gilded": 0, 
    	"id": "c95zmil", 
    	"link_id": 
    	"name": "t1_c95zmil", 
    	"parent_id": "t3_1bddiw", 
    	"removal_reason": null, 
    	"retrieved_on": 1431716826, 
    	"score": 1, 
    	"score_hidden": false, 
    	"subreddit": "pics", 
    	"subreddit_id": "t5_2qh0u", 
    	"t3_1bddiw", 
    	"ups": 1
    }

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

> Leon Derczynski, Isabelle Augenstein, Kalina Bontcheva (2015)<br />
> USFD: Twitter NER with Drift Compensation and Linked Data<br />
> Proceedings of the ACL Workshop on Noisy User-generated Text (W-NUT)<br />
> [[Paper]](https://aclweb.org/anthology/W/W15/W15-4306.pdf) [[bib]](https://aclweb.org/anthology/W/W15/W15-4306.bib)

Tools under active development until at least 2019 as part of the PHEME and COMRADES EU projects: www.pheme.eu
