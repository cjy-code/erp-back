from W_Main import app ,dumps, json, session,request, departmentDB, userDB, TaskDB, datetime, TaskHistoryDB, ObjectId, time, Resource, traceback, pd, jwt_require


@app.route('/widget/tasks/get', methods=['GET'])
# @jwt_require
# async def teask_list_get(UserId):
async def teask_list_get():
    try:
        # find_user = userDB.find_one({'_id': ObjectId(UserId)})
        find_user = userDB.find_one({'_id': ObjectId('606d71d2a96b3d38380aed1b')})
        if find_user is None:
            return '', 401
        agg_TaskList = departmentDB.aggregate([
                        {
                        '$match' : {'_id': ObjectId("606fb0585f35166a1fdd41fc") }
                        # '$match' : {'_id': ObjectId(find_user['Department']) }
                        },
                        {
                        '$lookup':{
                                    'from':'Tasks',
                                    'localField': 'TaskList',
                                    'foreignField': '_id',
                                    'as' : 'TaskInfo'
                                } 
                        },
                        {     
                        '$project':{'_id': 0, 'Administor': 0, 'Department': 0, 'TaskList': 0 }
                        }
                        # {
                        #      $project: { TaskInfo: 1 }
                        # }
                        ])
        TL = list(agg_TaskList)
        return dumps(TL[0])
        # return dumps(agg_TaskList)
    except:
        traceback.print_exc()
        return '', 500

