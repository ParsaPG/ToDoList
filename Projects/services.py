from .models import Project
from utils.exceptions import NotFoundError, LimitError
from .storage import InMemoryStorage
import os

MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))

"""
    Project service.
"""

class ProjectService:
    def __init__(self, storage: InMemoryStorage):
        self.db = storage

    def add(self, name: str, desc: str):
        """
        Add a new project.
        """
        if len(self.db.projects) >= MAX_PROJECTS:
            raise LimitError("Max number of project reached.")
        if any(p.name == name for p in self.db.projects.values()):
            raise ValueError("Duplicate project name.")
        
        pid = self.db.next_project_id
        self.db.projects[pid] = Project(pid, name, desc)
        self.db.next_project_id += 1
        return self.db.projects[pid]

    def edit(self, pid: int, name: str, desc: str):
        """
        Edit a project.
        """
        project = self.db.projects.get(pid)
        if not project:
            raise NotFoundError("Project not found.")
        project.name = name
        project.description = desc
        return project

    def delete(self, pid: int):
        """
        Delete a project.
        """
        if pid not in self.db.projects:
            raise NotFoundError("Project not found.")
        del self.db.projects[pid]

    def list(self):
        """
        List all projects.
        """
        return list(self.db.projects.values())