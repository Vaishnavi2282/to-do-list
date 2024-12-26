from fastapi import FastAPI
from app.routers import user, todo

app = FastAPI()

app.include_router(user.router)
app.include_router(todo.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo List API"}
