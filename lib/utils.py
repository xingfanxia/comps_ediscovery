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