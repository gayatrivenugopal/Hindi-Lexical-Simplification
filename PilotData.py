import pandas as pd
import numpy as np
import csv
import os
from py4j.java_gateway import JavaGateway
from py4j.java_gateway import java_import

def remove_duplicates(file):
	"""
	Removes duplicate values from the row number and decrements the corresponding count
	"""
	df = pd.read_csv(file, encoding='utf-8')
	new_df = df
	for index,row in df.iterrows():
		count = row['Count']
		rows = row['Row'].split(',')
		#remove duplicates and reduce count
		new_rows = []
		for value in rows:
			if not value in new_rows:
				new_rows.append(value)
			else:
				count = count - 1
		new_df.at[index,'Count'] = count
		#df.at[index,'Row'] = '"' + ','.join(new_rows) + '"'
		new_df.at[index,'Row'] = ','.join(new_rows)
	new_df.to_csv(file.replace("Native/", "Native/clean_"), encoding='utf-8', index=False)

def get_roots(word):
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
    gateway = JavaGateway.launch_gateway(classpath="/opt/PhD/Work/JHWNL_1_2/Code/hindiwn.jar")
    java_import(gateway.jvm,'WordnetToolsSimple')
    gateway.jvm.WordnetToolsSimple.initialize()
    os.chdir("/opt/PhD/Work/JHWNL_1_2/Code")

    #java_import(gateway.jvm,'WordnetToolsSimple')
    #gateway.jvm.WordnetToolsSimple()
    roots = gateway.jvm.WordnetToolsSimple.getRoot(word)

    #form a list if there are multiple roots
    if roots.find(";") != -1:
        roots = roots.split(";")#form a list
        roots = roots[:-1] #remove the '\r\n' element
        #roots = [root.split(":")[1] for root in roots]#remove the part before the ':'
    return roots

def merge_common_roots(file):
	"""
	Converts the words in the csv file to their root forms
	"""
	df = pd.read_csv(file, encoding='utf-8')
	root_dict = {}
	for index,row in df.iterrows():
		if(row['Root'] is np.nan):
			continue
		if(row['Root'] in root_dict):
			#print(row['Root'], " ", df.iloc[[index]]['Rowno'])
			#print("INDEX", " ", str(index))
			root_dict[row['Root']] = root_dict[row['Root']] + "," + str(index)
		else:
			root_dict[row['Root']] = str(index)
	f = open('dict.txt','w', encoding='utf-8')
	f.write(str(root_dict))
	f.close()
	#iterate through the dictionary, and for each root, get the indices.
	#If index is more than 1, add the count from all the indices and store in the first index,
	# merge the row numbers from all the indices and store in the first index.
	#Remove the rows belonging to the rest of the indices

	new_df = df.copy()
	for key,value in root_dict.items():
		if(len(value.split(",")) > 1):
			indices = value.split(",")
			first_index = int(indices[0])
			rowno = ''
			count = 0
			for i in indices:
				count += int(df.iloc[[int(i)]]['Count'])
				rowno += "," + str(df.iloc[int(i)]['Row'])
				new_df.at[int(i),'Row'] = "to be deleted"
			new_df.at[first_index,'Count'] = count
			new_df.at[first_index,'Row'] = rowno

	new_df.to_csv(file, encoding='utf-8', index=False)

def convert_to_root_form(file, i):
	"""
	Converts the words in the csv file to their root forms
	"""
	df = pd.read_csv(file, encoding='utf-8')
	new_df = df
	new_df['Root'] = ''
	for index,row in df.iterrows():
		count = row['Count']
		word = row['Word']
		rows = row['Row'].split(',')

		#get the root of the word
		roots = get_roots(word)
		if(isinstance(roots, list)):
			roots = roots[0][2:]
		else:
			roots = roots[2:]

		#new_rows = []
		new_df.at[index,'Root'] = roots

		i = i + 1
		if i == 25:
			break
		#new_df.at[index,'Row'] = ','.join(new_rows)
	new_df.to_csv(file, encoding='utf-8', index=False)


def convert_to_kalpha_format(filename):
		file = open(filename, "r", encoding = 'utf-8')
		csvfile = csv.reader(file)
		i = 0
		dict_word = {}
		list_raters = []
		for row in csvfile:
			if i == 0:
				i += 1
				continue
			word = row[1]
			str_raters = row[3].strip(',').split(',')
			for value in str_raters:
				if value is not '' and value not in list_raters:
					list_raters.append(value)
			if word not in list(dict_word.keys()):
				dict_word[word] = str_raters
			else:
				for value in str_raters:
					if value is not '':
						dict_word[word].append(value)
		kalpha = open("kalpha.csv", "w", encoding= 'utf-8')

		#write the header
		kalpha.write('word')
		for rater in list_raters:
			kalpha.write(',' + rater)
		kalpha.write('\n')

		#write the values of each cell in each row
		for key, item in dict_word.items():
			kalpha.write(key)
			for rater in list_raters:
				if rater in item:
					kalpha.write(',1')
				else:
					kalpha.write(',0')
			kalpha.write('\n')


#remove_duplicates('Native/nativepilot.csv')
#remove_duplicates('Non Native/nonnativepilot.csv')
#print(get_roots("वल्लरियों"))

#convert_to_root_form('../Data/Pilot/clean_nonnativepilot.csv', 0)
#merge_common_roots('../Data/Pilot/clean_nativepilot.csv')
#convert_to_kalpha_format('../Data/Pilot/Non Native/clean_pilot_nonnative_agreement.csv')
#convert_to_kalpha_format('../Data/Pilot/Native/clean_nativepilot_agreement.csv')
#convert_to_kalpha_format('../Data/Pilot/All.csv')

#get the roots of the words in a file and create a csv
file = open('Complex Words.csv', 'r', encoding = 'utf-8')
updated_file = open('Complex Words with Roots.csv', 'w', encoding = 'utf-8')
updated_file.write("Word" + "," + "Root\n")
reader = csv.reader(file)
i = 0
for row in reader:
	if i == 0 or row[0] == None:
		i += 1
		continue
	print(i)
	word = row[0]
	#print('विक्रय')
	roots = get_roots(word)
	#print(roots)
	if(isinstance(roots, list)):
		roots = roots[0][2:]
	else:
		roots = roots[2:]
	updated_file.write(row[0] + "," + roots + "\n")
