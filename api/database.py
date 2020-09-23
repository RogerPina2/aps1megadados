import uuid

from .models import Task

class DBSession:
    tasks = {}
    def __init__(self):
        self.tasks = DBSession.tasks

    def read_tasks(self):
        """
            This method returns the task list
        """
        return self.tasks

    def read_completed_tasks(self):
        """
            This method returns the list of completed tasks
        """
        return {
            uuid_: item
            for uuid_, item in self.tasks.items() if item.completed == True
        }

    def read_incompleted_tasks(self):
        """
            This method returns the list of incompleted tasks
        """
        return {
            uuid_: item
            for uuid_, item in self.tasks.items() if item.completed == False
        }

    def create_task(self, uuid_: uuid.UUID, item: Task):
        """
            This method creates a task in db and returns the task uuid
        """
        self.tasks[uuid_] = item
        return uuid_

    def read_task_from_uuid(self, uuid_: uuid.UUID):
        """
            This method returns the task by id
        """
        return self.tasks[uuid_]

    def update_task_from_uuid(self, uuid_: uuid.UUID, item: Task):
        """
            This method updates the task by id
        """
        self.tasks[uuid_] = item

    def update_partial_task_from_uuid(self, uuid_: uuid.UUID, item: Task):
        """
            This method partially updates the task by id
        """
        update_data = item.dict(exclude_unset=True)
        self.tasks[uuid_] = self.tasks[uuid_].copy(update=update_data)

    def delete_task_from_uuid(self, uuid_: uuid.UUID):
        """
            This method deletes the task by id
        """
        del self.tasks[uuid_]

    def contains(self, uuid_: uuid.UUID):
        """
            This method checks if uuid is in the db
        """
        if uuid_ in self.tasks.keys():
            return True
        return False

def get_db():
    return DBSession()