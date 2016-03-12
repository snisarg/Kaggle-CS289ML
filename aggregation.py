import pandas
import analysis
import analysis_on_test
import time_diff_mean
import classify_data

print "For Training Data"
self_bid = pandas.read_csv('data/self_bid.csv', sep='\t')
print 'Self bid imported'

self_bid['outbid_count'] = self_bid.groupby('bidder_id', as_index=False)['self_outbid'].transform('sum')
# normalising outbid count
self_bid['outbid_count'] = self_bid['outbid_count'].apply(lambda x: float(x)/65015.0)
self_bid = self_bid[['bidder_id', 'outbid_count', 'outcome']]

final_col = pandas.merge(left=analysis.train[['bidder_id','outcome']],right =self_bid[['bidder_id','outbid_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id' )

final_col = pandas.merge(left=final_col,
                         right=time_diff_mean.sorted_time_diff[['bidder_id', 'time_diff_mean']],how='left',
                         left_on='bidder_id', right_on='bidder_id')
#print final_col

# From analysis
final_col = pandas.merge(left=final_col, right=analysis.bid_count[['bidder_id', 'bid_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

#print final_col

final_col = pandas.merge(left=final_col, right=analysis.auction_counts[['bidder_id', 'auction_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

final_col = pandas.merge(left=final_col, right=analysis.device_counts[['bidder_id', 'device_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

final_col = pandas.merge(left=final_col, right=analysis.ip_counts[['bidder_id', 'ip_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

final_col = pandas.merge(left=final_col, right=analysis.country_counts[['bidder_id', 'country_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

edev = pandas.read_csv('edev.csv')
# eip = pandas.read_csv('eip.csv')
# ecntry = pandas.read_csv('ecntry.csv')

final_col = pandas.merge(left=final_col, right=edev ,how='left',
                         left_on='bidder_id', right_on='bidder_id')
# final_col = pandas.merge(left=final_col, right=eip ,how='left',
#                          left_on='bidder_id', right_on='bidder_id')
# final_col = pandas.merge(left=final_col, right=ecntry ,how='left',
#                          left_on='bidder_id', right_on='bidder_id')

final_col=final_col.drop_duplicates()
final_col.fillna(0.0,inplace=True)
print final_col


print "For Test Data"

test_self_bid = pandas.read_csv('data/test_self_bid.csv', sep='\t')
print 'Test Self bid imported'

test_self_bid['outbid_count'] = test_self_bid.groupby('bidder_id', as_index=False)['self_outbid'].transform('sum')
# normalising outbid count
test_self_bid['outbid_count'] = test_self_bid['outbid_count'].apply(lambda x: float(x)/65015.0)
test_self_bid = test_self_bid[['bidder_id', 'outbid_count']]

test_final_col = pandas.merge(left = analysis_on_test.test[['bidder_id']],right=test_self_bid[['bidder_id', 'outbid_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

test_final_col = pandas.merge(left=test_final_col,
                         right=time_diff_mean.test_sorted_time_diff[['bidder_id', 'time_diff_mean']],how='left',
                         left_on='bidder_id', right_on='bidder_id')
#print final_col

# From analysis
test_final_col = pandas.merge(left=test_final_col, right=analysis_on_test.bid_count[['bidder_id', 'bid_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

#print final_col

test_final_col = pandas.merge(left=test_final_col, right=analysis_on_test.auction_counts[['bidder_id', 'auction_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

test_final_col = pandas.merge(left=test_final_col, right=analysis_on_test.device_counts[['bidder_id', 'device_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

test_final_col = pandas.merge(left=test_final_col, right=analysis_on_test.ip_counts[['bidder_id', 'ip_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

test_final_col = pandas.merge(left=test_final_col, right=analysis_on_test.country_counts[['bidder_id', 'country_count']],how='left',
                         left_on='bidder_id', right_on='bidder_id')

test_edev = pandas.read_csv('test_edev.csv')
# test_eip = pandas.read_csv('test_eip.csv')
# test_ecntry = pandas.read_csv('test_ecntry.csv')

test_final_col = pandas.merge(left=test_final_col, right=test_edev,how='left',
                         left_on='bidder_id', right_on='bidder_id')
# test_final_col = pandas.merge(left=test_final_col, right=test_eip,how='left',
#                          left_on='bidder_id', right_on='bidder_id')
# test_final_col = pandas.merge(left=test_final_col, right=test_ecntry,how='left',
#                          left_on='bidder_id', right_on='bidder_id')



test_final_col=test_final_col.drop_duplicates()
test_final_col.fillna(0.0,inplace=True)
print test_final_col

print "Running classifier"
classify_data.classify(final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count','country_count','dev_ent']],final_col['outcome'],"logistic",
                       test_final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count','country_count','dev_ent']],
                       test_final_col[['bidder_id']])

classify_data.classify(final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count','country_count','dev_ent']],final_col['outcome'],"rf",
                       test_final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count','country_count','dev_ent']],
                       test_final_col[['bidder_id']])

classify_data.classify(final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count','country_count','dev_ent']],final_col['outcome'],"gboost",
                       test_final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count','country_count','dev_ent']],
                       test_final_col[['bidder_id']])

classify_data.classify(final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count','country_count','dev_ent']],final_col['outcome'],"svm",
                       test_final_col[['outbid_count','time_diff_mean', 'bid_count', 'auction_count','device_count','ip_count','country_count','dev_ent']],
                       test_final_col[['bidder_id']])
