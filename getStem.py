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
word = sys.argv[1].strip('b,\r,\n')#).strip('b,\', ')
print(word)
#word = word.split()
#word = map(lambda x: x.encode('utf-8').decode("unicode_escape"), word)
#word = ''.join(word)
word.replace('\\x', '').encode('utf8')
print(word.split())
#print(str(word))
#print(word.split())
#word = word.encode('utf-8')
#print(word.decode('utf-8'))
#print(type(word))

#print(word)
#word = word.decode('utf-8', 'ignore')
#print(word.list())
#print(word == "\xe0\xa4\xaa\xe0\xa5\x81\xe0\xa4\xb8\xe0\xa5\x8d\xe0\xa4\xa4\xe0\xa4\x95\xe0\xa5\x87\xe0\xa4\x82")
#print('\xe0\xa4\xaa\xe0\xa5\x81\xe0\xa4\xb8\xe0\xa5\x8d\xe0\xa4\xa4\xe0\xa4\x95\xe0\xa5\x87\xe0\xa4\x82')
#print("WORD: " , word.split())
print("\xe0\xa4\xaa\xe0\xa5\x81\xe0\xa4\xb8\xe0\xa5\x8d\xe0\xa4\xa4\xe0\xa4\x95\xe0\xa5\x87\xe0\xa4\x82".split())
#print(str(word))
#b = list(word)
#print(type(b))
#c = bytes(b)
#print(word == '\xe0\xa4\xaa\xe0\xa5\x81\xe0\xa4\xb8\xe0\xa5\x8d\xe0\xa4\xa4\xe0\xa4\x95\xe0\xa5\x87\xe0\xa4\x82')
#word = c.encode('utf8')
#print("TYPE OF ARGUMENT: " , type(word))
#print(word)
#print(word[word.find("=")+1:])
#print("Word: " + word)
#roots = wordnet.getRoot(word);
#print ("Roots: "+roots.encode('utf-8'))
'''