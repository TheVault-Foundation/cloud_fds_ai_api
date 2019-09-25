from datetime import datetime

import traceback
import sys 
# sys.path.append('../config')

import config
from log import Log

from bson.objectid import ObjectId

from mongoengine import *
connect(config.MONGO_DB["NAME"], host=config.MONGO_DB["HOST"], port=config.MONGO_DB["PORT"], username=config.MONGO_DB["USERNAME"], password=config.MONGO_DB["PASSWORD"])


class User(Document):
    username = StringField(required=True, unique=True, max_length=100)
    password = StringField(required=True, max_length=100)
    company = StringField(max_length=100)
    email = StringField(required=True, max_length=100)
    contactNumber = StringField(max_length=100)
    address = StringField(max_length=200)
    billingType = ObjectIdField()
    emailVerified = BooleanField(required=True, default=False)
    roleType = StringField(required=True, default="User", regex=r'^(Admin|User)$')
    isActive = BooleanField(required=True, default=True)
    lastSignin = DateTimeField()
    createdAt = DateTimeField(required=True, default = datetime.utcnow)
    createdBy = StringField(required=True)
    updatedAt = DateTimeField()
    updatedBy = StringField(max_length=100)
    
    meta = {
        'collection': 'user',
        'indexes': [
            'username',
            'email',
            '-createdAt'
        ]
    }


class UserAccessToken(Document):
    userId = ObjectIdField(required=True)
    accessToken = StringField(required=True, max_length=300)
    expireAt = DateTimeField(required=True)
    CreatedAt = DateTimeField(default = datetime.utcnow)

    meta = {
        'collection': 'userAccessToken',
        'indexes': [
            'userId',
            '-accessToken',
            'expireAt'
        ]
    }

    
class UserApi(Document):
    userId = ObjectIdField(required=True)
    apiKey = StringField(required=True, unique=True, max_length=100)
    apiSecret = StringField(required=True, max_length=300)
    isActive = BooleanField(required=True, default=True)
    createdAt = DateTimeField(required=True, default = datetime.utcnow)
    createdBy = StringField(required=True, max_length=100)
    updatedAt = DateTimeField()
    updatedBy = StringField(max_length=100)
    
    meta = {
        'collection': 'userApi',
        'indexes': [
            'userId',
            'apiKey',
            '-createdAt'
        ]
    }


class ApiUsageCount(Document):
    apiId = ObjectIdField(required=True)
    year = IntField(required=True)
    month = IntField(required=True)
    count = IntField(required=True, default=0)
    
    meta = {
        'collection': 'apiUsageCount',
        'indexes': [
            'apiId',
            '-year',
            '-month'
        ]
    }

    @staticmethod
    def increaseCount(apiId):
        curUtc = datetime.utcnow()

        year = curUtc.year
        month = curUtc.month

        ApiUsageCount.objects(apiId=apiId, year=year, month=month).update_one(inc__count=1, upsert=True)


class Transaction(Document):
    userId = ObjectIdField(required=True)
    fromAddress = StringField(required=True, max_length=200)
    fromCurrency = StringField(required=True, max_length=20)
    toAddress = StringField(required=True, max_length=200)
    toCurrency = StringField(required=True, max_length=20)
    amount = DecimalField(required=True, precision=10)
    senderDeviceId = IntField(required=False)
    senderIp = StringField(required=False, max_length=20)
    country = StringField(required=False, max_length=20)
    transactedAt = DateTimeField(required=False)  #StringField(required=False, max_length=15)
    score = DecimalField(required=True, default=0)
    txHash = StringField(required=False, max_length=200)
    createdAt = DateTimeField(default = datetime.utcnow)
    updatedAt = DateTimeField()
    updatedBy = StringField(max_length=100)
    
    meta = {
        'collection': 'transactions',
        'indexes': [
            'userId',
            'fromAddress',
            'fromCurrency',
            '-transactedAt',
            '-createdAt',
            'score'
        ]
    }

    def getAllHistory(self):
        try:
            trans = Transaction.objects(fromAddress = self.fromAddress, fromCurrency = self.fromCurrency).order_by('createdAt')
            if trans:
                return trans

            return Transaction.objects(userId = self.userId).order_by('createdAt')

        except:
            Log.error(traceback.format_exc())
            return None


class DeviceType(Document):
    deviceId = IntField(required=True)
    deviceType = StringField(required=True, max_length=50)
    
    meta = {'collection': 'deviceType'}

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by('deviceId')


class ApiSessionToken(Document):
    apiId = ObjectIdField(required=True)
    sessionToken = StringField(required=True, max_length=200)
    expireAt = DateTimeField(required=True)
    CreatedAt = DateTimeField(default = datetime.utcnow)

    meta = {
        'collection': 'apiSessionToken',
        'indexes': [
            'apiId',
            '-sessionToken',
            'expireAt'
        ]
    }

    def getUserId(self):
        try:
            api = UserApi.objects.get(id=ObjectId(self.apiId))
            return api.userId
        except:
            Log.error(traceback.format_exc())
            return None


class UserInvoice(Document):
    userId = ObjectIdField(required=True)
    invoiceAmount = DecimalField(required=True, default=0)
    paidAmount = DecimalField(required=True, default=0)
    createdAt = DateTimeField(default = datetime.utcnow)
    paidAt = DateTimeField()
    paymentDetail = StringField()
    
    meta = {
        'collection': 'userInvoice',
        'indexes': [
            'userId',
            '-createdAt',
            '-paidAt'
        ]
    }


class BillingType(Document):
    billingType = StringField(required=True, regex=r'^(Monthly|Metered)$', unique=True)
    
    meta = {'collection': 'billingType'}


class IpToCountry(Document):
    ipFrom = IntField(required=True)
    ipTo = IntField(required=True)
    registry = StringField(required=False, max_length=50)
    assigned = DateTimeField(required=False)
    ctry = StringField(required=True, max_length=20)
    cntry = StringField(required=True, max_length=20)
    country = StringField(required=True, max_length=50)
    
    meta = {
        'collection': 'ipToCountry',
        'indexes': [
            'ipFrom',
            'ipTo',
            'ctry',
            'country'
        ]
    }

    @staticmethod
    def findCountry(ipAddr):
        try:
            ipArray = ipAddr.split('.')

            # 1.2.3.4 = 4 + (3 * 256) + (2 * 256 * 256) + (1 * 256 * 256 * 256) is 4 + 768 + 13,1072 + 16,777,216 = 16,909,060
            ipVal = 0
            for i in range(4):
                ipVal += int(ipArray[i]) * 256**(3-i)

            return IpToCountry.objects.get(ipFrom__lte=ipVal, ipTo__gte=ipVal)

        except:
            Log.error(traceback.format_exc())
            return 

class IpToCountryTmp(Document):
    ipFrom = IntField(required=True)
    ipTo = IntField(required=True)
    registry = StringField(required=False, max_length=50)
    assigned = DateTimeField(required=False)
    ctry = StringField(required=True, max_length=20)
    cntry = StringField(required=True, max_length=20)
    country = StringField(required=True, max_length=50)
    
    meta = {
        'collection': 'ipToCountry_tmp',
        'indexes': [
            'ipFrom',
            'ipTo',
            'ctry',
            'country'
        ]
    }


class Seq(Document):
    name = StringField(required=True, unique=True, max_length=200)
    value = IntField(required=True, unique=True)
    
    meta = {
        'collection': 'sequence',
        'indexes': [
            'name'
        ]
    }

    @staticmethod
    def getNextValue(seqName):
        doc = Seq.objects(name=seqName).modify(
                                        upsert=True, new=True,
                                        inc__value=1, 
                                        set__name=seqName)
        return doc.value
        


class FDSAddress(Document):
    addressId = IntField(required=True, unique=True)
    address = StringField(required=True, max_length=200)
    currency = StringField(required=True, max_length=20)
    
    meta = {
        'collection': 'fdsAddress',
        'indexes': [{
                'fields': ['address', 'currency']
            }
        ]
    }

    @staticmethod
    def getId(address, currency):
        # Log.info(address + ',' + currency)
        try:
            doc = FDSAddress.objects.get(address=address, currency=currency)
            return doc.addressId
        except:            
            doc = FDSAddress(addressId=Seq.getNextValue('fdsAddress'), address=address, currency=currency)
            doc.save()
            return doc.addressId

