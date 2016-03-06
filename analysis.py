import pandas

train = pandas.read_csv('data/train.csv', index_col='bidder_id')
print train['outcome'].value_counts()
print train['address'].value_counts()

bids = pandas.read_csv('data/bids.csv').sort

#print train[train['outcome'] == 1]
