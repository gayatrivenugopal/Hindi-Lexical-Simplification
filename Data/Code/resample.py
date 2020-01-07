from collections import Counter
from sklearn.datasets import make_classification
from imblearn.under_sampling import EditedNearestNeighbours # doctest: +NORMALIZE_WHITESPACE
import pandas as pd
import csv
from collections import Counter
from sklearn.utils import resample


data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/Basic Binary Classification/DataForClassification.csv')
#print(data.iloc[:, 1:-1].head())
del data['word']
#del data['label_avg_rank']
print(data.columns)
X = data.iloc[:, :-1]
y = data['label']
'''
print('Original dataset shape %s' % Counter(y))
enn = EditedNearestNeighbours()
X_res, y_res = enn.fit_resample(X, y)
for i in range(6):
    X_res, y_res = enn.fit_resample(X_res, y_res)
X_res, y_res = enn.fit_resample(X_res, y_res)
X_res, y_res = enn.fit_resample(X_res, y_res)
X_res, y_res = enn.fit_resample(X_res, y_res)
X_res, y_res = enn.fit_resample(X_res, y_res)
print('Resampled dataset shape %s' % Counter(y_res))
print(type(X_res))
'''
'''
from imblearn.over_sampling import SMOTE

# applying SMOTE to our data and checking the class counts
X_resampled, y_resampled = SMOTE().fit_resample(x, y)
print(sorted(Counter(y_resampled).items()))
'''
print(data.label.value_counts())
df_majority = data[data.label==0]
df_minority = data[data.label==1]
 
# Downsample majority class
df_majority_downsampled = resample(df_majority, 
                                 replace=False,    # sample without replacement
                                 n_samples=3000,     # to match minority class
                                 random_state=123) # reproducible results
 
# Combine minority class with downsampled majority class
df_downsampled = pd.concat([df_majority_downsampled, df_minority])
 
# Display new class counts
print(df_downsampled.label.value_counts())
