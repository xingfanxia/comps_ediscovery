'''
Dummy Version of Random Forest
'''
from lib.tree import Tree
from lib.exceptions import *
import numpy as np
import pandas as pd
import random
import pickle

class RNF: 
    '''
    params:
    train_data - training data to trainthe tree
    n_trees - number of trees to setup
    tree_depth - max recursive
    random_seed - seed for random gen
    n_max_features - max num of features to pass to each tree
    n_max_input - max num of input to pass to each tree
    '''
    def __init__(self, train_data, n_trees, tree_depth, random_seed, n_max_features, n_max_input):
        self.trees = []
        self.train_data = train_data
        self.n_trees = n_trees
        self.tree_depth = tree_depth
        self.n_max_features = n_max_features
        self.n_max_input = n_max_input
#         self.features = [()] #list of tuples like (tree, emails, features)
        random.seed(random_seed)
    
        np.random.seed(random_seed)
    
    '''
    Randomly select features and emails from the train_data 
    '''
    def random_select(self, train_data):
        selected_rows = np.random.choice(self.train_data.shape[0], self.n_max_input)
        selected_features = np.random.choice(self.train_data.shape[1] - 1, self.n_max_features, replace=False)
        return (selected_rows, selected_features)
        
    '''
    pass randomly selected emails and features to each tree
    '''
    def fit(self):
        if len(self.trees) != 0:
            raise AlreadyFitException('This forest has already been fit to the data')
        for i in range(self.n_trees):
            selected = self.random_select(self.train_data)
#             self, train_data, depth, benchmark, rows, features
            self.trees.append(Tree(self.train_data, self.tree_depth, 0, selected[0], selected[1]))
        for tree in self.trees:
            tree.fit()
    
    '''
    calculate a proba from output of each tree's prediction
    should ouput two arrays: probas and classfication
    '''
    def some_majority_count_metric(self, score):
        return np.mean(score, axis=0)
    
    def predict(self, test_data):
        trees= [tree.predict(test_data) for tree in self.trees]
        scores = [ list() for doc in trees[0]]
        for doc in range(len(trees[0])):
            for tree in trees:
                scores[doc].append(tree[doc])
        probas = [self.some_majority_count_metric(score) for score in scores]
        classes = ['R' if proba[0] > proba[1] else 'M'  for proba in probas]
        return probas, classes
    
    '''
    params: 
    more_data - more training data to update the forest
    
    return: 
    Null or we can say something like which trees are changed
    '''
    def update(more_data):
        #add more_data to the end of self.train_data
        
        #calc oob error for each tree
        
        #calc threshold
        
        #for each tree in trees:
        #if oob < thresh
            #alg 3 (trash the tree and build a new one)
        #else alg 4
        pass
    
    def store_rnf(self, file_path):
        f = open('file_path', 'wb')
        pickle.dump(self, f)
        f.close()
#         pass
    
    def load_rnf(self, file_path):
        f = open('file_path', 'rb')
        temp = pickle.load(f)
        f.close()
        
#         reinitialize some variables
        self.__init__(temp.train_data, temp.n_trees, temp.tree_depth, temp.n_max_feature, temp.n_max_input)
#         the part that matters: load the pre-trained then stored trees into the RNF object instance
        self.trees = temp.trees