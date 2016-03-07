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

get_inner_join = pool.apply_async(
    lambda: pandas.merge(left=bids, right=train, left_on='bidder_id', right_on='bidder_id')
                  .sort_values(by=['bidder_id']))

annot_bids = pandas.merge(left=bids, right=train, how='left', left_on='bidder_id', right_on='bidder_id')
print annot_bids[['auction', 'bidder_id', 'outcome', 'time']]
# Looks like the bot bidder outbids his own highest bid

# Looking to see if country changes signify something
country_user = get_inner_join.get()[['bidder_id', 'country', 'outcome']]
print country_user[country_user['outcome']==0].drop_duplicates()

# print train[train['outcome'] == 1]
