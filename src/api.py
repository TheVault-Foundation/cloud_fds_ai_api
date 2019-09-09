from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

from log import Log
from controller import Controller

import json

import sys 
sys.path.append('../config')

import config

app = FlaskAPI(__name__)


ApiRoot = config.API_ROOT
@app.route(ApiRoot + '/authenticate', methods=['POST'])
def authenticate():
    con = Controller()
    return con.authenticate(request)

@app.route(ApiRoot + '/device', methods=['GET'])
def device():
    con = Controller()
    return con.device(request)

@app.route(ApiRoot + '/check', methods=['POST'])
def check():
    con = Controller()
    return con.check(request)

@app.route(ApiRoot + '/close', methods=['POST'])
def close():
    con = Controller()
    return con.close(request)


if __name__ == "__main__":
    app.run(debug=True, port=5000)