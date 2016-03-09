import pandas
from sklearn import linear_model, cross_validation
import numpy

self_bid = pandas.read_csv('data/self_bid.csv', sep='\t')
outbid_sum = self_bid.groupby('bidder_id', as_index=False).self_outbid.sum()

print outbid_sum

train = pandas.read_csv('data/train.csv')
merged_result = pandas.merge(left=outbid_sum, right=train, left_on='bidder_id', right_on='bidder_id')
cor = merged_result[['self_outbid', 'outcome']]

#print cor[cor['outcome']==1]
print cor

length = len(cor)

model = linear_model.LinearRegression()

X = cor.self_outbid.values.reshape(length, 1)
Y = cor.outcome.values.reshape(length, 1)
model.fit(X, Y)
print model.coef_

model = linear_model.LinearRegression()

predicted = cross_validation.cross_val_predict(model, X, Y, 10, 1, 0, None, 0)
scores = cross_validation.cross_val_score(model, X, Y,  cv=10, scoring='mean_squared_error')

print 'All RMSEs',  numpy.sqrt(-scores)
print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))
print 'Coefficients', model.coef_
