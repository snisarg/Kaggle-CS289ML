import pandas
import classify_data
from sklearn import linear_model, ensemble, tree

final_col = pandas.read_csv('data/smote_col.csv')

# model = linear_model.SGDClassifier(random_state=7, penalty='none', loss='hinge')

# model = ensemble.AdaBoostClassifier(random_state=7, n_estimators=40, base_estimator=tree.DecisionTreeClassifier(),
#                                    algorithm='SAMME')

# model = tree.DecisionTreeClassifier(random_state=7, max_features='auto', criterion='entropy')

model = ensemble.GradientBoostingClassifier(random_state=7, max_features='log2', loss='deviance', n_estimators=160,
                                            max_depth=5)

classify_data.classify_only(
    final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
               'country_count','dev_ent']],
    final_col['outcome'],
    model)
