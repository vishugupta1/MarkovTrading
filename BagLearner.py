import numpy as np

class BagLearner(object):
   
    def __init__ (self, learner, kwargs={"leaf_size":1}, bags=20, boost = False, verbose = False):
        self.learners = []
        self.bags = bags
        self.learner = learner 
        for i in range(0,bags):  
            self.learners.append(learner(**kwargs)) 
    
    def add_evidence(self, Xtrain, Ytrain):
        i = np.arange(0, Xtrain.shape[0]-1)
        for learner in self.learners:
            random = np.random.choice(i, i.size)
            X = Xtrain.take(random, axis = 0)
            Y = Ytrain.take(random, axis = 0)
            learner.add_evidence(X,Y)
    
    def query(self, Xtest):
        res = []
        for learner in self.learners:
            yPredict = learner.query(Xtest)
            res.append(yPredict)
        return np.mean(np.array(res), axis=0)

    def author(self):
        return "vgupta359"
    