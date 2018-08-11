# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:38:59 2018

@author: Gayatri
"""
import os
import codecs
import subprocess
import threading
import csv
from pymongo import MongoClient
from nltk import word_tokenize



os.chdir("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2")
output_file = "synsets.txt"
sense_count = 0

def read_file(word):
    """Read the content of the file containing the senses of a word
    
    Keyword arguments:
    word -- the word whose senses are to be retrieved
    
    """
    with codecs.open("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/" + 
                     output_file, "r", encoding="utf-8") as file:
        for line in file.readlines() :
            if line.lower().startswith("sense count is"):
                global sense_count
                sense_count = line[line.lower().find("sense count is") + 
                               len("sense count is "):]
                #connect to the MongoDB instance
                client = MongoClient('localhost:27017')
                database = client.TextSimplification

                try:
                    database.Words.insert_one({
                                    "word": word,
                                    "sense_count": sense_count,
                            })    
                except Exception as e:
                    print(str(e))
                break
    print("word: " + word)
    print(sense_count)
    #TODO: Store frequency in category, and overall, quicker alternative?
    #dataframe for each category: word, frequency
    #calculate number of characters and store in the Words collection
    #calculate number of syllables and store in the Words collection
    #calculate number of consonant conjuncts and store in the Words collection
    #store number of hypernyms/hyponyms etc. -> check notes from file in college
    
        
def get_num_of_senses(word):
    """Retrieves the number of senses for a given word from the Hindi WordNet

    Keyword arguments:
    word -- the word whose senses are to be retrieved
    """
    
    #write the word to the input file
    outfile = codecs.open("inputwords.txt", "w", "utf-8")
    outfile.write(word)
    outfile.close()
    
    #clear the contents of the output file
    outfile = codecs.open(output_file, "w", "utf-8")
    subprocess.Popen('java -Dfile.encoding=UTF-8 -jar JHWNL.jar', stdout=outfile)
    outfile.close()
    #check if word was found in HWN
    #print(os.stat(output_file).st_size)
    threading.Timer(15, read_file,[word]).start()
    
def read_from_source(source):
    """ Extracts words from the files and retrieves their properties from
    the Hindi WordNet, and calculates certain properties. The properties are
    stored in the database.
    
    Keyword arguments:
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
                    #extract the sentence
                    sentence = row[4]
                    #tokenize the sentence
                    for token in word_tokenize(sentence):
                        #get the number of senses of each word in the sentence 
                        #if it is in Hindi
                        if is_hindi(token):
                            get_num_of_senses(token.strip())
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

print(get_num_of_senses("याद"))