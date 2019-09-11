import jwt
import os
import datetime
import traceback

from log import Log

class JWT_AUTH:
    SESSION_TOKEN_LIFETIME = 86400  # 24 hours

    @staticmethod
    def generateSessionToken(userApi):
        """
        Generates the Auth Token
        :return: string
        """
        # print(userApi)
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=JWT_AUTH.SESSION_TOKEN_LIFETIME),
                'iat': datetime.datetime.utcnow(),
                'apiId': str(userApi.id),
                'userId': str(userApi.userId)
            }
            return jwt.encode(
                payload,
                os.getenv('FDS_API_SECRET_KEY', 'cloud_fds_ai_api'),
                algorithm='HS256'
            ).decode("utf-8")
        except Exception as e:
            Log.error(traceback.format_exc())
            return e


    @staticmethod
    def isValidSessionToken(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            return jwt.decode(auth_token, os.getenv('FDS_API_SECRET_KEY', 'cloud_fds_ai_api'))
        except jwt.ExpiredSignatureError:
            Log.error('Signature expired. Please log in again.')
            return False
        except jwt.InvalidTokenError:
            Log.error('Invalid token. Please log in again.')
            return False
        except:
            Log.error(traceback.format_exc())
            return False
