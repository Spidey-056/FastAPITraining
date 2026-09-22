from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"Page": "Home"}

print("Second Line")



@app.get("/about")
def about():
    return {"page":"About","author":"Ashutosh"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/create")
def create_something():
    return {"Message":"Created"}

@app.get("/students/{usn}")
def get_result(usn):
    return {"Result ":"Distinction","usn":usn}

