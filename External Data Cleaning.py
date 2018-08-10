# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 12:25:29 2018

@author: Gayatri
"""

import os
import codecs

os.chdir("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Corpora - External/To use/")


outfile = codecs.open("downloadedcorpus.txt", "w", "utf-8")
for filelineno, line in enumerate(open(
        "hindmonocorp05.plaintext", encoding="utf-8")):
        line = line.strip()
        if line.find("<s>") != -1:
            line = (line[line.find("<s>")+3:]).strip()
            line = line.replace("”","'")
            line = line.replace("\"","'")
            line = "web,misc,na,na,\""+line+"\""   
            print(line)
            outfile.write(line+"\n")
       
    