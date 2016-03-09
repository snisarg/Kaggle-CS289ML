import pandas
from sklearn import linear_model, cross_validation
import numpy

self_bid = pandas.read_csv('data/time_diff.csv', sep='\t')
self_bid['time_diff_mean'] = self_bid.groupby(by='bidder_id', as_index=False)['time_diff'].transform('mean')

print self_bid[['bidder_id', 'time_diff_mean', 'outcome']].drop_duplicates()