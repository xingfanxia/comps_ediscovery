



# The following is from "big run"
import sys
sys.path.append('..')
from lib import *
import pandas as pd
import numpy as np
import time


def one_run(df, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features, folds, filename):
    '''Do n-fold crossvalidation for a forest built with some set of params'''
    df = df.sample(frac=1) #shuffling
    foldsize = df.shape[0] // folds
    fold_stats = []
    for fold in range(1, folds + 1):
        test_set = df[(fold - 1) * foldsize : fold * foldsize]
        test_set = test_set.reset_index(drop=True)
        
        train_set = df[:(fold - 1) * foldsize].append(df[fold * foldsize:])
        train_set = train_set.reset_index(drop=True)
        
        forest = RNF(train_set, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features)

        start = time.time()
        forest.fit_parallel()
        end = time.time()
        fit_time = end - start
        
        start = time.time()
        predictions = forest.predict_parallel(test_set)[1]
        end = time.time()

        prediction_time = end - start

        stats = list(evalStats(predictions, test_set))
        stats.append(fit_time)
        stats.append(prediction_time)
        fold_stats.append(stats)
    
    with open(filename, 'w') as f:
        for stat in fold_stats:
            f.write("\n" + str(stat))
        fold_stats = np.array(fold_stats, dtype=np.float64)
        f.write("\naverage precision: {}\n".format(np.mean(fold_stats[:, 0], dtype=np.float64)))
        f.write("average recall: {}\n".format(np.mean(fold_stats[:, 1], dtype=np.float64)))
        f.write("average accuracy: {}\n".format(np.mean(fold_stats[:, 2], dtype=np.float64)))
        f.write("average f1: {}\n".format(np.mean(fold_stats[:, 3], dtype=np.float64)))
        f.write("average fit time: {}\n".format(np.mean(fold_stats[:, 4], dtype=np.float64)))
        f.write("average prediction time: {}\n".format(np.mean(fold_stats[:, 5], dtype=np.float64)))
        
        
    




# Setup
lsa_np = np.load('../data/parsed/lsa_output.npy')
metadata = pd.read_pickle('../data/parsed/pickles/pickled_data_test.pickle')
metadata = metadata.loc[metadata['Scenario'] == '401']
metadata = metadata.reset_index(drop=True)
lsa_df = pd.DataFrame(lsa_np)
df = pd.concat([metadata, lsa_df], axis=1, join_axes=[metadata.index])
df = df.loc[df['Label'] != '-1']
df = df.reset_index(drop=True)
cat_features = ['To','From']
features = list(range(100))
features.extend(cat_features + ['Date'])

df = df[features + ['Label'] + ['ID']]


random_seed = 42
n_max_input = 600
folds = 10

print("setup is done")



# prototyping for making multiple one_run calls
log_filename = 'log.txt'
# def one_run(df, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features, folds, filename):
for n_trees in [64, 128, 256]:
    for tree_depth in [70, 95]:
        for n_max_features in [90, 95]:
            # things to test on:
            # number of trees, tree_depth, n_max_features
            try:
                filename = 'param/{}.{}.{}.txt'.format(n_trees, tree_depth, n_max_features)
                one_run(df, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features, folds, filename)
                print("{} is done".format(filename))
            except KeyboardInterrupt as e:
                sys.exit()
            except Exception as e:
                with open(log_filename, 'a') as f:
                    f.write(str(e))
                    print(e)
                continue