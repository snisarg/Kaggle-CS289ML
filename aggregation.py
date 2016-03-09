import time_diff_mean
import pandas
import analysis
import classify_data

self_bid = pandas.read_csv('data/self_bid.csv', sep='\t')
print 'Self bid imported'

self_bid['outbid_count'] = self_bid.groupby('bidder_id', as_index=False)['self_outbid'].transform('sum')
self_bid = self_bid[['bidder_id', 'outbid_count', 'outcome']]

final_col = pandas.merge(left=self_bid[['bidder_id', 'outcome', 'outbid_count']],
                         right=time_diff_mean.sorted_time_diff[['bidder_id', 'time_diff_mean']],
                         left_on='bidder_id', right_on='bidder_id')
print final_col

# From analysis
final_col = pandas.merge(left=final_col, right=analysis.bid_count[['bidder_id', 'bid_count']],
                         left_on='bidder_id', right_on='bidder_id')

print final_col

final_col = pandas.merge(left=final_col, right=analysis.auction_counts[['bidder_id', 'auction_count']],
                         left_on='bidder_id', right_on='bidder_id')

print final_col

classify_data.random_forest(final_col[['outbid_count', 'time_diff_mean', 'bid_count', 'auction_count']],
                            final_col['outcome'])
