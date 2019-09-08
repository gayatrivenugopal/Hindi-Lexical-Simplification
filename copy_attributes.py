import re
import os
from os import listdir

#retrieve the attributes from the unclean text file in the source directory
# and add them to the file in the destination directory
source_dir = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Done corpora/Wikipedia (copy 1)/'
dest_dir = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Done corpora/Wikipedia/'

for f in sorted(listdir(source_dir)):
    if f in listdir(dest_dir):
        source = source_dir + f
        dest_in = dest_dir + f
        dest_out = open(dest_dir + 'clean_' + f, 'w', encoding = 'utf-8')
        first_line = ',,,,'
        with open(source, 'r', encoding = 'utf-8') as fp:
            for source_line in fp:
                if len(source_line.strip()) > 3:
                    elements = source_line.split(',')
                    first_line = elements[0] + ',' + elements[1] + ',' + elements[2] + ',' + elements[3] + ','
                    break
        with open(dest_in, 'r', encoding = 'utf-8') as fp:
            for line in fp:
                dest_out.write(first_line + line)
            os.remove(dest_in)
            os.rename(dest_dir + 'clean_' + f, dest_in)
