import pandas
from multiprocessing.pool import ThreadPool

#pool = ThreadPool(processes=4)

#get_bids = pool.apply_async(
#    lambda: pandas.read_csv('data/bids.csv', parse_dates=['time']).sort_values(by=['auction', 'time']))

train = pandas.read_csv('data/train.csv')
# print train['outcome'].value_counts()

# Trying to see if there are multiple users with the same address
# print train['address'].value_counts()
# TO DO

# Match bids and train set
bids = pandas.read_csv('data/bids.csv', parse_dates=['time']).sort_values(by=['auction', 'time'])

# get_inner_join = pool.apply_async(
#     lambda: pandas.merge(left=bids, right=train, left_on='bidder_id', right_on='bidder_id')
#                   .sort_values(by=['bidder_id']))

# annot_bids = pandas.merge(left=bids, right=train, how='left', left_on='bidder_id', right_on='bidder_id')
# print annot_bids[['auction', 'bidder_id', 'outcome', 'time']]

# annot_bids[['auction', 'bidder_id', 'outcome', 'time']].to_csv('data/temp.csv', sep='\t')
# Looks like the bot bidder outbids his own highest bid
# Self outbid column addition :
# UNCOMMENT TO GENERATE FILE. IT TAKES A WHILE
# last_auction_id = -1
# self_outbid = []
# for row_index in range(len(annot_bids)):
#     print row_index
#     if last_auction_id != annot_bids.loc[row_index]['auction']:
#         last_auction_id = annot_bids.loc[row_index]['auction']
#         self_outbid.append(0)
#     else:
#         if annot_bids.loc[row_index-1]['bidder_id'] == annot_bids.loc[row_index]['bidder_id']:
#             self_outbid.append(1)
#         else:
#             self_outbid.append(0)
#
# annot_bids['self_outbid'] = self_outbid
# annot_bids.to_csv('data/self_bid.csv', sep='\t')
# print annot_bids['self_outbid'].value_counts()
# 0    5582005
# 1    2074329
# Name: self_outbid, dtype: int64

# Looking to see if country changes signify something
# country_user = get_inner_join.get()[['bidder_id', 'country', 'outcome']]
# print country_user[country_user['outcome']==0].drop_duplicates()

# print train[train['outcome'] == 1]

# bid_per_user = annot_bids['bidder_id'].value_counts()
# print pandas.merge(left=bid_per_user, right=train, left_on='bidder_id', right_on='bidder_id')
inner_join = pandas.merge(left=bids, right=train, left_on='bidder_id', right_on='bidder_id') \
                   .sort_values(by=['bidder_id'])

# Number of bids per bidder
inner_join['bid_count'] = inner_join.groupby(by='bidder_id', as_index=False)['bidder_id'].transform(
    lambda s: (float(s.count()-1)/515032.0))
bid_count = inner_join[['bidder_id', 'bid_count', 'outcome']].sort_values(by=['bid_count']).drop_duplicates()

#print inner_join[['bidder_id', 'auction']].drop_duplicates()['bidder_id'].value_counts()

# Number of auctions per bidder participated
inner_join['auction_count'] = inner_join[['bidder_id', 'auction']].drop_duplicates().groupby(by=['bidder_id'], as_index=False)['auction'].transform(
    lambda s: float(s.count()-1)/1622.0
)
auction_counts = inner_join[['bidder_id', 'auction_count', 'outcome']].sort_values(by=['auction_count'], ascending=False).drop_duplicates()
auction_counts = auction_counts[auction_counts['auction_count'] > -1]
# print auction_counts

# print inner_join[['bidder_id', 'auction_count']]

inner_join = inner_join.sort_values(by=['bidder_id', 'time'])
#inner_join.to_csv('data/sorted_inner_join.csv')
# print inner_join[['bidder_id', 'time']]

# last_bidder_id = 'abc'
# prev_row = 0
# time_diff = []
# for index, row in inner_join.iterrows():
#     # print row_index
#     if last_bidder_id != row['bidder_id']:
#         last_bidder_id = row['bidder_id']
#         time_diff.append(0)
#     else:
#         # if inner_join.loc[row_index-1]['bidder_id'] == inner_join.loc[row_index]['bidder_id']:
#         difference = float(row['time']) - float(prev_row['time'])
#         if difference < 0:
#             print prev_row
#             print row
#         time_diff.append(difference)
#         #else:
#         #    self_outbid.append(0)
#     prev_row = row
#
# inner_join['time_diff'] = time_diff
# inner_join.to_csv('data/time_diff.csv', sep='\t')
