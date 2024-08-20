from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from curso_fastapi.database import get_session
from curso_fastapi.models import Task, User
from curso_fastapi.schemas import (ListTasks, TaskCreate, TaskFilter, TaskResponse,
                                      TaskUpdate)
from curso_fastapi.security import get_current_user

tasks_router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
)

T_Session = Annotated[Session, Depends(get_session)]
T_Current_User = Annotated[User, Depends(get_current_user)]
T_Filter = Annotated[TaskFilter, Depends()]


@tasks_router.get('/', response_model=ListTasks)
def list_tasks(
    session: T_Session,
    current_user: T_Current_User,
    filters: T_Filter,
):
    query = select(Task).filter(Task.user_id == current_user.id)
    if filters.title:
        query = query.filter(Task.title.contains(filters.title))
    if filters.description:
        query = query.filter(Task.description.contains(filters.description))
    if filters.state:
        query = query.filter(Task.state == filters.state)
    tasks = (
        session.execute(query.offset(filters.offset).limit(filters.limit))
        .scalars()
        .all()
    )

    return {'tasks': tasks}


@tasks_router.post(
    '/', response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate, session: T_Session, current_user: T_Current_User):
    new_task = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        user_id=current_user.id,
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@tasks_router.get('/{task_id}', response_model=TaskResponse)
def get_task(task_id: int, session: T_Session, current_user: T_Current_User):
    task = session.get(Task, task_id)
    if task is None:
        return status.HTTP_404_NOT_FOUND
    if task.user_id != current_user.id:
        return status.HTTP_403_FORBIDDEN

    return task


@tasks_router.patch('/{task_id}', response_model=TaskResponse)
def update_task(
    task_id: int, task: TaskUpdate, session: T_Session, current_user: T_Current_User
):
    db_task = session.get(Task, task_id)
    if db_task is None:
        return status.HTTP_404_NOT_FOUND
    if db_task.user_id != current_user.id:
        return status.HTTP_403_FORBIDDEN

    for field, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    session.commit()
    session.refresh(db_task)

    return db_task


@tasks_router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: T_Session, current_user: T_Current_User):
    task = session.get(Task, task_id)
    if task is None:
        return status.HTTP_404_NOT_FOUND
    if task.user_id != current_user.id:
        return status.HTTP_403_FORBIDDEN

    session.delete(task)
    session.commit()
    return status.HTTP_204_NO_CONTENT
