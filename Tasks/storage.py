from typing import Dict
from .models import Task
"""
    In-memory storage for tasks.
"""
class InMemoryStorage:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_task_id = 1

    def clear(self):
        """
        Clear all stored tasks.
        """
        self.tasks.clear()
        self.next_task_id = 1