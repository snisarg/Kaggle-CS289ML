import pandas

train = pandas.read_csv('../data/train.csv')
print train

train['new_col'] = 1
print train
