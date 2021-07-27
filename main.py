from fastapi.param_functions import Query
from starlette.routing import request_response
import uvicorn
import psycopg2
from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from uuid import UUID



AVAILABLE_SUBJECTS_9 = [
    "Math",
    "Science",
    "History",
    "English",
    "Foreign Language",
    "Performing Arts",
    "Visual Arts",
    "Physical Education",
    "CSIT",
    "FACS",
    "AP"
    
]
AVAILABLE_SUBJECTS_10 = [
    "Math",
    "Science",
    "History",
    "English",
    "Foreign Language",
    "Performing Arts",
    "Visual Arts",
    "Physical Education",
    "CSIT",
    "FACS",
    "AP"
    
]
AVAILABLE_SUBJECTS_11 = [
    "Math",
    "Science",
    "History",
    "English",
    "Foreign Language",
    "Performing Arts",
    "Visual Arts",
    "Physical Education",
    "CSIT",
    "FACS",
    "AP"
    
]
AVAILABLE_SUBJECTS_12 = [
    "Math",
    "Science",
    "History",
    "English",
    "Foreign Language",
    "Performing Arts",
    "Visual Arts",
    "Physical Education",
    "CSIT",
    "FACS",
    "AP"
    
]

def validate_subject(grade: int, subject: str):
    if grade == 9:
        if subject not in AVAILABLE_SUBJECTS_9:
            raise HTTPException(status_code=400, detail=f"Subject {subject} not available for grade {grade}")

    elif grade == 10:
        if subject not in AVAILABLE_SUBJECTS_10:
            raise HTTPException(status_code=400, detail=f"Subject {subject} not available for grade {grade}")

    elif grade == 11:
        if subject not in AVAILABLE_SUBJECTS_11:
            raise HTTPException(status_code=400, detail=f"Subject {subject} not available for grade {grade}")

    elif grade == 12:
        if subject not in AVAILABLE_SUBJECTS_12:
            raise HTTPException(status_code=400, detail=f"Subject {subject} not available for grade {grade}")

def validate_grade(grade: int):
    if grade < 9 or grade > 12:
        raise HTTPException(status_code=400, detail=f"Grade {grade} must be between 9 and 12")


def get_student_count(student_grade:int):
    cursor = connection.cursor()
    student_count = f"select count (*) from studentlist where student_grade = {student_grade}"
    cursor.execute(student_count)
    result = cursor.fetchall()
    cursor.close()
    return
def get_class_count(class_subject:int):
    cursor = connection.cursor()
    class_count = f"select count (*) from classinfo where class_subject = {class_subject}"
    cursor.execute(class_count)
    result = cursor.fetchall()
    cursor.close()
    return



app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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


#show list of all students
@app.get("/students")
async def get_students():   
    cursor = connection.cursor()
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
async def get_student_last_name(last_name: str):
    cursor = connection.cursor()
    student_last_name = f"select * from studentlist where last_name = '{last_name}'"
    cursor.execute(student_last_name)
    result = cursor.fetchall()
    cursor.close()
    return result

# delete user by id 
@app.delete("/students/delete/{student_id}")
async def delete_student_by_id(student_id: int) -> str:
    cursor = connection.cursor()
    delete_student = f"delete from studentlist where student_id = '{student_id}'"
    cursor.execute(delete_student)
    connection.commit()
    cursor.close()
    return "done"

# class for new student
class Newstudent(BaseModel):
    first_name: str
    last_name: str
    student_id: int
    student_grade: int


 #create new student   
@app.post("/students")    
async def new_student(student:Newstudent):
    cursor = connection.cursor()
    first_name = student.first_name
    last_name = student.last_name
    student_id = student.student_id
    student_grade = student.student_grade
    add_new = f"insert into studentlist(first_name,last_name,student_id,student_grade) values('{first_name}','{last_name}','{student_id}','{student_grade}')"
    validate_grade(student_grade)
    cursor.execute(add_new)
    connection.commit()
    cursor.close()
    return student

#update student by id
@app.put("/students/{student_id}")
async def update_student(student_id: int, update: Newstudent):
    cursor = connection.cursor()
    first_name = update.first_name
    last_name = update.last_name
    student_id = update.student_id
    student_grade = update.student_grade
    add_new = f"update studentlist set first_name = '{first_name}',last_name = '{last_name}',student_id = {student_id},student_grade = {student_grade} where student_id={student_id}"
    validate_grade(student_grade)
    cursor.execute(add_new)
    cursor.close()
    return update


#get student count by grade
@app.get("/students/count/{student_grade}")
async def get_student_count(student_grade:int):
    cursor = connection.cursor()
    student_count = f"select count (*) from studentlist where student_grade = {student_grade}"
    cursor.execute(student_count)
    result = cursor.fetchall()
    cursor.close()
    return result


#-------------------------------------------------------------------
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

#delete class by id
@app.delete("/class/delete/id/{class_id}")
async def delete_class_by_id(class_id):
    cursor = connection.cursor()
    delete_class = f"delete from classinfo where class_id = '{class_id}'"
    cursor.execute(delete_class)
    connection.commit()
    cursor.close()
    return "done"


#class for new and update clas
class Group(BaseModel):
    class_name: str
    class_grade: int
    class_subject: str
    class_size: int
    class_id: int
    max_students: int


#update class by id
@app.put("/class/{class_id}")
async def update_class(class_id: int, updatec: Group):
    cursor = connection.cursor()
    class_name = updatec.class_name
    class_grade = updatec.class_grade
    class_subject = updatec.class_subject
    class_size = updatec.class_size
    class_id = updatec.class_id
    updateclass = f"update classinfo set class_name ='{class_name}' , class_grade = {class_grade} , class_subject = '{class_subject}' , class_size = {class_size},class_id = {class_id} where class_id={class_id}"
    validate_grade(class_grade)
    validate_subject(class_grade,class_subject)
    cursor.execute(updateclass)
    cursor.close()
    return updatec

#make class and add students
@app.post("/class/new")    
async def new_class(new_group:Group):
    #define inputs
    cursor = connection.cursor()
    class_name = new_group.class_name
    class_grade = new_group.class_grade
    class_subject = new_group.class_subject
    class_size = new_group.class_size
    max_students = new_group.max_students
    #define how to make new class
  #######  new_class = f"insert into classinfo(class_name,class_grade,class_subject,class_size,class_id) values('{class_name}' , '{class_grade}' , '{class_subject}' , '{class_size}' ,{}"
   #validation of grade and subject
    validate_grade(class_grade)
    validate_subject(class_grade,class_subject)
    #read inputs for new class
    #count number of students in grade relating to class
    student_count = f"select count (*) from studentlist where student_grade = {class_grade}"
    cursor.execute(student_count)
    #determine how many of this class you need to create
    num_classes = ()
    if class_size<max_students:
        num_classes = max_students / class_size
    i = 0
    while i < num_classes:
        (cursor.execute (new_class))
        i = i + 1

    #commit to create
    connection.commit()
   
    result = cursor.fetchall()
    cursor.close()
    #return new class/es,num of students in grade, num of classes needed/made
    return new_group,"num of students in grade:{result}","number of classes needed:{num_classes}"







if __name__== "__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
