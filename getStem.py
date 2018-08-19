# -*- coding: utf-8 -*-
#!/usr/bin/env jython

'''

Gets stems of a word. In the output 

1: stands for noun, 
2: stands for adjective, 
3: stands for verb, 
4:stands for adverb

'''

import sys;
import re;
#import commands;
import subprocess
import pickle
import codecs

sys.path.append("./hindi-wn-simple.jar");
#sys.path.append("stem/stem.jar");
from sivareddy.in import WordnetToolsSimple;

wordnet= WordnetToolsSimple();
wordnet.initialize();
word = sys.argv[1]#.strip('b,\', ')
b = list(word)
print(type(b))
c = bytes(b)

word = c.encode('utf8')
#print("TYPE OF ARGUMENT: " , type(word))
word = word.decode('utf-8', 'ignore')
print(word)
#print(word[word.find("=")+1:])
print("Word: " + word)
roots = wordnet.getRoot(word);
print ("Roots: "+roots.encode('utf-8'))
'''