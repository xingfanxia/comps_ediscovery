import sys
sys.path.append("..")
from lib import *
from sklearn.utils import shuffle
from datetime import datetime
import numpy
import os.path

import urllib.request as request
file_path = 'data/research/sonar.all-data.csv'
if not os.path.isfile(file_path):
    d_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data'
    request.urlretrieve(d_url, file_path)

df = pd.read_csv(file_path, header=None)
# depth = 3
# benchmark = None
# rows = list(range(1, 170))
# rows = numpy.random.choice(list(range(1,200)), size)
# features = list(range(3, 10))

f = RNF(df, 3, 3, None, 20, 140)
f.fit()
# for tree in f.trees:
#     print(tree.calc_oob_error())

print(f.update(None))
# t1 = Tree(shuffle(df, random_state=numpy.random.RandomState()), depth, benchmark, rows, features)
# t1.fit()
# print(t1.calc_oob_error())
# print(t1.calc_oob_error())
# print(t1)
# t1.predict(df.loc[[1]])
