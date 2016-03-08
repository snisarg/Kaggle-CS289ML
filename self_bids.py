import pandas
from sklearn import linear_model

self_bid = pandas.read_csv('data/self_bid.csv', sep='\t')
outbid_sum = self_bid.groupby('bidder_id', as_index=False).self_outbid.sum()

print outbid_sum

train = pandas.read_csv('data/train.csv')
merged_result = pandas.merge(left=outbid_sum, right=train, left_on='bidder_id', right_on='bidder_id')
cor = merged_result[['self_outbid', 'outcome']]

print cor[cor['outcome']==1]

length = len(cor)

model = linear_model.LinearRegression()
model.fit(cor.self_outbid.values.reshape(length, 1), cor.outcome.values.reshape(length, 1))
print model.coef_
