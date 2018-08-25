# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:38:59 2018

@author: Gayatri
"""
import os
import codecs
import csv
import subprocess
import ntpath

from Model import insert_sentence
from Model import insert_word_props
from Model import append_word_props
from Model import get_word_props
from nltk import word_tokenize

from py4j.java_gateway import JavaGateway
from py4j.java_gateway import java_import

gateway = JavaGateway.launch_gateway(classpath="hindiwn.jar")
os.chdir("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Code")

def read_store_properties(word, file, sentence, source = "na", category = "na", 
                          author = "unk", year = "unk"):
    """Reads the content of the file containing the properties of the word 
    and stores in the collection
    
    Args:
        word (str): the word whose properties are to be retrieved
        file (str): the file containing the word
        sentence (str): the sentence containing the word
        source (str): the source of the sentence (twitter, web, story, wiki)
        category (str): the category of the sentence (e.g. art, sports, cinema)
        author (str): the author of the story
        year (str): the year in which the text was published
        
    Returns:
        (int): 1 if successful and -1 if unsuccessful
    """
    print(word)
    properties = {"word" : word}

    #TODO: POS tag of a word
    #TODO: NER of a word
    #TODO: calculate number of characters and store in the Words collection
    #calculate number of syllables and store in the Words collection
    #calculate number of consonant conjuncts and store in the Words collection
    #store number of hypernyms/hyponyms etc. -> check notes from file in college
    status = get_word_props(word)
    if status['status'] == -1:
        return status
    existing_props = status['data']
    
    if existing_props is None:
        #retrieve the root/s of the word
        #wordfile = codecs.open("sourceword.txt", "w", "utf-8")
        #wordfile.write(word)
        properties["file"] = [file]
        properties["roots"] = getRoots(word)
        #insert 1 as the frequency since the word was encountered
        #for the first time
        properties["word_count"] = 1
        properties["sense_count"] = get_sense_count(word)
        status = insert_sentence(sentence.strip('"'))
        
        if status['status'] != -1:
            #the sentence is being stored to retrieve the context of a word
            properties["sentenceid"] = [status['data']]
            properties["author"] = [author]
            properties["year"] = [year]
            properties["source_categ_freq"] = []
            properties["source_categ_freq"].append({"source": source,
                  "category":category, "frequency":1})
            #insert the properties
            status = insert_word_props(word, properties)
            if status['status'] == 1:
                return {'status': 1, 'data': None}
            return {'status': -1, 'data': status['data']}
        return {'status': -1, 'data': status['data']}
    else:
        properties["word_count"] = existing_props["word_count"] + 1
        status = insert_sentence(sentence.strip('"'))
        if status['status'] != -1:
            #if the sentence is not present, then add the id to properties
            if status['data'] not in existing_props['sentenceid']:
                existing_props['sentenceid'].append(status['data'])
                properties['sentenceid'] = existing_props['sentenceid']
            #if the file is not present, then add it to properties
            if file not in existing_props['file']:
                existing_props['file'].append(status['data'])
                properties['file'] = existing_props['file']
            #if the author is not present in existing properties, then add
            #it to properties
            if author not in existing_props['author']:
                existing_props['author'].append(status['data'])
                properties['author'] = existing_props['author']
            #if the year is not present in existing properties, then add
            #it to properties
            if year not in existing_props['year']:
                existing_props['year'].append(status['data'])
                properties['year'] = existing_props['year']
            #if source and category combination is not present, then add
            # to properties, otherwise, increase the frequency by 1
            source_category_list = existing_props['source_categ_freq']
            source_categ_exists = 0
            #check if the source and the category exist
            #if so, increase the frequency by 1
            #otherwise, set the frequency to 1 and append the new source, 
            #category and frequency to the existing list
            #the first time a value is added to source_categ_freq, it is not
            #added as a list, therefore this if condition.
            if type(source_category_list) == dict:
                if source_category_list['source'] == source and source_category_list['category'] == category:
                        properties['source_categ_freq'] = {"source": source_category_list['source'],
                         "category": source_category_list['category'],
                         "frequency": source_category_list['frequency'] + 1}
                        source_categ_exists = 1
            else:
                for items in source_category_list:
                    if items['source'] == source and items['category'] == category:
                         properties['source_categ_freq'] = {"source": items['source'],
                                   "category": items['category'],
                                   "frequency": items['frequency'] + 1}
                         source_categ_exists = 1
                        
            if source_categ_exists == 0:
                existing_props['source_categ_freq'].append({"source": source,
                  "category":category, "frequency":1})
                properties["source_categ_freq"] = existing_props['source_categ_freq']
           
            status = append_word_props(word, properties)
            
            if status['status'] == 1:
                return {'status': 1, 'data': None}
            return {'status': -1, 'data': status['data']}
    return {'status': -1, 'data': status['data']}
    

def getRoots(word):
    """ Calls the necessary Python functions and Java classes to retrieve the 
    roots of the word present in the file "sourceword.txt"
    
    Returns
        (list): the roots of the word
        
    Source: Adapted from sivareddy.in/downloads
        In the output 
        1: stands for noun, 
        2: stands for adjective, 
        3: stands for verb, 
        4:stands for adverb
    
    """
   
    java_import(gateway.jvm,'WordnetToolsSimple')
    gateway.jvm.WordnetToolsSimple()
    roots = gateway.jvm.WordnetToolsSimple.getRoot(word)

    #form a list if there are multiple roots
    if roots.find(";") != -1:
        roots = roots.split(";")#form a list
        roots = roots[:-1] #remove the '\r\n' element
        #roots = [root.split(":")[1] for root in roots]#remove the part before the ':'        
    return roots
    
def get_sense_count(word):
    """Reads the string returned from the Hindi WordNet API and returns the
    sense count for the given word
     Args:
        word (str): the word whose sense count is to be returned
        
    Returns
        (int): the sense count of the word
    """
    java_import(gateway.jvm,'in.ac.iitb.cfilt.jhwnl.examples.Synsets')
    sense_count = gateway.jvm.Synsets.getSenseCount(word)
    return sense_count

def tag_file():
    #pip install -e git+https://github.com/tqdm/py-make.git@master#egg=py-make
    cmd = "tokenize.sh test_file.txt > file1.txt"
    make_process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, shell=True,
                                    cwd="T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Code/Hindi_POStagger")
    result = make_process.communicate()
    

    if make_process.wait() != 0:
        print("oops!");
        
def fetch_from_hwn(word, file, sentence, source = "na", category = "na", 
                   author = "unk", year = "unk"):
    """Retrieves the number of senses for a given word from the Hindi WordNet

    Args:
        word (str): the word whose number senses are to be retrieved
        file (str): the file containing the word
        sentence (str): the sentence containing the word
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
    
    return read_store_properties(word, file, sentence, source, category, author, year);
    #return threading.Timer(15, read_properties,[word, source, category, 
                                                #author, year]).start()
''' 
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
'''    
 
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
                    year = row[2]
                    #extract the year
                    author = row[3]
                    #extract the sentence
                    sentence = row[4]
                    #tokenize the sentence
                    for token in word_tokenize(sentence):
                        #get the number of senses of each word in the sentence 
                        #if it is in Hindi
                        if is_hindi(token):
                            status = fetch_from_hwn(token.strip(), 
                                                    ntpath.basename(file.name), 
                                                    sentence, source, category, 
                                                    author, year)
                            if status['status'] == -1:
                                return  status
    return 1
                
#Source: https://stackoverflow.com/questions/44474085/how-to-separate-a-only-hindi-script-from-a-file-containing-a-mixture-of-hindi-e
def is_hindi(character):
    maxchar = max(character)
    if u'\u0900' <= maxchar <= u'\u097f':
        return 1
    return 0
    
status = read_from_source("../Final Corpora/Novels")
if status['status'] == -1:
    print(status['data'])
#read_from_source("T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2\Final Corpora\Tweets")
#read_from_source("T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2\Final Corpora\Wiki")
#read_from_source("T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2\Final Corpora\Web")

#tag_file()
#print(fetch_from_hwn("सालों"))