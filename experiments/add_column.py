import pandas

train = pandas.read_csv('../data/train.csv')

train['new_col'] = 1
print train

newer_col = []
flip = False
for row in range(len(train)):
    if flip:
        newer_col.append(2)
    else:
        newer_col.append(1)
    flip = not flip

train.new_col = newer_col
print train
