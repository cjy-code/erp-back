from run import app ,dumps, json, request, departmentDB, userDB, TaskDB, datetime, TaskHistoryDB, ObjectId, time, Resource, traceback
from Except.Exception import TasksAdd

@app.route('/task')
class Tasks(Resource):
    # Tasks List
    async def get(self):
        try:
            req_list = TaskDB.find({})
            print(datetime.datetime.now())
            print(datetime.time())
            print(datetime.date(2021, 4, 15))
            if req_list is None or req_list == '':
                return '', 400
            return dumps({req_list}), 200
        except :
            traceback.print_exc()
    
    # Tasks 생성
    async def post(self):
        try:
            Data = await request.get_json()
            req_task= Data['taskname']
            
            if req_task is None and req_task == '':
                return '', 400        
            # for result in range(1,100):

            TaskDB.insert_one({
                'Name': req_task
            }) 
            return '', 201  
        except:
            traceback.print_exc()
        return '', 401
    
    
      
@app.route('/task/<taskId>')
class tasksEdit(Resource):
    async def patch(self, taskId):
        Data = await request.get_json()
        try:
            find_task = TaskDB.find_one({'_id': ObjectId(taskId)})
            if find_task is None or Data['Name'] is None or Data['Name'] is '':
                return '', 401
            else:    
                req_name = Data['Name']
                
                TaskDB.update_one({
                    '_id': ObjectId(taskId)
                },
                {'$set':{'Name': req_name}})
                return '', 200
            return '', 402
        except:
            traceback.print_exc()
            return '', 403
    
    async def delete(self, taskId):
        try:
            find_task = TaskDB.find_one({'_id': ObjectId(taskId)})
            if find_task is None:
                return '', 401
            else:
                if taskId is None or taskId == '':
                    return '', 402
                else:
                    TaskDB.delete_one({
                        '_id' : ObjectId(taskId)
                    })
                    return '' , 200
                return '', 403
        except:
            traceback.print_exc()
        return '', 406
    