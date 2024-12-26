from fastapi import APIRouter, HTTPException
from app.models.todo import Todo
from app.database import db
from bson import ObjectId

router = APIRouter()

@router.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    todo_dict = todo.dict()
    result = db.todos.insert_one(todo_dict)
    todo_dict["_id"] = str(result.inserted_id)
    return todo_dict

@router.get("/todos")
def read_todos():
    todos = list(db.todos.find())
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return todos

@router.get("/todos/{id}", response_model=Todo)
def read_todo(id: str):
    todo = db.todos.find_one({"_id": ObjectId(id)})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo["_id"] = str(todo["_id"])
    return todo

@router.put("/todos/{id}", response_model=Todo)
def update_todo(id: str, todo: Todo):
    result = db.todos.update_one({"_id": ObjectId(id)}, {"$set": todo.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/todos/{id}")
def delete_todo(id: str):
    result = db.todos.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}
