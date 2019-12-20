from sklearn.metrics import accuracy_score

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
    tn = fp = fn = tp = accuracy = tpr = tnr = fpr = precision  = recall = f1 = f1_macro = {}
    for i in range(1,3):
        tn[i] = find_TN(y_true, y_pred, 1)
        fp[i] = find_FP(y_true, y_pred, 1)
        fn[i] = find_FN(y_true, y_pred, 1)
        tp[i] = find_TP(y_true, y_pred, 1)
        accuracy[i] = (tp[i] + tn[i])/(tp[i] + tn[i] + fp[i] + fn[i])
        tpr[i] = tp[i]/(fn[i] + tp[i])
        tnr[i] = tn[i]/(tn[i] + fp[i])
        fpr[i] = fp[i]/(fp[i] + tn[i])
        precision[i] = tp[i]/(tp[i] + fp[i])
        recall[i] = tp[i]/(tp[i] + fn[i])
        f1[i] = (2*precision[i]*recall[i])/(precision[i] + recall[i])
    f1_macro_f1 = (2 * ((precision[0] + precision[1])/2) * ((recall[0] + recall[1])/2))/(precision[0] + precision[1] + recall[0] + recall[1])