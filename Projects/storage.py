# core/storage.py
from typing import Dict
from .models import Project
"""
    In-memory storage for projects.
"""
class InMemoryStorage:
    def __init__(self):
        self.projects: Dict[int, Project] = {}
        self.next_project_id = 1

    def clear(self):
        """
        Clear all stored projects.
        """
        self.projects.clear()
        self.next_project_id = 1