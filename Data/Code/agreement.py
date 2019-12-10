from data import Data
import numpy as np
import csv
import json

def fleiss_kappa(M):
  """
  See `Fleiss' Kappa <https://en.wikipedia.org/wiki/Fleiss%27_kappa>`_.
  :param M: a matrix of shape (:attr:`N`, :attr:`k`) where `N` is the number of subjects (words) and `k` is the number of categories into 
  which assignments are made. `M[i, j]` represent the number of raters who assigned the `i`th subject to the `j`th category.
  :type M: numpy matrix
  """
  N, k = M.shape  # N is # of items, k is # of categories
  #print(M)
  #print(M[0,:])
  n_annotators = float(np.sum(M[0, :]))  # # of annotators

  p = np.sum(M, axis=0) / (N * n_annotators)
  P = (np.sum(M * M, axis=1) - n_annotators) / (n_annotators * (n_annotators - 1))
  Pbar = np.sum(P) / N
  PbarE = np.sum(p * p)

  kappa = (Pbar - PbarE) / (1 - PbarE)

  return kappa


if __name__ == '__main__':
    #load the ranked dataset
    #data = Data().data
    #words = set()
    #words = data['words']
    #print(words, len(words))
    #print(len(data[data['complexity']==0]))

    #TODO:  Calculate Fleiss' Kappa

    '''
    array: number of raters who assigned word i to category j (j=0 simple,1 complex)
    '''
    agreement = dict()
    reader = csv.reader(open("matrix.csv", "r", encoding='utf-8'), delimiter=",")
    x = list(reader)
    result = np.array(x)[:,1:] #remove the index column
    for i in range(1, 21):
        rows, cols = np.where(result == 'cwig'+str(i))
        subset_with_words = result[rows] #fetch the records (groupwise)
        #print(subset_with_words[0:1, 0:1])
        subset = subset_with_words[:,2:]
        subset = subset.astype(np.float)
        #print(subset)
        #print(subset[:,0])
        i = 0
	#TODO: find the number of raters for each word (group by word, calculate simple plus complex)
        #TODO: remove this -> replace the value in 'simple' with difference of 5-(complex+simple) (users did not find it complex)
        for row in subset:
            #print(row)
            #print('before: ', subset[i,0], subset[i,1])
            subset[i,0] += 5-row[0]-row[1]
            #print('after: ', subset[i,0], subset[i,1])
            i += 1
        print('Subset: ', subset_with_words[0:1,0:1])
        value = str(fleiss_kappa(subset))
        print(value)
        agreement[subset_with_words[0:1,0:1].item()] = value
        json.dump(agreement,open('fleiss_agreement.json','w'))
