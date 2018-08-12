# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 14:22:07 2018

@author: Gayatri
"""

from pymongo import MongoClient

def insert_word_props(word, properties):
    """ Inserts the word and its properties in the collection
    
    Args:
        word (str): the word whose properties are to be stored
        properties (dict): the properies such as senses, length, consonant
        conjuncts, and frequency
    
    Returns:
        (int): -1 if successful and -1 if unsuccessful
    """
    #connect to the MongoDB instance
    client = MongoClient('localhost:27017')
    database = client.TextSimplification
    
    try:
        database.Words.insert_one(properties)
        return 1
    except Exception as e:
        print(str(e))
        return -1
    
def get_word_props(word):
    """ Retrieves the word's properties from the collection
    
    Args:
        word (str): the word whose properties are to be stored
    
    Returns:
        (dict): A dictionary consisting of the properties and their values
        (int): -1 if unsuccessful
    """
    #connect to the MongoDB instance
    client = MongoClient('localhost:27017')#can we not replicate this in every function??
    database = client.TextSimplification
    
    try:
        properties = database.Words.find_one({"word": word})
        return properties
    except Exception as e:
        print(str(e))
        return -1