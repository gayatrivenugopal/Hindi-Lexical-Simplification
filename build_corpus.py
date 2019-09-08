from os import listdir
from ordered_set import OrderedSet
import string
import re

#clean all the files in a directory
#store only unique sentences in the files


def clean_text(dir_path, files):
    """ Remove punctuations, isolate digits, remove poornaviram.
    """
    digits = ['०','१','२','३','४','५','६','७','८','९']
    #files = [f for f in listdir(dir_path)]

    #lines = set()
    for filename in files:
        lines = OrderedSet()
        print("FILE: ", filename)
        print(dir_path+'/' + filename)
        with open(dir_path + '/' + filename, 'r', encoding = 'utf-8', errors = 'ignore') as fp:
            for line in fp:
                line = line.replace('?','\n')
                line = line.replace('.','\n')
                line = line.replace('!','\n')
                line = line.replace('।','\n')
                line = line.replace('©',' ')
                line = line.replace('“',' ')
                line = line.replace('”',' ')
                line = line.replace('…',' ')
                #replace English characters and digits
                line = re.sub(r'[a-zA-Z0-9]', ' ', line)
                temp = line
                for character in temp:
                    if character in string.punctuation:
                        line = line.replace(character,' ')
                for digit in digits:
                    line = line.replace(digit,' ' + digit + ' ')
                line = line.replace('’','')
                line = line.replace('‘','')
                #replace multiple spaces with a single space
                line = ' '.join(line.split(' '))
                #line = line.replace('\n',' .\n')
                #print(line.strip())
                if line != '' and line != '\n':
                    if line.strip() not in lines:
                        lines.add(line.strip())
            fp.close()
            file = open(dir_path + '/' + filename, 'w', encoding = 'utf-8')
            for id, line in enumerate(lines):
                file.write(str(line) + '\n')
            file.close()

dir_path = ''
files = sorted([f for f in listdir(dir_path)])
clean_text(dir_path, files)
