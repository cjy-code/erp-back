from quart import Quart, request, render_template, jsonify, session, escape, redirect, session, url_for
from bson.json_util import dumps
from functools import wraps
import pymongo, jwt, time, datetime, traceback, bcrypt, hashlib, secrets, base64, pylint, math, requests
from pymongo import MongoClient
# from datetime import datatime, timedelta
from bson import ObjectId
from quart_openapi import Pint,Resource
from secret import secret_key
from passlib.hash import pbkdf2_sha512
from hashlib import sha512
import pandas as pd

from urllib.parse import urlparse, parse_qsl
import json

from quart_cors import cors


ip = 'localhost'
port = 27017

# Connect MongoDB
connection = MongoClient(ip, port)
db = connection.ERP


# Collection 접근
userDB = db.User
departmentDB = db.Department
TaskDB = db.Tasks
TaskHistoryDB = db.TaskHistory
Tokens = db.Tokens
AttemdanceDB = db.Attendance

# Insert Data TEST
userDB.create_index

app = Pint(__name__)
cors(app)
# app = cors(app, **settings)

def accessJWT(User):
    Expire = time.time() + 300
    Token = jwt.encode({'User': User, 'exp': Expire}, secret_key, algorithm="HS512").decode('utf-8')
    return Token

def refreshJWT(User):
    Expire = time.time() + (86400 * 14) 
    Token = jwt.encode({'User': User, 'exp': Expire}, secret_key, algorithm="HS512").decode('utf-8')
   
    Tokens.insert_one({
        'Token': Token,
        'Expire': Expire
    })

    return Token

def checkAccessJWT(Token):
    try:
        Data = jwt.decode(Token, secret_key, algorithm=['HS512'])
        print('check:',Data['User'])
        if userDB.find_one({'_id': ObjectId(Data['User'])}) is not None: 
            return Data['User']
    except:
        traceback.print_exc()
    return False


def checkRefreshJWT(Token):
    try:
        Data = jwt.decode(Token, secret_key, algorithms=['HS512'])
        if Tokens.find_one({'Token': Token, 'exp': Data['Expire']}) is not None and userDB.find_one({'_id': ObjectId(Data['User'])}) is not None:
            Tokens.delete_one({'Token': Token, 'Expire': Data['Expire']})       
            return Data['User']
    except:
        traceback.print_exc()
    return False        


def jwt_require(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'Token' not in request.headers:
            return '', 400

        UserId = checkAccessJWT(request.headers['Token'])
        print("\n if 통과: ", UserId)
        if UserId is False:
            return dumps({'err': 'token expired'}), 401       

        return func(UserId, *args, **kwargs)
    return decorated_function


from Routes.W_Routes.W_Auth import *
from Routes.W_Routes.W_TaskHistory import * 
from Routes.W_Routes.W_Tasks import *


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='0.0.0.0', port=80)


