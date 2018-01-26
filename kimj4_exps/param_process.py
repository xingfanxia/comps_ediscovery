import os

directory_in_str = '/home/juyun/param_test/param/'
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
            print(filename.split('.txt')[0])
            for line in f:
                if 'average' in line:
                    if 'precision' in line:
                        precision = line.split()[-1]
                    elif 'recall' in line:
                        recall = line.split()[-1]
                    elif 'accuracy' in line:
                        accuracy = line.split()[-1]
                    elif 'f1' in line:
                        f1 = line.split()[-1]
                    elif 'fit time' in line:
                        fit_time = line.split()[-1]
                    elif 'predict_time' in line:
                        predict_time = line.split()[-1]
                    else:
                        a = 1

                    # print(line.split()[-1], end='\n')
        param_metrics_dict[filename.split('.txt')[0]] = (precision, recall, accuracy, f1, fit_time, predict_time)
        # print('{}, {}, {}, {}, {}, {}'.format(precision, recall, accuracy, f1, fit_time, predict_time))
        continue
    else:
        continue
for val in param_metrics_dict.values():
    print(val)
