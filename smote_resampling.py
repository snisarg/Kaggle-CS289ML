import pandas
from imblearn.combine import smote_enn

sme = smote_enn.SMOTEENN(random_state=42)

final_col = pandas.read_csv('data/final_col.csv')

X, Y = sme.fit_sample(
    final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
               'country_count','dev_ent']],
    final_col['outcome'])

print Y
print X

smote_col = pandas.DataFrame(X, columns=['outbid_count', 'time_diff_mean', 'bid_count', 'auction_count',
                                       'device_count', 'ip_count', 'country_count', 'dev_ent'])
smote_col['outcome'] = Y

smote_col.to_csv('data/smote_col.csv')