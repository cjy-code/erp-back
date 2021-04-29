from W_Main import app ,dumps, json, session,request, departmentDB, userDB, TaskDB, datetime, TaskHistoryDB, ObjectId, time, Resource, traceback, pd, jwt_require,AttemdanceDB

@app.route('/widget/attendance')
class attendace_widget_main(Resource):
    async def get(self):
    # async def post(self, UserId):
        Now = datetime.datetime.now()  
        Data = await request.get_json()
        try:
            AttemdanceDB.insert_one({
                    'StartDate': Now,
                    'EndDate': None,
                    'Time': None,
                    # 'User': ObjectId(UserId)
                    'User': ObjectId("606d71d2a96b3d38380aed1b")
                })

            find_time = AttemdanceDB.find_one({
                'EndDate': None,
                'User': ObjectId("606d71d2a96b3d38380aed1b")
            })

            return dumps({'TimeOid': find_time['_id'], 'H':0, 'M': 0, 'S': 0}), 205
        except:
            traceback.print_exc()
            return '', 500


    #전체 시간 동기화 GET
    async def post(self):
        Data = await request.get_json()
        Now = datetime.datetime.now()  
        try:
            req_id = Data['id']
            print('test: ',req_id)
            if req_id is None:
                return dumps({'H':0, 'M':0, 'S':0})
            else:
                find_time = AttemdanceDB.find_one({'_id': ObjectId(req_id)})
                start = find_time['StartDate']
                Time = str(Now - start)
                Result = datetime.datetime.strptime(Time.split('.')[0],'%H:%M:%S')
                Sec  = (Result.hour*60*60) + (Result.minute*60) + (Result.second)
                return dumps(Sec)
                # return dumps({'H': Result.hour, 'M':Result.minute, 'S':Result.second}), 200
        except :
            traceback.print_exc()
            return '', 500
                

    # async def patch(self,UserId):
    async def patch(self):
        Data = json.loads(await request.get_data())
        Now = datetime.datetime.now() 
        try:
            find_Atd = AttemdanceDB.find_one({'_id': ObjectId(Data['Atdid'])})
            if find_Atd is 'None':
                return '', 401
            AttemdanceDB.update_one({'_id': ObjectId(Data['Atdid'])},
                                        {'$set':
                                            {'EndDate': Now,
                                             'Time': str(Now - find_Atd['StartDate'])}
                                        })
            return ''
        except :
            traceback.print_exc()
            return '', 500
