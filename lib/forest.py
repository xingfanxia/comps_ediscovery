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
import time


NUM_CORES = 10

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
    def __init__(self, train_data, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features, user_input=False):
        self.trees = []
        self.input_type = user_input
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
    Randomly select features and emails from the train_data.
    Emails are selected with replacement, features without.
    np.delete calls are to resolve interference from non-feature columns
    '''
    def random_select(self, train_data):
        selected_rows = np.random.choice(self.train_data.index, self.n_max_input)
        selected_feature_indices = np.random.choice(self.train_data.shape[1] - 1, self.n_max_features, replace=False)
        selected_features = train_data.columns.values[[selected_feature_indices]]
        selected_features = np.delete(selected_features, np.where(selected_features == "Label"), axis=0)
        selected_features = np.delete(selected_features, np.where(selected_features == "Relevant"), axis=0)
        selected_features = np.delete(selected_features, np.where(selected_features == "ID"), axis=0)
        return (selected_rows, selected_features)


    '''
    Create and train trees for the forest.
    Use fit_parallel for a parallelized and updated version
    '''
    def fit(self):
        if len(self.trees) != 0:
            raise AlreadyFitException('This forest has already been fit to the data')
        for i in range(self.n_trees):
            selected = self.random_select(self.train_data)
            self.trees.append(Tree(self.train_data, self.tree_depth,
                                   0, selected[0], selected[1], self.cat_features,
                                   user_input=self.input_type))
        count = 0
        for tree in self.trees:
            count += 1
            tree = tree.fit()




    '''
    Parallelized version of fitting the model.
    Create trees with selected features and rows, and fits each on up to NUM_CORES number of cores
    '''
    def fit_parallel(self):
        if len(self.trees) != 0:
            raise AlreadyFitException('This forest has already been fit to the data')
        for i in range(self.n_trees):
            selected = self.random_select(self.train_data)
            self.trees.append(Tree(self.train_data, self.tree_depth, 0,
                                   selected[0], selected[1], self.cat_features,
                                   user_input=self.input_type))

        # create N new processes, where N = number of trees
        pool = multiprocessing.Pool( NUM_CORES )

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
        return np.nanmean(score, axis=0)

    '''
    Use the trained model to predict a label for previously unseen data.
    '''
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


    '''
    Check that there are no predictions that have probabilities over 1
    '''
    def _check_prediction_integrity(self, probabilities):
        num_exceeded = 0
        for p in probabilities:
            if p[0] > 1 or p[1] > 1:
                num_exceeded += 1
        return num_exceeded



    '''
    Use the trained model to predict a label for previously unseen data.
    This parallelized version asks each tree to do their predictions separately
    in their own cores, at up to NUM_CORES number of cores at a time.
    '''
    def predict_parallel(self, test_data, visualize=False, importance=False):
        pool = multiprocessing.Pool( NUM_CORES )
        # Asynchronous calls for the trees to do work
        results = []
        for i in range(len(self.trees)):
            results.append( pool.apply_async(self.trees[i].predict, (test_data, visualize, importance)) )

        r = []
        for result in results:
            r.append(result.get())

        pool.close()
        pool.join()

        trees_outputs = r
        # Aggregation of scores returned by each tree
        scores = [ list() for i in range(len(test_data))]
        for document_idx in range(len(test_data)):
            for tree in trees_outputs:
                scores[document_idx].append(tree[0][document_idx])
        probas = [self.some_majority_count_metric(score) for score in scores]
        classes = ['1' if proba[0] > proba[1] else '0'  for proba in probas]
        ids = trees_outputs[0][1]

        # Calculation of feature importances, if desired
        if importance:
            #sum up all of the importances
            importances = [{} for doc in trees_outputs[0][2]]
            for doc_idx, imp in enumerate(importances):
                for tree in trees_outputs:
                    for feature in tree[2][doc_idx].keys():
                        try:
                            imp[feature] += tree[2][doc_idx][feature]
                        except KeyError:
                            imp[feature] = tree[2][doc_idx][feature]
            #divide by num_trees
            for importance_dict in range(len(importances)):
                for feature in importances[importance_dict].keys():
                    importances[importance_dict][feature] = importances[importance_dict][feature] / len(self.trees)
            # print(importances)
            # print(ids)
            return probas, classes, ids, importances

        if self._check_prediction_integrity(probas) > 0:
            print("WARNING: Forest.predict_parallel(): {} of the {} predictions have probabilities above 1".format(self._check_prediction_integrity(probas), len(test_data)))

        return probas, classes, ids

    '''
    returns:
    probas - [(prob_rel, prob_irrel), ...]
        prob_rel - probability that this document is relevant
        prob_irrel - probability that this document is irrelevant
    classes - [relevance]
        relevance - '1' if relevant, '0' if irrelevant
    importances - [{feature:weight}]
        feature - a row of the df we used to predict
        weight - how important the feature was in the prediction, where positive means it nudged the prediction
            towards relevance and negative means it nudged the prediction towards irrelevance
    '''
    def predict_with_feat_imp(self, test_data):
        tree_results = [tree.predict_with_feat_imp(test_data) for tree in self.trees]
        scores = [list() for doc in tree_results[0][0]]
        for doc in range(len(tree_results[0][0])):
            for tree in tree_results:
                scores[doc].append(tree[0][doc])
        probas = [self.some_majority_count_metric(score) for score in scores]
        classes = ['1' if proba[0] > proba[1] else '0' for proba in probas]

        #sum up all of the importances
        importances = [{} for doc in tree_results[0][1]]
        for doc in range(len(importances)):
            for tree in tree_results:
                for feature in tree[1][doc].keys():
                    try:
                        importances[doc][feature] += tree[1][doc][feature]
                    except KeyError:
                        importances[doc][feature] = tree[1][doc][feature]
        #divide by num_trees
        for importance_dict in range(len(importances)):
            for feature in importances[importance_dict].keys():
                importances[importance_dict][feature] = importances[importance_dict][feature] / len(self.trees)
        return probas, classes, importances

    '''
    Used in incremental learning
    Randomly selects new data and features, creates the trees based on those, fits it, and returns it
    '''
    def retrain_tree(self):
        selected = self.random_select(self.train_data)
        tree = Tree(self.train_data, self.tree_depth,
                    0, selected[0], selected[1],
                    self.cat_features, user_input=self.input_type)
        tree.fit()
        return tree

    '''
    Used in incremental learning
    When a tree is good enough to be kept, instead of being retrained, the leaf nodes are updated
    This is done in a Tree member function
    params:
    tree - the Tree object that exists in self.trees to be updated
    '''
    def update_leaves(self, tree):
        tree.data = self.train_data
        tree.update(self.train_data, self.random_select(self.train_data)[0])


    '''
    Incremental learning functionality at the Forest level.
    Calculates a threshold based on the trees' out-of-bag errors
    Based on the threshold, decide which trees should be scrapped and replaced,
    and which should be updated.
    params:
    more_data - df, additional training data to update the forest. This is being appended to the
                existing train_data in the Forest.
    return:
    Null or we can say something like which trees are changed
    '''
    def update(self, more_data):
        # Update the data that the Forest can train on
        self.train_data = self.train_data.append(more_data)
        self.n_max_input = self.train_data.shape[0]
        # use average as placeholder function

        # Calculate the out-of-bag error threshold, a simple average for now
        thresh = 0
        for tree in self.trees:
            thresh += tree.calc_oob_error()
        thresh = thresh / len(self.trees)
        self.oob_threshold = thresh

        # Decide which trees are good enough to update, and which need to be replaced
        idx_trees_to_retrain = [] # indexes into self.trees for those to be replaced
        for i in range(len(self.trees)):
            if (self.trees[i].oob_error < thresh):
                idx_trees_to_retrain.append(i)
            else:
                self.update_leaves(self.trees[i])

        # To avoid errors from not having > 0 number of processes.
        # If there are no trees to retrain, just quit, since all
        # that need to be updated have been at this point.
        # TODO: possibly replace this with a try-except
        if idx_trees_to_retrain == []:
            return

        # Parallelized tree creation
        pool = multiprocessing.Pool( NUM_CORES )
        results = []

        for idx in idx_trees_to_retrain:
            results.append( pool.apply_async(self.retrain_tree) )

        retrained_trees = []
        for result in results:
            retrained_trees.append(result.get())

        pool.close()
        pool.join()

        # Place the returned trees into the slots previously marked for replacement
        for i in range(len(idx_trees_to_retrain)):
            self.trees[idx_trees_to_retrain[i]] = retrained_trees[i]


    '''
    Store the forest via pickling
    '''
    def store_rnf(self, file_path):
        f = open(file_path, 'wb')
        pickle.dump(self, f)
        f.close()

    '''
    Load the pickle, initialize the variable
    '''
    def load_rnf(self, file_path):
        f = open(file_path, 'rb')
        temp = pickle.load(f)
        f.close()

        # reinitialize some variables
        self.__init__(temp.train_data, temp.n_trees, temp.tree_depth,
                      temp.seed, temp.n_max_features, temp.n_max_input, temp.cat_features)
        # the part that matters: load the pre-trained then stored trees into the RNF object instance
        self.trees = temp.trees

    '''
    Returns a measure for which features are most important in the tree.
    returns:
    total - {feature:importance}, where importance is a measure of how important that feature is to the overall
        forest
    '''
    def get_feature_importances(self):
        total = {}
        for tree in self.trees:
            curr_importances = tree.get_mean_decrease_impurity()
            for feature in curr_importances.keys():
                try:
                    total[feature] += curr_importances[feature]
                except KeyError:
                    total[feature] = curr_importances[feature]
        return total
