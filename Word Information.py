# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:38:59 2018

@author: Gayatri
"""
import os
import codecs
import subprocess
import threading

os.chdir("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2")
output_file = "synsets.txt"
sense_count = 0

def read_file():
    """Read the content of the file containing the senses of a word"""
    with codecs.open("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/"+output_file, "r", encoding="utf-8") as file:
        for line in file.readlines() :
            if line.lower().startswith("sense count is"):
                sense_count = line[line.lower().find("sense count is")+
                               len("sense count is "):]
                break
    print(sense_count)
    #TODO: write to database
            
def get_num_of_synsets(word):
    """Retrieves the number of synsets for a given word from the Hindi WordNet

    Keyword arguments:
    word -- the word whose synsets are to be retrieved
    """
    
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
    threading.Timer(15, read_file).start()
    

print(get_num_of_synsets("कल"))