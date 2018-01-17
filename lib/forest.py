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
import sys

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
        selected_features = np.delete(selected_features, np.where(selected_features == "Label"), axis=0)
        return (selected_rows, selected_features)

        #selected_features = np.random.choice(self.train_data.shape[1] - 2, self.n_max_features, replace=False)
        #return (selected_rows, selected_features)

    '''
    pass randomly selected emails and features to each tree
    '''
    def fit(self):
        if len(self.trees) != 0:
            raise AlreadyFitException('This forest has already been fit to the data')
        for i in range(self.n_trees):
            selected = self.random_select(self.train_data)
            self.trees.append(Tree(self.train_data, self.tree_depth, 0, selected[0], selected[1], self.cat_features))
        count = 0
        for tree in self.trees:
            count += 1
            print('fitting the {}th tree.'.format(count))
            tree = tree.fit()




    '''
    A separate paralellized fit function for now
    '''
    def fit_parallel(self):
        # Tree creation
        if len(self.trees) != 0:
            raise AlreadyFitException('This forest has already been fit to the data')
        for i in range(self.n_trees):
            selected = self.random_select(self.train_data)
            self.trees.append(Tree(self.train_data, self.tree_depth, 0, selected[0], selected[1], self.cat_features))

        # create N new processes, where N = number of trees
        pool = multiprocessing.Pool( len(self.trees) )

        # start the N tree.fit processes
        results = []
        for tree in self.trees:
            results.append( pool.apply_async(tree.fit) )

        pool.close()
        pool.join()

        r = []
        for result in results:
            r.append(result.get())

        for i in range(len(self.trees)):
            self.trees[i] = r[i]


    '''
    calculate a proba from output of each tree's prediction
    should ouput two arrays: probas and classfication
    '''
    def some_majority_count_metric(self, score):
        return np.mean(score, axis=0)

    def predict(self, test_data, visualize=False):
        trees_outputs = [tree.predict(test_data, visualize) for tree in self.trees]
        scores = [ list() for i in range(len(test_data))]
        for document_idx in range(len(test_data)):
            for tree in trees_outputs:
                scores[document_idx].append(tree[document_idx][0])
        probas = [self.some_majority_count_metric(score) for score in scores]
        classes = ['1' if proba[0] > proba[1] else '0'  for proba in probas]
        ids = [doc[1] for doc in trees_outputs[0]]
        return probas, classes, ids



    def predict_parallel(self, test_data, visualize=False):
        pool = multiprocessing.Pool( len(self.trees) )
        tasks = []

        for tree in self.trees:
            tasks.append( (test_data, visualize) )

        results = []
        for i in range(len(self.trees)):
            results.append( pool.apply_async(self.trees[i].predict, (test_data, visualize)) )

        r = []
        for result in results:
            r.append(result.get())

        trees_outputs = r


        trees_outputs = [tree.predict(test_data, visualize) for tree in self.trees]
        scores = [ list() for i in range(len(test_data))]
        for document_idx in range(len(test_data)):
            for tree in trees_outputs:
                scores[document_idx].append(tree[document_idx][0])
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

        #self.train_data = more_data
        self.train_data.append(more_data)

        # use average as placeholder function
        thresh = 0
        for tree in self.trees:
            thresh += tree.calc_oob_error()
        thresh = thresh / len(self.trees)
        self.oob_threshold = thresh

        # TODO: This is temporary code for testing!!!
        #thresh = 0

        idx_trees_to_retrain = []

        for i in range(len(self.trees)):
            if (self.trees[i].oob_error < thresh):
                idx_trees_to_retrain.append(i)
                # discard and remake
                # self.trees[i] = self.retrain_tree()
            else:
                # update leave nodes
                self.update_leaves(self.trees[i])

        cpu_count = len(idx_trees_to_retrain)
        pool = multiprocessing.Pool( cpu_count )
        tasks = []
        tNum = 0
        max_t = cpu_count

        results = []
        for idx in idx_trees_to_retrain:
            results.append( pool.apply_async(self.retrain_tree) )

        retrained_trees = []
        for result in results:
            retrained_trees.append(result.get())

        for i in range(len(idx_trees_to_retrain)):
            self.trees[idx_trees_to_retrain[i]] = retrained_trees[i]




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
