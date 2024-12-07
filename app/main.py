from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from httpx import post
from pydantic import BaseModel
from random import randrange
import psycopg2
import psycopg2.extras import RealDictCursor # type: ignore

app = FastAPI()

# Data model for a post
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

# Get all posts
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECY * FROM posts""")
    Post = cursor.fetchall
    print("data":posts) 

    return {"data": my_posts}

# Create a new post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content,published) VALUES (%S,%S,%S) RETURNING * """,(post.title,post.content,post.published))
    NEW_POST = cursor.fetchone()
    return {"data": new_post}

  

# Get a specific post by ID
@app.get("/posts/{id}")
def get_post(id: int ,responce :Response):

    post = find_post(id)
    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")

    return{"post_detail":post}
 

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    #find the index in the array that has required id 
    #my_posts.pop(index)
     index = find_index_post(id)

     if index == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} dose not exist")
     my_posts.pop(index)
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}")
def update_post(id:int,post:Post):
       index = find_index_post(id)

       if index == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} dose not exist")
       post_dict= post.dict()
       my_posts[index]= post_dict
       post_dict['id']=id
       return{"data": post_dict}