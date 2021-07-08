import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def root():
    # go to database and get users 
    # put users into models using pydantic 
    return [{'name': 'jake'}, {'name': 'brandon'}]


if __name__== "__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
# CSC400_schedule_assistant
