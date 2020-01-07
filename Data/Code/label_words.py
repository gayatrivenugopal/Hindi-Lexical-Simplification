import os
import pandas as pd
import csv
import numpy as np
import string

df_complex_words = pd.read_csv('ComplexWords.csv')
df_sentences = pd.read_csv('Sentences.csv')

for index, row in df_complex_words.iterrows():
        #print(row['words'], row['words'] is not np.nan)
        sequence = []
        if row['words'] is not np.nan:
            if row['words'].find(',') != -1:    #multiple words
                words = row['words'].split(',')
            else:
                words = [row['words']]  #one word
            sentence_index = row['sentence_number']
            gid = row['gid']
            if np.isnan(gid):
                continue
            sentences_subset = df_sentences.loc[df_sentences['group_no'] == gid]
            sentence = sentences_subset.iloc[[sentence_index]].sentence.item()
            #remove punctuations
            sentence = sentence.replace('।', '')
            sentence = sentence.replace('\n', '').strip()
            for punct in string.punctuation:
                sentence = sentence.replace(punct, '')
            #split the sentence
            print(sentence)
            tokens = sentence.split(' ')
            #TODO: token label sentence
            for token in tokens:
                if token in words: #marked as complex
                    sequence.append((token, 1))
                else:
                    sequence.append((token, 0))
            #print(sequence)
            with open('sequence_data.txt', 'a', encoding = 'utf-8') as file:
                file.write(str(sequence) + '\n')