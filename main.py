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
    taskDB["tasks"][taskId] = task.dict()
    taskDB["taskQuantity"] += 1

    return {"task":task, "taskDB": taskDB}

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
    for key, stored_task in taskDB["tasks"].items():
        task = Task(**stored_task)
        if task.complete == True:
            completeTasks[key] = task
            
    return { "tasks": completeTasks }
 
#Get all incomplete tasks
@app.get("/tasks/incomplete")
def read_incomplete_tasks():
    incompleteTasks = {}
    for key, stored_task in taskDB["tasks"].items():
        task = Task(**stored_task)
        if task.complete == False:
            incompleteTasks[key] = task
            
    return {"tasks": incompleteTasks }
