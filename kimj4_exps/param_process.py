import os
import pprint

directory_in_str = '../data/params/param/'
directory = os.fsencode(directory_in_str)

param_metrics_dict = {}

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        # print(os.path.join(directory, filename))
        # print(directory_in_str + filename)
        precision = 0
        recall = 0
        accuracy = 0
        f1 = 0
        fit_time = 0
        predict_time = 0
        with open(directory_in_str + filename, 'r') as f:
            # print(filename.split('.txt')[0])
            for line in f:
                if 'average' in line:
                    if 'precision' in line:
                        precision = float(line.split()[-1])
                    elif 'recall' in line:
                        recall = float(line.split()[-1])
                    elif 'accuracy' in line:
                        accuracy = float(line.split()[-1])
                    elif 'f1' in line:
                        f1 = float(line.split()[-1])
                    elif 'fit time' in line:
                        fit_time = float(line.split()[-1])
                    elif 'predict_time' in line:
                        predict_time = float(line.split()[-1])
                    else:
                        a = 1

                    # print(line.split()[-1], end='\n')
        param_metrics_dict[filename.split('.txt')[0]] = (precision, recall, accuracy, f1, fit_time, predict_time)
        # print('{}, {}, {}, {}, {}, {}'.format(precision, recall, accuracy, f1, fit_time, predict_time))
        continue
    else:
        continue

#get the sum of precision, acc, etc and the total number of occurrences to calculate averages by # of trees
# tree_totals = {}
# tree_nums = {}
# print('yo')
pp = pprint.PrettyPrinter()
# pp.pprint(param_metrics_dict)
# for key in param_metrics_dict.keys():
#     num_trees = key.split('.')[0]
#     try:
#         tree_totals[num_trees] = tuple(map(sum, zip(tree_totals[num_trees], param_metrics_dict[key])))
#         tree_nums[num_trees] += 1
#     except KeyError:
#         tree_totals[num_trees]  = param_metrics_dict[key]
#         tree_nums[num_trees] = 1
# pp.pprint(tree_totals)
# pp.pprint(tree_nums)
# for key in sorted(tree_totals.keys(), key=lambda x: int(x)):
#     av = tuple(map(lambda x: float(x)/tree_nums[key], tree_totals[key]))
#     print('{} Trees:-------------------------'.format(key))
#     print('Precision {}\n recall {}\n accuracy {}\n f1 {}\n fit time {}\n predicttime {}'.format(*av))

#find best f1 score
score_tuples = []
for key in param_metrics_dict.keys():
    score_tuples.append((key, *param_metrics_dict[key]))    
print('Trees,tree_depth,features,precision,recall,accuracy,f1,fit_time')
for setting in score_tuples:
    # print('{}'.format(setting[0]))    
    # print('precision {}\n recall {}\n accuracy {}\n f1 {}\n fit time {}\n predicttime {}'.format(*setting[1:]))
    settings = (setting[0].split('.'))
    print('{},{},{},{},{},{},{},{}'.format(*(*settings, *setting[1:6])))