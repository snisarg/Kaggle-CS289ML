import pandas
import math
from multiprocessing.pool import ThreadPool

#pool = ThreadPool(processes=4)

#get_bids = pool.apply_async(
#    lambda: pandas.read_csv('data/bids.csv', parse_dates=['time']).sort_values(by=['auction', 'time']))

test = pandas.read_csv('data/test.csv')
print "Test read"
print len(test)
# print train['outcome'].value_counts()

# Trying to see if there are multiple users with the same address
# print train['address'].value_counts()
# TO DO

# Match bids and train set
bids = pandas.read_csv('data/bids.csv', parse_dates=['time']).sort_values(by=['auction', 'time'])
print "Bids read"
# get_inner_join = pool.apply_async(
#     lambda: pandas.merge(left=bids, right=train, left_on='bidder_id', right_on='bidder_id')
#                   .sort_values(by=['bidder_id']))

# annot_bids = pandas.merge(left=test, right=bids, how='left', left_on='bidder_id', right_on='bidder_id')
# print annot_bids[['auction', 'bidder_id', 'outcome', 'time']]

# annot_bids[['auction', 'bidder_id', 'outcome', 'time']].to_csv('data/temp.csv', sep='\t')
# Looks like the bot bidder outbids his own highest bid
# Self outbid column addition :
# UNCOMMENT TO GENERATE FILE. IT TAKES A WHILE
# last_auction_id = 'abc'
# prev_row = 0
# self_outbid = []
# for index, row in annot_bids.iterrows():
#     # print row_index
#     if last_auction_id != row['auction']:
#         last_auction_id = row['auction']
#         self_outbid.append(0)
#     else:
#         if prev_row['bidder_id'] == row['bidder_id']:
#             self_outbid.append(1)
#         else:
#             self_outbid.append(0)
#     prev_row = row
#
# annot_bids['self_outbid'] = self_outbid
# annot_bids.to_csv('data/test_self_bid.csv', sep='\t')
# print "Self_bid done"
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
inner_join = pandas.merge(left=bids, right=test, left_on='bidder_id', right_on='bidder_id') \
                    .sort_values(by=['bidder_id'])
print "Inner join done"
# Number of bids per bidder
inner_join['bid_count'] = inner_join.groupby(by='bidder_id', as_index=False)['bidder_id'].transform(
    lambda s: (float(s.count()-1)/515032.0))
bid_count = inner_join[['bidder_id', 'bid_count']].sort_values(by=['bid_count']).drop_duplicates()
print "Bid count done"
# print inner_join[['bidder_id', 'auction']].drop_duplicates()['bidder_id'].value_counts()

# Number of auctions per bidder participated
inner_join['auction_count'] = inner_join[['bidder_id', 'auction']].drop_duplicates().groupby(by=['bidder_id'], as_index=False)['auction'].transform(
    lambda s: float(s.count()-1)/1622.0
)
auction_counts = inner_join[['bidder_id', 'auction_count']].sort_values(by=['auction_count'], ascending=False).drop_duplicates()
# auction_counts.loc[auction_counts['auction_count'] > -1,'auction_count'] = 0.0
# auction_counts['auction_count'].fillna(0.0, inplace=True)
auction_counts = auction_counts[auction_counts['auction_count'] > -1]
print "Auction count done"
# print auction_counts

# print inner_join[['bidder_id', 'auction_count']]

# inner_join = inner_join.sort_values(by=['bidder_id', 'time'])
# inner_join.to_csv('data/sorted_inner_join.csv')
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
# inner_join['time_diff'] = time_diff
# print "Time diff done"
# inner_join.to_csv('data/test_time_diff.csv', sep='\t')
# print "time_diff.csv written"


inner_join['device_count'] = inner_join[['bidder_id', 'device']].drop_duplicates().groupby(by=['bidder_id'], as_index=False)['device'].transform(
    lambda s: float(s.count()-1)/2617.0
)
device_counts = inner_join[['bidder_id', 'device_count']].sort_values(by=['device_count'], ascending=False).drop_duplicates()
# device_counts.loc[device_counts['device_count'] > -1,'device_count'] = 0.0
# device_counts['device_count'].fillna(0.0,inplace=True)
device_counts = device_counts[device_counts['device_count'] > -1]
print "Device count done"

inner_join['ip_count'] = inner_join[['bidder_id', 'ip']].drop_duplicates().groupby(by=['bidder_id'], as_index=False)['ip'].transform(
    lambda s: float(s.count()-1)/111917.0
)
ip_counts = inner_join[['bidder_id', 'ip_count']].sort_values(by=['ip_count'], ascending=False).drop_duplicates()
# ip_counts.loc[ip_counts['ip_count'] > -1,'ip_count'] = 0.0
# ip_counts['ip_count'].fillna(0.0,inplace=True)
ip_counts = ip_counts[ip_counts['ip_count'] > -1]
print "IP count done"

inner_join['country_count'] = inner_join[['bidder_id', 'country']].drop_duplicates().groupby(by=['bidder_id'], as_index=False)['country'].transform(
    lambda s: float(s.count()-1)/177.0
)
country_counts = inner_join[['bidder_id', 'country_count']].sort_values(by=['country_count'], ascending=False).drop_duplicates()
# country_counts.loc[country_counts['country_count'] > -1,'country_count'] = 0.0
# country_counts['country_count'].fillna(0.0,inplace=True)
country_counts = country_counts[country_counts['country_count'] > -1]
print "Country count done"


#Device Entropy
# edev = inner_join[['bid_id', 'bidder_id', 'device']]
# print "Start entropy"
# edev['bid_count']=inner_join.groupby(by='bidder_id', as_index=False)['bidder_id'].transform(
#     lambda s: s.count()
# )
# edev['n_dev'] = inner_join[['bid_id', 'bidder_id', 'device']].drop_duplicates().groupby(by=['bidder_id', 'device'], as_index=False)['bid_id'].transform(
#     lambda s: s.count()
# )
# print "n_dev done"
# edev = edev[['bidder_id', 'device', 'bid_count', 'n_dev']].drop_duplicates()
# print edev
# for index, row in edev.iterrows():
#     print index
#     edev.loc[index,'n_dev_n'] = float(edev.loc[index,'n_dev'])/float(edev.loc[index,'bid_count'])
#     if(edev.loc[index,'n_dev_n']!=0):
#         edev.loc[index,'log_n_n_dev'] = math.log(float(1.0/float(edev.loc[index,'n_dev_n'])),2)
#     else:
#         edev.loc[index,'log_n_n_dev'] = 0.0
#     edev.loc[index,'n_dev_ent'] = edev.loc[index,'n_dev_n']*edev.loc[index,'log_n_n_dev']
# print "n_dev_ent done"
# print edev
# edev['dev_ent'] = edev[['bidder_id', 'n_dev_ent']].groupby(by=['bidder_id'], as_index=False)['n_dev_ent'].transform('sum')
# edev = edev[['bidder_id', 'dev_ent']].drop_duplicates()
# print edev
# edev.to_csv('test_edev.csv',index=False)


#IP Entropy
# eip = inner_join[['bid_id', 'bidder_id', 'ip']]
# print "Start entropy"
# eip['bid_count']=inner_join.groupby(by='bidder_id', as_index=False)['bidder_id'].transform(
#     lambda s: s.count()
# )
# eip['n_ip'] = inner_join[['bid_id', 'bidder_id', 'ip']].drop_duplicates().groupby(by=['bidder_id', 'ip'], as_index=False)['bid_id'].transform(
#     lambda s: s.count()
# )
# print "n_ip done"
# eip = eip[['bidder_id', 'ip', 'bid_count', 'n_ip']].drop_duplicates()
# print eip
# for index, row in eip.iterrows():
#     # print index
#     eip.loc[index,'n_ip_n'] = float(eip.loc[index,'n_ip'])/float(eip.loc[index,'bid_count'])
#     if(eip.loc[index,'n_ip_n']!=0):
#         eip.loc[index,'log_n_n_ip'] = math.log(float(1.0/float(eip.loc[index,'n_ip_n'])),2)
#     else:
#         eip.loc[index,'log_n_n_ip'] = 0.0
#     eip.loc[index,'n_ip_ent'] = eip.loc[index,'n_ip_n']*eip.loc[index,'log_n_n_ip']
# print "n_ip_ent done"
# print eip
# eip['ip_ent'] = eip[['bidder_id', 'n_ip_ent']].groupby(by=['bidder_id'], as_index=False)['n_ip_ent'].transform('sum')
# eip = eip[['bidder_id', 'ip_ent']].drop_duplicates()
# print eip
# eip.to_csv('test_eip.csv',index=False)

#Country entropy
# ecntry = inner_join[['bid_id', 'bidder_id', 'country']]
# print "Start entropy"
# ecntry['bid_count']=inner_join.groupby(by='bidder_id', as_index=False)['bidder_id'].transform(
#     lambda s: s.count()
# )
# ecntry['n_c'] = inner_join[['bid_id', 'bidder_id', 'country']].drop_duplicates().groupby(by=['bidder_id', 'country'], as_index=False)['bid_id'].transform(
#     lambda s: s.count()
# )
# print "n_c done"
# ecntry = ecntry[['bidder_id', 'country', 'bid_count', 'n_c']].drop_duplicates()
# print ecntry
# for index, row in ecntry.iterrows():
#     # print index
#     ecntry.loc[index, 'n_c_n'] = float(ecntry.loc[index, 'n_c']) / float(ecntry.loc[index, 'bid_count'])
#     if(ecntry.loc[index, 'n_c_n']!=0):
#         ecntry.loc[index, 'log_n_n_c'] = math.log(float(1.0 / float(ecntry.loc[index, 'n_c_n'])), 2)
#     else:
#         ecntry.loc[index, 'log_n_n_c'] = 0.0
#     ecntry.loc[index, 'n_c_ent'] = ecntry.loc[index, 'n_c_n'] * eip.loc[index, 'log_n_n_c']
# print "n_c_ent done"
# print ecntry
# ecntry['c_ent'] = ecntry[['bidder_id', 'n_c_ent']].groupby(by=['bidder_id'], as_index=False)['n_c_ent'].transform('sum')
# ecntry = ecntry[['bidder_id', 'c_ent']].drop_duplicates()
# print ecntry
# ecntry.to_csv('test_ecntry.csv',index=False)