# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import uuid

from typing import Optional, Dict

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field


# pylint: disable=too-few-public-methods
class Task(BaseModel):
    description: Optional[str] = Field(
        'no description',
        title='Task description',
        max_length=1024,
    )
    completed: Optional[bool] = Field(
        False,
        title='Shows whether the task was completed',
    )

    class Config:
        schema_extra = {
            'example': {
                'description': 'Buy baby diapers',
                'completed': False,
            }
        }


tags_metadata = [
    {
        'name': 'task',
        'description': 'Operations related to tasks.',
    },
]

app = FastAPI(
    title='Task list',
    description='Task-list project for the **Megadados** course',
    openapi_tags=tags_metadata,
)

class DBSession:
    tasks = {}
    def __init__(self):
        self.tasks = DBSession.tasks

    def read_tasks(self):
        return self.tasks

    def read_completed_tasks(self):
        return {
            uuid_: item
            for uuid_, item in self.tasks.items() if item.completed == True
        }

    def read_incompleted_tasks(self):
        return {
            uuid_: item
            for uuid_, item in self.tasks.items() if item.completed == False
        }

    def create_task(self, uuid_: uuid.UUID, item: Task):
        self.tasks[uuid_] = item
        return uuid_

    def read_task_from_uuid(self, uuid_: uuid.UUID):
        return self.tasks[uuid_]

    def update_task_from_uuid(self, uuid_: uuid.UUID, item: Task):
        self.tasks[uuid_] = item

    def update_partial_task_from_uuid(self, uuid_: uuid.UUID, item: Task):
        update_data = item.dict(exclude_unset=True)
        self.tasks[uuid_] = self.tasks[uuid_].copy(update=update_data)

    def delete_task_from_uuid(self, uuid_: uuid.UUID):
        del self.tasks[uuid_]

    def contains(self, uuid_: uuid.UUID):
        if uuid_ in self.tasks.keys():
            return True
        return False

def get_db():
    return DBSession()

@app.get(
    '/task',
    tags=['task'],
    summary='Reads task list',
    description='Reads the whole task list.',
    response_model=Dict[uuid.UUID, Task],
)
async def read_tasks(completed: bool = None, db: DBSession = Depends(get_db)):
    if completed is None:
        return db.read_tasks()
    elif completed:
        return db.read_completed_tasks()
    else:
        return db.read_incompleted_tasks()

@app.post(
    '/task',
    tags=['task'],
    summary='Creates a new task',
    description='Creates a new task and returns its UUID.',
    response_model=uuid.UUID,
)
async def create_task(item: Task, db: DBSession = Depends(get_db)):
    uuid_ = uuid.uuid4()
    return db.create_task(uuid_, item)

@app.get(
    '/task/{uuid_}',
    tags=['task'],
    summary='Reads task',
    description='Reads task from UUID.',
    response_model=Task,
)
async def read_task(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        return db.read_task_from_uuid(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception

@app.put(
    '/task/{uuid_}',
    tags=['task'],
    summary='Replaces a task',
    description='Replaces a task identified by its UUID.',
)
async def replace_task(uuid_: uuid.UUID, item: Task, db: DBSession = Depends(get_db)):        
    try: 
        if db.contains(uuid_):
            return db.update_task_from_uuid(uuid_, item)
        else:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from KeyError
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception

@app.patch(
    '/task/{uuid_}',
    tags=['task'],
    summary='Alters task',
    description='Alters a task identified by its UUID',
)
async def alter_task(uuid_: uuid.UUID, item: Task, db: DBSession = Depends(get_db)):
    try:
        if db.contains(uuid_):
            db.update_partial_task_from_uuid(uuid_, item)
        else:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from KeyError
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception

@app.delete(
    '/task/{uuid_}',
    tags=['task'],
    summary='Deletes task',
    description='Deletes a task identified by its UUID',
)
async def remove_task(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        db.delete_task_from_uuid(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception