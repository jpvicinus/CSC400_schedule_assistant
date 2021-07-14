import uvicorn
import psycopg2

from fastapi import FastAPI

# CSC400_schedule_assistant

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


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.get("/students")
async def get_students():  # return a list of all students 
    cursor = connection.cursor()
    # go to database and get users 
    cursor.execute("select * from studentlist;")
    result = cursor.fetchone() # shouldnt be fetch one, probably use fetch all 
    # put users into models using pydantic 
    cursor.close()
   # return await student.fetch_all(result)


# TODO 

# # get student by id 
@app.get("/students/{student_id}")
#   #-- return 1 student 
async def get_student_by_id(student_id):
        cursor = connection.cursor()
        student_by_id = f"select * from studentlist where student_id = {student_id}"
        cursor.execute(student_by_id)
        result = cursor.fetchone()
        cursor.close()
        return result
 # get student by last name
@app.get("/students/{last_name}")
async def get_student_last_name(last_name):
        cursor = connection.cursor()
        student_last_name = f"select * from studentlist where last_name = {last_name}"
        cursor.execute(student_last_name)
        result = cursor.fetchone()
        cursor.close()
        return result

# create new student
# @app.post("/students/new_student")   # POST 
# async def create_new_student():
#     cursor = connection.cursor()




# delete user by id 

# update user by id 



if __name__== "__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
