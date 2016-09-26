import pandas
import classify_data


final_col = pandas.read_csv('data/smote_col.csv')


result = classify_data.grid_grad_boost(
    final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count',
               'country_count','dev_ent']],
    final_col['outcome'])