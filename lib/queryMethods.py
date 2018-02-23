import sys
sys.path.append('..')
from lib import *
import pandas as pd
import numpy as np

def regular_increment(df, n_trees, tree_depth, random_seed, n_max_features, cat_features):
    incremental_forest = RNF(df[0:100], n_trees, tree_depth, random_seed, n_max_features, 100, cat_features)
    incremental_forest.fit_parallel()
    print(evalStats(incremental_forest.predict_parallel(df[-100:])[1], df[-100:]))
    incremental_forest.update(df[100:200])
    print(evalStats(incremental_forest.predict_parallel(df[-100:])[1], df[-100:]))

    incremental_forest.update(df[200:300])
    print(evalStats(incremental_forest.predict_parallel(df[-100:])[1], df[-100:]))

    incremental_forest.update(df[300:400])
    print(evalStats(incremental_forest.predict_parallel(df[-100:])[1], df[-100:]))

    incremental_forest.update(df[400:500])
    print(evalStats(incremental_forest.predict_parallel(df[-100:])[1], df[-100:]))

    incremental_forest.update(df[500:600])
    print(evalStats(incremental_forest.predict_parallel(df[-100:])[1], df[-100:]))

def entropy(probs):
    s = 0
    for x in probs:
        if x != 0:
            s += x * math.log(x)
    return -1 * s

def committee_increment(df, n_trees, tree_depth, random_seed, n_max_features, cat_features):
    # initial training
    committee_rnf = RNF(df[:100], n_trees, tree_depth, random_seed, n_max_features, 100, cat_features)
    committee_rnf.fit_parallel()

    increment_size = 100

    test_set = df[-100:]
    train_set = df[:-100]

    labeled_ids = df.loc[:100, 'ID'].values
    #trying to use -100: with df.loc just returns everything, so we need to get a little tricky
    test_ids = df.iloc[-100:, df.columns.get_loc('ID')].values
    labeled_ids = np.append(labeled_ids, test_ids)
    test_results = committee_rnf.predict_parallel(df.loc[df['ID'].isin(test_ids)])
    print(evalStats(test_results[1], df.loc[df['ID'].isin(test_ids)]))
    for i in range(((df.shape[0] - 100) // increment_size) - 1):
        # initial train scores
        unlabeled_predict = committee_rnf.predict_parallel(df.loc[np.logical_not(df['ID'].isin(labeled_ids))])

        # to_label = sorted(map(entropy, zip(unlabeled_predict[0], unlabeled_predict[2])), reverse=True)[:increment_size]
        to_label = sorted(zip(map(entropy, unlabeled_predict[0]), unlabeled_predict[2]), reverse=True)[:increment_size]

        to_label_ids = [x[1] for x in to_label]

        labeled_ids = np.append(labeled_ids, to_label_ids)

        increment_df = df.loc[df["ID"].isin(to_label_ids)]

        committee_rnf.update(increment_df)

        test_results = committee_rnf.predict_parallel(df.loc[df['ID'].isin(test_ids)])
        print(evalStats(test_results[1], df.loc[df['ID'].isin(test_ids)]))

def committee_increment_copy(df, n_trees, tree_depth, random_seed, n_max_features, cat_features):
    # initial training
    committee_rnf = RNF(df[:100], n_trees, tree_depth, random_seed, n_max_features, 100, cat_features)
    committee_rnf.fit_parallel()

    increment_size = 50

    test_set = df[-100:]
    train_set = df[:-100]

    print('Initial performance')
    print(evalStats(committee_rnf.predict_parallel(test_set)[1], test_set))

    for i in range(5):
        to_predict_on = train_set[~train_set['ID'].isin(committee_rnf.train_data['ID'])].dropna()
        print('the effective size of the train_set is {}'.format(to_predict_on.shape[0]))
        predictions = committee_rnf.predict_parallel(to_predict_on)

        # least_agreement = sorted(zip(predictions[0], predictions[2]), key= lambda x: entropy(x), reverse=True)[:100]
        least_agreement = sorted(zip(map(entropy, predictions[0]), predictions[2]), reverse=True)[:100]
        least_agreement_ids = [x[1] for x in least_agreement]
#         print(most_confident_ids)
        incrementing_set = train_set[train_set['ID'].isin(least_agreement_ids)]
        committee_rnf.update(incrementing_set)
        print(evalStats(committee_rnf.predict_parallel(test_set)[1], test_set))


def homogeneous_increment(df, n_trees, tree_depth, random_seed, n_max_features, cat_features):
    '''Incremental training, but tries to give data points that even out the proportions of relevant vs not relevant
        rows that the forest has'''
    homogenous_rnf = RNF(df[:100], n_trees, tree_depth, random_seed, n_max_features, 100, cat_features)
    homogenous_rnf.fit_parallel()

    labeled_ids = df.loc[:100, 'ID'].values
    #trying to use -100: with df.loc just returns everything, so we need to get a little tricky
    test_ids = df.iloc[-100:, df.columns.get_loc('ID')].values
    labeled_ids = np.append(labeled_ids, test_ids)
    test_results = homogenous_rnf.predict_parallel(df.loc[df['ID'].isin(test_ids)])
    print(evalStats(test_results[1], df.loc[df['ID'].isin(test_ids)]))

    # incremental steps
    for i in range(5):
        # add 100 rows at each increment
        num_new_rows = 100

        # get ratio in the forest's training data
        num_relevant = homogenous_rnf.train_data[homogenous_rnf.train_data['Label']=='1'].shape[0]
        num_irrelevant = homogenous_rnf.train_data[homogenous_rnf.train_data['Label']=='0'].shape[0]
#         print('forest has {} relevant and {} irrelevant docs in the training set'.format(num_relevant, num_irrelevant))

        # look at the distribution of new data points
        if (num_irrelevant > num_relevant):
#             print('here1')
            # need to supplement relevant docs
            difference = num_irrelevant - num_relevant
            num_new_rel = difference + (num_new_rows - difference) // 2
            num_new_irr = num_new_rows - num_new_rel
        elif (num_relevant > num_irrelevant):
#             print('here2')
            difference = num_relevant - num_irrelevant
            num_new_irr = difference + (num_new_rows - difference) // 2
            num_new_rel = num_new_rows - num_new_irr
        else:
#             print('here3')
            num_new_irr = num_new_rows // 2
            num_new_rel = num_new_rows - num_new_irr
#         print('rel rows added: {}, irr rows added: {}'.format(num_new_rel, num_new_irr))

        # predict on all of the rest of the training set that hasn't been added to the forest
#         unlabeled_predict = committee_rnf.predict_parallel(df.loc[np.logical_not(df['ID'].isin(labeled_ids))])
        not_yet_labeled = df.loc[np.logical_not(df['ID'].isin(labeled_ids))]
        not_yet_labeled_rel = not_yet_labeled[not_yet_labeled['Label'] == '1']
        not_yet_labeled_irr = not_yet_labeled[not_yet_labeled['Label'] == '0']

        if not not_yet_labeled_rel.shape[0] >= num_new_rel:
            continue
        elif not not_yet_labeled_irr.shape[0] >= num_new_irr:
            continue
        else:
#             to_add = .append(not_yet_labeled_rel, not_yet_labeled_irr)
            rel_to_add = not_yet_labeled_rel[:num_new_rel]
            irr_to_add = not_yet_labeled_irr[:num_new_irr]
            to_add = rel_to_add.append(irr_to_add)
            to_add_ids = to_add['ID'].values

            homogenous_rnf.update(to_add)
            test_results = homogenous_rnf.predict_parallel(df.loc[df['ID'].isin(test_ids)])
            print(evalStats(test_results[1], df.loc[df['ID'].isin(test_ids)]))
            labeled_ids = np.append(labeled_ids, to_add_ids)


def most_confident_increment(df, n_trees, tree_depth, random_seed, n_max_features, cat_features):
    '''
    Increments by 100 each run. Takes the 100 most confident data points to use add to the training set
    '''
    mc_rnf = RNF(df[:100], n_trees, tree_depth, random_seed, n_max_features, 100, cat_features)
    mc_rnf.fit_parallel()

    test_set = df[-100:]
    train_set = df[:-100]

    print(evalStats(mc_rnf.predict_parallel(test_set)[1], test_set))

    for i in range(5):
        to_predict_on = train_set[~train_set['ID'].isin(mc_rnf.train_data['ID'])].dropna()
        predictions = mc_rnf.predict_parallel(to_predict_on)

        most_confident = sorted(zip(predictions[0], predictions[2]), key= lambda x: abs(x[0][1] - x[0][0]), reverse=True)[:100]
        most_confident_ids = [x[1] for x in most_confident]
#         print(most_confident_ids)
        incrementing_set = train_set[train_set['ID'].isin(most_confident_ids)]
        mc_rnf.update(incrementing_set)
        print(evalStats(mc_rnf.predict_parallel(test_set)[1], test_set))


def non_incremental(df, n_trees, tree_depth, random_seed, n_max_features, cat_features):
    forest_100 = RNF(df[:100], n_trees, tree_depth, random_seed, n_max_features, 100, cat_features)
    forest_200 = RNF(df[:200], n_trees, tree_depth, random_seed, n_max_features, 200, cat_features)
    forest_300 = RNF(df[:300], n_trees, tree_depth, random_seed, n_max_features, 300, cat_features)
    forest_400 = RNF(df[:400], n_trees, tree_depth, random_seed, n_max_features, 400, cat_features)
    forest_500 = RNF(df[:500], n_trees, tree_depth, random_seed, n_max_features, 500, cat_features)
    forest_600 = RNF(df[:600], n_trees, tree_depth, random_seed, n_max_features, 600, cat_features)
    incremental_forests = [forest_100, forest_200, forest_300, forest_400, forest_500, forest_600]
    for forest in incremental_forests:
        forest.fit_parallel()
        print(evalStats(forest.predict_parallel(df[-100:])[1], df[-100:]), end='\n')
