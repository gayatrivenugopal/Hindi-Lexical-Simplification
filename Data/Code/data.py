import os
import csv
import pandas as pd
import numpy as np
import string
import stanfordnlp
import statistics

from collections import Counter 
#from pymongo import MongoClient
'''
import WordProperties
from WordProperties import get_root
from WordProperties import get_length
from WordProperties import get_syllable_count
from WordProperties import get_number_of_consonant_conjuncts
from WordProperties import get_number_of_vowels
from WordProperties import get_number_of_consonants
import WordInformation
from WordInformation import get_other_props

#client = MongoClient('localhost:27017')
#database = client.Experiment

#TODO: get final complex label
'''
class Data:
    #path = '/opt/PhD/Work/JHWNL_1_2/Data/sentences/'
    path = '/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/'

    '''
    def calculate_sentence_length(self, filename):
        nlp = stanfordnlp.Pipeline(lang = 'hi')
        file = open(self.path + filename, 'r', encoding = 'utf-8')
        length = 0
        lines = 0
        flag = 0
        minimum = 100
        maximum = 0
        stopwords = ['का',
'है',
'वह',
'में',
'कर',
'हो',
'यह',
'जा',
'और',
'से',
'था',
'को',
'मैं',
'नहीं',
'पर',
'रह',
'भी',
'कि',
'तो',
'ले',
'एक',
'दे',
'ही',
'ने',
'अपना',
'जो',
'आ',
'कह',
'कोई',
'हम',
'सक',
'आप',
'कुछ',
'देख',
'बात',
'साथ',
'क्या',
'दो',
'तक',
'ऐसा',
'लग',
'चल',
'सब',
'बन',
'लोग',
'मिल',
'या',
'फिर',
'वाला',
'लिए']
        lengths = list()
        for line in file:
            addition = 0
            words = line.split(' ')
            for token in words:
                token = token.strip()
                #print('token: ', token)
                if len(token) == 0 or token == None:
                    continue
                doc = nlp(token)
                for sent in doc.sentences:
                    for word in sent.words:
                        root = word.lemma
                        #print(type(root))
                if not token in string.punctuation and token != '।' and root not in stopwords:
                    addition = addition + 1
                    length = length + 1
                    flag = 1
            if flag == 1:
                lengths.append(addition)
                if addition < minimum:
                    minimum = addition
                if addition > maximum:
                    maximum = addition
                print('length: ', length, ' lines: ', lines)
                lines = lines + 1
                flag = 0
        freq_dist = sorted(Counter(lengths).items())
        file = open(filename + '_sentence_stats.txt', 'w')
        file.write('average: ' + str(statistics.mean(lengths)) + '\nmedian: ' + str(statistics.median(lengths)))
        file.write('standard deviation: ' + str(statistics.stdev(lengths)) + '\nskewness: ' + str((3*(statistics.mean(lengths)-statistics.median(lengths)))/statistics.stdev(lengths)))
        file.write('\nmin: ' + str(minimum) + '\nmax: ' + str(maximum) + '\n')
        file.write('Frequencies: \n')
        for tup in freq_dist:
            for item in tup:
                file.write(str(item) + ' ')
            file.write('\n')
        file.close()
    
    def clean_ranks(self):
        data = pd.read_csv(self.path + 'Raw Data/RankedWords.csv')
        data = data[~data.word.str.contains('_')]
        data = data[~data.word.str.contains('-')]
	#pid, words, complexity
        for index, row in data.iterrows():
            if data.loc[index]['simplicity'] <= 3:
                data.at[index,'complexity'] = 1
            else:
                data.at[index,'complexity'] = 0
        data.drop_duplicates(keep = 'first', inplace = True)
        data['word'] = data['word'].str.replace("'","")
        data['word'] = data['word'].str.strip()
        data.to_csv(self.path + 'CleanedData/RankedData.csv', encoding = 'utf-8')
        print('Cleaned rank file and stored in "Cleaned Data"')
	#cleaned manually (removed numbers, matras etc.) post script execution
     
    def value_in_complexwords(self, df, value):
        for index, row in df.iterrows():
            words = row['words']
            if words == np.nan:
                return -1
            words = str(words)
            words_list = list()
            if words.find(',') != -1:
                words_list = words.split(',')
            else:
                words_list.append(words)
            for word in words_list:
                if value.strip() == word.strip():
                    return row['sentence_number']
        return -1
	

    def combine_data(self):
        #read data from the cleaned ranked words file
        self.ranks = pd.read_csv(self.path + 'CleanedData/RankedData.csv') #pid, word, complexity
        self.groups = pd.read_csv(self.path + 'CleanedData/Groups.csv') #gid, pid
        self.complexdata = pd.read_csv(self.path + 'CleanedData/ComplexWords.csv') #gid, words, sentence_number
        self.sentences = pd.read_csv(self.path + 'Raw Data/Sentences.csv') #group_no, sentence
        #print('Sentences: ', self.sentences.loc[self.sentences['group_no'] == 1])
        self.data = self.ranks
        self.data['gid'] = ''
        self.data['sentence'] = ''
        self.data['category'] = ''
        for index, row in self.ranks.iterrows():
            pid = self.data.loc[index]['pid']
            gid = str(self.groups.loc[self.groups['pid'] == pid, 'gid'].iloc[0]).strip()
            #print('pid: ', pid, ' gid: ', gid)
            self.data.loc[self.data['pid'] == pid, 'gid'] = gid
            #if the current word is present in complexdata against the 
            #same pid, get the sentence number, and then get the sentence
            sentence_number = self.value_in_complexwords(self.complexdata, row['word'])
            if sentence_number != -1:
                sentence_df = self.sentences[self.sentences['group_no'] == int(gid)]
                counter = 0
                for i, val in sentence_df.iterrows():
                    print(counter, sentence_number)
                    if counter == sentence_number:
                        self.data.loc[self.data['pid'] == pid, 'sentence'] = val['sentence']
                        self.data.loc[self.data['pid'] == pid, 'category'] = val['category']
                        #print(self.data)
                    counter += 1
        self.data.to_csv(self.path + 'CleanedData/FinalData.csv', encoding = 'utf-8')
    
    def deem_as_complex(self, filename):
        nlp = stanfordnlp.Pipeline(lang = 'hi')
        df = pd.read_csv(self.path + filename)
        for i in range(1, 21):
            group_df = df[df.gid == i].copy()
            words = dict()
            word_pid = dict()
            #complex_df = pd.DataFrame(columns=['index', pid', 'word', 'simplicity', 'complexity', 'gid', 'sentence', 'category', 'complex_annotation_count', 'complex_annotators', 'label'])
            #complex_df = group_df.copy()
            complex_df = pd.DataFrame(index=group_df.index, columns=['pid', 'word', 'simplicity', 'complexity', 'gid', 'sentence', 'category', 'complex_annotation_count', 'complex_annotators', 'label'])
            complex_df[['pid', 'word', 'simplicity', 'complexity', 'gid', 'sentence', 'category']] = group_df[['pid', 'word', 'simplicity', 'complexity', 'gid', 'sentence', 'category']]
            complex_df['complex_annotation_count'] = 0
            complex_df['complex_annotators'] = ''
            complex_df['label'] = '' 
            #print(complex_df)
            for index, row in group_df.iterrows():
                doc = nlp(group_df.loc[index]['word'])
                for sent in doc.sentences:
                    for word in sent.words:
                        root = word.lemma

                if group_df.loc[index]['complexity'] == 1:
                    if len(words)>0 and root in words.keys():
                        if group_df.loc[index]['pid'] not in word_pid[root]:
                            #print(root)
                            words[root] += 1
                            word_pid[root].append(group_df.loc[index]['pid'])
                            #complex_df.loc[index]['complex_annotation_count'] = words[root]
                            complex_df.set_value(index, 'complex_annotation_count' , words[root])
                            #print(complex_df.loc[index]['complex_annotation_count'])
                            #print(words[root])
                            #print(complex_df)
                            #complex_df.loc[index]['complex_annotators'] = str(word_pid[root])
                            complex_df.set_value(index, 'complex_annotators' , str(word_pid[root]))
                            #print(complex_df.loc[index])
                            complex_df.to_csv(self.path + 'LabelledData.csv', encoding = 'utf-8')
                            if words[root] >= 2:
				#add to group_df
                                complex_df.set_value(index, 'label', 1)
                            else:
                                complex_df.set_value(index, 'label', 0)
                else:
                        words[root] = 1
                        word_pid[root] = list()
                        word_pid[root].append(complex_df.loc[index]['pid'])
                #print(complex_df.complex_annotators)
	
    def calculate_average_rating(self, filename):
        """ The average rating of words that have been annotated by atleast 2 annotators is calculated. The other words are ignored. """
        nlp = stanfordnlp.Pipeline(lang = 'hi')
        df = pd.read_csv(self.path + filename)
        words = dict()
        word_pid = dict()
        word_gid = dict()
        word_sentence = dict()
        word_category = dict()
        word_rank = dict()
        final_data = {'word':list(), 'pid': list(), 'gid': list(), 'sentence': list(), 'category': list(), 'rank': list(), 'label_avg_rank': list()}
        extra_data = {'word':list(), 'pid': list(), 'gid': list(), 'sentence': list(), 'category': list(), 'rank': list(), 'label_avg_rank': list()}
            
        for i in range(1, 21): #20 groups
            group_df = df[df.gid == i].copy()
            #iterate through each group of annotators
            for index, row in group_df.iterrows():
                doc = nlp(group_df.loc[index]['word'])
                for sent in doc.sentences:
                    for word in sent.words:
                        root = word.lemma

                if len(words)>0 and root in words.keys():
			#if the pid has not already annotated this word
                        if group_df.loc[index]['pid'] not in word_pid[root]:
                            print('GID: ', group_df.loc[index]['gid'], ' i: ', i)
                            words[root] += 1
                            word_rank[root].append(group_df.loc[index]['rank'])
                            word_pid[root].append(group_df.loc[index]['pid'])
                            word_gid[root].append(group_df.loc[index]['gid'])
                            print(root, word_gid[root])
                            if group_df.loc[index]['sentence'] not in word_sentence[root]:
                                word_sentence[root].append(group_df.loc[index]['sentence'])
                            if group_df.loc[index]['category'] not in word_category[root]:
                                word_category[root].append(group_df.loc[index]['category'])
                else:
                        #words keeps track of the words and the annotator count
                        words[root] = 1
                        #word_rank keeps track of the ranks
                        word_rank[root] = list()
                        word_rank[root].append(group_df.loc[index]['rank'])
                        #word_pid keeps track of the annotators
                        word_pid[root] = list()
                        word_pid[root].append(group_df.loc[index]['pid'])
                        #word_gid keeps track of the group ids
                        word_gid[root] = list()
                        word_gid[root].append(group_df.loc[index]['gid'])
                        #word_sentence keeps track of the sentence/s from which the word or its synonym was selected
                        word_sentence[root] = list()
                        word_sentence[root].append(group_df.loc[index]['sentence'])
                        #word_category keeps track of the category from which the sentence was extracted
                        word_category[root] = list()
                        word_category[root].append(group_df.loc[index]['category'])
                        #Not adding this to final_data as our objective is to keep track of words annotated by atleast two annotators
        #create a dictionary for average rating for words with more than one annotator
        for root, annotator_count in words.items():
            if annotator_count > 1:
                final_data['word'].append(root)
                final_data['pid'].append(','.join(str(v) for v in word_pid[root]))
                final_data['gid'].append(','.join(str(v) for v in word_gid[root]))
                final_data['sentence'].append(','.join(str(v) for v in word_sentence[root]))
                final_data['category'].append(','.join(str(v) for v in word_category[root]))
                final_data['rank'].append(','.join(str(v) for v in word_rank[root]))
                final_data['label_avg_rank'].append(sum(word_rank[root])/len(word_rank[root]))
            else:
                extra_data['word'].append(root)
                extra_data['pid'].append(','.join(str(v) for v in word_pid[root]))
                extra_data['gid'].append(','.join(str(v) for v in word_gid[root]))
                extra_data['sentence'].append(','.join(str(v) for v in word_sentence[root]))
                extra_data['category'].append(','.join(str(v) for v in word_category[root]))
                extra_data['rank'].append(','.join(str(v) for v in word_rank[root]))
                extra_data['label_avg_rank'].append(sum(word_rank[root])/len(word_rank[root]))
        #convert to dataframe and write to csv
        final_df = pd.DataFrame.from_dict(final_data)
        extra_df = pd.DataFrame.from_dict(extra_data)
        print(final_df.head())
        final_df.to_csv (self.path + 'LabelsAverage/consolidated_labels.csv', index = None, header=True)
        extra_df.to_csv (self.path + 'LabelsAverage/consolidated_labels_extra.csv', index = None, header=True)

	'''      
    def get_label(self, word):
        """Return 1 if any one label is 1. """
        flag = 0
        for file in sorted(os.listdir(self.path + 'Labels/')):
            print(file)
            df = pd.read_csv(self.path + 'Labels/' + file)
            print(df.head())
            #print('label: ', df[df['word'] == word.strip()]['label'].values)
            if len(df[df['word'] == word.strip()]['label'].values) > 0:
                for item in df[df['word'] == word.strip()]['label'].values:
                    print(word, ': ', item)
                    if item == 1:
                        flag = 1
        print('flag: ', flag)
        return flag
    '''
    def get_label_avg_rank(self, word):
        """Return -1 if rank is not present. """
        flag = -1
        for file in sorted(os.listdir(self.path + 'LabelsAverage/')):
            #print(file)
            df = pd.read_csv(self.path + 'LabelsAverage/' + file)
            print(df.dtypes)
            if len(df[df['word'] == word.strip()]['label_avg_rank'].values) > 0:
                for item in df[df['word'] == word.strip()]['label_avg_rank'].values:
                    #print(word, ': ', item)
                    flag = item
        print('flag: ', flag)
        return flag
  
    def get_synonyms(self, properties):
        synonyms = []
        #print('props: ', properties)
        for key, value in properties.items():
            #print('value: ', value)
            for synonym in value['synonyms'].split(','):
                synonyms.append(synonym.strip())
        return synonyms
	'''
    def get_synonyms(self, word):
        """ Return the synonyms of the word.
            Keyword Argument:
            word (str): the word whose synonyms are to be retrieved
        Returns:
            (set): set of synonyms if present, and None, otherwise
        """
        try:
            query = {'word': word}
            cursor = database['Words'].find(query)
            synonym_set = set()
            if cursor is None:
                return None
            for document in cursor:
                if len(document['synsets']) > 0:
                    for key, synset in document['synsets'].items():
                        synonyms = synset['synonyms'].split(",")
                        for synonym in synonyms:
                            synonym_set.add(synonym.strip())
            if len(synonym_set) == 0:
                return None
            return synonym_set
        except Exception as e:
            print(e)
        return None
	  
     
    def get_lemma(self, word):
        """ Return the root form of the specified word.
        Required argument:
	    word (str): the word whose root form is to be retrieved
        """
        try:
            query = {'word': word}
            cursor = database['Words'].find(query)
        
            if cursor is None:
                return None
            for document in cursor:
                if len(document['roots']) > 0:
                    return document['roots']
        except Exception as e:
            print(e)
        return None	
    
    def get_number_of_synonyms(self, properties):
        count = 0
        for key, value in properties.items():
            #print('values: ', value)
            count += int(value['synonymcount'])
        return count
	
    def get_number_of_hypernyms(self, properties):
        count = 0
        for key, value in properties.items():
            count += int(value['hypernyms'])
        return count
	
    def get_number_of_hyponyms(self, properties):
        count = 0
        for key, value in properties.items():
            count += int(value['hyponyms'])
        return count
	
    def get_properties(self, root):
        #properties = get_properties(root)
            properties = dict()
            word_props = get_other_props(root)
            if isinstance(word_props, str) == True:
                return None
            #print('word_props: ', word_props)
            properties['length'] = get_length(root)
            properties['n_synsets'] = len(word_props)
	    #properties['n_synsets'] = get_sense_count(word)
            properties['n_synonyms'] = self.get_number_of_synonyms(word_props)
            properties['n_hypernyms'] = self.get_number_of_hypernyms(word_props)
            properties['n_hyponyms'] = self.get_number_of_hyponyms(word_props)
            properties['n_avg_synonyms'] = properties['n_synonyms']/properties['n_synsets']
            properties['n_avg_hypernyms'] = properties['n_hypernyms']/properties['n_synsets']
            properties['n_avg_hyponyms'] = properties['n_hyponyms']/properties['n_synsets']
            properties['n_consonants'] = get_number_of_consonants(root)
            properties['n_vowels'] = get_number_of_vowels(root)
            properties['n_consonantconjuncts'] = get_number_of_consonant_conjuncts(root)
            properties['n_syllables'] = get_syllable_count(root)
            properties['label'] = self.get_label(root)
            properties['label_avg_rank'] = self.get_label_avg_rank(root)
            properties['word'] = root
            return properties

    def create_word_groups(self, input_file):
        """ Read the csv line by line, fetch the group id and the word. split the word and store in a list.
	Loop through the list and fetch the synonyms. For the words in the list, fetch the final label from the label file.
	Store the group id, pid, word_group_id, word and final label in a new csv file. Also add the properties of the word in the columns.
	Save and close the file.
	For all the words belonging to the same word_group_id, normalize the property values and add in new columns.
	Do this by looping through the word_group_id, fetch each property's value in a dict with property name as the key and
	their values as a list in the key's value. Store these word_group files in a separate directory.
	"""
        group_word = pd.read_csv(self.path + input_file)
        invalid_words = []
        words = group_word['words']
        words_file = open('words.txt', 'a', encoding = 'utf-8')
        for items in sorted(words.iteritems()): 
            #print(type(items[1]), items[1])
            if type(items[1]) is not float and len(items[1].strip()) != 0: #ignore NaN values
                words_file.write(items[1].replace(',','\n') + '\n')
        words_file.close()
        words_file = open('words.txt', 'r', encoding = 'utf-8')
        word_set = set(word for word in words_file)
        word_group_id = 1
        i = 1
        csv_columns = ['id','word', 'length','n_synsets', 'n_synonyms', 'n_avg_synonyms', 'n_consonants', 'n_vowels', 'n_hypernyms', 'n_avg_hypernyms', 'n_hyponyms', 'n_avg_hyponyms', 'n_consonantconjuncts', 'n_syllables', 'label', 'label_avg_rank']
        covered_words = []
        for word in word_set:
            word_file = open('wordgroups/word_' + str(word_group_id) + '.csv', 'w', encoding = 'utf-8')
            root = word
            if root == None or len(root.strip()) == 0:
                continue
            while True:
                root = get_root(root)
                if root == word or root == None:
                    root = word
                    break
                word = root
            if root.find('_') != -1 or root.find('-') != -1 or len(root.strip()) == 0 or root == None:
                print('found underscore or root is blank: ', root)
                invalid_words.append(root)
                continue
            if root.strip() in covered_words:
                #print('root is covered: ', root)
                continue
            print(str(word_group_id), ' word: ', word)
	    #fetch the synonyms from mongodb
	    #create a list of dictionaries to write to the csv file
            word_data = []
            properties = self.get_properties(root)
            if properties == None:
                continue
            properties['id'] = i

            if root not in covered_words:
                word_data.append(properties)
                i += 1
            covered_words.append(root.strip())
            #get properties except for frequency
            synonyms = self.get_synonyms(get_other_props(root))
            if synonyms is not None:
                for synonym in synonyms:
                    if synonym.find('_') != -1 or synonym.find('-') != -1 or len(synonym.strip()) == 0:
                        print('found underscore or root is blank: ', synonym)
                        invalid_words.append(synonym)
                        continue
                    if synonym.strip() in covered_words:
                        continue
                    properties = self.get_properties(synonym)
                    if properties == None:
                        continue
                    properties['id'] = i
                    if synonym not in covered_words:
                        word_data.append(properties)
                        i += 1
                        covered_words.append(synonym.strip())
            word_group_id += 1
            print('new word group is: ', word_group_id)
            writer = csv.DictWriter(word_file, fieldnames=csv_columns)
            writer.writeheader()
            for data in word_data:
                writer.writerow(data)
            word_file.close()
        words_file.close()
        file = open('invalid_words.txt', 'w', encoding = 'utf-8')
        for word in invalid_words:
            file.write(word+'\n')
     
    def modify_attribute_in_wordgroup(self, in_dir_path, attr_name):
        #/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/finalwordgroups/word_1.csv
        for file_name in sorted(os.listdir(self.path + in_dir_path)):
            print('file: ', file_name)
            word_group_df = pd.read_csv(self.path + in_dir_path + file_name)
            out_df = word_group_df.copy()
            out_df['label_avg_rank'] = -1
            for i, row in word_group_df.iterrows():
                root = row['word']
                out_df.ix[i, 'label_avg_rank'] = float(self.get_label_avg_rank(root))
            print("out: ", out_df)
            out_df.to_csv(self.path + in_dir_path + file_name, index = None, header = True)
            #TODO: the same for normalized word groups, then dataforregression
    '''
    def get_normalized_frequency_df(self):
        df_list = []
        for file in sorted(os.listdir(self.path + 'normalizedwordgroups/')):
            #print(file)
            df = pd.read_csv(self.path + 'normalizedwordgroups/' + file)
            df_list.append(df)
        pd.concat(df_list, ignore_index=True).to_csv(self.path + 'normalized_frequencies.csv', index = None, header = True)
        return pd.concat(df_list, ignore_index=True)
    '''    

    def modify_freq_in_csv(self, file_name):
        df = pd.read_csv(self.path + file_name)
        #freq_df = pd.read_csv(self.path + 'frequencies.csv')
        out_df = df.copy()
        normalized_freq_df = pd.read_csv(self.path + 'normalized_frequencies.csv')
        print(normalized_freq_df['frequency'])
        out_df['frequency'] = 0
        for i, row in df.iterrows():
            word = row['word']
            #freq = freq_df.loc[freq_df['word'] == word, 'frequency']
            freq = normalized_freq_df.loc[normalized_freq_df['word'] == word, 'frequency']
            print(freq.values)
            #out_df.loc[out_df['word'] == word, 'frequency'] = freq
            out_df.ix[i, 'frequency'] = freq.values[0]
        out_df.to_csv(self.path + file_name, index = None, header = True)

data = Data()
#data.create_word_groups('ComplexWords.csv')
#data.deem_as_complex('FinalData.csv')

#data.calculate_average_rating('FinalData.csv')
#data.modify_attribute_in_wordgroup('finalwordgroups/', 'label_avg_rank')
data.modify_freq_in_csv('DataForClassification.csv')
#for file in sorted(os.listdir('/opt/PhD/Work/JHWNL_1_2/Data/sentences/')):
#    data.calculate_sentence_length(file)
#data.combine_data()
#data.clean_ranks()
