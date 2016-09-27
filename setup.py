#!/usr/bin/env python3

from setuptools import setup

setup(
	author='Leon Derczynski, Isabelle Augenstein',
	author_email='leonderczynski@gmail.com',
	include_package_data=True,
	install_requires=['python-crfsuite', 'nltk', 'sklearn', 'scipy', 'numpy', 'json'],
	license='Apache 2.0',
	long_description=open('README.md').read(),
	name='entity_recognition',
	scripts=['er'],
	summary='Toolkit for recognising named entities through structured labeling',
	description='Toolkit for recognising named entities through structured labeling',
	url='https://github.com/leondz/entity_recognition/',
	version='1.0',
	entry_points={'console_scripts':['run_tagger=run_tagger.py:main', 'train_tagger=train_tagger.py:main']},
	)
