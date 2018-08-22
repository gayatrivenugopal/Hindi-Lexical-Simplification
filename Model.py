# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 14:22:07 2018

@author: Gayatri
"""

from pymongo import MongoClient

#connect to the MongoDB instance
client = MongoClient('localhost:27017')
database = client.TextSimplification

    
def insert_word_props(word, properties):
    """ Inserts the word and its properties in the collection
    
    Args:
        word (str): the word whose properties are to be stored
        properties (dict): the properies such as senses, length, consonant
        conjuncts, and frequency
    
    Returns:
        (tuple): the status which is 1, if successful and -1, if unsuccessful, 
        and the data to be sent back, in this case, the error if any.
    """
    
    try:
        database.Words.insert_one(properties)
        return {'status': 1, 'data': None}
    except Exception as e:
        return {'status': -1, 'data': str(e)}

####################################################################
def insert_sentence(sentence):
    """ Inserts the sentence if not already inserted, and returns the sentence 
    id
    
    Args:
        sentence (str): the sentence that is to be inserted
        
    Returns:
        (int): the id of the sentence if successful and -1 if unsuccessful
    """
    
    try:
        if database.Sentences.count() == 0:
            id = 1
        else:
            #check if sentence exists in the collection
            if document_exists('Sentences', 'sentence', sentence):
                print("Document exists")
                id = get_value('Sentences', 'sentence', sentence, '_id')
                return id
            print("Document does not exist")
            id = get_last_id('Sentences') + 1
            #insert the sentence since it does not exist in the collection
        database.Sentences.insert_one({"_id" : id, "sentence" : sentence})
        print("Inserted document")
        return id
    except Exception as e:
        print(str(e))
        return -1

def get_last_id(collection):
    """ Retrieves the last id of the collection
    
    Args:
        collection (str): the collection from which the last id is to be 
        retrieved
    
    Returns:
        (int): the id if successful and -1 if unsuccesful
    """
    
    try:
        id = database[collection].find().sort('_id', -1).limit(1)[0]['_id']
        return id
    except Exception as e:
        print(str(e))
        return -1
    
def document_exists(collection, field, value):
    """ Checks whether the document consisting of a particular value in the 
    specific field exists
    
    Args:
        collection (str): the collection that is to be queried
        field (str): the field whose value is to be checked
        value (str): the value that is to be checked
    
    Returns:
        (int): 1 if the document exists, 0 if the document does not exist, and
        -1 if there is any error
    """
    try:
        print("Collection: ", collection," Field: ", field, " Value: ", value)
        cursor = database[collection].find_one({field: value})
        print("Cursor: ", cursor)
        if cursor is None:
            return 0
        return 1
    except Exception as e:
        print(str(e))
        return -1
    
def get_value(collection, query_field, query_value, field):
    """ Retrieves the value of the specified field from the specified 
    collection
    
    Args:
        collection (str): the collection that is to be queried
        query_field (str): the field that is to be queried
        query_value (str): the value that is to be searched
        field (str): the field whose value is to be retrieved from the cursor
    
    Returns:
        (str/int): the value of the field from the collection and -1 if there is
        any error
    """
    try:
        cursor = database[collection].find_one({query_field: query_value})
        if cursor is None:
            return -1
        return cursor[field]
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
 
    try:
        properties = database.Words.find_one({"word": word})
        return properties
    except Exception as e:
        print(str(e))
        return -1