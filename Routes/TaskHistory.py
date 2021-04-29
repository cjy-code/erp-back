from run import app ,dumps, json, request, departmentDB, userDB, TaskDB, datetime, TaskHistoryDB, ObjectId, time, Resource, traceback, pd

@app.route('/taskhistory/<userId>/<taskId>')
class TaskHistorsfady(Resource):
    #@jwt_require
    async def post(self,userId, taskId):
        try:
            if taskId is not None or taskId is not '':
            
                TaskHistoryDB.insert_one({
                'StartDate': None,
                'EndDate': None,
                'TmpDate': None,
                'Time': None,
                'Status': 'working',
                'Task': ObjectId(taskId),
                'Description' : None,
                'User': ObjectId(userId),
                'RestTime': None
                })
                return '', 200
            return '', 401
        except:
            traceback.print_exc()
            return '', 402

@app.route('/taskhistory/delete', method)
async def delete(self, userId, taskId):
    try:
        find_taskH = TaskHistoryDB.find_one({'_id': ObjectId(taskId)})
        
        if find_taskH is None and find_taskH is '':
            return '', 400
        else:
            TaskHistoryDB.delete_one({
                '_id': ObjectId(taskId)
            })
            return '', 200
        return '' ,401
    except:
        traceback.print_exc()
        return '', 403
            
    async def get(self, userId, taskId):
        try:
            return '', 200
        except :
            traceback.print_exc()
            return '', 401



"""     async def petch(self, userId, taskId):
        Data = await request.get_json()
        try:
            #################################
            req_start = datetime.datetime.now()
            req_stat = None
            #################################
            # if req_start is None and req_time is '':
            #     return '', 400
            # if req_stat is None and req_stat is '':
            #     return '', 400
            # if req_time is None and req_time is '':
            #    req_time = None      
            # if req_tmp is None and req_tmp is '':
            #    req_tmp = None
            # if req_end is None and req_end is '':
            #    req_end = None    

            

            # TaskHistoryDB.update_one({
            #         '_id': ObjectId(taskId)
            #     },
            #         {'$set': {
            #             'StartDate': req_start,
            #             'EndDate': req_end,
            #             'TmpDate': req_tmp,
            #             'Time': req_time,
            #             'Status': req_stat,
            #             'Task': ObjectId(taskId),
            #             'User': ObjectId(userId),
            #             'RestTime': req_time
            # }})

            tasks_find = TaskHistoryDB.find_one({'_id':taskId})

            return dumps(tasks_find), 202
        except:
            traceback.print_exc()
        return '', 401 """