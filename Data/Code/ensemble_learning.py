# %%
import os
import json
import pandas as pd
import numpy as np
import eli5
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import learning_curve
from imblearn.under_sampling import NearMiss
from imblearn.over_sampling import SMOTE
from eli5.sklearn import PermutationImportance
#from xgboost import plot_importance
from collections import Counter
import matplotlib.pyplot as plt
from IPython.display import display

from data_tests import *
from models import get_model
from evaluation import get_metrics
from evaluation import plot_lc

def ensemble_learning(directory_name, data, X, y, baseline = -1, model_num = None, resample = 0, feature_set = None, feature_importance = 0, average_method='macro', path= None):
    """
    Store the results calculated according to the arguments and store them in a file.
    Arguments:
    directory_name (str): the directory under which the files should be stored
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
   
    #prepare the dictionary to be written to the file
    data_dict = dict()
    metrics_dict = dict()

    dir_name = path + directory_name + '/'
    os.mkdir(dir_name)
    
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
        print(sorted(Counter(y_train).items()))
        X_resampled, y_resampled = nm.fit_resample(X_train, y_train)
        X_train = X_resampled
        y_train = y_resampled
        print(str(sorted(Counter(y_train).items())))
    elif resample == 1:
        #oversample
        X_resampled, y_resampled = SMOTE().fit_resample(X_train, y_train)
        X_train = X_resampled
        y_train = y_resampled
        print(sorted(Counter(y_resampled).items()))
    #write the training dataset class distribution to the file
    file = open(dir_name + 'train_val_dist.csv', 'a')
    file.write(str(sorted(Counter(y_train).items())))
    file.write('\n')
    file.close()

    model = get_model(model_num)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    if baseline == 0:
        y_pred = y_pred.replace(1,0)
    elif baseline == 1:
        y_pred = y_pred.replace(0,1)

    plot_lc(model = model, cv = StratifiedKFold(n_splits = 5, shuffle=True, random_state=777), X = X, y = y)

    #evaluation
    metrics = get_metrics(y_test, y_pred)
    for key, value in metrics.items():
        metrics_dict[key] = value

    #correlation
    correlation(data)

    #linearity
    test_for_linearity(X_train, y_train)

    #homoscedasticity
    test_for_homoscedasticity(X_train, y_train, X_test, y_test)

    '''
    #learning curve
    #if model_num == 7:
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    #else:
    #cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=777)
    train_sizes, train_scores, test_scores = learning_curve(estimator = model, X = data[feature_set], y = data['label'], cv = cv, scoring = 'f1_macro', train_sizes=np.linspace(.1, 1.0, 10))
    # Create means and standard deviations of training set scores
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    print('scores: ', train_scores, train_mean)
    # Create means and standard deviations of test set scores
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    # Draw lines
    print('Learning Curve')
    plt.plot(train_sizes, train_mean, '--', color="#111111",  label="Training score")
    plt.plot(train_sizes, test_mean, color="#111111", label="Cross-validation score")
    # Draw bands
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="#DDDDDD")
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#DDDDDD")

    # Create plot
    plt.title("Learning Curve")
    plt.xlabel("Training Set Size"), plt.ylabel("Macro-F1 Score"), plt.legend(loc="best")
    plt.tight_layout()
    plt.show()
    '''
    plot_learning_curves(X_train, y_train, X_test, y_test, model, scoring = 'f1_macro')
    plt.show()

    if feature_importance == 1:
        feat_importances = pd.Series(model.feature_importances_, index=feature_set)
        print(feature_set)
        print('Feat: ', feat_importances)
        feat_importances.nlargest(20).plot(kind = 'barh')
        #plot_importance(model)
        plt.show()

        perm = PermutationImportance(model, random_state = 1).fit(X_train, y_train)
        display(eli5.show_weights(perm, feature_names = X_train.columns.tolist()))
        
        #write the training dataset class distribution to the file
        file = open(dir_name + 'feature_importances.csv', 'a')
        for ind in range(0, len(feature_set)):
            file.write(feature_set[ind] + ',' + str(feat_importances[ind]) + '\n')
        file.close()

        #write the permutation feature importance decrease in error values to the file
        file = open(dir_name + 'permutation_feature_importances.csv', 'a')
        print(perm.feature_importances_)
        for ind in range(0, len(feature_set)):
            file.write(feature_set[ind] + ',' + str(perm.feature_importances_[ind]) + '\n')
        file.close()


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
ensemble_learning('ensemble4', data, data.iloc[:, :-1], data.label, baseline = -1, model_num = 4, feature_set = list((data.iloc[:, :-1]).columns), feature_importance=1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/')


# %%
