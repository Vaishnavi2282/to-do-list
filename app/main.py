from fastapi import FastAPI, Depends, HTTPException, status, Query, Body
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId

from models import User, TodoCreate, TodoUpdate, TodoInResponse
from schemas import UserCreate, UserLogin, Token, UserInProfile
from utils import verify_password, get_password_hash, create_access_token, decode_access_token
from database import users_collection, todos_collection

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# User Signup
@app.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    hashed_password = get_password_hash(user.password)
    user_data = User(username=user.username, email=user.email, hashed_password=hashed_password)
    users_collection.insert_one(user_data.dict())
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# User Login
@app.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = users_collection.find_one({"username": user.username})
    if db_user is None or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# User Profile
@app.get("/profile", response_model=UserInProfile)
async def get_profile(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    db_user = users_collection.find_one({"username": payload["sub"]})
    return UserInProfile(username=db_user["username"], full_name=db_user.get("full_name"), email=db_user["email"])

# Create Todo
@app.post("/todos", response_model=TodoInResponse)
async def create_todo(todo: TodoCreate, token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    todo_data = todo.dict()
    todo_data["user"] = payload["sub"]
    todos_collection.insert_one(todo_data)
    
    return {**todo_data, "id": str(todo_data["_id"])}

# Read Todos
@app.get("/todos", response_model=List[TodoInResponse])
async def get_todos(token: str = Depends(oauth2_scheme), category: Optional[str] = None):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    filter_criteria = {"user": payload["sub"]}
    if category:
        filter_criteria["category"] = category
    
    todos = list(todos_collection.find(filter_criteria))
    return [{"id": str(todo["_id"]), **todo} for todo in todos]

# Update Todo
@app.put("/todos/{todo_id}", response_model=TodoInResponse)
async def update_todo(todo_id: str, todo: TodoUpdate, token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    todo_data = {k: v for k, v in todo.dict(exclude_unset=True).items()}
    result = todos_collection.update_one({"_id": ObjectId(todo_id), "user": payload["sub"]}, {"$set": todo_data})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    updated_todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    return {**updated_todo, "id": str(updated_todo["_id"])}

# Delete Todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    result = todos_collection.delete_one({"_id": ObjectId(todo_id), "user": payload["sub"]})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    return {"message": "Todo deleted successfully"}

# Mark Todo as Complete/Incomplete
@app.patch("/todos/{todo_id}/complete")
async def mark_complete(todo_id: str, token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    result = todos_collection.update_one(
        {"_id": ObjectId(todo_id), "user": payload["sub"]},
        {"$set": {"is_complete": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    return {"message": "Todo marked as complete"}
