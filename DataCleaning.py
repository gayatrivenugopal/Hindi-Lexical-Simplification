
# coding: utf-8

# In[1]:


#cd T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2


# In[2]:


#Source: https://stackoverflow.com/questions/44474085/how-to-separate-a-only-hindi-script-from-a-file-containing-a-mixture-of-hindi-e
def detect_language(character):
    maxchar = max(character)
    if u'\u0900' <= maxchar <= u'\u097f':
        return 'hindi'
    return 0


# In[ ]:


#Data Cleaning
import os
import codecs, string, time
import pdfminer
import sys
import subprocess
import re
import json

import pandas as pd
import numpy as np
import math

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
os.chdir("T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2")
#Store the list of matra's in a list
#Source: http://www.utf8-chartable.de/unicode-utf8-table.pl?start=2304&number=128
matras = ['ऽ', 'ँ', 'ं', 'ः', 'ऺ', 'ऻ', '़', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'ॅ', 'ॆ', 'े', 'ै', 'ॉ', 'ॊ', 'ो', 'ौ',
         '्', 'ॎ', 'ॏ', '॑', '॒', '॓', '॔', 'ॕ', 'ॖ', 'ॗ', 'ॢ', 'ॣ', '॰', 'ॱ', '।', '॥']
#separate_matras should not be associated with the same consonant
separate_matras = [ 'ऽ', 'ॉ' ,'ा', 'ि', 'ी', 'ु', 'ू','ॆ', 'े', 'ै', 'ॊ', 'ो', 'ौ']


#newDF = newDF.append(oldDF, ignore_index = True)
#input = PdfFileReader(open("Godan_by_Premchand.pdf", "rb"))

#for page in input.pages:
#    print(page.extractText().encode('UTF-8'))

def convert_pdf_to_txt(directory_path, pdf_directory_path, txt_directory_path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    
    #read each file in the directory that consists of the PDF files
    for pdfpath in os.listdir(directory_path + "/" + pdf_directory_path):
        with open(directory_path + "/" + pdf_directory_path + "/" +  pdfpath, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            password = ""
            caching = True
            pagenos = set()

            for page in PDFPage.get_pages(fp, pagenos, password=password,caching=caching, check_extractable=True):
                interpreter.process_page(page)

                text = retstr.getvalue()
            #write the generated text to the text file that has the same name as that of the pdf file but is stored in
            #a different directory
            #replace the pdf extension with .txt
            file = codecs.open(directory_path + "/" + txt_directory_path + "/" +  os.path.splitext(os.path.basename(pdfpath))[0] + ".txt", "w", "utf-8")
            file.write(text)
            file.close()

    device.close()
    retstr.close()
    
    return 1

def read_lines(directory_path, orig_directory_path, clean_directory_path):
    #read each file in the directory that consists of the original unprocessed text files
    for origpath in os.listdir(directory_path + "/" + orig_directory_path):
        #create a correponding 'cleaned' text file in a different directory
        outfile = codecs.open(directory_path + "/" + clean_directory_path + "/" + origpath, "w", "utf-8")
        with open(directory_path + "/" + orig_directory_path + "/" + origpath, encoding = "utf8") as rfp:
            #read each line of the unprocessed text file
            line = rfp.readline()
            cnt = 1
            while line:
                #print("Line {}: {}".format(cnt, line.strip()))
                #continue processing the line only if it is not blank
                if not line.isspace():
                    hindi = 1
                    #split the line into words to detect non-Hindi, non-special characters
                    wordStructure = line.split()
                    for word in wordStructure:
                        #hindi is a flag that indicates the the current word is Hindi (or a special character)
                        hindi = 1
                        #read each letter of the current word
                        for letter in word:
                            lang = detect_language(letter)
                            #set the flag to 0 if the character is not Hindi (or a special character)
                            if lang != "hindi":
                                hindi = 0
                                break #stop processing the line
                    #if the word is Hindi (or a special character), write the line to the clean file
                    if hindi == 1:
                        outfile.write(line)
                #read the next line
                line = rfp.readline()
                cnt += 1
        outfile.close()
    return 1

def clean_words(directory_path, clean_directory_path, output_file):
    #read each file in the directory that consists of the processed text files
    for file in os.listdir(directory_path + "/" + clean_directory_path):
        
        #identify the lines that are incomplete
        
        if file[-5:] == "1.txt":
            break
        mark_incomplete_lines(directory_path + "/" + clean_directory_path + "/" + file)
        
        form_sentences(directory_path + "/" + clean_directory_path + "/" + file)
        #remove the sentences consisting of <end>
        clean_sentences(directory_path + "/" + clean_directory_path + "/" + file)
        
        #create a dataframe to store the searched words and their corresponding replacements
        words_df = pd.DataFrame(columns=['token', 'replacement'])
        with open(directory_path + "/" + clean_directory_path + "/" + file, encoding = "utf8") as fp:
            #read each line of the unprocessed text file
            line = 1
            while line:
                try:
                    line = fp.readline()
                    
                except:
                    #words_df.set_value(len(words_df)-1, 'replacement', 'null')
                    continue
                #split the line into words
                wordStructure = re.split('[`\-=~—!@#$%^&*()_+\[\]{};\'\\:"|<,./<>? ]',line)
                for word in wordStructure:
                    
                    if word.startswith("lengthend"):
                        break
                        #TODO: check this change: continue to break
                    #not needed: searched_words.set_value(searched_words.size+1, word)
                    #store the word in the 'word' column if it does not already exist
                    if not words_df.empty:
                        #words_df = words_df['token'].map(lambda x: x.encode('utf-8'))
                        if not any(words_df.token == word) :
                            words_df.set_value(len(words_df), 'token', word)
                        else:
                        #if the word exists, continue with the next word
                                continue
                    else:
                        words_df.set_value(len(words_df), 'token', word)
                    
                    
                    #search for the word in HWN if it is not a special character
                    if not re.search(r'[`\-=~—!@#$%^&*()_+\[\]{};\'\\:"|<,./<>? ]', word):
                        #check if the word is present in HWN
                        if get_desc_from_hwn(word, "hwn data/word.txt") and word_in_hwn("hwn data/word.txt") == 0:
                            #word does not exist in HWN
                            #check the words for noisy characters
                            status_json = json.loads(read_word(word))
                           
                            if status_json['status'] == 1: #the modified word exists in HWN
                                print (word + "exists, replacing in file")
                                #store the modified word in the second column of the word in the data frame
                                words_df.set_value(len(words_df)-1, 'replacement', status_json['modified_word'])
                            elif status_json['status'] == 0:
                                print (word + "does not exist, removing the sentence")
                                #store the value null in the second column of the word in the data frame
                                words_df.set_value(len(words_df)-1, 'replacement', 'null')
                                #print(words_df);
                                #mark the line for removal
                                #line = "<end>"+ line
                                #write this to the file
                                #print(line)
                                break
                            elif status_json['status'] == -1: #status is -1 which means that the word was not modified
                                print (word + "was not modified")
#browse through all the files and search for the words in each file, in HWN.
#If it does not exist, find the closest word and replace the current word with this word
                            #search for the most similar word
                        #line.replace(textToSearch, textToReplace)
                #read the next line
                #line = fp.readline()pu
        #TODO: remove redundant lines from the file
        print ("Calling modify content for file")
        modify_content_in_file(words_df, directory_path + "/" + clean_directory_path + "/" + file)
    return 1

def get_desc_from_hwn(word, output_file):
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
    return 1

def word_in_hwn(file_path):
    start = time.time()
    while time.time() < start + 3:
        time.time()
    count = 0
    with open(file_path, encoding = "utf8") as fp:
        try:
            line = fp.readline()
            while line:
                count += 1
                try:
                    line = fp.readline()
                except:
                    continue
                if count > 10:
                    return 1
        except:
            return 0
    return 0

def read_word(word):
    word = word.strip()
    prevword = 0
    index = 0
    orig_word = word
    
    #read the word if it is not a matra
    if word not in matras:
        #check for matras at the beginning of the word because matras are processed after the consonant to which they are attached
        if word[:1] in matras:
            #if the word begins with a matra, remove the matra
            #print (character)
            word = word[1:]
            
            print ("Original word: " + orig_word + " Word: " + word)
        index = 0
        old_pos = -1 #used to store the position at which a separate_matra element was found
        word = list(word)
        
        for character in word:
            #if not character in matras:
                #TODO: check for consonants and special characters; if not consonant or special character, remove the line as it is an invalid character
                #if two matras that should not occur together, occur together, mark the first matra for removal
                if character in separate_matras:
                    if index - old_pos == 1 and not old_pos == -1:
                        #mark the previous character for removal
                        word[old_pos] = "R" #R = remove
                    old_pos = index
                index += 1
        #remove the characters from the word that have been marked for removal
        word = "".join(word)
        word = word.replace("R", "")
        
        #search for the modified word in WordNet
        if not orig_word == word:
            if get_desc_from_hwn(word, "hwn data/word.txt") and word_in_hwn("hwn data/word.txt") == 1:
                result = json.dumps({'status': 1, 'modified_word': word}, ensure_ascii=False)
            else:
                result = json.dumps({'status': 0}, ensure_ascii=False)
        else:
            result = json.dumps({'status': -1}, ensure_ascii=False)#no change
    else:
        result = json.dumps({'status': -1}, ensure_ascii=False)#no change
    return result
        
    
def mark_incomplete_lines(file):
    #add <end> at the end of each line that is to be removed
    #find the average length of the lines in the file
    print (file)
    avg_length = get_avg_length(file)
    max_length = len(max(open(file, 'r', encoding = "utf8"), key=len))
    #read each line and check whether its length is less than the average length
    with open(file, encoding = "utf8") as oldfile, open(os.path.splitext(file)[0] + "1.txt", "w", encoding = "utf8") as newfile:
        for line in oldfile:
           # if len(line) < avg_length/2 or (len(line) < max_length*3/4 and line.strip()[-1:] not in ["।", "?", "!"]):
            if len(line) < max_length*3/4 and (line.strip()[-1:] not in ["।", "?", "!"] or line.strip()[:1] in matras):
                newfile.write("lengthend" + line)
            else:
                newfile.write(line)
    if os.path.isfile(os.path.splitext(file)[0] + "1.txt"):
        os.remove(file)
        os.rename(os.path.splitext(file)[0] + "1.txt", os.path.splitext(file)[0] + ".txt")

def get_avg_length(file):
    with open(file, "r", encoding = "utf8") as f:
        lines = f.readlines()
        return (sum(len(line) for line in lines) / len(lines))
    
def form_sentences(file):
    #create sentences
    with open(file, "r", encoding = "utf8") as oldfile, open(os.path.splitext(file)[0] + "1.txt", "w", encoding = "utf8") as newfile:
        nonewlines = oldfile.read().splitlines()
        sentences = " ".join(nonewlines)
        sentences = sentences.replace("।", "।\n")
        sentences = sentences.replace("?", "?\n")
        sentences = sentences.replace("!", "!\n")
        #remove the sentences that have <end>
        newfile.write(sentences)        
    if os.path.isfile(os.path.splitext(file)[0] + "1.txt"):
        os.remove(file)
        os.rename(os.path.splitext(file)[0] + "1.txt", os.path.splitext(file)[0] + ".txt")
        
def clean_sentences(file):
    #create sentences
    with open(file, "r", encoding = "utf8") as oldfile, open(os.path.splitext(file)[0] + "1.txt", "w", encoding = "utf8") as newfile:
        lines = oldfile.readlines()
        lines = [line.strip() for line in lines if not "<end>" in line]
        #remove the sentences that have <end>
        newfile.write("\n".join(lines))
    if os.path.isfile(os.path.splitext(file)[0] + "1.txt"):
        os.remove(file)
        os.rename(os.path.splitext(file)[0] + "1.txt", os.path.splitext(file)[0] + ".txt")
        
def modify_content_in_file(words_df,file):
    with open(file, "r", encoding = "utf8") as oldfile, open(os.path.splitext(file)[0] + "1.txt", "w", encoding = "utf8") as newfile:
        lines = oldfile.readlines()
        for line in lines:
            write = 0
            words = line.split(" ")
            
            for word in words:
                if word.startswith("lengthend"):
                    break
                #row = words_df.loc[words_df['token'] == word]
                #print ("WORD IN FILE" + word)
                row = words_df.loc[words_df['token'] == word]
                if not row.empty:
                    if row['replacement'].iloc[0] != "null":
                #words_df.loc[words_df['token'] == word, 'token'].iloc[1] != "null":
                        #replace the word with its replacement
                        #print (words_df.loc[words_df['token'] == word, 'token'])
                        #if not pd.isnull(words_df.loc[words_df['token'] == word, 'token']):
                        
                        ####if words_df.loc[words_df['token'] == word, 'token'] is not None:
                        #print(math.isnan(row['replacement'].iloc[0]))
                        if type(row['replacement'].iloc[0]) == str: #not math.isnan(row['replacement'].iloc[0]):
                            line = line.replace(row['token'].iloc[0], row['replacement'].iloc[0])
                        write = 1;
                elif re.search(r'[`\-=~—!@#$%^&*()_+\[\]{};\'\\:"|<,./<>? ]', word):
                    write = 1;
                else:
                    write = 0
                    break
            if write == 1:
                newfile.write(line)
                    
    if os.path.isfile(os.path.splitext(file)[0] + "1.txt"):
        os.remove(file)
        os.rename(os.path.splitext(file)[0] + "1.txt", os.path.splitext(file)[0] + ".txt")   
        
    
        
    #iterate through the dataframe
    '''with open(file, "r", encoding = "utf8") as oldfile, open(os.path.splitext(file)[0] + "1.txt", "w", encoding = "utf8") as newfile:
        lines = oldfile.readlines()
        for index, row in words_df.iterrows():
            print (row['replacement'])
            if row['replacement'] != "null" and type(row['replacement']) == str:# not math.isnan(row['replacement']):
                
            #replace the word with its replacement
                for line in lines:
                    line = line.replace(row['token'], row['replacement'])
                    newfile.write(line)    det
    if os.path.isfile(os.path.splitext(file)[0] + "1.txt"):
        os.remove(file)
        os.rename(os.path.splitext(file)[0] + "1.txt", os.path.splitext(file)[0] + ".txt")
      '''  
    
        
        
        


   
#print (convert_pdf_to_txt("gaban.pdf", "gabanorig.txt"))
#print (convert_pdf_to_txt("nirmala.pdf", "nirmalaorig.txt"))
#print (read_lines("godanorig.txt", "godan.txt"))
#print (read_lines("gabanorig.txt", "gaban.txt"))
#print (read_lines("nirmalaorig.txt", "nirmala.txt"))

#convert the PDF files to unprocessed text files

##print (convert_pdf_to_txt("corpora", "pdf", "orig"))
#clean the text files and store in a different directory
print (read_lines("corpora", "orig", "clean"))
#get details of a word from the Hindi WordNet
#word = "िदिन"
#read_word("s")
clean_words("corpora", "clean", "hwn data/word.txt")


# In[3]:
'''

cd T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2\Final Corpora\Todo


# In[24]:


import csv

with open("bbc-test.csv", "r", encoding = "utf8") as source:
    rdr= csv.reader(source, delimiter = "^")
    with open("bbc-test-clean.txt", "w", encoding = "utf8") as result:
        #wtr= csv.writer( result )
        for r in rdr:
            #remove new line characters
            text = r[1].replace('\r', '')
            text = text.replace('\n', '')
            #remove commas
            text = text.replace(',', '')
            #remove quotes
            text = text.replace('"', '')
            text = text.replace("'", '')
            #remove brackets
            text = text.replace('(', '')
            text = text.replace(')', '')
            text = text.strip()
            text = text.replace(".", "।\nweb,news,na,na,")
            text = text.replace("?", "\nweb,news,na,na,")
            text = text.replace("!", "\nweb,news,na,na,")
            #remove the last line
            text = text[:text.rfind('\n')]
            if text != '':
                result.write("web,news,na,na," + text)


# In[28]:


import csv

with open("bbc-train.csv", "r", encoding = "utf8") as source:
    rdr= csv.reader(source, delimiter = "\t")
    with open("bbc-train-clean.txt", "w", encoding = "utf8") as result:
        #wtr= csv.writer( result )
        for r in rdr:
            #remove new line characters
            text = r[1].replace('\r', '')
            text = text.replace('\n', '')
            #remove commas
            text = text.replace(',', '')
            #remove quotes
            text = text.replace('"', '')
            text = text.replace("'", '')
            #remove brackets
            text = text.replace('(', '')
            text = text.replace(')', '')
            text = text.strip()
            text = text.replace(".", "।\nweb,news,na,na,")
            text = text.replace("?", "\nweb,news,na,na,")
            text = text.replace("!", "\nweb,news,na,na,")
            #remove the last line
            text = text[:text.rfind('\n')]
            if text != '':
                result.write("web,news,na,na," + text)


# In[ ]:


#include lines containing only hindi, puncutations and numbers
import csv
import os
import codecs
import re
outfile = codecs.open("web.txt", "w", "utf-8")
path = "Web/tokenised/"
dirs = os.listdir(path)
for file in dirs:
    with open("Web/tokenised/" + file, "r", encoding = "utf8") as rfp:
            #read each line of the unprocessed text file
            line = rfp.readline()
            while line:
                line = line.replace('web,news,na,na,', '')
                line = line.replace('"', '')
                #remove commas
                line = line.replace(',', '')
                #remove quotes
                line = line.replace('"', '')
                line = line.replace("'", '')
                #remove brackets
                line = line.replace('(', '')
                line = line.replace(')', '')
                line = line.strip()
                if not line.isspace():
                    #hindi is a flag that indicates that the current word is Hindi (or a special character)
                    hindi = 1
                    #split the line into words to detect non-Hindi, non-special characters
                    wordStructure = line.split()
                    for word in wordStructure:
                        print(word)
                        #check if it is a punctuation or a digit
                        if not re.search(r'[`\-=~—!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?0123456789 ]', word):
                            #read each letter of the current word
                            for letter in word:
                                lang = detect_language(letter)
                                #set the flag to 0 if the character is not Hindi (or a special character)
                                if lang != "hindi":
                                    #check if it is a digit in Hindi
                                    if not letter in ['०','१','२','३' ,'४','५' ,'६' ,'७','८','९']:
                                        hindi = 0
                                        break #stop processing the line
                        else:
                            hindi = 0
                            break
                    #if the word is Hindi (or a special character), write the line to the clean file
                    if hindi == 1:
                        outfile.write("web,news,na,na," + line + "\n")
                #read the next line
                line = rfp.readline()
                

'''