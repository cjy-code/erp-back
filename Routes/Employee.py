from run import app ,dumps, json, request, departmentDB, userDB, TaskDB, datetime, TaskHistoryDB, ObjectId, time, Resource, traceback, session, math, urlparse, parse_qsl

@app.route('/employee/info/<oid>')
class EmployeeList(Resource):
    # 사원 정보 Patch
    async def patch(self, oid):
        try:
            Data = await request.get_json()
            print('asdf')
            print(oid)
            
            # req_id = Data['email']
            # req_psw = Data['password']
            req_grd = Data['grade']
            req_dpt = Data['department']
            req_name = Data['name']
            req_ent = Data['etrdate']
            req_stat = Data['status']

            # if req_id is None or req_id is '':
            #     return  '', 400
            # elif req_psw is None or req_psw is '':
            #     return  '', 400
            if req_name is None or req_name is '':
                return  '', 400
            elif req_ent is None or req_ent is '':
                return  '', 400
            elif req_dpt is None or req_dpt is '':
                return  '', 400
            elif req_stat is None or req_stat is '':
                return  '', 400
            elif req_grd is None or req_grd is '':
                return  '', 400

            if req_grd == "관리자":
                req_grd = 0
            elif req_grd == "부서장":
                req_grd = 1
            elif req_grd == "사원":
                req_grd = 2
            else:
                print("직급을 정확하게 입력해주세요")
                return '',410
            # req_ent = datetime.datetime.strptime(req_ent, '%Y-%m-%d %h:%M:%S.%f')
            req_ent = datetime.datetime.strptime(req_ent, '%Y-%m-%d')
            userDB.update_one(
                {'_id': ObjectId(oid)},
                {'$set':{
                # 'Id': req_id,
                # 'Password': req_psw,
                'Grade': int(req_grd),
                'Department': req_dpt,
                'Name': req_name,
                'EtrDate': req_ent,
                'Status': req_stat,
                'EditDate' : datetime.datetime.now()
                }
            })
            return '', 200
        except:
            traceback.print_exc()
            return '', 401
        
    # 사원 상세 정보 Get
    async def get(self, oid):
        try:


            agg_user =userDB.aggregate([   
                {
                '$match':{'_id': ObjectId(oid)}
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
                    '$project' : {
                        'Password': 0,
                        'DepartmentInfo' : { '_id' : 0 , 'TaskList' : 0}
                    }
                },
                {      
                    '$unwind' :  "$DepartmentInfo"
                }
                ])

            User = list(agg_user)
            return dumps(User[0]), 200
        except :
            traceback.print_exc()
            return '', 400
    
    # 사원 정보 삭제
    async def delete(self, oid):
        try:
            find_userDB = userDB.find_one({'_id': ObjectId(oid)})
            
            if find_userDB is None:
                return '', 400
            else:
                userDB.delete_one({'_id': ObjectId(oid)})
                return '', 200
        except:
            traceback.print_exc()
            return '', 401



#  **** 정렬, 페이징, 서칭 ******
@app.route('/user', methods=['GET'])
async def User():
    try:
        url = urlparse(request.url)
        searchQuery = dict(parse_qsl(url.query))
        print(searchQuery)
        print('사원 관리페이지 Session Chack:', session['Grade'])
        search = {}
        search_Dpt = {}
        
        

        if math.ceil(int(userDB.count()) / int(searchQuery['limit'])) < int(searchQuery['page']):
            print('페이지 초과')
            return '', 400

        if searchQuery['search'] is not None and searchQuery['search'] != '' and len(searchQuery['search']) > 0:
            query = json.loads(searchQuery['search'])
            for key, value in query.items():         
                searchKey = key  
                if searchKey == "Department":
                    search_Dpt = { 'DepartmentInfo.Department' : {"$regex": value}} 
                elif key == "Grade":
                    if value == "관리자":
                        # if session['Grade'] > 0:
                            # return '',409
                        search = {"Grade" : 0}
                    elif value == "부서장":
                        # if session['Grade'] > 1:
                        #     return '',409
                        search = {"Grade" : 1}
                    elif value == "사원":
                        # if session['Grade']:
                        #     return '',409
                        search = {"Grade" : 2}
                    # else:
                    #     return '',409
                else:
                    search = {str(key) : {"$regex": value}}
       
        
        print("1: ",search_Dpt)
        print("2: ",search)
        agg_user = userDB.aggregate([
            
            {'$match' : {
                    '$and' : [
                        { 'Grade' : {'$gte': 0}},
                        search
                    ]
                    }
            } ,
            {'$sort': { searchQuery['orderby'] :int(searchQuery['ascending'])}},     
            # {'$sort': { 'Name':int(searchQuery['ascending'])}},         
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
            '$match': search_Dpt
            },
            
    
            {
                '$facet' : {
                    'edge' : [
                    {
                    '$match' : {}
                    },
                    {'$limit' : int(searchQuery['limit']) * int(searchQuery['page']) },
                    {'$skip' : (int(searchQuery['page']) -1) * int(searchQuery['limit']) },
                    {      
                    '$unwind' : {'path': "$DepartmentInfo", 'preserveNullAndEmptyArrays' : True}
                    }
                    
                    ],
                    'UserInfo' : [
                        { '$group' : 
                            {   '_id' : None,
                                'Count' : {'$sum' : 1} 
                            } 
                        }
                    ]
                }
            },
        {
            '$unwind': "$UserInfo"
        }
        ])
        
        # DB 결과가 O일경우 IndexError: list index out of range 발생, 조건문 추가하기
        Data = list(agg_user)
        # print(len(Data))

        if len(Data) > 0:
            return dumps({ 'Data' : Data[0]['edge'], 'Count' : Data[0]['UserInfo']['Count']}), 201

        return dumps({ 'Data' : [], 'Count' : 1 }), 201
     
    except :
        traceback.print_exc()
        return '',401



# 특정 Grade 사원 리스트 GET -> 부서장 리스트 불러오기
@app.route('/employee/grade', methods=['GET'])
async def UserGradeList():
    try: 
        agg_user =userDB.aggregate([   
        {
        '$match':{'Grade': int(1)}
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
            '$project' : {
                'Password': 0,
                'DepartmentInfo' : { '_id' : 0 , 'TaskList' : 0}
            }
        },
        {      
            '$unwind' :  "$DepartmentInfo"
        }
        ])

        if agg_user is None:
            return '', 400

        # print('부서장: ',dumps(agg_user))
        return dumps(agg_user), 200
    except :
        traceback.print_exc()
        return '', 401






    




















# # 사원관리 Searching
# @app.route('/employee/search', methods=['GET'])
# async def Searching():
#     try:
        
#         return '', 200        
#     except:
#         traceback.print_exc()
#         return '', 403


# # 사원관리 Sort
# @app.route('/employee/sort/<sort>/<sort_opt>', methods=['GET'])
# async def Sorting(sort, sort_opt):
#     try:
#         Data = await request.get_json()
#         req_sort = Data['sort']
#         req_sort_opt = Data['sortOpt']
        
#         print(sort, sort_opt)

#         agg_user =userDB.aggregate([   
#         {
#         '$sort':{sort: int(sort_opt)}
#         },
#         {
#         '$lookup':
#             {
#             'from': 'Department',
#             'localField': 'Department',
#             'foreignField': '_id',
#             'as': 'DepartmentInfo'
#             }
#         },
#         {
#             '$project' : {
#                 'Password': 0,
#                 'DepartmentInfo' : { '_id' : 0 , 'TaskList' : 0}
#             }
#         },
#         {      
#             '$unwind' : "$DepartmentInfo"
#         }
#         ])
        
       

#         return dumps(agg_user), 200   
 
#     except:
#         traceback.print_exc()
#         return '', 403
        """ @app.route('/user/<opt>', methods=['GET'])
async def User_option(opt):
    try:
        # print(session['Grade'])
        #print(session['User'])
        if len(opt) is 1:

            print(opt)
            agg_user =userDB.aggregate([   
            {
            '$match':{'Grade': {'$eq': opt}}
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
                '$project' : {
                    'Password': 0,
                    'DepartmentInfo' : { '_id' : 0 , 'TaskList' : 0}
                }
            },
            {      
                '$unwind' :  "$DepartmentInfo"
            }
            ])

            return dumps(agg_user), 200
        else:
            agg_user =userDB.aggregate([   
            {
            '$match':{'_id': ObjectId(opt)}
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
                '$project' : {
                    'Password': 0,
                    'DepartmentInfo' : { '_id' : 0 , 'TaskList' : 0}
                }
            },
            {      
                '$unwind' :  "$DepartmentInfo"
            }
            ])

            User = list(agg_user)
            
            return dumps(User[0]), 201
    except :
        traceback.print_exc()
        return '',401 """


""" # 사원 상세보기 GET
@app.route('/employee/info/<oid>', methods=['GET'])
async def UserInfo(oid):
    try:
        agg_user =userDB.aggregate([   
            {
            '$match':{'_id': ObjectId(oid)}
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
                '$project' : {
                    'Password': 0,
                    'DepartmentInfo' : { '_id' : 0 , 'TaskList' : 0}
                }
            },
            {      
                '$unwind' :  "$DepartmentInfo"
            }
            ])

        User = list(agg_user)
        return dumps(User[0]), 200
    except :
        traceback.print_exc()
        return '', 400 """