#ensemble learning

#random forest - bagging, majority vote
#adaptive boosting - boosting, learns by increasing the weight of misclassified data points,
#prediction - weighted majority vote for each candidate in the test set
#gradient boosting - boosting, learns from residual error,
#prediction - adds the predictions

#unsure about logistic regression assumptions
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import NearestCentroid
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier, ExtraTreesClassifier
import xgboost as xgb

def get_model(model_num):
    """
    Return the model based on the model number.
    Argument:
    model_num (int)
    """
    if model_num == 1:
        return DecisionTreeClassifier()
    elif model_num == 2:
        return NearestCentroid()
    elif model_num==3:
        return svm.SVC()
    elif model_num == 4:
        return RandomForestClassifier(n_estimators=100, max_features="auto",random_state=0)
    elif model_num == 5:
        return ExtraTreesClassifier(n_estimators=100, max_features="auto",random_state=0)
    elif model_num == 6:
        return AdaBoostClassifier(n_estimators=100)
    elif model_num == 7:
        return GradientBoostingClassifier(n_estimators=100)
    elif model_num == 8:
        return xgb.XGBClassifier(random_state=1,learning_rate=0.01)