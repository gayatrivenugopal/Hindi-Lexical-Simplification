import fasttext
import glob

filenames = glob.glob("./gayatri/train/pos/*.txt")
with open('train.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write('__label__pos '+line+'\n')
                
filenames = glob.glob("./gayatri/train/neg/*.txt")
with open('train.txt', 'a') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write('__label__neg '+line+'\n')
                

filenames = glob.glob("./gayatri/test/pos/*.txt")
with open('test.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write('__label__pos '+line+'\n')
                
filenames = glob.glob("./gayatri/test/neg/*.txt")
with open('neg_test.txt', 'w+') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write('__label__neg '+line+'\n')


#classification
classifier = fasttext.supervised('train.txt', 'model', label_prefix='__label__')
result = classifier.test('test.txt')

print('Precision: ', result.precision)
print('Recall: ', result.recall)
print('Number of examples: ', result.nexamples)

texts = ['This was a good movie', 'This movie could have been better', 'Horrible movie']
labels = classifier.predict(texts)
print(labels)
