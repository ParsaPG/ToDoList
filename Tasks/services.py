from .models import Task
from utils.exceptions import NotFoundError, LimitError
from .storage import InMemoryStorage
from Projects.storage import InMemoryStorage as InMemoryStorageProjects
import os

MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASK", 20))

"""
    Project service.
"""

class TaskService:
    def __init__(self, storage: InMemoryStorage, projects_storage: InMemoryStorageProjects):
        self.db = storage
        self.db_projects = projects_storage

    def add(self, pid: int, title: str, desc: str, deadline=None, status="todo"):
        """
        Add a new task to a project.
        """
        project = self.db_projects.projects.get(pid)
        if not project:
            raise NotFoundError("Project not found.")
        
        if len(project.tasks) >= MAX_TASKS:
            raise LimitError("Max number of task reached.")
        task = Task(self.db.next_task_id, title, desc, pid, status, deadline)
        project.tasks.append(task)
        self.db.next_task_id += 1
        return task

    def edit(self, pid: int, tid: int, **kwargs):
        """
        Edit a task within a project.
        """
        project = self.db_projects.projects.get(pid)
        if not project:
            raise NotFoundError("Project not found.")
        task = next((t for t in project.tasks if t.id == tid), None)
        if not task:
            raise NotFoundError("Task not found.")
        for k, v in kwargs.items():
            if hasattr(task, k):
                setattr(task, k, v)
        return task

    def delete(self, pid: int, tid: int):
        """
        Delete a task from a project.
        """
        project = self.db_projects.projects.get(pid)
        if not project:
            raise NotFoundError("Project not found.")
        project.tasks = [t for t in project.tasks if t.id != tid]
        del self.db.tasks[tid]

    def list(self, pid: int):
        """
        List all tasks for a project.
        """
        project = self.db_projects.projects.get(pid)
        if not project:
            raise NotFoundError("Project not found.")
        return project.tasks