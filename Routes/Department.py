from Main import app ,dumps, json, session,request, departmentDB, userDB, TaskDB, datetime, TaskHistoryDB, ObjectId, time, Resource, traceback, pd, urlparse, parse_qsl
from Except.Exception import DepartmentAdd


@app.route('/department')
class Department(Resource):
    # 부서 리스트 호출
    async def get(self):
        try:
            department_list = departmentDB.find({})
            
            #-----------------------------------------
            # Department Task List 추가 시 중복 제거 Test용
            # a = ['a', 'b', 'c', 'd']
            # a.append('d')
            # print(len(a))
            # print(len(set(a)))
            # if len(a) != len(set(a)):
            #     print('딱걸림')
            # print("test: ",a)-----------------------

            if department_list is not None:
                return dumps(department_list), 200
            else:
                return dumps('부서정보가 없습니다.'), 400
            
        except Exception as exc:
            print(exc)
            return '', 400
    
    # 부서 개설
    async def post(self):
        try:
            Data = await request.get_json()
            # admin_name = Data['Administor']
            department_name = Data['department']
            
            if department_name == '' and department_name is None:
                print('부서명을 입력해주세요') 
                return '', 401
        
            #부서명 중보검사
            department_find = departmentDB.find_one({'Department': department_name})
            
            if department_find is not None and department_find is not '':
                print('\n부서명 중복\n')
                return '', 409

            departmentDB.insert_one({
                'Administor': None,
                'Department': department_name,
                'TaskList': None
            })
            return '', 204
        except:
            traceback.print_exc()
            return '', 400
        return 200 


# 부서 리스트 상세페이지
@app.route('/department/<departmentId>')
class DepartmentDetail(Resource):
    async def get(self, departmentId):
        try:
            # Department_Data = departmentDB.find_one({'_id': ObjectId(departmentId)})
            find_user = userDB.find({'Department': ObjectId(departmentId)})
            Department_Data = departmentDB.aggregate([
                                            {
                                                '$match' : {'_id': ObjectId(departmentId)  }
                                            },
                                            {
                                                '$lookup' : {
                                                    'from' : 'Tasks',
                                                    'localField' : 'TaskList',
                                                    'foreignField' : '_id',
                                                    'as' : 'DepartmentInfo'
                                                }
                                            }
                                        ]) 
            if Department_Data != None or Department_Data != '':
                print('부서 있음')
                return dumps(Department_Data), 200 
            else:
                print('부서 없음')
                return dumps({'해당하는 정보가 없습니다.'}), 401
        except Exception as exc:
            print(exc)
            return '', 402
        
        return dumps({Department_Data}), 201
    
    # 부서 수정
    async def patch(self, departmentId):
        try:
            Data = await request.get_json()
            req_adm = Data['administor']
            req_dep = Data['department']
            # req_select = Data['selectlist']
            req_task = Data['sumArray']
            ABC = list(req_task)
            print("\nadm: ",req_adm)
            # print("aaaa: ", req_select)
            print('TASK: ', req_task)
            # ABC.append(req_select)
            print(ABC)
          
            
            duplicate = []
            for index,value in enumerate(req_task):
                req_task[index] = ObjectId(value['_id']['$oid'])
                duplicate.append(value['Name'])

            if len(duplicate) != len(set(duplicate)):
                return '', 404
           
            if req_adm is None or req_adm == '':
                return  '', 400
            elif req_dep is None or req_dep == '':
                return  '', 401
            if req_task is None or req_task == '':
                req_task = []
            
            departmentDB.update_one({'_id':ObjectId(departmentId)}, {'$set':{'Department': req_dep, 'Administor': req_adm, 'TaskList' : req_task}})

            return '', 200
        except:
            traceback.print_exc() 
            return '', 402

    # 부서 삭제
    async def delete(self, departmentId):
        try:
            _id_result = departmentDB.find_one({'_id': ObjectId(departmentId)})
            
            if _id_result is None:  
                return  '', 400
            else:
                departmentDB.delete_one({
                    '_id': ObjectId(departmentId)
                })    
                return '', 200
        except Exception as exc:
            print(exc)
            return '', 401
        return '', 402       



