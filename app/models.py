from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# User Model
class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    hashed_password: str

# Todo Model
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = "General"
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(1, ge=1, le=5)  # Priority from 1 to 5
    is_complete: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    is_complete: Optional[bool]

class TodoInResponse(TodoBase):
    id: str

    class Config:
        orm_mode = True
