'''
A dummy version of tree nodes
'''
from lib.exceptions import *
import random
import numpy as np
import pandas as pd
import math

class Node:
      
    def __init__(self, data, rows, features, depth, max_depth, parent=None, side=None):
        self.left = None
        self.right = None
        self.data = data
        self.rows = rows
        self.features = features
        self.label_index = 'Label'
        self.labels = data[self.label_index].unique()
        self.spliting_feature_val = None
        self.id = random.randrange(10**9, 10**10)
        self.depth = depth
        self.max_depth = max_depth
        self.min_feature = None
        self.min_break_point = None
        self.min_gini = None
        self.parent = parent
        self.side = side

    
    def calc_shannon_entropy(self):
        raw_val = 0
        for label in self.labels:
            members = self.data.loc[self.data[self.label_index] == label]
            if len(members) <= 0: continue
            filtered = [x for x in members.index.values if x in self.rows]
            intermediate = len(filtered)/len(self.rows)
            raw_val += -intermediate*np.log2(intermediate)
        return raw_val
    
    def calc_gini_index(self):
        raw_val = 1
#        string = '['
#        for row in self.rows:
#            string += str(row) 
#            string += ','
#        string += ']'
#        print(string)
#        print(type(self.data))
#        print(self.data.shape)
#        print(self.label_index)
#        members = [self.data[self.label_index][x] for x in self.rows]
        members = self.data.loc[self.rows][self.label_index].values
        for label in self.labels:
#             members = self.data.loc[self.data[self.label_index] == label]
            #maybe do as a for loop?
            #filtered = [x for x in members if x == label]
            filtered = members[members == label]
#             filtered = members
            raw_val -= (len(filtered)/len(self.rows))**2
        return raw_val
    
        
    '''
    calculate info gain from gini/entropy
    '''
    def cal_info_gain():
        pass
    
    def find_break_points(self, df, feature):
        breaks = []
        for i in range(len(df)-1):
            row = df[i:i+1]
            next_row = df[i+1:i+2]
#             print(row[self.label_index])
            if row[self.label_index].values[0] != next_row[self.label_index].values[0]:
                breaks.append(next_row[feature].values[0]) #float precision issue, care
        return breaks
    
        
    '''
    Choose the best feature to split at this point
    i.e. low gini/entropy, high infoGain
    '''
    
    def split(self):
        #are we a leaf node?
        if len(self.rows) == 0:
            raise ValueError('The node has no document feed, no more splitting')
        elif self.calc_gini_index() == 0:
            raise ValueError('The node is pure, no more splitting')
        elif self.depth == self.max_depth:
            raise ValueError('The node has reached max recursion depth, no more splitting')
        elif len(self.features) == 0:
            raise ValueError('There are no more features to split on.')
            
        #we are not a leaf node.
        min_gini, min_feature, min_break_point, left_members, right_members = 2, -999, -999, [], []
        bp_len_sum = 0
        for feature in self.features:
#             print('parsing')
            to_parse = [(self.data[feature][x],self.data[self.label_index][x]) for x in self.rows]
            to_parse = pd.DataFrame(to_parse, columns=(feature,self.label_index), index=self.rows)
#             print(to_parse)
            to_parse.sort_values(feature, inplace=True)
#             print(to_parse)
#             to_parse = self.data[[feature, self.label_index]]
#             to_parse = to_parse.loc[to_parse.index.isin (self.rows)]
#             to_parse.sort_values(feature, inplace=True)
#             print(to_parse)
            break_points = self.find_break_points(to_parse, feature)
#             print(break_points)
            bp_len_sum += len(break_points)

            best_gini_this_feature, best_breakpoint_this_feature = self.find_best_breakpoint(to_parse.values[:,0], to_parse.values[:,1])
            if best_gini_this_feature < min_gini:
                left_members = to_parse.loc[to_parse[feature] < best_breakpoint_this_feature].index.values
                right_members = to_parse.loc[to_parse[feature] >= best_breakpoint_this_feature].index.values
                min_gini, min_break_point, min_feature = best_gini_this_feature, best_breakpoint_this_feature, feature
        if bp_len_sum == 0:
            print(to_parse)
            print(self.calc_gini_index())
        #Node(self.data, , [x for x in self.features if x != feature], self.depth+1, self.max_depth)
        self.left = Node(self.data, left_members, [x for x in self.features if x != min_feature], self.depth+1, self.max_depth, parent=self.id, side='l')
        self.right = Node(self.data, right_members, [x for x in self.features if x != min_feature], self.depth+1, self.max_depth, parent=self.id, side='r')
        self.min_feature, self.min_break_point, self.min_gini = min_feature, min_break_point, min_gini
        try:
            if self.left is None:
                print(self.min_feature,self.min_break_point,self.min_gini)
            self.left.split()
        except ValueError: # probably need a customized error class
            pass
        try:
            self.right.split()
        except ValueError:
            pass
    
    '''
    A faster way to find the best breakpoint. 
    Note that we're assuming that the node we're splitting isn't pure.
    
    input:
    values - an arraylike of the values associated with each element
    classes - a arraylike of the labels for each element, in the same order as values
    
    returns:
    (min_gini, min_break_point)
    '''
#    def find_best_breakpoint(self, values, classes, feature):
    def find_best_breakpoint(self, values, classes):
        if len(values) != len(classes):
            raise ValueError("Values and classes must be the same length.")
        best_gini = 2
        best_ind = -1
        multiple_classes_same_value = False #deal with cases like 2/R,3/R,3/M,4/M
        #class member values
        left_members = {}
        right_members = {}
        #print('vals:{}'.format(values))
        #print('classes:{}'.format(classes))
        #everything starts on the right
        for i in range(len(values)):
            try:
                right_members[classes[i]] += 1
            except KeyError:
                right_members[classes[i]] = 1
                
        #compare different breakpoints
        for i in range(len(values)-1):
            #add ith value to the left (we're considering splitting after i)
            try:
                left_members[classes[i]] += 1
            except KeyError:
                left_members[classes[i]] = 1
            
            #remove ith value from the right 
            right_members[classes[i]] -= 1
            
            #if i and i+1 aren't the same class, consider splitting here
            diff_classes = classes[i] != classes[i+1]
            diff_vals = values[i] != values[i+1]
            if diff_vals and (diff_classes or multiple_classes_same_value):
                #l_g_test = Node(self.data, [x for x in self.rows if self.data[feature][x] <= values[i]], [x for x in self.features], self.depth+1, self.max_depth).calc_gini_index()
                #r_g_test = Node(self.data, [x for x in self.rows if self.data[feature][x] > values[i]], [x for x in self.features], self.depth+1, self.max_depth).calc_gini_index()
                left_gini = Node.calc_gini_from_props(left_members)
                right_gini = Node.calc_gini_from_props(right_members)
                #assert math.isclose(left_gini,l_g_test)
                #assert math.isclose(right_gini,r_g_test)
                curr_gini = Node.aggregate_gini(left_gini, right_gini, i+1, len(values)-(i+1))
                if best_gini > curr_gini:
                    best_gini = curr_gini
                    best_ind = i+1 #if we're less than the breakpoint, we're put in one bucket, and geq is in the other bucket
                multiple_classes_same_value = False
            elif (not diff_vals) and diff_classes:
                multiple_classes_same_value = True
        #return the best value
        return (best_gini, values[best_ind])
            
    '''
    Calculates the gini index from a dictionary of proportions
    
    input:
    members - a dict from string label to int count of members
    
    returns - the gini index for a node containing these members
    '''        
    def calc_gini_from_props(members):
        answer = 1
        total = 0
        for label in members.keys():
            total += members[label]
        for label in members.keys():
            answer -= (members[label]/total)**2
        return answer
    
    '''
    Calculates the aggregate gini index from two child nodes.
    
    input:
    score1 - the gini score for one child
    score2 - the gini score for the other child
    num1 - the number of members of the first child
    num2 - the number of members of the second child
    
    returns - a weighted average of the two scores
    '''
    def aggregate_gini(score1, score2, num1, num2):
        return (score1*num1 + score2*num2)/(num1 + num2)
    
    def __str__(self):
#         if self.left and self.right:
        children = [(x.side, x.id) for x in (self.left, self.right)] if self.left and self.right else []
        return "[{ID}, {Gini}, {Size}, {Feature}, {BP}, {Children}]".format(ID=self.id, 
                                                            Gini = self.calc_gini_index(),
                                                            Size = len(self.rows),
                                                            Feature=self.min_feature, 
                                                            BP=self.min_break_point,
                                                           Children=children)
#         else:
#             "[{ID}, (Children=None)]".format(ID=self.id)
    
    def get_proportions(self, target_label):
        members = [self.data[self.label_index][x] for x in self.rows]
        filtered = [x for x in members if x == target_label]
#         members = self.data.loc[self.data[self.label_index] == target_label]
#         filtered = [x for x in members.index.values if x in self.rows]
        raw_val = (len(filtered)/len(self.rows))
        return raw_val
        