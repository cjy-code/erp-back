from W_Main import app ,dumps, json, session,request, departmentDB, userDB, TaskDB, datetime, TaskHistoryDB, ObjectId, time, Resource, traceback, pd, jwt_require,AttemdanceDB

@app.route('/widget/taskhistory')
class TaskHistory_widget_main(Resource):
    # GET
    # @jwt_require
    # async def get(self, UserId):
    async def get(self):
        try:
            find_taskH = TaskHistoryDB.find({'User': ObjectId("606d71d2a96b3d38380aed1b"),
                                             'EndDate': None})
            if find_taskH is None:
                return '', 401
            seartch = {}
            agg_taskH = TaskHistoryDB.aggregate([{
                                    '$match': {
                                        '$and': [
                                                # {'User': ObjectId(UserId['_id'])},
                                                {'User': ObjectId("606d71d2a96b3d38380aed1b")},
                                                {'EndDate': None},
                                                seartch
                                    ]
                                    }
                                },
                                {'$lookup': {
                                        'from': 'Tasks',
                                        'localField': 'Task',
                                        'foreignField': '_id',
                                        'as': 'TaskInfo'
                                        }
                                },
                                {'$facet': {
                                            'edge': [{
                                                        '$match': {}
                                                    }],
                                        'ListInfo': [{ 
                                                    '$group' :{   
                                                            '_id' : "$items",
                                                            'Count' : {'$sum' : 'NumberInt(1)'} 
                                                        } 
                                                    }]
                                            }
                                },
                                {
                                    '$unwind': {'path': '$TaskInfo' , 'preserveNullAndEmptyArrays' : True}
                                }
                                ])
                                
            # return '', 200
            return dumps(agg_taskH)
        except :
            traceback.print_exc
            return '', 500



# TaskHistoryDB 생성
@app.route('/widget/taskhistory/create/<task_id>', methods=['POST'])
async def task_create(task_id):
    Data = await request.get_json()
    Now = datetime.datetime.now()
    try:
        req_dsc = Data['dscription']
        TaskHistoryDB.insert_one({
            'StartDate': Now,
            'EndDate': None,
            'TmpDate': None,
            'Time': None,
            'Status': 'ready',
            'Task': ObjectId(task_id),
            'Description' : req_dsc,
            'User': ObjectId('606d71d2a96b3d38380aed1b'),
            # 'User': ObjectId(UserId['_id']),
            'RestTime': None
        })
        return ''
    except :
        traceback.print_exc()
        return '', 500

# TaskHistoryDB 삭제
@app.route('/widget/taskhistory/delete/<taskH_id>', methods=['DELETE'])
async def task_delete(taskH_id):
    try:
        find_TskH = TaskHistoryDB.find_one({'_id': ObjectId(taskH_id)})
        if find_TskH is None:
            return dumps({'err': '요청하신 업무는 없습니다.'}), 401

        TaskHistoryDB.delete_one({'_id': ObjectId(taskH_id)})
        return ''
    except :
        traceback.print_exc()
        return '', 500


# TaskHistoryDB 선택
@app.route('/widget/taskhistory/get/<taskH_id>', methods=['GET'])
async def task_get(taskH_id):
    try:
        agg_taskH = TaskHistoryDB.aggregate([
                                {
                                '$match': 
                                    {'_id': ObjectId(taskH_id)}
                                },
                                {'$lookup': {
                                        'from': 'Tasks',
                                        'localField': 'Task',
                                        'foreignField': '_id',
                                        'as': 'TaskInfo'
                                        }
                                },
                                {
                                    '$unwind': {'path': '$TaskInfo' , 'preserveNullAndEmptyArrays' : True}
                                }
                                ])
        return dumps(agg_taskH)
    except:
        traceback.print_exc()
        return '', 500

# Timer 시작
@app.route('/widget/taskhistory/timer/start/<taskH_id>', methods=['PATCH'])
async def timer_start(taskH_id):
    try:    
        Now = datetime.datetime.now()
        TaskHistoryDB.update_one({'_id': ObjectId(taskH_id)},
                                        {'$set': 
                                            {'Status':'working',
                                            'StartDate': Now}
                                    })
        return ''
    except :
        traceback.print_exc()
        return '', 500

# Timer 멈춤, 재시작
@app.route('/widget/taskhistory/timer/toogle/<taskH_id>', methods=['PATCH'])
async def timer_toogle(taskH_id):
    try:
        Now = datetime.datetime.now()
        f_taskH = TaskHistoryDB.find_one({'_id': ObjectId(taskH_id)})
        
        # 멈춤
        if f_taskH['Status'] is 'working':
            TaskHistoryDB.update_one({'_id': ObjectId(taskH_id)},
                                    {'$set': 
                                        {'Status':'pause',
                                         'Time': str(Now - f_taskH['StartDate'] - f_taskH['RestTime']),
                                         'TmpDate': Now}
                                    })
        
        # 재시작
        elif f_taskH['Status'] is 'pause':        
            TaskHistoryDB.update_one({'_id': ObjectId(taskH_id)},
                                    {'$set': 
                                        {'Status':'working',
                                         'RestTime': str(Now - f_taskH['TmpDate'] + f_taskH['RestTime'] )}
                                    })
        return ''
    except :
        traceback.print_exc()
        return '', 500

# Timer 종료
@app.route('/widget/taskhistory/timer/end/<taskH_id>', methods=['PATCH'])
async def timer_end(taskH_id):
    try:
        Now = datetime.datetime.now()
        f_taskH = TaskHistoryDB.find_one({'_id': ObjectId(taskH_id)})
        TaskHistoryDB.update_one({'_id': ObjectId(taskH_id)},
                                        {'$set': 
                                            {'Status':'done',
                                            'EndDate': Now,
                                            'Time': str(Now - f_taskH['StartDate'] - f_taskH['RestTime'])}# 수정 필요
                                        })
        return ''
    except :
        traceback.print_exc()
        return '', 500

# Timer 업무 전환
@app.route('/widget/taskhistory/timer/switch/<taskH_id>', methods=['PATCH'])
async def timer_switch(taskH_id):
    try:
        Now = datetime.datetime.now()
        f_taskH = TaskHistoryDB.find_one({'_id': ObjectId(taskH_id)})
        

        TaskHistoryDB.update_one({'_id': ObjectId(taskH_id)},
                                {'$set': 
                                    {'Status':'pause',
                                        'Time': str(Now - f_taskH['StartDate'] - f_taskH['RestTime']),
                                        'TmpDate': Now}
                                })
        return ''
    except:
        traceback.print_exc()
        return '', 500 




















































''' # Timer
@app.route('/widget/taskhistory/timer/<state>/<taskid>', methods=['PATCH'])
# @jwt_require
# async def Timer(state, taskid, UserId):
async def Timer(state, taskid):
    try:
        Now = datetime.datetime.now()
        f_taskH = TaskHistoryDB.find_one({'_id': ObjectId(taskid)})
        
        if f_taskH is not None:
            # 시작
            if int(state) == 1: 
                TaskHistoryDB.update_one({'_id': ObjectId(taskid)},
                                         {'$set': 
                                               {'Status':'working',
                                                'StartDate': Now}
                                        })
           
            # 멈춤
            elif int(state) == 2:
                TaskHistoryDB.update_one({'_id': ObjectId(taskid)},
                                        {'$set': 
                                            {'Status':'pause',
                                                'Description':'', #필수? 선택? 멈추기할 경우 None값이라도 와야함
                                                'TmpDate': Now}
                                        })
                
            # 재시작
            elif int(state) == 3:
                TaskHistoryDB.update_one({'_id': ObjectId(taskid)},
                                        {'$set': 
                                            {'Status':'working',
                                             'RestTime': str(Now - f_taskH['TmpDate'])}
                                        })
                
            # 종료
            elif int(state) == 4:
                print(f_taskH['EndDate'])
                print(f_taskH['StartDate'])
                TaskHistoryDB.update_one({'_id': ObjectId(taskid)},
                                        {'$set': 
                                            {'Status':'done',
                                            'EndDate': Now,
                                            'Time': str(Now - f_taskH['StartDate'])}
                                        }),,,,,,
                
            else:
                return dumps({'msg': '찾을 수 없는 TaskHistory'}), 400
            return ''
        else:
            return '',400
    except :
        traceback.print_exc()
        return '', 500 '''