import pandas
import matplotlib

bids = pandas.read_csv('../data/bids.csv', parse_dates=['time']).sort_values(by=['auction', 'time'])
train = pandas.read_csv('../data/train.csv')

print bids
print bids['merchandise'].value_counts()
bids['merchandise'].value_counts().plot(kind='bar')


merged = pandas.merge(left=bids, right=train, how='left', left_on='bidder_id', right_on='bidder_id')
#print merged

print merged['outcome'].value_counts()
# We therefore have train data for 3071224 bids whether they're bots or humans.

train_merge = pandas.merge(left=bids, right=train, left_on='bidder_id', right_on='bidder_id')
print merged[['auction', 'bidder_id', 'outcome', 'time']]


matplotlib.pyplot.show()


# bids_result = pandas.concat([bids, train])
# print bids_result
