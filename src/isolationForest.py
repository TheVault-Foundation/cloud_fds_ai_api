import pandas as pd 
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import itertools
import matplotlib.pyplot as plt
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

from nltk.probability import FreqDist

import random

from log import Log
from models import *


class isolationForest:
    
    def __init__(self, transHistory):
        Log.debug('isolationForest::__init__()')

        self.clf = IsolationForest(behaviour='new', random_state=np.random.RandomState(42), contamination="auto")

        npArray = np.asarray(transHistory)
        self.clf.fit(npArray.reshape(-1, 4))
        
        # pca = PCA()
        # pcaData = pca.fit(npArray)
        # self.clf.fit(pca.components_.T.reshape(-1, 4))

    
    def getScore(self, transaction):
        Log.debug('isolationForest::getScore()')

        score = self.clf.score_samples(np.asarray(transaction).reshape(1, 4))[0]

        return abs(score) * 100



if __name__ == "__main__":
    fds = isolationForest('')

    score = fds.getScore()

    print(score)