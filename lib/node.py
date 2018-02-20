'''
A dummy version of tree nodes
'''
from lib.exceptions import *
import random
import numpy as np
import pandas as pd
import math
class Node:

    def __init__(self, data, rows, features, depth, max_depth, cat_features, parent_node, parent_id=None, side=None, user_input=False):
        self.left = None
        self.right = None
        self.data = data
        self.rows = rows
        self.features = features
        self.cat_features = cat_features
        if user_input:
            self.label_index = 'Relevant'
        else:
            self.label_index = 'Label'
        self.input_type = user_input
        self.labels = data[self.label_index].unique()
        self.spliting_feature_val = None
        self.id = random.randrange(10**9, 10**10)
        self.depth = depth
        self.max_depth = max_depth
        self.min_feature = None
        self.min_break_point = None
        self.min_gini = None
        self.parent_id = parent_id
        self.side = side
        self.cat_already_split_on = []
        self.proportions = {}
        self.parent_node = parent_node




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
        members = self.data.loc[self.rows][self.label_index].values
        for label in self.labels:
            filtered = members[members == label]
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


    def split_cat(self, feature):
        best_gini = 2
        best_address = None

        #TODO: do we need to calculate to_parse, or can we just do self.data.loc[self.rows]?
        to_parse = [(self.data[feature][x],self.data[self.label_index][x]) for x in self.rows]
        to_parse = pd.DataFrame(to_parse, columns=(feature,self.label_index), index=self.rows)

        #TODO: we might want to keep track of all members instead of just the firsts
        #TODO:fix
        uniques = sorted(list(set([address for email in to_parse[feature] for address in email])))
        #uniques = to_parse[feature].apply(lambda x: x[0]).unique()

        for address in uniques:
            if (feature, address) in self.cat_already_split_on:
                # this feature, address combo has already been split on, so move on to the next address.
                continue
            else:
                #'split' on that address
                #print(feature, address)
                #TODO:fix
                this_sender_rows = to_parse.loc[to_parse[feature].apply(lambda x: address in x)].index.values
                #this_sender_rows = to_parse.loc[to_parse[feature].apply(lambda x: x[0]) == address].index.values

                #other_sender_rows = to_parse.loc[to_parse[feature].apply(lambda x: x[0]) != address].index.values
                other_sender_rows = to_parse.loc[to_parse[feature].apply(lambda x: address not in x)].index.values

                #maybe a little sketch to not remove this feature?
                from_this_address = Node(self.data, this_sender_rows, self.features, self.depth + 1, self.max_depth, self.cat_features, self, user_input=self.input_type)
                from_other_address = Node(self.data, other_sender_rows, self.features, self.depth + 1, self.max_depth, self.cat_features, self, user_input=self.input_type)

                if len(this_sender_rows) <= 0 or len(other_sender_rows) <= 0:
                    continue

                #record gini value
                curr_gini = Node.aggregate_gini(from_this_address.calc_gini_index(), from_other_address.calc_gini_index(),
                                               len(from_this_address.rows), len(from_other_address.rows))

                #take the best gini value
                if curr_gini < best_gini:
                    best_gini = curr_gini
                    best_address = address

                    # TODO: these are for debugging, remove later:
                    best_left_rows = this_sender_rows
                    best_right_rows = other_sender_rows

        if best_address is None:
            print('when splitting categorically, no best address found: {}'.format(self.rows))
            raise SingleChildSplitException("No split points found for feature {}".format(feature))

#        print('\n')
#        print('split_cat: current feature: ' + feature)
#        print('split_cat: splitting on address: ' + best_address)
#        print('split_cat: num left: ' + str(len(best_left_rows)))
#        print('split_cat: num right: ' + str(len(best_right_rows)))
#        print('\n')
        return best_gini, best_address

    def split_num(self, feature):
        to_parse = [(self.data[feature][x],self.data[self.label_index][x]) for x in self.rows]
        to_parse = pd.DataFrame(to_parse, columns=(feature,self.label_index), index=self.rows)
        to_parse.sort_values(feature, inplace=True)
        # print('to_parse: {}'.format(to_parse))

        #I don't think we need to find breakpoints here since they go unused below...
        #break_points = self.find_break_points(to_parse, feature)
        # print('break points: {}'.format(break_points))
        return self.find_best_breakpoint(to_parse.values[:,0], to_parse.values[:,1])

    '''
    Choose the best feature to split at this point
    i.e. low gini/entropy, high infoGain
    '''
    def split(self):
        # Checking if the current node is a leaf
        '''
        if len(self.rows) == 0:
            raise ValueError('The node has no document feed, no more splitting')
        elif self.calc_gini_index() == 0:
            raise ValueError('The node is pure, no more splitting')
        elif self.depth == self.max_depth:
            raise ValueError('The node has reached max recursion depth, no more splitting')
        elif len(self.features) == 0:
            raise ValueError('There are no more features to split on.')
        '''

        if len(self.rows) == 0:
            return self
        elif self.calc_gini_index() == 0:
            return self
        elif self.depth == self.max_depth:
            return self
        elif len(self.features) == 0:
            return self

        # Proceed since the current node is not a leaf
        min_gini, min_feature, min_break_point, left_members, right_members = 2, -999, -999, [], []
        bp_len_sum = 0
        new_features = []
        try:
            for feature in self.features:
                members = self.data.loc[self.rows]
                if feature in self.cat_features:
                    best_gini_this_feature, best_breakpoint_this_feature = self.split_cat(feature)
                    if best_gini_this_feature < min_gini:
#                        print('best_breakpoint_this_feature: ' + best_breakpoint_this_feature)

                        left_members = members.loc[members[feature].apply(lambda x: best_breakpoint_this_feature in x)].index.values
                        right_members = members.loc[members[feature].apply(lambda x: best_breakpoint_this_feature not in x)].index.values
                        min_gini, min_break_point, min_feature = best_gini_this_feature, best_breakpoint_this_feature, feature

                        #If there are no more options for this feature, remove it from consideration for a child

                        #x = list(set([address for email in test[feature] for address in email]))
                        unique_left = list(set([address for email in self.data.loc[left_members][feature] for address in email]))
                        #unique_left = self.data.loc[left_members][feature].apply(lambda x: x[0]).unique()
                        unique_right = list(set([address for email in self.data.loc[right_members][feature] for address in email]))
                        #unique_right = self.data.loc[right_members][feature].apply(lambda x: x[0]).unique()
                        left_are_options = False
                        right_are_options = False

                        for unl in unique_left:
                            if unl not in self.cat_already_split_on and unl != best_breakpoint_this_feature:
                                left_are_options = True
                                break

                        for unr in unique_right:
                            if unr not in self.cat_already_split_on and unr != best_breakpoint_this_feature:
                                right_are_options = True
                                break

                        left_features = self.features if left_are_options else [x for x in self.features if x != min_feature]
                        right_features = self.features if right_are_options else [x for x in self.features if x != min_feature]

                else:
                    best_gini_this_feature, best_breakpoint_this_feature = self.split_num(feature)
                    # print('best gini: {} for feature {}'.format(best_gini_this_feature, feature))
                    if best_gini_this_feature < min_gini:
                        left_members = members.loc[members[feature] < best_breakpoint_this_feature].index.values
                        right_members = members.loc[members[feature] >= best_breakpoint_this_feature].index.values
                        min_gini, min_break_point, min_feature = best_gini_this_feature, best_breakpoint_this_feature, feature
                        left_features = [x for x in self.features if x != min_feature]
                        right_features = [x for x in self.features if x != min_feature]
        except SingleChildSplitException:
            raise ValueError("There are no more features to split on for this node.")

       # print('feature we used: {}'.format(min_feature))
       # print('features we might have used: {}'.format(self.features))
       # print('rows we have: {}'.format(self.rows))
       # print('Depth: {}'.format(self.depth))

        #if all rows are identical according to these features, there's no more splitting we can do
        if min_gini == 2:
            identical = True
            for feature in self.features:
                val = self.data[feature][self.rows[0]]
                for row in self.rows[1:]:
                    if val != self.data[feature][row]:
                        identical = False
            if identical:
                raise CannotDistinguishException("All of the rows remaining have the same values for all of the features remaining.")

        self.left = Node(self.data, left_members, left_features, self.depth+1, self.max_depth, self.cat_features, self, parent_id=self.id, side='l', user_input=self.input_type)
        self.right = Node(self.data, right_members, right_features, self.depth+1, self.max_depth, self.cat_features, self, parent_id=self.id, side='r', user_input=self.input_type)

        self.min_feature, self.min_break_point, self.min_gini = min_feature, min_break_point, min_gini

        # This is just setting the children's variable
        # TODO: do this more elegantly
        self.left.cat_already_split_on = self.cat_already_split_on
        self.right.cat_already_split_on = self.cat_already_split_on


        if min_feature in self.cat_features:
            # JK: keep track of the feature/address that you/parent split on.
            self.left.cat_already_split_on.append((min_feature, min_break_point))
            self.right.cat_already_split_on.append((min_feature, min_break_point))

        try:
            if self.left is None:
                print(self.min_feature,self.min_break_point,self.min_gini)
            self.left = self.left.split()
        except ValueError as e: # probably need a customized error class
            # TODO: use a separate exception class
            #print(e)
            pass
        try:
            self.right = self.right.split()
        except ValueError as e:
            # TODO: use a separate exception class
            #print(e)
            pass
        return self
    '''
    A faster way to find the best breakpoint.
    Note that we're assuming that the node we're splitting isn't pure.
    input:
    values - an arraylike of the values associated with each element (sorted)
    classes - a arraylike of the labels for each element, in the same order as values
    returns:
    (min_gini, min_break_point)
    '''
    def find_best_breakpoint(self, values, classes):
        if len(values) != len(classes):
            raise ValueError("Values and classes must be the same length.")
        best_gini = 2
        best_ind = -1

        unique_values, val_class_dict = Node.get_val_class_dict(values, classes)

        #class member values
        left_members = {}
        right_members = {}

        #everything starts on the right
        for i in range(len(values)):
            try:
                right_members[classes[i]] += 1
            except KeyError:
                right_members[classes[i]] = 1

        #compare different breakpoints
        for i in range(len(unique_values) - 1):
            val = unique_values[i]
            next_val = unique_values[i+1]
            for key in val_class_dict[val]:
                mems_with_val = val_class_dict[val][key]
                right_members[key] -= mems_with_val
                try:
                    left_members[key] += mems_with_val
                except KeyError:
                    left_members[key] = mems_with_val
            if not (len(val_class_dict[val]) == 1 and val_class_dict[val] == val_class_dict[next_val]):
                left_gini = Node.calc_gini_from_props(left_members)
                right_gini = Node.calc_gini_from_props(right_members)
                curr_gini = Node.aggregate_gini(left_gini, right_gini, i+1, len(values)-(i+1))
                # print('considering splitting at {}, with gini of {}'.format(i,curr_gini))
                if best_gini > curr_gini:
                    best_gini = curr_gini
                    best_ind = i+1 #if we're less than the breakpoint, we're put in one bucket, and geq is in the other bucket
        return (best_gini, unique_values[best_ind])

    '''
    Initial pass to build a structure like this:
    {value: {class1:count,class2:count}, value: {class1:count}}
    returns all unique values, as a sorted list, and the structure above.
    We assume that values are sorted, and classes are in the corresponding order.
    '''
    def get_val_class_dict(values, classes):
        if len(values) != len(classes):
            raise ValueError("Values and classes must be the same length.")
        uniq_vals = []
        val_class_dict = {}
        for i in range(len(values)):
            val = values[i]
            cl = classes[i]
            #add to the dict
            try:
                val_class_dict[val][cl] += 1
            except KeyError:
                try:
                    val_class_dict[val][cl] = 1
                except KeyError:
                    val_class_dict[val] = {cl: 1}
            #add to uniq_vals
            if len(uniq_vals) == 0 or uniq_vals[-1] != val:
                uniq_vals.append(val)
        return uniq_vals, val_class_dict

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
        try:
            return self.proportions[target_label]
        except KeyError:
#             print('I\'m a node and I have {} rows'.format(len(self.rows)))
            members = self.data.loc[self.rows][self.label_index].values
            
#             s = set(self.rows) - set(self.data.index)
#             if (len(s) > 0):
#                 print('the problem rows: {}'.format(s))
#                 print('data indices: {}'.format(sorted(self.data.index)))
#                 print('I am a node with {} rows'.format(len(self.data.index)))
#             else:
#                 print('I am a node with {} rows'.format(len(self.data.index)))

            filtered = [x for x in members if x == target_label]
    #         members = self.data.loc[self.data[self.label_index] == target_label]
    #         filtered = [x for x in members.index.values if x in self.rows]
            raw_val = (len(filtered)/len(self.rows))
            self.proportions[target_label] = raw_val
            return raw_val