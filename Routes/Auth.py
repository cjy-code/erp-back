from Main import app ,dumps, json, request, departmentDB, userDB, TaskDB, datetime, TaskHistoryDB, ObjectId, time, jwt, jsonify, accessJWT, refreshJWT, bcrypt, traceback, pbkdf2_sha512, session, hashlib, secrets, base64, escape, redirect, webdriver, cookies, User_c


@app.route('/')
def index():
    if 'name' in session: 
        return '%s' % escape(session['name'])
    return 'no login'

# 로그인
@app.route('/login', methods=['POST'])
async def Member():
    Data = await request.get_json()
    try:
        print('123123',session)
        req_email = Data['email']
        req_psw = Data['password']

        
        if req_email is None or req_email == '':
            return '', 400
        if req_psw is None or req_psw == '':
            return '', 400       

        account_user = userDB.find_one({'Id': req_email})
        
        if account_user != None and account_user != '':
            if account_user['Password'] == hashlib.md5(req_psw.encode()).hexdigest():
                
                session['Grade'] = int(account_user['Grade'])
                session['_id'] = str(account_user['_id'])
                
                print("login: ",session)
                
                User = userDB.aggregate([
                            {
                            '$match': {'_id': ObjectId(str(account_user['_id']))}
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
                return  dumps({'session': session['_id'], 'UserInfo': User}) , 202
            # return dumps(User), 202
        return '', 403
    except:
        traceback.print_exc()
        return '', 402
  

# Logout
@app.route('/logout', methods=['POST']) 
async def logout():
    session.clear()
    print("logout: ",session)
    return '', 200

@app.route('/Auth/isLogin', methods=['GET'])
async def MemberIsLogin():
    try:
        if 'Grade' in session and '_id' in session:
            User = userDB.aggregate([
                            {
                            '$match': {'_id': ObjectId(str(session['_id']))}
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
            return  dumps({'session': session['_id'], 'UserInfo': User}) , 202
        return '',401
    except print(0):
        pass


# REGISTER function
@app.route('/register', methods=['POST'])
async def register():
    Data = await request.get_json()
    try:
        
        req_id = Data['email']
        req_psw = Data['password']
        req_grade = Data['grade']
        req_department = Data['department']
        req_name = Data['name']
        # req_edate = Data['entdate']
        print('아이디: ',req_id)
        print('비밀번호: ', req_psw)
        print('이름: ', req_name)    

        # 빈스트링 체크
        if req_id == None or req_id =='':
            return '', 400
        elif req_psw == None or req_psw == '':
            return '', 401
        elif req_name == None or req_name == '':
            return '', 402

        # 아이디 중복 검사 
        account_user = userDB.find_one({'Id': req_id})
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        # 아이디 중복 검사
        if account_user != None:
            return '', 403
        else:
            userDB.insert_one({
                'Id': req_id,
                'Password': req_psw,
                'Grade': int(req_grade),
                'Department': ObjectId(req_department),
                'Name': req_name,
                # 'EtrDate': req_edate,
                'Status': '재직' ,
                'CreateDate' : datetime.datetime.now(),
                'EditDate' : datetime.datetime.now()
            })
            return '', 202
        return '', 404
    except:
        traceback.print_exc()
        return '', 405




# @app.route('/test1', methods=['GET'])
# async def dkdkdkdkdk():
#     # print("123")
#     try:
#         # print("asd")
        
#         # print(dumps(User_c.find({})))
#         return '', 200
#     except :
#         pass