'''
A dummy implementation of decision trees
'''
from lib.node import Node
import numpy as np
import pandas as pd
import pickle
class Tree:
    
    '''
    params:
    train_data - training data to trainthe tree
    depth - max recursion depth of the tree
    benchmark - benchmark for geni/entropy
    '''
    def __init__(self, data, depth, benchmark, rows, features): #should we include data here
        self.depth = depth
        self.rows = rows
        self.features = features
        self.data = data
        self.benchmark = benchmark
        self.head = Node(data, rows, features, 0, depth)
        self.oob_error = -1
        
    '''
    Recursively split until geni/entropy benchmark met or max_depth reached
    '''
    def fit(self):
        #think about behavior of pure nodes more
        try:
            self.head.split()
        except ValueError: #change this to whatever node.split() throws
            print('Head is a pure node.')
    '''
    params: 
    test_data - test data to run the prediction on
    
    return: 
    outputs confidence/probability of each category
    '''
    def predict(self, test_data):
#         assuming input data is a dataframe right now
        confidences = []
        for index, row in test_data.iterrows():
            cur_node = self.head
            while (cur_node.left and cur_node.right):
                if (row[cur_node.min_feature] < cur_node.min_break_point):
                    cur_node = cur_node.left
                else:
                    cur_node = cur_node.right
#         here, cur_node should be the leaf
            r_confidence = cur_node.get_proportions('R')
            m_confidence = cur_node.get_proportions('M')
            confidences.append((r_confidence, m_confidence))
        return confidences
    
    '''
    params: 
    more_data - more training data to update the tree
    
    return: 
    Null or we can say something like which nodes are changed
    '''
    def update(more_data):
        #decide whether to call alg 3 or alg 4
        #call the relevant one
        pass
    
    '''
    return:
    The number of ignored data pieces that we get incorrect (n) divided by the number of rows we ignored (l)
    That is, n/l
    '''
    def calc_oob_error(self):
        #complement of rows
        test_data = self.data.loc[~self.data.index.isin(self.rows)]
        complement = set(range(self.data.shape[1])) - set(self.rows)
        #predict each of those (TODO: update this once we have batch training)
        num_incorrect = 0
        for row in complement:
            case = self.data.loc[[row]]
            prediction = self.predict(case)
            prediction = prediction[0]
            if prediction[0] > prediction[1]:
                num_incorrect += 1 if case[60].values[0] == 'M' else 0
            else:
                num_incorrect += 1 if case[60].values[0] == 'R' else 0
        return num_incorrect / len(test_data)
        #calculate incorrect / total
        
    def store_tree(self, file_path):
        f = open('file_path', 'wb')
        pickle.dump(self, f)
        f.close()
        
    
    def load_tree(self, file_path):
        f = open('file_path', 'rb')
        temp = pickle.load(f)
        f.close()
        
#         reinitialize some variables
        self.__init__(temp.data, temp.depth, temp.benchmark, temp.rows, temp.features)
#         reassign the head
        self.head = temp.head
    
    
    '''
    String representation
    '''
    def __str__(self):
        string = ''
        string += str(sorted(self.features))
        string += '\n'
        nodes = [self.head]
        while(len(nodes) > 0):
            new_nodes = []
            level_str = ''
            for node in nodes:
                level_str += str(node) + "\n"
                if node.left:
                    new_nodes.append(node.left)
                if node.right:
                    new_nodes.append(node.right)
            string += level_str+"\n--------------------------------------------------\n"
            nodes = new_nodes
        return string