from bson.objectid import ObjectId
from bson import json_util, errors

from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta

import traceback

import utils
from utils import Log
from model import *
from fds import CheckTransaction

import json
from hashlib import sha256

from flask import jsonify


class Controller:
    SESSION_TOKEN_LIFETIME = 86400  # 24 hours
    
    def __init__(self):
        pass
        # Log.info('__init__()')

    def ResError(self, code, message):
        return jsonify({ "error": {"message": message, "code": code} }), code

    def generateSessionToken(self, api):
        curTime = datetime.utcnow()       ### UTC now()
        expireAt = curTime + timedelta(seconds=self.SESSION_TOKEN_LIFETIME)
        tokinObj = { 'id': api.id, 'key': api.apiKey, 'secret': api.apiSecret, 'expireAt': expireAt }

        token = sha256(json_util.dumps(tokinObj).encode('utf-8')).hexdigest()

        # session = ApiSessionToken(
        #     apiId = api.id,
        #     sessionToken = token,
        #     expireAt = expireAt,
        #     CreatedAt = curTime
        # )
        # session.save()

        session = ApiSessionToken.objects(apiId=api.id).modify(
                upsert=True, new=True,
                set__apiId = api.id,
                set__sessionToken = token,
                set__expireAt = expireAt,
                set__CreatedAt = curTime
        )

        return session.sessionToken
        
    def isValidSessionToken(self, sessonToken):
        strippedToken = sessonToken.strip()
        if not strippedToken:
            return False

        Log.info(strippedToken)
        try:
            token = ApiSessionToken.objects.get(sessionToken=strippedToken, expireAt__gt=datetime.utcnow)

            user = User.objects.get(id=token.getUserId(), isActive=True)

            return token
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

            return jsonify({
                'session_token': sessionToken,
                'lifetime': self.SESSION_TOKEN_LIFETIME
            }), 200
        except DoesNotExist:
            return self.ResError(403, "Invalid api key or secret.")
        except:
            Log.error(traceback.format_exc())
            return self.ResError(500, "An error occurred.")

    def device(self, request):
        Log.info('device()')

        try:
            sessionToken = request.headers.get("Authorization", "").split(' ')[1]
            if self.isValidSessionToken(sessionToken):
                retList = []
                for d in DeviceType.objects:
                    retList.append({'device_id': d.deviceId, 'device_type': d.deviceType})
                
                return json.dumps(retList), 200

            else:
                return self.ResError(401, "Invalid Authentication.")
            
        except:
            Log.error(traceback.format_exc())
            return self.ResError(500, "An error occurred.")


    def check(self, request):
        Log.info('check()')
        Log.info(request.data)

        try:
            sessionToken = request.headers.get("Authorization", "").split(' ')[1]
            tokenDoc = self.isValidSessionToken(sessionToken)
            if tokenDoc:
                reqData = request.data

                check = CheckTransaction(tokenDoc, reqData)
                
                return check.process()

            else:
                return self.ResError(401, "Invalid Authentication.")
            
        except:
            Log.error(traceback.format_exc())
            return self.ResError(500, "An error occurred.")


    def update(self, request):
        Log.info('update()')
        Log.info(request.data)

        try:
            sessionToken = request.headers.get("Authorization", "").split(' ')[1]
            tokenDoc = self.isValidSessionToken(sessionToken)
            if tokenDoc:
                reqData = request.data

                if (reqData['score'] not in [0, 100]):
                    return self.ResError(403, "Invalid score.")

                trans = Transaction.objects.get(id=ObjectId(reqData['id']))
                trans.score = reqData['score']
                trans.save()

                return jsonify({
                }), 200
            else:
                return self.ResError(401, "Invalid Authentication.")
        
        except (DoesNotExist, errors.InvalidId) as e:
            return self.ResError(403, "Invalid id.")
        except:
            Log.error(traceback.format_exc())
            return self.ResError(500, "An error occurred.")


    def close(self, request):
        Log.info('close()')
        
        try:            
            sessionToken = request.headers.get("Authorization", "").split(' ')[1]
            tokenDoc = self.isValidSessionToken(sessionToken)
            if tokenDoc:
                tokenDoc.expireAt = datetime.utcnow
                tokenDoc.save()
                
                return jsonify({
                }), 201

            else:
                return self.ResError(401, "Invalid Authentication.")

        except:
            Log.error(traceback.format_exc())
            return self.ResError(500, "An error occurred.")
