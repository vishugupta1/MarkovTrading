import BagLearner as bl
import LinRegLearner as lrl
import numpy as np
class InsaneLearner(object):
    def __init__ (self, verbose = False):
        self.learners = []
        self.verbose = verbose
        for i in range(20):
            self.learners.append(bl.BagLearner(lrl.LinRegLearner, kwargs={}, bags = 20, verbose = self.verbose))
    def add_evidence(self, Xtrain, Ytrain):
        for learner in self.learners:
            learner.add_evidence(Xtrain, Ytrain)
    def query(self, Xtest):
        res = np.empty((Xtest.shape[0],20))
        for i in range(20):
            res[:,i] = self.learners[i].query(Xtest)
        return res.mean(axis=1)
    def author(self): 
        return "vgupta359"

    