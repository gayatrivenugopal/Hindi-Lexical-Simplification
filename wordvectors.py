# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 23:40:16 2018

@author: Gayatri
"""

import gensim
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from nltk.corpus import brown

sentences = brown.sents()
model = gensim.models.Word2Vec(sentences, min_count = 1)
model.save('brown_model')
print("Model trained and saved")

model = Word2Vec.load('brown_model')
print(model.wv.most_similar(positive = ['mother']))
#print(model.doesnt_match("cat dog table".split()))
#vector representation of word human
#print(model['human'])

model = KeyedVectors.load_word2vec_format('wordvectorsmodel.txt', binary=False, encoding = 'utf-8', unicode_errors='ignore')

result = model.most_similar(positive=['रोटी'])
print(result)

def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)
    
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
        
    plt.figure(figsize=(16, 16)) 
    for i in range(len(x)):
        plt.scatter(x[i],y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()