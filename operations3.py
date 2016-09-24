import pandas
import classify_data
from sklearn import neural_network, linear_model, grid_search, ensemble, tree, svm

def grid_grad_boost(X, Y):
    model = ensemble.GradientBoostingClassifier(random_state=7)
    parameters = {'loss': ['deviance', 'exponential'],
                  'n_estimators': [i for i in range(80, 200, 10)],
                  'max_depth': [2, 3, 4, 5],
                  'max_features': ['log2', 'sqrt']}
    clf = grid_search.GridSearchCV(model, parameters, cv=10)
    clf.fit(X, Y)
    print clf.grid_scores_
    print clf.best_params_


final_col = pandas.read_csv('data/final_col.csv')


result = grid_grad_boost(
    final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
               'country_count','dev_ent']],
    final_col['outcome'])