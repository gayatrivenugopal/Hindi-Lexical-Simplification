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
        (dict): the status which is 1, if successful and -1, if unsuccessful, 
        and the data, to be sent back, in this case, the description of the 
        status, or the error, if any.
    """
    
    try:
        database.Words.insert_one(properties)
        return {'status': 1, 'data': 'Success'}
    except Exception as e:
        return {'status': -1, 'data': e}

def append_word_props(word, properties):
    """ Appends the properties of the existing word
    
    Args:
        word (str): the word whose properties are to be stored
        properties (dict): the properies such as senses, length, consonant
        conjuncts, and frequency
    
    Returns:
        (dict): the status which is 1, if successful and -1, if unsuccessful, 
        and the data, to be sent back, in this case, the description of the 
        status, or the error, if any.
    """
    
    try:
        print(properties)
        print(word)
        database.Words.update_one({'word':word}, 
                                               {"$set":{'word': 'ग्यारह', 'word_count': 2, 'source_categ_freq': {'source': 'story', 'category': 'na', 'frequency': 2}}
                                                },
                                                upsert = True)
        print("Success")
        
        return {'status': 1, 'data': 'Success'}
    except Exception as e:
        return {'status': -1, 'data': e}


def insert_sentence(sentence):
    """ Inserts the sentence if not already inserted, and returns the sentence 
    id
    
    Args:
        sentence (str): the sentence that is to be inserted
        
    Returns:
        (dict): the status which is 1, if successful and -1, if unsuccessful, 
        and the data to be sent back, in this case, the id of the sentence, or 
        the description of the error.
    """
    
    try:
        if database.Sentences.count() == 0:
            id = 1
        else:
            #check if sentence exists in the collection
            status = document_exists('Sentences', 'sentence', sentence)
    
            if status['status'] == 1 and status['data'] != 0:
                print("Document exists")
                status = get_value('Sentences', 'sentence', sentence, '_id')
                if status['status'] == 1 and status['data'] != 0:
                    id = status['data']
                    return {'status': 1, 'data': id}
                if status['status'] == 1: #data is 0
                    return {'status': -1, 'data': 'Empty Cursor'}
                return status
            #if the document does not exist
            if status['status'] == 1:
                print("Document does not exist")
                status = get_last_id('Sentences')
                if status['status'] != -1:
                    id = status['data'] + 1
                    print("SENTENCE ID: ", id)
            else: #error
                return status
        #insert the sentence since it does not exist in the collection
        database.Sentences.insert_one({"_id" : id, "sentence" : sentence})
        print("Inserted document")
        return {'status': 1, 'data': id}
    except Exception as e:
        print(str(e))
        return {'status': -1, 'data': e}


def get_last_id(collection):
    """ Retrieves the last id of the collection
    
    Args:
        collection (str): the collection from which the last id is to be 
        retrieved
    
    Returns:
        (dict): the status which is 1, if successful and -1, if unsuccessful, 
        and the data to be sent back, in this case, the id of the last document,
        or the description of the error if any.
    """
    
    try:
        id = database[collection].find().sort('_id', -1).limit(1)[0]['_id']
        return {'status': 1, 'data': id}
    except Exception as e:
        print(str(e))
        return {'status': -1, 'data': e}

   
def document_exists(collection, field, value):
    """ Checks whether the document consisting of a particular value in the 
    specific field exists
    
    Args:
        collection (str): the collection that is to be queried
        field (str): the field whose value is to be checked
        value (str): the value that is to be checked
    
    Returns:
        (dict): the status which is 1, if successful and -1, if unsuccessful, 
        and the data to be sent back, in this case, 1, if the document exists, 
        0, if the document does not exist, or the description of the error, if 
        any.
    """
    print("Collection: ", collection, " Field: ", field, " Value: ", value)
    try:
        cursor = database[collection].find_one({field: value})
        if cursor is None:
            return {'status': 1, 'data': 0}
        return {'status': 1, 'data': -1}
    except Exception as e:
        return {'status': -1, 'data': e}
  
def get_value(collection, query_field, query_value, field):
    """ Retrieves the value of the specified field from the specified 
    collection
    
    Args:
        collection (str): the collection that is to be queried
        query_field (str): the field that is to be queried
        query_value (str): the value that is to be searched
        field (str): the field whose value is to be retrieved from the cursor
    
    Returns:
        (dict): the status which is 1, if successful and -1, if unsuccessful, 
        and the data to be sent back, in this case, the value of the field from
        the collection, 0, if there is no value, or the description of the 
        error, if any.
    """
    try:
        cursor = database[collection].find_one({query_field: query_value})
        if cursor is None:
            return {'status': 1, 'data': 0}
        return {'status': 1, 'data': cursor[field]}
    except Exception as e:
        print(str(e))
        return {'status': -1, 'data': e}

def get_word_props(word):
    """ Retrieves the word's properties from the collection
    
    Args:
        word (str): the word whose properties are to be stored
    
    Returns:
        (dict): the status which is 1, if successful and -1, if unsuccessful, 
        and the data to be sent back, in this case, the dictionary consisting 
        of the fields and their values, or the description of the error, if any.
    """
 
    try:
        properties = database.Words.find_one({"word": word})
        return {'status': 1,  'data': properties}
    except Exception as e:
        print(str(e))
        return {'status': -1, 'data': e}