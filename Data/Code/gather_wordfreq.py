#!/usr/bin/env python3
from collections import defaultdict
import math
import pickle
import re
import subprocess
import sys
import os

import stanfordnlp

MIN_ARTICLES = 1
line_trans = str.maketrans('–’', "-\'")
words_split_re = re.compile(r'[^\w\-\']')
is_word_re = re.compile(r'^\w.*\w$')
not_is_word_re = re.compile(r'.*\d.*')
nlp = stanfordnlp.Pipeline(lang = 'hi')

def get_root(word):
    """ Return the root form of the specified word.
    Required argument:
	word (str): the word whose root form is to be retrieved
    """
    word = word.strip()
    doc = nlp(word)
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.lemma != None and word.lemma != '':
                return word.lemma
            return word
'''
if not len(sys.argv) > 1:
	sys.stderr.write("Usage: %s dumps/*.bz2\n" % sys.argv[0])
	sys.exit(1)
'''

# collect data

word_uses = defaultdict(int)
word_docs = {}

doc_no = 0
#for fn in sys.argv[1:]:
        #sys.stderr.write("Processing %s\n" % fn)
        #with subprocess.Popen("bzcat %s | wikiextractor/WikiExtractor.py --no-templates -o - -" % fn,stdout=subprocess.PIPE,shell=True) as proc:
            #while doc_no<50:
                    #print(doc_no)
                    #line = proc.stdout.readline()
for directory in os.listdir('output'):
        print(directory)
        for file_name in os.listdir('output/' + directory):
                file = open('output/' + directory + '/' + file_name, 'r', encoding = 'utf-8')
                #print(file_name)
                for line in file:
                    if not line:
                        break
                    if line.startswith('<'):
                        doc_no += 1
                        continue
                    #line = line.decode('utf-8')
                    line = line.translate(line_trans)
                    line = line.lower()
                    for word in filter(None, words_split_re.split(line)):
                        word = get_root(word)
                        if is_word_re.match(word) and not not_is_word_re.match(word):
                            word_uses[word] += 1
                            if not word in word_docs:
                                word_docs[word] = {doc_no}
                            elif len(word_docs[word]) < MIN_ARTICLES:
                                word_docs[word].add(doc_no)
                file.close()
# remove words only used once

for word in list(word_uses.keys()):
	if len(word_docs[word]) < MIN_ARTICLES:
		del word_uses[word]

# save raw data

words = list(word_uses.keys())
words.sort(key=lambda w: word_uses[w], reverse=True)
out_file = open('wordcount.txt', 'w', encoding = 'utf-8')
for word in words:
        print("%s %d" % (word, word_uses[word]))
        out_file.write(word + ',' + str(word_uses[word]) + '\n')
out_file.close()
