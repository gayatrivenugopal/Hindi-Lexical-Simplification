# %%
import os
import json
import pandas as pd
import numpy as np
import eli5
from sklearn import svm
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import ShuffleSplit
from imblearn.under_sampling import NearMiss
from imblearn.over_sampling import SMOTE
from eli5.sklearn import PermutationImportance
from collections import Counter
import matplotlib.pyplot as plt
from IPython.display import display

from models import get_model
from data_tests import *
from evaluation import get_metrics
from evaluation import plot_lc
    

def crossvalidate(directory_name, splits, data, X, y, baseline = -1, model_num = None, resample = 0, 
feature_set = None, feature_importance = 0, average_method = 'macro', path= None):
    """
    Store the results calculated according to the arguments and store them in a file.
    Arguments:
    directory_name (str): the directory under which the files should be stored
    splits (int): number of folds
    data (dataframe): the whole dataset
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
    feature_importance (int): 0 for absent, 1 for present
    average_method: macro by default
    path: the path to the directory where the recordings should be stored
    """
    

    #prepare the dictionary to be written to the file
    data_dict = dict()
    metrics_dict = dict()
    
    dir_name = path + directory_name + '/'
    os.mkdir(dir_name)
    #create a directory for each split
    for fold in range(1, splits + 1):
        os.mkdir(dir_name + str(fold))
        print(dir_name + str(fold))
    #open the config file for writing
    config_file = open(dir_name + 'config.json', 'w')
    #open the metrics file for writing
    metrics_file = open(dir_name + 'metrics.json', 'w')

    data_dict =  {'model_num':model_num}
    data_dict =  {'baseline':baseline}
    data_dict.update({'resample':resample})
    data_dict.update({'feature_set':feature_set})
    data_dict.update({'n_features':n_features})
    data_dict.update({'feature_importance':feature_importance})    
    
    metrics_dict = dict()
    metrics_dict['f1_macro'] = list()
    metrics_dict['tpr'] = list() 
    metrics_dict['tnr'] = list()
    metrics_dict['fpr'] = list()
    metrics_dict['precision'] = list()
    metrics_dict['recall'] = list()
    metrics_dict['accuracy'] = list()
    metrics_dict['f1'] = list()

    model = get_model(model_num)
    kfold = StratifiedKFold(n_splits=splits, shuffle=True, random_state=777)
    #if model_num == 3:
        #kfold = ShuffleSplit(n_splits=splits, test_size=0.2, random_state=0)
    
    plot_lc(model = model, cv = kfold, X = X, y = y, resample = resample)
    #linearity
    test_for_linearity(X, y)

    i = 0
    for train_index, test_index in kfold.split(X, y):
        #create train-test splits
        X_train, y_train = X.iloc[train_index], y.iloc[train_index]
        X_test, y_test = X.iloc[test_index], y.iloc[test_index]

        '''
        #create test set labels for the baseline if applicable
        if baseline == 0:
            y_test = y_test.replace(1,0)
        elif baseline == 1:
            y_test = y_test.replace(0,1)
        ''' 
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
        file = open(dir_name + str(i+1) +'/train_val_dist.csv', 'a')
        file.write(str(sorted(Counter(y_train).items())))
        file.write('\n')
        file.close()

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        if baseline == 0:
            y_pred = y_pred.replace(1,0)
        elif baseline == 1:
            y_pred = y_pred.replace(0,1)

        metrics = get_metrics(y_test, y_pred)
        for key, value in metrics.items():
            metrics_dict[key].append(value)

        #homoscedasticity
        test_for_homoscedasticity(X_train, y_train, X_test, y_test)

        #correlation
        correlation(data)

        if feature_importance == 1:
            if model_num == 1:
                feat_importances = pd.Series(model.feature_importances_, index=X.columns)
            elif model_num == 3:
                feat_importances = pd.Series(abs(svm.coef_[0]), index=X.columns)
            if model_num != 2:
                print('Feat. Imp.: ', feat_importances)
                feat_importances.nlargest(20).plot(kind='barh')
                #plot_importance(model)
                plt.show()

                #write the feature importance values to the file
                file = open(dir_name + str(i+1) + '/feature_importances.csv', 'a')
                for ind in range(0, len(feature_set)):
                    file.write(feature_set[ind] + ',' + str(feat_importances[ind]) + '\n')
                file.close()

            perm = PermutationImportance(model, random_state=1).fit(X_train, y_train)
            print('PERM: ', perm.feature_importances_)
            display(eli5.show_weights(perm, feature_names = X_train.columns.tolist()))

            #write the permutation feature importance decrease in error values to the file
            file = open(dir_name + str(i+1) + '/permutation_feature_importances.csv', 'a')
            for ind in range(0, len(feature_set)):
                file.write(feature_set[ind] + ',' + str(perm.feature_importances_[ind]) + '\n')
            file.write('\n')
            file.close()
        
        i += 1
    for key, values in metrics_dict.items():
        metrics_dict[key] = sum(values)/len(values)

    #write the scores to the file
    json.dump(metrics_dict, metrics_file)
    metrics_file.close()

    #write the configuration values to the file
    json.dump(data_dict, config_file)
    config_file.close()

data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/Basic Binary Classification/DataForClassification.csv')
#print(data.iloc[:, 1:-1].head())
del data['word']
print(data.columns)
print(data.groupby('label').mean()) #class means
#splits is 5 so that the test size is 1/5 = 20%
crossvalidate('run2', 5, data, data.iloc[:, :-1], data.label, model_num = 1, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = -1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 

# %%
