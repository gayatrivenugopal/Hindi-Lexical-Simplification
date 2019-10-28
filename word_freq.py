#Source: https://medium.com/towards-artificial-intelligence/text-mining-in-python-steps-and-examples-78b3f8fd913b
#Source: https://kavita-ganesan.com/tfidftransformer-tfidfvectorizer-usage-differences/#.XWtLKaeYW00

from nltk.probability import FreqDist
import nltk
from nltk.tokenize import word_tokenize
import os
import pandas as pd
import stanfordnlp
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

#PATH = 'To analyze/Clean TDIL Corpora/Clean English_Hindi_Tourism Text Corpus - EILMT/English_Hindi/Clean Hindi/'
#PATH = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Corpus to release/To analyze/Clean TDIL Corpora/Clean English_Hindi_Tourism Text Corpus - EILMT/CLEAN/'
#PATH = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Corpus to release/To analyze/Clean TDIL Corpora/Clean Hindi_English_ilci2corpus Agriculture Entertainment/Hindi Clean/'
#PATH = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Corpus to release/To analyze/Clean TDIL Corpora/Clean Hindi Monolingual Text Corpus ILCI II/'
#PATH = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Corpus to release/To analyze/Clean TDIL Corpora/Clean NamedEntityAnnotatedCorporaForHindi/Clean/'
#PATH = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Corpus to release/To analyze/Clean TDIL Corpora/Clean NER Corpora Hindi Marathi Punjabi/Clean/'
#PATH = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Corpus to release/To analyze/Clean TDIL Corpora/Hindi_English_Health ILCI_Clean/'
#PATH = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Corpus to release/To analyze/Done CFILT/Clean Final Hindi MWE Dataset/from corpus/'
#PATH = '/opt/PhD/Work/JHWNL_1_2/Final Corpora/Corpus to release/To analyze/Done CFILT/Clean Final Hindi MWE Dataset/from wordnet/'
#PATH = 'Clean hin_corp_unicode/'
#PATH = 'hindi/'
PATH = 'Entire/'
out_file = open(PATH + 'freq.txt', 'w', encoding = 'utf-8')
out_lemma_file = open(PATH + 'lemma_freq.txt', 'w', encoding = 'utf-8')
out_tfidf_file = open(PATH + 'tfidf.txt', 'w', encoding = 'utf-8')
out_tfidf_lemma_file = open(PATH + 'lemma_tfidf.txt', 'w', encoding = 'utf-8')

sentences = []
lemmatised_sentences = []
token_collection = []
lemmatised_tokens = []

#stanfordnlp.download('hi')
nlp = stanfordnlp.Pipeline(lang='hi')

def get_root(token):
    """ Return the lemma for the specified token
    Args tokens (str): token to be lemmatised
    Return (str): lemmatised token
    """
    doc = nlp(token)
    for sentence in doc.sentences:
        for word in sentence.words:
            return word.lemma
    return ''

for filename in sorted(os.listdir(PATH)):
    print(PATH+filename)
    file = open(PATH + filename, 'r', encoding = 'utf-8', errors='ignore')
    for line in file.readlines():
        if line.strip() != '' and line.strip() != '\n':
            sentences.append(line)
            lemmatised_sentences.append(line)
            for token in word_tokenize(line):
                token_collection.append(token)
                root = get_root(token)
                if root != '' and root != None:
                    lemmatised_sentences[len(lemmatised_sentences)-1] = lemmatised_sentences[len(lemmatised_sentences)-1].replace(token, root)
                    lemmatised_tokens.append(root)
                else:
                    lemmatised_tokens.append(token)


if len(token_collection) != 0:
    fdist = FreqDist(token_collection)
    for key in list(fdist.keys()):
        print('word: ', key)
        print(fdist.get(key))
        out_file.write(key + ',' + str(fdist.get(key)) + '\n')

if len(lemmatised_tokens) != 0:
    fdist = FreqDist(lemmatised_tokens)
    for key in list(fdist.keys()):
        print('word: ', key)
        print(fdist.get(key))
        out_lemma_file.write(key + ',' + str(fdist.get(key)) + '\n')


#td-idf - lemmas?
#instantiate CountVectorizer()
cv_words=CountVectorizer()
cv_lemmas=CountVectorizer()
# this steps generates word counts for the words in your docs
word_count_vector=cv_words.fit_transform(sentences)
lemma_count_vector = cv_lemmas.fit_transform(lemmatised_sentences)

print(word_count_vector.shape)
print(lemma_count_vector.shape)

# create the transform
tfidf_transformer_words = TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer_lemmas = TfidfTransformer(smooth_idf=True,use_idf=True)

# tokenize and build vocab
tfidf_transformer_words.fit(word_count_vector)
tfidf_transformer_lemmas.fit(lemma_count_vector)

# print idf values
df_idf_words = pd.DataFrame(tfidf_transformer_words.idf_, index=cv_words.get_feature_names(),columns=["idf_weights"])
df_idf_lemmas = pd.DataFrame(tfidf_transformer_lemmas.idf_, index=cv_lemmas.get_feature_names(),columns=["idf_weights"])

# sort ascending
df_idf_words.sort_values(by=['idf_weights'])
df_idf_lemmas.sort_values(by=['idf_weights'])

out_tfidf_file.write(df_idf_words.to_csv())
out_tfidf_lemma_file.write(df_idf_lemmas.to_csv())
