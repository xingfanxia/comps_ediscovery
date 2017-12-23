'''
Dummy Version of Random Forest
'''
from lib.tree import Tree
from lib.exceptions import *
import numpy as np
import pandas as pd
import random
import pickle
import multiprocessing

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
    def __init__(self, train_data, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features):
        self.trees = []
        self.train_data = train_data
        self.n_trees = n_trees
        self.tree_depth = tree_depth
        self.n_max_features = n_max_features
        self.n_max_input = n_max_input
        self.cat_features = cat_features
        self.seed = random_seed
#         self.features = [()] #list of tuples like (tree, emails, features)
        random.seed(random_seed)

        np.random.seed(random_seed)

        self.oob_threshold = 0
        
        self.label_col_num = 60

    '''
    Randomly select features and emails from the train_data
    '''
    #TODO: fix this so that the features selected are the actual features, not the indices of the features.
    def random_select(self, train_data):
        selected_rows = np.random.choice(self.train_data.shape[0], self.n_max_input)
        selected_feature_indices = np.random.choice(self.train_data.shape[1] - 1, self.n_max_features, replace=False)
        selected_features = train_data.columns.values[[selected_feature_indices]]
        return (selected_rows, selected_features)
        
        selected_features = np.random.choice(self.train_data.shape[1] - 2, self.n_max_features, replace=False)
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
            self.trees.append(Tree(self.train_data, self.tree_depth, 0, selected[0], selected[1], self.cat_features)) 
            
        # handling multiprocessing logic

        # count cpus
        # cpu_count = multiprocessing.cpu_count()
        cpu_count = len(self.trees)
        pool = multiprocessing.Pool( cpu_count )
        tasks = []
        tNum = 0
        max_t = cpu_count
        
        results = []
        for tree in self.trees:
            results.append( pool.apply_async(tree.fit) )
        
        r = []
        for result in results:
            r.append(result.get())
        print('done!')

    '''
    calculate a proba from output of each tree's prediction
    should ouput two arrays: probas and classfication
    '''
    def some_majority_count_metric(self, score):
        return np.mean(score, axis=0)

    def predict(self, test_data):
        
        
                
        # count cpus
        # cpu_count = multiprocessing.cpu_count()
        cpu_count = len(self.trees)
        pool = multiprocessing.Pool( cpu_count )
        tasks = []
        tNum = 0
        max_t = cpu_count
        
        for tree in self.trees:
            tasks.append( (test_data,) )
        
        results = []
        for i in range(len(self.trees)):
            results.append( pool.apply_async(self.trees[i].predict, tasks[i]) )
        #for tree in self.trees:
        #   results.append( pool.apply_async(tree.predict, tasks[0]) )
        
        r = []
        for result in results:
            r.append(result.get())
        
        #print (r);
        for a in r:
            print(a)
        print ("len(test_data): {}".format(len(test_data)))
        print ("len(r): {}".format(len(r)))
        # return
        #trees = r
        
        
        trees = [tree.predict(test_data) for tree in self.trees]
        print ("len(trees): {}".format(len(trees)))
        print ("trees == r : {}".format(trees == r))
        scores = [ list() for doc in trees[0]]
        for doc in range(len(trees[0])):
            for tree in trees:
                scores[doc].append(tree[doc])
        probas = [self.some_majority_count_metric(score) for score in scores]
        classes = ['1' if proba[0] > proba[1] else '0'  for proba in probas]
        return probas, classes

    def retrain_tree(self):
        # assume that self.data contains the new data
        # TODO: change as necessary
        selected = self.random_select(self.train_data)
        tree = Tree(self.train_data, self.tree_depth, 0, selected[0], selected[1], self.cat_features)
        tree.fit()
        return tree
    
    def update_leaves(self, tree):
        # assume that self.data contains the new data
        # TODO: change as necessary
        tree.update(self.train_data, self.random_select(self.train_data)[0])

    
    '''
    params:
    more_data - more training data to update the forest

    return:
    Null or we can say something like which trees are changed
    '''
    def update(self, more_data):
        
        self.train_data = more_data
        # or self.train_data.append(more_data)
        
        # use average as placeholder function
        thresh = 0
        for tree in self.trees:
            thresh += tree.calc_oob_error()
        thresh = thresh / len(self.trees)
        self.oob_threshold = thresh
        
        # TODO: This is temporary code for testing!!!
        #thresh = 0
        
        for i in range(len(self.trees)):
            if (self.trees[i].oob_error < thresh):
                
                # discard and remake
                self.trees[i] = self.retrain_tree()
            else:
                # update leave nodes
                self.update_leaves(self.trees[i])
                

                
    def store_rnf(self, file_path):
        f = open(file_path, 'wb')
        pickle.dump(self, f)
        f.close()
#         pass

    def load_rnf(self, file_path):
        f = open(file_path, 'rb')
        temp = pickle.load(f)
        f.close()

#         reinitialize some variables
        self.__init__(temp.train_data, temp.n_trees, temp.tree_depth, temp.seed, temp.n_max_features, temp.n_max_input, temp.cat_features)
#         the part that matters: load the pre-trained then stored trees into the RNF object instance
        self.trees = temp.trees
