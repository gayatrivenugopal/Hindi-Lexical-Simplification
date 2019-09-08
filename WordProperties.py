'''length, root, syllables, consonants, vowels, conjuncts, number of synsets,
synsets, synonyms in synset, number of synonyms in synset, gloss,
hypernyms (number), hyponyms (number), freq'''
#synsets returns the synsets and synset[0] - sense 1. lemmas - synonyms
import Words

from pyiwn import pyiwn
#pywin.download()
iwn = pyiwn.IndoWordNet('hindi')

def get_length(word):
    word = word.strip()
    return len(word)

def get_root(word):
    """ Return the root form of the specified word.
    Required argument:
	word (str): the word whose root form is to be retrieved
    """
    word = word.strip()
    doc = nlp(word)
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.lemma != None and word.lemma != '':
                return word.lemma
            return word

def get_synsets(word):
    word = word.strip()
    return iwn.synsets(word)

def get_number_of_synsets(word):
    word = word.strip()
    return len(iwn.synsets(word))

def get_synonyms_in_synset(synset):
    synonyms = []
    lemma_list = synset.lemmas()
    for i in range(0, len(lemma_list)):
        if lemma_list[i].name() not in synonyms:
            synonyms.append(lemma_list[i].name())
    return synonyms

def get_number_of_synonyms_in_synset(synset):
    synonyms = []
    lemma_list = synset.lemmas()
    for i in range(0, len(lemma_list)):
        if lemma_list[i].name() not in synonyms:
            synonyms.append(lemma_list[i].name())
    return len(synonyms)

def get_synset_id(synset):
    return synset.synset_id()

def get_synset_gloss(synset):
    return synset.gloss()

def get_word_gloss(word):
    word = word.strip()
    synsets = get_synsets(word)
    gloss_list = []
    for synset in synsets:
        gloss_list.append(synset.gloss())
    return gloss_list

def get_synset_examples(synset):
    return synset.examples()

def get_ontology_nodes(synset):
    print(synset.ontology_nodes())
    return synset.ontology_nodes()

def is_person(synset):
    """ Return true if all the nodes are person nodes. """
    person = True
    ontology_list = get_ontology_nodes(synset)
    for item in ontology_list:
        if item.find('PRSN') == -1:
            person = False
    return person

def is_place(synset):
    """ Return true if all the nodes are physical place nodes. """
    place = True
    ontology_list = get_ontology_nodes(synset)
    for item in ontology_list:
        if item.find('PHSCL') == -1:
            place = False
    return place

def get_number_of_consonants(word):
    word = word.strip()
    consonants = 0
    charList = list(word)
    for character in charList:
        if character in Words.consonants_list:
            consonants = consonants + 1
    return consonants

def get_number_of_vowels(word):
    word = word.strip()
    vowels = 0
    charList = list(word)
    for character in charList:
        if character in Words.vowels_list:
            vowels = vowels + 1
    return vowels

def get_number_of_consonant_conjuncts(word):
    word = word.strip()
    conjuncts = 0
    charList = list(word)
    for character in charList:
        if character == '्':
            conjuncts = conjuncts + 1
    return conjuncts

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


#Source: https://stackoverflow.com/questions/44474085/how-to-separate-a-only-hindi-script-from-a-file-containing-a-mixture-of-hindi-e
def is_hindi(character):
    if character is None or character.strip() == '':
        return 0
    maxchar = max(character)
    if u'\u0900' <= maxchar <= u'\u097f':
        return 1
    return 0


#synsets = get_synsets('लाल')
#print(synsets[0])
