from yellowbrick.regressor import ResidualsPlot
from sklearn.linear_model import LinearRegression
import scipy.stats as stats
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt

from data_tests import *

#correlation and collinearity
def correlation(data):
    """
    Display a heatmap of the correlation values.

    Arguments:
    data (dataframe): examples and target
    """

    corrmat = data.corr()
    top_corr_features = corrmat.index
    plt.figure(figsize=(20,20))
    #plot heat map
    sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")
    plt.show()

def test_for_linearity(X, y):
    """ Plot the data and check for linearity.
    Arguments:
    X (dataframe): examples
    y (dataframe): target/label
    """
    plt.style.use('seaborn-whitegrid')
    #scatter plot
    plt.plot(X, y, 'o', color='black')
    plt.title("Linear Relationship")
    plt.show()

def test_for_normality(X):
    """ Plot the data and check for normality.
    Arguments:
    X (Series): examples
    """
    #quantile-quantile plot - to compare two probability distributions
    stats.probplot(X[:,0], dist="norm", plot=plt)
    plt.show()

#homoscedasticity: the error term is the same across all values of the independent variables - for linear regression models
def test_for_homoscedasticity(X_train, y_train, X_test, y_test):
    """ Plot the data and check for homoscedasticity.
    Arguments:
    X_train (dataframe): examples in the training set
    X_test (dataframe): examples in the test set
    y_train (dataframe): target in the training set
    y_train (dataframe): target in the test set
    """
    lr = LinearRegression()
    visualizer = ResidualsPlot(lr)
    visualizer.fit(X_train, y_train)
    visualizer.score(X_test, y_test)
    #there should be no clear pattern
    visualizer.poof()
