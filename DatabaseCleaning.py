# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 2019

@author: Gayatri
"""

#from Model import get_duplicate_sentences;
from Model import get_word_sentences;
import collections

cursor = get_word_sentences()
for doc in cursor:
    #print(doc)
    duplicates = [item for item, count in collections.Counter(doc['sentenceid']).items() if count > 1]
    if len(duplicates)>0:
        print(duplicates)
        print("\n")
    


