from sklearn.decomposition import TruncatedSVD


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