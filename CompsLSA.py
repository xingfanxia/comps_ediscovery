from sklearn.decomposition import TruncatedSVD


#Input: tfidf matrix, [1]output from build_TFIDF_Matrix
#Output: lsa matrix
#Build LSA matrix off TFIDF matrix. Must be done on computer with more RAM
def build_LSA_Matrix(tfMatrix):
    svd = TruncatedSVD(n_components = 100, algorithm='randomized')
    lsa = svd.fit_transform(scenario_1_tfidf)
    return lsa