from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.model_selection import KFold
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import f_regression
from matplotlib import pyplot
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import numpy as np
import pandas as pd
import csv
import seaborn as sns


cv = KFold(n_splits=10)

class Classifier:
    #1: logit
    classifier_type = 0
    def __init__(self, classifier_type):
        if classifier_type == 1:
            self.model = LinearRegression()
        elif classifier_type == 2:
            self.model = svm.SVC(kernel='linear', C = 1.0)
        elif classifier_type == 3:
            self.model = ExtraTreesClassifier()
        elif classifier_type == 4:
            self.classifier_type = 4
        elif classifier_type == 5:
            self.classifier_type = 5
	    

    def cv(self, splits, X, y, average_method):
        kfold = KFold(n_splits=splits, shuffle=True, random_state=777)
        accuracy = []
        precision = []
        recall = []
        f1 = []
        for train_index, test_index in kfold.split(X, y):
            X_train, y_train = X.iloc[train_index], y.iloc[train_index]
            X_test, y_test = X.iloc[test_index], y.iloc[test_index]
            #rus = RandomUnderSampler(random_state = 42)
            #X_train, y_train = rus.fit_resample(X_train, y_train)
            #smote = SMOTE()
            #X_train, y_train = smote.fit_sample(X_train, y_train) #balance the training dataset
            if self.classifier_type <4:
                self.model.fit(X_train, y_train)
                #feat_importances = pd.Series(self.model.feature_importances_, index=X_train.columns)
                #print(feat_importances)
                #feat_importances.nlargest(10).plot(kind='barh')
                #pyplot.show()
                
                y_pred = self.model.predict(X_test)
                scores = self.model.score(X_test, y_test)
                print(scores)
                #accuracy.append(scores * 100)
                #precision.append(precision_score(y_test, y_pred, average=average_method)*100)
                #print('              negative    positive')
                #print('precision:',precision_score(y_test, y_pred))
                #recall.append(recall_score(y_test, y_pred, average=average_method)*100)
                #print('recall:   ',recall_score(y_test, y_pred))
                #f1.append(f1_score(y_test, y_pred, average=average_method)*100)
                #print('f1 score: ',f1_score(y_test, y_pred))
                
            elif self.classifier_type == 5:
                #pyplot.figure(figsize=(8,5))
                #pyplot.plot(X_train['frequency'], y_train, 'ro')
                
                df = pd.concat([X_train, y_train], axis = 1)
                print(df.head())
                corrmat = df.corr()
                top_corr_features = corrmat.index
                pyplot.figure(figsize=(20,20))
                #plot heat map
                sns.heatmap(df[top_corr_features].corr(),annot=True,cmap="RdYlGn")
                
                pyplot.show()
            elif self.classifier_type == 4:
                mut_info_score = mutual_info_classif(X_train,y_train)
                print(X_train.columns, mut_info_score)
            
        '''    
        print("accuracy: %.2f%% (+/- %.2f%%)" % (np.mean(accuracy), np.std(accuracy)))
        print("precision: %.2f%% (+/- %.2f%%)" % (np.mean(precision), np.std(precision)))
        print("recall: %.2f%% (+/- %.2f%%)" % (np.mean(recall), np.std(recall)))
        print("f1 score: %.2f%% (+/- %.2f%%)" % (np.mean(f1), np.std(f1)))
	'''
clf = Classifier(1)
data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/DataForRegression.csv')
#print(data.iloc[:, 1:-1].head())
del data['word']
del data['label']
print(data.columns)
clf.cv(10, data.iloc[:, :-1], data.label_avg_rank, 'macro')
