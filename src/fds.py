from log import Log
from models import *

from isolationForest import isolationForest

import random
import math


MIN_SAMPLE_COUNT = 2

HOUR_GROUP = [ 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2 ]

class FDS:
    
    def __init__(self, transaction):
        Log.debug('FDS::__init__()')

        self.preCreatedAt = None

        self.transHistory = []
        for trans in transaction.getAllHistory():
            data = self.convertData(trans)
            self.transHistory.append(data)
            
        self.transaction = self.convertData(transaction)

        self.transHistory.append(self.transaction) # Important!!

        if len(self.transHistory) >= MIN_SAMPLE_COUNT:
            self.isolationForest = isolationForest(self.transHistory)

    
    def convertData(self, transaction):
        # Log.debug('isolationForest::convertData()')

        data = []
        data.append(FDSAddress.getId(transaction.fromAddress, transaction.fromCurrency))
        data.append(FDSAddress.getId(transaction.toAddress, transaction.toCurrency))
        
        data.append(float(transaction.amount))
        data.append(transaction.senderDeviceId)

        if transaction.transactedAt:
            data.append(HOUR_GROUP[transaction.transactedAt.hour])
        else:
            data.append(0)
            
        if transaction.country:
            data.append(ord(transaction.country[0])*256 + ord(transaction.country[1]))
        else:
            data.append(0)
        
        if self.preCreatedAt:
            data.append(math.floor((transaction.createdAt - self.preCreatedAt).total_seconds()/3600))
        else:
            data.append(0)
        
        self.preCreatedAt = transaction.createdAt

        for elem in data:
            print(elem, end=' ')                
        print()

        return data
    

    def getScore(self, transaction=None):
        Log.debug('FDS::getScore()')
        
        # return random.randint(0, 100)
        # print(self.transHistory)
        # print(str(len(self.transHistory)))
        if len(self.transHistory) < MIN_SAMPLE_COUNT:
            return 0
        
        if transaction:
            return self.isolationForest.getScore(transaction)
        elif self.transaction:
            return self.isolationForest.getScore(self.transaction)
        else:
            return 0





if __name__ == "__main__":
    fds = FDS('')

    score = fds.getScore()

    print(score)