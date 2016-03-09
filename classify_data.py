import pandas
from sklearn import linear_model, cross_validation
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
import numpy

K_FOLDS = 10


def logistic_regression(X, Y):
    length = len(X)

    model = linear_model.LogisticRegression()

    # X = X.values.reshape(length, 1)
    # Y = Y.values.reshape(length, 1)

    predicted = cross_validation.cross_val_predict(model, X, Y, K_FOLDS, 1, 0, None, 0)
    scores = cross_validation.cross_val_score(model, X, Y, cv=K_FOLDS, scoring='mean_squared_error')

    print 'All RMSEs',  numpy.sqrt(-scores)
    print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
    print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))
    # print 'Coefficients', model.coef_


def random_forest(x, y):
    model = RandomForestRegressor(n_estimators=50,
                          max_features=1,
                          max_depth= 9,
                          n_jobs=1)
    predicted = cross_validation.cross_val_predict(model, x, y, 10, 1, 0, None, 0)
    scores = cross_validation.cross_val_score(model, x, y,  cv=10, scoring='mean_squared_error')

    print 'All RMSEs',  numpy.sqrt(-scores)
    print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
    print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))
    print 'Coefficients', model.feature_importances_


def svm(x, y):
    model = SVC()
    predicted = cross_validation.cross_val_predict(model, x, y, 10, 1, 0, None, 0)
    scores = cross_validation.cross_val_score(model, x, y,  cv=10, scoring='mean_squared_error')

    print 'All RMSEs',  numpy.sqrt(-scores)
    print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
    print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))
    print 'Coefficients', model.feature_importances_