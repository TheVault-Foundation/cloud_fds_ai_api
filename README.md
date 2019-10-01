# cloud_fds_ai_api
FDS API and AI module

** Setup
1. chmod +x start_server.sh

2. pipenv install

3. pipenv shell

4. docker-compose build

5. docker-compose up # localhost:6000


** Test
1. Authenticate
'''
curl -X POST -d "api_key=asfsdfsadf&api_secret=aaaaaaaaafffffffffff" http://localhost:5000/v1/fds/session/authenticate
'''

2. Get user device list
'''
curl -H "Authorization: Bearer ab8d720f1082d28dcbff4da1dc683e63a6bb64bc3e8116afe7b29b4761f962f4" http://localhost:5000/v1/fds/userdevice
'''

3. Close session
'''
curl -X POST -H "Authorization: Bearer ab8d720f1082d28dcbff4da1dc683e63a6bb64bc3e8116afe7b29b4761f962f4" http://localhost:5000/v1/fds/session/close
'''

4. Check transaction
'''
curl -X POST -d "{\"fromAddress\":\"33geh4Z1inbdcTjU1WV4QkFffr5Ac1auPe\",\"fromCurrency\":\"BTC\",\"toAddress\":\"3Jr1S6mRhZPmk9jYQT7gFX74At8vMJ4JKP\",\"toCurrency\":\"BTC\",\"amount\":3.5,\"senderDeviceId\":1,\"senderIp\":\"10.0.0.1\",\"transactedAt\":\"20190909T1212\"}" -H "Content-Type: application/json" -H "Authorization: Bearer ab8d720f1082d28dcbff4da1dc683e63a6bb64bc3e8116afe7b29b4761f962f4" http://localhost:5000/v1/fds/transaction/check
'''

5. Update transaction score(0 or 100)
'''
curl -X POST -d "{\"id\":\"5d8daa767a9f0c4291b87ff0\",\"score\":0}" -H "Content-Type: application/json" -H "Authorization: Bearer ab8d720f1082d28dcbff4da1dc683e63a6bb64bc3e8116afe7b29b4761f962f4" http://localhost:5000/v1/fds/transaction/update
'''
