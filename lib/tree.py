'''
A dummy implementation of decision trees
'''
from lib.node import Node
from lib.exceptions import *
import numpy as np
import pandas as pd
import pickle, os
class Tree:
    
    '''
    params:
    train_data - training data to trainthe tree
    depth - max recursion depth of the tree
    benchmark - benchmark for geni/entropy
    '''
    def __init__(self, data, depth, benchmark, rows, features, cat_features): #should we include data here
        self.depth = depth
        self.rows = rows
        self.features = features
        self.data = data
        self.benchmark = benchmark
        self.head = Node(data, rows, features, 0, depth, cat_features)
        self.oob_error = -1
        self.cat_features = cat_features
    
    def visualize(self):
        if not os.path.exists('vis'):
            os.makedirs('vis')
        cur = self.head
        to_put = []
        nodes = [cur]
        depth = 0
        while len(nodes) > 0:
            children = []           
            for node in nodes:
                if node.left or node.right:
                     to_put.append('{ID} [label="X[{min_feature}] < {min_break}\ngini = {min_gini}\nsamples = {rows}\ndistribution = [{left}, {right}]"];'.format(ID=node.id, min_feature=node.min_feature, min_break=node.min_break_point, min_gini=node.min_gini, rows=len(node.rows), left=len(node.left.rows), right=len(node.right.rows)))
                else:
                     to_put.append('{ID} [label="samples = {rows}\nratio = [{left}, {right}]"];'.format(ID=node.id, rows=len(node.rows), left=node.get_proportions('0'), right=node.get_proportions('1')))
                if node.parent != None:
                    if node.side == 'l':
                        to_put.append('{} -> {} [labeldistance=8, labelangle=30, xlabel="True"]'.format(node.parent, node.id))
                    else:
                        to_put.append('{} -> {} [labeldistance=8, labelangle=-30, xlabel="False"]'.format(node.parent, node.id))
                if node.left:
                    children.append(node.left)
                if node.right:
                    children.append(node.right)
            nodes = children
        joined = "digraph Tree {\nnode [shape=box];\n" + "\n".join(to_put) + "\n}" 
        with open("vis/tree.dot", "w") as f:
            f.write(joined)
        return joined
        
    '''
    Recursively split until geni/entropy benchmark met or max_depth reached
    '''
    def fit(self):
        #think about behavior of pure nodes more
        try:
            self.head.split()
        except (ValueError, CannotDistinguishException) as e: #change this to whatever node.split() throws
            print(e)
    '''
    params: 
    test_data - test data to run the prediction on
    
    return: 
    outputs confidence/probability of each category
    '''
    def predict(self, test_data):
#         assuming input data is a dataframe right now
        confidences = []
        if not os.path.exists('vis'):
            os.makedirs('vis')
        for index, row in test_data.iterrows():
            to_put = []
            cur_node = self.head
            while (cur_node.left and cur_node.right):
                if cur_node.left or cur_node.right:
                     to_put.append('{ID} [label="X[{min_feature}] < {min_break}\ngini = {min_gini}\nsamples = {rows}\ndistribution = [{left}, {right}]"];'.format(ID=cur_node.id, min_feature=cur_node.min_feature, min_break=cur_node.min_break_point, min_gini=cur_node.min_gini, rows=len(cur_node.rows), left=len(cur_node.left.rows), right=len(cur_node.right.rows)))
                else:
                     to_put.append('{ID} [label="samples = {rows}\nratio = [{left}, {right}]"];'.format(ID=cur_node.id, rows=len(cur_node.rows), left=cur_node.get_proportions('0'), right=cur_node.get_proportions('1')))
                if cur_node.parent != None:
                        if cur_node.side == 'l':
                            to_put.append('{} -> {} [labeldistance=8, labelangle=30, xlabel="True"]'.format(cur_node.parent, cur_node.id))
                        else:
                            to_put.append('{} -> {} [labeldistance=8, labelangle=-30, xlabel="False"]'.format(cur_node.parent, cur_node.id))

                if self._should_go_left(row, cur_node):
                    cur_node = cur_node.left
                else:
                    cur_node = cur_node.right
#         here, cur_node should be the leaf
            relevant_confidence = cur_node.get_proportions('1')
            irrelevant_confidence = cur_node.get_proportions('0')
            confidences.append((relevant_confidence, irrelevant_confidence))
            joined = "digraph Tree {\nnode [shape=box];\n" + "\n".join(to_put) + "\n}" 
            with open("vis/{}_predict_vis.dot".format(index), "w") as f:
                f.write(joined)
        return confidences
    
    '''
    helper function to determine which way we should traverse through the tree.
    params:
    row - arraylike from the test data. Should have the same length as the training data.
    cur_node - the node that we are currently on.

    return:
    true if row's value is the same as cur_node's categorical breakpoint, or less than
        cur_node's numerical breakpoint
    false otherwise
    '''
    def _should_go_left(self, row, cur_node):
        if cur_node.min_feature in self.cat_features:
            return row[cur_node.min_feature] == cur_node.min_break_point
        return row[cur_node.min_feature] < cur_node.min_break_point

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