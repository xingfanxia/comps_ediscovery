# import lib.forest as forest
import math
import random
import numpy as np
import pandas as pd
from lib.tree import Tree
from lib.forest import RNF
from lib.evalMetrics import *
from sklearn.utils import shuffle
import sys

def cross_val_tree(df, tries):
    for i in range(tries):
        shuffle = df.sample(frac=1)
        shuffle = shuffle.reset_index(drop=True)
        ls = [x for x in range(60)]
        tree = Tree(shuffle, 3, None, range(shuffle.shape[0]-20), ls)
        tree.fit()
        score = 0
        labels = [row[60]  for index, row in shuffle[188:208].iterrows()]
        probas = tree.predict(shuffle[188:208])
        for i in range(len(labels)):
            if probas[i][0] > probas[i][1]:
        #         print('R/{}'.format(actual))
                if 'R' == labels[i]: 
                    score+=1
            else:
        #         print('M/{}'.format(actual))
                if 'M' == labels[i]: 
                    score+=1
        print(score/(208-188))

def cross_val_rnf(df, tries):
    for i in range(tries):
        shuffle = df.sample(frac=1, random_state=1)
        shuffle = shuffle.reset_index(drop=True)
        forest = RNF(shuffle[0:188], 2, 3, random.randint(1, 100), 40, 80)
        forest.fit()
        score = 0
        labels = [row[60]  for index, row in shuffle[188:208].iterrows()]
        predicted_classes = forest.predict(shuffle[188:208])[1]
#         print(predicted_classes, labels)
        score = sum( [ 1 for i in range(len(predicted_classes)) if predicted_classes[i] == labels[i]])
        print(score/(208-188))
        
def cross_val_rnf_incremental(num_trees, df, tries, num_increments, random_seed, cat_features, overall_training_ratio, 
                              initial_training_ratio, increment_size):
    ''' 
        Testing for incremental learning. 
        Start some small subset of the dataset and increment with 10 more, see if there's an improvement.
        args:
            df (dataframe)
            tries (int) number of times to repeat the test
            num_increments (int) number of times to incrementally train a model
            random_seed (some object)
            cat_features (list) required to initalize forest
            overall_training_ratio (float) fraction of df to use as the training set
            initial_training_ratio (float) fraction of df to use as the training set before any increments
            increment_size (int) number of new rows to use per incremental step
    '''
    if (overall_training_ratio >= 1):
        print("The training set should be samller than the dataset")
        return
    if (initial_training_ratio >= 1):
        print("The initial training set should be smaller than the dataset")
        return
    if (initial_training_ratio >= overall_training_ratio):
        print("The initial training set should be smaller than the overall training set")
        return
    
    
        
    dataset_size = df.shape[0]
    initial_train_size = math.floor(dataset_size * initial_training_ratio)
    overall_train_size = math.floor(dataset_size * overall_training_ratio)
    test_size = dataset_size - overall_train_size;
    
    increment_limit = (overall_train_size - initial_train_size) / increment_size
    increment_limit = int(math.floor(increment_limit))
    
    if num_increments > increment_limit:
        print('too many increments specified ({}), running with the max possible: ({})'.format(num_increments, increment_limit))
        num_increments = increment_limit;
    for i in range(tries):
        cur_max = initial_train_size
        shuffled_df = df.sample(frac=1, random_state=1)
        #shuffled_df = shuffle(df, random_state=random_seed)
        shuffled_df = shuffled_df.reset_index(drop=True)
        
        # initial fit
        initial_df = shuffled_df[0:cur_max]
        n_features = math.floor(math.sqrt(df.shape[1]))
        tree_depth = 20
        forest = RNF(initial_df, num_trees, tree_depth, random_seed, n_features, cur_max, cat_features)
        #forest.fit()
        forest.fit_parallel()
        
        score = 0
        # This is the answer key
        labels = [row["Label"] for index, row in shuffled_df[-test_size:].iterrows()]
        print("LABELS:")
        print(labels)        
        
        predicted_classes = forest.predict_parallel(shuffled_df[-test_size:])[1]
        print("predicted_classes:")
        print(predicted_classes)
        score = sum( [ 1 for i in range(len(predicted_classes)) if predicted_classes[i] == labels[i]])
        print('score before incremental training: ' + str(score / test_size))
        
        last = initial_train_size
        for j in range(1, num_increments + 1):
            
            # print(last)
            
            # put this into RNF later!!!
            forest.n_max_input = last
            predicted = forest.predict_parallel(shuffled_df[last:last + increment_size])
            prediction_ratios = predicted[0]
            
            
            low_confidence_threshold = .05
            high_confidence_threshold = .8
            
            
            # these store indices
            less_confident = []
            more_confident = []
            for i in range(len(prediction_ratios)):
                ratio = prediction_ratios[i]
                if abs(ratio[0] - ratio[1]) <= low_confidence_threshold:
                    less_confident.append(last + i)
                if abs(ratio[0] - ratio[1]) >= high_confidence_threshold:
                    more_confident.append(last + i)
                    
                
            print("len(less_confident): {}".format(len(less_confident)))
            print("len(more_confident): {}".format(len(more_confident)))
            
            less_confident.extend(more_confident)
            
            forest.update(shuffled_df.loc[less_confident])
            # print(type(forest.trees[0].head.rows[0]))
            
#             evalMetrics.evalStats(predicted[1], shuffled_df[last:last + increment_size].reset_index(drop=True))
            
            score = 0
            labels = [row["Label"] for index, row in shuffled_df[-test_size:].iterrows()]
            predicted_classes = forest.predict_parallel(shuffled_df[-test_size:])[1]
            evalStats(predicted_classes, shuffled_df[-test_size:])
            score = sum( [ 1 for i in range(len(predicted_classes)) if predicted_classes[i] == labels[i]])
            print('score at increment ' + str(j) + ': ' + str(score / test_size))
            
            last = last + increment_size