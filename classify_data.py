import pandas as pd
from sklearn import linear_model, cross_validation, neural_network, grid_search
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.metrics import roc_curve,auc
import matplotlib.pyplot as plt
from scipy import interp
import numpy

K_FOLDS = 10


def logistic_regression():

    return linear_model.LogisticRegression(C=300)

    # OLD FUNCTION
    # scores = cross_validation.cross_val_score(model, X, Y, cv=K_FOLDS, scoring='mean_squared_error')
    # # predicted = cross_validation.cross_val_predict(model, X, Y, K_FOLDS, 1, 0, None, 0)
    # print 'All RMSEs',  numpy.sqrt(-scores)
    # print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
    # print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))
    #
    # # (X_train,X_test,Y_train,Y_test) = divideTrainData(0.9,X,Y)
    # # model.fit(X_train,Y_train)
    # # predicted = model.predict_proba(X_test)
    # # print predicted
    #
    # # print 'Coefficients', model.coef_
    #
    # # X_test['outcome']=predicted
    # # X_test['bidder_id','outcome'].to_csv('logistic.csv',index = False)
    # # submit = pd.DataFrame({'bidder_id':X_test_id.bidder_id.tolist()})
    # # submit['prediction'] = predicted
    # # submit = submit.drop_duplicates()
    # # submit.to_csv('logistic.csv',index=False)

def random_forest():
    return RandomForestClassifier(n_estimators=50)
    # predicted = cross_validation.cross_val_predict(model, x, y, 10, 1, 0, None, 0)
    # scores = cross_validation.cross_val_score(model, x, y,  cv=10, scoring='mean_squared_error')
    # predicted = cross_validation.cross_val_predict(model, x, y, 10, 1, 0, None, 0)

    # print 'All RMSEs',  numpy.sqrt(-scores)
    # print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
    # print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))
    #
    # (X_train,X_test,Y_train,Y_test) = divideTrainData(0.9,x,y)
    # model.fit(X_train,Y_train)
    # predicted = model.predict_proba(X_test)
    # print predicted
    # #print 'Coefficients', model.feature_importances_


def svm():
    return SVC(kernel='rbf',C=20,probability=True)
    # predicted = cross_validation.cross_val_predict(model, x, y, 10, 1, 0, None, 0)
    # scores = cross_validation.cross_val_score(model, x, y,  cv=10, scoring='mean_squared_error')
    #
    # print 'All RMSEs',  numpy.sqrt(-scores)
    # print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
    # print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))
    # #print 'Coefficients', model.feature_importances_

def gradient_boosting():
    return GradientBoostingClassifier(n_estimators=50)

def classify(X,Y,model_type,X_test,X_test_id):
    if(model_type == "logistic"):
        model = logistic_regression()
    if(model_type == "svm"):
        model = svm()
    if(model_type == "rf"):
        model = random_forest()
    if(model_type == "gboost"):
        model = gradient_boosting()
    cv = cross_validation.StratifiedKFold(Y, n_folds=K_FOLDS)
    # print len(Y)
    mean_tpr = 0.0
    mean_fpr = numpy.linspace(0, 1, 100)
    all_tpr = []

    for i, (train, test) in enumerate(cv):
        probas_ = model.fit(X.values[train], Y.values[train]).predict_proba(X.values[test])
        # Compute ROC curve and area the curve
        fpr, tpr, thresholds = roc_curve(Y.values[test], probas_[:, 1])
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))

    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

    mean_tpr /= len(cv)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'k--', label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example: '+model_type)
    plt.legend(loc="lower right")
    plt.show()
    print "Plot done"
    model.fit(X,Y)
    predicted = model.predict_proba(X_test)
    print predicted
    submit = pd.DataFrame({'bidder_id':X_test_id.bidder_id.tolist()})
    submit['prediction'] = predicted[:,1]
    submit = submit.drop_duplicates()
    filename = "submission_"+model_type+".csv"
    submit.to_csv(filename,index=False)
    print "submit file written"
    print 'All RMSEs',  numpy.sqrt(-scores)
    print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
    print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))
    print 'Coefficients', model.feature_importances_


def neural_networks(x, y):
    model = neural_network.MLPRegressor([1,1,1,1,1], 'relu', 'adam', 0.0001, 200, 'constant', 0.001, 0.5, 200,
                                        True, None, 0.0001, False, False, 0.9, True, False, 0.1, 0.9, 0.999, 1e-08)
    predicted = cross_validation.cross_val_predict(model, x, y, 10, 1, 0, None, 0)
    scores = cross_validation.cross_val_score(model, x, y,  cv=10, scoring='mean_squared_error')

    print 'All RMSEs',  numpy.sqrt(-scores)
    print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
    print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))
    print 'Coefficients', model.get_params(True)


def grid_logistic(X, Y):
    model = linear_model.LogisticRegression(n_jobs=7)
    parameters = {'C': [i for i in range(50, 500, 50)]}
    clf = grid_search.GridSearchCV(model, parameters)
    clf.fit(X, Y)
    print clf.grid_scores_


