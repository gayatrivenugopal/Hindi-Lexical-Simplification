from os import listdir
import string
import re

#store only unique sentences in the files
#dir_path = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Corpus to release/duplicate'
#clean_text()

def clean_text(dir_path, files):
    """ Remove punctuations, isolate digits, remove poornaviram.
    """
    digits = ['०','१','२','३','४','५','६','७','८','९']
    #files = [f for f in listdir(dir_path)]

    lines = set()
    for filename in files:
        print(filename)
        print(dir_path+'/' + filename)
        with open(dir_path + '/' + filename, 'r', encoding = 'utf-8') as fp:
            #print(fp.readlines())
            for line in fp:
                line = line.replace('?','\n')
                line = line.replace('!','\n')
                line = line.replace('।','\n')
                line = line.replace('©',' ')
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
                line = ' '.join(line.split())
                #line = line.replace('\n',' .\n')
                lines.add(line.strip())
            fp.close()
            file = open(dir_path + '/' + filename, 'w', encoding = 'utf-8')
            for id, line in enumerate(lines):
                file.write(str(line) + '\n')
            file.close()

def fetch_duplicate_sentences():
    """ Find out if there are duplicate sentences in the corpus.
    If so, store the file names in a separate file.
    """
    files = [f for f in listdir(dir_path)]

    lines = {}
    duplicate_file = open(dir_path + '/' + 'duplicates.txt', 'w', encoding = 'utf-8')
    for filename in files:
        with open(dir_path + '/' + filename, 'r', encoding = 'utf-8') as fp:
            #duplicate_file.write('new: ' + filename + '\n')
            lines[filename] = []
            for line in fp:
                print(line)
                print(lines)
                files = exists(line, lines)
                if len(files) != 0 and line.strip() != '.':
                    for i in files:
                        duplicate_file.write(i + ' ; ' + line.replace('\n','') + ' ; ' + filename + '\n')
                else:
                    lines[filename].append(line)

def exists(line, lines):
    """Checks if the sentence exists in a list in the dictionary passed
    Arguments:
    line: the sentence to be searched
    lines: the dictionary containing the filename and the list of sentences in
    the file
    Returns:
    List of filenames which contain the line
    """
    files = []
    for file, list_lines in lines.items():
        if line in list_lines:
            files.append(file)
    return files

#fetch_duplicate_sentences()
