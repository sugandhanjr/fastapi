from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from httpx import post
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return{"status": "success"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    Post = cursor.fetchall
    return {"data": post}

# Create a new post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content,published) VALUES (%S,%S,%S) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": get_post}

  

# Get a specific post by ID
@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute(""" SELECT * from posts WHERE id = %s """,(str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")

    return{"post_detail":post}
 

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
   cursor.execute(""" DELETE FROM posts WHERE id = %s returining * """,(str(id),))
   deleted_post = cursor.fetchone()
   if delete_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} dose not exist")
   return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}")
def update_post(id:int,post:Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s,
    WHERE id = %s RETURINING * """,(Post.title,post.content,post.published ,str(id)))
    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} dose not exist")
    
    return{"data": updated_post}