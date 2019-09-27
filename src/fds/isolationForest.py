import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

import random
import math

from utils import Log
from model import *


class isolationForest:
    
    def __init__(self, transHistory):
        Log.debug('isolationForest::__init__()')
        
        self.transHistory = transHistory
        self.DATA_COL_COUNT = len(transHistory[0])

        self.clf = IsolationForest(behaviour='new', random_state=np.random.RandomState(42), contamination="auto")

        # npArray = np.asarray(transHistory)
        npArray = transHistory
        self.clf.fit(npArray.reshape(-1, self.DATA_COL_COUNT))
        
        # pca = PCA()
        # pca.fit(npArray)
        # self.clf.fit(pca.components_.T.reshape(-1, self.DATA_COL_COUNT))
        # print(pca.components_.T)

    
    def getScore(self, transaction):
        Log.debug('isolationForest::getScore()')

        # print(self.clf.decision_function(self.transHistory))
        # print(self.clf.score_samples(self.transHistory))

        score = self.clf.score_samples(np.asarray(transaction).reshape(1, self.DATA_COL_COUNT))[0]

        Log.info('score:' + str(score))
        return math.floor(abs(score) * 100)




if __name__ == "__main__":
    fds = isolationForest('')

    score = fds.getScore()

    print(score)