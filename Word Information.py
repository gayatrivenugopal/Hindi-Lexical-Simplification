# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:38:59 2018

@author: Gayatri
"""
import os
import codecs
import subprocess
import csv
from subprocess import STDOUT
from Model import insert_word_props
from Model import get_word_props
from nltk import word_tokenize


os.chdir("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Code")
output_file = "synsets.txt"
#TODO: get root first

def read_properties(word, source = "na", category = "na", author = "unk", 
                    year = "unk"):
    """Reads the content of the file containing the properties of the word 
    and stores in the collection
    
    Args:
        word (str): the word whose properties are to be retrieved
        source (str): the source of the sentence (twitter, web, story, wiki)
        category (str): the category of the sentence (e.g. art, sports, cinema)
        author (str): the author of the story
        year (str): the year in which the text was published
        
    Returns:
        (int): 1 if successful and -1 if unsuccessful
    """
    properties = {"word" : word}
    
    #TODO: read from collection. if value is null then add otherwise
    #read value add 1 to it
    existing_props = get_word_props(word)
        
    if existing_props is None:
        #insert 1 as the frequency since the word was encountered
        #for the first time
        properties["word_count"] = 1
        properties["sense_count"] = get_sense_count(word)
        properties["author"] = [author]
        properties["year"] = [year]

        properties["source_categ_freq"] = {"source": source,
                  "category":category, "frequency":1}
        #insert the properties
        if insert_word_props(word, properties) == 1:
            print(properties)
            return 1
        return -1
    else:
        properties["word_count"] = existing_props["word_count"] + 1
                
    return -1
    #TODO: Store frequency in category, and overall, quicker alternative?
    #calculate number of characters and store in the Words collection
    #calculate number of syllables and store in the Words collection
    #calculate number of consonant conjuncts and store in the Words collection
    #store number of hypernyms/hyponyms etc. -> check notes from file in college
    
        
def fetch_from_hwn(word, source = "na", category = "na", author = "unk", 
                   year = "unk"):
    """Retrieves the number of senses for a given word from the Hindi WordNet

    Args:
        word (str): the word whose number senses are to be retrieved
        source (str): the source of the sentence (twitter, web, story, wiki)
        category (str): the category of the sentence (e.g. art, sports, cinema)
        author (str): the author of the story
        year (str): the year in which the text was published
    
    Returns:
        (int): 1 if successful and -1 if unsuccessful
    """
    
    #write the word to the input file
    outfile = codecs.open("inputwords.txt", "w", "utf-8")
    outfile.write(word)
    outfile.close()
    
    return read_properties(word, source, category, author, year);
    #return threading.Timer(15, read_properties,[word, source, category, 
                                                #author, year]).start()
  
def get_sense_count(word):
    """Reads the string returned from the Hindi WordNet API and returns the
    sense count for the given word
     Args:
        word (str): the word whose sense count is to be returned
        
    Returns
        (int): the sense count of the word
    """
    sense_count = 0
    cmd = 'java -classpath JHWNL.jar in.ac.iitb.cfilt.jhwnl.examples.Synsets'
    #execute the java command - the jar file consists of the Synsets class
    proc = subprocess.Popen(cmd, stderr = STDOUT, stdout = subprocess.PIPE, 
                            cwd = "T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Code/")
    result = proc.communicate()
    #result[0] consists of stdout
    #convert byte to string
    result = result[0].decode('ASCII')
    #extract the sense count - between the last and the second last occurrences
    #of \r\n
    last_occurrence = result[0].rfind("\r\n")
    second_last_occurrence = result.rfind("\r\n", 0, result.rfind("\r\n"))
    sense_count = result[second_last_occurrence+2:last_occurrence-1]
    return sense_count

def count_occurrence(word):
    """Counts the occurrence of the word in each category, as well as in the 
    entire corpus
     Args:
        word (str): the word whose occurrence is to be counted
       
    """
    
def read_from_source(source):
    """ Extracts words from the files and retrieves their properties from
    the Hindi WordNet, and calculates certain properties. The properties are
    stored in the database.
    
    Args:
    source -- the directory consisting of the text files
    
    """
    #recursively read all the files
    for (dirpath, dirnames, filenames) in os.walk(source):
        for filename in filenames:
            with codecs.open(source + "/" + filename, "r", encoding="utf-8") as file:
                #read the csv file
                csv_reader = csv.reader(file, delimiter=',')
                #read each row in the csv file
                for row in csv_reader:
                    #extract the source
                    source = row[0]
                    #extract the category
                    category = row[1]
                    #extract the author
                    author = row[2]
                    #extract the year
                    year = row[3]
                    #extract the sentence
                    sentence = row[4]
                    #tokenize the sentence
                    for token in word_tokenize(sentence):
                        #get the number of senses of each word in the sentence 
                        #if it is in Hindi
                        if is_hindi(token):
                            return fetch_from_hwn(token.strip(),  source, 
                                                 category, author, year)
    return 1
                
#Source: https://stackoverflow.com/questions/44474085/how-to-separate-a-only-hindi-script-from-a-file-containing-a-mixture-of-hindi-e
def is_hindi(character):
    maxchar = max(character)
    if u'\u0900' <= maxchar <= u'\u097f':
        return 1
    return 0
    
#print(read_from_source("Final Corpora/Novels"))
#read_from_source("T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2\Final Corpora\Tweets")
#read_from_source("T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2\Final Corpora\Wiki")
#read_from_source("T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2\Final Corpora\Web")

#print(fetch_from_hwn("पुस्तकें"))







f = codecs.open("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Code/test.txt", "r", encoding="utf-8")
for line in f:
    word = line
word ="u'"+word
cmd="java -classpath StemItCustom.jar in.ac.iitb.cfilt.cpost.StemItCustom " + "tokens.txt" + " -c HindiStemmerConfig.txt"
print("cmd: " + cmd)
proc = subprocess.Popen(cmd, stderr = STDOUT, stdout = subprocess.PIPE, 
                            cwd = "T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Code/")
result = proc.communicate()
print(result)