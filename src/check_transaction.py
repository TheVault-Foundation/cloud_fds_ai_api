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
            ipDoc = IpToCountry.findCountry(self.transaction.senderIp)
            if ipDoc:
                self.transaction.country = ipDoc.ctry

        self.transaction.transactedAt = datetime.strptime(self.reqData.get('transactedAt', ''), '%Y%m%dT%H%M%S')

        return True


    def saveTransaction(self):
        if self.transaction:
            self.transaction.save()


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

        ApiUsageCount.increaseCount(self.tokenDoc.apiId)
                
        return jsonify({ 
            'transaction': self.reqData,
            'score': self.transaction.score
        }), 200