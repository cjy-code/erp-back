from W_Main import app ,dumps, json, request, departmentDB, userDB, TaskDB, datetime, TaskHistoryDB, ObjectId, time, jwt, jsonify, accessJWT, refreshJWT, bcrypt, traceback, pbkdf2_sha512, session, hashlib, secrets, base64, escape, redirect, checkRefreshJWT, secret_key, requests, jwt_require


# from http import cookies
# 로그인
@app.route('/widget/login', methods=['POST'])
async def W_Login():
    Data = await request.get_json()
    try:
        req_email = Data['email']
        req_psw = Data['password']

        if req_email is None or req_email == '':
            return '', 400
        if req_psw is None or req_psw == '':
            return '', 400       
        
        find_user = userDB.find_one({'Id': req_email})
       
        if find_user != None:
            if find_user['Password'] == hashlib.md5(req_psw.encode()).hexdigest():
                
                AccessToken = accessJWT(str(find_user['_id']))
                RefreshToken = refreshJWT(str(find_user['_id']))
                print(AccessToken)
                print(RefreshToken)
                User = userDB.aggregate([
                            {
                            '$match': {'_id': ObjectId(str(find_user['_id']))}
                            },
                            {
                            '$lookup':
                                {
                                'from': 'Department',
                                'localField': 'Department',
                                'foreignField': '_id',
                                'as': 'DepartmentInfo'
                                }
                            },
                            {      
                                '$unwind' : { 'path' : "$DepartmentInfo", 'preserveNullAndEmptyArrays': True }
                            },
                            {
                                '$project' : {'Password': 0, '_id':0 }
                            }
                            ])
                
                return dumps({'token': AccessToken, 'rtoken': RefreshToken, 'User': User})
        return '', 401
    except:
        traceback.print_exc()
        return '', 500

# @app.route('widget/logout', methods = ['POST'])
# async def W_Logout():
#     try:
          
#         return '', 200
#     except :
#         traceback.print_exc()
#         return '', 400
    
@app.route('/widget/login/reset', methods=['POST'])
async def ResetAuth():

    Data = json.load(await request.get_date())
    try:
        TokenInfo = refreshJWT(Data['Token'])
        if TokenInfo is not False:
            return dumps({'token': accessJWT(TokenInfo), 'rtoken': refreshJWT(TokenInfo)})
        else:
            return '', 400
    except:
        traceback.print_exc()
        return '', 500


@app.route('/test123', methods=['POST'])
@jwt_require
async def MTF(UserId):
    print('GoGo')
    print('Excellent')
    print(UserId)

    return '', 200

@app.route('/test111', methods=['GET'])
# @jwt_require
async def mbc(UserId):
    print('GoGo')
    print('Excellent')
    # print(UserId)
    # print(request.headers)
    return '', 200

@app.route('/test18', methods=['GET'])
@jwt_require
async def kbs(UserId):
    print('GoGo')
    print('Excellent')
    # print(UserId)
    # print(request.headers)
    return '', 200