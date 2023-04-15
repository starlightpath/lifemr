from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import Database

import secrets
from typing import List
import asyncpg
import time


app = FastAPI()

# CORS Policies
origins = ["http://localhost", "http://localhost:5173/*", "http://localhost:8000/*", "http://127.0.0.1:8000/*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()

class Assignment(BaseModel):
    name: str
    duedate: int
    description: str
    quicklink: str
    weight: int

class LoginUser(BaseModel):
    username: str
    password: str


# Page to add a user
@app.post("/create_user/")
async def add_users(user: LoginUser):
    status = await db.add_user(user.username, user.password)
    return {"status": status}


# Page to get a list of users
@app.get("/users")
async def get_users():
    users = await db.get_users()
    return users

# Page to validate users
@app.post("/validateuser/")
async def validateuser(user: LoginUser):
    status = await db.validate_user(user.username, user.password)
    if(status):
        cryptographic_string = secrets.token_hex(32)
        await db.assignToken(user.username, cryptographic_string, int(time.time()) + 3600)
        return {"status":status,"token":cryptographic_string}
    return {"status":status}

# Page to validate users
@app.post("/validatetoken/")
async def validateuser(user: LoginUser):
    status = await db.validate_token(user.username, user.password, int(time.time()))
    return {"status":status}

@app.get("/")
async def root():
    return {"message": "Hello World"}