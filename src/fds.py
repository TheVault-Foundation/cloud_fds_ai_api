from log import Log
from models import *

from isolationForest import isolationForest

import random


class FDS:
    
    def __init__(self, transaction):
        Log.debug('FDS::__init__()')

        self.transaction = self.convertData(transaction)

        self.transHistory = []
        for trans in transaction.getAllHistory():
            data = self.convertData(trans)
            self.transHistory.append(data)

        self.isolationForest = isolationForest(self.transHistory)

    
    def convertData(self, transaction):
        # Log.debug('isolationForest::convertData()')

        data = []
        data.append(FDSAddress.getId(transaction.fromAddress, transaction.fromCurrency))
        data.append(FDSAddress.getId(transaction.toAddress, transaction.toCurrency))
        data.append(transaction.senderDeviceId)
        data.append(float(transaction.amount))

        for elem in data:
            print(elem, end=' ')                
        print()

        return data
    

    def getScore(self, transaction=None):
        Log.debug('FDS::getScore()')
        
        # return random.randint(0, 100)
        # print(self.transHistory)
        # print(str(len(self.transHistory)))
        if len(self.transHistory) < 2:
            return 0
        
        if transaction:
            return self.isolationForest.getScore(transaction)
        else:
            return self.isolationForest.getScore(self.transaction)





if __name__ == "__main__":
    fds = FDS('')

    score = fds.getScore()

    print(score)