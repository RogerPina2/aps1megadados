from typing import Optional, List
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations with tasks.",
    },
    {
        "name": "filter",
        "description": "Operations that filter a data base item by some parameter.",
    },
    {
        "name": "create",
        "description": "Operations that create a data base item.",
    },
    {
        "name": "update",
        "description": "Operations that modify a data base item.",
    },
    {
        "name": "delete",
        "description": "Operations that delete a data base item.",
    },
]

app = FastAPI(
    title="APS1 MEGADADOS",
    description="This is a very fancy MEGADADOS project, with auto docs for the API and everything",
    version="1.0.0",
    openapi_tags=tags_metadata
)

taskDB = {
    "taskQuantity": 0,
    "tasks": {}
    }

class Task(BaseModel):
    name: str
    description: str
    complete: bool = False

# Root route project
@app.get("/")
def read_root():
    """
        This function returns some informations about the project and members.
    """
    return {
        "title":"APS 1",
        "subject": "Megadados",
        "members": {
            "Gabriel Zanneti": {
                "email":"gabrielztk@al.insper.edu.br",
                "github":"gabrielztk"
                },
            "Roger Pina": { 
                "email": "rogerrfp@al.insper.edu.br", 
                "github": "RogerPina2"
                }
        }
    }

# List all tasks
@app.get("/tasks/", tags=["tasks"])
def read_tasks():
    """
        This function lists all tasks in the database taskDB.
    """
    return { "tasks": taskDB["tasks"] }

# List all complete tasks
@app.get("/tasks/complete", tags=["tasks", "filter"])
def read_complete_tasks():
    """
        This function lists all tasks in the database taskDB that are complete.
    """
    completeTasks = {}
    for key, stored_task in taskDB["tasks"].items():
        task = Task(**stored_task)
        if task.complete == True:
            completeTasks[key] = task
            
    return { "tasks": completeTasks }
 
# List all incomplete tasks
@app.get("/tasks/incomplete", tags=["tasks", "filter"])
def read_incomplete_tasks():
    """
        This function lists all tasks in the database taskDB that are incomplete.
    """
    incompleteTasks = {}
    for key, stored_task in taskDB["tasks"].items():
        task = Task(**stored_task)
        if task.complete == False:
            incompleteTasks[key] = task
            
    return {"tasks": incompleteTasks }


# Create task
@app.post("/task/", tags=["tasks", "create"])
def create_task(
    task: Task = Body(
        ..., 
        title="New task",
        description="The contents of the new task"
        )
    ):
    """
        This function creates a task with the model of class Task and saves it in database taskDB.
    """
    taskId = taskDB["taskQuantity"]
    taskDB["tasks"][taskId] = task.dict()
    taskDB["taskQuantity"] += 1

    return {"task":task}

# Update task description
@app.patch("/task/{taskId}/description", tags=["tasks", "update"])
def update_taskDescription(
    *,
    taskId: int = Path(
        ..., 
        title="Task ID", 
        description="The ID of the task to get", 
        ge=0
        ), 
    description: str = Query(
        ..., 
        title="Task description", 
        description="The new description of the task"
        )
    ):
    """
        This function updates the description of task by ID.
    """
    if description:
        taskDB["tasks"][taskId]["description"] = description
    return taskDB["tasks"][taskId]


# Update task status
@app.patch("/task/{taskId}/complete", tags=["tasks", "update"])
def update_taskCompletion(
    *,
    taskId: int = Path(
        ..., 
        title="Task ID", 
        description="The ID of the task to get", 
        ge=0
        ), 
    complete: bool = Query(
        ..., 
        title="Task completion", 
        description="The new status of the task"
        )
    ):
    """
        This function updates the status of task by ID.
    """
    if complete:
        taskDB["tasks"][taskId]["complete"] = complete
    return taskDB["tasks"][taskId]

# Delete task by ID
@app.delete("/task/{taskId}", tags=["tasks", "delete"])
def remove_task(
    *,
    taskId: int = Path(
        ..., 
        title="Task ID", 
        description="The ID of the task to get", 
        ge=0
        )
    ):
    """
        This functions deletes the task by ID.
    """
    if taskId in taskDB["tasks"]:
        del taskDB["tasks"][taskId]
    return {"message": "Task deleted"}