# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import string

groups = []
i = 1
limit = 201
stopwords = []
task2_data = []
token_dict = dict()
data_dict = dict()

#create a list of stopwords
with open("stopwords") as stopwords_file:
    for line in stopwords_file.readlines():
        line = line.split(",")[0]
        stopwords.append(line.strip("\n"))

with open("Task2.csv") as task2_file:
    task2_data = task2_file.readlines()
    
for no in range(1, 21):
    groups.append("cwig" + str(no))

sentences_file = open("Sentences_Cleaned.csv", "r")
    
for gno in groups:
    pid = []
    data_dict = dict()
    with open("Groups.csv") as groups_file:
        lines = groups_file.readlines()
        for line in lines:
            #print(line)
            line = line.strip("\n")
            details = line.split(",")
            if details[0] == gno and details[1].find("temp") == -1:
                pid.append(details[1].strip("'"))
                token_dict[details[1]] = dict()
                data_dict[details[1]] = dict()
            #pid contains participant ids in the current group
        #print(data_dict.keys())
        i = 1
        for sentence_no in range(i, limit):
				#print(sentence_no)
                sentences_line = sentences_file.readline()
                if sentences_line.strip() == "":
                    continue
				#print("line: ", sentences_line)
                sentence = sentences_line.strip("\n")[sentences_line.find(",")+1:]
				#print("sentence:", sentence)
                tokens = sentence.split(" ")
				#print(tokens)
                for token in tokens:
                    if token == 'sentence':
                        continue
					#remove punctuations
                    for punctuation in string.punctuation:
                        token = token.strip(punctuation)
                    if token not in stopwords and token != "।" and token != "":
                        for line in task2_data:
							#print(line)
                            line = line.strip("\n")
                            line = line.split(",")
                            curr_pid = line[0]
                            curr_word = line[1].strip("'")
						   
							
                            if curr_pid in token_dict.keys() and curr_pid in pid and token not in token_dict[curr_pid]:
                                data_dict[curr_pid][token] = 0
                                token_dict[curr_pid][token] = 0
                            if curr_pid in pid and curr_word == token and (token not in token_dict[curr_pid] or token_dict[curr_pid][token] == 0):
								#print(curr_pid)
								
                                complexity = line[2]
								#print(data_dict)
								
                                data_dict[curr_pid][token] = int(complexity)
								
                                token_dict[curr_pid][token] += 1
		#print("sample: ", data_dict['ocwnigep1'])
    with open("data_dict_" + str(gno) + ".txt", "w") as data_dict_file:
        for key, details in data_dict.items():
            data_dict_file.write(str(key) + ",")
            for word, label in details.items():
                data_dict_file.write(word + ":" + str(label) + ",")
            data_dict_file.write("\n")
