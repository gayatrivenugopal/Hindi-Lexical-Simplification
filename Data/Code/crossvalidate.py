# %%
import os
import time
import json
import pandas as pd
from sklearn import svm
from sklearn.model_selection import StratifiedKFold
from imblearn.under_sampling import NearMiss
from imblearn.over_sampling import SMOTE
import eli5
from eli5.sklearn import PermutationImportance
from collections import Counter
import matplotlib.pyplot as plt
from IPython.display import display

from models import get_model

#from data_tests import *
from evaluation import get_accuracy

def crossvalidate(splits, X, y, baseline = -1, model_num = None, resample = 0, 
feature_set = None, n_features = 0, feature_importance = 0, average_method='macro', path= None):
    """
    Store the results calculated according to the arguments and store them in a file.
    Arguments:
    splits (int): number of folds
    X (dataframe): examples
    y (dataframe): target/label
    baseline (int): -1 for no baseline, 1 for all predictions as 1, 0 for all predictions as 0
    model_num (int): classification model
    1: 
    2:
    3:
    4:
    5:
    6:
    resample (int): -1 for undersampling, 1 for oversampling and 0 for no resampling
    feature_set (list): list of features to be considered
    n_features (int): the number of features to be considered at a time for classification/importance
    feature_importance (int): 0 for absent, 1 for present
    average_method: macro by default
    path: the path to the directory where the recordings should be stored
    """
    

    #prepare the dictionary to be written to the file
    data_dict = dict()
    dir_name = path + str(time.time())
    os.mkdir(dir_name)
    #open the config file for writing
    config_file = open(dir_name + '/config.jso n', 'w')
    data_dict =  {'model_num':model_num}
    data_dict =  {'baseline':baseline}
    data_dict.update({'resample':resample})
    data_dict.update({'feature_set':feature_set})
    data_dict.update({'n_features':n_features})
    data_dict.update({'feature_importance':feature_importance})

    model = get_model(model_num)
    
    kfold = StratifiedKFold(n_splits=splits, shuffle=True, random_state=777)
    
    accuracy_values = list()
    
    for train_index, test_index in kfold.split(X, y):
        #create train-test splits
        X_train, y_train = X.iloc[train_index], y.iloc[train_index]
        X_test, y_test = X.iloc[test_index], y.iloc[test_index]

        #create test set labels for the baseline if applicable
        if baseline == 0:
            y_test = y_test.replace(1,0)
        elif baseline == 1:
            y_test = y_test.replace(0,1)
            
        #resample the training set (if applicable)
        if resample == -1:
            #undersample
            '''NearMiss 3 . NearMiss-3 is a 2-step algorithm: first, for each minority sample, 
            their :m nearest-neighbors will be kept; then, the majority samples selected are the 
            on for which the average distance to the k nearest neighbors is the largest.'''
            nm = NearMiss(version=3)
            print(str(sorted(Counter(y_train).items())))
            X_resampled, y_resampled = nm.fit_resample(X_train, y_train)
            X_train = X_resampled
            y_train = y_resampled
            print(sorted(Counter(y_train).items()))
        elif resample == 1:
            #oversample
            X_resampled, y_resampled = SMOTE().fit_resample(X_train, y_train)
            X_train = X_resampled
            y_train = y_resampled
            print(sorted(Counter(y_resampled).items()))
        #write the training dataset class distribution to the file
        file = open(dir_name + '/train_val_dist.csv', 'a')
        file.write(str(sorted(Counter(y_train).items())))
        file.write('\n')
        file.close()

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        accuracy = get_accuracy(y_test, y_pred)
        accuracy_values.append(accuracy * 100)

        if feature_importance == 1:
            if model_num == 1 or model_num == 3:
                feat_importances = pd.Series(model.feature_importances_, index=X.columns)
            elif model_num == 2:
                feat_importances = pd.Series(abs(svm.coef_[0]), index=X.columns)
            print(feat_importances)
            feat_importances.nlargest(20).plot(kind='barh')
            #plot_importance(model)
            plt.show()
            
            perm = PermutationImportance(model, random_state=1).fit(X_train, y_train)
            display(eli5.show_weights(perm, feature_names = X_train.columns.tolist()))

            #write the feature importance values to the file
            file = open(dir_name + '/feature_importances.csv', 'a')
            file.write(str(model.feature_importances_))
            file.write('\n')
            file.close()
            
    data_dict['accuracy'] = sum(accuracy_values)/len(accuracy_values)
    json.dump(data_dict, config_file)
    config_file.close()

data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/Basic Binary Classification/DataForClassification.csv')
#print(data.iloc[:, 1:-1].head())
del data['word']
print(data.columns)
print(data.groupby('label').mean()) #class means
#splits is 5 so that the test size is 1/5 = 20%
crossvalidate(5, data.iloc[:, :-1], data.label, model_num = 1, feature_importance = 1, baseline = -1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#TODO: evaluation and learning curve

# %%
