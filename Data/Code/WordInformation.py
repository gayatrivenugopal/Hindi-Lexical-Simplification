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
import string

#nlpimport stanfordnlp
import Words
from Model import insert_sentence
from Model import insert_word_props
from Model import append_word_props
from Model import get_word_props
from nltk import word_tokenize

from py4j.java_gateway import JavaGateway
from py4j.java_gateway import java_import

import nltk
#nltk.download('punkt')
#stanfordnlp.download('hi')
#nlp = stanfordnlp.Pipeline(lang='hi')
gateway = JavaGateway.launch_gateway(classpath="/opt/PhD/Work/JHWNL_1_2/Code/hindiwn.jar")

#TODO: documentation
def read_store_properties(word, file="na", sentence="na", source = "na", category = "na",
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
    #print(word)
    word = word.strip()
    properties = {"word" : word}

    #TODO: POS tag of a word
    #TODO: NER of a word
    #TODO: store number of hypernyms/hyponyms etc. -> check notes from file in college

    #get synset pos, number of synonyms in a synset, number of hypernyms, nymber of hyponyms
    status = get_word_props(word)
    if status['status'] == -1:
        return status
    existing_props = status['data']

    if existing_props is None:
        status = insert_sentence(sentence.strip('"'))

        if status['status'] != -1:
            #store the root/s of the word
            properties["roots"] = get_root(word)
            #store the length of the word
            properties["length"] = len(word)
             #store the number of syllables in the word
            properties["syllables"] = get_syllable_count(word)
            #store the number of consonants and vowels in a list
            numberList = get_number_of_const_vowels_conjuncts(word)
            #store the number of consonants
            properties["consonants"] = numberList[0]
            #store the number of vowels
            properties["vowels"] = numberList[1]
            #store the number of consonant conjuncts
            properties["consonantconjuncts"] = numberList[2]
            #store the synsets,number of hypernyms and hyponyms
            properties["synsets"] = get_other_props(word)
            #the sentence is being stored to retrieve the context of a word
            properties["sentenceid"] = [status['data']]
            #retrieve the root/s of the word
            #wordfile = codecs.open("sourceword.txt", "w", "utf-8")
            #wordfile.write(word)
            properties["file"] = [file]

            #insert 1 as the frequency since the word was encountered
            #for the first time
            properties["word_count"] = 1
            properties["sense_count"] = get_sense_count(word)
            properties["author"] = [author]
            properties["source_category"] = [source + "_" + category]
            properties["year"] = [year]
            ####properties["source_categ_freq"] = [{"source": source,
            ####      "category":category, "frequency":1}]
            #insert the properties
            status = insert_word_props(word, properties)
            if status['status'] == 1:
                #if recursive_synonym_props(properties["synsets"]) == 0:
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
                existing_props['file'].append(file)
                properties['file'] = existing_props['file']
            #if the author is not present in existing properties, then add
            #it to properties
            if author not in existing_props['author']:
                existing_props['author'].append(author)
                properties['author'] = existing_props['author']
            #if the year is not present in existing properties, then add
            #it to properties
            if year not in existing_props['year']:
                existing_props['year'].append(year)
                properties['year'] = existing_props['year']

            if source+"_"+category not in existing_props['source_category']:
                existing_props['source_category'].append(source + "_" + category)
                properties['source_category'] = existing_props['source_category']
            #if source and category combination is not present, then add
            # to properties, otherwise, increase the frequency by 1

            status = append_word_props(word, properties)

            if status['status'] == 1:
                return {'status': 1, 'data': None}
            return {'status': -1, 'data': status['data']}
    return {'status': -1, 'data': status['data']}
'''
def get_root(word):
    """ Return the root form of the specified word.
    Required argument:
	word (str): the word whose root form is to be retrieved
    """
    doc = nlp(word)
    for sentence in doc.sentences:
        for word in sentence.words:
            return word.lemma
'''
def get_other_props(word):
    """ Calls the necessary Java classes and functions to retrieve other
    properties of the word such as number of hypernyms, number of hyponyms etc."

    Args:
        word (str): the word whose properties are to be fetched.
    Returns
        ??


    """


    #output = autoclass('in.ac.iitb.cfilt.jhwnl.examples.Properties').getProperties(word)
    java_import(gateway.jvm,'in.ac.iitb.cfilt.jhwnl.examples.Properties')
    output = gateway.jvm.Properties.getProperties(word)
    properties = {}
    count = 1
    #print(word)
    #print(output)
    if output is None:
        return ""
    for itemArray in output:
        #count the hypernyms
        hypernyms = 0
        hyponyms = 0
        gloss = ""
        for item in itemArray:
            if item.find('gloss') == 0:
                gloss = item[item.find('gloss')+len('gloss: '):]
            elif item.find('hypernyms') == 0:
                hypernyms = hypernyms + int(item[item.find('hypernyms')+len('hypernyms: '):])
            elif item.find('hyponyms') == 0:
                hyponyms = item[item.find('hyponyms')+len('hyponyms: '):]
        properties[str(count)] = dict({})
        properties[str(count)]['synonymcount'] = itemArray[0]
        properties[str(count)]['synonyms'] = itemArray[1]
        properties[str(count)]['gloss'] = gloss
        properties[str(count)]['hypernyms'] = hypernyms
        properties[str(count)]['hyponyms'] = hyponyms
        count = count + 1

    return properties

def get_number_of_const_vowels_conjuncts(word):
    consonants = 0
    vowels = 0
    conjuncts = 0
    charList = list(word)
    for character in charList:
        if character in Words.consonants_list:
            consonants = consonants + 1
        elif character in Words.vowels_list:
            vowels = vowels + 1
        if character == '्':
            conjuncts = conjuncts + 1
    return [consonants, vowels, conjuncts]

def get_syllable_count(word):
    syllables = 0
    consonants = 1
    consonant_flag = 0
    charList = list(word)
    prev = -1
    index = 1
    syllables = 1
    #print(charList)
    #find the second consonant
    for i in range(1, len(charList)):
        character = charList[i]
        #print(character)
        if character in Words.consonants_list:
            consonants = consonants + 1
            if consonants == 2:
                break
        index = index + 1
    beg = index
    #print("BEG: ", beg)
    #print(syllables)
    for i in range(index, len(charList)):
        character = charList[i]
        #print(character)
        #character_count = character_count + 1
        #if character_count == 1:
        #    syllables = 1
        #elif character in Words.consonants_list:
        #    consonants = 1
        #    consonant_flag = 1
        #print("PREV: ", prev)
        if character in Words.consonants_list and syllables > 0 and i != len(charList)-1:# and i != prev + 1:
            if (i+1 < len(charList) and charList[i+1] != '़'):
                #print("Charlist i + 1: ", charList[i+1])
                prev = i
                syllables = syllables + 1
                consonant_flag = consonant_flag + 1
        elif ((character == 'य' and charList[i-1] in Words.vowels_list) or character == 'त्र' or (character == 'र' and charList[i-1] == '्') or character == 'ज्ञ')and i == len(charList) - 1:
            syllables = syllables + 1
            continue
        elif character in Words.vowels_list and character != '़' and  character != '्' and i == len(charList)-1 and i != prev + 1:
            if consonant_flag > 0:
                syllables = syllables - 1
            syllables = syllables + 1
            prev = i
        elif character in Words.vowels_list and character != '़' and  character != '्' and i < len(charList)-1 and i != prev + 1 and charList[i-1] == '़':
            syllables = syllables + 1
            prev = i
        if character == '्':
            syllables = syllables - 1
        if character == '़' and i != len(charList)-1 and i-1 != beg and i-1 == prev:
            syllables = syllables - 1
        if character in Words.vowels_list and character != '़' and  character != '्' and i == len(charList)-1 and charList[i-2] in Words.consonants_list and charList[i-1] not in Words.vowels_list:
            syllables = syllables - 1
        #if character == '्' and i == len(charList)-2:
        #    syllables = syllables + 1
        #elif character in Words.vowels_list and syllables > 0 and consonants > 0 and consonant_flag == 1:
         #   if character != '्':
         #       syllables = syllables + 1
          #      consonant_flag = 0
        index = index + 1
        #print(syllables)
    return syllables

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

def fetch_from_hwn(word, file = "na", sentence = "na", source = "na", category = "na",
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
    if type(word) is not 'int':
        return read_store_properties(word, file, sentence, source, category, author, year);
    return

def read_from_source(src):
    """ Extract words from the files and retrieves their properties from
    the Hindi WordNet, and calculates certain properties. The properties are
    stored in the database.

    Args:
    src -- the directory consisting of the text files
    """
    #recursively read all the files
    for (dirpath, dirnames, filenames) in os.walk(src):
        for filename in sorted(filenames):
            temp = open('files.txt', 'a', encoding='utf-8')
            temp.write(filename + '\n')
            with codecs.open(src + "/" + filename, "r", encoding="utf-8") as file:
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
                    #tokenize the sentence after removing the punctuations
                    translate_table = dict((ord(char), None) for char in string.punctuation)
                    sentence.translate(translate_table)
                    for token in word_tokenize(sentence):
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
    if character is None or character.strip() == '':
        return 0
    maxchar = max(character)
    if u'\u0900' <= maxchar <= u'\u097f':
        return 1
    return 0

#status = read_from_source("/opt/PhD/Work/JHWNL_1_2/Final Corpora/Todo/Premchand")
#if status['status'] == -1:
#    print(status['data'])
