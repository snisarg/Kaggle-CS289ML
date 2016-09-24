import pandas
import classify_data
from sklearn import neural_network, linear_model, grid_search

def grid_nn(X, Y):
    model = model = neural_network.MLPClassifier(activation='relu', solver='lbgfs')
    parameters = {'hidden_layer_size': [[5, 15, 15, 5], [10, 30, 30, 10], [5, 15, 30, 30, 15, 5],
                                        [50, 100, 100, 100, 75, 50]]}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_lr(X, Y):
    model = linear_model.LinearRegression(n_jobs=7)
    parameters = {'normalize': [True, False]}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_ridge(X, Y):
    model = linear_model.Ridge()
    parameters = {'alpha': [i * 0.1 for i in range(10)],
                  'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_bayesian(X, Y):
    model = linear_model.BayesianRidge()
    parameters = {'n_iter': [100, 200, 300, 400, 500, 600]}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


def grid_SGD(X, Y):
    model = linear_model.SGDClassifier()
    parameters = {'loss': ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron'],
                  'penalty': ['none', 'l2', 'l1', 'elasticnet']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


final_col = pandas.read_csv('data/final_col.csv')

# classify_data.grid_logistic(
#     final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
#                'country_count','dev_ent']],
#     final_col['outcome'])

# classify_data.grid_random_forest(
#     final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
#                'country_count','dev_ent']],
#     final_col['outcome'])


result = grid_SGD(
    final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
               'country_count','dev_ent']],
    final_col['outcome'])