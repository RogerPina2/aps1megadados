from typing import Optional, List

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

taskDB = {
    "taskQuantity": 0,
    "tasks": {}
    }

class Task(BaseModel):
    name: str
    description: str
    complete: bool = False

# rota raiz
@app.get("/")
def read_root():
    return {
        "title":"APS 1",
        "subject": "Megadados",
        "memebers": {
            "Gabriel Zanneti": "gabrielztk@al.insper.edu.br",
            "Roger Pina": "rogerrfp@al.insper.edu.br"
        }
    }


@app.post("/task/")
def create_task(task: Task):    
    taskId = taskDB["taskQuantity"]
    taskDB["tasks"][taskId] = task
    taskDB["taskQuantity"] += 1

    return {"task":task, "taskDB": taskDB}
'''
@app.patch("/task/{taskId}")
def update_taskDescription(
    taskId: int = Path(..., title="The ID of the task to get", ge=0, lt= taskDB["taskQuantity"]),
    description: str = Query(..., title="New description to the task got")
):
    results = {"taskId": taskId}
    if description:
        results.update({"description": description})
    return results
'''
'''
@app.patch("/task/{taskId}", response_model=Task)
def update_task(taskId: int, task: Task):
    task_data = taskDB["tasks"][taskId]
    task_model = Task(**task_data)
    update_data = task.dict(exclude_unset=True)
    updated_task = task_model.copy(update=update_data)
    taskDB["tasks"][taskId] = jsonable_encoder(updated_task)
    return updated_task
'''
@app.delete("/task/{taskId}")
def remove_task(taskId: int):
    if taskId in taskDB["tasks"]:
        del taskDB["tasks"][taskId]
    return

#Get all tasks
@app.get("/tasks")
def read_tasks():  
    return { "tasks": taskDB["tasks"] }

#Get all complete tasks
@app.get("/tasks/complete")
def read_complete_tasks():
    completeTasks = {}
    for key, task in taskDB["tasks"].items():
        if task.complete == True:
            completeTasks[key] = task
            
    return { "tasks": completeTasks }
 
#Get all incomplete tasks
@app.get("/tasks/incomplete")
def read_incomplete_tasks():
    incompleteTasks = {}
    for key, task in taskDB["tasks"].items():
        if task.complete == False:
            incompleteTasks[key] = task
            
    return { "tasks": incompleteTasks }


