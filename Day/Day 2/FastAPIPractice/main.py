from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"Page": "Home"}

@app.get("/about")
def about():
    return {"page":"About","author":"Ashutosh"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/create")
def create_something():
    return {"Message":"Created"}

#Path Parameters
@app.get("/students/{usn}")
def get_result(usn):
    return {"Result ":"Distinction","usn":usn}

#Path Parameters with Type Hint
@app.get("/candidate/{rollno}")
def get_result(rollno : int):
    return {"Result ":"Distinction","rollno":rollno,"type":str(type(rollno))}

