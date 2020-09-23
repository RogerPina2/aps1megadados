from fastapi import APIRouter, HTTPException, Depends
import uuid
from typing import Optional, Dict

try:
    from api.models import Task
except ImportError:
    from aps1megadados.api.models import Task

try:
    from api.database import get_db, DBSession
except ImportError:
    from aps1megadados.api.database import get_db, DBSession


router = APIRouter()

@router.get(
    '/',
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

@router.post(
    '/',
    summary='Creates a new task',
    description='Creates a new task and returns its UUID.',
    response_model=uuid.UUID,
)
async def create_task(item: Task, db: DBSession = Depends(get_db)):
    uuid_ = uuid.uuid4()
    return db.create_task(uuid_, item)

@router.get(
    '/{uuid_}',
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

@router.put(
    '/{uuid_}',
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

@router.patch(
    '/{uuid_}',
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

@router.delete(
    '/{uuid_}',
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