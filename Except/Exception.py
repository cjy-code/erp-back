from run import app 

DepartmentAdd = app.create_validator('DepartmentAdd',{
     'type' : 'object',
     'properties' : { 'department' : 'string' } 
     })


TasksAdd = app.create_validator('TaskAdd',{
    'type': 'object',
    'properties' : { 'task': 'string'}
})

# TaskHisotryAdd = app.cteate_validator('TaskHisotryAdd',{
#     'type': 'object',
#     'properties' : { 'taskhistory': 'string'}
# })