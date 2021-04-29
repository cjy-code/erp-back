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
from selenium import webdriver #<-------------크롤링??
from http import cookies

from urllib.parse import urlparse, parse_qsl
import json

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
User_c = db.User_copy


# Insert Data TEST
userDB.create_index

app = Pint(__name__)
app.secret_key = "_#asfof3342soso@!#"

def accessJWT(User):
    
    Expire = datetime.datetime.now() + datetime.timedelta(days=3)
    
    token = jwt.encode({'User': User}, secret_key, algorithm="HS512").decode('utf-8')
    return token
    
def refreshJWT(User):
    
    Expire = datetime.datetime.now() + datetime.timedelta(days=14)
    Token = jwt.encode({'User': User, 'exp': Expire}, secret_key, algorithm="HS512").decode('utf-8')
   
    Tokens.insert_one({
        'Token': Token,
        'Expire': Expire
    })

    return Token

def checkAccessJWT(Token):
    try:
        Data = jwt.decode(Token, secret_key, alforithms=['HS512'])
        if Data['exp'] - datetime.datetime.now() >= 0 and userDB.find_one({'_id': ObjectId(Data['User'])}) is not None:
            return Data['User']
        return '', 400
    except:
        traceback.print_exc()
    return False


def checkRefreshJWT(Token):
    try:
        Data = jwt.decode(Token, secret_key, algorithms=['HS512'])
        if Data['exp'] - datetime.datetime.now() >= 0 and Tokens.find_one({'Token': Token, 'exp': Data['Expire']}) is not None and userDB.find_one({'_id': ObjectId(Data['User'])}) is not None:
            Tokens.delete_one({'Token': Token, 'Expire': Data['Expire']})       
            return Data['User']
    except:
        traceback.print_exc()
    return False        

def jwt_require(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'TimeToken' not in request.headers:
            return '', 400

        Data = checkAccessJWT(request.headers['TimeToken'])
        if Data is False:
            print('Token Expire')
            return '', 401

        return func(Data, *args, **kwargs)

    return decorated_function

@app.before_request
async def before_request():
    # Data = await request.get_json()
    try:
        # print(request.headers)
        print(session)
        if request.headers.get('User-Agnet') is not None:
            print("Session 종료")
            return '',204
            
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(hours=1)

        # session.permanent = False

        # return '', 200
    except:
        traceback.print_exc()
        return '', 401

@app.route('/session', methods=['GET'])
async def Session():
    print('session',session)
    return '',200


from Routes.Department import *
from Routes.Tasks import * 
from Routes.Auth import *
from Routes.TaskHistory import * 
from Routes.Employee import * 


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='0.0.0.0', port=80)


