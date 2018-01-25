import numpy as np
from sklearn.decomposition import TruncatedSVD

scenario_1_tfidf = np.load('scenario_1_tfidf.npy')
svd = TruncatedSVD(n_components = 100, algorithm='randomized')

lsa = svd.fit_transform(scenario_1_tfidf)

np.save('lsa_output_Jan25.npy', lsa)
