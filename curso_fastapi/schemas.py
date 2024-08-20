from datetime import datetime

from pydantic import BaseModel, EmailStr

from curso_fastapi.models import TaskState


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserList(BaseModel):
    users: list[UserResponse] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TaskCreate(BaseModel):
    title: str
    description: str
    state: TaskState


class TaskResponse(TaskCreate):
    id: int


class ListTasks(BaseModel):
    tasks: list[TaskResponse] = []


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None


class TaskFilter(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None
    offset: int = 0
    limit: int = 10
