#### Forest.predict content linear processing edition
trees= [tree.predict(test_data) for tree in self.trees]
        scores = [ list() for doc in trees[0]]
        for doc in range(len(trees[0])):
            for tree in trees:
                scores[doc].append(tree[doc])
        probas = [self.some_majority_count_metric(score) for score in scores]
        classes = ['1' if proba[0] > proba[1] else '0'  for proba in probas]
        return probas, classes
####

#### Forest.predict content Multiprocessing edition
        # count cpus
        # cpu_count = multiprocessing.cpu_count()
        cpu_count = len(self.trees)
        pool = multiprocessing.Pool( cpu_count )
        tasks = []
        tNum = 0
        max_t = cpu_count

        for tree in self.trees:
            tasks.append( (test_data,) )

        results = []
        for i in range(len(self.trees)):
            #results.append( pool.apply_async(self.trees[i].predict, tasks[i]) )
            results.append( pool.apply_async(self.trees[i].predict, (test_data,)) )
        #for tree in self.trees:
        #   results.append( pool.apply_async(tree.predict, tasks[0]) )

        r = []
        for result in results:
            r.append(result.get())

        print("size of r: {}".format(len(r)))
        print("r[0] == r[1]?: {}".format(r[0] == r[1]))
        # print("THE FOLLOWING IS r:")
        # for a in r:
        #    print(a)
        #print ("len(test_data): {}".format(len(test_data)))
        #print ("len(r): {}".format(len(r)))
        # return
        trees = r

        
        #trees = [tree.predict(test_data) for tree in self.trees]
        print ("len(trees): {}".format(len(trees)))
        print ("trees == r : {}".format(trees == r))
        scores = [ list() for doc in trees[0]]
        for doc in range(len(trees[0])):
            for tree in trees:
                scores[doc].append(tree[doc])
        probas = [self.some_majority_count_metric(score) for score in scores]
        classes = ['1' if proba[0] > proba[1] else '0'  for proba in probas]
        return probas, classes
#### End multiprocessing

#### Forest.fit content Multiprocessing edition
if len(self.trees) != 0:
            raise AlreadyFitException('This forest has already been fit to the data')
        for i in range(self.n_trees):
            selected = self.random_select(self.train_data)
#             self, train_data, depth, benchmark, rows, features
            self.trees.append(Tree(self.train_data, self.tree_depth, 0, selected[0], selected[1], self.cat_features))

        # handling multiprocessing logic

        # count cpus
        # cpu_count = multiprocessing.cpu_count()
        cpu_count = len(self.trees)
        pool = multiprocessing.Pool( cpu_count )
        tasks = []
        tNum = 0
        max_t = cpu_count

        results = []
        for tree in self.trees:
            results.append( pool.apply_async(tree.fit) )

        r = []
        for result in results:
            r.append(result.get())

        print('done!')

#### End multiprocessing
