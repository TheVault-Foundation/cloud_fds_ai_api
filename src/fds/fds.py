from utils import Log
from model import *

from sklearn import preprocessing
import numpy as np

from .isolationForest import isolationForest
# from .autoEncoder import autoEncoder

import random
import math
import pandas as pd


MIN_SAMPLE_COUNT = 2

#              0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
HOUR_GROUP = [ 1, 1, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1 ]

class FDS:
    
    def __init__(self, transaction):
        Log.debug('FDS::__init__()')

        self.prevCreatedAt = None
        self.transHistory = []
        dbDocs = transaction.getAllHistory()
        if len(dbDocs) >= MIN_SAMPLE_COUNT:
            for trans in transaction.getAllHistory():
                data = self.convertTransaction(trans)
                self.transHistory.append(data)
                
            self.transaction = self.convertTransaction(transaction)
            self.transHistory.append(self.transaction) # Important!!

            df_norm = self.normalizeConvertedData()

            self.transaction = df_norm[-1]
            Log.debug('--------------------')
            Log.debug(self.transaction)

            self.isolationForest = isolationForest(df_norm)

    
    def convertTransaction(self, transaction):
        # Log.debug('isolationForest::convertData()')

        data = []
        data.append(FDSAddress.getId(transaction.fromAddress, transaction.fromCurrency))
        data.append(FDSAddress.getId(transaction.toAddress, transaction.toCurrency))
        
        data.append(float(transaction.amount)/100)
        data.append(transaction.senderDeviceId)

        if transaction.transactedAt:
            # data.append(HOUR_GROUP[transaction.transactedAt.hour])
            data.append(transaction.transactedAt.hour)
        else:
            data.append(0)
            
        if transaction.country:
            data.append(ord(transaction.country[0])*256 + ord(transaction.country[1]))
        else:
            data.append(0)
        
        if self.prevCreatedAt:
            data.append(math.floor((transaction.createdAt - self.prevCreatedAt).total_seconds()/3600))
        else:
            data.append(0)
        
        self.prevCreatedAt = transaction.createdAt

        for elem in data:
            print(elem, end=' ')                
        print()

        return data

    
    def normalizeConvertedData(self):
        # df = pd.DataFrame(self.transHistory)
        # print('-------------')
        # print(df)
        # print('-------------')
        # print(df.min())
        # print('-------------')
        # print(df.max())
        # print('-------------')
        # df_norm = ((df - df.min() ) / (df.max() - df.min() )).fillna(0)
        # print('-------------')
        # print(df_norm)

        scaled = preprocessing.scale(np.asarray(self.transHistory))
        Log.debug(scaled)

        return scaled
    

    def getScore(self):
        Log.debug('FDS::getScore()')
        
        if len(self.transHistory) < MIN_SAMPLE_COUNT:
            return 50
        
        return self.isolationForest.getScore(self.transaction)





if __name__ == "__main__":
    fds = FDS('')

    score = fds.getScore()

    print(score)