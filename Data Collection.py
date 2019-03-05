''' Read from folders - wiki, twitter, and novels
Open each file and count the number of lines
generate a random number between 1 and the number of lines
use this as the line number, extract the sentence part of the string and store in a file as follows:
folder name, file name,,sentence\n '''

import os
import random

base_path = "T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Final Corpora/"

def read_directory(out_file, category):
	for filename in os.listdir(os.getcwd()):
		file = open(filename, "r", encoding="utf-8")
		num_lines = sum(1 for line in file)
		if num_lines != 0:
			print(filename," ",num_lines)
			random_line_number = random.randint(1, num_lines)
			file.seek(0)
			lines = file.readlines()
			#print(lines)
			random_line = lines[random_line_number-1]
			random_line = random_line.split(",", 4)[-1]
			print(category + "," + filename.strip(".txt") + "," + random_line.strip('"'))
			out_file.write(category + "," + filename.strip(".txt") + "," + random_line.strip('"'))

for i in range(1,101):
	out_file = open(base_path + "Manual Annotation/" + str(i) + ".txt", "w", encoding="utf-8")
	#os.chdir(base_path + "Twitter")
	#read_directory(out_file, "Twitter")

	#Copy Twitter lines from Q1.txt
	file = open(base_path + "Q1.txt", "r", encoding="utf-8")
	lines = file.readlines()
	lines = lines[:30]
	strlines = "".join(str(x) for x in lines)
	out_file.write(strlines)
	
	os.chdir(base_path + "Novels")
	read_directory(out_file, "Novels")
	os.chdir(base_path + "Wikipedia")
	read_directory(out_file, "Wiki")