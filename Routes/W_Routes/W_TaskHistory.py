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



# TaskHistoryDB ??????
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

# TaskHistoryDB ??????
@app.route('/widget/taskhistory/delete/<taskH_id>', methods=['DELETE'])
async def task_delete(taskH_id):
    try:
        find_TskH = TaskHistoryDB.find_one({'_id': ObjectId(taskH_id)})
        if find_TskH is None:
            return dumps({'err': '???????????? ????????? ????????????.'}), 401

        TaskHistoryDB.delete_one({'_id': ObjectId(taskH_id)})
        return ''
    except :
        traceback.print_exc()
        return '', 500


# TaskHistoryDB ??????
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

# Timer ??????
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

# Timer ??????, ?????????
@app.route('/widget/taskhistory/timer/toogle/<taskH_id>', methods=['PATCH'])
async def timer_toogle(taskH_id):
    try:
        Now = datetime.datetime.now()
        f_taskH = TaskHistoryDB.find_one({'_id': ObjectId(taskH_id)})
        
        # ??????
        if f_taskH['Status'] is 'working':
            TaskHistoryDB.update_one({'_id': ObjectId(taskH_id)},
                                    {'$set': 
                                        {'Status':'pause',
                                         'Time': str(Now - f_taskH['StartDate'] - f_taskH['RestTime']),
                                         'TmpDate': Now}
                                    })
        
        # ?????????
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

# Timer ??????
@app.route('/widget/taskhistory/timer/end/<taskH_id>', methods=['PATCH'])
async def timer_end(taskH_id):
    try:
        Now = datetime.datetime.now()
        f_taskH = TaskHistoryDB.find_one({'_id': ObjectId(taskH_id)})
        TaskHistoryDB.update_one({'_id': ObjectId(taskH_id)},
                                        {'$set': 
                                            {'Status':'done',
                                            'EndDate': Now,
                                            'Time': str(Now - f_taskH['StartDate'] - f_taskH['RestTime'])}# ?????? ??????
                                        })
        return ''
    except :
        traceback.print_exc()
        return '', 500

# Timer ?????? ??????
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
            # ??????
            if int(state) == 1: 
                TaskHistoryDB.update_one({'_id': ObjectId(taskid)},
                                         {'$set': 
                                               {'Status':'working',
                                                'StartDate': Now}
                                        })
           
            # ??????
            elif int(state) == 2:
                TaskHistoryDB.update_one({'_id': ObjectId(taskid)},
                                        {'$set': 
                                            {'Status':'pause',
                                                'Description':'', #??????? ??????? ???????????? ?????? None???????????? ?????????
                                                'TmpDate': Now}
                                        })
                
            # ?????????
            elif int(state) == 3:
                TaskHistoryDB.update_one({'_id': ObjectId(taskid)},
                                        {'$set': 
                                            {'Status':'working',
                                             'RestTime': str(Now - f_taskH['TmpDate'])}
                                        })
                
            # ??????
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
                return dumps({'msg': '?????? ??? ?????? TaskHistory'}), 400
            return ''
        else:
            return '',400
    except :
        traceback.print_exc()
        return '', 500 '''