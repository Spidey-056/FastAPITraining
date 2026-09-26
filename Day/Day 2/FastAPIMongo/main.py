from fastapi import FastAPI
from pymongo import MongoClient
app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["College"]
collection = db["Students"]

@app.get("/")
async def home():
    return {"Message":"FastAPI with MongoDB is running"}

@app.get("/health")
async def health_check():
    result = await db.comment("ping")
    return {"MongoDB connection": "Successful","Ping":result["ok"]}
