# import lib.forest as forest
import math
import random
import numpy as np
import pandas as pd
from lib.tree import Tree
from lib.forest import RNF

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
        
def cross_val_rnf_incremental(df, tries, num_increments):
    ''' 
        Testing for incremental learning. 
        Start some small subset of the dataset and increment with 10 more, see if there's an improvement.
    '''
    increment_size = 20
    initial_train_size = 100
    
    increment_limit = (190 - initial_train_size) / increment_size
    increment_limit = int(math.floor(increment_limit))
    
    if num_increments > increment_limit:
        print('too many increments specified, running with the max possible...')
        num_increments = increment_limit;
    for i in range(tries):
        cur_max = initial_train_size
        shuffled_df = df.sample(frac=1, random_state=1)
        shuffled_df = shuffled_df.reset_index(drop=True)
        n_features = 8
        
        
        
        # initial fit
        forest = RNF(shuffled_df[0:cur_max], 64, 5, None, n_features, cur_max)
        forest.fit()
        
        # initial score 
        score = 0
        labels = [row[60] for index, row in shuffled_df[190:208].iterrows()]
        predicted_classes = forest.predict(shuffled_df[190:208])[1]
        score = sum( [ 1 for i in range(len(predicted_classes)) if predicted_classes[i] == labels[i]])
        print('score before incremental training: ' + str(score / (208 - 190)))
        
        
        for j in range(1, num_increments + 1):
            last = initial_train_size + j * increment_size
            print(last)
            
            # put this into RNF later!!!
            forest.n_max_input = last
            
            forest.update(shuffled_df[:last])
            
            
            
            score = 0
            labels = [row[60] for index, row in shuffled_df[190:208].iterrows()]
            predicted_classes = forest.predict(shuffled_df[190:208])[1]
            score = sum( [ 1 for i in range(len(predicted_classes)) if predicted_classes[i] == labels[i]])
            print('score at increment ' + str(j) + ': ' + str(score / (208 - 190)))
            
            
        
              
    
    
    
    