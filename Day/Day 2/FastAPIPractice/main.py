from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hellofunc():
    return {"Message": "Hi, how are you","Number":44,"is_fun":True}

print("Second Line")