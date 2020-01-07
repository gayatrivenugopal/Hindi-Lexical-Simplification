from sklearn.model_selection import learning_curve
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import NearMiss
from imblearn.over_sampling import SMOTE
import numpy as np
import matplotlib.pyplot as plt

'''
AUC
F1
Macro-F1 - harmonic mean of average P and average R
Learning Curve - important
'''
#Source: https://www.researchgate.net/post/Which_one_is_better_regarding_a_classification_problem_with_four_classes_Single_model_capable_of_nonlinear_classification_or_3_one-versus-rest_SVMs

def find_TP(y_true, y_pred, label):
    # counts the number of true positives (y_true = 1, y_pred = 1)
    return sum((y_true == label) & (y_pred == label))

def find_FN(y_true, y_pred, label):
    # counts the number of false negatives (y_true = 1, y_pred = 0)
    return sum((y_true == label) & (y_pred != label))

def find_FP(y_true, y_pred, label):
    # counts the number of false positives (y_true = 0, y_pred = 1)
    return sum((y_true != label) & (y_pred == label))

def find_TN(y_true, y_pred, label):
    # counts the number of true negatives (y_true = 0, y_pred = 0)
    return sum((y_true != label) & (y_pred != label))

def get_metrics(y_true, y_pred):
    """
    Return Accuracy, TP, TN, FP, FN, Sensitivity/TPR, Specificity/FPR, AUC, Precision, Recall, F1, Learning Curve - important.
    Arguments:
    y_test (dataframe): the target in the test dataset 
    y_pred (dataframe): the predicted labels
    """
    tn = fp = fn = tp = accuracy = tpr = tnr = fpr = precision  = recall = f1 = f1_macro = []
    i = 0
    while i <= 1:
        print('here')
        tn.append(find_TN(y_true, y_pred, i))
        print('tn: ', tn)
        fp.append(find_FP(y_true, y_pred, i))
        print('fp: ', fp)
        fn.append(find_FN(y_true, y_pred, i))
        print('fn: ', fn)
        tp.append(find_TP(y_true, y_pred, i))
        print('tp: ', tp)
        accuracy.append((tp[i] + tn[i])/(tp[i] + tn[i] + fp[i] + fn[i]))
        tpr.append(tp[i]/(fn[i] + tp[i]))
        tnr.append(tn[i]/(tn[i] + fp[i]))
        fpr.append(fp[i]/(fp[i] + tn[i]))
        precision.append(tp[i]/(tp[i] + fp[i]))
        recall.append(tp[i]/(tp[i] + fn[i]))
        f1.append((2*precision[i]*recall[i])/(precision[i] + recall[i]))
        i += 1
    f1_macro = (2 * ((precision[0] + precision[1])/2) * ((recall[0] + recall[1])/2))/(precision[0] + precision[1] + recall[0] + recall[1])
    return {'f1_macro': f1_macro, 'f1': f1[1], 'tpr': tpr[1], 'tnr': tnr[1], 'fpr': fpr[1], 'precision': precision[1], 'recall': recall[1], 'accuracy': accuracy[1]}

def plot_lc(model, X, y, cv, resample = 0):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    #resample the training set (if applicable)
    if resample == -1:
        #undersample
        '''NearMiss 3 . NearMiss-3 is a 2-step algorithm: first, for each minority sample, 
        their :m nearest-neighbors will be kept; then, the majority samples selected are the 
        on for which the average distance to the k nearest neighbors is the largest.'''
        nm = NearMiss(version=3)
        #print(str(sorted(Counter(y_train).items())))
        X_resampled, y_resampled = nm.fit_resample(X_train, y_train)
        X_train = X_resampled
        y_train = y_resampled
        #print(sorted(Counter(y_train).items()))
    elif resample == 1:
        #oversample
        X_resampled, y_resampled = SMOTE().fit_resample(X_train, y_train)
        X_train = X_resampled
        y_train = y_resampled
        print(sorted(Counter(y_resampled).items()))
    train_sizes, train_scores, test_scores = learning_curve(estimator = model, X = X, y = y, train_sizes = np.linspace(0.01, 1.0, 50), cv = cv, scoring = 'f1_macro')

    # Create means and standard deviations of training set scores
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)

    # Create means and standard deviations of test set scores
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    # Draw lines
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