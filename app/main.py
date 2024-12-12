from typing import Optional, List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.Function import mode 
from . import models,schemas,utils
from .database import engine,get_db





models .Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
try:
    conn = psycopg2. connect(host ='localhost',database= 'fastapi',user='fastapi',password='newpassword', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was succesfull !")
except Exception as error:
        print("Connecting to database failed")
        print("error:", error)


# In-memory data store
my_posts = [
    {"title": "Title of Post 1", "content": "Content of Post 1", "id": 1},
    {"title": "Favorite Foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


# Root endpoint
@app.get("/")
def root():
    return {"message": "Hello World"}
 

