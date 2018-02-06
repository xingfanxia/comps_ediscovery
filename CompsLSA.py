from sklearn.decomposition import TruncatedSVD
import numpy as np


#Input: tfidf matrix, [1]output from build_TFIDF_Matrix
#Output: lsa matrix
#Build LSA matrix off TFIDF matrix. Must be done on computer with more RAM
def build_LSA_Matrix(tfMatrix):
    svd = TruncatedSVD(n_components = 100, algorithm='randomized')
    lsa = svd.fit_transform(tfMatrix)
    return lsa



#Input: LSA fit() from train data, tfidf matrix
#Output: LSA matrix
#LSA matrix off TFIDF matrix using svd trained already. Must be done on computer with more RAM
def build_LSA_train_test(vectorized_test, vectorized_train):
    svd = TruncatedSVD(n_components = 100, algorithm='randomized')
    svd_one = svd.fit(vectorized_train)
    lsa_one = svd_one.transform(vectorized_train)
    lsa_two = svd_one.transform(vectorized_test)
    np.save('svd_LSA_train_test.npy', svd_one)
    np.save('lsa_output_train_Feb2.npy', lsa_one)
    np.save('lsa_output_test_Feb2.npy', lsa_two)
    print("LSA files saved")
