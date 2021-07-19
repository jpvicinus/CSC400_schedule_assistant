from fastapi.param_functions import Query
import uvicorn
import psycopg2
from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
app = FastAPI()

DB_NAME = "student"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    print(f'trying to connect to database... waiting \n\n')
    connection = psycopg2.connect(
        user = DB_USER,
        password = DB_PASS,
        host = DB_HOST,
        port = DB_PORT,
        database = DB_NAME
    )
except Exception as err:
    print(f'\n\ndone fucked up making database connection \n\n[{err}]\n\n')

#base case
@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


#show list of all classes
@app.get("/class")
async def get_class():  # return a list of all classes
    cursor = connection.cursor()
    # go to database and get classes 
    get_classes = "select * from classinfo;"
    cursor.execute(get_classes)
    result = cursor.fetchall()  
    # put classes into models using pydantic 
    cursor.close()
    return  (result)

#get class by id
@app.get("/class/id/{class_id}")
async def get_class_by_id(class_id):
    cursor = connection.cursor()
    class_by_id = f"select * from classinfo where class_id = {class_id}"
    cursor.execute(class_by_id)
    result = cursor.fetchone()
    cursor.close()
    return result

#get class list by subject
@app.get('/class/subject/{class_subject}')
async def get_class_by_subject(class_subject):
    cursor = connection.cursor()
    class_by_sub = f"select * from classinfo where class_subject = '{class_subject}'"
    cursor.execute(class_by_sub)
    result = cursor.fetchall()
    cursor.close()
    return result

#get class list by grade
@app.get('/class/grade/{class_grade}')
async def get_class_by_grade(class_grade):
    cursor = connection.cursor()
    class_by_grade = f"select * from classinfo where class_grade = {class_grade}"
    cursor.execute(class_by_grade)
    result = cursor.fetchall()
    cursor.close()
    return result

#get class list by name
@app.get('/class/name/{class_name}')
async def get_class_by_name(class_name):
    cursor = connection.cursor()
    class_by_name = f"select * from classinfo where class_name = '{class_name}'"
    cursor.execute(class_by_name)
    result = cursor.fetchall()
    cursor.close()
    return result

#delete class by id
@app.delete("/class/delete/id/{class_id}")
async def delete_class_by_id(class_id):
    cursor = connection.cursor()
    delete_class = f"delete from classinfo where class_id = '{class_id}'"
    cursor.execute(delete_class)
    #result = cursor.fetchone()
    cursor.close()
    return "done"

#show list of all students
@app.get("/students")
async def get_students():  # return a list of all students 
    cursor = connection.cursor()
    # go to database and get users 
    get_students = "select * from studentlist;"
    cursor.execute(get_students)
    result = cursor.fetchall()  
    # put users into models using pydantic 
    cursor.close()
    return  (result)

# get student by id 
@app.get("/students/{student_id}")
async def get_student_by_id(student_id):
    cursor = connection.cursor()
    student_by_id = f"select * from studentlist where student_id = {student_id}"
    cursor.execute(student_by_id)
    result = cursor.fetchone()
    cursor.close()
    return result
    

 # get student by last name
@app.get("/students/lastname/{last_name}")
async def get_student_last_name(last_name):
    cursor = connection.cursor()
    student_last_name = f"select * from studentlist where last_name = '{last_name}'"
    cursor.execute(student_last_name)
    result = cursor.fetchall()
    cursor.close()
    return result

# delete user by id 
@app.delete("/students/delete/{student_id}")
async def delete_student_by_id(student_id):
    cursor = connection.cursor()
    delete_student = f"delete from studentlist where student_id = '{student_id}'"
    cursor.execute(delete_student)
    #result = cursor.fetchone()
    cursor.close()
    return "done"

# # create new student
# class newstudent(BaseModel):
#     first_name: str
#     last_name: str
#     student_id: float
#     student_grade: float


# @app.post("/students/newStudent")   # POST 
#  #POST take body - get data through body not url parameters
# async def new_student(request:newstudent):
#     return {'record':f'New record is created with {request.name}'

# @app.put("/students/new",function (Request))
# async def getstudent():
#     str "first_name"      = Request.body.first_name;
#     str "last_name"       = Request.body.last_name;
#     float "student_id"    = Request.body.student_id;
#     float student_grade   = Request.body.student_grade;


# @app.post("/students/newstudent")
# async def new_student(first_name:str,last_name:str,student_id:float,student_grade:float,newStudent:newstudent,q,):
#     cursor = connection.cursor()
#    # add_new = f"insert into studentlist(first_name,last_name,student_id,student_grade) values('{first_name}''{last_name}''{student_id}''{student_grade}')"
#     cursor.execute()
#     cursor.close()

# @app.post('/students/newstudent',response_model=studentlist)
# async def register_student(st: newstudent):
#     query = student.insert().values(
#         sfirst_name = first_name,
#         slast_name = last_name,
#         stu_id = student_id,
#         sgrade = student_grade
#     )
#     await db.execute(query)
#     return {"message":"Successfully registered !","created": True}

    
# update user by id 



#add a new class

#update class



if __name__== "__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
