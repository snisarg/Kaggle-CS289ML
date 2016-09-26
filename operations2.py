import pandas
import classify_data


final_col = pandas.read_csv('data/smote_col.csv')

# classify_data.grid_logistic(
#     final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
#                'country_count','dev_ent']],
#     final_col['outcome'])

# classify_data.grid_random_forest(
#     final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
#                'country_count','dev_ent']],
#     final_col['outcome'])


result = classify_data.grid_lr(
    final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
               'country_count','dev_ent']],
    final_col['outcome'])