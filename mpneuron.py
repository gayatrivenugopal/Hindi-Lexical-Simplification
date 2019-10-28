import sklearn.datasets
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split


breast_cancer = sklearn.datasets.load_breast_cancer()

X = breast_cancer.data
Y = breast_cancer.target
data = pd.DataFrame(breast_cancer.data, columns = breast_cancer.feature_names)
data['class'] = breast_cancer.target
'''
print(data.head())
print(data['class'].value_counts())
print(breast_cancer.target_names)
print(data.groupby('class').mean())
'''

X = data.drop('class', axis = 1) #delete the column
Y = data['class']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, stratify = Y, random_state = 1) #some constant number as random state so that every time the split runs, the split data stays the same
print(Y.mean(), Y_train.mean(), Y_test.mean()) #means should be comparable across test and train so that the data is not  skewed

print(X.shape, X_train.shape, X_test.shape)


plt.plot(X_train, '*')
plt.xticks(rotation='vertical')
plt.show()

X_binarised_3_train = X_train['mean_area'].map(lambda x: 0 if x < 1000 else 1)

X_binarised_train = X_train.apply(pd.cut, bins = 2, labels = [0,1]) #cut cols
X_binarised_test = X_test.apply(pd.cut, bins = 2, labels = [0,1])

X_binarised_test = X_binarised_test.values #convert to numpy array
X_binarised_train = X_binarised_train.values


class MPNeuron:
    def __init__(self):
        self.b = None

    def model(self, x):
        return (sum(x) >= self.b)

    def predict(self, X):
       Y = [] 
       for x in X:
            result = self.model(x)
            Y.append(result)
       return np.array(Y)

    def fit(self, X, Y):
        accuracy = {}
        for b in range(X.shape[1] + 1): #no. of columns
            self.b = b
            y_pred = seld.predict(X)
            accuracy[b] = accuracy_score(Y_pred, Y)

        best_b = max(accuracy, key = accuracy.get)
        self.b = best_b

        print('Optimal value of b is ', best_b)
        print('Highest accuracy is ', accuracy[best_b])


mp_neuron = MPNeuron()
mp_neuron.fit(X_binarised_train, Y_train)
'''
