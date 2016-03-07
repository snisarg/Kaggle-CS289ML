import pandas
from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=4)

get_bids = pool.apply_async(
    lambda: pandas.read_csv('data/bids.csv', parse_dates=['time']).sort_values(by=['auction', 'time']))

train = pandas.read_csv('data/train.csv')
print train['outcome'].value_counts()

# Trying to see if there are multiple users with the same address
print train['address'].value_counts()
# TO DO

# Match bids and train set
bids = get_bids.get()
annot_bids = pandas.merge(left=bids, right=train, how='left', left_on='bidder_id', right_on='bidder_id')
print annot_bids[['auction', 'bidder_id', 'outcome', 'time']]
# Looks like the bot bidder outbids his own highest bid

# print train[train['outcome'] == 1]
