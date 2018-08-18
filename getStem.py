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
import commands;
import pickle
import codecs

sys.path.append("./hindi-wn-simple.jar");
from sivareddy.in import WordnetToolsSimple;

wordnet= WordnetToolsSimple();
wordnet.initialize();
word = ''
f = codecs.open("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Code/sourceword.txt", "r", encoding="utf-8")
for line in f:
	word = line
roots = wordnet.getRoot(word);
print ("Roots: "+roots.encode('utf-8'))
'''
while 1:
	word = raw_input("Input a word: ")
	word = word.strip().decode("utf-8", "ignore")
	roots = wordnet.getRoot(word);
	print roots
'''