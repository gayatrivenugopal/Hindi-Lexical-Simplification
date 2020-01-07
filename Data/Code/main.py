from crossvalidate import *
from ensemble_learning import *
from models import *

'''
Cases

A. BinaryClassificationAnnotators
Baseline 0 Model 1 1 feature undersample oversample
Baseline 0 Model 1 2 features undersample oversample
Baseline 0 Model 1 3 features undersample oversample
Baseline 0 Model 1 4 features undersample oversample
Baseline 0 Model 1 5 features undersample oversample
Baseline 0 Model 1 6 features undersample oversample
Baseline 0 Model 1 7 features undersample oversample
Baseline 0 Model 1 8 features undersample oversample
Baseline 0 Model 1 9 features undersample oversample
Baseline 0 Model 2 1 feature undersample oversample
Baseline 0 Model 2 2 features undersample oversample
Baseline 0 Model 2 3 features undersample oversample
Baseline 0 Model 2 4 features undersample oversample
Baseline 0 Model 2 5 features undersample oversample
Baseline 0 Model 2 6 features undersample oversample
Baseline 0 Model 2 7 features undersample oversample
Baseline 0 Model 2 8 features undersample oversample
Baseline 0 Model 2 9 features undersample oversample
Baseline 0 Model 3 1 feature undersample oversample
Baseline 0 Model 3 2 features undersample oversample
Baseline 0 Model 3 3 features undersample oversample
Baseline 0 Model 3 4 features undersample oversample
Baseline 0 Model 3 5 features undersample oversample
Baseline 0 Model 3 6 features undersample oversample
Baseline 0 Model 3 7 features undersample oversample
Baseline 0 Model 3 8 features undersample oversample
Baseline 0 Model 3 9 features undersample oversample
Baseline 0 Model 4 1 feature undersample oversample
Baseline 0 Model 4 2 features undersample oversample
Baseline 0 Model 4 3 features undersample oversample
Baseline 0 Model 4 4 features undersample oversample
Baseline 0 Model 4 5 features undersample oversample
Baseline 0 Model 4 6 features undersample oversample
Baseline 0 Model 4 7 features undersample oversample
Baseline 0 Model 4 8 features undersample oversample
Baseline 0 Model 4 9 features undersample oversample
Baseline 0 Model 5 1 feature undersample oversample
Baseline 0 Model 5 2 features undersample oversample
Baseline 0 Model 5 3 features undersample oversample
Baseline 0 Model 5 4 features undersample oversample
Baseline 0 Model 5 5 features undersample oversample
Baseline 0 Model 5 6 features undersample oversample
Baseline 0 Model 5 7 features undersample oversample
Baseline 0 Model 5 8 features undersample oversample
Baseline 0 Model 5 9 features undersample oversample
Baseline 0 Model 6 1 feature undersample oversample
Baseline 0 Model 6 2 features undersample oversample
Baseline 0 Model 6 3 features undersample oversample
Baseline 0 Model 6 4 features undersample oversample
Baseline 0 Model 6 5 features undersample oversample
Baseline 0 Model 6 6 features undersample oversample
Baseline 0 Model 6 7 features undersample oversample
Baseline 0 Model 6 8 features undersample oversample
Baseline 0 Model 6 9 features undersample oversample
Baseline 0 Model 7 1 feature undersample oversample
Baseline 0 Model 7 2 features undersample oversample
Baseline 0 Model 7 3 features undersample oversample
Baseline 0 Model 7 4 features undersample oversample
Baseline 0 Model 7 5 features undersample oversample
Baseline 0 Model 7 6 features undersample oversample
Baseline 0 Model 7 7 features undersample oversample
Baseline 0 Model 7 8 features undersample oversample
Baseline 0 Model 7 9 features undersample oversample
Baseline 0 Model 8 1 feature undersample oversample
Baseline 0 Model 8 2 features undersample oversample
Baseline 0 Model 8 3 features undersample oversample
Baseline 0 Model 8 4 features undersample oversample
Baseline 0 Model 8 5 features undersample oversample
Baseline 0 Model 8 6 features undersample oversample
Baseline 0 Model 8 7 features undersample oversample
Baseline 0 Model 8 8 features undersample oversample
Baseline 0 Model 8 9 features undersample oversample
(b) Baseline 1
Baseline 1 Model 1 1 feature undersample oversample
Baseline 1 Model 1 2 features undersample oversample
Baseline 1 Model 1 3 features undersample oversample
Baseline 1 Model 1 4 features undersample oversample
Baseline 1 Model 1 5 features undersample oversample
Baseline 1 Model 1 6 features undersample oversample
Baseline 1 Model 1 7 features undersample oversample
Baseline 1 Model 1 8 features undersample oversample
Baseline 1 Model 1 9 features undersample oversample
Baseline 1 Model 2 1 feature undersample oversample
Baseline 1 Model 2 2 features undersample oversample
Baseline 1 Model 2 3 features undersample oversample
Baseline 1 Model 2 4 features undersample oversample
Baseline 1 Model 2 5 features undersample oversample
Baseline 1 Model 2 6 features undersample oversample
Baseline 1 Model 2 7 features undersample oversample
Baseline 1 Model 2 8 features undersample oversample
Baseline 1 Model 2 9 features undersample oversample
Baseline 1 Model 3 1 feature undersample oversample
Baseline 1 Model 3 2 features undersample oversample
Baseline 1 Model 3 3 features undersample oversample
Baseline 1 Model 3 4 features undersample oversample
Baseline 1 Model 3 5 features undersample oversample
Baseline 1 Model 3 6 features undersample oversample
Baseline 1 Model 3 7 features undersample oversample
Baseline 1 Model 3 8 features undersample oversample
Baseline 1 Model 3 9 features undersample oversample
Baseline 1 Model 4 1 feature undersample oversample
Baseline 1 Model 4 2 features undersample oversample
Baseline 1 Model 4 3 features undersample oversample
Baseline 1 Model 4 4 features undersample oversample
Baseline 1 Model 4 5 features undersample oversample
Baseline 1 Model 4 6 features undersample oversample
Baseline 1 Model 4 7 features undersample oversample
Baseline 1 Model 4 8 features undersample oversample
Baseline 1 Model 4 9 features undersample oversample
Baseline 1 Model 5 1 feature undersample oversample
Baseline 1 Model 5 2 features undersample oversample
Baseline 1 Model 5 3 features undersample oversample
Baseline 1 Model 5 4 features undersample oversample
Baseline 1 Model 5 5 features undersample oversample
Baseline 1 Model 5 6 features undersample oversample
Baseline 1 Model 5 7 features undersample oversample
Baseline 1 Model 5 8 features undersample oversample
Baseline 1 Model 5 9 features undersample oversample
Baseline 1 Model 6 1 feature undersample oversample
Baseline 1 Model 6 2 features undersample oversample
Baseline 1 Model 6 3 features undersample oversample
Baseline 1 Model 6 4 features undersample oversample
Baseline 1 Model 6 5 features undersample oversample
Baseline 1 Model 6 6 features undersample oversample
Baseline 1 Model 6 7 features undersample oversample
Baseline 1 Model 6 8 features undersample oversample
Baseline 1 Model 6 9 features undersample oversample
Baseline 1 Model 7 1 feature undersample oversample
Baseline 1 Model 7 2 features undersample oversample
Baseline 1 Model 7 3 features undersample oversample
Baseline 1 Model 7 4 features undersample oversample
Baseline 1 Model 7 5 features undersample oversample
Baseline 1 Model 7 6 features undersample oversample
Baseline 1 Model 7 7 features undersample oversample
Baseline 1 Model 7 8 features undersample oversample
Baseline 1 Model 7 9 features undersample oversample
Baseline 1 Model 8 1 feature undersample oversample
Baseline 1 Model 8 2 features undersample oversample
Baseline 1 Model 8 3 features undersample oversample
Baseline 1 Model 8 4 features undersample oversample
Baseline 1 Model 8 5 features undersample oversample
Baseline 1 Model 8 6 features undersample oversample
Baseline 1 Model 8 7 features undersample oversample
Baseline 1 Model 8 8 features undersample oversample
Baseline 1 Model 8 9 features undersample oversample

Do the same with test data, compare the metrics with the corresponding baseline, choose the one with the
maximum difference from the baseline - doesn't make sense

OR
'''
data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/Basic Binary Classification/train.csv')
#data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/RankedClassification/train.csv')
#print(data.iloc[:, 1:-1].head())
del data['word']
#a. Baseline 1 and 0 for each model with all 9 features together undersample and oversample
crossvalidate('b1under', 5, data, data.iloc[:, :-1], data.label, model_num = 1, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/')
#crossvalidate('b1over', 5, data, data.iloc[:, :-1], data.label, model_num = 1, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1under', 5, data, data.iloc[:, :-1], data.label, model_num = 4, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m4over', 5, data, data.iloc[:, :-1], data.label, model_num = 4, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b0under', 5, data, data.iloc[:, :-1], data.label, model_num = 1, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b0over', 5, data, data.iloc[:, :-1], data.label, model_num = 1, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0under', 5, data, data.iloc[:, :-1], data.label, model_num = 4, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0over', 5, data, data.iloc[:, :-1], data.label, model_num = 4, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 

#crossvalidate('b1m2under', 5, data, data.iloc[:, :-1], data.label, model_num = 2, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b1m3under', 5, data, data.iloc[:, :-1], data.label, model_num = 3, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m5under', 5, data, data.iloc[:, :-1], data.label, model_num = 5, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m6under', 5, data, data.iloc[:, :-1], data.label, model_num = 6, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m7under', 5, data, data.iloc[:, :-1], data.label, model_num = 7, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m8under', 5, data, data.iloc[:, :-1], data.label, model_num = 8, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b1m2over', 5, data, data.iloc[:, :-1], data.label, model_num = 2, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b1m3over' 5, data, data.iloc[:, :-1], data.label, model_num = 3, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m4over', 5, data, data.iloc[:, :-1], data.label, model_num = 4, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m5over', 5, data, data.iloc[:, :-1], data.label, model_num = 5, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m6over', 5, data, data.iloc[:, :-1], data.label, model_num = 6, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m7over', 5, data, data.iloc[:, :-1], data.label, model_num = 7, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b1m8over', 5, data, data.iloc[:, :-1], data.label, model_num = 8, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 1, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b0m1under', 5, data, data.iloc[:, :-1], data.label, model_num = 1, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b0m2under', 5, data, data.iloc[:, :-1], data.label, model_num = 2, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b0m3under', 5, data, data.iloc[:, :-1], data.label, model_num = 3, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m4under', 5, data, data.iloc[:, :-1], data.label, model_num = 4, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m5under', 5, data, data.iloc[:, :-1], data.label, model_num = 5, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m6under', 5, data, data.iloc[:, :-1], data.label, model_num = 6, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m7under', 5, data, data.iloc[:, :-1], data.label, model_num = 7, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m8under', 5, data, data.iloc[:, :-1], data.label, model_num = 8, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = -1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b0m1over', 5, data, data.iloc[:, :-1], data.label, model_num = 1, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b0m2over', 5, data, data.iloc[:, :-1], data.label, model_num = 2, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#crossvalidate('b0m3over', 5, data, data.iloc[:, :-1], data.label, model_num = 3, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m4over', 5, data, data.iloc[:, :-1], data.label, model_num = 4, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m5over', 5, data, data.iloc[:, :-1], data.label, model_num = 5, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m6over', 5, data, data.iloc[:, :-1], data.label, model_num = 6, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m7over', 5, data, data.iloc[:, :-1], data.label, model_num = 7, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 
#ensemble_learning('b0m8over', 5, data, data.iloc[:, :-1], data.label, model_num = 8, feature_set = list((data.iloc[:, :-1]).columns), feature_importance = 1, baseline = 0, resample = 1, path = '/opt/PhD/Work/JHWNL_1_2/Data/Analysis/') 


'''
b. 
Test data Model 1 1 feature undersample oversample
Test data Model 1 2 features undersample oversample
Test data Model 1 3 features undersample oversample
Test data Model 1 4 features undersample oversample
Test data Model 1 5 features undersample oversample
Test data Model 1 6 features undersample oversample
Test data Model 1 7 features undersample oversample
Test data Model 1 8 features undersample oversample
Test data Model 1 9 features undersample oversample
Test data Model 2 1 feature undersample oversample
Test data Model 2 2 features undersample oversample
Test data Model 2 3 features undersample oversample
Test data Model 2 4 features undersample oversample
Test data Model 2 5 features undersample oversample
Test data Model 2 6 features undersample oversample
Test data Model 2 7 features undersample oversample
Test data Model 2 8 features undersample oversample
Test data Model 2 9 features undersample oversample
Test data Model 3 1 feature undersample oversample
Test data Model 3 2 features undersample oversample
Test data Model 3 3 features undersample oversample
Test data Model 3 4 features undersample oversample
Test data Model 3 5 features undersample oversample
Test data Model 3 6 features undersample oversample
Test data Model 3 7 features undersample oversample
Test data Model 3 8 features undersample oversample
Test data Model 3 9 features undersample oversample
Test data Model 4 1 feature undersample oversample
Test data Model 4 2 features undersample oversample
Test data Model 4 3 features undersample oversample
Test data Model 4 4 features undersample oversample
Test data Model 4 5 features undersample oversample
Test data Model 4 6 features undersample oversample
Test data Model 4 7 features undersample oversample
Test data Model 4 8 features undersample oversample
Test data Model 4 9 features undersample oversample
Test data Model 4 1 feature undersample oversample
Test data Model 5 2 features undersample oversample
Test data Model 5 3 features undersample oversample
Test data Model 5 4 features undersample oversample
Test data Model 5 5 features undersample oversample
Test data Model 5 6 features undersample oversample
Test data Model 5 7 features undersample oversample
Test data Model 5 8 features undersample oversample
Test data Model 5 9 features undersample oversample
Test data Model 6 1 feature undersample oversample
Test data Model 6 2 features undersample oversample
Test data Model 6 3 features undersample oversample
Test data Model 6 4 features undersample oversample
Test data Model 6 5 features undersample oversample
Test data Model 6 6 features undersample oversample
Test data Model 6 7 features undersample oversample
Test data Model 6 8 features undersample oversample
Test data Model 6 9 features undersample oversample
Test data Model 7 1 feature undersample oversample
Test data Model 7 2 features undersample oversample
Test data Model 7 3 features undersample oversample
Test data Model 7 4 features undersample oversample
Test data Model 7 5 features undersample oversample
Test data Model 7 6 features undersample oversample
Test data Model 7 7 features undersample oversample
Test data Model 7 8 features undersample oversample
Test data Model 7 9 features undersample oversample
Test data Model 8 1 feature undersample oversample
Test data Model 8 2 features undersample oversample
Test data Model 8 3 features undersample oversample
Test data Model 8 4 features undersample oversample
Test data Model 8 5 features undersample oversample
Test data Model 8 6 features undersample oversample
Test data Model 8 7 features undersample oversample
Test data Model 8 8 features undersample oversample
Test data Model 8 9 features undersample oversample

Choose the model with the maximum deviation from the baseline score (metrics and learning curve).

AND

c. Use test data, all models, all features together, undersample and oversample, perm_feature importance and correlation - check if there is any similarity - for the readability formula paper



B. Same as above except for resampling - resampling should be 0.