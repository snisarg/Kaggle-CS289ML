import pandas as pd
from sklearn import linear_model, cross_validation, neural_network, grid_search, tree, ensemble
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
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_random_forest(X, Y):
    model = RandomForestClassifier(random_state=7)
    parameters = {'n_estimators': [i for i in range(50, 1050, 50)],
                  'max_features': ['sqrt', 'log2', 'auto']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10, n_jobs=8)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_svm(X, Y):
    model = SVC(probability=True)
    parameters = {'C': [1, 10, 50, 100, 500, 1000],
                  'kernel': ['rbf']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10, n_jobs=8)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_nn(X, Y):
    model = model = neural_network.MLPClassifier(activation='relu', solver='lbgfs')
    parameters = {'hidden_layer_size': [[5, 15, 15, 5], [10, 30, 30, 10], [5, 15, 30, 30, 15, 5],
                                        [50, 100, 100, 100, 75, 50]]}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_

# Reg
def grid_lr(X, Y):
    model = linear_model.LogisticRegression(random_state=7)
    parameters = {'penalty': ['l1'],
                  'C': [i for i in range(10, 100, 10)],
                  'solver': ['liblinear']
                  }
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


# Reg
def grid_ridge(X, Y):
    model = linear_model.Ridge(random_state=7)
    parameters = {'alpha': [i * 0.1 for i in range(10)],
                  'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_

# Reg
def grid_bayesian(X, Y):
    model = linear_model.BayesianRidge()
    parameters = {'n_iter': [100, 200, 300, 400, 500, 600]}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_SGD(X, Y):
    model = linear_model.SGDClassifier(random_state=7)
    parameters = {'loss': ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron'],
                  'penalty': ['none', 'l2', 'l1', 'elasticnet']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_DT(X, Y):
    model = tree.DecisionTreeClassifier(random_state=7)
    parameters = {'criterion': ['gini', 'entropy'],
                  'max_features': ['auto', 'sqrt', 'log2']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_ada(X, Y):
    model = ensemble.AdaBoostClassifier(random_state=7)
    parameters = {'base_estimator': [tree.DecisionTreeClassifier()],
                  'n_estimators': [i for i in range(30, 80, 10)],
                  'algorithm': ['SAMME', 'SAMME.R']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print 'Options considered: {}'.format(clf.grid_scores_)
    print 'Best option: {}'.format(clf.best_params_)


def grid_grad_boost(X, Y):
    model = ensemble.GradientBoostingClassifier(random_state=7)
    parameters = {'loss': ['deviance', 'exponential'],
                  'n_estimators': [i for i in range(80, 200, 10)],
                  'max_depth': [2, 3, 4, 5],
                  'max_features': ['log2', 'sqrt']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10, n_jobs=7)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def classify_only(X, Y, model):
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
    plt.title('Receiver operating characteristic example: '+model.__class__.__name__)
    plt.legend(loc="lower right")
    plt.show()
    print "Plot done"
