import sys 
# sys.path.append('../config')  # for config module

from flask import request, Response, url_for
from flask_api import FlaskAPI, status, exceptions

from utils import Log
from controller.controller import Controller

import json

import config


class CustomResponse(Response):
    default_mimetype = 'application/json'

app = FlaskAPI(__name__)
app.response_class = CustomResponse


ApiRoot = config.API_ROOT
@app.route(ApiRoot + '/session/authenticate', methods=['POST'])
def authenticate():
    con = Controller()
    return con.authenticate(request)

@app.route(ApiRoot + '/userdevice', methods=['GET'])
def device():
    con = Controller()
    return con.device(request)

@app.route(ApiRoot + '/transaction/check', methods=['POST'])
def check():
    con = Controller()
    return con.check(request)

@app.route(ApiRoot + '/transaction/update', methods=['POST'])
def update():
    con = Controller()
    return con.update(request)

@app.route(ApiRoot + '/session/close', methods=['POST'])
def close():
    con = Controller()
    return con.close(request)


if __name__ == "__main__":
    app.run(debug=True, port=6000)