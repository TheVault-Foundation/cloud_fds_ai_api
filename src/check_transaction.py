from bson.objectid import ObjectId
from bson import json_util

from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta

import traceback

from log import Log
from models import *
from fds import FDS

from flask import jsonify


class CheckTransaction:
    def __init__(self, tokenDoc, reqData):
        self.tokenDoc = tokenDoc
        self.reqData = reqData
        self.transaction = Transaction()

    def isDataValid(self):
        if not self.tokenDoc or not self.reqData:
            return False
        if not self.reqData.get('fromAddress', ''):
            return False
        if not self.reqData.get('fromCurrency', ''):
            return False
        if not self.reqData.get('toAddress', ''):
            return False
        if not self.reqData.get('amount', ''):
            return False

        self.transaction.userId = self.tokenDoc.getUserId()
        if not self.transaction.userId:
            return False

        self.transaction.fromAddress = self.reqData.get('fromAddress', '')
        self.transaction.fromCurrency = self.reqData.get('fromCurrency', '')
        self.transaction.toAddress = self.reqData.get('toAddress', '')
        self.transaction.toCurrency = self.reqData.get('toCurrency', self.transaction.fromCurrency)
        self.transaction.amount = float(self.reqData.get('amount', '0.0'))
        if self.transaction.amount <= 0.0:
            return False
        
        self.transaction.senderDeviceId = int(self.reqData.get('senderDeviceId', '0'))

        if self.reqData.get('senderIp', ''):
            self.transaction.senderIp = self.reqData.get('senderIp', '')
            self.transaction.country = self.findCountry(self.transaction.senderIp)

        self.transaction.transactedAt = datetime.strptime(self.reqData.get('transactedAt', ''), '%Y%m%dT%H%M%S')

        return True


    def findCountry(self, ipAddr):
        try:
            ipArray = ipAddr.split('.')

            # 1.2.3.4 = 4 + (3 * 256) + (2 * 256 * 256) + (1 * 256 * 256 * 256) is 4 + 768 + 13,1072 + 16,777,216 = 16,909,060
            ipVal = 0
            for i in range(4):
                ipVal += int(ipArray[i]) * 256**(3-i)

            ipDoc = IpToCountry.objects.get(ipFrom__lte=ipVal, ipTo__gte=ipVal)
            return ipDoc.country

        except:
            Log.error(traceback.format_exc())
            return 


    def saveTransaction(self):
        if self.transaction:
            self.transaction.save()


    def increaseAPIUsageCount(self):
        curUtc = datetime.utcnow()

        year = curUtc.year
        month = curUtc.month

        ApiUsageCount.objects(apiId=self.tokenDoc.apiId, year=year, month=month).update_one(inc__count=1, upsert=True)


    def process(self):
        if not self.isDataValid():
            return { 
                'request': self.reqData,
                'error': 'Invalid data.'
            }, 400

        # self.saveTransaction()

        fds = FDS(self.transaction)
        self.transaction.score = fds.getScore()
        self.saveTransaction()

        self.increaseAPIUsageCount()
                
        return jsonify({ 
            'transaction': self.reqData,
            'score': self.transaction.score
        }), 200