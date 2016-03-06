import pandas
import matplotlib

bids = pandas.read_csv('data/bids.csv', parse_dates=['time']).sort_values(by=['auction', 'time'])
train = pandas.read_csv('data/train.csv')
print bids
print bids['merchandise'].value_counts()
bids['merchandise'].value_counts().plot(kind='bar')
matplotlib.pyplot.show()

# bids_result = pandas.concat([bids, train])
# print bids_result
