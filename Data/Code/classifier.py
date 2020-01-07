from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.model_selection import StratifiedKFold
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import mutual_info_classif
from xgboost import XGBClassifier
from xgboost import plot_importance
from matplotlib import pyplot
from sklearn.calibration import calibration_curve
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import brier_score_loss
from sklearn.metrics import roc_auc_score
import numpy as np
import pandas as pd
import csv
import seaborn as sns


cv = StratifiedKFold(n_splits=10)

class Classifier:
    #1: logit
    classifier_type = 0
    def __init__(self, classifier_type):
        if classifier_type == 0:
            self.model = LogisticRegression()
            self.classifier_type = 0
        elif classifier_type == 1:
            self.model = svm.SVC(kernel='linear', C = 1.0)
            self.classifier_type = 1
        elif classifier_type == 2:
            self.model = ExtraTreesClassifier()
            self.classifier_type = 2
        elif classifier_type == 3:
            self.model = XGBClassifier()
            self.classifier_type = 3
        elif classifier_type == 4:
            self.classifier_type = 4
        elif classifier_type == 5:
            self.classifier_type = 5
	    

    def cv(self, splits, X, y, average_method):
        kfold = StratifiedKFold(n_splits=splits, shuffle=True, random_state=777)
        accuracy = []
        precision = []
        recall = []
        f1 = []
        for train_index, test_index in kfold.split(X, y):
            X_train, y_train = X.iloc[train_index], y.iloc[train_index]
            X_test, y_test = X.iloc[test_index], y.iloc[test_index]
            rus = RandomUnderSampler(random_state = 42)
            X_train, y_train = rus.fit_resample(X_train, y_train)
            #smote = SMOTE()
            #X_train, y_train = smote.fit_sample(X_train, y_train) #balance the training dataset
            if self.classifier_type == 2 or self.classifier_type == 3:
                print('here')
                self.model.fit(X_train, y_train)
                feat_importances = pd.Series(self.model.feature_importances_, index=X_train.columns)
                #print(feat_importances)
                feat_importances.nlargest(10).plot(kind='barh')
                pyplot.show()
                
                y_pred = self.model.predict(X_test)
                scores = self.model.score(X_test, y_test)
                accuracy.append(scores * 100)
                precision.append(precision_score(y_test, y_pred, average=average_method)*100)
                print('accuracy: ', scores*100)
                print('precision:',precision_score(y_test, y_pred))
                recall.append(recall_score(y_test, y_pred, average=average_method)*100)
                print('recall:   ',recall_score(y_test, y_pred))
                f1.append(f1_score(y_test, y_pred, average=average_method)*100)
                print('f1 score: ',f1_score(y_test, y_pred))
                
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
            #probs_uncalibrated = self.model.predict_proba(X_test)[:,1]
            # reliability diagram
            #fop_uncalibrated, mpv_uncalibrated = calibration_curve(y_test.values, probs_uncalibrated, n_bins=10, normalize = True)
           
            #calibrated = CalibratedClassifierCV(self.model, method='sigmoid', cv=5)
            #calibrated.fit(X_train, y_train)
            #predictions = calibrated.predict(X_test)
            #probs_calibrated = calibrated.predict_proba(X_test)[:,1]
            # reliability diagram
            #fop_calibrated, mpv_calibrated = calibration_curve(y_test.values, probs_calibrated, n_bins=10)
            # plot perfectly calibrated
            #pyplot.plot([0, 1], [0, 1], linestyle='--', color='black')
            # plot model reliabilities
            #pyplot.plot(mpv_uncalibrated, fop_uncalibrated, marker='.')
            #pyplot.plot(mpv_calibrated, fop_calibrated, marker='.')
	    #fpr, tpr, thresholds = roc_curve(y_test, probs)
	    # plot no skill
	    #pyplot.plot([0, 1], [0, 1], linestyle='--')
	    # plot the roc curve for the model
	    #pyplot.plot(fpr, tpr)
	    # show the plot
	    #pyplot.show()
	    #print(type(y_test), y_test.values)
	    #loss = roc_auc_score(y_test.values, probs[:,1])
	    #print(loss)
	    # plot predictions vs loss
	    #pd.DataFrame(y_test.values).hist()
	    #blue is uncalibrated, orange is calibrated
            #pyplot.show()        
            
	    #probs = self.model.predict_proba(X_test)
            #print('1: ', probs[:, 1])
            #print('Score 1: ', brier_score_loss(y_test.values, probs_calibrated[:, 1]))
            #print('0: ', probs[:, 0])
            #print('Score 0: ', brier_score_loss(y_test.values, probs_calibrated[:, 0]))
        '''
        print("accuracy: %.2f%% (+/- %.2f%%)" % (np.mean(accuracy), np.std(accuracy)))
        print("precision: %.2f%% (+/- %.2f%%)" % (np.mean(precision), np.std(precision)))
        print("recall: %.2f%% (+/- %.2f%%)" % (np.mean(recall), np.std(recall)))
        print("f1 score: %.2f%% (+/- %.2f%%)" % (np.mean(f1), np.std(f1)))
	'''
clf = Classifier(3)
#data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/RankedClassification/DataForRankedClassificationFeatureSubset.csv')
data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/Basic Binary Classification/DataForClassification.csv')
#print(data.iloc[:, 1:-1].head())
del data['word']
del data['label_avg_rank']
print(data.columns)
clf.cv(10, data.iloc[:, :-1], data.label, 'macro')
