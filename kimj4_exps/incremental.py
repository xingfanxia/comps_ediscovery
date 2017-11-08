from importlib import reload
import sys
s = sys.stdout
# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.stdout = stdout
# import sys
# stdout = sys.stdout
sys.path.append("..")
from lib import *
from sklearn.utils import shuffle

# %mkdir -p data/research

import urllib.request as request
file_path = 'data/research/sonar.all-data.csv'
d_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data'
request.urlretrieve(d_url, file_path)

sys.stdout = s
# file_path = 'data/research/sonar.all-data.csv'

df = pd.read_csv(file_path, header=None)
df = shuffle(df)
df = df.reset_index()
depth = 3
benchmark = None
rows = list(range(1, 170))
features = list(range(3, 10))

random_seed = 678
cross_val_rnf_incremental(df, 5, 999, random_seed)
