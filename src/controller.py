from bson.objectid import ObjectId
from bson import json_util

from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta

import traceback

from log import Log
from models import *

import json
from hashlib import sha256


class Controller:
    SESSION_TOKEN_LIFETIME = 86400  # 24 hours
    
    def __init__(self):
        pass
        # Log.info('__init__()')

    def generateSessionToken(self, api):
        curTime = datetime.utcnow()       ### UTC now()
        expireAt = curTime + timedelta(seconds=self.SESSION_TOKEN_LIFETIME)
        tokinObj = { 'id': api.id, 'key': api.apiKey, 'secret': api.apiSecret, 'expireAt': expireAt }

        token = sha256(json_util.dumps(tokinObj).encode('utf-8')).hexdigest()

        session = ApiSessionToken(
            apiId = api.id,
            sessionToken = token,
            expireAt = expireAt,
            CreatedAt = curTime
        )
        session.save()

        return session.sessionToken
        
    def isValidSessionToken(self, sessonToken):
        strippedToken = sessonToken.strip()
        if not strippedToken:
            return False

        Log.info(strippedToken)
        try:
            return ApiSessionToken.objects.get(sessionToken=strippedToken, expireAt__gt=datetime.utcnow)
        except:
            Log.error(traceback.format_exc())
            return False

    def authenticate(self, request):
        Log.info('authenticate()')
        # Log.info(request.form)

        try:
            apiKey = request.form.get('api_key', '')
            apiSecret = request.form.get('api_secret', '')

            # Log.info('apiKey: ' + apiKey)
            # Log.info('apiSecret: ' + apiSecret)

            api = UserApi.objects.get(apiKey=apiKey, apiSecret=apiSecret, isActive=True)
            sessionToken = self.generateSessionToken(api)

            return {
                'session_token': sessionToken,
                'lifetime': self.SESSION_TOKEN_LIFETIME
            }, 200            
        except DoesNotExist:
            return {
                "error": "Invalid api."
            }, 403
        except:
            Log.error(traceback.format_exc())
            return {
                "error": "An error occurred."
            }, 500

    def device(self, request):
        Log.info('device()')

        try:
            sessionToken = request.headers.get("Authentication", "")
            if self.isValidSessionToken(sessionToken):
                retList = []
                for d in DeviceType.objects:
                    retList.append({'device_id': d.deviceId, 'device_type': d.deviceType})
                
                return json.dumps(retList)

            else:
                return {
                    "error": "Invalid Authentication."
                }, 403
            
        except:
            Log.error(traceback.format_exc())
            return {
                "error": "An error occurred."
            }, 500


    def check(self, request):
        Log.info('check()')
        Log.info(request.data)

        try:
            sessionToken = request.headers.get("Authentication", "")
            tokenDoc = self.isValidSessionToken(sessionToken)
            if tokenDoc:
                reqData = request.data

                trans = Transaction(
                                userId = tokenDoc.getUserId(),
                                fromAddress = reqData.get('fromAddress', ''),
                                fromCurrency = reqData.get('fromCurrency', ''),
                                toAddress = reqData.get('toAddress', ''),
                                toCurrency = reqData.get('toCurrency', reqData.get('fromCurrency', '')),
                                amount = float(reqData.get('amount', '0.0')),
                                senderDeviceId = int(reqData.get('senderDeviceId', '')),
                                senderIp = reqData.get('senderIp', ''),
                                transactedAt = datetime.strptime(reqData.get('transactedAt', ''), '%Y%m%dT%H%M')
                )
                trans.save()
                
                return { 
                    'request': reqData,
                    'score': trans.score
                }, 200

            else:
                return {
                    "error": "Invalid Authentication."
                }, 403
            
        except:
            Log.error(traceback.format_exc())
            return {
                "error": "An error occurred."
            }, 500


    def close(self, request):
        Log.info('close()')
        
        try:            
            sessionToken = request.headers.get("Authentication", "")
            tokenDoc = self.isValidSessionToken(sessionToken)
            if tokenDoc:
                tokenDoc.expireAt = datetime.utcnow
                tokenDoc.save()
                
                return {
                }, 200

            else:
                return {
                    "error": "Invalid Authentication."
                }, 403

        except:
            Log.error(traceback.format_exc())
            return {
                "error": "An error occurred."
            }, 500



