import sys
sys.path.append('..')
from lib import *
import pandas as pd
import numpy as np

#Input: lsa_output_datapath = datapath .npy saved LSA matrix, email_clean = dataframe containing cleaned email data
#Ouput: dataframe contaning LSA values and email data
#Combine LSA matrix and email data
def setup_dataframe(lsa_output_datapath, email_clean):
    lsa_np = np.load(lsa_output_datapath)
    lsa_df = pd.DataFrame(lsa_np)
    
    metadata = email_clean
    metadata = metadata.loc[metadata['Scenario'] == '401']
    metadata = metadata.reset_index(drop=True)
    
    full_df = pd.concat([metadata, lsa_df], axis=1, join_axes=[metadata.index])
    full_df = full_df.loc[df['Label'] != '-1']
    full_df = full_df.reset_index(drop=True)
    
    cat_features = ['To','From']
    features = list(range(100))
    features.extend(cat_features + ['Date'])
    full_df = full_df[features + ['Label']]
    
    return full_df


#Input: full_dataframe =  output from setup_dataframe()
#Output: None
#Use full dataframe to train tree and save it.
def train_tree(full_dataframe):
    n_trees = 64
    tree_depth = 10
    random_seed = 42
    n_max_features = 20
    n_max_input = train_df.shape[0]
    benchmark = None
    rows = range(df.shape[0])
    
    forest = RNF(train_df, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features)
    
    forest.fit()
    forest.store_rnf('scenario_1_full_train.pickle')
    


#Input: tree_datapath = trained tree, test_dataframe = output from setup_dataframe with test data
#Output: None
#Evaluate tree on test data
def test_tree(tree_datapath, test_dataframe):
    test_forest = RNF(None, None, None, None, None, None, None)
    test_forest.load_rnf('scenario_1_full_train.pickle') 
    test_forest.predict(test_dataframe)
    
    