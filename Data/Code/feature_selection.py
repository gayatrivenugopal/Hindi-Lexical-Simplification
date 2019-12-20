import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import ExtraTreesClassifier
from xgboost import XGBClassifier
from xgboost import plot_importance
from matplotlib import pyplot

data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/DataForClassification.csv')

del data['n_avg_synonyms']
del data['n_avg_hyponyms']
del data['n_avg_hypernyms']
print(data.columns)
X = data.iloc[:,1:-1]  #independent columns
y = data.iloc[:,-1]    #target column i.e price range

'''
clf = ExtraTreesClassifier()
clf.fit(X, y)
feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
'''
'''
clf = XGBClassifier()
clf.fit(X, y)
#print(X.columns)
#print(clf.feature_importances_)

plot_importance(clf)
pyplot.show()
'''
'''
#apply SelectKBest class to extract top 10 best features
bestfeatures = SelectKBest(score_func=mutual_info_classif, k=10)
fit = bestfeatures.fit(X,y)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X.columns)
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']  #naming the dataframe columns
print(featureScores.nlargest(10,'Score'))  #print 10 best features
'''
'''
corrmat = data.corr(method = 'kendall')
top_corr_features = corrmat.index
pyplot.figure(figsize=(20,20))
#plot heat map
sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")
pyplot.show()
'''
mut_info_score = mutual_info_classif(X,y)
