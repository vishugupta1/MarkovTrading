import math
import numpy as np
from scipy import stats
import pandas as pd

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

    # def gini_impurity():

    # def calculate_sub_tree(x_vector, y_vector):
    #     soln = [] # -1(sell), 0(hold), 1(buy)
    #     for i in x_vector.index:
    #         if 
    
    def gini_impurity(self, data):

        gini_impurities = []
        for column in range(0,data.shape[1]): # calculate gini impurity for each column
            average_adj = []
            average_adj_gini = []
            data_local = data[data[:, 0].argsort()]
            # calculate adjacent averages
            for row in range(1, data_local.shape[0]):
                avg = (data_local[row - 1, column] + data_local[row, column])/2
                average_adj.append(avg)
            
            # calculate lowest gini impurity out of column
            for j in range(len(average_adj)):
                # sell(-1), nothing(0), buy(1)
                true_case = [0,0,0] 
                false_case = [0,0,0]
                for k in range(0, data_local.shape[0]):
                    if data[k, column] < average_adj.get(j):
                        if data[k, -1] == -1:
                            true_case[0] = true_case[0] + 1
                        elif data[k, -1] == 0:
                            true_case[1] = true_case[1] + 1
                        if data[k, -1] == 1:
                            true_case[2] = true_case[2] + 1
                    else:
                        if data[k, -1] == -1:
                            false_case[0] = false_case[0] + 1
                        elif data[k, -1] == 0:
                            false_case[1] = false_case[1] + 1
                        if data[k, -1] == 1:
                            false_case[2] = false_case[2] + 1
                impurity_true = 1 - math.pow(true_case[0]/(true_case[0]+true_case[1]+true_case[2]),2) - math.pow(true_case[1]/(true_case[0]+true_case[1]+true_case[2]),2) - math.pow(true_case[2]/(true_case[0]+true_case[1]+true_case[2]),2)
                impurity_false = 1 - math.pow(false_case[0]/(false_case[0]+false_case[1]+false_case[2]),2) - math.pow(false_case[1]/(false_case[0]+false_case[1]+false_case[2]),2) - math.pow(false_case[2]/(false_case[0]+false_case[1]+false_case[2]),2)
                total_impurity = ((true_case[0] + true_case[1] + true_case[2]) / (true_case[0] + true_case[1] + true_case[2] + false_case[0] + false_case[1] + false_case[2])*impurity_true) + ((false_case[0] + false_case[1] + false_case[2]) / (true_case[0] + true_case[1] + true_case[2] + false_case[0] + false_case[1] + false_case[2])*impurity_false)
                average_adj_gini.append(total_impurity)
            min_value = min(average_adj_gini)
            gini_impurities.append([min_value, average_adj[average_adj_gini.index(min_value)]])
        
                            
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
        #print(pd.DataFrame(data))
        self.tree = self.build_tree(data)

    def calculate_random(self, data):
        return np.random.randint(0, data.shape[1]-2)

    def author(self):
            return "vgupta359"


# if __name__ =="__main__":
#     return 0


            