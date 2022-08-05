import numpy as np
from scipy import stats

class RTLearner:
    def __init__(self, leaf_size=1, verbose=False):
        self.leafsize = leaf_size
        self.tree = None

    def query(self, Xtest):
        soln = np.zeros(Xtest.shape[0])
        for i in range(Xtest.shape[0]):
            soln[i] = self.traverse_tree(Xtest[i,:])
        return soln

    def traverse_tree(self, Xtest):
        index = 0
        while(self.tree[index,0] != -1):
            index = int(index)
            factor = int(self.tree[index,0])
            splitval = self.tree[index,1]
            left = int(self.tree[index,2])
            right = int(self.tree[index,3])
            if(float(Xtest[factor]) <= splitval):
                index = index + left
            else:
                index = index + right
        return self.tree[index][1]
    
    def build_tree(self, data):
        if data.shape[0] <= self.leafsize:
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])
        yColumn = data[:,-1]
        if np.unique(yColumn.size == 1):
            return np.array([[-1, yColumn[0, -1], np.nan, np.nan]])
        else:
            index = int(self.calculate_random(data))
            SplitVal = np.median(data[:, index])
            if SplitVal == max(data[:, index]):
                return np.array([[-1,  np.mean(data[:, -1]), np.nan, np.nan]])
            lefttree = self.build_tree(data[data[:,index]<=SplitVal])
            righttree = self.build_tree(data[data[:,index]>SplitVal])
            root = np.array([[index, SplitVal, 1, lefttree.shape[0] + 1]])
            halfTree = np.append(root, lefttree, axis=0)
            fullTree = np.append(halfTree, righttree, axis=0)
            return fullTree

    def add_evidence(self, Xtrain, Ytrain):
        Xtrain1 = Xtrain
        Ytrain1 = np.array([Ytrain])
        Ytrain_transpose = Ytrain1.T
        data = np.append(Xtrain1, Ytrain_transpose, axis=1)
        self.tree = self.build_tree(data)

    def calculate_random(self, data):
        return np.random.randint(0, data.shape[1]-2)

    def author(self):
            return "vgupta359"


            